#!/usr/bin/env python3
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = []
pattern = re.compile(r"(?m)^(.+?) \((https?://[^\s)]+(?:\)[^\s]*)?)\)\s*$")
for path in sorted(HERE.glob("discovery-search-*.json")):
    data = json.loads(path.read_text())
    text = "\n".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
    for title, url in pattern.findall(text):
        rows.append({"batch": int(path.stem.rsplit("-", 1)[1]), "title": title.strip(), "url": url.strip()})

unique, seen = [], set()
for row in rows:
    key = row["url"].rstrip("/")
    if key not in seen:
        seen.add(key)
        unique.append(row)

previous = json.loads((HERE.parent / "daily-20261122T033544-0500/discovery-candidates-raw.json").read_text())
old = {x["url"].rstrip("/") for x in previous.get("candidates", [])}
for row in unique:
    row["new_vs_previous_run"] = row["url"].rstrip("/") not in old

out = {"count": len(unique), "new_vs_previous_run": sum(x["new_vs_previous_run"] for x in unique), "candidates": unique}
(HERE / "discovery-candidates-raw.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ("count", "new_vs_previous_run")}, ensure_ascii=False))
