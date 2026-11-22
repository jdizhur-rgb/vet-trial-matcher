#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def split_results(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n-{40,}\n", text) if part.strip()]


def assemble(kind: str) -> dict:
    rows = []
    for path in sorted(HERE.glob(f"web-{kind}-open-[0-9][0-9].json")):
        payload = json.loads(path.read_text())
        urls = payload["urls"]
        text = "\n".join(
            item.get("text", "")
            for item in payload["result"].get("content", [])
            if item.get("type") == "text"
        )
        segments = split_results(text)
        if len(urls) != len(segments):
            raise SystemExit(f"{path.name}: {len(urls)} urls, {len(segments)} results")
        completed_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        evidence = f"research/audit-runs/{HERE.name}/{path.name}"
        for url, segment in zip(urls, segments):
            internal_error = segment.startswith("Internal Error")
            crawled = re.search(r"Crawled: ([^;\n]+)", segment)
            label = crawled.group(1).strip() if crawled else None
            rows.append({
                "url": url,
                "batch": payload["batch"],
                "completed_at": completed_at,
                "method": "web_open",
                "result": "web_error" if internal_error else "success",
                "opened": not internal_error,
                "crawled_label": label,
                "crawled_today": label == "today",
                "title": segment.splitlines()[0].strip() if segment else "",
                "text_sha256": hashlib.sha256(segment.encode()).hexdigest(),
                "excerpt": segment[:1800],
                "evidence_file": evidence,
            })
    return {
        "schema_version": 1,
        "run_id": HERE.name,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "method": "web_open_same_official_urls_after_shell_transport_failure",
        "routes": rows,
        "summary": {
            "routes": len(rows),
            "success": sum(row["result"] == "success" for row in rows),
            "web_error": sum(row["result"] == "web_error" for row in rows),
            "crawled_today": sum(row["crawled_today"] for row in rows),
        },
    }


for kind in ("source", "protocol"):
    payload = assemble(kind)
    (HERE / f"current-{kind}-web-summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    )
    print(kind, payload["summary"])
