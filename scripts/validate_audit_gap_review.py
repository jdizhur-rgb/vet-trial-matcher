#!/usr/bin/env python3
"""Validate per-source gap diagnosis without changing the strict coverage result."""
import argparse
from collections import Counter
import json
from pathlib import Path

CATEGORIES = {
    "source_unavailable", "roster_unestablished", "freshness_uncertain",
    "discovery_source_not_trial_roster", "protocol_uncertainty",
}
ASSESSMENTS = {"external_blocker", "executor_unfinished", "not_established"}


def validate(review, receipt):
    errors = []
    gaps = {r["source_id"]: r for r in receipt["sources"] if not r.get("content_sufficient")}
    rows = review.get("rows", [])
    ids = [r.get("source_id") for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(gaps):
        errors.append("review must cover each insufficient source exactly once")
    if review.get("original_run_id") != receipt.get("run_id"):
        errors.append("review and receipt run IDs differ")
    for row in rows:
        sid = row.get("source_id")
        if row.get("category") not in CATEGORIES:
            errors.append(f"{sid}: unknown gap category")
        assessment = row.get("processing_assessment")
        if assessment not in ASSESSMENTS:
            errors.append(f"{sid}: missing processing assessment")
        for key in ("question", "reason", "next_action"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                errors.append(f"{sid}: missing {key}")
        evidence = row.get("evidence", {})
        recorded = {a.get("url") for a in gaps.get(sid, {}).get("attempted_urls", [])}
        urls = evidence.get("attempted_urls", [])
        if evidence.get("source_id") != sid or not urls or not set(urls) <= recorded:
            errors.append(f"{sid}: evidence must reference actual receipt attempts")
        if assessment == "external_blocker":
            # A partial label alone is never evidence that all available work finished.
            decision = row.get("completion_decision", {})
            for key in ("remaining_fact", "routes_exhausted_evidence", "available_reconciliation_done_evidence"):
                if not decision.get(key):
                    errors.append(f"{sid}: external blocker lacks {key}")
        if assessment == "executor_unfinished" and not row.get("unperformed_steps"):
            errors.append(f"{sid}: executor unfinished lacks specific steps")
    summary = {
        "gap_total": len(gaps),
        "categories": dict(Counter(r.get("category") for r in rows)),
        "processing_assessments": dict(Counter(r.get("processing_assessment") for r in rows)),
        "processing_completion": "NOT_VERIFIED" if any(r.get("processing_assessment") == "not_established" for r in rows)
        else "INCOMPLETE" if any(r.get("processing_assessment") == "executor_unfinished" for r in rows)
        else "EXTERNAL_GAPS_ONLY",
        "strict_coverage_status": "INCOMPLETE" if gaps else "PASS",
    }
    return errors, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    errors, summary = validate(json.loads(args.review.read_text()), json.loads(args.receipt.read_text()))
    print(json.dumps({"review_validation": "FAIL" if errors else "PASS", "errors": errors, **summary}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
