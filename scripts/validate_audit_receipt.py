#!/usr/bin/env python3
"""Reject unsupported sufficient-coverage claims in a trial audit receipt."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(receipt):
    rows = receipt.get("sources", [])
    errors = []
    ids = [row.get("source_id") for row in rows]
    if not ids or None in ids or len(ids) != len(set(ids)):
        errors.append("missing or duplicate source IDs")
    for key, actual in (
        ("source_total", len(rows)),
        ("attempted_total", sum(row.get("opened_this_run") is True for row in rows)),
        ("content_sufficient_total", sum(row.get("content_sufficient") is True for row in rows)),
    ):
        if receipt.get(key) != actual:
            errors.append(f"{key}: saved={receipt.get(key)} actual={actual}")
    for row in rows:
        if not row.get("content_sufficient"):
            continue
        name = row.get("source_id", "unknown")
        count = row.get("protocols_seen")
        if type(count) is not int or count < 0:
            errors.append(f"{name}: sufficient coverage has no current roster count")
        if not row.get("opened_this_run") or not row.get("attempted_urls") or not row.get("route_used"):
            errors.append(f"{name}: sufficient coverage lacks an opened official route")
        if row.get("master_result") in ("partial", "unreachable"):
            errors.append(f"{name}: result contradicts sufficient coverage")
        if row.get("master_result") == "unchanged" and row.get("fingerprint_preserved_from_prior_same_day_visit"):
            errors.append(f"{name}: historical fingerprint cannot prove current unchanged content")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", nargs="?", type=Path, default=ROOT / "data/audit_source_coverage.json")
    args = parser.parse_args()
    errors = validate(json.loads(args.receipt.read_text()))
    print(json.dumps({"status": "INCOMPLETE" if errors else "PASS", "receipt": str(args.receipt), "errors": errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
