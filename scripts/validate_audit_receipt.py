#!/usr/bin/env python3
"""Validate trial-audit receipt evidence and completion coverage."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "data/audit_source_coverage.json"
DEFAULT_INVENTORY = ROOT / "data/source_inventory.json"


def _norm_url(value):
    return str(value or "").strip().rstrip("/")


def _inventory_rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("sources", [])
    return []


def validate(receipt, inventory):
    rows = receipt.get("sources", [])
    errors = []
    coverage_gaps = []
    ids = [row.get("source_id") for row in rows]
    if not ids or None in ids or len(ids) != len(set(ids)):
        errors.append("missing or duplicate source IDs")

    inventory_rows = _inventory_rows(inventory)
    inventory_by_id = {
        row.get("source_id") or row.get("id"): row
        for row in inventory_rows
        if row.get("source_id") or row.get("id")
    }
    inventory_ids = set(inventory_by_id)
    receipt_ids = {source_id for source_id in ids if source_id}

    missing_from_receipt = sorted(inventory_ids - receipt_ids)
    extra_in_receipt = sorted(receipt_ids - inventory_ids)
    if missing_from_receipt:
        errors.append(
            "mandatory inventory sources missing from receipt: "
            + ", ".join(missing_from_receipt)
        )
    if extra_in_receipt:
        errors.append(
            "receipt contains sources absent from current inventory: "
            + ", ".join(extra_in_receipt)
        )

    for key, actual in (
        ("source_total", len(rows)),
        ("attempted_total", sum(row.get("opened_this_run") is True for row in rows)),
        ("content_sufficient_total", sum(row.get("content_sufficient") is True for row in rows)),
    ):
        if receipt.get(key) != actual:
            errors.append(f"{key}: saved={receipt.get(key)} actual={actual}")

    for row in rows:
        name = row.get("source_id", "unknown")
        count = row.get("protocols_seen")
        attempted_urls = row.get("attempted_urls") or []

        if row.get("content_sufficient"):
            if type(count) is not int or count < 0:
                errors.append(f"{name}: sufficient coverage has no current roster count")
            if not row.get("opened_this_run") or not attempted_urls or not row.get("route_used"):
                errors.append(f"{name}: sufficient coverage lacks an opened official route")
            if row.get("master_result") in ("partial", "unreachable"):
                errors.append(f"{name}: result contradicts sufficient coverage")
            if row.get("master_result") == "unchanged" and row.get(
                "fingerprint_preserved_from_prior_same_day_visit"
            ):
                errors.append(
                    f"{name}: historical fingerprint cannot prove current unchanged content"
                )
            continue

        # A mandatory source without current-run roster evidence is an incomplete
        # source, even if HTTP 200, a fresh fingerprint, or a timestamp was saved.
        if not row.get("opened_this_run"):
            coverage_gaps.append(f"{name}: mandatory source was not attempted this run")
            continue

        gap = f"{name}: current roster/status not proven"
        if type(count) is int:
            gap += f" despite protocols_seen={count}"
        coverage_gaps.append(gap)

        inv = inventory_by_id.get(name, {})
        fallbacks = inv.get("fallback_urls") or inv.get("official_fallback_urls") or []
        attempted = {
            _norm_url(item.get("url"))
            for item in attempted_urls
            if isinstance(item, dict) and item.get("url")
        }
        missing_fallbacks = [
            url for url in fallbacks if _norm_url(url) not in attempted
        ]
        if missing_fallbacks:
            coverage_gaps.append(
                f"{name}: official fallbacks not attempted: "
                + ", ".join(missing_fallbacks)
            )

    return errors, coverage_gaps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "receipt", nargs="?", type=Path, default=DEFAULT_RECEIPT
    )
    parser.add_argument(
        "--inventory", type=Path, default=DEFAULT_INVENTORY,
        help="canonical source inventory used to verify mandatory source and fallback coverage",
    )
    args = parser.parse_args()

    receipt = json.loads(args.receipt.read_text())
    inventory = json.loads(args.inventory.read_text())
    errors, coverage_gaps = validate(receipt, inventory)

    status = "PASS" if not errors and not coverage_gaps else "INCOMPLETE"
    print(json.dumps({
        "status": status,
        "receipt": str(args.receipt),
        "inventory": str(args.inventory),
        "errors": errors,
        "coverage_gaps": coverage_gaps,
        "coverage_gap_count": len(coverage_gaps),
    }, indent=2))
    raise SystemExit(status != "PASS")


if __name__ == "__main__":
    main()
