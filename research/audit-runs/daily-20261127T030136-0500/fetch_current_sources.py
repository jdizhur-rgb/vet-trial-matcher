#!/usr/bin/env python3
import concurrent.futures
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
OUT = RUN / "raw-current"
OUT.mkdir(exist_ok=True)


def norm(url):
    p = urlsplit(url.strip())
    path = re.sub(r"/+", "/", p.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ""))


inventory = json.loads((ROOT / "data/source_inventory.json").read_text())
restriction_doc = json.loads((ROOT / "data/source_access_restrictions.json").read_text())
restricted = {}
for row in restriction_doc.get("routes", []):
    if row.get("do_not_retry") and row.get("url"):
        restricted[norm(row["url"])] = row
for source in inventory["sources"]:
    for row in source.get("access_restrictions") or []:
        if row.get("do_not_retry") and row.get("url"):
            restricted[norm(row["url"])] = row

jobs = []
for source in inventory["sources"]:
    urls = [source["master_url"], *(source.get("fallback_urls") or [])]
    seen = set()
    for index, url in enumerate(urls):
        key = norm(url)
        if key in seen:
            continue
        seen.add(key)
        jobs.append({"source_id": source["id"], "url": url, "normalized_url": key,
                     "route": "master" if index == 0 else "fallback"})


def one(job):
    started = datetime.now(timezone.utc).isoformat()
    key = job["normalized_url"]
    if key in restricted:
        row = restricted[key]
        return {**job, "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
                "result": "skipped_exact_restriction", "status": None,
                "restriction_evidence": row.get("origin") or row.get("evidence_file") or row.get("observed_at")}
    filename = hashlib.sha256((job["source_id"] + "\n" + job["url"]).encode()).hexdigest()[:20] + ".bin"
    target = OUT / filename
    cmd = ["curl", "-L", "--connect-timeout", "5", "--max-time", "20", "--retry", "1",
           "--retry-delay", "1", "--retry-max-time", "20", "--retry-connrefused",
           "-A", "VetTrialFinderAudit/1.0", "-sS", "-o", str(target),
           "-w", "%{http_code}", job["url"]]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    status_text = proc.stdout.strip()[-3:]
    status = int(status_text) if status_text.isdigit() and status_text != "000" else None
    body = target.read_bytes() if target.exists() else b""
    if status is not None:
        return {**job, "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
                "result": "http_response", "status": status, "bytes": len(body),
                "content_sha256": hashlib.sha256(body).hexdigest(),
                "artifact": str(target.relative_to(ROOT)), "curl_exit": proc.returncode,
                "stderr": proc.stderr[-2000:]}
    target.unlink(missing_ok=True)
    return {**job, "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
            "result": "transport_error", "status": None, "curl_exit": proc.returncode,
            "error": proc.stderr[-2000:] or "curl returned no HTTP status"}


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows = list(pool.map(one, jobs))

result = {
    "run_id": RUN.name,
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "method": "requests; connect timeout 5s, total/read timeout 20s; one retry only for connection/timeout/429/5xx",
    "restriction_count_loaded": len(restricted),
    "source_total": len(inventory["sources"]),
    "jobs": len(jobs),
    "attempts": rows,
}
(RUN / "current-source-evidence.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"sources": result["source_total"], "jobs": len(jobs),
                  "results": {k: sum(r["result"] == k for r in rows) for k in sorted({r["result"] for r in rows})}}, indent=2))
