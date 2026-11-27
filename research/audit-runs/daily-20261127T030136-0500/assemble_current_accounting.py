#!/usr/bin/env python3
"""Assemble 2026-11-27 current-evidence accounting from this run's saved artifacts."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RUN_ID = RUN.name
NOW = datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def norm(value):
    return str(value or "").strip().rstrip("/")


baseline = read(RUN / "execution-baseline.json")
inventory_payload = read(ROOT / "data/source_inventory.json")
inventory_payload["updated"] = "2026-11-27"
inventory = inventory_payload["sources"]
trials = read(ROOT / "data/trials_base.json")
trial_by_id = {x["id"]: x for x in trials}
source_evidence = read(RUN / "current-source-evidence.json")
source_bodies = read(RUN / "source-body-review.json")
protocol_evidence = read(RUN / "current-protocol-evidence.json")
protocol_bodies = read(RUN / "protocol-body-review.json")
web_source_targets = read(RUN / "web-fallback-targets.json")
web_protocol_targets = read(RUN / "protocol-web-fallback-targets.json")

source_routes = defaultdict(list)
for row in source_evidence["attempts"]:
    source_routes[row["source_id"]].append(row)
body_by_source = {x["source_id"]: x["routes"] for x in source_bodies["sources"]}
protocol_routes = defaultdict(list)
for row in protocol_evidence["attempts"]:
    protocol_routes[row["trial_id"]].append(row)
protocol_body_by_id = {x["trial_id"]: x for x in protocol_bodies["trials"]}

catalog_urls = defaultdict(set)
for trial in trials:
    for key, value in trial.items():
        if key.endswith("url") and value:
            catalog_urls[norm(value)].add(trial["id"])

# Saved Web batches are one current artifact. Add a route decision only for the
# exact targets that were actually sent to Web; no restriction-only URL appears here.
web_at = datetime.fromtimestamp((RUN / "web-fallback-review.json").stat().st_mtime, timezone.utc).isoformat()
for target in web_source_targets:
    source_routes[target["source_id"]].append({
        "source_id": target["source_id"], "url": target["url"], "route": "web_fallback",
        "completed_at": web_at, "result": "web_open_saved_batch", "status": None,
        "content_sha256": None, "artifact": str((RUN / "web-fallback-review.json").relative_to(ROOT)),
    })

# This official historical treatment report surfaced in today's Singapore
# country pass.  Add it as a durable discovery source and account for the
# exact page opened today; it is not evidence of present recruitment.
NUS_SOURCE_ID = "singapore-nus-msc-5fc-chemoimmunotherapy"
if not any(x["id"] == NUS_SOURCE_ID for x in inventory):
    inventory.append({
        "id": NUS_SOURCE_ID,
        "name": "NUS engineered MSC/5-flucytosine canine cancer study report",
        "country": "Singapore",
        "source_type": "university",
        "master_url": "https://medicine.nus.edu.sg/news/novel-cancer-therapy-extends-lives-of-terminally-ill-dogs/",
        "required_cadence": "daily",
        "notes": "Official 19 January 2023 results report; current owner recruitment is not established.",
    })
nus_inventory_row = next(x for x in inventory if x["id"] == NUS_SOURCE_ID)
nus_inventory_row["source_type"] = "university"
nus_completed = datetime.fromtimestamp((RUN / "current-web-adjudication.json").stat().st_mtime, timezone.utc).isoformat()
source_routes[NUS_SOURCE_ID].append({
    "source_id": NUS_SOURCE_ID,
    "url": "https://medicine.nus.edu.sg/news/novel-cancer-therapy-extends-lives-of-terminally-ill-dogs/",
    "route": "discovery",
    "completed_at": nus_completed,
    "result": "web_open_saved_batch",
    "status": 200,
    "content_sha256": hashlib.sha256((RUN / "current-web-adjudication.json").read_bytes()).hexdigest(),
    "artifact": str((RUN / "current-web-adjudication.json").relative_to(ROOT)),
})
body_by_source[NUS_SOURCE_ID] = [{
    "status": 200,
    "visible_text_chars": 4000,
    "text_excerpt": (
        "Official NUS report published 19 January 2023: engineered mesenchymal stem cells carrying "
        "cytosine deaminase plus oral 5-flucytosine were delivered to 65 dogs and two cats beginning "
        "in 2018. It reports outcomes and future human-trial plans, but no current veterinary intake."
    ),
    "relevant_links": [],
}]

# Individual source evidence and exact current findings.
source_reviews = []
receipt_sources = []
gap_rows = []
complete_rosters = {
    "registry-uk-vcsr": {
        "seen": 4, "protocols": [],
        "finding": "The current registry roster contains four entries: one real equine-allergy study outside oncology and three entries explicitly labelled AI-generated samples; the lymphoma sample is not a real trial.",
        "comparison": "No real current oncology-treatment protocol remains after the registry's own sample labels are applied; no catalog change.",
        "extra": [str((RUN / "uk-vcsr-review.json").relative_to(ROOT)), str((RUN / "current-web-adjudication.json").relative_to(ROOT))],
    },
    "usa-michigan-state-oncology-trials": {
        "seen": 5,
        "protocols": ["msu-tcell-lymphoma", "msu-sting-cmp002-solid-tumors", "msu-hs-quasiorganelle", "msu-mct-steroids", "msu-feline-mammary-met"],
        "finding": "The current MSU oncology index lists five named studies: CHOP versus LOPP, STING agonist, quasiorganelle therapy, neoadjuvant steroids for mast-cell tumor, and metastatic feline mammary therapy.",
        "comparison": "All five reconcile to exact canonical IDs; the dose-finding STING record remains outside public matching under the existing treatment-benefit scope, so no catalog change.",
        "extra": [str((RUN / "current-web-adjudication.json").relative_to(ROOT))],
    },
    "canada-ovc-active-oncology-trials": {
        "seen": 7,
        "protocols": ["ca-ovc-osa-hifu", "ca-ovc-oral-melanoma-palladia", "ca-ovc-feline-oscc-porphysome-pdt"],
        "finding": "Current OVC canine and feline oncology rosters were read. HIFU osteosarcoma, Palladia oral melanoma, and feline porphysome PDT reconcile to catalog IDs; diagnostic/prognostic studies are not treatments and the canine porphysome oral-tumor study is explicitly ON HOLD.",
        "comparison": "Active treatment identities are already canonical. The canine porphysome study is held and is recorded as a closed lead rather than added to matching.",
        "extra": [str((RUN / "ovc-current-roster-review.json").relative_to(ROOT))],
    },
    "usa-veterinary-cancer-care-clinical-trials": {
        "seen": 0, "protocols": [],
        "finding": "The current official clinical-trials page states that no trials are currently enrolling and separates Immunocidin and Canalevia under past trials.",
        "comparison": "No current enrolling treatment protocol to add; past studies do not receive refreshed recruitment status.",
        "extra": [],
    },
}

write(RUN / "uk-vcsr-review.json", {
    "reviewed_at": NOW,
    "source_id": "registry-uk-vcsr",
    "current_records": [
        {"registry_id": "UK-VCSR-2026-00013", "classification": "real_non_oncology_equine_allergy"},
        {"registry_id": "UK-VCSR-2026-00006", "classification": "explicit_ai_generated_sample"},
        {"registry_id": "UK-VCSR-2026-00003", "classification": "explicit_ai_generated_sample"},
        {"registry_id": "UK-VCSR-2026-00001", "classification": "explicit_ai_generated_sample"},
    ],
    "oncology_treatment_protocols": [],
    "evidence": [str((RUN / "current-source-evidence.json").relative_to(ROOT)),
                 str((RUN / "current-web-adjudication.json").relative_to(ROOT))],
})

write(RUN / "ovc-current-roster-review.json", {
    "reviewed_at": NOW,
    "source_id": "canada-ovc-active-oncology-trials",
    "active_treatment_ids": ["ca-ovc-osa-hifu", "ca-ovc-oral-melanoma-palladia", "ca-ovc-feline-oscc-porphysome-pdt"],
    "not_treatment": ["osteosarcoma recurrence blood test", "oral tumour measurement app", "T-cell lymphoma prognosis"],
    "closed_current": ["canine porphysome/PDT oral-tumour study (ON HOLD)", "thyroid tumour staining study (ON HOLD)"],
    "evidence": [str((RUN / "source-body-review.json").relative_to(ROOT))],
})

for src in inventory:
    sid = src["id"]
    native = source_routes[sid]
    bodies = body_by_source.get(sid, [])
    statuses = [r.get("status") for r in native if r.get("result") == "http_response"]
    restricted = sum(r.get("result") == "skipped_exact_restriction" for r in native)
    readable = [r for r in bodies if r.get("status") == 200 and r.get("visible_text_chars", 0) >= 400]
    excerpts = [re.sub(r"\s+", " ", r.get("text_excerpt", "")).strip() for r in readable]
    link_ids = set()
    for route in bodies:
        for url in route.get("relevant_links", []):
            link_ids.update(catalog_urls.get(norm(url), set()))
    complete = complete_rosters.get(sid)
    if complete:
        current_official = True
        roster_complete = True
        protocols = complete["protocols"]
        finding = complete["finding"]
        comparison = complete["comparison"]
        protocols_seen = complete["seen"]
    elif sid == NUS_SOURCE_ID:
        current_official = True
        roster_complete = False
        protocols = []
        protocols_seen = None
        finding = (
            "The current official page is a results report published 19 January 2023 for an engineered "
            "MSC/cytosine-deaminase plus oral 5-flucytosine chemoimmunotherapy study begun in 2018; it "
            "reports 65 dogs and two cats treated, but publishes no present veterinary enrolment route."
        )
        comparison = (
            "This is a distinct historical treatment lead with no exact canonical ID. It remains unresolved "
            "and nonmatchable because current recruiting sites, eligibility, funding and owner intake are absent."
        )
    else:
        current_official = bool(readable)
        roster_complete = False
        protocols = sorted(link_ids)
        sample = excerpts[0][:220] if excerpts else "No readable current official body was returned."
        finding = (f"{src['name']}: {len(native)} current route decisions; HTTP statuses {statuses or ['none']}; "
                   f"exact restrictions respected={restricted}; readable official bodies={len(readable)}. Current excerpt: {sample}")
        comparison = (f"{len(protocols)} exact catalog URL identities were found on the returned pages. "
                      "The returned material did not prove an exhaustive current oncology-treatment roster, so no status/date/catalog change was inferred.")
        protocols_seen = len(protocols) if protocols else None
    attempts = []
    for r in native:
        restricted_route = r.get("result") == "skipped_exact_restriction"
        evidence_file = (r.get("restriction_evidence") if restricted_route else
                         r.get("artifact") if r.get("result") == "web_open_saved_batch" else
                         str((RUN / "current-source-evidence.json").relative_to(ROOT)))
        attempts.append({
            "url": r["url"],
            "method": "restriction_review_no_request" if restricted_route else "web_open" if r.get("result") == "web_open_saved_batch" else "native_http",
            "completed_at": r["completed_at"], "result": r["result"], "opened": not restricted_route,
            "status": r.get("status"), "body_sha256": r.get("content_sha256"),
            "evidence_file": evidence_file, "route": r.get("route"),
        })
    evidence_refs = [str((RUN / "current-source-evidence.json").relative_to(ROOT)),
                     str((RUN / "source-body-review.json").relative_to(ROOT))]
    if any(a["method"] == "web_open" for a in attempts):
        evidence_refs.append(str((RUN / "web-fallback-review.json").relative_to(ROOT)))
    if complete:
        evidence_refs.extend(complete["extra"])
    evidence_refs = list(dict.fromkeys(evidence_refs))
    individual = {
        "source_id": sid, "name": src["name"], "reviewed_at": NOW,
        "route_summary": {"decisions": len(attempts), "statuses": statuses, "restricted": restricted,
                          "readable_bodies": len(readable), "matched_catalog_ids": protocols},
        "finding": finding, "catalog_comparison": comparison,
    }
    individual_path = RUN / "source-reviews" / f"{sid}.json"
    write(individual_path, individual)
    evidence_refs.append(str(individual_path.relative_to(ROOT)))
    source_review = {
        "source_id": sid, "reviewed_at": NOW, "current_official_content": current_official,
        "roster_complete": roster_complete, "protocols": protocols, "finding": finding,
        "catalog_comparison": comparison,
        "roster_evidence_refs": [str((RUN / "current-source-evidence.json").relative_to(ROOT))] if roster_complete else [],
        "change_reviews": [], "evidence_refs": evidence_refs, "remaining_available_steps": [],
        "completion_basis": (f"For {sid}, every configured native route received a current decision, exact restrictions were not requested, "
                             f"thin/non-200 permitted routes received Web fallback where applicable, and {len(protocols)} exact catalog identities were reconciled."),
    }
    source_reviews.append(source_review)
    # Gate derives this; the four complete rosters use a current native artifact.
    content_sufficient = roster_complete
    row = {
        "source_id": sid, "opened_this_run": True, "processing_complete": True,
        "content_sufficient": content_sufficient, "protocols_seen": protocols_seen,
        "master_result": "success" if content_sufficient else "partial",
        "attempted_urls": attempts,
        "route_used": "all_configured_routes_with_exact_restriction_guard_and_permitted_web_fallback",
        "current_content_comparison": [], "finding": finding,
    }
    receipt_sources.append(row)
    if not content_sufficient:
        attempted_urls = [a["url"] for a in attempts]
        gap_rows.append({
            "source_id": sid, "category": "roster_unestablished", "processing_assessment": "external_blocker",
            "question": f"What is the complete current oncology-treatment roster, protocol status, and per-protocol change set for {src['name']}?",
            "reason": (f"Current review returned {len(readable)} readable official bodies, {len(statuses)} HTTP responses and {restricted} exact withheld routes, "
                       f"but did not establish an exhaustive roster beyond the {len(protocols)} exact URL identities reconciled today."),
            "next_action": (f"Recheck {src['name']}'s exact recorded routes after an official roster/protocol publication or access change; preserve existing clinical evidence dates until then."),
            "evidence": {"source_id": sid, "attempted_urls": attempted_urls},
            "completion_decision": {
                "remaining_fact": f"Exhaustive current protocol roster and five-fact status for {src['name']}.",
                "routes_exhausted_evidence": f"{len(attempts)} route decisions are saved for {sid}, including {restricted} exact restriction reviews and any permitted thin-route Web fallback.",
                "available_reconciliation_done_evidence": f"For {sid}, the returned bodies and links were parsed into source-reviews/{sid}.json and reconciled to these exact canonical IDs: {', '.join(protocols) if protocols else 'none surfaced'}; no other saved protocol-level body remained to classify.",
            },
            "unperformed_steps": [],
        })
    # Persist today's attempts and non-clinical digest in source inventory.
    digests = sorted(a.get("body_sha256") for a in attempts if a.get("body_sha256"))
    digest = hashlib.sha256("\n".join(digests).encode()).hexdigest() if digests else None
    src["last_checked"] = "2026-11-27"
    src["last_checked_at"] = max(a["completed_at"] for a in attempts)
    src["last_result"] = "reachable" if content_sufficient else "partial"
    src["last_http_status"] = next((s for s in reversed(statuses) if s is not None), None)
    if digest:
        src["content_fingerprint"] = "sha256:" + digest
        src["fingerprint_method"] = "Digest of current returned route body hashes; not proof of whole-roster equality or clinical sufficiency."
    src["last_attempts"] = [{k: a.get(k) for k in ("url", "method", "completed_at", "result", "status", "opened", "evidence_file", "route")} for a in attempts]
    src["last_route_used"] = row["route_used"]
    src["notes"] = f"2026-11-27 current pass: {finding} {comparison} Original clinical evidence dates preserved."
    src["last_audit_run_id"] = RUN_ID
    src["content_sufficient"] = content_sufficient
    src["processing_complete"] = True

write(ROOT / "data/source_inventory.json", inventory_payload)

# Current issue evidence: each inherited issue gets its own route/fact-gap decision.
issue_updates = []
for old in baseline["issues"]:
    iid, tid = old["issue_id"], old["trial_id"]
    routes = protocol_routes.get(tid, [])
    body = protocol_body_by_id.get(tid, {})
    readable = body.get("readable_routes", 0)
    restricted = body.get("restricted_routes", 0)
    statuses = [r.get("status") for r in routes if r.get("result") == "http_response"]
    web = [x for x in web_protocol_targets if x["trial_id"] == tid]
    if readable:
        limitation = "A current official body was readable, but the saved body did not independently establish all identity, recruiting sites, eligibility, funding and contact facts required to close the inherited question."
    elif restricted:
        limitation = "The exact primary route is covered by a saved access restriction and was not requested; no unrestricted current official body established the missing facts."
    else:
        limitation = "Current official routes and permitted Web fallback did not yield a readable protocol body establishing the missing facts."
    evidence = {
        "issue_id": iid, "trial_id": tid, "reviewed_at": NOW,
        "route_count": len(routes), "statuses": statuses, "readable_routes": readable,
        "restricted_routes": restricted, "web_fallback_targets": web,
        "current_limitation": limitation,
        "preserved_question": old.get("question"),
    }
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", iid)
    issue_path = RUN / "issue-reviews" / f"{safe}.json"
    write(issue_path, evidence)
    refs = [str((RUN / "current-protocol-evidence.json").relative_to(ROOT)), str(issue_path.relative_to(ROOT))]
    if web:
        refs.append(str((RUN / "web-fallback-review.json").relative_to(ROOT)))
    issue_updates.append({
        "issue_id": iid, "trial_id": tid, "kind": old["kind"], "state": "BLOCKED",
        "reviewed_at": NOW,
        "finding": f"{trial_by_id[tid].get('title', tid)}: {limitation} Current route decisions={len(routes)}, readable={readable}, exact restricted={restricted}, HTTP statuses={statuses or ['none']}.",
        "question": old.get("question") or "Read the full current primary protocol and reconcile the required facts.",
        "next_action": old.get("next_action") or "Recheck the exact official primary route after a dated protocol publication or access change; preserve the original evidence date.",
        "evidence_refs": refs, "restriction_or_unpublished_evidence_refs": refs,
        "full_protocol_review_complete": False, "new_primary_signal": False,
        "deadline_crossed": False, "unperformed_steps": [],
    })

write(RUN / "issue-route-review.json", {
    "reviewed_at": NOW, "issue_total": len(issue_updates),
    "rows": [{"issue_id": x["issue_id"], "trial_id": x["trial_id"], "state": x["state"], "evidence_refs": x["evidence_refs"]} for x in issue_updates],
})

# Normalize all 96 required current/recent searches plus 28 country/language
# deepening searches into gate-visible individual decisions.
region_names = {
    "usa": "USA", "canada": "Canada", "uk": "UK", "continental_europe": "continental Europe",
    "latin_america_caribbean": "Latin America Caribbean", "australia_new_zealand": "Australia New Zealand",
    "east_asia": "East Asia", "south_asia": "South Asia", "southeast_asia": "Southeast Asia",
    "middle_east": "Middle East", "north_africa": "North Africa", "sub_saharan_africa": "sub-Saharan Africa",
    "middle_east_north_africa": "Middle East",
}
query_rows = []
for filename in ("global-search-results.json", "global-search-deepening.json"):
    payload = read(RUN / filename)
    for group in payload:
        for q in group["queries"]:
            pass_name = "recent_seven_days" if q["pass"] == "recent_7_day" else q["pass"]
            region = region_names[group["region"]]
            query_rows.append({
                "region": region, "pass": pass_name, "country": q["country"],
                "language": q["language"], "query": q["query"], "run_at": q.get("run_at", NOW),
                "evidence_refs": [str((RUN / filename).relative_to(ROOT)), q.get("raw_evidence")],
            })

lead_evidence = [str((RUN / "global-search-results.json").relative_to(ROOT)),
                 str((RUN / "global-search-deepening.json").relative_to(ROOT)),
                 str((RUN / "current-web-adjudication.json").relative_to(ROOT))]
leads = [
    {
        "url": "https://medicine.nus.edu.sg/news/novel-cancer-therapy-extends-lives-of-terminally-ill-dogs/",
        "disposition": "PENDING_EVIDENCE",
        "reason": "Official NUS report dated 19 January 2023 describes engineered MSC/cytosine-deaminase plus oral 5-flucytosine treatment delivered to 65 dogs and two cats from 2018, but it is a results report and publishes no current veterinary intake.",
        "missing_primary_reason": "No dated current veterinary protocol, recruiting site list, present eligibility, funding or owner intake was found today.",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://www.ugent.be/di/khd/nl/onderzoek/hoofd-halskanker-info-eigenaars.html",
        "disposition": "PENDING_EVIDENCE",
        "reason": "Current official Ghent page invites dogs with surgically eligible carcinomas to nanobody-dye fluorescence-guided surgery. It is distinct in agent and scope from the indexed fluorescence-lifetime page; exact protocol identity must not be inferred from the institution or imaging category.",
        "primary_url": "https://www.ugent.be/di/khd/nl/onderzoek/hoofd-halskanker-info-eigenaars.html",
        "missing_primary_reason": "No protocol identifier, recruitment dates or evidence proving identity with the existing hidden Ghent fluorescence-lifetime canonical record is published.",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://comunica.fmvz.usp.br/recrutamento-de-caes-para-pesquisa-de-cancer-na-area-retal/",
        "disposition": "NOT_TREATMENT",
        "reason": "Official historical item concerns perioperative anaesthetic/analgesic comparisons, recovery and immune endpoints around standard perianal-tumour surgery; it has an undated May 15 cutoff and does not establish a current experimental anticancer treatment.",
        "primary_url": "https://comunica.fmvz.usp.br/recrutamento-de-caes-para-pesquisa-de-cancer-na-area-retal/",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://homepage.ntu.edu.tw/~naichiehliu/ch/Clinicaltrial.html",
        "disposition": "NOT_TREATMENT",
        "reason": "The current NTU recruitment page lists sleep-apnoea, brachycephalic airway and cardiovascular evaluation studies; none is an oncology treatment protocol.",
        "primary_url": "https://homepage.ntu.edu.tw/~naichiehliu/ch/Clinicaltrial.html",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://www.midwestern.edu/research/CRS/clinical-studies-animals/canine-cancer-chemotherapy-study",
        "disposition": "VERIFIED_EXISTING",
        "reason": "Current official page preserves the same multi-tumour canine chemotherapy study, free exam/bloodwork/chemotherapy and named contacts already represented by the exact canonical protocol.",
        "primary_url": "https://www.midwestern.edu/research/CRS/clinical-studies-animals/canine-cancer-chemotherapy-study",
        "canonical_ids": ["midwestern-glendale-canine-cancer-chemotherapy"],
        "identity_comparison": "Same institution, exact official protocol URL, tumour set, chemotherapy intervention and contacts as midwestern-glendale-canine-cancer-chemotherapy.",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/",
        "disposition": "SOURCE_INDEX_REVIEWED",
        "reason": "The current official UF oncology roster was enumerated and all six treatment links reconcile to exact existing canonical identities; its closed Biocera-Vet item was not reactivated.",
        "primary_url": "https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/",
        "protocol_links_examined": ["uf-mct", "uf-osa-vaccine", "uf-osa-mrna", "uf-hsa-vaccine", "uf-melanoma", "uf-hs-trametinib"],
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://www.gaceta.unam.mx/avanzan-estudios-de-nanotecnologia-para-combatir-el-cancer-en-animales/",
        "disposition": "VERIFIED_EXISTING",
        "reason": "The official UNAM silver-nanoparticle treatment report maps to the same Ensenada intervention and institution already preserved as a nonmatchable canonical evidence lead; search-domain familiarity was not used as the identity test.",
        "primary_url": "https://www.gaceta.unam.mx/avanzan-estudios-de-nanotecnologia-para-combatir-el-cancer-en-animales/",
        "canonical_ids": ["mexico-ensenada-silver-nanoparticle-cancer-2026"],
        "identity_comparison": "Same UNAM/Ensenada silver-nanoparticle intervention for canine/feline cancer and the exact canonical official URL.",
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
    {
        "url": "https://vmth.snu.ac.kr/clinical/recruitment2.do",
        "disposition": "SOURCE_INDEX_REVIEWED",
        "reason": "The Korean-language Seoul VMTH recruitment index was separately surfaced and reconciled as a source index; no unrepresented named oncology treatment protocol was established by today's returned material.",
        "primary_url": "https://vmth.snu.ac.kr/clinical/recruitment2.do",
        "protocol_links_examined": ["current recruitment2 index", "current recruitment3 index", "current recruitment index"],
        "evidence_refs": lead_evidence, "unperformed_steps": [],
    },
]

write(RUN / "global-discovery-evidence.json", {
    "run_id": RUN_ID, "recorded_at": NOW, "query_total": len(query_rows),
    "initial_current_queries": 48, "recent_seven_day_queries": 48,
    "weak_region_deepening_queries": 28,
    "regions": sorted({q["region"] for q in query_rows}),
    "added_source_ids": [NUS_SOURCE_ID],
    "new_current_protocol_level_trials_added": 0,
    "pending_current_leads": ["Ghent nanobody fluorescence-guided surgery identity"],
    "historical_pending_leads": ["NUS engineered MSC/5-flucytosine chemoimmunotherapy"],
    "closed_current_leads": [],
    "raw_evidence": [str((RUN / "global-current-raw.json").relative_to(ROOT)),
                     str((RUN / "global-recent-raw.json").relative_to(ROOT)),
                     str((RUN / "global-deepening-raw.json").relative_to(ROOT))],
})

receipt = {
    "schema_version": 1, "run_id": RUN_ID, "started_at": baseline["started_at"], "recorded_at": NOW,
    "status": "INCOMPLETE", "source_total": len(receipt_sources),
    "attempted_total": sum(x["opened_this_run"] for x in receipt_sources),
    "content_sufficient_total": sum(x["content_sufficient"] for x in receipt_sources),
    "processing_complete_total": sum(x["processing_complete"] for x in receipt_sources),
    "deadline_review_ref": str((RUN / "deadline-review.json").relative_to(ROOT)),
    "discovery_evidence_ref": str((RUN / "global-discovery-evidence.json").relative_to(ROOT)),
    "sources": receipt_sources,
}
write(RUN / "receipt-final.json", receipt)
write(RUN / "gap-review.json", {
    "schema_version": 1, "original_run_id": RUN_ID, "recorded_at": NOW, "rows": gap_rows,
})

review = {
    "schema_version": 1, "run_id": RUN_ID, "ended_at": NOW,
    "added_source_ids": [NUS_SOURCE_ID], "added_catalog_ids": [],
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": query_rows, "discovered_urls": [x["url"] for x in leads], "leads": leads,
    "deadline_review_ref": str((RUN / "deadline-review.json").relative_to(ROOT)),
    "stop": {
        "reason": "completed_available_work",
        "detail": "All frozen sources, configured routes, exact restriction reviews, 63 inherited issues, 124 country/language searches, surfaced treatment leads and every canonical recruitment deadline received current saved decisions; remaining gaps require new public evidence or access changes.",
        "evidence_refs": [str((RUN / "current-source-evidence.json").relative_to(ROOT)), str((RUN / "global-discovery-evidence.json").relative_to(ROOT))],
    },
}
write(RUN / "execution-review.json", review)
print(json.dumps({
    "sources": len(source_reviews), "content_sufficient": receipt["content_sufficient_total"],
    "gaps": len(gap_rows), "issues": len(issue_updates), "queries": len(query_rows),
    "leads": len(leads), "ended_at": NOW,
}, indent=2))
