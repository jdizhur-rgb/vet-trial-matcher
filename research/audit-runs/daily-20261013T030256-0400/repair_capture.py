#!/usr/bin/env python3
"""Repair local response-body capture for routes whose first fetch parser lost the body."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
TZ = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (compatible; VetTrialFinderAudit/1.0; +https://vettrialfinder.com/)"
KEYWORDS = re.compile(r"oncolog|cancer|tumou?r|neoplas|sarcoma|lymphoma|melanoma|carcinoma|glioma|osteosarcoma|hemangiosarcoma|mast.?cell|clinical.?trial|clinical.?stud|recruit|enrol", re.I)
MARK = b"\n__VTF_CURL_META__"


def now():
    return datetime.now(TZ).isoformat()


def fetch(old):
    proc = subprocess.run([
        "curl", "-L", "--compressed", "--silent", "--show-error",
        "--connect-timeout", "5", "--max-time", "20", "-A", UA,
        "-w", "\n__VTF_CURL_META__%{http_code}\t%{url_effective}\t%{content_type}", old["url"],
    ], cwd=ROOT, capture_output=True)
    payload = proc.stdout
    body, _, meta = payload.rpartition(MARK)
    parts = meta.decode("utf-8", errors="replace").split("\t") if meta else []
    status = int(parts[0]) if parts and parts[0].isdigit() else old.get("http_status")
    effective = parts[1] if len(parts) > 1 else old.get("effective_url")
    ctype = parts[2] if len(parts) > 2 else old.get("content_type", "")
    decoded = body.decode("utf-8", errors="replace")
    title = ""
    links = []
    if "html" in ctype.lower() or "<html" in decoded[:1000].lower():
        soup = BeautifulSoup(decoded, "html.parser")
        if soup.title:
            title = soup.title.get_text(" ", strip=True)
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        for a in soup.find_all("a", href=True):
            label = " ".join(a.get_text(" ", strip=True).split())
            href = a.get("href", "").strip()
            if KEYWORDS.search(f"{label} {href}"):
                links.append({"text": label[:300], "href": href})
        text = "\n".join(x.strip() for x in soup.get_text("\n").splitlines() if x.strip())
    else:
        text = decoded
    lines = [x[:800] for x in text.splitlines() if KEYWORDS.search(x)][:120]
    return {**old, "capture_repaired_at": now(), "capture_note": "First request completed but local header/body parser lost the body; this corrective read preserved it.",
            "method": "shell_curl_capture_repair", "exit_code": proc.returncode,
            "http_status": status, "effective_url": effective, "content_type": ctype,
            "raw_sha256": hashlib.sha256(body).hexdigest() if body else None,
            "text_sha256": hashlib.sha256(text.encode()).hexdigest() if text else None,
            "text_length": len(text), "title": title[:500], "keyword_excerpt": lines,
            "relevant_links": links[:150], "stderr": proc.stderr.decode("utf-8", errors="replace")[-1000:]}


def main():
    path = RUN / "native-reader-evidence.json"
    rows = json.loads(path.read_text())
    targets = [r for r in rows if r.get("http_status") == 200 and r.get("text_length", 0) < 300]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        repaired = list(pool.map(fetch, targets))
    by_key = {(r["source_id"], r["route"], r["url"]): r for r in repaired}
    merged = [by_key.get((r["source_id"], r["route"], r["url"]), r) for r in rows]
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
    summary = {"completed_at": now(), "targets": len(targets),
               "repaired_text_ge_300": sum(r.get("text_length", 0) >= 300 for r in repaired),
               "still_insufficient": sum(r.get("text_length", 0) < 300 for r in repaired)}
    (RUN / "capture-repair-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
