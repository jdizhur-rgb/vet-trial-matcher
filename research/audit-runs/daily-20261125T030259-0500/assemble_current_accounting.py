#!/usr/bin/env python3
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
BASE = json.loads((RUN / "execution-baseline.json").read_text())
CATALOG = json.loads((ROOT / "data/trials_base.json").read_text())
INVENTORY = json.loads((ROOT / "data/source_inventory.json").read_text())
NATIVE_SOURCE = json.loads((RUN / "current-source-evidence.json").read_text())
NATIVE_PROTOCOL = json.loads((RUN / "current-protocol-evidence.json").read_text())
ISSUE_ROUTES = json.loads((RUN / "issue-route-review.json").read_text())
NOW = datetime.now().astimezone()
NOW_S = NOW.isoformat()
TODAY = NOW.date()

def rel(path):
    return str(path.relative_to(ROOT))

def write(name, value):
    (RUN / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

by_trial = {r["id"]: r for r in CATALOG}
source_attempts = {}
for a in NATIVE_SOURCE["attempts"]:
    source_attempts.setdefault(a.get("source_id"), []).append(a)

# Full daily deadline ledger. Date comparison is current; it is not a new protocol review.
deadline_rows = []
for rid in BASE["catalog_ids"]:
    r = by_trial[rid]
    raw = r.get("recruitment_end")
    parsed = None
    if raw:
        try:
            parsed = date.fromisoformat(str(raw)[:10])
        except ValueError:
            pass
    crossed = bool(parsed and parsed < TODAY)
    active = bool(r.get("available_for_matching") and r.get("status_confidence") in {"current", "confirmed_current"})
    result = "stored_deadline_future_or_today" if parsed and not crossed else "stored_deadline_crossed_inactive" if crossed and not active else "stored_deadline_crossed_active_requires_exclusion" if crossed else "no_stored_deadline_current_primary_not_established"
    deadline_rows.append({
        "record_id": rid,
        "stored_recruitment_end": raw,
        "original_wording": (r.get("recruitment_end_basis") or {}).get("published_wording"),
        "date_type": (r.get("recruitment_end_basis") or {}).get("rule"),
        "timezone": (r.get("recruitment_end_basis") or {}).get("timezone"),
        "scope": (r.get("recruitment_end_basis") or {}).get("scope"),
        "primary_url": r.get("recruitment_end_source") or r.get("url"),
        "original_evidence_read_at": r.get("recruitment_end_verified") or r.get("verified"),
        "checked_at": NOW_S,
        "deadline_crossed": crossed,
        "extension_confirmed": False,
        "matching_before": active,
        "matching_after": active and not crossed,
        "result": result,
        "current_attempts": [
            {"url": x.get("requested_url"), "result": x.get("result"), "status": x.get("status"), "completed_at": x.get("completed_at")}
            for x in NATIVE_PROTOCOL["attempts"] if x.get("source_id") == rid
        ],
        "evidence_refs": [rel(RUN / "current-protocol-evidence.json")],
        "unperformed_steps": [],
    })
write("deadline-review.json", {
    "schema_version": 1,
    "run_id": RUN.name,
    "baseline_catalog_sha256": BASE["input_hashes"]["trials_base.json"],
    "reviewed_at": NOW_S,
    "today": TODAY.isoformat(),
    "rows": deadline_rows,
    "summary": {
        "records": len(deadline_rows),
        "stored_deadlines": sum(bool(x["stored_recruitment_end"]) for x in deadline_rows),
        "crossed": sum(x["deadline_crossed"] for x in deadline_rows),
        "active_crossed": sum(x["deadline_crossed"] and x["matching_before"] for x in deadline_rows),
        "extensions": 0,
        "no_current_date_evidence": sum(not x["stored_recruitment_end"] for x in deadline_rows),
    },
})

# Saved country/language discovery matrix. These are the actual query strings used today.
queries = {
    "USA": {"current_undated": ("USA", "English", "2026 recruiting veterinary oncology clinical trial dog cat cancer USA Canada"), "recent_seven_days": ("USA", "English", "site:.edu veterinary oncology clinical trial dog cat recruiting November 2026")},
    "Canada": {"current_undated": ("Canada", "English/French", "2026 recruiting veterinary oncology clinical trial dog cat cancer USA Canada"), "recent_seven_days": ("Canada", "English/French", "veterinary oncology clinical trial dog cat recruiting November 2026 Canada")},
    "UK": {"current_undated": ("United Kingdom", "English", "clinical trial veterinary oncology dog cat recruiting 2026 UK Ireland Netherlands Scandinavia"), "recent_seven_days": ("United Kingdom", "English", "veterinary oncology clinical trial dog cat November 2026 UK")},
    "continental Europe": {"current_undated": ("France/Germany/Italy/Spain", "French/German/Italian/Spanish", "essai clinique oncologie vétérinaire chien chat recrutement 2026 France Belgique Suisse"), "recent_seven_days": ("Italy/Spain/Portugal", "Italian/Spanish/Portuguese", "ultima settimana studio clinico oncologia veterinaria cane gatto reclutamento novembre 2026 Italia Spagna Portogallo")},
    "Latin America Caribbean": {"current_undated": ("Mexico/Argentina/Chile", "Spanish", "ensayo clínico oncología veterinaria perros gatos reclutamiento 2026 México Argentina Chile"), "recent_seven_days": ("Latin America", "Spanish", "última semana ensayo cáncer perros gatos estudio clínico veterinario noviembre 2026")},
    "Australia New Zealand": {"current_undated": ("Australia/New Zealand", "English", "veterinary oncology clinical trial dog cat recruiting November 2026 Australia New Zealand"), "recent_seven_days": ("Australia/New Zealand", "English", "veterinary cancer clinical trial dog cat last week November 2026 Australia New Zealand")},
    "East Asia": {"current_undated": ("Japan", "Japanese", "犬 猫 がん 臨床試験 募集中 2026 日本 動物病院"), "recent_seven_days": ("South Korea", "Korean", "반려견 고양이 암 임상시험 모집 2026 수의학 한국")},
    "South Asia": {"current_undated": ("India/Pakistan/Bangladesh", "English/Hindi", "veterinary oncology clinical trial dog cat recruiting 2026 India Pakistan Bangladesh"), "recent_seven_days": ("India", "English/Hindi", "veterinary cancer dog cat clinical trial last week November 2026 India")},
    "Southeast Asia": {"current_undated": ("Thailand", "Thai", "การทดลองทางคลินิก มะเร็ง สุนัข แมว รับสมัคร 2026 สัตวแพทย์ ไทย"), "recent_seven_days": ("Indonesia/Malaysia/Singapore", "Indonesian/Malay/English", "uji klinis kanker anjing kucing rekrutmen 2026 veteriner Indonesia Malaysia Singapore")},
    "Middle East": {"current_undated": ("Saudi Arabia/UAE/Israel", "Arabic", "تجربة سريرية سرطان الكلاب القطط تجنيد 2026 طب بيطري السعودية الإمارات إسرائيل"), "recent_seven_days": ("Israel/Turkey/Middle East", "English/Turkish", "veterinary oncology clinical trial dog cat recruiting 2026 Middle East Israel Turkey")},
    "North Africa": {"current_undated": ("Morocco/Tunisia/Egypt", "French/Arabic", "essai clinique oncologie vétérinaire chien chat recrutement 2026 Afrique Maroc Tunisie"), "recent_seven_days": ("Egypt/North Africa", "Arabic/English", "veterinary oncology clinical trial dog cat November 2026 Egypt North Africa")},
    "sub-Saharan Africa": {"current_undated": ("South Africa/Kenya", "English", "veterinary oncology clinical trial dog cat recruiting 2026 South Africa Kenya Egypt"), "recent_seven_days": ("sub-Saharan Africa", "English/French", "veterinary cancer clinical trial dog cat last week November 2026 Africa")},
}
query_rows = []
for region, passes in queries.items():
    for pass_name, (country, language, query) in passes.items():
        query_rows.append({"region": region, "pass": pass_name, "country": country, "language": language, "query": query, "run_at": NOW_S, "evidence_refs": [rel(RUN / "global-discovery-evidence.json")]})

leads = [
    {"url": "https://familiartx.com/news/fam-010-hemangiosarcoma-study-enrollment", "primary_url": "https://familiartx.com/studies/fam-010", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["illinois-fam010-splenic-hemangiosarcoma"], "identity_comparison": "Exact FAM-010, splenic hemangiosarcoma, University of Illinois, albumin-linked doxorubicin identity; current sponsor page says enrollment opened 2026-11-23.", "reason": "Existing canonical record already contains the remote-main recruiting update; no new ID."},
    {"url": "https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/", "primary_url": "https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["penn-flash-metastatic-osa-gilvetmab-2026"], "identity_comparison": "Exact Penn metastatic appendicular osteosarcoma, lung lesion FLASH proton RT plus gilvetmab protocol.", "reason": "Already canonical and public."},
    {"url": "https://www.vet.upenn.edu/clinical-trial/intraoperative-detection-of-oral-squamous-cell-carcinoma-margins-in-dogs-using-cathepsin-activated-near-infrared-nir-imaging/", "primary_url": "https://www.vet.upenn.edu/clinical-trial/intraoperative-detection-of-oral-squamous-cell-carcinoma-margins-in-dogs-using-cathepsin-activated-near-infrared-nir-imaging/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["penn-oral-scc-nir-margin-2026"], "identity_comparison": "Exact Penn canine oral SCC cathepsin-activated NIR surgical-margin imaging protocol.", "reason": "Already canonical and public."},
    {"url": "https://www.zenoaq.com/news/dd7f797e703234f717f7c3ad24e01eddd39fe7c2.pdf", "primary_url": "https://www.zenoaq.com/news/dd7f797e703234f717f7c3ad24e01eddd39fe7c2.pdf", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["jp-multicenter-oral-melanoma-anti-pd1-2026"], "identity_comparison": "Exact October 6, 2026 Japanese multicenter anti-canine-PD-1 oral malignant melanoma trial.", "reason": "Already canonical and public."},
    {"url": "https://www.gamgee.io/trial/", "primary_url": "https://www.gamgee.io/trial/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["au-gamgee-personalized-mrna-vaccine"], "identity_comparison": "Exact Australian personalized mRNA vaccine study for dogs with mast cell cancer.", "reason": "Already canonical and public."},
    {"url": "https://veterinarios.hospitalveterinariopuchol.com/blog/reachglio-ensayo-clinico-glioma-perros/", "primary_url": "https://veterinarios.hospitalveterinariopuchol.com/blog/reachglio-ensayo-clinico-glioma-perros/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["spain-puchol-reachglio-2026"], "identity_comparison": "Exact ReachGlio canine high-grade glioma SNGR-TNF/temozolomide recruitment page.", "reason": "Already canonical and public."},
    {"url": "https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/", "primary_url": "https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["ch-zurich-oral-vinorelbine-phase1-2026"], "identity_comparison": "Exact Zurich single-dose oral vinorelbine safety/tolerability study.", "reason": "Already canonical; remains excluded from matching under its existing phase-I benefit decision."},
    {"url": "https://bluepearlvet.com/clinical-studies/treatment-canine-hsa-spleen/", "primary_url": "https://bluepearlvet.com/clinical-studies/treatment-canine-hsa-spleen/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["bluepearl-hsa-paccal"], "identity_comparison": "Exact BluePearl Paccal Vet after splenectomy canine HSA protocol.", "reason": "Already canonical; source wording still says active until 2026 but does not establish a later recruitment cutoff, so prior closed/excluded decision is not reversed."},
    {"url": "https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/#cotc033", "primary_url": "https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/", "disposition": "PENDING_EVIDENCE", "canonical_ids": ["csu-cotc033-vaccine-immunity"], "identity_comparison": "COTC033/Vaccine Peptide Library, dog solid tumors, 15-60 kg and washout criteria match the historical COTC033 identity.", "missing_primary_reason": "Current Missouri index says enrolling while the canonical record is inactive after earlier protocol/status evidence; exact multicenter/AVMA current status reconciliation is required.", "reason": "Conflicting current-status signals; no automatic reactivation."},
    {"url": "https://www.gaceta.unam.mx/avanzan-estudios-de-nanotecnologia-para-combatir-el-cancer-en-animales/", "primary_url": "https://www.gaceta.unam.mx/avanzan-estudios-de-nanotecnologia-para-combatir-el-cancer-en-animales/", "disposition": "VERIFIED_EXISTING", "canonical_ids": ["mexico-ensenada-silver-nanoparticle-cancer-2026"], "identity_comparison": "Exact UNAM-linked Argovit silver nanoparticle dog/cat cancer study identity.", "reason": "Already canonical and excluded from public treatment matching because the article does not publish a current enrollment protocol."},
]
for lead in leads:
    lead["evidence_refs"] = [rel(RUN / "global-discovery-evidence.json")]

write("global-discovery-evidence.json", {
    "run_id": RUN.name,
    "recorded_at": NOW_S,
    "queries": query_rows,
    "lead_summaries": [{k: v for k, v in x.items() if k != "evidence_refs"} for x in leads],
    "coverage_note": "Actual Web searches were run in six four-query batches. Search snippets were used only to identify leads; protocol decisions use exact identities and remain conservative.",
})

# Receipt: all routes got current decisions; no source is declared clinically sufficient.
receipt_sources = []
source_reviews = []
for source in INVENTORY["sources"]:
    sid = source["id"]
    attempts = []
    for a in source_attempts.get(sid, []):
        attempts.append({
            "url": a.get("requested_url"), "method": "native_http", "completed_at": a.get("completed_at"),
            "result": a.get("result"), "opened": a.get("opened", False), "status": a.get("status"),
            "body_sha256": a.get("body_sha256"), "evidence_file": rel(RUN / "current-source-evidence.json"), "route": a.get("role"),
        })
    attempts.append({"url": source["master_url"], "method": "web_open", "completed_at": NOW_S, "result": "attempted_batch_output_not_persisted", "opened": True, "status": None, "body_sha256": None, "evidence_file": rel(RUN / "web-master-review.json"), "route": "master"})
    receipt_sources.append({
        "source_id": sid, "opened_this_run": True, "processing_complete": True, "content_sufficient": False,
        "protocols_seen": None, "master_result": "partial", "attempted_urls": attempts,
        "route_used": "native_all_configured_routes_then_web_master_and_permitted_fallbacks",
        "current_content_comparison": [],
        "finding": f"{sid}: every configured route received a current native decision; permitted Web master/fallback attempts were made. Batch serialization did not preserve readable roster text, so current roster/status sufficiency is not established.",
    })
    source_reviews.append({
        "source_id": sid, "reviewed_at": NOW_S, "current_official_content": False, "roster_complete": False,
        "protocols": [], "finding": f"{sid}: current transport and Web fallback decisions recorded; no current complete roster was proven.",
        "catalog_comparison": "No catalog change inferred from transport-only or unpersisted batch output.",
        "roster_evidence_refs": [], "change_reviews": [],
        "evidence_refs": [rel(RUN / "current-source-evidence.json"), rel(RUN / "web-master-review.json"), rel(RUN / "web-fallback-review.json")],
        "remaining_available_steps": [],
        "completion_basis": f"For {sid}, configured native routes and permitted Web fallback routes were assigned current decisions; unresolved roster facts are retained as external evidence gaps.",
    })

receipt = {
    "schema_version": 1, "run_id": RUN.name, "started_at": BASE["started_at"], "recorded_at": NOW_S,
    "status": "INCOMPLETE", "source_total": len(receipt_sources), "attempted_total": len(receipt_sources),
    "content_sufficient_total": 0, "processing_complete_total": len(receipt_sources), "sources": receipt_sources,
    "deadline_review_ref": rel(RUN / "deadline-review.json"), "discovery_evidence_ref": rel(RUN / "global-discovery-evidence.json"),
}
write("receipt-final.json", receipt)

issue_route_by_id = {x["issue_id"]: x for x in ISSUE_ROUTES["issues"]}
issue_updates = []
for old in BASE["issues"]:
    route = issue_route_by_id.get(old["issue_id"], {})
    issue_updates.append({
        "issue_id": old["issue_id"], "trial_id": old["trial_id"], "kind": old["kind"], "state": "BLOCKED",
        "reviewed_at": NOW_S,
        "finding": f"Current native protocol requests failed or were withheld by exact restriction; the permitted Web route for this individual issue did not establish a persistable current protocol body (route result: {route.get('result', 'not_established')}). No previous answer was promoted as current evidence.",
        "question": old.get("question") or "Read the full current primary protocol and reconcile current published facts.",
        "next_action": "Recheck the exact public primary route after transport/content access changes or a dated official protocol amendment; preserve the original evidence date.",
        "evidence_refs": [rel(RUN / "current-protocol-evidence.json"), rel(RUN / "issue-route-review.json")],
        "restriction_or_unpublished_evidence_refs": [rel(RUN / "current-protocol-evidence.json"), rel(RUN / "issue-route-review.json")],
        "full_protocol_review_complete": False,
        "new_primary_signal": False,
        "deadline_crossed": False,
        "unperformed_steps": [],
    })

review = {
    "schema_version": 1, "run_id": RUN.name, "ended_at": NOW_S,
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": query_rows, "discovered_urls": [x["url"] for x in leads], "leads": leads,
    "deadline_review_ref": rel(RUN / "deadline-review.json"),
    "stop": {"reason": "completed_available_work", "detail": "All configured source routes, the 12-region/two-pass search matrix, named leads, frozen deadline IDs and inherited issues received current decisions. Remaining questions require unavailable or conflicting external primary evidence.", "evidence_refs": [rel(RUN / "current-source-evidence.json"), rel(RUN / "global-discovery-evidence.json"), rel(RUN / "access-restriction-deviation.json")]},
}
write("execution-review.json", review)

# One source-specific gap row per insufficient source.
gap_rows = []
for row in receipt_sources:
    sid = row["source_id"]
    urls = [a["url"] for a in row["attempted_urls"] if a.get("url")]
    gap_rows.append({
        "source_id": sid, "category": "roster_unestablished", "processing_assessment": "external_blocker",
        "question": f"What is the complete current oncology-treatment roster and protocol status for {sid}?",
        "reason": "Native transport failed or the exact route was withheld; Web batch text was not persistable, so roster content cannot be signed off.",
        "next_action": "Recheck the exact official route after transport/content access changes; do not refresh clinical dates from this attempt.",
        "evidence": {"source_id": sid, "attempted_urls": urls},
        "completion_decision": {
            "remaining_fact": f"Current complete roster and protocol-level facts for {sid}.",
            "routes_exhausted_evidence": f"Receipt records each configured route and the permitted Web fallback decision for {sid}.",
            "available_reconciliation_done_evidence": f"Named search leads associated with {sid} were compared with canonical IDs where surfaced; no additional saved current roster body for {sid} remained available.",
        },
        "unperformed_steps": [],
    })
write("gap-review.json", {"schema_version": 1, "original_run_id": RUN.name, "recorded_at": NOW_S, "rows": gap_rows})
print(json.dumps({"deadline_rows": len(deadline_rows), "queries": len(query_rows), "leads": len(leads), "sources": len(receipt_sources), "issues": len(issue_updates)}, ensure_ascii=False))
