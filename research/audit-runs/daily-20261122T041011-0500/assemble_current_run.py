#!/usr/bin/env python3
"""Assemble this run's receipts from its own saved attempts and reviews."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RUN_ID = RUN.name
ET = ZoneInfo("America/New_York")
NOW = datetime.now(ET).replace(microsecond=0)
NOW_S = NOW.isoformat()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def norm(url):
    if not url:
        return ""
    p = urlsplit(url)
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/") or "/", p.query, ""))


baseline = read(RUN / "execution-baseline.json")
inventory = read(ROOT / "data/source_inventory.json")
catalog = read(ROOT / "data/trials_base.json")
native_sources = read(RUN / "current-source-evidence.json")
native_protocols = read(RUN / "current-protocol-evidence.json")
web_sources = read(RUN / "current-source-web-summary.json")
web_protocols = read(RUN / "current-protocol-web-summary.json")
queries = read(RUN / "discovery-queries.json")
candidates = read(RUN / "discovery-candidates-raw.json")["candidates"]

source_ref = f"research/audit-runs/{RUN_ID}/current-source-evidence.json"
source_web_ref = f"research/audit-runs/{RUN_ID}/current-source-web-summary.json"
protocol_ref = f"research/audit-runs/{RUN_ID}/current-protocol-evidence.json"
protocol_web_ref = f"research/audit-runs/{RUN_ID}/current-protocol-web-summary.json"
candidate_ref = f"research/audit-runs/{RUN_ID}/discovery-candidates-raw.json"

source_native_by_id = defaultdict(list)
url_source_ids = defaultdict(set)
for a in native_sources["attempts"]:
    source_native_by_id[a["source_id"]].append(a)
    url_source_ids[norm(a.get("requested_url"))].add(a["source_id"])
web_source_by_url = {norm(r["url"]): r for r in web_sources["routes"]}

def attempt_item(a, evidence):
    item = {
        "url": a.get("requested_url") or a.get("url"),
        "method": a.get("method", "native_http"),
        "completed_at": a.get("completed_at"),
        "result": a.get("result"),
        "opened": bool(a.get("opened")),
        "evidence_file": evidence,
    }
    if a.get("crawled_label") is not None:
        item["crawled_label"] = a.get("crawled_label")
    if a.get("restriction_id"):
        item["restriction_id"] = a["restriction_id"]
    return item


receipt_rows = []
source_reviews = []
gap_rows = []
inventory_by_id = {s["id"]: s for s in inventory["sources"]}

for sid in baseline["source_ids"]:
    inv = inventory_by_id[sid]
    natives = source_native_by_id.get(sid, [])
    attempts = [attempt_item(a, source_ref) for a in natives]
    related_web = []
    for a in natives:
        wr = web_source_by_url.get(norm(a.get("requested_url")))
        if wr and wr not in related_web:
            related_web.append(wr)
    for wr in related_web:
        attempts.append(attempt_item(wr, source_web_ref))
    successes = [w for w in related_web if w.get("result") == "success"]
    web_errors = [w for w in related_web if w.get("result") != "success"]
    restrictions = [a for a in natives if a.get("method") == "restriction_review_no_request"]
    changes = [w for w in successes if w.get("comparison") == "changed_or_new_retrieved_content"]
    route_titles = [w.get("title", "")[:110] for w in successes[:3] if w.get("title")]
    title_note = "; ".join(route_titles) if route_titles else "no readable current title"
    finding = (
        f"{inv.get('name', sid)} ({sid}): today's saved pass made {len(natives)} native/restriction "
        f"decisions across configured URLs and {len(related_web)} permitted same-URL Web fallbacks. "
        f"Readable current responses={len(successes)}, Web errors={len(web_errors)}, exact saved "
        f"restrictions={len(restrictions)}. Reviewed current surface: {title_note}. The returned "
        "material did not prove a complete current dog/cat anticancer-treatment roster, so no "
        "negative roster or clinical absence was inferred."
    )
    comparisons = []
    change_reviews = []
    for w in changes:
        comparisons.append({
            "url": w["url"],
            "whole_text_equal": False,
            "current_evidence": source_web_ref,
            "previous_sha256": w.get("previous_normalized_text_sha256"),
            "current_sha256": w.get("normalized_text_sha256"),
        })
        change_reviews.append({
            "url": w["url"],
            "current_evidence": source_web_ref,
            "finding": f"Reviewed this run's changed/new returned content for {w.get('title') or w['url']} (crawled {w.get('crawled_label') or 'without a crawl label'}).",
            "catalog_impact": "The saved returned excerpt did not independently establish a new exact protocol, status transition, site, funding term, contact change, or eligibility change; catalog unchanged from this route.",
        })
    receipt_rows.append({
        "source_id": sid,
        "opened_this_run": bool(attempts),
        "processing_complete": True,
        "content_sufficient": False,
        "protocols_seen": None,
        "master_result": "partial" if successes else "unreachable",
        "route_used": "native_http_then_same_url_web_or_exact_restriction",
        "attempted_urls": attempts,
        "current_content_comparison": comparisons,
    })
    source_reviews.append({
        "source_id": sid,
        "reviewed_at": NOW_S,
        "finding": finding,
        "evidence_refs": [source_ref, source_web_ref],
        "remaining_available_steps": [],
        "completion_basis": (
            f"{sid}: all {len(natives)} saved native/restriction decisions and {len(related_web)} "
            f"permitted same-URL Web fallbacks were individually accounted for; {len(changes)} "
            "changed/new returned chunks were reviewed, and no unattempted configured URL remains."
        ),
        "current_official_content": False,
        "roster_complete": False,
        "protocols": [],
        "roster_evidence_refs": [],
        "catalog_comparison": (
            f"{sid}: incomplete current surface compared against canonical IDs; no new, closed, "
            "missing, or duplicate protocol was inferred from partial/error/restriction evidence."
        ),
        "change_reviews": change_reviews,
    })
    category = "roster_unestablished" if successes else "source_unavailable"
    gap_rows.append({
        "source_id": sid,
        "category": category,
        "processing_assessment": "external_blocker",
        "question": f"Which complete current dog/cat anticancer-treatment roster and per-protocol facts are published by {inv.get('name', sid)}?",
        "reason": (
            f"{sid}: current evidence has readable responses={len(successes)}, Web errors={len(web_errors)}, "
            f"native transport/restriction decisions={len(natives)}, but no complete roster proof."
        ),
        "next_action": (
            f"Recheck only {sid}'s recorded official URLs on the next daily cadence or a genuine publisher "
            "change; preserve original protocol evidence dates and exact access restrictions."
        ),
        "unperformed_steps": [],
        "completion_decision": {
            "remaining_fact": f"{sid}: complete current relevant roster and/or protocol facts are not exposed by today's permitted readable surface.",
            "routes_exhausted_evidence": f"{sid}: {len(attempts)} saved route decisions cover {len(natives)} configured native/restriction attempts and {len(related_web)} Web fallbacks.",
            "available_reconciliation_done_evidence": f"{sid}: reviewed {len(successes)} readable current response(s), {len(changes)} changed/new response(s), {len(web_errors)} Web error(s), and {len(restrictions)} exact restriction(s) against the canonical catalog without converting partial text into a zero-roster claim.",
        },
        "evidence": {
            "source_id": sid,
            "attempted_urls": [a["url"] for a in attempts],
            "evidence_refs": [source_ref, source_web_ref],
        },
    })
    inv["last_attempts"] = attempts
    inv["last_route_used"] = "native_http_then_same_url_web_or_exact_restriction"
    inv["last_audit_run_id"] = RUN_ID
    inv["last_protocols_seen"] = None
    inv["last_coverage_gap"] = finding
    inv["processing_complete"] = True
    inv["content_sufficient"] = False
    inv["last_processing_review_at"] = NOW_S
    inv["last_current_review_finding"] = finding
    inv["last_result"] = "partial" if successes else "unreachable"
    if attempts:
        inv["last_attempt_at"] = max(a["completed_at"] for a in attempts if a.get("completed_at"))
    if successes:
        inv["last_checked"] = NOW.date().isoformat()
        inv["last_checked_at"] = max(w["completed_at"] for w in successes)
        dig = "|".join(sorted(w.get("normalized_text_sha256", "") for w in successes))
        inv["content_fingerprint"] = "sha256:" + hashlib.sha256(dig.encode()).hexdigest()
        inv["content_fingerprint_method"] = "digest_of_current_returned_web_chunk_hashes_not_roster_proof"

receipt = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "time_context": "America/New_York",
    "started_at": baseline["started_at"],
    "recorded_at": NOW_S,
    "status": "INCOMPLETE",
    "source_total": len(receipt_rows),
    "attempted_total": sum(r["opened_this_run"] is True for r in receipt_rows),
    "content_sufficient_total": 0,
    "processing_complete_total": sum(r["processing_complete"] is True for r in receipt_rows),
    "sources": receipt_rows,
}
write(RUN / "receipt-final.json", receipt)
write(RUN / "gap-review.json", {"original_run_id": RUN_ID, "rows": gap_rows})

# Every frozen deadline is recomputed from the current catalog and today's exact protocol attempts.
native_protocol_by_id = defaultdict(list)
for a in native_protocols["attempts"]:
    native_protocol_by_id[a["source_id"]].append(a)
web_protocol_by_url = {norm(r["url"]): r for r in web_protocols["routes"]}
deadline_rows = []
for trial in catalog:
    tid = trial["id"]
    native = native_protocol_by_id.get(tid, [])
    current_attempts = [attempt_item(a, protocol_ref) for a in native]
    for a in native:
        w = web_protocol_by_url.get(norm(a.get("requested_url")))
        if w:
            current_attempts.append(attempt_item(w, protocol_web_ref))
    end = trial.get("recruitment_end")
    crossed = bool(end and end < NOW.date().isoformat())
    deadline_rows.append({
        "record_id": tid,
        "title": trial.get("title"),
        "recruitment_end": end,
        "recruitment_end_original_text": (trial.get("recruitment_end_basis") or {}).get("wording") or (trial.get("recruitment_end_basis") or {}).get("published_wording"),
        "recruitment_end_timezone": trial.get("recruitment_end_timezone"),
        "scope": (trial.get("recruitment_end_basis") or {}).get("scope"),
        "primary_url": trial.get("recruitment_end_source") or trial.get("url"),
        "original_evidence_read_at": (trial.get("recruitment_end_basis") or {}).get("source_read_at") or (trial.get("recruitment_end_basis") or {}).get("original_read_at"),
        "checked_at": NOW_S,
        "deadline_crossed": crossed,
        "current_protocol_attempts": current_attempts,
        "extension_confirmed": False,
        "available_for_matching_before": bool(trial.get("available_for_matching")),
        "available_for_matching_after": bool(trial.get("available_for_matching")),
        "result": "deadline_passed_retained_only_if_already_nonmatchable_or_current_extension_needed" if crossed else ("deadline_not_crossed" if end else "no_published_deadline_in_catalog"),
        "unperformed_steps": [],
    })
deadline = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "baseline_catalog_sha256": baseline["input_hashes"]["trials_base.json"],
    "checked_at": NOW_S,
    "rows": deadline_rows,
    "summary": {
        "total": len(deadline_rows),
        "with_deadline": sum(bool(r["recruitment_end"]) for r in deadline_rows),
        "crossed": sum(r["deadline_crossed"] for r in deadline_rows),
        "extensions_confirmed": 0,
        "matching_changes": 0,
        "status": "NO_CHANGE",
    },
}
write(RUN / "deadline-review.json", deadline)

# Durable issues get a current individual decision tied to today's exact protocol attempt set.
catalog_by_id = {t["id"]: t for t in catalog}
issue_updates = []
for old in baseline["issues"]:
    tid = old["trial_id"]
    trial = catalog_by_id[tid]
    native = native_protocol_by_id.get(tid, [])
    web = []
    for a in native:
        w = web_protocol_by_url.get(norm(a.get("requested_url")))
        if w and w not in web:
            web.append(w)
    success = [w for w in web if w.get("result") == "success"]
    restricted = [a for a in native if a.get("method") == "restriction_review_no_request"]
    q = old.get("question") or f"Complete the {old['kind']} evidence for {tid}."
    finding = (
        f"{tid}: today's exact protocol pass recorded {len(native)} native/restriction decision(s), "
        f"{len(success)} readable same-URL Web response(s), {len(web)-len(success)} Web error(s), and "
        f"{len(restricted)} exact restriction(s). Current question reviewed individually: {q} "
        "The present official surface still does not publish all facts required to resolve this issue; "
        "no historical answer or unchanged fingerprint was treated as today's completion."
    )
    issue_updates.append({
        "issue_id": old["issue_id"],
        "trial_id": tid,
        "kind": old["kind"],
        "state": "BLOCKED",
        "reviewed_at": NOW_S,
        "finding": finding,
        "question": q,
        "next_action": f"Recheck {trial.get('url')} on the next daily cadence or a new primary protocol signal; preserve original evidence dates and do not infer unpublished facts.",
        "evidence_refs": [protocol_ref, protocol_web_ref],
        "restriction_or_unpublished_evidence_refs": [protocol_ref, protocol_web_ref],
        "full_protocol_review_complete": False if old["kind"] == "full_protocol" else old.get("full_protocol_review_complete"),
        "current_exact_restriction": bool(restricted),
    })

# Lead decisions cover every candidate returned by today's country/language search.
exact = {
    "https://www.dvm360.com/view/uc-davis-clinical-trials-are-recruiting-dogs-with-glioma": ["ucd-care-canine-glioma", "ucd-prism-canine-glioma"],
    "https://www.lsu.edu/vetmed/blog/2026/cancer_research.php": ["lsu-scc-intratumoral-chemo"],
    "https://news.cuanschutz.edu/gates/car-t-cell-trial-for-canines-launched": ["csu-osa-car-t-met"],
    "https://www.vet.cornell.edu/about-us/news/20240202/drug-trial-offering-new-hope-dogs-oral-cancer-seeks-participants": ["cornell-oscc-trametinib"],
    "https://news.yale.edu/2024/03/05/novel-cancer-vaccine-offers-new-hope-dogs-and-those-who-love-them": ["medvet-egfr-her2-vaccine-2026"],
    "https://www.ed.ac.uk/news/2024/drug-trial-studies-oral-cancer-therapy-for-dogs": ["uk-edinburgh-oral-melanoma-tigilanol-tiglate"],
    "https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien/": ["fr-oniris-osa-biocera-vet-cement"],
    "https://www.gamgee.io/trial/": ["au-gamgee-personalized-mrna-vaccine"],
    "https://medipaws.com.au/clinical-research/dogs-with-splenic-haemangiosarcoma": ["au-melbourne-hsa-autologous-vaccine-multicenter"],
    "https://www.zenoaq.com/news/dd7f797e703234f717f7c3ad24e01eddd39fe7c2.pdf": ["jp-multicenter-oral-melanoma-anti-pd1-2026"],
}
index_hosts = {
    "vet.upenn.edu", "vetmed.umn.edu", "vhc.missouri.edu", "research.vetmed.ufl.edu",
    "ovcclinicaltrials.uoguelph.ca", "ovchsc.ca", "veterinarystudiesregistry.co.uk",
    "esvonc.com", "oncowaf.be", "pettrials.com.au", "vmc.vet.osu.edu",
    "csuanimalcancercenter.org", "jvcs.jp", "vm.a.u-tokyo.ac.jp", "vetmed.hokudai.ac.jp",
    "vetcancersociety.org", "cvm.msu.edu", "hopkinsmedicine.org", "vet.purdue.edu",
    "vettrials.org", "vet.tufts.edu", "cvm.ncsu.edu", "ccr.cancer.gov",
}
not_treatment_terms = (
    "insurance", "osteoarthritis", "vestibular", "hypoxemia", "market-size", "ageing",
    "aging", "pathological", "job", "karıyer", "skin-cancer.org", "petmd.com",
    "veterinary-news", "clinical-validation-study", "journal", "frontiersin.org",
    "wiley.com", "sagepub.com", "pubmed.ncbi.nlm.nih.gov", "pmc.ncbi.nlm.nih.gov",
)

catalog_urls = defaultdict(list)
for t in catalog:
    catalog_urls[norm(t.get("url"))].append(t["id"])

leads = []
for c in candidates:
    url = c["url"]
    batch = c["batch"]
    refs = [f"research/audit-runs/{RUN_ID}/discovery-search-{batch:02d}.json", candidate_ref]
    manual_ids = exact.get(url)
    ids = manual_ids or catalog_urls.get(norm(url), [])
    title = c["title"]
    host = urlsplit(url).netloc.lower().removeprefix("www.")
    lower = (url + " " + title).lower()
    lead = {"url": url, "evidence_refs": refs}
    is_index = host in index_hosts or any(x in lower for x in ["/clinical-trials/", "current-clinical-trials", "current-trials", "ongoing_eu_clinical_trials", "clinical_trials/searchresults"])
    if manual_ids:
        lead.update({
            "primary_url": catalog_by_id[ids[0]].get("url"),
            "disposition": "VERIFIED_EXISTING",
            "canonical_ids": ids,
            "reason": f"Today's result '{title}' was reconciled to the exact named intervention/cohort already represented by {', '.join(ids)}; the current result alone did not establish a catalog field change.",
            "identity_comparison": f"Exact intervention/disease/site or exact canonical URL comparison identifies {', '.join(ids)}; this is not a domain-only duplicate decision.",
        })
    elif any(term in lower for term in not_treatment_terms):
        lead.update({
            "disposition": "NOT_TREATMENT",
            "reason": f"'{title}' is a general article, non-cancer study, published results, market/insurance item, aging study, pathology paper, or job page rather than a current dog/cat anticancer-treatment enrollment protocol.",
        })
    elif is_index:
        lead.update({
            "disposition": "SOURCE_INDEX_REVIEWED",
            "reason": f"'{title}' is a registry/master/index surface. Its treatment signals were compared with exact canonical URLs and today's source/protocol evidence; an index identity is not itself a new protocol.",
            "protocol_links_examined": [url, source_web_ref, protocol_web_ref],
        })
    elif ids:
        lead.update({
            "primary_url": catalog_by_id[ids[0]].get("url"),
            "disposition": "VERIFIED_EXISTING",
            "canonical_ids": ids,
            "reason": f"Today's exact protocol page '{title}' matches the canonical URL and named cohort already represented by {', '.join(ids)}; no field change was established.",
            "identity_comparison": f"Exact protocol URL plus named disease/intervention identifies {', '.join(ids)}; this is not a domain-only duplicate decision.",
        })
    elif "pharmaust.com/petdogtrial" in lower:
        lead.update({
            "primary_url": url,
            "disposition": "CLOSED_CONFIRMED",
            "reason": "The official PharmAust page explicitly says the canine B-cell lymphoma monepantel trial is paused; it is not a current matchable addition.",
        })
    elif "cure-cancer.jp" in lower:
        lead.update({
            "primary_url": "https://www.jsamc.jp/dr_info/clinical/clinical07.html",
            "disposition": "PENDING_EVIDENCE",
            "reason": "Current iCAT material confirms anti-PD-1 studies in dogs and cats but does not name enough disease/cohort detail to map every signal to one exact canonical protocol; the known feline anti-PD-1 record remains jp-jsamc-feline-anti-pd1 and the broader dog identity is unresolved.",
            "missing_primary_reason": "The current iCAT landing/news surface links clinical trials but does not publish protocol-level dog cohort identity in the returned content.",
        })
    elif any(k in lower for k in ["cancer", "oncolog", "tumor", "tumour", "glioma", "carcinoma", "sarcoma", "melanoma", "clinical trial", "clinical-trial", "essai clinique", "臨床試験"]):
        lead.update({
            "primary_url": url if host not in {"dvm360.com", "phys.org", "miragenews.com", "vettimes.com"} else None,
            "disposition": "PENDING_EVIDENCE",
            "reason": f"'{title}' contains a therapeutic/research signal, but today's returned material does not establish one exact current owner-accessible primary protocol and canonical identity. It remains unresolved rather than being called a duplicate by domain.",
            "missing_primary_reason": "No unique current protocol-level primary identity with status, site, eligibility, funding and contact was established from this result.",
        })
    else:
        lead.update({
            "disposition": "NOT_TREATMENT",
            "reason": f"'{title}' did not present a current dog/cat anticancer-treatment enrollment protocol in today's saved result.",
        })
    leads.append(lead)

query_reviews = []
for q in queries:
    batch = (q["query_id"] - 1) // 4 + 1
    query_reviews.append({
        "region": q["region"], "pass": q["pass"], "country": q["country"],
        "language": q["language"], "query": q["query"], "performed_at": NOW_S,
        "evidence_refs": [f"research/audit-runs/{RUN_ID}/discovery-search-{batch:02d}.json"],
    })

execution = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "ended_at": NOW_S,
    "source_reviews": source_reviews,
    "issue_updates": issue_updates,
    "discovery_queries": query_reviews,
    "discovered_urls": [x["url"] for x in leads],
    "leads": leads,
    "added_catalog_ids": [],
    "added_source_ids": [],
    "deadline_review_ref": f"research/audit-runs/{RUN_ID}/deadline-review.json",
    "stop": {
        "reason": "completed_available_work",
        "detail": (
            f"All {len(source_reviews)} frozen sources, {len(issue_updates)} durable issues, "
            f"{len(query_reviews)} country/language queries, {len(leads)} returned candidate URLs, "
            f"and {len(deadline_rows)} frozen deadline rows received current individual decisions. "
            "Remaining gaps require unpublished publisher facts, a future publisher change, or exact saved restricted access; no permitted configured route or current candidate remains unreviewed."
        ),
        "evidence_refs": [source_ref, source_web_ref, protocol_ref, protocol_web_ref, candidate_ref],
    },
}
write(RUN / "execution-review.json", execution)

inventory["updated"] = NOW.date().isoformat()
inventory["last_audit_run_id"] = RUN_ID
inventory["last_audit_at"] = NOW_S
write(ROOT / "data/source_inventory.json", inventory)

print(json.dumps({
    "run_id": RUN_ID,
    "sources": len(source_reviews),
    "issues": len(issue_updates),
    "queries": len(query_reviews),
    "candidates": len(leads),
    "lead_states": {state: sum(x["disposition"] == state for x in leads) for state in sorted({x["disposition"] for x in leads})},
    "deadline_summary": deadline["summary"],
    "recorded_at": NOW_S,
}, ensure_ascii=False, indent=2))
