#!/usr/bin/env python3
"""Validate the canonical trial catalog before it reaches production."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo.catalog_selection import current_public  # noqa: E402


DEFAULT_CATALOG = ROOT / "data" / "trials_base.json"
REQUIRED_ACTIVE_FIELDS = {
    "id",
    "title",
    "center",
    "country",
    "species",
    "cancers",
    "status",
    "study_type",
    "url",
    "verified",
    "notes",
}


def validate(path: Path) -> tuple[int, int]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise AssertionError("Catalog root must be a JSON array")

    ids: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise AssertionError(f"Catalog row {index} must be a JSON object")
        trial_id = row.get("id")
        if not isinstance(trial_id, str) or not trial_id.strip():
            raise AssertionError(f"Catalog row {index} has no non-empty id")
        if trial_id in ids:
            raise AssertionError(f"Duplicate trial id: {trial_id}")
        ids.add(trial_id)

    active = current_public(rows)
    for row in active:
        missing = sorted(
            field
            for field in REQUIRED_ACTIVE_FIELDS
            if field not in row
            or row[field] is None
            or row[field] == []
            or (isinstance(row[field], str) and not row[field].strip())
        )
        if missing:
            raise AssertionError(
                f"Active trial {row['id']} missing required fields: {', '.join(missing)}"
            )

    return len(rows), len(active)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    total, active = validate(args.path)
    print(
        "TRIAL_CATALOG_VALIDATION_OK",
        f"records={total}",
        f"unique_ids={total}",
        f"active={active}",
        f"required_active_fields={len(REQUIRED_ACTIVE_FIELDS)}",
    )


if __name__ == "__main__":
    main()
