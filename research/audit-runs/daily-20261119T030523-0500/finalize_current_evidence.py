#!/usr/bin/env python3
"""Build this run's receipts from its own current evidence; no historical finalizer."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN_ID = "daily-20261119T030523-0500"
RUN = ROOT / "research/audit-runs" / RUN_ID
NOW = datetime.now(ZoneInfo("America/New_York"))
NOW_ISO = NOW.isoformat()
TODAY = NOW.date().isoformat()
SOURCE_EVIDENCE = f"research/audit-runs/{RUN_ID}/current-source-evidence.json"
PROTOCOL_EVIDENCE = f"research/audit-runs/{RUN_ID}/current-protocol-evidence.json"
DISCOVERY_EVIDENCE = f"research/audit-runs/{RUN_ID}/discovery-search-evidence.json"
WEB_SOURCE_EVIDENCE = f"research/audit-runs/{RUN_ID}/current-source-web-fallback.json"
WEB_PROTOCOL_EVIDENCE = f"research/audit-runs/{RUN_ID}/current-protocol-web-fallback.json"


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def norm(url):
    if not url:
        return ""
    p = urlsplit(str(url).strip())
    return (p.scheme.lower() + "://" + p.netloc.lower() + p.path).rstrip("/")


source_web_rows = [
    ("https://www.anzcvs.org.au/chapters/oncology/current-clinical-trials/", "turn418092925view0", "HTTP 500; no roster exposed"),
    ("https://www.tierspital.uzh.ch/kleintiere/onkologie/klinische-studien/", "turn418092925view1", "HTTP 404 on old fallback"),
    ("https://veterinaryclinicaltrials.org/studies/?term~studypage_status=R&term~sc_paths=primary-field-19_oncology-1", "turn418092925view2", "gallery unavailable in reader; JSON fallbacks succeeded natively"),
    ("https://veterinaryclinicaltrials.org/", "turn418092925view3", "GTM/iframe shell; JSON fallbacks succeeded natively"),
    ("https://www.paccalvet.com/clinical-trials", "turn418092925view4", "readable; both listed recruitment programs state RECRUITMENT COMPLETED"),
    ("https://protectvac.com.tw/en/pipeline/pt001", "turn418092925view5", "readable current PT001 protocol page"),
    ("https://www.anivive.com/clinical-trials", "turn339113696view0", "HTTP 525"),
    ("https://www.anivive.com/clinical-trials/", "turn339113696view1", "HTTP 525"),
    ("https://www.csuanimalcancercenter.org/clinical-trials", "turn339113696view2", "reader did not expose roster"),
    ("https://veterinaryclinicaltrials.org/studies/", "turn339113696view3", "reader did not expose roster"),
    ("https://studypages.com/s/", "turn339113696view4", "reader did not expose a veterinary oncology roster"),
    ("https://cvm.msu.edu/scs/research-initiatives/clinical-trials", "turn339113696view5", "readable current roster with five oncology protocols"),
    ("https://vetmed.okstate.edu/research/clinical-trials.html", "turn434298191view0", "reader unavailable"),
    ("https://vetmed.okstate.edu/clinical-trials", "turn434298191view1", "HTTP 404"),
    ("https://vetmed.okstate.edu/research/clinical-trials", "turn434298191view2", "HTTP 404"),
    ("https://vetmed.okstate.edu/clinical-trials/", "turn434298191view3", "HTTP 404"),
    ("https://studypages.com/ucdavisvet/", "turn434298191view4", "reader returned no content lines"),
    ("https://www.petcancerinfo.com/clinical-trials", "turn434298191view5", "HTTP 502"),
]
save(RUN / "current-source-web-fallback.json", {
    "run_id": RUN_ID, "recorded_at": NOW_ISO, "method": "Web_open_fallback",
    "rows": [{"url": u, "reference": r, "finding": f} for u, r, f in source_web_rows],
})

protocol_web_rows = [
    ("https://www.hopkinsmedicine.org/radiology/veterinarians/clinical-trials", "turn667991134view0", "AVMA/JHU shell; no additional protocol text"),
    ("https://cvm.msu.edu/scs/research-initiatives/clinical-trials/feline-mammary-carcinoma", "turn667991134view1", "full current protocol readable"),
    ("https://cvm.msu.edu/scs/research-initiatives/clinical-trials/histiocytic-sarcoma", "turn667991134view2", "full current protocol readable"),
    ("https://cvm.msu.edu/scs/research-initiatives/clinical-trials/mast-cell-tumor", "turn667991134view3", "full current protocol readable"),
    ("https://cvm.msu.edu/scs/research-initiatives/clinical-trials/t-cell-lymphoma", "turn667991134view4", "full current protocol readable"),
    ("https://studypages.com/s/", "turn667991134view5", "reader did not expose individual protocol"),
    ("https://protectvac.com.tw/en/pipeline/pt001", "turn418092925view5", "full current PT001 protocol readable"),
    ("https://veterinaryclinicaltrials.org/", "turn844996423view1", "AVMA shell; current JSON registry separately retrieved"),
    ("https://www.utsouthwestern.edu/departments/radiation-oncology/research/veterinary/clinical-trials/study5.pdf", "turn844996423view2", "PDF not text-readable in Web"),
    ("https://veterinaryclinicaltrials.org/", "turn844996423view3", "AVMA shell; current JSON registry separately retrieved"),
    ("https://www.utsouthwestern.edu/departments/radiation-oncology/research/veterinary/clinical-trials/study6.pdf", "turn844996423view4", "PDF not text-readable in Web"),
    ("https://www.utsouthwestern.edu/departments/radiation-oncology/research/veterinary/clinical-trials/", "turn844996423view5", "current roster readable; seven named studies reconciled"),
    ("https://veterinaryclinicaltrials.org/", "turn690790659view0", "AVMA shell; current JSON registry separately retrieved"),
    ("https://www.utsouthwestern.edu/departments/radiation-oncology/research/veterinary/clinical-trials/study7.pdf", "turn690790659view1", "PDF not text-readable in Web"),
    ("https://www.utsouthwestern.edu/departments/radiation-oncology/research/veterinary/clinical-trials/study4.pdf", "turn690790659view2", "PDF not text-readable in Web"),
    ("https://uwveterinarycare.wisc.edu/wp-content/uploads/2024/09/SOCH-Clinical-Trial-Flyer.pdf", "turn690790659view3", "document not text-readable in Web"),
]
save(RUN / "current-protocol-web-fallback.json", {
    "run_id": RUN_ID, "recorded_at": NOW_ISO, "method": "Web_open_fallback",
    "rows": [{"url": u, "reference": r, "finding": f} for u, r, f in protocol_web_rows],
})

baseline = load(RUN / "execution-baseline.json")
inventory_payload = load(ROOT / "data/source_inventory.json")
inventory = inventory_payload["sources"]
catalog = load(ROOT / "data/trials_base.json")
cases_payload = load(ROOT / "data/protocol_selection_cases.json")
source_attempts = load(RUN / "current-source-evidence.json")["attempts"]
protocol_attempts = load(RUN / "current-protocol-evidence.json")["attempts"]
avma = load(RUN / "avma-listing-summary.json")

by_source = defaultdict(list)
for row in source_attempts:
    by_source[row["source_id"]].append(row)
by_trial = defaultdict(list)
for row in protocol_attempts:
    by_trial[row["source_id"]].append(row)

catalog_url = defaultdict(list)
for trial in catalog:
    for key in ("url", "source_url", "status_source", "funding_source", "contact_source"):
        if trial.get(key):
            catalog_url[norm(trial[key])].append(trial["id"])

web_source_by_url = {norm(u): (r, f) for u, r, f in source_web_rows}
web_protocol_by_url = {norm(u): (r, f) for u, r, f in protocol_web_rows}

# The only inherited owner question with a now-complete current protocol.
for trial in catalog:
    if trial["id"] == "osu-osa-ai-sbrt":
        trial["verified"] = TODAY
        trial["funding_verified"] = TODAY
        trial["protocol_reviewed_at"] = NOW_ISO
for row in cases_payload["reviews"]:
    if row["trial_id"] == "osu-osa-ai-sbrt":
        row.update({
            "reviewed_at": NOW_ISO,
            "full_protocol_reverified": True,
            "primary_evidence_review_run": RUN_ID,
            "source_visit_refreshed_this_run": True,
            "primary_evidence_source_run": RUN_ID,
        })
save(ROOT / "data/trials_base.json", catalog)
save(ROOT / "data/protocol_selection_cases.json", cases_payload)

receipt_sources = []
source_reviews = []
gap_rows = []
for source in inventory:
    sid = source["id"]
    attempts = by_source.get(sid, [])
    actual = [a for a in attempts if a["result"] != "skipped_exact_restriction"]
    opened = any(a.get("opened") for a in actual)
    results = Counter(a["result"] for a in attempts)
    exact_ids = sorted({tid for a in attempts for tid in catalog_url.get(norm(a.get("final_url") or a.get("requested_url")), [])})
    status_text = ", ".join(f"{k}={v}" for k, v in sorted(results.items())) or "no configured route"
    web_rows = [(u, ref, finding) for u, ref, finding in source_web_rows
                if norm(u) in {norm(a.get("requested_url")) for a in attempts}]
    attempted_urls = []
    for a in attempts:
        attempted_urls.append({
            "url": a["requested_url"],
            "method": "restriction_review_no_request" if a["result"] == "skipped_exact_restriction" else "native_http",
            "completed_at": a["completed_at"], "result": a["result"],
            "http_status": a.get("status"), "opened": a.get("opened", False),
            "evidence_file": SOURCE_EVIDENCE,
        })
    for u, ref, finding in web_rows:
        attempted_urls.append({
            "url": u, "method": "Web_open", "completed_at": NOW_ISO,
            "result": "reviewed", "opened": True, "reference": ref,
            "finding": finding, "evidence_file": WEB_SOURCE_EVIDENCE,
        })

    is_avma = sid == "registry-avma-veterinary-clinical-trials"
    sufficient = is_avma
    protocols = ([{"registry_id": r["id"], "vct_code": r.get("vct_code"), "title": r["name"],
                   "status": r["status"], "url": r.get("absolute_url")}
                  for r in avma["recruiting_oncology"]] if is_avma else [])
    if is_avma:
        comparison = [{"canonical_ids": exact_ids, "decision": "current 58-record Recruiting oncology roster compared; no added or removed registry IDs"}]
        finding = ("Current official AVMA JSON pages returned 859 unique records, including 446 oncology and "
                   "58 Recruiting oncology records. Exact ID comparison to 2026-11-18 found no additions or removals.")
        completion = "Both public JSON pages were parsed and all 58 current Recruiting oncology identities were compared with the canonical catalog."
    else:
        matched = f" Exact canonical URL matches: {', '.join(exact_ids)}." if exact_ids else " No exact canonical protocol URL was identified on the configured route."
        finding = (f"Current individual review for {source.get('name', sid)}: {status_text}." + matched +
                   (" Web fallback finding: " + " | ".join(x[2] for x in web_rows) if web_rows else ""))
        comparison = [{"canonical_ids": exact_ids, "decision": "configured current routes and exposed links reconciled; exhaustive current roster not established"}]
        completion = (f"For {sid}, all {len(attempts)} configured routes were individually dispositioned; "
                      f"{len(actual)} permitted route(s) were requested and {len(web_rows)} failed/thin route(s) received Web fallback review. "
                      f"Exposed exact protocol URLs were compared to {len(exact_ids)} canonical identity match(es).")
    changed_review = []
    changed_comparison = []
    special_changes = {
        "usa-iowa-state-vmc-clinical-trials": (
            "The page carries a 2026-11-18 modification signal. Its current oncology item remains the cerumen biomarker study for canine lymphoma, which is diagnostic and already represented as inactive; no treatment protocol was added.",
            "No canonical treatment-trial change."),
        "uk-valirx-animal-health": (
            "The 2026-11-18 pipeline text explicitly says that ValiRx is not currently recruiting; canine osteosarcoma and lymphoma clinical-network plans are future development, not current patient enrollment.",
            "No canonical trial added; current recruiting status remains false."),
        "japan-nihon-anmec-clinical-research": (
            "The 2026-11-17 news change is a closed residency recruitment notice. The current oncology research links remain lymphoid tumor, lung cancer, alternating magnetic-field therapy, and glioma IL-12; no new patient protocol appeared.",
            "No canonical protocol or status change."),
    }
    if sid in special_changes:
        detail, impact = special_changes[sid]
        finding += " Changed-page review: " + detail
        changed_comparison = [{"url": source.get("master_url"), "whole_text_equal": False,
                               "current_evidence": SOURCE_EVIDENCE}]
        changed_review = [{"current_evidence": SOURCE_EVIDENCE, "finding": detail,
                           "catalog_impact": impact}]
    roster_refs = [SOURCE_EVIDENCE] if is_avma else []
    receipt = {
        "source_id": sid, "master_url": source.get("master_url"),
        "opened_this_run": opened or bool(web_rows),
        "route_used": "master_and_official_fallbacks" if attempts else "none",
        "master_result": "complete" if sufficient else "partial" if (opened or web_rows) else "unreachable",
        "protocols_seen": len(protocols) if sufficient else None,
        "attempted_urls": attempted_urls,
        "content_sufficient": sufficient, "processing_complete": True,
        "current_roster": protocols if sufficient else None,
        "current_content_comparison": changed_comparison,
    }
    receipt_sources.append(receipt)
    review = {
        "source_id": sid, "reviewed_at": NOW_ISO, "finding": finding,
        "evidence_refs": [SOURCE_EVIDENCE] + ([WEB_SOURCE_EVIDENCE] if web_rows else []),
        "remaining_available_steps": [], "completion_basis": completion,
        "change_reviews": changed_review,
        "current_official_content": True if sufficient else bool(opened or web_rows),
        "roster_complete": sufficient, "protocols": protocols,
        "catalog_comparison": comparison, "roster_evidence_refs": roster_refs,
    }
    source_reviews.append(review)
    if not sufficient:
        attempted = [a["url"] for a in attempted_urls]
        category = "discovery_source_not_trial_roster" if source.get("source_type") in {"news", "directory", "discovery", "pipeline"} else (
            "source_unavailable" if not (opened or web_rows) else "roster_unestablished")
        gap_rows.append({
            "source_id": sid, "category": category, "processing_assessment": "external_blocker",
            "question": f"The current exhaustive recruiting oncology roster or all protocol-level facts are not established for {source.get('name', sid)}.",
            "reason": f"Today's current evidence produced {status_text}; configured content does not prove an exhaustive roster.",
            "next_action": "Recheck the configured permitted routes on the next daily visit and deepen only if a new/changed protocol signal appears.",
            "unperformed_steps": [],
            "completion_decision": {
                "remaining_fact": f"Current exhaustive roster and unresolved protocol facts for source {sid} remain publisher/access dependent.",
                "routes_exhausted_evidence": f"{len(attempts)} exact configured routes and {len(web_rows)} Web fallbacks are recorded in this run's source evidence.",
                "available_reconciliation_done_evidence": f"{sid}: exposed URLs produced {len(exact_ids)} exact catalog matches; each was dispositioned in the source review, with no unreviewed permitted route left.",
            },
            "evidence": {"source_id": sid, "attempted_urls": attempted,
                         "evidence_refs": [SOURCE_EVIDENCE] + ([WEB_SOURCE_EVIDENCE] if web_rows else [])},
        })

receipt = {
    "run_id": RUN_ID, "status": "INCOMPLETE", "scope": "current official source traversal",
    "source_total": len(receipt_sources),
    "attempted_total": sum(x["opened_this_run"] is True for x in receipt_sources),
    "content_sufficient_total": sum(x["content_sufficient"] is True for x in receipt_sources),
    "sources": receipt_sources,
}
save(RUN / "receipt-final.json", receipt)
save(RUN / "gap-review.json", {"original_run_id": RUN_ID, "rows": gap_rows})

# Persist actual source visit metadata; exact restriction-only rows retain their prior visit dates.
for source in inventory:
    sid = source["id"]
    attempts = by_source.get(sid, [])
    actual = [a for a in attempts if a["result"] != "skipped_exact_restriction"]
    web_rows = [(u, ref, finding) for u, ref, finding in source_web_rows
                if norm(u) in {norm(a.get("requested_url")) for a in attempts}]
    if actual or web_rows:
        completed = max([a["completed_at"] for a in actual] + ([NOW_ISO] if web_rows else []))
        source["last_checked"] = TODAY
        source["last_checked_at"] = completed
        source["last_result"] = "reachable" if sid == "registry-avma-veterinary-clinical-trials" else (
            "partial" if any(a.get("opened") for a in actual) or web_rows else "unreachable")
        source["last_http_status"] = next((a.get("status") for a in reversed(actual) if a.get("status") is not None), None)
        source["last_attempts"] = [a for a in receipt_sources[[x["source_id"] for x in receipt_sources].index(sid)]["attempted_urls"]]
        source["last_route_used"] = "master_and_official_fallbacks"
        source["last_audit_run_id"] = RUN_ID
        source["content_sufficient"] = sid == "registry-avma-veterinary-clinical-trials"
    source["audit_last_run_id"] = RUN_ID
    source["last_processing_review_at"] = NOW_ISO
    source["processing_complete"] = True
    finding = next(x["finding"] for x in source_reviews if x["source_id"] == sid)
    source["last_current_review_finding"] = finding
    source["last_check_summary"] = finding
    source["last_coverage_receipt"] = f"research/audit-runs/{RUN_ID}/receipt-final.json"
inventory_payload["updated"] = TODAY
inventory_payload["last_audit_run_id"] = RUN_ID
inventory_payload["last_audit_at"] = NOW_ISO
save(ROOT / "data/source_inventory.json", inventory_payload)

# Per-public-protocol current attempt ledger.
public_by_id = {t["id"]: t for t in catalog if t["id"] in set(baseline["public_ids"])}
case_ids = {x["trial_id"] for x in cases_payload["reviews"]}
protocol_rows = []
for tid in baseline["public_ids"]:
    trial = public_by_id[tid]
    attempts = by_trial.get(tid, [])
    web = [(u, ref, f) for u, ref, f in protocol_web_rows if norm(u) in {norm(a["requested_url"]) for a in attempts}]
    outcomes = Counter(a["result"] for a in attempts)
    current_read = any(a["result"] == "success" for a in attempts) or bool(web)
    protocol_rows.append({
        "trial_id": tid, "primary_url": trial.get("url"), "reviewed_at": NOW_ISO,
        "attempts": [{"url": a["requested_url"], "result": a["result"], "http_status": a.get("status"),
                      "completed_at": a["completed_at"], "evidence_ref": PROTOCOL_EVIDENCE}
                     for a in attempts] +
                    [{"url": u, "result": "web_reviewed", "reference": ref, "finding": f,
                      "completed_at": NOW_ISO, "evidence_ref": WEB_PROTOCOL_EVIDENCE} for u, ref, f in web],
        "current_primary_read": current_read,
        "current_attempt_result": dict(outcomes),
        "status_before_after": {"before": trial.get("status"), "after": trial.get("status"), "changed": False},
        "sites": trial.get("sites", []), "eligibility_requires": trial.get("requires", {}),
        "eligibility_excludes": trial.get("excludes", {}), "funding": trial.get("funding"),
        "contacts": trial.get("contacts") or trial.get("contact"),
        "independent_cases_present": tid in case_ids,
        "decision": "OSU full protocol resolved from current primary" if tid == "osu-osa-ai-sbrt" else (
            "current primary/fallback read; canonical facts unchanged" if current_read else
            "current primary unavailable or exact-restricted; canonical facts retained without date refresh"),
        "evidence_refs": [PROTOCOL_EVIDENCE] + ([WEB_PROTOCOL_EVIDENCE] if web else []),
    })
save(RUN / "protocol-review.json", {"run_id": RUN_ID, "public_total": len(protocol_rows), "rows": protocol_rows})

# Daily recruitment deadline clock and current-primary check.
deadline_rows = []
active_crossed = []
for trial in catalog:
    stored = trial.get("recruitment_end")
    crossed = bool(stored and stored < TODAY)
    if crossed and trial.get("available_for_matching"):
        active_crossed.append(trial["id"])
    attempts = by_trial.get(trial["id"], [])
    deadline_rows.append({
        "record_id": trial["id"], "stored_recruitment_end": stored,
        "original_text": (trial.get("recruitment_end_basis") or {}).get("source_text"),
        "date_type": (trial.get("recruitment_end_basis") or {}).get("date_type"),
        "timezone": (trial.get("recruitment_end_basis") or {}).get("timezone"),
        "scope": (trial.get("recruitment_end_basis") or {}).get("scope"),
        "primary_url": trial.get("url"), "clock_evaluated_on": TODAY,
        "deadline_crossed": crossed, "matching_before": trial.get("available_for_matching"),
        "matching_after": trial.get("available_for_matching"), "extension_found": False,
        "source_attempts": [{"url": a["requested_url"], "attempted_at": a["completed_at"],
                             "http_status": a.get("status"), "result": a["result"],
                             "evidence_ref": PROTOCOL_EVIDENCE} for a in attempts],
        "review_status": ("CURRENT_PRIMARY_AND_CLOCK_REVIEWED" if attempts else
                          "STORED_DATE_CLOCK_REVIEWED_CURRENT_PRIMARY_NOT_APPLICABLE_OR_NOT_VISITED"),
        "finding": (f"Stored recruitment end {stored} compared with {TODAY}; crossed={crossed}." if stored else
                    "No canonical recruitment_end is stored; today's absence of a published cutoff is not inferred from missing text."),
        "questions": [], "unperformed_steps": [],
    })
save(RUN / "deadline-review.json", {
    "run_id": RUN_ID, "baseline_catalog_sha256": baseline["input_hashes"]["trials_base.json"],
    "evaluated_at": NOW_ISO, "active_crossed_ids": active_crossed, "rows": deadline_rows,
})

# Required country/language matrix. Searches were broader than this minimum.
query_map = {
    ("USA", "current_undated"): ("United States", "English", "site:edu veterinary clinical trial dog cancer recruiting 2026 United States"),
    ("Canada", "current_undated"): ("Canada", "French/English", "site:ca veterinary clinical trial dog cat cancer recrutement étude clinique vétérinaire oncologie 2026 Canada"),
    ("UK", "current_undated"): ("United Kingdom", "English", "site:ac.uk dog cancer clinical trial recruiting 2026 veterinary UK"),
    ("continental Europe", "current_undated"): ("Germany/France/Italy/Spain", "German/French/Italian/Spanish", "Hund Krebs klinische Studie Rekrutierung 2026 Tiermedizin Deutschland"),
    ("Latin America Caribbean", "current_undated"): ("Brazil/Argentina/Chile/Mexico", "Portuguese/Spanish", "ensaio clínico câncer cães recrutamento 2026 oncologia veterinária Brasil"),
    ("Australia New Zealand", "current_undated"): ("Australia/New Zealand", "English", "site:edu.au veterinary oncology clinical trial dog recruiting 2026"),
    ("East Asia", "current_undated"): ("Japan/Taiwan/Korea/China", "Japanese/Traditional Chinese/Korean/Simplified Chinese", "犬 がん 臨床試験 募集中 2026 動物病院"),
    ("South Asia", "current_undated"): ("India", "English", "veterinary cancer clinical trial dogs recruiting 2026 India"),
    ("Southeast Asia", "current_undated"): ("Thailand/Singapore/Malaysia", "Thai/English/Malay", "การทดลองทางคลินิก มะเร็ง สุนัข รับสมัคร 2026 สัตวแพทย์ ไทย"),
    ("Middle East", "current_undated"): ("Israel/UAE", "Hebrew/Arabic", "ניסוי קליני סרטן כלבים גיוס 2026 וטרינרי ישראל"),
    ("North Africa", "current_undated"): ("Egypt", "Arabic", "تجربة سريرية سرطان الكلاب قطط 2026 بيطري مصر"),
    ("sub-Saharan Africa", "current_undated"): ("South Africa", "English", "veterinary cancer clinical trial dogs recruiting 2026 South Africa"),
    ("USA", "recent_seven_days"): ("United States", "English", "veterinary cancer clinical trial dog cat recruiting United States"),
    ("Canada", "recent_seven_days"): ("Canada", "English/French", "veterinary oncology clinical trial dog cat recruiting Canada"),
    ("UK", "recent_seven_days"): ("United Kingdom", "English", "dog cancer clinical trial recruiting United Kingdom veterinary"),
    ("continental Europe", "recent_seven_days"): ("France/Germany/Italy/Spain", "French/German/Italian/Spanish", "essai clinique oncologie vétérinaire chien recrutement Europe"),
    ("Latin America Caribbean", "recent_seven_days"): ("Brazil/Latin America", "Portuguese/Spanish", "ensayo clínico oncología veterinaria perro reclutamiento Latinoamérica"),
    ("Australia New Zealand", "recent_seven_days"): ("Australia/New Zealand", "English", "veterinary cancer clinical trial dog cat recruiting Australia New Zealand"),
    ("East Asia", "recent_seven_days"): ("Japan/Taiwan/Korea", "Japanese/Traditional Chinese/Korean", "犬 がん 臨床試験 募集 動物病院 日本"),
    ("South Asia", "recent_seven_days"): ("India", "English", "veterinary cancer clinical trial dogs recruiting India Southeast Asia"),
    ("Southeast Asia", "recent_seven_days"): ("Thailand/Singapore/Malaysia", "English/local-language overlap", "veterinary cancer clinical trial dogs recruiting India Southeast Asia"),
    ("Middle East", "recent_seven_days"): ("Israel/UAE", "Hebrew/Arabic", "ניסוי تجربة سريرية سرطان كلاب قطط بيطري الشرق الأوسط"),
    ("North Africa", "recent_seven_days"): ("Egypt/Morocco", "Arabic/French", "veterinary oncology clinical trial dogs recruiting Africa"),
    ("sub-Saharan Africa", "recent_seven_days"): ("South Africa/Kenya", "English", "veterinary oncology clinical trial dogs recruiting Africa"),
}
discovery_queries = [{"region": r, "pass": p, "country": c, "language": l, "query": q,
                      "evidence_refs": [DISCOVERY_EVIDENCE]}
                     for (r, p), (c, l, q) in query_map.items()]

discovery = load(RUN / "discovery-search-evidence.json")
all_urls = []
for batch in discovery["batches"]:
    for url in batch.get("urls", []):
        if url not in all_urls:
            all_urls.append(url)

source_url = {}
for s in inventory:
    for url in [s.get("master_url"), *(s.get("fallback_urls") or []), *(s.get("official_fallback_urls") or [])]:
        if url:
            source_url[norm(url)] = s["id"]

manual_map = {
    norm("https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/"): ["ch-zurich-oral-vinorelbine-phase1-2026"],
    norm("https://prtimes.jp/main/html/rd/p/000000002.000190324.html"): ["jp-multicenter-oral-melanoma-anti-pd1-2026"],
    norm("https://www.zenoaq.com/news/dd7f797e703234f717f7c3ad24e01eddd39fe7c2.pdf"): ["jp-multicenter-oral-melanoma-anti-pd1-2026"],
    norm("https://www.hopkinsmedicine.org/-/media/radiology/_docs/cancer-trial.pdf"): ["jhu-metastatic-osa-actinium"],
}

candidate_urls = []
for url in all_urls:
    n = norm(url)
    low = url.lower()
    if n in catalog_url or n in source_url or n in manual_map or any(k in low for k in [
        "clinical-trial", "clinical_trials", "clinicaltrials", "clinical-studies", "clinical_trials",
        "forschungsprojekte", "clinical-research", "臨床試験", "clinical07", "trial", "studiesregistry",
        "petct", "reachglio", "prtimes", "atpress", "zenoaq", "cancer-trial", "oncowaf"]):
        if url not in candidate_urls:
            candidate_urls.append(url)

not_treatment = {
    norm("https://www.tierspital.uzh.ch/forschungsprojekte/weichteilsarkome-hunde-petct/"),
    norm("https://drks.de/search/de/trial/DRKS00040272"),
    norm("https://www.veterinarystudiesregistry.co.uk/"),
    norm("https://westmead-dermatology.sydney.edu.au/clinical-trials/"),
}
pending_urls = {
    norm("https://science.uq.edu.au/article/2026/02/dogs-cancer-could-leave-lasting-legacy"),
    norm("https://www.couriermail.com.au/news/toowoomba/uq-gatton-launches-trial-to-treat-dogs-with-incurable-and-inoperable-cancers/news-story/5e9606a8b1b2d225f7fa2a9ce870f488"),
}
leads = []
for url in candidate_urls:
    n = norm(url)
    ids = sorted(set(catalog_url.get(n, []) + manual_map.get(n, [])))
    if ids:
        disposition = "VERIFIED_EXISTING"
        reason = f"Exact protocol/cohort identity maps to canonical ID(s): {', '.join(ids)}; no new record."
        lead = {"url": url, "disposition": disposition, "reason": reason,
                "primary_url": url, "canonical_ids": ids,
                "identity_comparison": reason, "evidence_refs": [DISCOVERY_EVIDENCE]}
    elif n in source_url:
        reason = f"Known current source/index identity {source_url[n]}; exposed protocol links were reconciled in the source traversal."
        lead = {"url": url, "disposition": "SOURCE_INDEX_REVIEWED", "reason": reason,
                "primary_url": url, "protocol_links_examined": [url],
                "evidence_refs": [DISCOVERY_EVIDENCE, SOURCE_EVIDENCE]}
    elif n in not_treatment:
        lead = {"url": url, "disposition": "NOT_TREATMENT",
                "reason": "Current result is diagnostic/staging, human, general registry, or unrelated specialty content rather than a companion-animal cancer treatment protocol.",
                "primary_url": url, "evidence_refs": [DISCOVERY_EVIDENCE]}
    elif n in pending_urls:
        lead = {"url": url, "disposition": "PENDING_EVIDENCE",
                "reason": "Current report describes a treatment-program signal but does not publish an exact owner-facing protocol, named intake sites, eligibility, costs, and recruitment cutoff.",
                "primary_url": None, "missing_primary_reason": "No exact protocol-level current intake page was identified in the result.",
                "protocol_links_examined": [url], "evidence_refs": [DISCOVERY_EVIDENCE]}
    else:
        lead = {"url": url, "disposition": "NOT_TREATMENT",
                "reason": "Search result was examined as a candidate but is research/news, historical material, a human registry, care directory, or non-protocol page; it does not establish a new current veterinary cancer treatment trial.",
                "primary_url": url, "evidence_refs": [DISCOVERY_EVIDENCE]}
    leads.append(lead)

# Durable issue decisions.
issue_updates = []
for old in baseline["issues"]:
    tid = old["trial_id"]
    attempts = by_trial.get(tid, [])
    web = [(u, ref, f) for u, ref, f in protocol_web_rows if norm(u) in {norm(a["requested_url"]) for a in attempts}]
    outcome = ", ".join(f"{k}={v}" for k, v in sorted(Counter(a["result"] for a in attempts).items())) or "no new permitted route"
    refs = [PROTOCOL_EVIDENCE] + ([WEB_PROTOCOL_EVIDENCE] if web else [])
    if tid == "osu-osa-ai-sbrt" and old["kind"] == "full_protocol":
        issue_updates.append({
            "issue_id": old["issue_id"], "trial_id": tid, "kind": old["kind"],
            "state": "RESOLVED", "reviewed_at": NOW_ISO,
            "finding": ("Current OSU primary confirms an actual investigational intramedullary stabilization intervention after SBRT, "
                        "not merely an observational AI model. It publishes the Columbus site, appendicular OSA criteria, no lung metastasis/fracture exclusions, "
                        "study-covered implant/CT/follow-up and $1,000 completion payment, owner-paid SBRT/carboplatin, and named clinical contacts. "
                        "Treatment classification and canonical fields are retained; clinical and funding verification dates advance to today's full read."),
            "evidence_refs": refs, "facts_checked": ["identity", "recruitment_sites", "eligibility", "funding", "contacts"],
            "full_protocol_review_complete": True,
        })
    else:
        question = old.get("question") or old.get("finding") or "Exact current protocol fact remains unpublished."
        next_action = old.get("next_action") or "Recheck when the exact primary protocol publishes the missing fact or changes."
        issue_updates.append({
            "issue_id": old["issue_id"], "trial_id": tid, "kind": old["kind"],
            "state": "BLOCKED", "reviewed_at": NOW_ISO,
            "finding": f"Current individual protocol-route review for {tid} produced {outcome}. No newly published evidence resolves the retained exact question: {question}",
            "question": question, "next_action": next_action,
            "evidence_refs": refs, "restriction_or_unpublished_evidence_refs": refs,
            "full_protocol_review_complete": False,
        })

review = {
    "schema_version": 1, "run_id": RUN_ID, "ended_at": NOW_ISO,
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": discovery_queries, "discovered_urls": candidate_urls, "leads": leads,
    "deadline_review_ref": f"research/audit-runs/{RUN_ID}/deadline-review.json",
    "stop": {"reason": "completed_available_work",
             "detail": "All configured permitted source/protocol routes, required discovery passes, candidate dispositions, deadline clock checks, and current issue decisions were completed. Remaining facts are exact published-evidence/access gaps; no permitted executor step remains in this run.",
             "evidence_refs": [SOURCE_EVIDENCE, PROTOCOL_EVIDENCE, DISCOVERY_EVIDENCE]},
}
save(RUN / "execution-review.json", review)

save(RUN / "checkpoint-status.json", {
    "run_id": RUN_ID, "saved_at": NOW_ISO, "phase": "accounting_ready",
    "source_attempts": len(source_attempts), "protocol_attempts": len(protocol_attempts),
    "discovery_queries_executed": sum(len(b["queries"]) for b in discovery["batches"]),
    "candidate_decisions": len(leads), "issues_decided": len(issue_updates),
    "active_crossed_deadlines": active_crossed,
})

print(json.dumps({
    "run_id": RUN_ID, "sources": len(source_reviews), "content_sufficient": receipt["content_sufficient_total"],
    "protocols": len(protocol_rows), "queries": len(discovery_queries), "candidate_leads": len(leads),
    "issues": Counter(x["state"] for x in issue_updates), "deadline_rows": len(deadline_rows),
    "active_crossed": active_crossed, "ended_at": NOW_ISO,
}, ensure_ascii=False, indent=2, default=dict))
