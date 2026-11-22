#!/usr/bin/env python3
"""Save validator receipts, source-date provenance, catalog stats and audit state."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_ID = HERE.name
RUN_REF = f"research/audit-runs/{RUN_ID}"


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


review = read(HERE / "execution-review.json")
receipt = read(HERE / "receipt-final.json")
deadline = read(HERE / "deadline-review.json")
execution_validation = json.loads((HERE / "execution-gate-check.txt").read_text())
strict_validation = json.loads((HERE / "strict-receipt-check.txt").read_text())
gap_validation = json.loads((HERE / "gap-review-check.txt").read_text())
write(HERE / "execution-validation.json", execution_validation)
write(HERE / "strict-receipt-validation.json", strict_validation)
write(HERE / "gap-validation.json", gap_validation)


current_inventory = read(ROOT / "data/source_inventory.json")
baseline_inventory = json.loads(subprocess.check_output(
    ["git", "show", "HEAD:data/source_inventory.json"], cwd=ROOT, text=True
))
before = {x["id"]: x for x in baseline_inventory["sources"]}
date_rows = []
for row in current_inventory["sources"]:
    old = before[row["id"]]
    advanced = row.get("last_checked_at") != old.get("last_checked_at")
    date_rows.append({
        "source_id": row["id"],
        "previous_last_checked": old.get("last_checked"),
        "previous_last_checked_at": old.get("last_checked_at"),
        "saved_last_checked": row.get("last_checked"),
        "saved_last_checked_at": row.get("last_checked_at"),
        "advanced": advanced,
        "basis": "web_response_labelled_crawled_today" if advanced else "no_current_fresh_body_or_exact_restriction_only_date_preserved",
    })
write(HERE / "source-date-delta.json", {
    "run_id": RUN_ID,
    "recorded_at": review["ended_at"],
    "rows": date_rows,
    "summary": {"sources": len(date_rows), "advanced": sum(x["advanced"] for x in date_rows), "preserved": sum(not x["advanced"] for x in date_rows)},
})


write(HERE / "avma-current-review.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "status": "NOT_VERIFIED",
    "recorded_at": review["ended_at"],
    "routes": [
        "https://veterinaryclinicaltrials.org/studies/?term~studypage_status=R&term~sc_paths=primary-field-19_oncology-1",
        "https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip=0&take=500",
        "https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip=500&take=500",
        "https://veterinaryclinicaltrials.org/",
    ],
    "finding": "All four permitted routes received bounded native attempts. Shell transport failed; same-URL Web fallback could read only the root iframe and returned tool-inaccessible errors for the filtered roster and both JSON pages. No current AVMA objects, counts, identities, or status changes are asserted.",
    "historical_comparison_only": "The prior run's AVMA counts remain historical evidence and were not reused as today's roster.",
    "evidence_refs": [f"{RUN_REF}/current-source-evidence.json", f"{RUN_REF}/current-source-web-summary.json"],
})


catalog = read(ROOT / "data/trials_base.json")
from seo.catalog_selection import current_public
public = current_public(catalog)
treatment = [x for x in public if x.get("study_type") == "treatment" and x.get("available_for_matching") is True]
country = Counter(str(x.get("country") or "Unknown") for x in treatment)
species = Counter()
for trial in treatment:
    value = trial.get("species")
    values = value if isinstance(value, list) else [value]
    for item in values:
        species[str(item or "Unknown")] += 1
catalog_stats = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "catalog_sha256": hashlib.sha256((ROOT / "data/trials_base.json").read_bytes()).hexdigest(),
    "effective_records": len(catalog),
    "current_public_records": len(public),
    "strict_treatment_opportunities": len(treatment),
    "treatment_access_programs": len(public) - len(treatment),
    "strict_treatment_by_country": dict(sorted(country.items())),
    "strict_treatment_by_species": dict(sorted(species.items())),
    "added_ids": [],
    "substantively_updated_ids": [],
    "closed_or_deleted_ids": [],
    "watchlist_or_inactive_records": len(catalog) - len(public),
    "catalog_change": "NO_CHANGE",
}
write(HERE / "catalog-statistics.json", catalog_stats)


write(HERE / "selection-validation.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "catalog_sha256": catalog_stats["catalog_sha256"],
    "records_checked": len(catalog),
    "public_records_checked": len(public),
    "catalog_change": "NO_CHANGE",
    "independent_source_cases": "PASS: SOURCE_DERIVED_SELECTION_OK public_reviewed=142/153 pending=11 retained_reviews=157 cases=1336",
    "generated_selection_matrix": "PASS: canonical=323 public=153 checks=1471 criteria=222",
    "browser_python_parity": "PASS: public=153 disease_checks=18360",
    "catalog_loading": "PASS: Japan=14, USA=96 after delayed load",
    "production_sync": "PASS: total=153 treatment=150 access=3",
    "unclassified_keys": [],
    "unreachable_public_records": 0,
    "unresolved_medical_or_selector_issues": 11,
    "evidence_refs": [f"{RUN_REF}/build-and-matcher-tests.txt"],
})


write(HERE / "validation-results.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "execution_gate": execution_validation,
    "strict_receipt": {"status": strict_validation["status"], "coverage_gap_count": strict_validation["coverage_gap_count"], "errors": strict_validation["errors"]},
    "gap_review": gap_validation,
    "catalog_validator": "PASS records=323 active=153",
    "source_inventory_validator": "PASS sources=168",
    "catalog_sanitation": "PASS with 4 known unresolved partial records and no new partial records",
    "repository_hygiene": "PASS",
    "audit_gate_tests": "PASS 29 tests",
    "matcher_and_build": "PASS",
    "evidence_key_scan": "PASS",
    "evidence_refs": [f"{RUN_REF}/validators-prebuild.txt", f"{RUN_REF}/audit-gate-tests.txt", f"{RUN_REF}/build-and-matcher-tests.txt", f"{RUN_REF}/evidence-key-check.txt"],
})


state_path = ROOT / "data/audit_state.json"
state = read(state_path)
previous = state.get("last_incremental_audit")
state["previous_incremental_audit"] = previous
state["last_incremental_audit"] = {
    "run_id": RUN_ID,
    "started_at": receipt["started_at"],
    "ended_at": review["ended_at"],
    "status": "INCOMPLETE",
    "sources_total": receipt["source_total"],
    "sources_processed": receipt["processing_complete_total"],
    "sources_attempted": receipt["attempted_total"],
    "content_sufficient": receipt["content_sufficient_total"],
    "queue_processing": execution_validation["execution"],
    "clinical_reconciliation": execution_validation["clinical_reconciliation"],
    "discovery": "INCOMPLETE_NO_NEW_CONFIRMED_AVAILABLE_PROTOCOL",
    "strict_receipt": strict_validation["status"],
    "accounting_validator": execution_validation["status"],
    "public_count": len(public),
    "new_canonical_trials": 0,
    "receipt": f"{RUN_REF}/receipt-final.json",
    "execution_review": f"{RUN_REF}/execution-review.json",
    "deadline_review": f"{RUN_REF}/deadline-review.json",
    "publication": "PENDING",
    "production_readback": f"{RUN_REF}/production-readback.json",
    "published_data_commit": None,
}
state["last_source_discovery_attempt"] = "2026-11-22"
state["last_deadline_review"] = {
    "run_id": RUN_ID,
    "evidence": f"{RUN_REF}/deadline-review.json",
    "summary": {
        "records": deadline["summary"]["records"],
        "published_dates": deadline["summary"]["with_published_recruitment_end"],
        "crossed": deadline["summary"]["deadline_crossed"],
        "crossed_still_matchable": deadline["summary"]["passed_and_matchable"],
        "extensions": deadline["summary"]["extensions_found"],
    },
}
state["last_run_id"] = RUN_ID
state["last_audit_at"] = review["ended_at"]
state["last_receipt"] = f"{RUN_REF}/receipt-final.json"
state["last_execution_review"] = {
    "run_id": RUN_ID,
    "evidence": f"{RUN_REF}/execution-review.json",
    "status": execution_validation["status"],
    "validation": f"{RUN_REF}/execution-validation.json",
}
write(state_path, state)

print(json.dumps({
    "source_dates_advanced": sum(x["advanced"] for x in date_rows),
    "catalog": catalog_stats,
    "audit_state": "updated_prepublication",
}, ensure_ascii=False, indent=2))
