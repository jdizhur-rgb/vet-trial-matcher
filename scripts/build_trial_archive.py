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
CLEANUP = DATA / "catalog_patch_zzzz_archive_closed.json"

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


def merge(old: dict, patch: dict) -> dict:
    out = dict(old)
    for key, value in patch.items():
        if key in {"requires", "excludes"} and isinstance(value, dict):
            nested = dict(out.get(key, {}) if isinstance(out.get(key), dict) else {})
            nested.update(value)
            out[key] = nested
        else:
            out[key] = value
    return out


def load_prearchive_catalog() -> dict[str, dict]:
    rows = {r["id"]: r for r in json.loads((DATA / "trials_base.json").read_text())}
    paths = [DATA / "trial_updates.json"] + sorted(DATA.glob("catalog_patch_*.json"))
    for path in paths:
        if path.name == CLEANUP.name:
            continue
        doc = json.loads(path.read_text())
        for rid in doc.get("delete", []):
            rows.pop(rid, None)
        for patch in doc.get("upsert", []):
            rows[patch["id"]] = merge(rows.get(patch["id"], {}), patch)
    return rows


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

    cleanup_doc = {
        "note": "Applied last alphabetically. Removes only explicitly completed/closed studies from the effective working catalog; full records live in data/archive/trials_closed.json.",
        "delete": [r["id"] for r in closed],
        "upsert": [],
    }
    CLEANUP.write_text(json.dumps(cleanup_doc, ensure_ascii=False, indent=2) + "\n")

    print(f"ARCHIVED_CLOSED {len(closed)}")
    print(f"WORKING_AFTER_ARCHIVE {len(rows) - len(closed)}")


if __name__ == "__main__":
    main()
