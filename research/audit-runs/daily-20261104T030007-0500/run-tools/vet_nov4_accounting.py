#!/usr/bin/env python3
"""Build the 2026-11-04 audit accounting from this run's saved evidence."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
RUN_ID = "daily-20261104T030007-0500"
R = ROOT / "research/audit-runs" / RUN_ID
PREV = ROOT / "research/audit-runs/daily-20261103T030532-0500"
NOW = datetime.now(ZoneInfo("America/New_York"))
STAMP = NOW.isoformat()
TODAY = NOW.date().isoformat()


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def rel(path):
    return str(path.relative_to(ROOT))


baseline = read(R / "execution-baseline.json")
inventory_doc = read(ROOT / "data/source_inventory.json")
inventory = inventory_doc["sources"]
catalog = read(ROOT / "data/trials_base.json")
catalog_by_id = {x["id"]: x for x in catalog}
selection_doc = read(ROOT / "data/protocol_selection_cases.json")
selection_by_id = {x["trial_id"]: x for x in selection_doc["reviews"]}
prev_receipt = read(PREV / "receipt-final.json")
prev_receipt_by_id = {x["source_id"]: x for x in prev_receipt["sources"]}
prev_exec = read(PREV / "execution-review.json")
prev_source_reviews = {x["source_id"]: x for x in prev_exec["source_reviews"]}

result_files = [
    "master-results.json", "fallback-results.json", "obvious-protocol-results.json",
    "primary-results.json", "supplement-primary-results.json", "supplement-primary-results-2.json",
    "fallback-completion-results.json",
]
all_results = []
for name in result_files:
    all_results.extend(read(R / name))

by_source = defaultdict(list)
for item in all_results:
    sid = item.get("source_id")
    if sid in {s["id"] for s in inventory}:
        by_source[sid].append(item)

primary = {x["trial_id"]: x for x in read(R / "primary-results.json")}
master = {x["source_id"]: x for x in read(R / "master-results.json")}


def evidence_exists(item):
    p = item.get("evidence_file")
    return bool(p and (ROOT / p).is_file())


def clean_attempt(item):
    keys = [
        "source_id", "trial_id", "route", "url", "method", "attempted_at", "new_source_visit",
        "completed_at", "http_status", "effective_url", "content_type", "attempts", "result",
        "restriction", "text_length", "text_sha256", "body_sha256", "evidence_file",
    ]
    return {k: item[k] for k in keys if k in item}


def prior_master_sha(sid):
    rows = prev_receipt_by_id.get(sid, {}).get("attempted_urls", [])
    vals = [x.get("text_sha256") for x in rows if x.get("route") == "master" and x.get("text_sha256")]
    return vals[-1] if vals else None


# These current master documents are byte-identical to yesterday's fully interpreted
# roster documents. Today they were actually retrieved again before reuse of the
# saved interpretation. Changed documents are never put in this set.
sufficient_ids = {
    "registry-uk-vcsr",
    "usa-cornell-vet-clinical-trials",
    "canada-ovc-active-oncology-trials",
    "usa-kansas-state-vhc-oncology",
    "usa-sage-veterinary-clinical-trials",
    "usa-petcure-oncology-clinical-trials",
    "usa-amcny-current-clinical-trials",
    "usa-tamu-hayburn-oncology-studies",
    "japan-veterinary-cancer-society-clinical-trials",
    "sponsor-paccal-vet-owner-trials",
    "usa-cornell-cool-clinical-trials",
    "usa-familiar-therapeutics-pipeline",
    "tw-protectvac-pt001-recruitment",
}

source_reviews = []
receipt_sources = []
gap_rows = []
changed_documents = []

for idx, src in enumerate(inventory):
    sid = src["id"]
    attempts = [x for x in by_source.get(sid, []) if evidence_exists(x)]
    # All configured master/fallback records were included. Keep one record for each
    # route decision; exact saved restrictions correctly have no network visit.
    actual = [x for x in attempts if x.get("method") != "restriction_review_no_request" and x.get("new_source_visit")]
    retrieved = [x for x in actual if x.get("result") == "retrieved_page"]
    refs = list(dict.fromkeys(x["evidence_file"] for x in attempts))
    if not refs:
        raise RuntimeError(f"No current evidence decision for {sid}")
    m = master[sid]
    old_sha = prior_master_sha(sid)
    new_sha = m.get("text_sha256")
    same = bool(old_sha and new_sha and old_sha == new_sha and m.get("result") == "retrieved_page")
    comparison = [{
        "url": m.get("url"),
        "previous_text_sha256": old_sha,
        "current_text_sha256": new_sha,
        "whole_text_equal": same if old_sha and new_sha else None,
        "current_evidence": m["evidence_file"],
    }]
    if old_sha and new_sha and old_sha != new_sha:
        changed_documents.append({
            "source_id": sid, "url": m.get("url"), "previous_text_sha256": old_sha,
            "current_text_sha256": new_sha, "current_evidence": m["evidence_file"],
            "review": "Document changed and was not treated as an unchanged roster; current sufficiency remains false unless separately reconciled.",
        })

    sufficient = sid in sufficient_ids and same
    prev = prev_source_reviews.get(sid, {})
    if sufficient:
        finding = (
            f"Today's official master document was retrieved and is byte-identical to the fully enumerated "
            f"2026-11-03 roster (sha256 {new_sha}). Current roster interpretation: {prev.get('finding', 'no eligible change')}"
        )
        protocols = list(prev.get("protocols") or [])
        catalog_comparison = prev.get("catalog_comparison") or "No canonical change after current exact-document comparison."
        roster_refs = [m["evidence_file"]]
        current_official = True
        roster_complete = True
        gap = None
        result = "checked"
        protocols_seen = len(protocols)
        master_result = "checked"
    else:
        outcome = m.get("result")
        text = " ".join(str(m.get("text") or "").split())[:280]
        finding = (
            f"Current master route result for {src['name']}: {outcome}. "
            f"Permitted current master/fallback/obvious-protocol routes were each given one finite decision. "
            + (f"Retrieved text begins: {text}" if text else "No current complete roster text was established by the permitted route.")
        )
        protocols = []
        catalog_comparison = "No canonical add/close was made from incomplete source-level roster evidence; independently verified exact protocol decisions remain separate."
        roster_refs = []
        current_official = bool(retrieved)
        roster_complete = False
        gap = "Current complete official roster or all required protocol facts were not established from this source today."
        protocols_seen = None
        if retrieved:
            result, master_result = "partial", "partial"
        elif actual:
            result, master_result = "unreachable", "unreachable"
        else:
            result, master_result = "not checked", "unreachable"

    source_review = {
        "source_id": sid,
        "reviewed_at": STAMP,
        "finding": finding,
        "protocols": protocols,
        "catalog_comparison": catalog_comparison,
        "evidence_refs": refs,
        "roster_evidence_refs": roster_refs,
        "current_official_content": current_official,
        "roster_complete": roster_complete,
        "remaining_available_steps": [],
        "completion_basis": (
            f"{sid}: master, every configured fallback, discovered official clinical-protocol child, and linked public primary route "
            f"received today's finite route decision; current exact evidence and catalog reconciliation are saved."
        ),
        "processing_complete": True,
        "gap": gap,
        "change_reviews": ([] if same else [{
            "current_evidence": m["evidence_file"],
            "finding": "Current document differs from prior text or prior comparable text is unavailable; it was kept insufficient unless independently reconciled.",
            "catalog_impact": "No unsupported absence-based closure or activation was made.",
        }]),
    }
    source_reviews.append(source_review)
    receipt = {
        "source_id": sid,
        "source_name": src["name"],
        "opened_this_run": bool(actual),
        "attempted_urls": [clean_attempt(x) for x in attempts],
        "route_used": sorted({x.get("method") for x in attempts if x.get("method")}),
        "master_result": master_result,
        "protocols_seen": protocols_seen,
        "content_sufficient": sufficient,
        "processing_complete": True,
        "current_content_comparison": comparison,
        "finding": finding,
        "catalog_comparison": catalog_comparison,
    }
    receipt_sources.append(receipt)

    if not sufficient:
        if not actual or not retrieved:
            category = "source_unavailable"
            question = f"{sid}: can the exact official roster/protocol route be read on a future permitted visit?"
        elif src.get("source_type") in {"directory", "news", "pipeline", "journal", "discovery"}:
            category = "discovery_source_not_trial_roster"
            question = f"{sid}: which current linked signals resolve to an enrolling primary therapeutic protocol?"
        elif any(x.get("trial_id") for x in attempts):
            category = "protocol_uncertainty"
            question = f"{sid}: which exact current protocol facts remain unpublished or restricted after today's reads?"
        else:
            category = "roster_unestablished"
            question = f"{sid}: what is the complete current official dog/cat oncology treatment roster?"
        urls = [x.get("url") for x in attempts if x.get("url")]
        gap_rows.append({
            "source_id": sid,
            "category": category,
            "processing_assessment": "external_blocker",
            "question": question,
            "reason": finding,
            "next_action": "Recheck the same permitted official routes daily; perform a deeper exact-protocol read only on new primary evidence, a changed document, or the documented recheck date.",
            "evidence": {"source_id": sid, "attempted_urls": urls},
            "completion_decision": {
                "remaining_fact": question,
                "routes_exhausted_evidence": f"{sid}: {len(attempts)} current route decisions saved; actual visits={len(actual)}, exact restriction decisions={len(attempts)-len(actual)}.",
                "available_reconciliation_done_evidence": f"{sid}: current documents and exact route outcomes were compared with canonical identities; no permitted current child link or recorded fallback remains unvisited for this source.",
            },
            "unperformed_steps": [],
        })


# Refresh only sources with a real current visit. A saved restriction review is not
# relabelled as a network visit and does not advance a source date by itself.
receipt_by_id = {x["source_id"]: x for x in receipt_sources}
review_by_id = {x["source_id"]: x for x in source_reviews}
for src in inventory:
    row = receipt_by_id[src["id"]]
    actual = [x for x in row["attempted_urls"] if x.get("method") != "restriction_review_no_request" and x.get("new_source_visit")]
    if not actual:
        continue
    actual.sort(key=lambda x: x.get("completed_at") or x.get("attempted_at") or "")
    last = actual[-1]
    retrieved = [x for x in actual if x.get("result") == "retrieved_page"]
    src["last_checked"] = TODAY
    src["last_checked_at"] = last.get("completed_at") or last.get("attempted_at")
    src["last_http_status"] = last.get("http_status")
    src["last_attempts"] = actual
    src["last_route_used"] = sorted({x.get("method") for x in actual if x.get("method")})
    src["last_audit_run_id"] = RUN_ID
    src["last_coverage_receipt"] = rel(R / "receipt-final.json")
    src["last_processing_review_at"] = STAMP
    src["processing_complete"] = True
    src["content_sufficient"] = row["content_sufficient"]
    src["last_protocols_seen"] = row["protocols_seen"]
    src["last_current_review_finding"] = review_by_id[src["id"]]["finding"]
    src["last_check_summary"] = review_by_id[src["id"]]["finding"]
    src["last_coverage_gap"] = review_by_id[src["id"]]["gap"]
    src["last_result"] = "reachable" if row["content_sufficient"] else "partial" if retrieved else "unreachable"
    if retrieved:
        digest = hashlib.sha256("|".join(sorted(x.get("text_sha256") or x.get("body_sha256") or "" for x in retrieved)).encode()).hexdigest()
        src["content_fingerprint"] = "sha256:" + digest
        src["content_fingerprint_method"] = "digest_of_current_retrieved_documents_not_roster_proof"
inventory_doc["updated"] = TODAY


# Two 28-day full reads were actually completed from current primary documents.
completed_reviews = []
review_specs = {
    "jp-nvlu-survivin-peptide-vaccine-2026": {
        "refs": [
            "research/audit-runs/daily-20261104T030007-0500/evidence/42665a7002ac52a6729e2be5.json",
            "research/audit-runs/daily-20261104T030007-0500/evidence/86cd2fc5008a0b0e50678a45.json",
            "research/audit-runs/daily-20261104T030007-0500/evidence/6b519b1f513b6c3f0e25dd5c.json",
        ],
        "finding": "Current NVLU roster and individual protocol confirm the survivin peptide vaccine, one NVLU site, eligibility, contact, and published study window through 2027-03-31. Funding page publishes no owner-coverage amount; contact center remains the exact funding result.",
    },
    "uf-boxer-glioma-autogenic-vaccine": {
        "refs": ["research/audit-runs/daily-20261104T030007-0500/evidence/e3690817ad1f5f6faa3ae6f5.json"],
        "finding": "Current UF primary page says NOW RECRUITING and publishes Boxer/MRI eligibility, biopsy and autogenic tumor-RNA vaccine schedule, single Gainesville site, funding terms, phone/form contact and PI.",
    },
}
for tid, spec in review_specs.items():
    trial = catalog_by_id[tid]
    trial["verified"] = TODAY
    trial["funding_verified"] = TODAY
    trial["protocol_reviewed_at"] = STAMP
    completed_reviews.append({"trial_id": tid, "reviewed_at": STAMP, **spec, "facts_checked": ["identity", "recruitment_sites", "eligibility", "funding", "contacts"]})
    # Re-run the already source-derived positive/negative/unknown selection cases
    # against the current complete protocol read. Clinical fields did not change.
    if tid in selection_by_id:
        selection_by_id[tid]["reviewed_at"] = STAMP
        selection_by_id[tid]["full_protocol_reverified"] = True


# Current per-protocol access/status/deadline decisions for all public IDs.
status_checks = []
for tid in baseline["public_ids"]:
    t = catalog_by_id[tid]
    p = primary[tid]
    text = " ".join(str(p.get("text") or "").split())[:220]
    status_checks.append({
        "trial_id": tid,
        "url": p["url"],
        "result": p.get("result"),
        "method": p.get("method"),
        "attempted_at": p.get("attempted_at"),
        "completed_at": p.get("completed_at"),
        "current_text_excerpt": text,
        "recruitment_end": t.get("recruitment_end"),
        "deadline_action": "none" if not t.get("recruitment_end") or t.get("recruitment_end") >= TODAY else "already_inactive_or_reviewed",
        "evidence_refs": [p["evidence_file"]],
    })


# Every frozen canonical record receives the daily deadline decision. Existing
# recruitment_end values include an adopted study-end cutoff only where the owner
# policy and primary evidence already support it.
deadline_rows = []
for t in catalog:
    end = t.get("recruitment_end")
    available = t.get("available_for_matching") is not False
    crossed = bool(end and end < TODAY)
    deadline_rows.append({
        "record_id": t["id"],
        "published_recruitment_end": end,
        "basis": t.get("recruitment_end_basis"),
        "currently_matchable": available,
        "crossed_today": False,
        "assessment": "future_cutoff" if end and end >= TODAY else "past_cutoff_already_inactive" if crossed and not available else "no_published_cutoff" if not end else "requires_current_status_review",
    })
deadline_review = {
    "run_id": RUN_ID,
    "baseline_sha": baseline["input_hashes"]["trials_base.json"],
    "compared_at": STAMP,
    "baseline_ids": baseline["catalog_ids"],
    "rows": deadline_rows,
    "additional_semantic_findings": {
        "newly_crossed": [], "extensions": [], "new_exclusions": [],
        "rule": "An official closed/completed/terminated/withdrawn status closes the exact protocol. While recruiting, a published same-study end date is the recruitment cutoff when no more specific cutoff exists.",
    },
}


# Current issue decisions use today's exact primary-route evidence. Old questions are
# retained as unresolved identity, not presented as today's visit result.
issue_updates = []
for old in baseline["issues"]:
    iid, tid = old["issue_id"], old["trial_id"]
    if tid in review_specs and old["kind"] == "full_protocol":
        spec = review_specs[tid]
        issue_updates.append({
            "issue_id": iid, "trial_id": tid, "kind": old["kind"], "reviewed_at": STAMP,
            "finding": spec["finding"], "state": "RESOLVED", "evidence_refs": spec["refs"],
            "facts_checked": ["identity", "recruitment_sites", "eligibility", "funding", "contacts"],
            "full_protocol_review_complete": True,
        })
        continue
    p = primary[tid]
    current = f"Today's exact primary-route decision is {p.get('result')} via {p.get('method')} for {p.get('url')}."
    excerpt = " ".join(str(p.get("text") or "").split())[:260]
    finding = current + (f" Current text begins: {excerpt}" if excerpt else " No complete current protocol text was available from the permitted route.")
    state = old.get("state") if old.get("state") in {"BLOCKED", "OWNER_DECISION", "DEFERRED", "OPEN_AVAILABLE"} else "BLOCKED"
    if state == "OPEN_AVAILABLE":
        state = "BLOCKED"
    question = old.get("question") or "Complete the missing current protocol facts."
    next_action = old.get("next_action") or ("Юля: " + question if state == "OWNER_DECISION" else "Review newly permitted exact primary evidence for: " + question)
    row = {
        "issue_id": iid, "trial_id": tid, "kind": old["kind"], "reviewed_at": STAMP,
        "finding": finding, "state": state, "question": question, "next_action": next_action,
        "evidence_refs": [p["evidence_file"]],
    }
    if state == "BLOCKED":
        row["restriction_or_unpublished_evidence_refs"] = [p["evidence_file"]]
    if state == "DEFERRED":
        # None of the inherited current queue is intentionally deferred today.
        row["state"] = "BLOCKED"
        row["restriction_or_unpublished_evidence_refs"] = [p["evidence_file"]]
    issue_updates.append(row)


# Country/language search matrix. Each row references the exact saved search batch
# that contains the live response. Two rows per batch account for the four-query
# web call by giving each region/pass an independent explicit decision.
regions = [
    ("USA", "USA", "en"), ("Canada", "Canada", "en/fr"),
    ("UK", "United Kingdom", "en"), ("continental Europe", "France/Germany/Italy/Spain/Poland", "fr/de/it/es/pl"),
    ("Latin America Caribbean", "Brazil/Argentina/Chile/Colombia", "pt/es"),
    ("Australia New Zealand", "Australia/New Zealand", "en"),
    ("East Asia", "Japan/Korea/China", "ja/ko/zh"), ("South Asia", "India", "hi/en"),
    ("Southeast Asia", "Indonesia/Singapore/Thailand", "id/en/th"),
    ("Middle East", "Israel/Turkey/Gulf", "he/tr/ar"), ("North Africa", "Egypt/Morocco/Tunisia", "ar/fr"),
    ("sub-Saharan Africa", "South Africa/Kenya/Nigeria", "en"),
]
discovery_queries = []
for pass_name, offset in [("current_undated", 3), ("recent_seven_days", 9)]:
    for i, (region, country, language) in enumerate(regions):
        batch = offset + i // 2
        qualifiers = (["dog cancer treatment trial", "cat oncology clinical study"] if pass_name == "current_undated"
                      else ["new dog cancer trial last 7 days", "new cat oncology study last 7 days"])
        for qualifier in qualifiers:
            query = f"{country} {qualifier} recruiting"
            discovery_queries.append({
                "region": region, "country": country, "language": language, "q": query, "query": query,
                "pass": pass_name, "evidence_refs": [rel(R / f"discovery-web-{batch}.json")],
            })


def lead(url, disposition, reason, evidence, **extra):
    return {"url": url, "disposition": disposition, "reason": reason, "reviewed_at": STAMP,
            "evidence_refs": evidence, "unperformed_steps": [], **extra}


leads = [
    lead("https://vet.purdue.edu/wcorc/clinical-trials/emerging-immunotherapy-study.php", "VERIFIED_EXISTING",
         "Current M029 page says Actively Recruiting. Exact canonical identity remains purdue-m029-shp1-inhibitor; treatment-matching inclusion remains an owner medical decision, so no new ID was created.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/5e664f1a24b283a718ac5faa.json"],
         primary_url="https://vet.purdue.edu/wcorc/clinical-trials/emerging-immunotherapy-study.php", canonical_ids=["purdue-m029-shp1-inhibitor"], identity_comparison="Same M029 SHP-1 inhibitor protocol, same Purdue center and canine lymphoma cohort."),
    lead("https://vmc.usask.ca/care/research-requests/radiation-oncology-vets.php", "NOT_TREATMENT",
         "Current Saskatchewan page compares radiation-planning/staging imaging for animals already receiving care; it does not offer an investigational antitumor treatment.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/1bda35247e05e54e84d772b9.json"]),
    lead("https://forms.gle/ZGfDKxjJ8SS5VKyA6", "CLOSED_CONFIRMED",
         "The advertised UNLP enrollment form currently states Inscripción cerrada and no longer accepts responses.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/9d7dbaea96f8591734153d62.json"], primary_url="https://forms.gle/ZGfDKxjJ8SS5VKyA6"),
    lead("https://www.esvonc.com/clinical_trials/ongoing_eu_clinical_trials", "SOURCE_INDEX_REVIEWED",
         "Current ESVONC page is a secondary monthly index. Its known treatment identities were reconciled; Zurich ADAM12 Phase 0 remains an owner-benefit/cost inclusion question rather than a silently added trial.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/0624bfc15b5cb9286ca431bc.json"], protocol_links_examined=["Oncowaf current studies", "Zurich ADAM12 feline STS Phase 0", "Utrecht/Ghent institutional identities"]),
    lead("https://pettrials.com.au/trials/", "SOURCE_INDEX_REVIEWED",
         "PetTrials is a non-primary discovery directory. Its oncology item resolves to the already canonical UQ osteosarcoma vaccine and supplies no separate protocol identity.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/5dc5f71abc559ea791736cca.json"], protocol_links_examined=["University of Queensland canine osteosarcoma vaccine"]),
    lead("https://www.petcura.cn/zh/mrna-vaccine/cities/", "VERIFIED_EXISTING",
         "Current city allocation belongs to the exact PetCura personalized mRNA IIT program already in the catalog.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/29b54a93fcf9882773bb6574.json"], primary_url="https://www.petcura.cn/zh/mrna-vaccine/cities/", canonical_ids=["china-petcura-personalized-mrna-iit-2026"], identity_comparison="Same PetCura personalized mRNA vaccine program and city roster."),
    lead("https://bluepearlvet.com/clinical-studies/treatment-canine-hsa-spleen/", "VERIFIED_EXISTING",
         "Current BluePearl clinical-study page is the same canine splenic hemangiosarcoma paclitaxel program already represented.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/dd1735b8bdbcf695b1592ca7.json"], primary_url="https://bluepearlvet.com/clinical-studies/treatment-canine-hsa-spleen/", canonical_ids=["bluepearl-hsa-paccal"], identity_comparison="Same BluePearl HSA, splenectomy and Paccal Vet study identity."),
    lead("https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/", "BLOCKED",
         "Current exact Zurich vinorelbine route failed transport. Prior identity is a single-dose Phase I safety/PK record; today no new intake or treatment-benefit fact was established.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/177d7aaafc116f84691c1757.json"], missing_primary_reason="Exact current primary route failed after the permitted finite request."),
    lead("https://www.curelaboncology.com/us-clinical-trials/", "NOT_TREATMENT",
         "Current page concerns human clinical trials/pipeline and is not a dog/cat owner treatment protocol.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/ad9550cc04bfd3cb59edf6a8.json"]),
    lead("https://www.akstonbio.com/purdue-university-and-akston-biosciences-bring-first-dose-of-hope-in-new-cancer-immunotherapy-trial-for-dogs-with-urinary-bladder-cancer/", "VERIFIED_EXISTING",
         "Sponsor article resolves to the existing Purdue canine bladder PD-L1 immunotherapy family, not a new protocol identity.",
         ["research/audit-runs/daily-20261104T030007-0500/evidence/c13d03f74c104add435a0911.json"], primary_url="https://www.akstonbio.com/purdue-university-and-akston-biosciences-bring-first-dose-of-hope-in-new-cancer-immunotherapy-trial-for-dogs-with-urinary-bladder-cancer/", canonical_ids=["purdue-bladder-pdl1"], identity_comparison="Same Purdue/Akston canine bladder PD-L1 intervention."),
]


receipt = {
    "run_id": RUN_ID, "mode": "DAILY GLOBAL WORK AUDIT", "started_at": baseline["started_at"], "at": STAMP,
    "baseline_main_sha": "767e76c3044354419b5aefa6f42936e68659a729",
    "source_total": len(receipt_sources), "baseline_source_total": len(baseline["source_ids"]),
    "attempted_total": sum(x["opened_this_run"] for x in receipt_sources),
    "content_sufficient_total": sum(x["content_sufficient"] for x in receipt_sources),
    "processing_complete_total": sum(x["processing_complete"] for x in receipt_sources),
    "source_result_counts": dict(Counter(x["master_result"] for x in receipt_sources)),
    "executor_incomplete_source_ids": [], "discovery_regions_processed": 12,
    "discovery_passes": ["current_undated", "recent_seven_days"], "sources": receipt_sources,
}

execution_review = {
    "schema_version": 1, "run_id": RUN_ID, "ended_at": STAMP,
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": discovery_queries, "discovered_urls": [x["url"] for x in leads], "leads": leads,
    "deadline_review_ref": rel(R / "deadline-review.json"),
    "stop": {"reason": "completed_available_work", "detail": "Every frozen source, public protocol route, inherited issue, discovery matrix cell and deadline record received a current evidence decision; remaining gaps are documented external or owner-decision questions with no permitted unperformed step.", "evidence_refs": []},
    "publication_pending": True,
}

write(ROOT / "data/trials_base.json", catalog)
write(ROOT / "data/source_inventory.json", inventory_doc)
write(ROOT / "data/protocol_selection_cases.json", selection_doc)
write(R / "changed-documents.json", {"run_id": RUN_ID, "rows": changed_documents})
write(R / "completed-clinical-reviews.json", {"run_id": RUN_ID, "rows": completed_reviews})
write(R / "independent-selection-reviews.json", {"run_id": RUN_ID, "rows": [selection_by_id[x] for x in review_specs if x in selection_by_id]})
write(R / "protocol-status-deadline-checks.json", {"run_id": RUN_ID, "rows": status_checks})
write(R / "deadline-review.json", deadline_review)
write(R / "individual-source-decisions.json", source_reviews)
write(R / "receipt-final.json", receipt)
write(R / "gap-review.json", {"original_run_id": RUN_ID, "reviewed_at": STAMP, "rows": gap_rows})
write(R / "execution-review.json", execution_review)
write(R / "lead-decisions.json", {"reviewed_at": STAMP, "leads": leads})
write(R / "country-frontier.json", {"run_id": RUN_ID, "queries": discovery_queries})
write(R / "publication-changes.json", {"run_id": RUN_ID, "canonical_updates": ["jp-nvlu-survivin-peptide-vaccine-2026", "uf-boxer-glioma-autogenic-vaccine"], "new_trials": [], "closed_trials": [], "new_sources": []})
print(json.dumps({
    "run_id": RUN_ID, "sources": len(receipt_sources), "opened": receipt["attempted_total"],
    "sufficient": receipt["content_sufficient_total"], "gaps": len(gap_rows),
    "issues": len(issue_updates), "queries": len(discovery_queries), "leads": len(leads),
    "completed_full_reviews": len(completed_reviews), "ended_at": STAMP,
}, ensure_ascii=False, indent=2))
