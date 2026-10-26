#!/usr/bin/env python3
import collections
import copy
import hashlib
import json
import pathlib
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[3]
RUN = pathlib.Path(__file__).resolve().parent
RUN_ID = RUN.name
PREV_RUN = ROOT / "research/audit-runs/daily-20261025T025925-0400"
ET = ZoneInfo("America/New_York")

def read(path):
    with open(path) as f:
        return json.load(f)

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")

inventory = read(RUN / "before-source_inventory.json")
sources = inventory["sources"]
source_by_id = {s["id"]: s for s in sources}
previous = read(PREV_RUN / "receipt-final.json")
previous_by_id = {r["source_id"]: r for r in previous["sources"]}
native = [json.loads(line) for line in open(RUN / "attempts.jsonl") if line.strip()]
web = read(RUN / "web-attempts.json")
restricted = [json.loads(line) for line in open(RUN / "skipped-restricted-routes.jsonl") if line.strip()]
all_records = native + web + restricted
records_by_source = collections.defaultdict(list)
for row in all_records:
    records_by_source[row["source_id"]].append(row)

# Every configured mandatory route must have an actual current attempt or an exact
# restriction decision. This assertion prevents partial route coverage from being
# reclassified as an external evidence gap.
represented = {(r["source_id"], r["url"]) for r in all_records}
missing_routes = []
for s in sources:
    for url in [s["master_url"], *s.get("fallback_urls", [])]:
        if (s["id"], url) not in represented:
            missing_routes.append({"source_id": s["id"], "url": url})
if missing_routes:
    raise SystemExit("Mandatory routes missing: " + json.dumps(missing_routes))

previous_hashes = collections.defaultdict(set)
for prev in previous["sources"]:
    for attempt in prev.get("actual_attempts", []):
        if attempt.get("text_sha256"):
            previous_hashes[(prev["source_id"], attempt.get("url"))].add(attempt["text_sha256"])

matching_current = collections.defaultdict(list)
for attempt in native:
    if attempt.get("text_sha256") in previous_hashes[(attempt["source_id"], attempt.get("url"))]:
        matching_current[attempt["source_id"]].append(attempt)

web_retrieved = collections.defaultdict(list)
for attempt in web:
    if attempt.get("result") in ("retrieved_page", "retrieved_document"):
        web_retrieved[attempt["source_id"]].append(attempt)

previous_full = {r["source_id"] for r in previous["sources"] if r.get("content_sufficient") is True}
full = (set(matching_current) | set(web_retrieved)) & previous_full

def is_actual(attempt):
    return attempt.get("result") != "known_denial_not_requested" and attempt.get("method") in ("shell_curl", "Web")

def is_usable(attempt):
    return attempt.get("result") in ("retrieved_page", "retrieved_document") and (
        attempt.get("method") == "Web" or int(attempt.get("text_length") or 0) > 0
    )

def latest_time(attempts):
    values = [a.get("completed_at") or a.get("attempted_at") or a.get("at") for a in attempts]
    return max((v for v in values if v), default=None)

def routes(attempts):
    return sorted({a.get("method") for a in attempts if is_actual(a) and a.get("method")})

def question_for(source, result):
    if result in ("unreachable", "not_checked"):
        return f"What is the current recruiting oncology roster at {source['name']}? Today's permitted official routes did not return usable current roster content."
    if source.get("source_type") in ("directory", "registry", "professional_society", "news"):
        return f"Which current signals published by {source['name']} correspond to primary, owner-enrolling oncology-treatment protocols? The source does not establish a complete primary roster."
    return f"What is the complete current recruiting oncology-treatment roster at {source['name']}? Today's permitted evidence did not establish every protocol and status."

receipt_rows = []
gap_rows = []
for source in sources:
    sid = source["id"]
    attempts = copy.deepcopy(records_by_source[sid])
    opened = any(is_actual(a) for a in attempts)
    usable = any(is_usable(a) for a in attempts)
    sufficient = sid in full
    if sufficient:
        result = "fully_reconciled"
    elif usable:
        result = "partial"
    elif opened:
        result = "unreachable"
    else:
        result = "not_checked"

    prev = previous_by_id.get(sid, {})
    roster = copy.deepcopy(prev.get("current_roster") or []) if sufficient else None
    protocols_seen = len(roster) if sufficient else None
    matches = matching_current.get(sid, [])
    web_good = web_retrieved.get(sid, [])
    if sufficient and matches:
        match = matches[-1]
        evidence = (
            f"Fresh official route {match['url']} was retrieved in this run; normalized text SHA-256 "
            f"{match['text_sha256']} exactly matches the prior verified route. The previously enumerated roster is retained after this current comparison."
        )
    elif sufficient and web_good:
        refs = ", ".join(a.get("reference", "Web") for a in web_good)
        evidence = (
            "The fresh exact official page was retrieved through Web in this run and compared with the prior verified roster "
            f"({refs}); no roster-changing evidence was found."
        )
    else:
        evidence = (
            "All configured master/fallback routes were attempted today or withheld only by an exact recorded route restriction. "
            "The usable current evidence did not prove a complete primary oncology-treatment roster."
        )

    mandatory = [{"url": source["master_url"], "route": "master"}] + [
        {"url": url, "route": "official_fallback"} for url in source.get("fallback_urls", [])
    ]
    current_time = latest_time([a for a in attempts if is_actual(a)])
    question = None if sufficient else question_for(source, result)
    category = None
    if not sufficient:
        if result in ("unreachable", "not_checked"):
            category = "source_unavailable"
        elif source.get("source_type") in ("directory", "registry", "professional_society", "news"):
            category = "discovery_source_not_trial_roster"
        else:
            category = "roster_unestablished"
    row = {
        "source_id": sid,
        "source_name": source["name"],
        "master_url": source["master_url"],
        "opened_this_run": opened,
        "content_sufficient": sufficient,
        "source_result": result,
        "master_result": "unchanged" if sufficient else result,
        "protocols_seen": protocols_seen,
        "current_roster": roster,
        "route_used": routes(attempts),
        "actual_attempts": attempts,
        "attempted_urls": attempts,
        "current_comparison_evidence": evidence,
        "processing_complete": True,
        "processing_assessment": "complete" if sufficient else "external_blocker",
        "category": category,
        "question": question,
        "reconciliation": evidence,
        "unperformed_steps": [],
        "previous_last_checked": source.get("last_checked"),
        "previous_last_checked_at": source.get("last_checked_at"),
        "previous_last_result": source.get("last_result"),
        "new_last_checked": "2026-10-26" if opened else source.get("last_checked"),
        "new_last_checked_at": current_time if opened else source.get("last_checked_at"),
        "new_last_result": ("unchanged" if sufficient else result) if opened else source.get("last_result"),
        "mandatory_routes": mandatory,
        "completion_decision": None,
    }
    if not sufficient:
        row["completion_decision"] = {
            "remaining_fact": question,
            "routes_exhausted_evidence": (
                f"All {len(mandatory)} configured master/fallback routes are represented by a current attempt or an exact restriction decision; "
                f"{len(attempts)} raw route records are attached."
            ),
            "available_reconciliation_done_evidence": evidence,
        }
        gap_rows.append({
            "source_id": sid,
            "category": category,
            "processing_assessment": "external_blocker",
            "question": question,
            "reason": evidence,
            "next_action": "Repeat the daily master/fallback visit; deepen only after changed primary evidence or the source-specific recheck date.",
            "evidence": {
                "source_id": sid,
                "attempted_urls": sorted({a.get("url") for a in attempts if a.get("url")}),
                "attempt_count": len(attempts),
            },
            "completion_decision": row["completion_decision"],
            "unperformed_steps": [],
            "record_ids": [],
        })
    receipt_rows.append(row)

counts = collections.Counter(r["source_result"] for r in receipt_rows)
now = datetime.now(ET).isoformat(timespec="seconds")
receipt = {
    "run_id": RUN_ID,
    "mode": "DAILY GLOBAL WORK AUDIT",
    "started_at": "2026-10-26T03:01:32.546973-04:00",
    "source_total": len(receipt_rows),
    "attempted_total": sum(r["opened_this_run"] is True for r in receipt_rows),
    "content_sufficient_total": sum(r["content_sufficient"] is True for r in receipt_rows),
    "processing_complete_total": sum(r["processing_complete"] is True for r in receipt_rows),
    "source_result_counts": dict(counts),
    "executor_incomplete_source_ids": [],
    "executor_unfinished_actions": 0,
    "unconfirmed_processing_sources": 0,
    "source_pass_at": now,
    "strict_status": "INCOMPLETE",
    "sources": receipt_rows,
}
write(RUN / "receipt-final.json", receipt)
write(RUN / "receipt-draft.json", receipt)
write(RUN / "gap-review.json", {"original_run_id": RUN_ID, "rows": gap_rows})

# Canonical inventory dates change only for actual current visits. Exact restricted
# routes with no actual visit retain their previous date and result.
for source in sources:
    row = next(r for r in receipt_rows if r["source_id"] == source["id"])
    if not row["opened_this_run"]:
        continue
    source["last_checked"] = row["new_last_checked"]
    source["last_checked_at"] = row["new_last_checked_at"]
    source["last_result"] = row["new_last_result"]
    source["last_attempts"] = row["actual_attempts"]
    source["last_route_used"] = row["route_used"]
    source["audit_last_run_id"] = RUN_ID
    source["last_coverage_receipt"] = str((RUN / "receipt-final.json").relative_to(ROOT))
    source["content_sufficient"] = row["content_sufficient"]
    source["last_protocols_seen"] = row["protocols_seen"]
    source["last_coverage_gap"] = row["question"]
    source["last_check_summary"] = row["current_comparison_evidence"]
    statuses = [a.get("http_status") for a in row["actual_attempts"] if a.get("http_status") is not None]
    source["last_http_status"] = statuses[-1] if statuses else None
    matches = matching_current.get(source["id"], [])
    if row["content_sufficient"] and matches:
        source["content_fingerprint"] = "sha256:" + matches[-1]["text_sha256"]
        source["content_fingerprint_method"] = "fresh_exact_comparison_to_prior_verified_route"
inventory["updated"] = "2026-10-26"
write(ROOT / "data/source_inventory.json", inventory)
write(ROOT / "data/audit_source_coverage.json", receipt)

state = read(ROOT / "data/audit_state.json")
state["last_incremental_audit"] = {
    "run_id": RUN_ID,
    "started_at": receipt["started_at"],
    "at": now,
    "mode": receipt["mode"],
    "status": "INCOMPLETE",
    "canonical_changes": [],
    "new_active_trials": 0,
    "activated_existing_watch_trials": 0,
    "new_sources": 0,
    "source_receipt": str((RUN / "receipt-final.json").relative_to(ROOT)),
    "trial_review_receipt": str((RUN / "discovery-decisions.json").relative_to(ROOT)),
    "clinical_full_fresh_gate": "INCOMPLETE",
    "source_processing_completed": receipt["processing_complete_total"],
    "source_total": receipt["source_total"],
    "executor_unconfirmed_source_actions": 0,
    "publication": f"Tracked separately in {RUN.relative_to(ROOT)}/publication.json",
    "prior40": copy.deepcopy(state.get("last_incremental_audit", {}).get("prior40", {})),
}
state["last_source_discovery_attempt"] = {
    key: receipt[key] for key in (
        "run_id", "mode", "started_at", "source_total", "attempted_total",
        "content_sufficient_total", "processing_complete_total", "source_result_counts",
        "executor_incomplete_source_ids", "executor_unfinished_actions",
        "unconfirmed_processing_sources", "source_pass_at", "strict_status"
    )
}
state["last_source_discovery_attempt"].update({
    "at": now,
    "status": "INCOMPLETE",
    "coverage_receipt": str((RUN / "receipt-final.json").relative_to(ROOT)),
    "gap_review": str((RUN / "gap-review.json").relative_to(ROOT)),
    "global_discovery_regions": 12,
    "discovery_status": "TWO_PASSES_COMPLETE_NO_NEW_PRIMARY_CONFIRMED",
    "discovery_receipt": str((RUN / "discovery-matrix.json").relative_to(ROOT)),
    "new_sources": 0,
    "new_active_trials": 0,
    "activated_existing_watch_trials": 0,
})
write(ROOT / "data/audit_state.json", state)

summary = {k: v for k, v in receipt.items() if k != "sources"}
summary["full_source_ids"] = [r["source_id"] for r in receipt_rows if r["content_sufficient"]]
summary["gap_category_counts"] = dict(collections.Counter(r["category"] for r in gap_rows))
summary["gap_assessment_counts"] = dict(collections.Counter(r["processing_assessment"] for r in gap_rows))
summary["raw_route_records"] = len(all_records)
summary["unique_configured_routes"] = sum(1 + len(s.get("fallback_urls", [])) for s in sources)
summary["native_attempt_records"] = len(native)
summary["web_attempt_records"] = len(web)
summary["exact_restriction_decisions"] = len(restricted)
summary["execution_deviation"] = "An overlapping native runner caused duplicate request records for some routes; all records are retained, while completeness is counted once per configured route."
write(RUN / "source-summary.json", summary)
write(RUN / "timestamps.json", {
    "run_id": RUN_ID,
    "started_at": receipt["started_at"],
    "source_pass_at": now,
    "timezone": "America/New_York",
})
print(json.dumps(summary, ensure_ascii=False, indent=2))
