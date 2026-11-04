#!/usr/bin/env python3
"""Finite current-source reader for the daily-20261104T030007-0500 audit.

Each job is one permitted official URL. It enforces the saved exact-route holds,
connect/total timeouts, a single transient retry, six global workers and two
concurrent requests per host. It records the actual method and timestamps.
"""
from __future__ import annotations
import hashlib, html, json, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urljoin, urlsplit
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent
RUN=ROOT/"research/audit-runs/daily-20261104T030007-0500"
EVIDENCE=RUN/"evidence"; EVIDENCE.mkdir(parents=True,exist_ok=True)
NY=ZoneInfo("America/New_York")

def now(): return datetime.now(NY).isoformat()
def norm(url):
    p=urlsplit(url)
    return (p.scheme.lower(),p.netloc.lower().removeprefix("www."),p.path.rstrip("/"),tuple(sorted(parse_qsl(p.query))))

inventory=json.loads((RUN/"baseline-source_inventory.json").read_text())["sources"]
restriction_doc=json.loads((RUN/"baseline-source_access_restrictions.json").read_text())
restrictions=list(restriction_doc.get("routes",[]))
for source in inventory: restrictions.extend(source.get("access_restrictions",[]))
blocked={norm(x["url"]):x for x in restrictions if x.get("do_not_retry") and x.get("url")}

domain_locks={}
domain_guard=threading.Lock()
write_guard=threading.Lock()

class VisibleHTML(HTMLParser):
    def __init__(self,base):
        super().__init__();self.base=base;self.depth=0;self.parts=[];self.links=[];self.current=None;self.label=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {"script","style","noscript","svg"}:self.depth+=1
        if tag=="a" and a.get("href"):self.current=urljoin(self.base,a["href"]);self.label=[]
    def handle_endtag(self,tag):
        if tag in {"script","style","noscript","svg"}:self.depth=max(0,self.depth-1)
        if tag=="a" and self.current:
            self.links.append({"text":" ".join(x for x in self.label if x).strip(),"url":self.current})
            self.current=None;self.label=[]
    def handle_data(self,data):
        value=" ".join(data.split())
        if value and not self.depth:self.parts.append(value)
        if value and self.current:self.label.append(value)

def extract(body,ctype,effective):
    if body.startswith(b"%PDF") or "pdf" in ctype.lower():
        tmp=EVIDENCE/("_tmp_"+hashlib.sha256(body).hexdigest()[:16]+".pdf");tmp.write_bytes(body)
        p=subprocess.run(["pdftotext",str(tmp),"-"],capture_output=True,text=True)
        tmp.unlink(missing_ok=True);return p.stdout,[],{"format":"pdf","pdftotext_exit":p.returncode}
    raw=body.decode("utf-8",errors="replace")
    if "json" in ctype.lower() or raw.lstrip().startswith(("{","[")):
        return raw,[],{"format":"json"}
    parser=VisibleHTML(effective)
    try:parser.feed(raw)
    except Exception:pass
    islands=re.findall(r'<script[^>]*type=["\']application/(?:ld\+)?json["\'][^>]*>(.*?)</script>',raw,re.I|re.S)
    return "\n".join(parser.parts),parser.links,{"format":"html","json_islands":[html.unescape(x) for x in islands]}

def read_one(job):
    url=job["url"];key=hashlib.sha256((job["source_id"]+"\0"+job["route"]+"\0"+url).encode()).hexdigest()[:24]
    out=EVIDENCE/(key+".json")
    if out.exists():return json.loads(out.read_text())
    row={**job,"method":"shell_curl","attempted_at":now(),"new_source_visit":True}
    held=blocked.get(norm(url))
    if held:
        row.update(method="restriction_review_no_request",new_source_visit=False,
                   result="saved_exact_access_restriction",restriction=held,completed_at=now(),
                   evidence_file=str(out.relative_to(ROOT)))
        out.write_text(json.dumps(row,ensure_ascii=False,indent=2)+"\n");return row
    host=urlsplit(url).netloc.lower().removeprefix("www.")
    with domain_guard:lock=domain_locks.setdefault(host,threading.Semaphore(2))
    attempts=[];body=b"";headers=b"";status=0;effective=url;ctype=""
    with lock:
        for retry in range(2):
            raw=EVIDENCE/(key+".raw");head=EVIDENCE/(key+".headers")
            p=subprocess.run(["curl","-sS","-L","--connect-timeout","5","--max-time","20","--max-redirs","5",
                              "-D",str(head),"-o",str(raw),"-w","%{http_code}\n%{url_effective}\n%{content_type}",url],
                             capture_output=True,text=True)
            meta=p.stdout.splitlines();status=int(meta[0]) if meta and meta[0].isdigit() else 0
            effective=meta[1] if len(meta)>1 else url;ctype=meta[2] if len(meta)>2 else ""
            body=raw.read_bytes() if raw.exists() else b"";headers=head.read_bytes() if head.exists() else b""
            attempts.append({"at":now(),"retry":retry,"exit_code":p.returncode,"http_status":status,"stderr":p.stderr[:1000]})
            raw.unlink(missing_ok=True);head.unlink(missing_ok=True)
            transient=(p.returncode==28 or status==429 or 500<=status<600)
            if retry or not transient:break
            m=re.search(br"(?im)^retry-after:\s*(\d+)",headers);delay=min(int(m.group(1)),60) if m else 1
            time.sleep(delay)
    text,links,meta=extract(body,ctype,effective)
    gate=bool(status==403 or re.search(r"verify you are human|captcha|attack attempt detected|access denied|cloudflare",text[:10000],re.I))
    row.update(completed_at=now(),http_status=status,effective_url=effective,content_type=ctype,
               attempts=attempts,result="retrieved_page" if status==200 and attempts[-1]["exit_code"]==0 else "request_failed",
               access_gate_observed=gate,body_bytes=len(body),body_sha256=hashlib.sha256(body).hexdigest(),
               text=text,text_length=len(text),text_sha256=hashlib.sha256(text.encode()).hexdigest(),
               links=links,extraction=meta,evidence_file=str(out.relative_to(ROOT)))
    out.write_text(json.dumps(row,ensure_ascii=False,indent=2)+"\n")
    with write_guard:
        with (RUN/"attempts.jsonl").open("a") as f:
            f.write(json.dumps({k:v for k,v in row.items() if k not in {"text","links","extraction"}},ensure_ascii=False)+"\n")
    return row

def main():
    jobs=json.loads(Path(sys.argv[1]).read_text())
    results=[];start=time.monotonic();last_checkpoint=start
    with ThreadPoolExecutor(max_workers=6) as pool:
        future={pool.submit(read_one,j):j for j in jobs}
        for i,f in enumerate(as_completed(future),1):
            row=f.result();results.append(row)
            print(i,len(jobs),row["source_id"],row["route"],row["result"],row.get("http_status"),row.get("text_length"),flush=True)
            if time.monotonic()-last_checkpoint>=900:
                stamp=datetime.now(NY).strftime("%H%M%S")
                (RUN/f"segment-auto-{stamp}.json").write_text(json.dumps({"at":now(),"completed":i,"total":len(jobs)},indent=2)+"\n")
                last_checkpoint=time.monotonic()
    Path(sys.argv[2]).write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__":main()
