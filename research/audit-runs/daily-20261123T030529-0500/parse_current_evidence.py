#!/usr/bin/env python3
import glob, hashlib, json, pathlib, re
from urllib.parse import urlsplit, urlunsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[3]
RUN = pathlib.Path(__file__).resolve().parent
PREV = ROOT / "research/audit-runs/daily-20261122T041011-0500"

def norm(url):
    p=urlsplit(url.strip()); path=re.sub(r"/+", "/", unquote(p.path or "/"))
    if path != "/": path=path.rstrip("/")
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,""))

def blocks(folder, pattern):
    out={}
    for fn in sorted(glob.glob(str(folder/pattern))):
        d=json.load(open(fn)); text="\n".join(x.get("text","") for x in d.get("content",[]) if x.get("type")=="text")
        for block in re.split(r"\n-{20,}\n", text):
            m=re.search(r'Source: open\(\{"ref_id":"(https?://[^"}]+)"', block)
            if not m: continue
            url=m.group(1); success="Internal Error" not in block and "Failed to fetch" not in block
            page_lines=[]
            for line in block.splitlines():
                mline=re.match(r"L\d+:\s?(.*)", line)
                if mline:
                    value=re.sub(r"【\d+†([^】]*)】", r"\1", mline.group(1))
                    value=re.sub(r"\s+", " ", value).strip()
                    page_lines.append(value)
            if page_lines:
                cleaned="\n".join(page_lines)
            else:
                cleaned=re.sub(r"turn\d+(?:view|fetch|search)\d+","REF",block)
                cleaned=re.sub(r"Crawled: [^;\n]+", "Crawled: CURRENT", cleaned)
                cleaned=re.sub(r'\{"ref_id":"[^"]+"', '{"ref_id":"URL"', cleaned)
            out[norm(url)]={"url":url,"success":success,"artifact":str(pathlib.Path(fn).relative_to(ROOT)),
                            "content_sha256":hashlib.sha256(cleaned.encode()).hexdigest(),
                            "excerpt":block[:3000]}
    return out

def summarize(kind, evidence_name, web_pattern):
    current=blocks(RUN,web_pattern); previous=blocks(PREV,web_pattern)
    evidence=json.load(open(RUN/evidence_name)); rows=[]
    for a in evidence["attempts"]:
        w=current.get(norm(a["requested_url"]))
        old=previous.get(norm(a["requested_url"]))
        row={"id":a.get("source_id"),"role":a.get("role"),"url":a["requested_url"],
             "native_result":a.get("result"),"native_completed_at":a.get("completed_at"),
             "native_artifact":a.get("raw_artifact"),"web":w}
        if w:
            row["comparison"]="new_route" if not old else ("unchanged_web_extract" if old["content_sha256"]==w["content_sha256"] else "changed_web_extract")
        else: row["comparison"]="no_web_attempt"
        rows.append(row)
    summary={"run_id":RUN.name,"kind":kind,"rows":rows,
             "counts":{"routes":len(rows),"web_success":sum(bool((r.get("web") or {}).get("success")) for r in rows),
                       "web_failed":sum(bool(r.get("web")) and not r["web"]["success"] for r in rows),
                       "restricted":sum(r["native_result"].endswith("restriction") for r in rows),
                       "changed":sum(r["comparison"]=="changed_web_extract" for r in rows),
                       "unchanged":sum(r["comparison"]=="unchanged_web_extract" for r in rows),
                       "new_route":sum(r["comparison"]=="new_route" for r in rows)}}
    (RUN/f"current-{kind}-web-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(kind,summary["counts"])

summarize("source","current-source-evidence.json","web-source-open-*.json")
summarize("protocol","current-protocol-evidence.json","web-protocol-open-*.json")
