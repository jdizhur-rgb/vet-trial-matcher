#!/usr/bin/env python3
import concurrent.futures as cf
import hashlib
import json
import mimetypes
import re
import time
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote

import httpx
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RAW = RUN / "raw-current-proxy"
RAW.mkdir(exist_ok=True)
INV = json.loads((ROOT / "data/source_inventory.json").read_text())
RESTR = json.loads((ROOT / "data/source_access_restrictions.json").read_text())
UA = "VetTrialFinderDailyAudit/2026-11-24 (+https://vettrialfinder.com/)"
HOST_LOCKS = {}
HOST_LOCKS_GUARD = threading.Lock()

def host_lock(url):
    host = urlsplit(url).netloc.lower()
    with HOST_LOCKS_GUARD:
        return HOST_LOCKS.setdefault(host, threading.BoundedSemaphore(2))

def norm(url):
    p = urlsplit(url.strip())
    path = re.sub(r"/+", "/", unquote(p.path or "/"))
    if path != "/": path = path.rstrip("/")
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ""))

blocked = {}
for row in RESTR.get("routes", []):
    if row.get("do_not_retry") and row.get("url"):
        blocked[norm(row["url"])] = row

def blocked_row(url):
    return blocked.get(norm(url))

def visible_text_and_links(body, ctype, base):
    if "html" not in ctype.lower():
        return "", []
    try:
        class P(HTMLParser):
            def __init__(self):
                super().__init__(); self.skip=0; self.text=[]; self.links=[]; self.href=None; self.anchor=[]
            def handle_starttag(self, tag, attrs):
                if tag in {"script","style","noscript","svg"}: self.skip += 1
                if tag == "a" and not self.skip:
                    self.href=dict(attrs).get("href"); self.anchor=[]
            def handle_endtag(self, tag):
                if tag in {"script","style","noscript","svg"} and self.skip: self.skip -= 1
                if tag == "a" and self.href and not self.skip:
                    self.links.append((self.href," ".join(self.anchor))); self.href=None; self.anchor=[]
            def handle_data(self, data):
                if not self.skip:
                    self.text.append(data)
                    if self.href: self.anchor.append(data)
        p=P(); p.feed(body.decode("utf-8","replace"))
        text = " ".join(" ".join(p.text).split())
        links = []
        for href,anchor in p.links:
            u = urljoin(base, href)
            if u.startswith(("http://", "https://")):
                links.append({"url": u, "text": " ".join(anchor.split())[:300]})
        seen=set(); uniq=[]
        for x in links:
            k=norm(x["url"])
            if k not in seen: seen.add(k); uniq.append(x)
        return text, uniq
    except Exception:
        return "", []

def _one(source_id, role, initial_url, seq):
    stamp = datetime.now(timezone.utc).isoformat()
    br = blocked_row(initial_url)
    if br:
        return {"source_id": source_id, "role": role, "requested_url": initial_url,
                "result": "skipped_exact_restriction", "completed_at": stamp,
                "restriction": br, "opened": False}
    s=httpx.Client(trust_env=True, headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/pdf,application/json;q=0.9,*/*;q=0.5"}, follow_redirects=False, timeout=httpx.Timeout(20,connect=5))
    url=initial_url; redirects=[]; tries=[]
    for hop in range(6):
        br=blocked_row(url)
        if br:
            return {"source_id":source_id,"role":role,"requested_url":initial_url,
                    "result":"redirect_blocked_exact_restriction","completed_at":datetime.now(timezone.utc).isoformat(),
                    "redirects":redirects,"restriction":br,"tries":tries,"opened":False}
        resp=None; err=None
        for attempt in range(2):
            t0=time.monotonic()
            try:
                resp=s.get(url)
                tries.append({"url":url,"attempt":attempt+1,"status":resp.status_code,"elapsed_seconds":round(time.monotonic()-t0,3)})
                transient = resp.status_code==429 or 500 <= resp.status_code < 600
                if transient and attempt==0:
                    delay=min(float(resp.headers.get("Retry-After","0") or 0),2.0)
                    resp.close()
                    if delay: time.sleep(delay)
                    continue
                break
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                err=f"{type(e).__name__}: {e}"[:600]
                tries.append({"url":url,"attempt":attempt+1,"error":err,"elapsed_seconds":round(time.monotonic()-t0,3)})
                if attempt==0: continue
        if resp is None:
            return {"source_id":source_id,"role":role,"requested_url":initial_url,"final_url":url,
                    "result":"transport_error","error":err,"completed_at":datetime.now(timezone.utc).isoformat(),
                    "redirects":redirects,"tries":tries,"opened":True}
        if 300 <= resp.status_code < 400 and resp.headers.get("Location"):
            target=urljoin(url,resp.headers["Location"]); resp.close()
            redirects.append({"from":url,"status":resp.status_code,"to":target})
            url=target; continue
        chunks=[]; size=0; truncated=False
        try:
            for chunk in resp.iter_bytes(65536):
                if not chunk: continue
                if size+len(chunk)>12_000_000:
                    chunks.append(chunk[:12_000_000-size]); truncated=True; break
                chunks.append(chunk); size += len(chunk)
        except Exception as e:
            err=f"body_read_error:{type(e).__name__}:{e}"[:600]
        body=b"".join(chunks); ctype=resp.headers.get("Content-Type","")
        ext=".pdf" if ("pdf" in ctype.lower() or urlsplit(url).path.lower().endswith('.pdf')) else ".bin"
        art=f"{seq:04d}-{hashlib.sha256(initial_url.encode()).hexdigest()[:12]}{ext}"
        (RAW/art).write_bytes(body)
        text,links=visible_text_and_links(body,ctype,url)
        text_sha=hashlib.sha256(text.encode()).hexdigest() if text else None
        result="success" if 200 <= resp.status_code < 300 else "http_error"
        if result=="success" and "html" in ctype.lower() and len(text)<120: result="thin_or_js_shell"
        return {"source_id":source_id,"role":role,"requested_url":initial_url,"final_url":url,
                "status":resp.status_code,"result":result,"completed_at":datetime.now(timezone.utc).isoformat(),
                "content_type":ctype,"bytes":len(body),"body_sha256":hashlib.sha256(body).hexdigest(),
                "visible_text_sha256":text_sha,"visible_text_chars":len(text),"visible_text_excerpt":text[:1200],
                "links":links,"raw_artifact":str((RAW/art).relative_to(ROOT)),"truncated":truncated,
                "redirects":redirects,"tries":tries,"read_error":err,"opened":True}
    return {"source_id":source_id,"role":role,"requested_url":initial_url,"final_url":url,
            "result":"too_many_redirects","completed_at":datetime.now(timezone.utc).isoformat(),
            "redirects":redirects,"tries":tries,"opened":True}

def one(source_id, role, initial_url, seq):
    with host_lock(initial_url):
        return _one(source_id, role, initial_url, seq)

jobs=[]; seq=0
for source in INV["sources"]:
    urls=[("master",source["master_url"])] + [(f"fallback_{i+1}",u) for i,u in enumerate(source.get("fallback_urls") or [])]
    for role,url in urls:
        seq+=1; jobs.append((source["id"],role,url,seq))

rows=[]
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    futs=[ex.submit(one,*j) for j in jobs]
    for f in cf.as_completed(futs):
        try: rows.append(f.result())
        except Exception as e: rows.append({"result":"worker_error","error":repr(e),"completed_at":datetime.now(timezone.utc).isoformat()})
rows.sort(key=lambda x:(x.get("source_id",""),x.get("role",""),x.get("requested_url","")))
out={"run_id":RUN.name,"recorded_at":datetime.now(timezone.utc).isoformat(),"method":"native_proxy_fallback_bounded",
     "limits":{"workers":6,"same_host_max":2,"connect_seconds":5,"total_read_seconds":20,"transient_retry_max":1,"body_cap_bytes":12000000},
     "restriction_count_loaded":len(blocked),"jobs":len(jobs),"attempts":rows}
(RUN/"current-source-proxy-evidence.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
from collections import Counter
print(json.dumps({"jobs":len(jobs),"results":Counter(r.get('result') for r in rows),"sources":len(set(r.get('source_id') for r in rows if r.get('source_id')))},default=dict,ensure_ascii=False))
