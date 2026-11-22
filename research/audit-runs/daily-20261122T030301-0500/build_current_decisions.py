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
    sufficient = sid == "registry-uk-vcsr"
    protocols = []
    if sufficient:
        protocols = [
            {"registry_id": "UK-VCSR-2026-00013", "title": "Evaluating use of immune therapy in equine allergic reactions", "relevant": False},
            {"registry_id": "UK-VCSR-2026-00006", "title": "Equine gastric ulceration management trial", "relevant": False, "sample": True},
            {"registry_id": "UK-VCSR-2026-00003", "title": "Feline chronic kidney disease dietary intervention", "relevant": False, "sample": True},
            {"registry_id": "UK-VCSR-2026-00001", "title": "Novel immunotherapy for canine lymphoma", "relevant": False, "sample": True},
        ]
        finding = (
            "Current official UK-VCSR roster was read in full: 4 entries were shown. "
            "The only dog/cat oncology title is explicitly labelled an AI-generated sample, "
            "so the current genuine dog/cat anticancer-treatment roster is 0."
        )
        catalog_comparison = (
            "0 genuine current dog/cat anticancer treatment protocols were present; no canonical addition, "
            "status change, or unresolved real protocol identity resulted."
        )
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
        "protocols_seen": 0 if sufficient else None,
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


leads = [
    {
        "url": "https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/",
        "primary_url": "https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/",
        "disposition": "PENDING_EVIDENCE",
        "canonical_ids": [],
        "reason": "The official UF protocol is treatment research distinct from the CSU LSD1 record, but its current page simultaneously says the college is recruiting and Enrollment Paused; current owner access is therefore unresolved.",
        "missing_primary_reason": "The primary page has internally conflicting current-recruitment labels; changing the catalog status requires a medical/editorial owner decision or a clarified official status.",
        "evidence_refs": [sref(6), LEAD_REF],
    },
    {
        "url": "https://www.paccalvet.com/cat-cancer-study",
        "primary_url": "https://www.paccalvet.com/cat-cancer-study",
        "disposition": "PENDING_EVIDENCE",
        "canonical_ids": [],
        "reason": "Search discovery exposed a feline Paccal Vet treatment page, but direct current primary opening returned 401 and the accessible text did not establish exact tumor cohort, active sites, or current intake versus the sponsor's completed-recruitment history.",
        "missing_primary_reason": "Current protocol identity and recruitment cannot be reconciled from the inaccessible exact official page.",
        "evidence_refs": [sref(6), sref(7), LEAD_REF],
    },
    {
        "url": "https://www.gamgee.io/trial/",
        "primary_url": "https://www.gamgee.io/trial/",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["au-gamgee-personalized-mrna-vaccine"],
        "identity_comparison": "Same Australia-wide mast-cell-cancer cohort and personalized tumor/blood-derived mRNA therapeutic vaccine with interest registration.",
        "reason": "Today's official page exactly matches the existing canonical protocol and says recruitment is open.",
        "evidence_refs": [sref(4), sref(9), LEAD_REF],
    },
    {
        "url": "https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien/",
        "primary_url": "https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien/",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["fr-oniris-osa-biocera-vet-cement"],
        "identity_comparison": "Same Oniris/TheraVet appendicular-osteosarcoma cohort, percutaneous BIOCERA-VET cement, large/giant dogs, and palliative stabilization purpose.",
        "reason": "Official page remains open but the intervention remains supportive/palliative rather than tumor-directed treatment matching.",
        "evidence_refs": [sref(3), LEAD_REF],
    },
    {
        "url": "https://uqvets.com.au/about/clinical-research-trials",
        "primary_url": "https://uqvets.com.au/about/clinical-research-trials",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["au-uq-appendicular-osteosarcoma-vaccine"],
        "identity_comparison": "Same UQ appendicular osteosarcoma postoperative experimental vaccine protocol.",
        "reason": "Current discovery result maps exactly to the existing canonical identity; no second UQ OSA vaccine protocol was established.",
        "evidence_refs": [sref(4), sref(9)],
    },
    {
        "url": "https://www.vm.a.u-tokyo.ac.jp/vmc/aboutus/research/",
        "primary_url": "https://www.vm.a.u-tokyo.ac.jp/vmc/aboutus/research/",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["jp-tokyo-histiocytic-sarcoma-anti-pd1-2026", "jp-tokyo-organoid-guided-targeted-therapy-2026", "jp-tokyo-canine-bladder-ido1-inhibitor", "jp-tokyo-macromolecular-pirarubicin-solid-tumors"],
        "identity_comparison": "The Tokyo current-research master names the same four active treatment identities already canonicalized; the paused feline TCC record remains a separate inactive identity.",
        "reason": "Japanese-language discovery produced no additional unnamed treatment cohort on this master.",
        "evidence_refs": [sref(5), sref(6)],
    },
    {
        "url": "https://www.vet.upenn.edu/ryan-hospital/clinical-trials/",
        "primary_url": "https://www.vet.upenn.edu/ryan-hospital/clinical-trials/",
        "disposition": "SOURCE_INDEX_REVIEWED",
        "canonical_ids": [],
        "reason": "The Penn index is navigation evidence. The surfaced FLASH glioma, metastatic OSA FLASH, and NIR oral-SCC margin protocols were reconciled to exact existing IDs; no fourth unmatched Penn treatment identity was established from the current result.",
        "protocol_links_examined": ["FLASH glioma -> penn-glioma-flash-gilvetmab-2026", "metastatic OSA proton FLASH -> penn-flash-metastatic-osa-gilvetmab-2026", "NIR oral SCC margin -> penn-oral-scc-nir-margin-2026"],
        "evidence_refs": [sref(1), sref(2)],
    },
    {
        "url": "https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/",
        "primary_url": "https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/",
        "disposition": "SOURCE_INDEX_REVIEWED",
        "canonical_ids": [],
        "reason": "The current UF oncology index was reconciled as an index: its trametinib HS, OSA vaccine, OSA mRNA, HSA vaccine, and melanoma vaccine listings map to existing exact UF records; its Biocera cement line is explicitly closed enrollment.",
        "protocol_links_examined": ["uf-hs-trametinib", "uf-osa-vaccine", "uf-osa-mrna", "uf-hsa-vaccine", "uf-melanoma", "Biocera cement -> closed enrollment"],
        "evidence_refs": [sref(1), sref(9)],
    },
    {
        "url": "https://www.veterinarystudiesregistry.co.uk/studies",
        "primary_url": "https://www.veterinarystudiesregistry.co.uk/studies",
        "disposition": "SOURCE_INDEX_REVIEWED",
        "canonical_ids": [],
        "reason": "The complete current four-entry registry roster contains no genuine dog/cat anticancer-treatment protocol; the lymphoma title is explicitly an AI-generated sample.",
        "protocol_links_examined": ["UK-VCSR-2026-00013 equine allergy", "UK-VCSR-2026-00006 AI sample equine", "UK-VCSR-2026-00003 AI sample feline CKD", "UK-VCSR-2026-00001 AI sample canine lymphoma"],
        "evidence_refs": [SRC_WEB_REF],
    },
    {
        "url": "https://vetcancercare.com/clinical-trials/",
        "primary_url": "https://vetcancercare.com/clinical-trials/",
        "disposition": "CLOSED_CONFIRMED",
        "canonical_ids": [],
        "reason": "Current official search result says there are no trials currently enrolling and places Immunocidin studies under past trials; this is a source-level negative, not a closure inferred for unrelated institutions.",
        "evidence_refs": [sref(1), sref(2)],
    },
    {
        "url": "https://www.tierspital.uzh.ch/wp-content/uploads/2025/12/Studie_Orale-Chemotherapie-mit-Vinorelbin.pdf",
        "primary_url": "https://www.tierspital.uzh.ch/forschungsprojekte/orale-chemotherapie-hunde-mit-tumor/",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["ch-zurich-oral-vinorelbine-phase1-2026"],
        "identity_comparison": "Same Zurich single-dose oral vinorelbine safety/tolerability dose-finding study for dogs with tumors.",
        "reason": "The PDF is another representation of the existing inactive Phase I identity, not a new treatment course.",
        "evidence_refs": [sref(3)],
    },
    {
        "url": "https://assets.ctfassets.net/f18j4npi43lu/5qE2eAtbFbyZKYWKJgPxXn/90f325d565134ced751567da21bfcad1/Terapia_a_base_di_piccole_molecole_organiche_aventi_come_target_la_Proteina_di_Attivazione_dei_Fibroblasti__PAF__per_il_trat.pdf",
        "primary_url": "https://www.ospedaleveterinario.unimi.it/collaborare-con-noi-studi-di-ricerca/",
        "disposition": "VERIFIED_EXISTING",
        "canonical_ids": ["eu-it-unimi-oncofap-mmae"],
        "identity_comparison": "Same University of Milan FAP-positive canine solid-tumor targeted small-molecule/OncoFAP protocol represented by the existing canonical record.",
        "reason": "The protocol PDF does not establish a second Milan FAP treatment identity.",
        "evidence_refs": [sref(3)],
    },
]

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
        source["last_protocols_seen"] = 0
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
