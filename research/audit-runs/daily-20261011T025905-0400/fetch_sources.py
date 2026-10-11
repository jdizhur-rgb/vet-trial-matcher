import hashlib
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
REPO = ROOT.parents[2]


def now():
    return datetime.now(ZoneInfo("America/New_York")).isoformat()


def fetch(item):
    number, source_id, route, url = item
    attempted_at = now()
    out = ROOT / "http"
    out.mkdir(exist_ok=True)
    stem = f"{number:03d}"
    raw = out / f"{stem}.raw"
    headers = out / f"{stem}.headers"
    command = [
        "curl", "--connect-timeout", "5", "--max-time", "20", "--location",
        "--silent", "--show-error", "-D", str(headers), "-o", str(raw),
        "-w", "%{http_code}\n%{url_effective}", url,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    status = int(result.stdout.splitlines()[0]) if result.stdout.splitlines() and result.stdout.splitlines()[0].isdigit() else 0
    if status in {429, 500, 502, 503, 504} or result.returncode in {6, 7, 28, 35, 56}:
        time.sleep(1)
        result = subprocess.run(command, capture_output=True, text=True)
        status = int(result.stdout.splitlines()[0]) if result.stdout.splitlines() and result.stdout.splitlines()[0].isdigit() else 0
    body = raw.read_bytes() if raw.exists() else b""
    pdf_text = None
    if body.startswith(b"%PDF"):
        converted = out / f"{stem}.txt"
        subprocess.run(["pdftotext", "-layout", str(raw), str(converted)], capture_output=True)
        pdf_text = converted.read_text(errors="replace") if converted.exists() else ""
        html = b""
    else:
        html = body
    soup = BeautifulSoup(html, "html.parser")
    links = [{"text": a.get_text(" ", strip=True), "url": urljoin(url, a["href"])} for a in soup.select("a[href]")]
    islands = [
        {"id": s.get("id"), "type": s.get("type"), "text": s.get_text()}
        for s in soup.select("script")
        if s.get("type") == "application/json" or (s.get("id") and not s.get("src"))
    ]
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()
    text = pdf_text if pdf_text is not None else soup.get_text("\n", strip=True)
    evidence = {
        "source_id": source_id,
        "route": route,
        "url": url,
        "attempted_at": attempted_at,
        "method": "shell_curl",
        "exit_code": result.returncode,
        "http_status": status,
        "effective_url": result.stdout.splitlines()[1] if len(result.stdout.splitlines()) > 1 else None,
        "error": result.stderr,
        "title": title,
        "text": text,
        "links": links,
        "data_islands": islands,
        "raw_sha256": hashlib.sha256(body).hexdigest() if body else None,
        "reader_text_sha256": hashlib.sha256(text.encode()).hexdigest() if text else None,
        "raw_file": str(raw.relative_to(ROOT)),
    }
    (out / f"{stem}.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(number, source_id, route, result.returncode, status, len(text), flush=True)
    return evidence


def batches(queue):
    remaining = list(queue)
    while remaining:
        current, domains = [], {}
        for item in list(remaining):
            domain = urlparse(item[3]).netloc
            if domains.get(domain, 0) >= 2:
                continue
            current.append(item)
            domains[domain] = domains.get(domain, 0) + 1
            remaining.remove(item)
            if len(current) == 6:
                break
        yield current, remaining


if __name__ == "__main__":
    inventory = json.loads((REPO / "data/source_inventory.json").read_text())["sources"]
    queue = []
    number = 0
    for source in inventory:
        queue.append((number, source["id"], "master", source["master_url"]))
        number += 1
        for url in source.get("fallback_urls", []):
            queue.append((number, source["id"], "fallback", url))
            number += 1
    (ROOT / "request-queue.json").write_text(json.dumps([
        {"number": n, "source_id": sid, "route": route, "url": url}
        for n, sid, route, url in queue
    ], ensure_ascii=False, indent=2) + "\n")
    results = []
    for current, remaining in batches(queue):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results.extend(pool.map(fetch, current))
        (ROOT / "fetch-checkpoint.json").write_text(json.dumps({
            "recorded_at": now(), "completed": len(results), "remaining": len(remaining)
        }, indent=2) + "\n")
    (ROOT / "native-reader-evidence.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
