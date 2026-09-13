#!/usr/bin/env python3
"""Move explicitly completed/closed trials out of the effective working catalog.

The archive keeps the full merged record for history and duplicate prevention.
On-hold and needs-reconfirmation records are deliberately NOT archived: they may
return to active matching and remain part of the working review set.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARCHIVE = DATA / "archive" / "trials_closed.json"
CATALOG = DATA / "trials_base.json"

CLOSED_WORDS = (
    "closed",
    "completed",
    "ended",
    "withdrawn",
    "terminated",
    "cancelled",
    "canceled",
    "no longer active",
    "enrollment complete",
    "enrollment ended",
    "not recruiting",
)


def load_prearchive_catalog() -> dict[str, dict]:
    return {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))}


def is_explicitly_closed(row: dict) -> bool:
    # Never bury a record merely because matching is disabled. A disabled study
    # can be on hold or awaiting reconfirmation and belongs in the working set.
    fields = [
        row.get("status"),
        row.get("status_confidence"),
        row.get("recruitment_status"),
        row.get("enrollment_status"),
    ]
    text = " | ".join(str(x).strip().lower() for x in fields if x)
    return bool(text) and any(word in text for word in CLOSED_WORDS)


def main() -> None:
    rows = load_prearchive_catalog()
    closed = [r for r in rows.values() if is_explicitly_closed(r)]
    closed.sort(key=lambda r: (str(r.get("center", "")), str(r.get("title", "")), r["id"]))

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    archive_doc = {
        "purpose": "Historical archive of explicitly completed/closed cancer studies. Not loaded by the patient-facing finder.",
        "policy": "Full merged records are retained here to prevent accidental re-addition. On-hold and needs-reconfirmation studies stay in the working catalog.",
        "generated_on": date.today().isoformat(),
        "count": len(closed),
        "records": closed,
    }
    ARCHIVE.write_text(json.dumps(archive_doc, ensure_ascii=False, indent=2) + "\n")

    closed_ids = {r["id"] for r in closed}
    remaining = [r for r in rows.values() if r["id"] not in closed_ids]
    CATALOG.write_text(json.dumps(remaining, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ARCHIVED_CLOSED {len(closed)}")
    print(f"WORKING_AFTER_ARCHIVE {len(rows) - len(closed)}")


if __name__ == "__main__":
    main()
