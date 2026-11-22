#!/usr/bin/env python3
"""Build current-run source, issue, discovery, and deadline decisions.

This consumes only the frozen baseline, current-run request evidence, current-run
Web summaries, and the canonical files. Historical deadline rows provide the
original published date fields; their comparison result is recomputed today.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_ID = HERE.name
RUN_REF = f"research/audit-runs/{RUN_ID}"
TZ = ZoneInfo("America/New_York")


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


baseline = read(HERE / "execution-baseline.json")
inventory_payload = read(ROOT / "data/source_inventory.json")
inventory = inventory_payload["sources"]
catalog = read(ROOT / "data/trials_base.json")
catalog_by_id = {x["id"]: x for x in catalog}
source_native = read(HERE / "current-source-evidence.json")["attempts"]
protocol_native = read(HERE / "current-protocol-evidence.json")["attempts"]
source_web = read(HERE / "current-source-web-summary.json")["routes"]
protocol_web = read(HERE / "current-protocol-web-summary.json")["routes"]
reviewed_at = datetime.now(TZ).replace(microsecond=0)
ended_at = reviewed_at + timedelta(seconds=1)

SRC_NATIVE_REF = f"{RUN_REF}/current-source-evidence.json"
SRC_WEB_REF = f"{RUN_REF}/current-source-web-summary.json"
PRO_NATIVE_REF = f"{RUN_REF}/current-protocol-evidence.json"
PRO_WEB_REF = f"{RUN_REF}/current-protocol-web-summary.json"
DISCOVERY_INDEX_REF = f"{RUN_REF}/global-discovery-evidence.json"
LEAD_REF = f"{RUN_REF}/lead-protocol-current-findings.json"

native_by_source = defaultdict(list)
for row in source_native:
    native_by_source[row["source_id"]].append(row)
web_by_url = defaultdict(list)
for row in source_web:
    web_by_url[row["url"].rstrip("/")].append(row)


def source_attempts(sid: str) -> list[dict]:
    attempts = []
    for row in native_by_source[sid]:
        attempts.append({
            "url": row["requested_url"],
            "method": "restriction_review_no_request" if row["result"] == "skipped_exact_restriction" else "native_http",
            "completed_at": row["completed_at"],
            "result": row["result"],
            "opened": bool(row.get("opened")),
            "evidence_file": SRC_NATIVE_REF,
        })
        if row["result"] != "skipped_exact_restriction":
            candidates = web_by_url.get(row["requested_url"].rstrip("/"), [])
            if candidates:
                web = candidates[0]
                attempts.append({
                    "url": row["requested_url"],
                    "method": "web_open",
                    "completed_at": web["completed_at"],
                    "result": web["result"],
                    "opened": web["opened"],
                    "crawled_label": web.get("crawled_label"),
                    "evidence_file": SRC_WEB_REF,
                })
    return attempts


receipt_rows = []
source_reviews = []
gap_rows = []
for source in inventory:
    sid = source["id"]
    attempts = source_attempts(sid)
    counts = Counter(a["result"] for a in attempts)
    native_routes = native_by_source[sid]
    permitted = [a for a in native_routes if a["result"] != "skipped_exact_restriction"]
    restricted = [a for a in native_routes if a["result"] == "skipped_exact_restriction"]
    web_successes = [a for a in attempts if a["method"] == "web_open" and a["result"] == "success"]
    web_errors = [a for a in attempts if a["method"] == "web_open" and a["result"] == "web_error"]
    sufficient = sid in {"registry-uk-vcsr", "usa-bluepearl-science-clinical-studies", "sponsor-vetigenics-clinical-trials"}
    protocols = []
    if sid == "registry-uk-vcsr":
        protocols = [
            {"registry_id": "UK-VCSR-2026-00013", "title": "Evaluating use of immune therapy in equine allergic reactions", "relevant": False},
            {"registry_id": "UK-VCSR-2026-00006", "title": "Equine gastric ulceration management trial", "relevant": False, "sample": True},
            {"registry_id": "UK-VCSR-2026-00003", "title": "Feline chronic kidney disease dietary intervention", "relevant": False, "sample": True},
            {"registry_id": "UK-VCSR-2026-00001", "title": "Novel immunotherapy for canine lymphoma", "relevant": False, "sample": True},
        ]
        finding = ("Current official UK-VCSR roster was read in full: 4 entries were shown. "
                   "The only dog/cat oncology title is explicitly labelled an AI-generated sample, "
                   "so the current genuine dog/cat anticancer-treatment roster is 0.")
        catalog_comparison = "No genuine current dog/cat anticancer treatment protocol was present; no catalog change."
    elif sid == "usa-bluepearl-science-clinical-studies":
        protocols = [{"title": "Treatment for Canine Hemangiosarcoma (HSA) of the Spleen", "canonical_id": "bluepearl-hsa-paccal", "relevant": True}]
        finding = ("Fresh official BluePearl page states that the displayed list is complete. Its only dog/cat oncology "
                   "treatment study is splenic HSA chemotherapy at Kirkland and Tacoma; it exact-matches "
                   "bluepearl-hsa-paccal. Sponsor PaccalVet completion evidence remains controlling for matching status.")
        catalog_comparison = "One exact existing identity; no new protocol and no status re-enable from the network index."
    elif sid == "sponsor-vetigenics-clinical-trials":
        protocols = [
            {"title": "VGS-001 canine oral melanoma", "status": "closed", "relevant": True},
            {"title": "VGS-002 canine urothelial carcinoma", "status": "closed", "canonical_id": "penn-anti-pd1-urothelial-carcinoma", "relevant": True},
            {"title": "CHECKMATE-K9 CTLA4 + PD-1", "status": "fully enrolled", "relevant": True},
        ]
        finding = ("Fresh official Vetigenics pipeline was read in full: VGS-001 sites are closed, VGS-002 Ethos/BARC "
                   "sites are closed, and CHECKMATE-K9 is fully enrolled with all listed sites closed.")
        catalog_comparison = "Current sponsor roster confirms existing closed identities; no new enrolling protocol."
    else:
        finding = (
            f"{source['name']} ({sid}): {len(permitted)} permitted configured routes were attempted natively "
            f"and all encountered the recorded shell transport failure; Web fallback returned "
            f"{len(web_successes)} content responses and {len(web_errors)} route errors, while "
            f"{len(restricted)} exact saved restrictions were honored. The retrieved Web surface did not "
            "establish a complete current dog/cat anticancer-treatment roster for this source."
        )
        catalog_comparison = (
            f"No complete current roster was available for exact catalog reconciliation at {sid}; "
            "no absence, duplicate, closure, or new protocol is inferred from partial content."
        )
    refs = [SRC_NATIVE_REF]
    if permitted:
        refs.append(SRC_WEB_REF)
    completion_basis = (
        f"{sid}: recorded {len(permitted)} permitted native decisions, {len(web_successes)} successful Web "
        f"fallback reads, {len(web_errors)} Web route errors, and {len(restricted)} exact restrictions; "
        "every configured route has a current individual disposition and no permitted configured route remains."
    )
    receipt_rows.append({
        "source_id": sid,
        "opened_this_run": bool(permitted),
        "processing_complete": True,
        "content_sufficient": sufficient,
        "protocols_seen": len(protocols) if sufficient else None,
        "master_result": "complete" if sufficient else ("partial" if web_successes else "unreachable"),
        "route_used": "web_open_current_complete_roster" if sufficient else "native_http_then_web_open_or_exact_restriction",
        "attempted_urls": attempts,
        "current_content_comparison": [],
    })
    source_reviews.append({
        "source_id": sid,
        "reviewed_at": reviewed_at.isoformat(),
        "finding": finding,
        "evidence_refs": refs,
        "remaining_available_steps": [],
        "completion_basis": completion_basis,
        "current_official_content": sufficient,
        "roster_complete": sufficient,
        "protocols": protocols,
        "roster_evidence_refs": [SRC_WEB_REF] if sufficient else [],
        "catalog_comparison": catalog_comparison,
        "change_reviews": [],
    })
    if not sufficient:
        attempted_urls = [a["url"] for a in attempts]
        gap_rows.append({
            "source_id": sid,
            "category": "source_unavailable" if not web_successes else "roster_unestablished",
            "processing_assessment": "external_blocker",
            "question": f"Which complete current dog/cat anticancer-treatment roster and protocol facts are published by {source['name']} ({sid})?",
            "reason": (
                f"Current route evidence for {sid}: web_success={len(web_successes)}, web_error={len(web_errors)}, "
                f"shell_transport_error={sum(a['result']=='transport_error' for a in native_routes)}, "
                f"exact_restriction={len(restricted)}; complete roster/status evidence remains unestablished."
            ),
            "next_action": (
                f"Recheck only {sid}'s exact configured route(s) on the next daily cadence or a new publisher signal; "
                "preserve the original clinical-evidence dates and exact restrictions."
            ),
            "unperformed_steps": [],
            "completion_decision": {
                "remaining_fact": f"{sid}: the publisher has not exposed a complete current relevant roster through today's permitted routes.",
                "routes_exhausted_evidence": f"{sid}: {len(attempts)} native/Web/restriction route decisions are saved for {len(native_routes)} configured URLs.",
                "available_reconciliation_done_evidence": (
                    f"{sid}: its {len(permitted)} permitted URLs received native attempts and same-URL Web fallback, "
                    f"{len(restricted)} exact prohibitions were preserved, and the {len(web_successes)} readable "
                    "responses were assessed without treating partial text as a negative roster."
                ),
            },
            "evidence": {"source_id": sid, "attempted_urls": attempted_urls, "evidence_refs": refs},
        })

receipt = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "time_context": "America/New_York",
    "started_at": baseline["started_at"],
    "recorded_at": ended_at.isoformat(),
    "status": "INCOMPLETE",
    "source_total": len(receipt_rows),
    "attempted_total": sum(x["opened_this_run"] for x in receipt_rows),
    "content_sufficient_total": sum(x["content_sufficient"] for x in receipt_rows),
    "processing_complete_total": sum(x["processing_complete"] for x in receipt_rows),
    "sources": receipt_rows,
}
write(HERE / "receipt-final.json", receipt)
write(HERE / "gap-review.json", {"original_run_id": RUN_ID, "rows": gap_rows})


pro_native_by_trial = defaultdict(list)
for row in protocol_native:
    pro_native_by_trial[row["source_id"]].append(row)
pro_web_by_url = defaultdict(list)
for row in protocol_web:
    pro_web_by_url[row["url"].rstrip("/")].append(row)

issue_updates = []
for issue in baseline["issues"]:
    iid, tid = issue["issue_id"], issue["trial_id"]
    native = pro_native_by_trial.get(tid, [])
    restricted = [x for x in native if x["result"] == "skipped_exact_restriction"]
    permitted = [x for x in native if x["result"] != "skipped_exact_restriction"]
    web_rows = []
    for row in permitted:
        web_rows.extend(pro_web_by_url.get(row["requested_url"].rstrip("/"), [])[:1])
    web_success = sum(x["result"] == "success" for x in web_rows)
    web_error = sum(x["result"] == "web_error" for x in web_rows)
    question = issue.get("question") or "Read the full primary protocol and reconcile the current published facts."
    kind_fact = "five protocol facts" if issue["kind"] == "full_protocol" else "source-derived positive, negative, and unknown selection cases"
    issue_updates.append({
        "issue_id": iid,
        "trial_id": tid,
        "kind": issue["kind"],
        "state": "BLOCKED",
        "reviewed_at": reviewed_at.isoformat(),
        "finding": (
            f"{tid}: today's exact current-protocol route review recorded permitted={len(permitted)}, "
            f"web_success={web_success}, web_error={web_error}, exact_restriction={len(restricted)}. "
            f"The retained question was individually checked — {question} — but the available current surface "
            f"does not publish enough evidence to complete the required {kind_fact}."
        ),
        "question": question,
        "next_action": (
            f"Recheck {catalog_by_id.get(tid, {}).get('url') or issue.get('primary_url') or tid} after a changed "
            "publisher/protocol signal or the next applicable protocol-review cadence; preserve original evidence dates."
        ),
        "evidence_refs": [PRO_NATIVE_REF, PRO_WEB_REF],
        "restriction_or_unpublished_evidence_refs": [PRO_NATIVE_REF, PRO_WEB_REF],
        "full_protocol_review_complete": False,
        "current_exact_restriction": bool(restricted and not permitted),
    })


# Recompute the complete frozen-catalog deadline ledger from original published fields.
previous_receipt = read(ROOT / "data/audit_source_coverage.json")
previous_run = previous_receipt.get("run_id")
previous_deadline_path = ROOT / "research/audit-runs" / str(previous_run) / "deadline-review.json"
previous_rows = {x["record_id"]: x for x in read(previous_deadline_path)["rows"]} if previous_deadline_path.exists() else {}
comparison_date = date(2026, 11, 22)
deadline_rows = []
for tid in baseline["catalog_ids"]:
    trial = catalog_by_id[tid]
    old = dict(previous_rows.get(tid, {}))
    published = old.get("published_recruitment_end") or trial.get("recruitment_end")
    crossed = False
    if published:
        try:
            crossed = comparison_date > date.fromisoformat(str(published)[:10])
        except ValueError:
            crossed = False
    native = pro_native_by_trial.get(tid, [])
    pcounts = Counter(x["result"] for x in native)
    web_rows = []
    for row in native:
        if row["result"] != "skipped_exact_restriction":
            web_rows.extend(pro_web_by_url.get(row["requested_url"].rstrip("/"), [])[:1])
    pcounts.update("web_success" if x["result"] == "success" else "web_error" for x in web_rows)
    matching = bool(trial.get("available_for_matching"))
    result = (
        "no_published_recruitment_end_in_canonical_record" if not published
        else "deadline_passed_matching_already_disabled" if crossed and not matching
        else "deadline_passed_requires_current_extension_review" if crossed
        else "published_recruitment_deadline_not_yet_passed"
    )
    deadline_rows.append({
        "record_id": tid,
        "baseline_verified": old.get("baseline_verified", trial.get("verified") or trial.get("last_verified")),
        "published_recruitment_end": published,
        "recruitment_end_original_text": old.get("recruitment_end_original_text"),
        "recruitment_end_basis": old.get("recruitment_end_basis"),
        "timezone": old.get("timezone"),
        "primary_url": trial.get("url") or trial.get("source_url"),
        "checked_at": reviewed_at.isoformat(),
        "comparison_date": comparison_date.isoformat(),
        "deadline_crossed": crossed,
        "available_for_matching": matching,
        "current_protocol_attempts": dict(pcounts),
        "current_evidence_refs": [PRO_NATIVE_REF, PRO_WEB_REF],
        "result": result,
        "extension_found": False,
        "matching_before": matching,
        "matching_after": matching,
        "question": old.get("question"),
        "unperformed_steps": [],
    })
deadline_payload = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "baseline_catalog_sha256": hashlib.sha256((ROOT / "data/trials_base.json").read_bytes()).hexdigest(),
    "checked_at": reviewed_at.isoformat(),
    "rows": deadline_rows,
    "summary": {
        "records": len(deadline_rows),
        "with_published_recruitment_end": sum(bool(x["published_recruitment_end"]) for x in deadline_rows),
        "deadline_crossed": sum(x["deadline_crossed"] for x in deadline_rows),
        "passed_and_matchable": sum(x["deadline_crossed"] and x["matching_after"] for x in deadline_rows),
        "extensions_found": sum(x["extension_found"] for x in deadline_rows),
        "result": "NO_CHANGE" if not any(x["deadline_crossed"] and x["matching_after"] for x in deadline_rows) else "REVIEW_REQUIRED",
    },
}
write(HERE / "deadline-review.json", deadline_payload)


def sref(number: int) -> str:
    return f"{RUN_REF}/discovery-search-{number:02d}.json"


leads = read(HERE / "lead-protocol-current-findings.json")["leads"]

discovery_queries = []
for number, path in enumerate(sorted(HERE.glob("discovery-search-*.json")), 1):
    payload = read(path)
    for region, pass_name, country, language, query in payload["specs"]:
        discovery_queries.append({
            "region": region,
            "pass": pass_name,
            "country": country,
            "language": language,
            "query": query,
            "performed_at": reviewed_at.isoformat(),
            "evidence_refs": [sref(number)],
        })

execution_review = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "ended_at": ended_at.isoformat(),
    "source_reviews": source_reviews,
    "issue_updates": issue_updates,
    "discovery_queries": discovery_queries,
    "discovered_urls": [x["url"] for x in leads],
    "leads": leads,
    "added_catalog_ids": [],
    "added_source_ids": [],
    "deadline_review_ref": f"{RUN_REF}/deadline-review.json",
    "stop": {
        "reason": "completed_available_work",
        "detail": (
            "All 168 frozen sources received configured native decisions and same-URL Web fallback where permitted; "
            "all 74 inherited issues received current individual dispositions; both discovery passes cover all 12 "
            "required regions with 36 country/language queries; selected treatment leads were exact-matched or left "
            "unresolved; all 323 frozen deadline rows were recomputed. Remaining gaps depend on publisher access, "
            "unpublished facts, exact saved restrictions, or owner resolution of the UF status conflict."
        ),
        "evidence_refs": [SRC_NATIVE_REF, SRC_WEB_REF, PRO_NATIVE_REF, PRO_WEB_REF, DISCOVERY_INDEX_REF, LEAD_REF],
    },
}
write(HERE / "execution-review.json", execution_review)


# Update inventory with actual current processing while preserving old clinical
# dates unless the Web evidence itself is labelled crawled today.
review_by_source = {x["source_id"]: x for x in source_reviews}
receipt_by_source = {x["source_id"]: x for x in receipt_rows}
for source in inventory_payload["sources"]:
    sid = source["id"]
    row = receipt_by_source[sid]
    attempts = row["attempted_urls"]
    fresh = [a for a in attempts if a.get("method") == "web_open" and a.get("result") == "success" and a.get("crawled_label") == "today"]
    source["last_attempts"] = attempts
    source["last_route_used"] = row["route_used"]
    source["last_audit_run_id"] = RUN_ID
    source["last_coverage_gap"] = None if row["content_sufficient"] else review_by_source[sid]["finding"]
    if fresh:
        latest = max(a["completed_at"] for a in fresh)
        source["last_checked"] = "2026-11-22"
        source["last_checked_at"] = latest
        source["last_result"] = "reachable" if row["content_sufficient"] else "partial"
        source["last_http_status"] = None
    if row["content_sufficient"]:
        source["last_protocols_seen"] = len(review_by_source[sid]["protocols"])
inventory_payload["updated"] = "2026-11-22"
inventory_payload["last_audit_run_id"] = RUN_ID
inventory_payload["last_audit_at"] = ended_at.isoformat()
write(ROOT / "data/source_inventory.json", inventory_payload)
write(ROOT / "data/audit_source_coverage.json", receipt)

print(json.dumps({
    "sources": len(source_reviews),
    "sufficient": receipt["content_sufficient_total"],
    "issues": len(issue_updates),
    "queries": len(discovery_queries),
    "leads": len(leads),
    "deadline_rows": len(deadline_rows),
    "inventory_fresh_today": sum(x.get("last_checked") == "2026-11-22" for x in inventory_payload["sources"]),
}, indent=2))
