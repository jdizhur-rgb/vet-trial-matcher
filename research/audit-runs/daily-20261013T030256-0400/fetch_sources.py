#!/usr/bin/env python3
"""Finite one-pass fetch of every configured daily trial source route."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
INVENTORY = json.loads((ROOT / "data/source_inventory.json").read_text())["sources"]
TZ = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (compatible; VetTrialFinderAudit/1.0; +https://vettrialfinder.com/)"
KEYWORDS = re.compile(
    r"oncolog|cancer|tumou?r|neoplas|sarcoma|lymphoma|melanoma|carcinoma|glioma|"
    r"osteosarcoma|hemangiosarcoma|mast.?cell|clinical.?trial|clinical.?stud|recruit|enrol",
    re.I,
)


def now() -> str:
    return datetime.now(TZ).isoformat()


def clean_text(raw: bytes, content_type: str) -> tuple[str, str, list[dict]]:
    decoded = raw.decode("utf-8", errors="replace")
    title = ""
    links: list[dict] = []
    if "html" in content_type.lower() or "<html" in decoded[:1000].lower():
        soup = BeautifulSoup(decoded, "html.parser")
        if soup.title:
            title = soup.title.get_text(" ", strip=True)
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        for a in soup.find_all("a", href=True):
            text = " ".join(a.get_text(" ", strip=True).split())
            href = a.get("href", "").strip()
            if KEYWORDS.search(f"{text} {href}"):
                links.append({"text": text[:300], "href": href})
        text = "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
    else:
        text = decoded
    return title[:500], text[:120000], links[:150]


def fetch(item: tuple[str, str, str, str]) -> dict:
    sid, route, url, source_name = item
    attempted_at = now()
    cmd = [
        "curl", "-L", "--compressed", "--silent", "--show-error",
        "--connect-timeout", "5", "--max-time", "20", "--retry", "1",
        "--retry-delay", "1", "--retry-max-time", "25",
        "-A", UA, "-D", "-", "-o", "-", url,
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    payload = proc.stdout
    # curl -D - prepends one or more header blocks. Split at the final header/body boundary.
    markers = [m.end() for m in re.finditer(rb"\r?\n\r?\n", payload)]
    body_start = markers[-1] if markers else 0
    headers = payload[:body_start].decode("latin-1", errors="replace")
    body = payload[body_start:]
    statuses = re.findall(r"HTTP/\S+\s+(\d{3})", headers)
    status = int(statuses[-1]) if statuses else None
    types = re.findall(r"(?im)^content-type:\s*([^\r\n]+)", headers)
    ctype = types[-1] if types else ""
    effective = ""
    if proc.returncode == 0:
        eff = subprocess.run(
            ["curl", "-L", "--silent", "--show-error", "--connect-timeout", "5", "--max-time", "20", "-A", UA, "-o", "/dev/null", "-w", "%{url_effective}", url],
            cwd=ROOT, capture_output=True, text=True,
        )
        effective = eff.stdout.strip()
    title, text, links = clean_text(body, ctype)
    # Keep concise proof, not full third-party pages or embedded configuration.
    keyword_lines = []
    for line in text.splitlines():
        if KEYWORDS.search(line):
            keyword_lines.append(line[:800])
        if len(keyword_lines) >= 120:
            break
    return {
        "source_id": sid,
        "source_name": source_name,
        "route": route,
        "url": url,
        "attempted_at": attempted_at,
        "method": "shell_curl",
        "exit_code": proc.returncode,
        "http_status": status,
        "effective_url": effective or url,
        "content_type": ctype,
        "raw_sha256": hashlib.sha256(body).hexdigest() if body else None,
        "text_sha256": hashlib.sha256(text.encode()).hexdigest() if text else None,
        "text_length": len(text),
        "title": title,
        "keyword_excerpt": keyword_lines,
        "relevant_links": links,
        "stderr": proc.stderr.decode("utf-8", errors="replace")[-1000:],
    }


def main() -> None:
    queue = []
    for src in INVENTORY:
        sid = src["id"]
        queue.append((sid, "master", src["master_url"], src["name"]))
        for url in src.get("fallback_urls", []):
            queue.append((sid, "fallback", url, src["name"]))
    (RUN / "request-queue.json").write_text(json.dumps({
        "created_at": now(), "source_total": len(INVENTORY), "route_total": len(queue),
        "queue": [{"source_id": x[0], "route": x[1], "url": x[2]} for x in queue],
    }, ensure_ascii=False, indent=2) + "\n")
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for row in pool.map(fetch, queue):
            rows.append(row)
            if len(rows) % 18 == 0:
                (RUN / "fetch-checkpoint.json").write_text(json.dumps({
                    "updated_at": now(), "completed_routes": len(rows), "route_total": len(queue),
                    "completed_sources": len({x["source_id"] for x in rows}),
                }, indent=2) + "\n")
    (RUN / "native-reader-evidence.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    summary = {
        "completed_at": now(), "sources": len({x["source_id"] for x in rows}), "routes": len(rows),
        "http_200": sum(x["http_status"] == 200 for x in rows),
        "shell_failures": sum(x["exit_code"] != 0 for x in rows),
        "http_403": sum(x["http_status"] == 403 for x in rows),
        "http_404": sum(x["http_status"] == 404 for x in rows),
        "insufficient_text": sum(x["http_status"] == 200 and x["text_length"] < 300 for x in rows),
    }
    (RUN / "fetch-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
