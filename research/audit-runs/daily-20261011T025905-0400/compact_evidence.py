#!/usr/bin/env python3
"""Compact native fetch evidence while preserving current roster proof."""
from collections import Counter
import json
from pathlib import Path
import re

RUN = Path(__file__).resolve().parent
rows = json.loads((RUN / "native-reader-evidence.json").read_text())
keyword = re.compile(
    r"oncolog|cancer|tumou?r|sarcoma|lymphoma|melanoma|carcinoma|glioma|"
    r"osteosarcoma|hemangiosarcoma|mast.?cell|neoplas|clinical.?trial|clinical.?stud",
    re.I,
)

compact = []
for row in rows:
    item = {key: row.get(key) for key in (
        "source_id", "route", "url", "attempted_at", "method", "exit_code",
        "http_status", "effective_url", "error", "title", "raw_sha256",
        "reader_text_sha256", "raw_file",
    )}
    text = row.get("text") or row.get("text_excerpt") or ""
    item["text_length"] = len(text)
    item["text_excerpt"] = text[:1500]
    relevant_links = []
    for link in row.get("links") or row.get("relevant_links") or []:
        if not isinstance(link, dict):
            continue
        blob = f"{link.get('text', '')} {link.get('url', link.get('href', ''))}"
        if keyword.search(blob):
            relevant_links.append(link)
    item["relevant_links"] = relevant_links[:50]
    item["data_island_count"] = len(row.get("data_islands") or [])

    raw_path = RUN / row.get("raw_file", "")
    if raw_path.exists() and row.get("http_status") == 200:
        try:
            payload = json.loads(raw_path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = None
        if isinstance(payload, dict) and isinstance(payload.get("studies"), list):
            studies = payload["studies"]
            oncology = []
            for study in studies:
                blob = json.dumps(study, ensure_ascii=False)
                if keyword.search(blob):
                    oncology.append({
                        "id": study.get("id"),
                        "name": study.get("name"),
                        "status": study.get("status"),
                        "url": study.get("url"),
                    })
            item["structured_roster"] = {
                "reported_total": payload.get("total"),
                "page_records": len(studies),
                "status_counts": dict(Counter(str(study.get("status")) for study in studies)),
                "oncology_keyword_records": oncology,
            }
        elif isinstance(payload, dict) and isinstance(payload.get("data"), list):
            data = payload["data"]
            item["structured_roster"] = {
                "page_records": len(data),
                "oncology_keyword_records": [
                    {key: value.get(key) for key in ("id", "title", "name", "status", "url")}
                    for value in data
                    if keyword.search(json.dumps(value, ensure_ascii=False))
                ],
            }
    compact.append(item)

(RUN / "native-reader-evidence.json").write_text(
    json.dumps(compact, ensure_ascii=False, indent=2) + "\n"
)
print({"rows": len(compact), "bytes": (RUN / "native-reader-evidence.json").stat().st_size})
