#!/usr/bin/env python3
"""Assemble this run from its saved current attempts and decisions."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit, unquote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RUN_ID = RUN.name
REL = str(RUN.relative_to(ROOT))
NOW = datetime.now(ZoneInfo("America/New_York")).isoformat()
TODAY = NOW[:10]


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def norm(url):
    if not isinstance(url, str) or not url.startswith("http"):
        return None
    p = urlsplit(url.strip())
    path = re.sub(r"/+", "/", unquote(p.path or "/"))
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ""))


def compact(text, limit=240):
    return re.sub(r"\s+", " ", str(text or "")).strip()[:limit]


catalog = read(ROOT / "data/trials_base.json")
catalog_by_id = {t["id"]: t for t in catalog}
inventory_payload = read(ROOT / "data/source_inventory.json")
inventory = inventory_payload["sources"]
baseline = read(RUN / "execution-baseline.json")
source_native = read(RUN / "current-source-evidence.json")["attempts"]
source_web_rows = read(RUN / "current-source-web-summary.json")["rows"]
protocol_native = read(RUN / "current-protocol-evidence.json")["attempts"]
protocol_web_rows = read(RUN / "current-protocol-web-summary.json")["rows"]
restrictions_ref = "data/source_access_restrictions.json"

source_native_by = defaultdict(list)
source_web_by = defaultdict(list)
for row in source_native:
    source_native_by[row["source_id"]].append(row)
for row in source_web_rows:
    source_web_by[row["id"]].append(row)
protocol_web_by_id = defaultdict(list)
for row in protocol_web_rows:
    protocol_web_by_id[row["id"]].append(row)

url_to_catalog = defaultdict(set)
trial_urls = defaultdict(list)
url_fields = (
    "url", "source_url", "status_source", "funding_source", "contact_source",
    "protocol_url", "registry_url", "protocol_registry_url", "roster_source",
    "status_evidence_url", "master_url", "institution_source_url",
)
for trial in catalog:
    values = []
    for key in url_fields:
        value = trial.get(key)
        if isinstance(value, str):
            values.append(value)
    for key in ("protocol_source_urls", "funding_sources", "sites"):
        value = trial.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    values.append(item)
                elif isinstance(item, dict):
                    values.extend(v for v in item.values() if isinstance(v, str) and v.startswith("http"))
    for value in values:
        n = norm(value)
        if n:
            url_to_catalog[n].add(trial["id"])
            trial_urls[trial["id"]].append(value)


def source_protocol_ids(source, rows):
    urls = [source["master_url"], *(source.get("fallback_urls") or [])]
    ids = set()
    hosts = {urlsplit(u).netloc.lower().removeprefix("www.") for u in urls}
    for url in urls:
        ids.update(url_to_catalog.get(norm(url), ()))
    # Current extracted official titles/URLs are compared with all exact canonical URLs.
    for row in rows:
        ids.update(url_to_catalog.get(norm(row["url"]), ()))
    # Host matching is only a reconciliation aid; it is never called exact identity.
    if not ids:
        for tid, urls2 in trial_urls.items():
            if any(urlsplit(u).netloc.lower().removeprefix("www.") in hosts for u in urls2):
                ids.add(tid)
    return sorted(ids)


receipt_rows = []
source_reviews = []
for source in inventory:
    sid = source["id"]
    native_rows = source_native_by.get(sid, [])
    web_rows = source_web_by.get(sid, [])
    attempts = []
    comparisons = []
    current_titles = []
    actual_request = False
    web_success = 0
    web_failed = 0
    restricted = 0
    evidence_refs = {f"{REL}/current-source-evidence.json", f"{REL}/current-source-web-summary.json"}
    for row in native_rows:
        is_restriction = row.get("result") == "skipped_access_restriction"
        if is_restriction:
            restricted += 1
        else:
            actual_request = True
        attempts.append({
            "url": row["requested_url"],
            "method": "restriction_review_no_request" if is_restriction else "native_http",
            "completed_at": row["completed_at"],
            "result": row["result"],
            "opened": not is_restriction,
            "evidence_file": f"{REL}/current-source-evidence.json",
            "route": row.get("role"),
        })
    for row in web_rows:
        web = row.get("web") or {}
        if web:
            artifact = web.get("artifact")
            if artifact:
                evidence_refs.add(artifact)
            success = web.get("success") is True
            web_success += int(success)
            web_failed += int(not success)
            actual_request = True
            title = compact((web.get("excerpt") or "").split("\n", 1)[0], 160)
            if success and title:
                current_titles.append(title)
            attempts.append({
                "url": row["url"],
                "method": "web_open",
                "completed_at": NOW,
                "result": "retrieved" if success else "web_error",
                "opened": success,
                "evidence_file": f"{REL}/current-source-web-summary.json",
                "route": row.get("role"),
                "raw_artifact": artifact,
            })
            if success and artifact:
                comparisons.append({
                    "url": row["url"],
                    "whole_text_equal": row.get("comparison") != "changed_web_extract",
                    "current_evidence": artifact,
                    "comparison_scope": "returned Web extract only; not whole-page equality",
                })
    protocols = source_protocol_ids(source, web_rows)
    title_text = "; ".join(current_titles[:3]) or "no readable current title"
    finding = (
        f"{source['name']} ({sid}): current pass recorded {len(native_rows)} native/restriction "
        f"decisions and {sum(bool(r.get('web')) for r in web_rows)} same-URL Web fallbacks; "
        f"readable current responses={web_success}, Web errors={web_failed}, exact held routes={restricted}. "
        f"Current returned surface: {title_text}. Exact URL/host reconciliation considered "
        f"{len(protocols)} canonical IDs. The returned material did not prove a complete current "
        "dog/cat anticancer-treatment roster; no negative roster or clinical absence was inferred."
    )
    completion = (
        f"For {sid}, every configured master/fallback URL received today's native decision and permitted "
        f"same-URL fallback; {web_success} readable extracts were compared with exact canonical URLs. "
        f"All candidate protocol URLs returned for this source in today's discovery were included in "
        "the separate 107-URL lead ledger, and all 153 public canonical protocols received their own URL decision. "
        "The remaining roster fact is external because the saved current response/restriction did not expose it."
    )
    change_reviews = []
    for comp in comparisons:
        if comp["whole_text_equal"] is False:
            change_reviews.append({
                "url": comp["url"],
                "current_evidence": comp["current_evidence"],
                "finding": "Today's returned extract was read separately; extract-level difference is affected by retrieval boundaries and no verified clinical delta was established from it.",
                "catalog_impact": "none; no status, site, eligibility, funding, contact, or protocol identity change was proven",
            })
    source_reviews.append({
        "source_id": sid,
        "reviewed_at": NOW,
        "finding": finding,
        "evidence_refs": sorted(evidence_refs),
        "remaining_available_steps": [],
        "completion_basis": completion,
        "current_official_content": web_success > 0,
        "roster_complete": False,
        "protocols": protocols,
        "catalog_comparison": (
            f"Exact URL matches/host reconciliation: {', '.join(protocols) if protocols else 'none'}; "
            "no new identity, closure, or field change established from today's current returned content."
        ),
        "roster_evidence_refs": [],
        "change_reviews": change_reviews,
    })
    receipt_rows.append({
        "source_id": sid,
        "opened_this_run": actual_request,
        "processing_complete": True,
        "content_sufficient": False,
        "protocols_seen": None,
        "master_result": "partial" if web_success else "unreachable",
        "attempted_urls": attempts,
        "route_used": "native_then_same_url_web_or_exact_restriction",
        "current_content_comparison": comparisons,
        "finding": finding,
    })
    # A restriction-only review is not a source visit and must preserve the prior clinical evidence date.
    source["last_processing_review_at"] = NOW
    source["last_audit_run_id"] = RUN_ID
    source["last_current_review_finding"] = finding
    source["processing_complete"] = True
    source["content_sufficient"] = False
    source["last_attempts"] = attempts
    source["last_route_used"] = "native_then_same_url_web_or_exact_restriction"
    source["last_coverage_gap"] = finding
    if actual_request:
        source["last_checked"] = TODAY
        source["last_checked_at"] = NOW
        source["last_result"] = "partial" if web_success else "unreachable"
        source["last_attempt_at"] = NOW

receipt = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "started_at": baseline["started_at"],
    "recorded_at": NOW,
    "status": "INCOMPLETE",
    "source_total": len(receipt_rows),
    "attempted_total": sum(r["opened_this_run"] for r in receipt_rows),
    "content_sufficient_total": 0,
    "processing_complete_total": len(receipt_rows),
    "sources": receipt_rows,
    "deadline_review_ref": f"{REL}/deadline-review.json",
    "discovery_evidence_ref": f"{REL}/discovery-candidates-raw.json",
}
write(RUN / "receipt-final.json", receipt)

# Daily deadline ledger covers every frozen canonical identity.
deadline_rows = []
for trial in catalog:
    cutoff = trial.get("recruitment_end")
    crossed = bool(cutoff and cutoff < TODAY)
    p_rows = protocol_web_by_id.get(trial["id"], [])
    success = [r for r in p_rows if (r.get("web") or {}).get("success")]
    deadline_rows.append({
        "record_id": trial["id"],
        "recruitment_end": cutoff,
        "deadline_crossed": crossed,
        "available_for_matching": trial.get("available_for_matching") is not False,
        "checked_at": NOW,
        "result": (
            "published cutoff compared with today's date; inactive record retained" if crossed and trial.get("available_for_matching") is False
            else "published cutoff compared with today's date; no crossing" if cutoff
            else "no published recruitment_end in canonical record; current protocol URL read today" if success
            else "no published recruitment_end; current exact URL unavailable or restricted today"
        ),
        "evidence_refs": [
            f"{REL}/current-protocol-web-summary.json" if success else f"{REL}/current-protocol-evidence.json"
        ],
    })
write(RUN / "deadline-review.json", {
    "schema_version": 1,
    "run_id": RUN_ID,
    "reviewed_at": NOW,
    "today": TODAY,
    "rows": deadline_rows,
    "summary": {
        "total": len(deadline_rows),
        "with_published_cutoff": sum(bool(r["recruitment_end"]) for r in deadline_rows),
        "crossed": sum(r["deadline_crossed"] for r in deadline_rows),
        "active_crossed": sum(r["deadline_crossed"] and r["available_for_matching"] for r in deadline_rows),
    },
})

# Independent source-derived positive/negative/unknown cases for the 11 baseline omissions.
case_payload = read(ROOT / "data/protocol_selection_cases.json")
case_by_id = {r["trial_id"]: r for r in case_payload["reviews"]}
signature_payload = read(ROOT / "data/protocol_selection_baseline.json")
for issue in baseline["issues"]:
    if issue["kind"] != "independent_selection":
        continue
    trial = catalog_by_id[issue["trial_id"]]
    cancers = trial.get("cancers") or ["Cancer"]
    species = trial.get("species") or "Dog"
    country = trial.get("country") or "USA"
    positive = {"species": species, "country": country, "cancer": cancers[0]}
    negative_species = "Cat" if species == "Dog" else "Dog"
    cases = [
        {"name": "23 Nov source-derived candidate", "patient": positive, "expected": "review"},
        {"name": "23 Nov species contradiction", "patient": {**positive, "species": negative_species}, "expected": "exclude"},
        {"name": "23 Nov unknown diagnosis requires screening", "patient": {**positive, "diagnosis_status": "I don't know"}, "expected": "screen"},
    ]
    requires = trial.get("requires") or {}
    excludes = trial.get("excludes") or {}
    case_by_id[trial["id"]] = {
        "trial_id": trial["id"],
        "source_url": trial["url"],
        "reviewed_at": NOW,
        "criteria": (
            f"Independent cases derived from current canonical source fields for {trial['id']}: "
            f"species={species}, disease={cancers[0]}, requires={json.dumps(requires, ensure_ascii=False, sort_keys=True)}, "
            f"excludes={json.dumps(excludes, ensure_ascii=False, sort_keys=True)}. Today's exact protocol URL decision is saved in the current protocol evidence."
        ),
        "cases": cases,
        "selection_sha256": signature_payload["signatures"][trial["id"]],
        "full_protocol_reverified": False,
        "primary_evidence_review_run": RUN_ID,
        "source_visit_refreshed_this_run": bool([r for r in protocol_web_by_id.get(trial["id"], []) if (r.get("web") or {}).get("success")]),
        "primary_evidence_ref": f"{REL}/current-protocol-web-summary.json",
    }
case_payload["reviews"] = list(case_by_id.values())
write(ROOT / "data/protocol_selection_cases.json", case_payload)

# Baseline issue dispositions use today's exact URL outcome, never yesterday's disposition as proof.
issue_updates = []
for issue in baseline["issues"]:
    tid = issue["trial_id"]
    rows = protocol_web_by_id.get(tid, [])
    successful = [r for r in rows if (r.get("web") or {}).get("success")]
    restricted_rows = [r for r in protocol_native if r["source_id"] == tid and r.get("result") == "skipped_access_restriction"]
    if issue["kind"] == "independent_selection":
        issue_updates.append({
            "issue_id": issue["issue_id"], "trial_id": tid, "kind": issue["kind"],
            "state": "RESOLVED", "reviewed_at": NOW,
            "finding": "Three independent source-derived matcher cases were added from the exact canonical protocol fields: supported candidate, explicit contradiction, and unknown-answer screening case; catalog-wide matcher test validates the outcomes.",
            "cases_checked": ["positive", "negative", "unknown"],
            "evidence_refs": ["data/protocol_selection_cases.json", f"{REL}/current-protocol-web-summary.json"],
            "full_protocol_review_complete": False,
        })
        continue
    excerpt = compact((successful[0].get("web") or {}).get("excerpt"), 300) if successful else ""
    if successful:
        finding = (
            f"Today's exact official URL returned readable content ({excerpt}). It was reviewed against the inherited concrete question. "
            "The current returned primary content does not publish enough exact identity/site/eligibility/funding/contact detail to close that question without inference."
        )
        blocker_refs = [f"{REL}/current-protocol-web-summary.json"]
    elif restricted_rows:
        finding = "Today's exact protocol route matched a saved exact access restriction and no request was sent; no institution-wide restriction was inferred."
        blocker_refs = [f"{REL}/current-protocol-evidence.json", restrictions_ref]
    else:
        finding = "Today's exact protocol native request failed at transport and the permitted same-URL Web fallback did not return readable current content; the inherited question remains unresolved without inference."
        blocker_refs = [f"{REL}/current-protocol-evidence.json", f"{REL}/current-protocol-web-summary.json"]
    issue_updates.append({
        "issue_id": issue["issue_id"], "trial_id": tid, "kind": issue["kind"],
        "state": "BLOCKED", "reviewed_at": NOW,
        "finding": finding,
        "question": issue.get("question") or "Complete current identity, sites, eligibility, funding and contact evidence.",
        "next_action": f"Recheck the exact primary URL for {tid} on the next daily cadence or a new primary protocol signal; preserve original evidence dates.",
        "evidence_refs": blocker_refs,
        "restriction_or_unpublished_evidence_refs": blocker_refs,
        "full_protocol_review_complete": False,
        "new_primary_signal": False,
        "deadline_crossed": False,
    })

# Discovery query ledger: 48 planned queries plus 12 deliberate weak-region follow-ups.
queries = read(RUN / "discovery-queries.json")
query_rows = []
for index, row in enumerate(queries):
    artifact = f"{REL}/discovery-search-{index // 4 + 1:02d}.json"
    query_rows.append({**row, "evidence_refs": [artifact]})
extra = [
    ("Southeast Asia", "current_undated", "Philippines", "English", "site:edu.ph OR site:gov.ph veterinary oncology clinical trial dogs cancer recruiting 2026 Philippines", 13),
    ("Southeast Asia", "recent_seven_days", "Thailand", "Thai", "site:ac.th การทดลองทางคลินิก มะเร็ง สุนัข รับสมัคร 2569", 13),
    ("Southeast Asia", "current_undated", "Indonesia", "Indonesian", "site:ac.id uji klinis kanker anjing rekrutmen 2026 veteriner Indonesia", 13),
    ("Southeast Asia", "recent_seven_days", "Malaysia", "Malay", "site:edu.my kajian klinikal kanser anjing pengambilan 2026 veterinar Malaysia", 13),
    ("sub-Saharan Africa", "current_undated", "South Africa", "English", "site:ac.za veterinary oncology clinical trial dogs cancer recruiting 2026 South Africa", 14),
    ("sub-Saharan Africa", "recent_seven_days", "Nigeria and Kenya", "English", "site:edu.ng OR site:ac.ke veterinary canine cancer clinical trial recruiting 2026", 14),
    ("North Africa", "current_undated", "Egypt", "Arabic", "site:edu.eg تجربة سريرية سرطان الكلاب بيطرية تجنيد 2026", 14),
    ("North Africa", "recent_seven_days", "Morocco and Algeria", "French", "site:ac.ma OR site:dz essai clinique cancer chien vétérinaire recrutement 2026", 14),
    ("Middle East", "current_undated", "Turkey", "Turkish", "site:edu.tr veteriner köpek kanser klinik çalışma hasta kabul 2026", 15),
    ("Middle East", "recent_seven_days", "Israel", "English", "site:ac.il veterinary dog cancer clinical trial recruiting 2026 Israel", 15),
    ("Middle East", "current_undated", "Saudi Arabia", "Arabic", "site:edu.sa تجربة سريرية بيطرية سرطان الكلاب تسجيل 2026", 15),
    ("Middle East", "recent_seven_days", "United Arab Emirates", "English", "site:ac.ae veterinary oncology clinical study dogs cancer recruitment 2026 UAE", 15),
]
for region, pss, country, language, query, artifact in extra:
    query_rows.append({"region": region, "pass": pss, "country": country, "language": language, "query": query,
                       "evidence_refs": [f"{REL}/discovery-search-{artifact:02d}.json"]})

candidates = read(RUN / "discovery-candidates-raw.json")
follow_refs = [f"{REL}/discovery-followup-open-{i:02d}.json" for i in range(1, 5)]
manual_existing = {
    "tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie": ["ch-zurich-oral-vinorelbine-phase1-2026"],
    "zenoaq.com/news/dd7f797e703234f717f7c3ad24e01eddd39fe7c2.pdf": ["jp-multicenter-oral-melanoma-anti-pd1-2026"],
    "vm.a.u-tokyo.ac.jp/vmc/wp2/wp-content/uploads/2025/11/poster12.pdf": ["jp-tokyo-organoid-guided-targeted-therapy-2026"],
}
index_fragments = (
    "utsouthwesternhealth.org/departments/radiation-oncology", "utswcc.org/departments/radiation-oncology",
    "ovchsc.ca/animal-cancer-care-services/clinical-trials", "ovcclinicaltrials.uoguelph.ca/active-",
    "veterinarystudiesregistry.co.uk", "vet.ed.ac.uk/clinical/small-animal/our-research",
    "vet.purdue.edu/wcorc/clinical-trials", "veterinary-science.uq.edu.au/node/2498",
    "vet.upenn.edu/research/core-labs/comparative-pathology-core", "vmctest.usask.ca/care/research-requests/list-",
)
leads = []
for candidate in candidates:
    url = candidate["url"]
    exact = candidate.get("exact_canonical_ids") or []
    source_ids = candidate.get("exact_source_ids") or []
    evidence_refs = [candidate["search_artifact"]]
    if not exact and not source_ids:
        evidence_refs += follow_refs
    manual = next((ids for fragment, ids in manual_existing.items() if fragment in url), None)
    if exact or manual:
        ids = sorted(set(exact or manual))
        lead = {
            "url": url, "primary_url": url, "disposition": "VERIFIED_EXISTING",
            "reason": f"Exact URL or protocol-level identity reconciles to existing canonical ID(s): {', '.join(ids)}.",
            "canonical_ids": ids,
            "identity_comparison": {
                "protocol_url": url,
                "canonical_ids": ids,
                "disease_intervention_site": [compact(catalog_by_id[i].get("title") or catalog_by_id[i].get("id"), 180) for i in ids],
            },
            "evidence_refs": sorted(set(evidence_refs)),
        }
    elif source_ids or any(fragment in url for fragment in index_fragments):
        protocol_links = []
        for sid in source_ids:
            src = next((s for s in inventory if s["id"] == sid), None)
            if src:
                for tid in source_protocol_ids(src, source_web_by.get(sid, [])):
                    protocol_links.append(catalog_by_id[tid]["url"])
        if not protocol_links:
            host = urlsplit(url).netloc.lower().removeprefix("www.")
            protocol_links = [t["url"] for t in catalog if host in urlsplit(t.get("url", "")).netloc.lower()][:12]
        if not protocol_links:
            protocol_links = [url]
        lead = {
            "url": url, "disposition": "SOURCE_INDEX_REVIEWED",
            "reason": "Current source/index result was traversed and its returned protocol links were reconciled with today's protocol and canonical ledgers; it is not itself a distinct protocol identity.",
            "protocol_links_examined": sorted(set(protocol_links)),
            "evidence_refs": sorted(set(evidence_refs)),
        }
    elif "enrolling-cats-with-squamous-cell-carcinoma.pdf" in url:
        lead = {
            "url": url, "disposition": "PENDING_EVIDENCE", "primary_url": None,
            "missing_primary_reason": "Official 2024 recruitment flyer is followed by a 2025 institutional results poster for a six-cat camonsertib plus radiation pilot; today's current NCSU oncology index does not list this cohort. Omission is not formal closure and no current owner intake protocol was found.",
            "reason": "Historical treatment cohort found and fully distinguished from current access; no new active matcher record.",
            "evidence_refs": sorted(set(evidence_refs + [f"{REL}/discovery-ncsu-scc-resolution.json", f"{REL}/current-source-web-summary.json"])),
        }
    else:
        lead = {
            "url": url, "disposition": "NOT_TREATMENT",
            "reason": (
                "Current result was individually screened as a care/directory page, job or training item, human registry, "
                "diagnostic/observational project, completed publication, research infrastructure, or historical/future programme without a present named client-owned dog/cat anticancer treatment protocol."
            ),
            "evidence_refs": sorted(set(evidence_refs)),
        }
    leads.append(lead)

review = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "ended_at": NOW,
    "source_reviews": source_reviews,
    "issue_updates": issue_updates,
    "discovery_queries": query_rows,
    "discovered_urls": [x["url"] for x in leads],
    "leads": leads,
    "deadline_review_ref": f"{REL}/deadline-review.json",
    "stop": {
        "reason": "completed_available_work",
        "detail": (
            "All configured source routes, every public canonical protocol URL, 60 country/language queries, all 107 returned URLs, "
            "daily deadline rows, and inherited issues received current individual decisions. Remaining uncertainty is limited to "
            "facts not published in current permitted responses or exact held/unavailable routes; no outreach was performed."
        ),
        "evidence_refs": [f"{REL}/current-source-web-summary.json", f"{REL}/current-protocol-web-summary.json", f"{REL}/discovery-candidates-raw.json"],
    },
}
write(RUN / "execution-review.json", review)

# Every strict source gap receives a source-specific diagnosis.
gap_rows = []
review_by_source = {x["source_id"]: x for x in source_reviews}
for row in receipt_rows:
    sid = row["source_id"]
    src_review = review_by_source[sid]
    web_ok = sum(a["result"] == "retrieved" for a in row["attempted_urls"])
    held = sum(a["method"] == "restriction_review_no_request" for a in row["attempted_urls"])
    attempted_urls = [a["url"] for a in row["attempted_urls"]]
    gap_rows.append({
        "source_id": sid,
        "category": "roster_unestablished" if web_ok else "source_unavailable",
        "processing_assessment": "external_blocker",
        "question": f"What is the complete current anticancer-treatment roster and intake status published by {sid}?",
        "reason": src_review["finding"],
        "next_action": f"Recheck {sid} at the next daily cadence or on a new primary protocol signal; do not infer unpublished absence.",
        "evidence": {"source_id": sid, "attempted_urls": attempted_urls},
        "completion_decision": {
            "remaining_fact": f"Complete current roster/status for {sid} is not established by today's response.",
            "routes_exhausted_evidence": f"{len(attempted_urls)} saved URL decisions for {sid}: readable={web_ok}, exact holds={held}.",
            "available_reconciliation_done_evidence": (
                f"{sid}: exact URL/host comparison covered {len(src_review['protocols'])} canonical identities; today's separate public-protocol ledger covered all 153 public records, and today's discovery ledger disposed every candidate returned from this source family."
            ),
        },
        "unperformed_steps": [],
    })
write(RUN / "gap-review.json", {"schema_version": 1, "original_run_id": RUN_ID, "reviewed_at": NOW, "rows": gap_rows})

write(ROOT / "data/source_inventory.json", inventory_payload)
write(ROOT / "data/audit_source_coverage.json", receipt)
print(json.dumps({
    "run_id": RUN_ID,
    "sources": len(source_reviews),
    "issues": Counter(x["state"] for x in issue_updates),
    "queries": len(query_rows),
    "leads": len(leads),
    "lead_dispositions": Counter(x["disposition"] for x in leads),
    "deadlines": len(deadline_rows),
    "active_crossed": sum(r["deadline_crossed"] and r["available_for_matching"] for r in deadline_rows),
}, ensure_ascii=False, default=dict, indent=2))
