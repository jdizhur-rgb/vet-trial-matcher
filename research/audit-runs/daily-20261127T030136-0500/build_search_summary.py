#!/usr/bin/env python3
"""Normalize this run's saved global-search calls into auditable query rows."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
NOW = datetime.now(timezone.utc).isoformat()
REGIONS = [
    "usa", "canada", "uk", "continental_europe", "latin_america_caribbean",
    "australia_new_zealand", "east_asia", "south_asia", "southeast_asia",
    "middle_east", "north_africa", "sub_saharan_africa",
]


def read(name):
    return json.loads((RUN / name).read_text())


def write(name, value):
    (RUN / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


groups = []
current = read("global-current-raw.json")
recent = read("global-recent-raw.json")
for index, region in enumerate(REGIONS):
    queries = []
    for pass_name, payload, recency in (
        ("current_undated", current, None),
        ("recent_7_day", recent, 7),
    ):
        for query in payload[index]["queries"]:
            queries.append({
                "pass": pass_name,
                "country": region,
                "language": "mixed_local_and_english",
                "query": query,
                "recency_days": recency,
                "run_at": NOW,
                "raw_evidence": f"research/audit-runs/{RUN.name}/global-{('current' if recency is None else 'recent')}-raw.json",
            })
    groups.append({"region": region, "queries": queries})

deep_regions = [
    "continental_europe", "latin_america_caribbean", "east_asia", "south_asia",
    "southeast_asia", "middle_east_north_africa", "sub_saharan_africa",
]
deep = []
for index, batch in enumerate(read("global-deepening-raw.json")):
    deep.append({
        "region": deep_regions[index],
        "queries": [{
            "pass": "weak_region_deepening",
            "country": "country_specific",
            "language": "local_language_or_english",
            "query": row["q"],
            "run_at": NOW,
            "raw_evidence": f"research/audit-runs/{RUN.name}/global-deepening-raw.json",
        } for row in batch["queries"]],
    })

write("global-search-results.json", groups)
write("global-search-deepening.json", deep)
print(json.dumps({
    "regions": len(groups),
    "initial_and_recent_queries": sum(len(x["queries"]) for x in groups),
    "deepening_queries": sum(len(x["queries"]) for x in deep),
}, indent=2))
