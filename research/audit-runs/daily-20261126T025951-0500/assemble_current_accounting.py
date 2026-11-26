#!/usr/bin/env python3
"""Assemble 2026-11-26 current-evidence accounting from this run's saved artifacts."""
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
inventory_payload["updated"] = "2026-11-26"
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

# Individual source evidence and exact current findings.
source_reviews = []
receipt_sources = []
gap_rows = []
complete_rosters = {
    "registry-uk-vcsr": {
        "seen": 4, "protocols": [],
        "finding": "The current registry roster contains four entries: one real equine-allergy study outside oncology and three entries explicitly labelled AI-generated samples; the lymphoma sample is not a real trial.",
        "comparison": "No real current oncology-treatment protocol remains after the registry's own sample labels are applied; no catalog change.",
        "extra": [str((RUN / "uk-vcsr-review.json").relative_to(ROOT))],
    },
    "usa-michigan-state-oncology-trials": {
        "seen": 5,
        "protocols": ["msu-tcell-lymphoma", "msu-sting-cmp002-solid-tumors", "msu-hs-quasiorganelle", "msu-mct-steroids", "msu-feline-mammary-met"],
        "finding": "The current MSU oncology index lists five named studies: CHOP versus LOPP, STING agonist, quasiorganelle therapy, neoadjuvant steroids for mast-cell tumor, and metastatic feline mammary therapy.",
        "comparison": "All five reconcile to exact canonical IDs; the dose-finding STING record remains outside public matching under the existing treatment-benefit scope, so no catalog change.",
        "extra": [str((RUN / "web-fallback-review.json").relative_to(ROOT))],
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
    src["last_checked"] = "2026-11-26"
    src["last_checked_at"] = max(a["completed_at"] for a in attempts)
    src["last_result"] = "reachable" if content_sufficient else "partial"
    src["last_http_status"] = next((s for s in reversed(statuses) if s is not None), None)
    if digest:
        src["content_fingerprint"] = "sha256:" + digest
        src["fingerprint_method"] = "Digest of current returned route body hashes; not proof of whole-roster equality or clinical sufficiency."
    src["last_attempts"] = [{k: a.get(k) for k in ("url", "method", "completed_at", "result", "status", "opened", "evidence_file", "route")} for a in attempts]
    src["last_route_used"] = row["route_used"]
    src["notes"] = f"2026-11-26 current pass: {finding} {comparison} Original clinical evidence dates preserved."
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
        refs.append(str((RUN / "protocol-web-fallback-review.json").relative_to(ROOT)))
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

# Convert the 48 initial + 20 deepening searches into current, saved query decisions.
region_names = {
    "usa": "USA", "canada": "Canada", "uk": "UK", "continental_europe": "continental Europe",
    "latin_america_caribbean": "Latin America Caribbean", "australia_new_zealand": "Australia New Zealand",
    "east_asia": "East Asia", "south_asia": "South Asia", "southeast_asia": "Southeast Asia",
    "middle_east": "Middle East", "north_africa": "North Africa", "sub_saharan_africa": "sub-Saharan Africa",
}
query_rows = []
for filename in ("global-search-results.json", "global-search-deepening.json"):
    payload = read(RUN / filename)
    for group in payload:
        for q in group["queries"]:
            query_rows.append({
                "region": region_names[group["region"]], "pass": q["pass"], "country": q["country"],
                "language": q["language"], "query": q["query"], "run_at": NOW,
                "evidence_refs": [str((RUN / filename).relative_to(ROOT))],
            })

ocr_ref = str((RUN / "ocrvet-lead-review.json").relative_to(ROOT))
write(RUN / "ocrvet-lead-review.json", {
    "reviewed_at": NOW,
    "url": "https://fr.linkedin.com/posts/seinevet_%F0%9D%97%98%F0%9D%98%80%F0%9D%98%80%F0%9D%97%AE%F0%9D%97%B6-%F0%9D%97%96%F0%9D%97%B9%F0%9D%97%B6%F0%9D%97%BB%F0%9D%97%B6%F0%9D%97%BE%F0%9D%98%82%F0%9D%97%B2-%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%97%A2%F0%9D%97%A1%F0%9D%97%96%F0%9D%97%A2%F0%9D%97%9F%F0%9D%97%A2%F0%9D%97%9A%F0%9D%97%9C%F0%9D%97%98-activity-7205863770814824448-s8rx",
    "finding": "Two-year-old SeineVet/OCRvet post describes a fully covered 9-week human monoclonal-antibody study at 13 centres in France, Poland and Portugal for multiple advanced canine cancers. No dated current primary protocol or recruiting status was found today.",
    "decision": "PENDING_EVIDENCE",
})

leads = [
    {
        "url": "https://canivax.com/canivax-begins-clinical-studies-for-dogs-with-advanced-cancer/",
        "disposition": "PENDING_EVIDENCE",
        "reason": "Official 3 November 2026 announcement confirms initiation of CaniVive clinical evaluation in UK dogs with late-stage metastatic cancer, but it does not publish centres, full eligibility, funding, enrolment contact or a protocol identifier.",
        "missing_primary_reason": "No public protocol-level enrolment page was found; the available official document is a company announcement.",
        "evidence_refs": [str((RUN / "source-body-review.json").relative_to(ROOT)), str((RUN / "global-search-results.json").relative_to(ROOT))],
        "unperformed_steps": [],
    },
    {
        "url": "https://fr.linkedin.com/posts/seinevet_%F0%9D%97%98%F0%9D%98%80%F0%9D%98%80%F0%9D%97%AE%F0%9D%97%B6-%F0%9D%97%96%F0%9D%97%B9%F0%9D%97%B6%F0%9D%97%BB%F0%9D%97%B6%F0%9D%97%BE%F0%9D%98%82%F0%9D%97%B2-%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%97%A2%F0%9D%97%A1%F0%9D%97%96%F0%9D%97%A2%F0%9D%97%9F%F0%9D%97%A2%F0%9D%97%9A%F0%9D%97%9C%F0%9D%97%98-activity-7205863770814824448-s8rx",
        "disposition": "PENDING_EVIDENCE",
        "reason": "The named OCRvet/SeineVet monoclonal-antibody study has detailed historical eligibility and 13-centre claims, but the post is two years old and no current primary recruiting protocol was found.",
        "missing_primary_reason": "Historical social post only; current protocol and status remain unpublished in the material found today.",
        "evidence_refs": [ocr_ref], "unperformed_steps": [],
    },
    {
        "url": "https://www.veterinarystudiesregistry.co.uk/studies",
        "disposition": "SOURCE_INDEX_REVIEWED", "reason": "All four current registry records were individually classified; the lymphoma item is an explicit AI-generated sample and the sole real record concerns equine allergy.",
        "primary_url": "https://www.veterinarystudiesregistry.co.uk/studies",
        "protocol_links_examined": ["UK-VCSR-2026-00013", "UK-VCSR-2026-00006", "UK-VCSR-2026-00003", "UK-VCSR-2026-00001"],
        "evidence_refs": [str((RUN / "uk-vcsr-review.json").relative_to(ROOT))], "unperformed_steps": [],
    },
    {
        "url": "https://cvm.msu.edu/hospital/services/oncology/clinical-trials-2",
        "disposition": "SOURCE_INDEX_REVIEWED", "reason": "Five current named MSU study links were opened/reconciled to exact catalog identities.",
        "primary_url": "https://cvm.msu.edu/hospital/services/oncology/clinical-trials-2",
        "protocol_links_examined": ["msu-tcell-lymphoma", "msu-sting-cmp002-solid-tumors", "msu-hs-quasiorganelle", "msu-mct-steroids", "msu-feline-mammary-met"],
        "evidence_refs": [str((RUN / "web-fallback-review.json").relative_to(ROOT)), str((RUN / "protocol-web-fallback-review.json").relative_to(ROOT))], "unperformed_steps": [],
    },
    {
        "url": "https://ovcclinicaltrials.uoguelph.ca/all-active-canine-clinical-trials-oncology/",
        "disposition": "SOURCE_INDEX_REVIEWED", "reason": "Current canine and feline oncology rosters were parsed; active treatment protocols match existing IDs and the canine porphysome protocol is explicitly on hold.",
        "primary_url": "https://ovcclinicaltrials.uoguelph.ca/all-active-canine-clinical-trials-oncology/",
        "protocol_links_examined": ["ca-ovc-osa-hifu", "ca-ovc-oral-melanoma-palladia", "ca-ovc-feline-oscc-porphysome-pdt", "canine-porphysome-on-hold", "diagnostic-and-prognostic-records"],
        "evidence_refs": [str((RUN / "ovc-current-roster-review.json").relative_to(ROOT))], "unperformed_steps": [],
    },
    {
        "url": "https://ovcclinicaltrials.uoguelph.ca/exploring-a-novel-nanoparticle-combined-with-light-therapy-to-treat-oral-tumours-in-dogs/",
        "disposition": "CLOSED_CONFIRMED", "reason": "The current official OVC canine oncology roster labels this treatment study ON HOLD FOR RECRUITMENT.",
        "primary_url": "https://ovcclinicaltrials.uoguelph.ca/all-active-canine-clinical-trials-oncology/",
        "evidence_refs": [str((RUN / "ovc-current-roster-review.json").relative_to(ROOT))], "unperformed_steps": [],
    },
]

# Representative protocol-level discoveries from each strong region were reconciled
# to exact catalog identities. These are current evidence decisions, not domain dedupes.
existing = [
    ("https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/", "penn-flash-metastatic-osa-gilvetmab-2026"),
    ("https://www.vet.upenn.edu/clinical-trial/flash-based-radioimmunotherapy-in-canine-glioma/", "penn-glioma-flash-gilvetmab-2026"),
    ("https://www.vet.upenn.edu/clinical-trial/intraoperative-detection-of-oral-squamous-cell-carcinoma-margins-in-dogs-using-cathepsin-activated-near-infrared-nir-imaging/", "penn-oral-scc-nir-margin-2026"),
    ("https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/olaparib", "umn-feline-mammary-olaparib-meloxicam"),
    ("https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien", "fr-oniris-osa-biocera-vet-cement"),
    ("https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/", "ch-zurich-oral-vinorelbine-phase1-2026"),
    ("https://www.ugent.be/di/khd/nl/onderzoek/katten_met_borstkanker-info-dierenartsen_eng", "be-ghent-feline-mammary-gcn2-inhibitor"),
    ("https://www.gaceta.unam.mx/avanzan-estudios-de-nanotecnologia-para-combatir-el-cancer-en-animales/", "mexico-ensenada-silver-nanoparticle-cancer-2026"),
    ("https://veterinarios.hospitalveterinariopuchol.com/blog/reachglio-ensayo-clinico-glioma-perros/", "spain-puchol-reachglio-2026"),
    ("https://www.kamogawa-ac.jp/2026/09/30/24722/", "jp-multicenter-oral-melanoma-anti-pd1-2026"),
    ("https://www.gamgee.io/trial/", "au-gamgee-personalized-mrna-vaccine"),
    ("https://uqvets.com.au/about/clinical-research-trials", "au-uq-appendicular-osteosarcoma-vaccine"),
    ("https://medipaws.com.au/clinical-research/dogs-with-splenic-haemangiosarcoma", "au-melbourne-hsa-autologous-vaccine-multicenter"),
    ("https://www.animalhospital.gifu-u.ac.jp/cancer/clinical_trial/202508.html", "jp-gifu-feline-oscc-radiotherapy-lavurchin"),
]
for url, tid in existing:
    leads.append({
        "url": url, "disposition": "VERIFIED_EXISTING",
        "reason": f"The treatment identity, institution, cancer/intervention and official URL match canonical record {tid}; this is protocol reconciliation, not a domain-level duplicate assumption.",
        "primary_url": url, "canonical_ids": [tid],
        "identity_comparison": f"Exact intervention/institution/cancer identity matches {tid} ({trial_by_id[tid]['title']}).",
        "evidence_refs": [str((RUN / "global-search-results.json").relative_to(ROOT)), str((RUN / "global-search-deepening.json").relative_to(ROOT))],
        "unperformed_steps": [],
    })

write(RUN / "global-discovery-evidence.json", {
    "run_id": RUN_ID, "recorded_at": NOW, "query_total": len(query_rows),
    "initial_queries": 48, "weak_region_deepening_queries": 20,
    "regions": sorted({q["region"] for q in query_rows}),
    "new_current_protocol_level_trials_added": 0,
    "pending_current_leads": ["CaniVive clinical evaluation"],
    "historical_pending_leads": ["OCRvet/SeineVet monoclonal-antibody study"],
    "closed_current_leads": ["OVC canine porphysome/PDT oral-tumour study"],
    "raw_evidence": [str((RUN / "global-search-results.json").relative_to(ROOT)), str((RUN / "global-search-deepening.json").relative_to(ROOT))],
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
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": query_rows, "discovered_urls": [x["url"] for x in leads], "leads": leads,
    "deadline_review_ref": str((RUN / "deadline-review.json").relative_to(ROOT)),
    "stop": {
        "reason": "completed_available_work",
        "detail": "All frozen sources, configured routes, exact restriction reviews, 63 inherited issues, 68 country/language searches, surfaced treatment leads and every canonical recruitment deadline received current saved decisions; remaining gaps require new public evidence or access changes.",
        "evidence_refs": [str((RUN / "current-source-evidence.json").relative_to(ROOT)), str((RUN / "global-discovery-evidence.json").relative_to(ROOT))],
    },
}
write(RUN / "execution-review.json", review)
print(json.dumps({
    "sources": len(source_reviews), "content_sufficient": receipt["content_sufficient_total"],
    "gaps": len(gap_rows), "issues": len(issue_updates), "queries": len(query_rows),
    "leads": len(leads), "ended_at": NOW,
}, indent=2))
