#!/usr/bin/env python3
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREV = ROOT / "research/audit-runs/daily-20261122T033544-0500"


def normalized(text):
    text = re.sub(r"turn\d+(?:view|search)\d+", "turnREF", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def content_core(text):
    match = re.search(r"(?:^|\n)L0(?:@P\d+)?:", text)
    core = text[match.start():] if match else text
    return normalized(core)


def same_retrieved_content(old, new):
    a, b = content_core(old), content_core(new)
    if not a or not b:
        return False
    common = min(len(a), len(b), 1800)
    return common >= 500 and a[:common] == b[:common]


def parse(kind):
    requested = json.loads((HERE / f"{kind}-web-routes.json").read_text())
    found = {}
    for path in sorted(HERE.glob(f"web-{kind}-open-*.json")):
        payload = json.loads(path.read_text())
        text = "\n".join(x.get("text", "") for x in payload.get("content", []) if x.get("type") == "text")
        pieces = re.split(r"\n-{20,}\n", text)
        for piece in pieces:
            for url in requested:
                if url not in piece:
                    continue
                crawled = re.search(r"Crawled: ([^;\n]+)", piece)
                failed = "Failed to fetch" in piece or "Internal Error" in piece
                title = piece.strip().splitlines()[0] if piece.strip() else ""
                norm = normalized(piece)
                found[url] = {
                    "url": url,
                    "batch_file": str(path.relative_to(ROOT)),
                    "completed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "method": "web_open",
                    "result": "web_error" if failed else "success",
                    "opened": not failed,
                    "crawled_label": crawled.group(1).strip() if crawled else None,
                    "crawled_today": bool(crawled and crawled.group(1).strip() == "today"),
                    "title": title[:500],
                    "normalized_text_sha256": hashlib.sha256(norm.encode()).hexdigest(),
                    "excerpt": piece[:4000],
                }
    previous = {}
    prev_file = PREV / f"current-{kind}-web-summary.json"
    if prev_file.exists():
        for row in json.loads(prev_file.read_text()).get("routes", []):
            previous[row["url"]] = row.get("excerpt", "")
    rows = []
    for url in requested:
        row = found.get(url, {
            "url": url,
            "completed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "method": "web_open",
            "result": "web_error",
            "opened": False,
            "crawled_label": None,
            "crawled_today": False,
            "title": "",
            "normalized_text_sha256": None,
            "excerpt": "No saved Web response block was returned for this exact URL.",
        })
        old = previous.get(url)
        row["previous_normalized_text_sha256"] = hashlib.sha256(normalized(old).encode()).hexdigest() if old else None
        row["comparison"] = "unchanged_retrieved_content" if old and same_retrieved_content(old, row.get("excerpt", "")) else ("changed_or_new_retrieved_content" if row.get("opened") else "unavailable")
        rows.append(row)
    summary = {
        "routes": len(rows),
        "success": sum(r["result"] == "success" for r in rows),
        "web_error": sum(r["result"] != "success" for r in rows),
        "crawled_today": sum(r.get("crawled_today", False) for r in rows),
        "unchanged_retrieved_content": sum(r["comparison"] == "unchanged_retrieved_content" for r in rows),
        "changed_or_new_retrieved_content": sum(r["comparison"] == "changed_or_new_retrieved_content" for r in rows),
    }
    out = {"schema_version": 1, "run_id": HERE.name, "recorded_at": dt.datetime.now(dt.timezone.utc).isoformat(), "method": "web_open_same_official_urls_after_shell_transport_failure", "routes": rows, "summary": summary}
    (HERE / f"current-{kind}-web-summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(kind, json.dumps(summary, ensure_ascii=False))


parse("source")
parse("protocol")
