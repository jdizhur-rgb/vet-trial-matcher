#!/usr/bin/env python3
"""Build a clean archive of inactive/closed studies from the canonical catalog."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "archive" / "inactive_trials.json"
CURRENT = {"current", "confirmed_current"}


def merge_catalog():
    return {
        x["id"]: x
        for x in json.loads((DATA / "trials_base.json").read_text(encoding="utf-8"))
    }


def is_current(row):
    return row.get("available_for_matching", True) and row.get("status_confidence") in CURRENT


def main():
    rows = merge_catalog()
    inactive = []
    for row in rows.values():
        if is_current(row):
            continue
        inactive.append({
            "id": row.get("id"),
            "title": row.get("title", ""),
            "center": row.get("center", ""),
            "country": row.get("country", ""),
            "state": row.get("state", ""),
            "species": row.get("species", ""),
            "cancers": row.get("cancers", []),
            "study_type": row.get("study_type", "treatment"),
            "status": row.get("status", ""),
            "status_confidence": row.get("status_confidence", ""),
            "available_for_matching": row.get("available_for_matching", True),
            "url": row.get("url", ""),
            "registry_url": row.get("registry_url", ""),
            "verified": row.get("verified", ""),
            "archived_reason": "not current/available in effective catalog",
        })
    inactive.sort(key=lambda x: (str(x.get("center", "")), str(x.get("title", "")), str(x.get("id", ""))))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "generated": str(date.today()),
        "purpose": "Historical tomb for inactive, closed, on-hold, withdrawn, watch, planned, or reconfirmation-needed studies. Never loaded by the patient-facing Finder.",
        "count": len(inactive),
        "trials": inactive,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ARCHIVED {len(inactive)} -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
