#!/usr/bin/env python3
"""Current-evidence and durable-work gate; never fetches sites or grants access.

init RUN_DIR freezes IDs/queues and creates an UNREVIEWED execution-review.json.
check RUN_DIR --receipt RECEIPT validates decisions; --queue-out PATH persists the
validated unresolved handoff. PASS validates the accounting, not medical truth.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from seo.catalog_selection import current_public

REGIONS = {"USA", "Canada", "UK", "continental Europe", "Latin America Caribbean",
           "Australia New Zealand", "East Asia", "South Asia", "Southeast Asia",
           "Middle East", "North Africa", "sub-Saharan Africa"}
PASSES = {"current_undated", "recent_seven_days"}
LEAD_STATES = {"ADDED", "VERIFIED_EXISTING", "DUPLICATE", "CLOSED_CONFIRMED",
               "NOT_TREATMENT", "PENDING_EVIDENCE", "BLOCKED", "SOURCE_INDEX_REVIEWED"}
RESOLVED_STATES = {"RESOLVED", "POLICY_RESOLVED"}
ISSUE_STATES = RESOLVED_STATES | {"OPEN_AVAILABLE", "BLOCKED", "DEFERRED", "OWNER_DECISION"}


def policy_resolution_valid(item, previous, root):
    """Owner-approved status/date decisions are not five-fact clinical reviews."""
    resolution = item.get("policy_resolution", {})
    policy_path = root / "data/audit_owner_policy.json"
    catalog_path = root / "data/trials_base.json"
    if (not policy_path.is_file() or not catalog_path.is_file()
            or not exists_refs(resolution.get("evidence_refs"), root)
            or not resolution.get("identity_comparison")
            or item.get("full_protocol_review_complete") is not False):
        return False
    policy = read(policy_path).get("rules", {})
    trial = next((t for t in read(catalog_path) if t.get("id") == item.get("trial_id")), {})
    rule = resolution.get("rule")
    if not policy.get(rule, {}).get("enabled") or not trial:
        return False
    if trial.get("verified") != item.get("previous_verified"):
        return False  # Policy application cannot manufacture a clinical-review date.
    if rule == "avma_closed":
        status = "".join(c for c in str(resolution.get("registry_status", "")).lower() if c.isalnum())
        return bool(trial.get("available_for_matching") is False
                    and status in {"completed", "completedwithresults", "closed", "terminated", "withdrawn"}
                    and trial.get("registry_status") == resolution.get("registry_status")
                    and trial.get("avma_vct_code") == resolution.get("avma_vct_code")
                    and resolution.get("avma_vct_code")
                    and item.get("resolved_scope") == "current_access")
    if rule == "study_end_as_recruitment_end":
        try:
            adopted = date.fromisoformat(resolution.get("published_study_end", ""))
        except (ValueError, TypeError):
            return False
        basis = trial.get("recruitment_end_basis", {})
        return bool(previous and previous.get("state") == "OWNER_DECISION"
                    and item.get("kind") == "full_protocol"
                    and item.get("resolved_scope") == "deadline_interpretation"
                    and trial.get("recruitment_end") == adopted.isoformat()
                    and basis.get("rule") == rule and basis.get("primary_url")
                    and basis.get("published_study_end") == adopted.isoformat()
                    and exists_refs(basis.get("evidence_refs"), root))
    return False


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result if result.tzinfo else None
    except (TypeError, ValueError, AttributeError):
        return None


def exists_refs(refs, root):
    """Saved local evidence only; a URL or nonempty prose is not an artifact."""
    if not isinstance(refs, list) or not refs:
        return False
    for ref in refs:
        if not isinstance(ref, str):
            return False
        path = root / ref
        if not path.is_file() or path.stat().st_size == 0:
            return False
    return True


def current_source_sufficient(source, review, root, start, end):
    """No previous status, old fingerprint or any(equal) completion shortcut."""
    at = timestamp(review.get("reviewed_at"))
    if not at or not start <= at <= end:
        return False
    actual = {a.get("evidence_file") for a in source.get("attempted_urls", [])
              if a.get("method") != "restriction_review_no_request"
              and timestamp(a.get("completed_at"))
              and start <= timestamp(a["completed_at"]) <= end}
    roster_refs = review.get("roster_evidence_refs", [])
    changed = {c.get("current_evidence") for c in source.get("current_content_comparison", [])
               if c.get("whole_text_equal") is False}
    examined = {c.get("current_evidence") for c in review.get("change_reviews", [])
                if c.get("finding") and c.get("catalog_impact")}
    return bool(review.get("current_official_content") is True
                and review.get("roster_complete") is True
                and isinstance(review.get("protocols"), list)
                and review.get("finding") and review.get("catalog_comparison")
                and exists_refs(roster_refs, root) and set(roster_refs) <= actual
                and None not in changed and changed <= examined)


def seed_queue(root, catalog, public, now):
    """Preserve prior issue identity; add actual due/missing work, never close it."""
    queue_path = root / "data/audit_execution_queue.json"
    queue = read(queue_path) if queue_path.exists() else {"schema_version": 1, "issues": []}
    previous = {x["issue_id"]: dict(x) for x in queue["issues"]}
    issues = {iid: item for iid, item in previous.items() if item.get("state") not in RESOLVED_STATES}
    state = read(root / "data/audit_state.json").get("protocol_selection_review", {})
    prior_path = root / state.get("progress_receipt", "__missing__")
    decisions = {x["trial_id"]: x for x in read(prior_path)} if prior_path.is_file() else {}
    cases = {x["trial_id"] for x in read(root / "data/protocol_selection_cases.json")["reviews"]}
    pending = {tid for tid, row in decisions.items()
               if row.get("status") == "current_full_protocol_not_verified"}
    # Also preserve the latest public full-review ledger, including inherited files.
    receipt_path = root / "data/audit_source_coverage.json"
    previous_run = read(receipt_path).get("run_id") if receipt_path.exists() else None
    if previous_run:
        directory = root / "research/audit-runs" / previous_run
        for name in ("trial-review-queue.json", "inherited-trial-review-queue.json"):
            path = directory / name
            if path.exists():
                pending.update(read(path).get("old_pending_remaining", []))
    for trial in public:
        tid = trial["id"]
        old_date = str(trial.get("verified") or "")[:10]
        try:
            due = date.fromisoformat(old_date) + timedelta(days=28) <= now.date()
        except ValueError:
            due = True
        kinds = (["full_protocol"] if tid in pending or due else [])
        if tid not in cases:
            kinds.append("independent_selection")
        for kind in kinds:
            iid = f"{kind}:{tid}"
            if kind == "full_protocol" and previous.get(iid, {}).get("state") in RESOLVED_STATES and not due:
                continue  # An obsolete historical pending list cannot reopen completed work.
            if iid not in issues:
                reviewed_before = previous.get(iid, {}).get("state") in RESOLVED_STATES
                issues[iid] = {"issue_id": iid, "trial_id": tid, "kind": kind,
                    "state": "UNTRIAGED", "primary_url": trial.get("url"),
                    "previous_verified": trial.get("verified"),
                    "question": (None if reviewed_before else decisions.get(tid, {}).get("remaining_fact")) or
                                "Read the full primary protocol and reconcile current published facts.",
                    "due_reason": "28_day_review" if reviewed_before and due else "retained_pending" if tid in pending else
                                  "missing_independent_cases" if kind == "independent_selection" else "28_day_review"}
    # Inactive/removal is not an automatic resolution of an inherited question.
    return {"schema_version": 1, "issues": list(issues.values()),
            "resolved_history": [x for x in previous.values() if x.get("state") in RESOLVED_STATES]}


def initialize(directory, root, now, scheduled=False):
    baseline_path = directory / "execution-baseline.json"
    if baseline_path.exists() or (directory / "execution-review.json").exists():
        raise ValueError("refusing to overwrite an existing execution snapshot")
    catalog = read(root / "data/trials_base.json")
    public = current_public(catalog)
    inventory = read(root / "data/source_inventory.json")["sources"]
    queue = seed_queue(root, catalog, public, now)
    deadline = now.replace(hour=6, minute=0, second=0, microsecond=0) if scheduled else now + timedelta(minutes=180)
    if deadline <= now:
        raise ValueError("scheduled initialization must precede the morning 06:00 boundary")
    baseline = {"schema_version": 1, "run_id": directory.name, "started_at": now.isoformat(),
        "execution_deadline": deadline.isoformat(), "scheduled": scheduled,
        "source_ids": [s["id"] for s in inventory], "catalog_ids": [t["id"] for t in catalog],
        "public_ids": [t["id"] for t in public], "issues": queue["issues"],
        "resolved_history": queue["resolved_history"],
        "input_hashes": {name: hashlib.sha256((root / "data" / name).read_bytes()).hexdigest()
                         for name in ["trials_base.json", "source_inventory.json", "audit_state.json",
                                      "protocol_selection_cases.json"]}}
    write(baseline_path, baseline)
    write(directory / "execution-review.json", {"schema_version": 1, "run_id": directory.name,
        "ended_at": None, "source_reviews": [], "issue_updates": [],
        "discovery_queries": [], "discovered_urls": [], "leads": [], "deadline_review_ref": None,
        "stop": {"reason": None, "detail": None, "evidence_refs": []}})
    return baseline


def validate(baseline, review, receipt, root):
    errors = []
    start, end = timestamp(baseline.get("started_at")), timestamp(review.get("ended_at"))
    if not start or not end or end < start:
        return ["valid timezone-aware start/end required"], {"status": "FAIL"}, []
    if baseline.get("run_id") != review.get("run_id") or receipt.get("run_id") != baseline.get("run_id"):
        errors.append("run IDs must match")
    def keyed(rows, key, label):
        ids = [r.get(key) for r in rows]
        if None in ids or len(ids) != len(set(ids)):
            errors.append(f"{label}: duplicate/missing IDs")
        return {r.get(key): r for r in rows}
    sources = keyed(receipt.get("sources", []), "source_id", "receipt")
    source_reviews = keyed(review.get("source_reviews", []), "source_id", "source reviews")
    added_sources = review.get("added_source_ids", [])
    if (not isinstance(added_sources, list)
            or len(added_sources) != len(set(added_sources))
            or set(added_sources) & set(baseline["source_ids"])):
        errors.append("added sources must be distinct new identities")
        added_sources = []
    if added_sources:
        inventory_path = root / "data/source_inventory.json"
        current_sources = {s["id"] for s in read(inventory_path)["sources"]} if inventory_path.is_file() else set()
        if not set(added_sources) <= current_sources:
            errors.append("added source identities must exist in the actual current inventory")
    expected_sources = set(baseline["source_ids"]) | set(added_sources)
    if set(sources) != expected_sources or set(source_reviews) != set(sources):
        errors.append("every frozen source needs one current decision")
    sufficient = 0
    available = []
    for sid, source in sources.items():
        decision = source_reviews.get(sid, {})
        derived = current_source_sufficient(source, decision, root, start, end)
        sufficient += derived
        if source.get("content_sufficient") is not derived:
            errors.append(f"{sid}: content_sufficient differs from current evidence")
        at = timestamp(decision.get("reviewed_at"))
        if not at or not start <= at <= end or not decision.get("finding"):
            errors.append(f"{sid}: missing current individual review")
        if not exists_refs(decision.get("evidence_refs"), root):
            errors.append(f"{sid}: missing saved decision evidence")
        steps = decision.get("remaining_available_steps")
        if not isinstance(steps, list):
            errors.append(f"{sid}: remaining_available_steps must be explicit")
        available.extend(f"{sid}: {s}" for s in steps or [])
        if source.get("processing_complete") and (steps or not decision.get("completion_basis")):
            errors.append(f"{sid}: processing completion unsupported")
    if receipt.get("content_sufficient_total") != sufficient:
        errors.append("source sufficient total must be derived from current decisions")

    old = keyed(baseline.get("issues", []), "issue_id", "baseline issues")
    updates = keyed(review.get("issue_updates", []), "issue_id", "issue updates")
    known_catalog_ids = set(baseline["catalog_ids"]) | set(review.get("added_catalog_ids", []))
    if review.get("added_catalog_ids"):
        current_ids = {x["id"] for x in read(root / "data/trials_base.json")}
        if not set(review["added_catalog_ids"]) <= current_ids:
            errors.append("added catalog identities must exist in the actual current canonical catalog")
    if set(old) - set(updates):
        errors.append("inherited issues omitted: " + ", ".join(sorted(set(old) - set(updates))))
    next_queue = []
    for iid, item in updates.items():
        previous = old.get(iid)
        if previous and any(item.get(k) != previous.get(k) for k in ("trial_id", "kind")):
            errors.append(f"{iid}: issue identity changed")
        if item.get("trial_id") not in known_catalog_ids:
            errors.append(f"{iid}: unknown trial identity")
        if item.get("kind") not in {"full_protocol", "independent_selection"}:
            errors.append(f"{iid}: unknown issue kind")
        state = item.get("state")
        at = timestamp(item.get("reviewed_at"))
        if state not in ISSUE_STATES or not at or not start <= at <= end:
            errors.append(f"{iid}: explicit current issue disposition required")
        if not item.get("finding") or not exists_refs(item.get("evidence_refs"), root):
            errors.append(f"{iid}: missing actual issue review evidence")
        if state == "POLICY_RESOLVED":
            if not policy_resolution_valid(item, previous, root):
                errors.append(f"{iid}: unsupported owner-policy resolution; not a clinical review")
        elif state == "RESOLVED":
            needed = {"identity", "recruitment_sites", "eligibility", "funding", "contacts"}
            if item.get("kind") == "full_protocol" and not needed <= set(item.get("facts_checked", [])):
                errors.append(f"{iid}: incomplete full protocol review")
            if item.get("kind") == "independent_selection" and not {"positive", "negative", "unknown"} <= set(item.get("cases_checked", [])):
                errors.append(f"{iid}: independent source-derived cases missing")
        else:
            if not item.get("question") or not item.get("next_action"):
                errors.append(f"{iid}: concrete remaining question/action required")
            if state == "BLOCKED" and not exists_refs(item.get("restriction_or_unpublished_evidence_refs"), root):
                errors.append(f"{iid}: blocker must reference exact restriction or published evidence gap")
            if state == "DEFERRED":
                after = timestamp(item.get("recheck_after"))
                if not after or after <= end or not item.get("deferral_basis"):
                    errors.append(f"{iid}: deferral requires a future date and reason")
                if item.get("deadline_crossed") or item.get("new_primary_signal"):
                    errors.append(f"{iid}: due signal cannot be deferred")
            if state == "OPEN_AVAILABLE":
                available.append(iid)
            next_queue.append({**(previous or {}), **item})

    queries = review.get("discovery_queries", [])
    coverage = {(q.get("region"), q.get("pass")) for q in queries
                if q.get("country") and q.get("language") and q.get("query")
                and exists_refs(q.get("evidence_refs"), root)}
    if not {(r, p) for r in REGIONS for p in PASSES} <= coverage:
        errors.append("discovery missing country/language-specific saved queries in required region/pass")
    lead_ids = []
    for lead in review.get("leads", []):
        lead_ids.append(lead.get("url"))
        state = lead.get("disposition")
        if state not in LEAD_STATES or not lead.get("reason") or not exists_refs(lead.get("evidence_refs"), root):
            errors.append(f"lead {lead.get('url')}: missing decision/evidence; known source is not a protocol identity")
        if state in {"ADDED", "VERIFIED_EXISTING", "DUPLICATE"}:
            ids = lead.get("canonical_ids", [])
            if not ids or not set(ids) <= set(baseline["catalog_ids"]) | set(review.get("added_catalog_ids", [])) or not lead.get("identity_comparison"):
                errors.append(f"lead {lead.get('url')}: exact canonical identity comparison required")
        if state not in {"NOT_TREATMENT", "SOURCE_INDEX_REVIEWED"} and not lead.get("primary_url") and not (
                state in {"PENDING_EVIDENCE", "BLOCKED"} and lead.get("missing_primary_reason")):
            errors.append(f"lead {lead.get('url')}: primary protocol URL or explicit unknown required")
        if state == "SOURCE_INDEX_REVIEWED" and not lead.get("protocol_links_examined"):
            errors.append(f"lead {lead.get('url')}: index requires actual protocol-link reconciliation")
        if lead.get("unperformed_steps"):
            available.extend(lead["unperformed_steps"])
    expected_leads = review.get("discovered_urls")
    if not isinstance(expected_leads, list) or set(expected_leads) != set(lead_ids) or len(lead_ids) != len(set(lead_ids)):
        errors.append("all discovered URLs must receive one disposition")
    ref = review.get("deadline_review_ref")
    if not ref or not exists_refs([ref], root):
        errors.append("daily deadline ledger missing")
    else:
        ledger = read(root / ref)
        ids = [r.get("record_id") for r in ledger.get("rows", [])]
        if len(ids) != len(set(ids)) or set(ids) != set(baseline["catalog_ids"]):
            errors.append("deadline ledger must cover every frozen canonical ID")

    stop = review.get("stop", {})
    reason = stop.get("reason")
    if reason not in {"completed_available_work", "time_limit", "runtime_failure"} or not stop.get("detail"):
        errors.append("explicit stop reason/detail required")
    if reason == "completed_available_work" and available:
        errors.append("cannot finish available work while permitted tasks remain")
    if reason == "time_limit":
        limit = timestamp(stop.get("deadline"))
        planned = timestamp(baseline.get("execution_deadline"))
        if not limit or not planned or limit != planned or end < planned:
            errors.append("time limit not reached")
    if reason == "runtime_failure" and not exists_refs(stop.get("evidence_refs"), root):
        errors.append("runtime failure needs saved error evidence")
    summary = {"status": "FAIL" if errors else "PASS", "source_sufficient": sufficient,
        "source_total": len(sources), "baseline_source_total": len(baseline["source_ids"]),
        "sources_added": len(added_sources), "issues_before": len(old),
        "issues_resolved": sum(x.get("state") in RESOLVED_STATES for x in updates.values()),
        "policy_questions_resolved": sum(x.get("state") == "POLICY_RESOLVED" for x in updates.values()),
        "issues_remaining": len(next_queue), "available_remaining": available,
        "issue_states": dict(Counter(x.get("state") for x in updates.values())),
        "execution": "INCOMPLETE" if available or any(not x.get("processing_complete") for x in sources.values()) else "PASS",
        "clinical_reconciliation": "INCOMPLETE" if next_queue else "PASS",
        "discovery": "INCOMPLETE" if any(x.get("disposition") in {"PENDING_EVIDENCE", "BLOCKED"}
                                            for x in review.get("leads", [])) else "PASS_WITH_COVERAGE_LIMITS",
        "scope": "Accounting/evidence gate; not independent medical verification or exhaustive global coverage."}
    history = {x["issue_id"]: x for x in baseline.get("resolved_history", [])}
    history.update(updates)
    return errors, summary, list(history.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["init", "check"])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--queue-out", type=Path)
    parser.add_argument("--scheduled", action="store_true", help="freeze the morning 06:00 local boundary")
    args = parser.parse_args()
    if args.action == "init":
        baseline = initialize(args.run_dir, ROOT, datetime.now(ZoneInfo("America/New_York")), args.scheduled)
        print(json.dumps({"status": "INITIALIZED_NOT_REVIEWED", "issues": len(baseline["issues"])}))
        return
    if not args.receipt:
        parser.error("check requires --receipt")
    errors, summary, queue = validate(read(args.run_dir / "execution-baseline.json"),
        read(args.run_dir / "execution-review.json"), read(args.receipt), ROOT)
    write(args.run_dir / "execution-validation.json", {**summary, "errors": errors})
    if args.queue_out:
        if errors:
            parser.error("invalid accounting cannot replace durable queue; save incomplete checkpoint separately")
        write(args.queue_out, {"schema_version": 1, "last_run_id": args.run_dir.name, "issues": queue})
    print(json.dumps({**summary, "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
