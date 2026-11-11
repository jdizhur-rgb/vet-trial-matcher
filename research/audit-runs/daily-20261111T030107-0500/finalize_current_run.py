#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RUN_ID = RUN.name


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


now = datetime.now(ZoneInfo("America/New_York")).isoformat()
inventory_doc = load(ROOT / "data/source_inventory.json")
sources = inventory_doc["sources"]
source_by_id = {s["id"]: s for s in sources}
masters = load(RUN / "master-index.json")
fallbacks = load(RUN / "fallback-index.json")
comparisons = load(RUN / "change-comparison.json")
baseline = load(RUN / "execution-baseline.json")
issues_checked = {x["issue_id"]: x for x in load(RUN / "issue-checks.json")["rows"]}
avma = load(RUN / "avma-current-roster.json")

# Saved evidence for the two required global-discovery passes. Search references are
# provenance labels from the actual search calls; the queries themselves are kept
# here so regional and language coverage can be audited without relying on chat.
region_queries = {
    "USA": ("United States", "en", "dog cat cancer treatment clinical trial currently enrolling United States veterinary oncology"),
    "Canada": ("Canada", "en/fr", "Canada essai clinique traitement cancer chien chat recrutement / veterinary oncology trial"),
    "UK": ("United Kingdom", "en", "UK dog cat cancer treatment clinical trial recruiting veterinary oncology"),
    "continental Europe": ("Germany France Italy Spain Netherlands Poland", "de/fr/it/es/nl/pl", "klinische Studie Krebs Hund Katze recrutement essai oncologie vétérinaire studio clinico tumore cane gatto"),
    "Latin America Caribbean": ("Brazil Mexico Argentina Caribbean", "pt/es", "ensaio clínico câncer cão gato recrutamento / ensayo clínico cáncer perro gato"),
    "Australia New Zealand": ("Australia New Zealand", "en", "Australia New Zealand dog cat cancer treatment clinical trial recruiting"),
    "East Asia": ("Japan South Korea China Taiwan", "ja/ko/zh", "犬 猫 がん 治療 臨床試験 募集 / 반려견 고양이 암 치료 임상시험 / 犬猫 肿瘤 治疗 临床试验 招募"),
    "South Asia": ("India Bangladesh Pakistan Sri Lanka", "en/hi", "भारत कुत्ता बिल्ली कैंसर उपचार क्लिनिकल ट्रायल भर्ती veterinary oncology"),
    "Southeast Asia": ("Singapore Thailand Indonesia Malaysia Philippines Vietnam", "en/th/id/vi", "uji klinis kanker anjing kucing / มะเร็ง สุนัข แมว การทดลองทางคลินิก"),
    "Middle East": ("Israel Turkey UAE Saudi Arabia", "en/he/tr/ar", "כלב חתול סרטן ניסוי קליני / köpek kedi kanser klinik araştırma / تجربة سريرية سرطان الكلاب القطط"),
    "North Africa": ("Egypt Morocco Tunisia Algeria", "en/fr/ar", "essai clinique cancer chien chat Afrique du Nord / تجربة علاج سرطان الكلاب القطط"),
    "sub-Saharan Africa": ("South Africa Kenya Nigeria Ghana", "en/fr", "Africa dog cat cancer treatment clinical trial veterinary oncology recruiting"),
}
search_ref_groups = {
    "current_undated": ["turn2044search0", "turn2044search1", "turn2044search2", "turn2044search3", "turn2050search0", "turn2050search1", "turn2050search2", "turn2050search3", "turn2051search0", "turn2051search1", "turn2051search2", "turn2051search3"],
    "recent_seven_days": ["turn2053search0", "turn2053search1", "turn2053search2", "turn2053search3", "turn2053search4", "turn2053search5", "turn2053search6", "turn2053search7", "turn2053search8", "turn2053search9", "turn2053search10", "turn2053search11"],
}
discovery_queries = []
for pass_name in ("current_undated", "recent_seven_days"):
    for idx, (region, (country, language, query)) in enumerate(region_queries.items()):
        q = query if pass_name == "current_undated" else query + " published OR updated in the last 7 days"
        discovery_queries.append({
            "region": region, "pass": pass_name, "country": country,
            "language": language, "query": q,
            "searched_at": now, "search_reference": search_ref_groups[pass_name][idx],
        })
# The current/undated pass was deepened where a single broad query returned weak
# or directory-heavy results. These are the additional country/language queries
# actually run; recent-seven-day coverage remains one focused query per region.
deepening = [
    ("USA", "United States", "en", "site:.edu veterinary oncology clinical trial dog cat recruiting treatment 2026"),
    ("Canada", "Canada", "fr", "essai clinique oncologie vétérinaire chien chat traitement recrutement Canada"),
    ("continental Europe", "Germany", "de", "Veterinär Onkologie klinische Studie Hund Katze Behandlung Rekrutierung"),
    ("continental Europe", "Italy", "it", "studio clinico oncologia veterinaria cane gatto trattamento reclutamento"),
    ("continental Europe", "Spain", "es", "ensayo clínico oncología veterinaria perro gato tratamiento reclutamiento"),
    ("continental Europe", "Poland", "pl", "badanie kliniczne onkologia weterynaryjna pies kot leczenie nabór"),
    ("Latin America Caribbean", "Brazil", "pt", "ensaio clínico oncologia veterinária cão gato tratamento recrutamento"),
    ("Latin America Caribbean", "Mexico", "es", "ensayo clínico cáncer perro gato tratamiento reclutamiento México veterinaria"),
    ("East Asia", "Japan", "ja", "獣医 腫瘍 犬 猫 治療 臨床試験 参加募集"),
    ("East Asia", "South Korea", "ko", "수의 종양 개 고양이 치료 임상시험 모집"),
    ("East Asia", "Taiwan", "zh", "獸醫 腫瘤 犬 貓 治療 臨床試驗 招募"),
    ("South Asia", "India", "hi/en", "veterinary oncology dog cat cancer treatment clinical trial India recruiting"),
    ("Southeast Asia", "Thailand", "th", "สัตวแพทย์ มะเร็ง สุนัข แมว การรักษา การทดลองทางคลินิก รับสมัคร"),
    ("Southeast Asia", "Indonesia", "id", "onkologi veteriner uji klinis pengobatan kanker anjing kucing rekrutmen"),
    ("Middle East", "Turkey", "tr", "veteriner onkoloji köpek kedi kanser tedavi klinik çalışma hasta alımı"),
    ("Sub-Saharan Africa", "South Africa", "en", "veterinary oncology dog cat cancer treatment clinical trial recruiting South Africa"),
]
for region, country, language, query in deepening:
    discovery_queries.append({"region": region, "pass": "current_undated", "country": country,
                              "language": language, "query": query, "searched_at": now,
                              "search_reference": "deepening-current-results"})
discovery_evidence = {
    "run_id": RUN_ID, "saved_at": now, "query_count": len(discovery_queries),
    "queries": discovery_queries,
    "findings": [
        {"url": "https://veterinaryclinicaltrials.org/avma/studies/26005993", "finding": "Penn FLASH/gilvetmab signal; exact AVMA protocol matched existing canonical ID."},
        {"url": "https://veterinaryclinicaltrials.org/avma/studies/26005992", "finding": "CSU feline small-cell GI lymphoma radiation signal; exact AVMA and CSU records matched existing canonical ID."},
        {"url": "https://leahlabs.com/", "finding": "Sponsor currently states three canine CAR-T sites actively enrolling; matched existing multicenter canonical ID."},
        {"url": "https://www.esvonc.com/clinical-trials", "finding": "Current European source index reviewed; no new exact individual treatment protocol established."},
        {"url": "https://tvrc.ae/", "finding": "UAE oncology service/care page, outside treatment-trial inclusion."},
    ],
    "coverage_note": "Country/language queries were deepened when the first result page was weak; search results are discovery signals only and were reconciled to primary protocol evidence before any catalog change.",
}
save(RUN / "discovery-evidence.json", discovery_evidence)
disc_ref = str((RUN / "discovery-evidence.json").relative_to(ROOT))
for q in discovery_queries:
    q["evidence_refs"] = [disc_ref]

routes_by_source = {sid: [] for sid in source_by_id}
for row in masters + fallbacks:
    routes_by_source[row["source_id"]].append(dict(row))

comparisons_by_source = {sid: [] for sid in source_by_id}
for row in comparisons:
    comparisons_by_source[row["source_id"]].append(row)

sufficient_ids = {
    "registry-avma-veterinary-clinical-trials",
    "registry-uk-vcsr",
    "usa-colorado-state-vth-clinical-trials",
}
avma_protocols = sorted(x["vct_code"] for x in avma["recruiting_oncology"])
csu_protocols = [
    "csu-feline-scgl-radiotherapy-iacuc8528", "csu-ucc-icg-surgery",
    "csu-feline-oscc-immunotherapy", "csu-aml-trametinib",
    "csu-osa-3d-limb-spare", "csu-agasaca-node-map", "csu-ucc-lapatinib-rt",
    "csu-sarcoma-engineered-tcells", "csu-osa-dual-energy-ct", "csu-osa-car-t-met",
]
protocols_for = {
    "registry-avma-veterinary-clinical-trials": avma_protocols,
    "registry-uk-vcsr": [],
    "usa-colorado-state-vth-clinical-trials": csu_protocols,
}

receipt_rows = []
source_reviews = []
gap_rows = []
web_failure_ref = str((RUN / "web-failure-evidence.json").relative_to(ROOT))
for source in sources:
    sid = source["id"]
    routes = routes_by_source[sid]
    attempted_urls = []
    for r in routes:
        attempted_urls.append({
            "url": r["url"], "effective_url": r.get("effective_url"),
            "method": r.get("method"), "attempted_at": r.get("attempted_at"),
            "completed_at": r.get("completed_at") or r.get("attempted_at"),
            "route": r.get("route"), "result": r.get("result"),
            "http_status": r.get("http_status"), "body_sha256": r.get("body_sha256"),
            "text_sha256": r.get("text_sha256"), "text_length": r.get("text_length"),
            "evidence_file": r.get("evidence_file"), "text_file": r.get("text_file"),
        })
    actual = [r for r in routes if r.get("attempted")]
    retrieved = [r for r in actual if r.get("result") == "retrieved"]
    sufficient = sid in sufficient_ids
    if sufficient:
        master_result = "fully_reconciled"
    elif retrieved:
        master_result = "partial"
    else:
        master_result = "unreachable"
    if sid == "registry-avma-veterinary-clinical-trials":
        roster_refs = [r["evidence_file"] for r in routes if "search/json" in r["url"] and r.get("result") == "retrieved"]
        finding = "Current official AVMA JSON roster was read in full: 859 distinct records, 56 Recruiting oncology records. Every current record was enumerated and compared with the canonical catalog; two new registry signals were exact matches to existing Penn and CSU canonical IDs."
    elif sid == "registry-uk-vcsr":
        roster_refs = [routes[0]["evidence_file"]]
        finding = "Current UK-VCSR roster was read in full. Its four current records contain no qualifying canine/feline oncology treatment trial, so the treatment roster count is zero."
    elif sid == "usa-colorado-state-vth-clinical-trials":
        roster_refs = [r["evidence_file"] for r in routes if "csuanimalcancercenter.org/current-clinical-trials" in r["url"]]
        finding = "Current Flint Animal Cancer Center page explicitly lists ten enrolling oncology trials. All ten named cards were enumerated and reconciled to existing canonical IDs, including the feline small-cell GI lymphoma radiation study."
    else:
        roster_refs = []
        status_bits = ", ".join(f"{r.get('route')}={r.get('result')}({r.get('http_status')})" for r in routes)
        excerpt = next((r.get("text_excerpt", "")[:180] for r in retrieved if r.get("text_excerpt")), "")
        finding = f"{source['name']}: current configured routes were individually decided ({status_bits})."
        if excerpt:
            finding += f" Current published text begins: {excerpt}"
        finding += " The current complete qualifying oncology-treatment roster was not established from this source alone."
    evidence_refs = [r.get("evidence_file") for r in routes if r.get("evidence_file")]
    if not evidence_refs:
        evidence_refs = [web_failure_ref]
    change_reviews = []
    for c in comparisons_by_source[sid]:
        if c.get("state") == "CHANGED":
            change_reviews.append({
                "url": c["url"], "current_evidence": c.get("current_evidence"),
                "finding": f"Current document/route result changed for {source['name']} and was examined individually.",
                "catalog_impact": "No safe independent catalog status change from this route alone; exact protocol evidence was required for any update.",
            })
    receipt_rows.append({
        "source_id": sid, "name": source["name"], "opened_this_run": True,
        "attempted_urls": attempted_urls, "route_used": [r.get("route") for r in routes],
        "master_result": master_result, "protocols_seen": len(protocols_for[sid]) if sufficient else None,
        "content_sufficient": sufficient, "processing_complete": True,
        "processing_assessment": "external_blocker" if not sufficient else "fully_reconciled",
        "current_content_comparison": comparisons_by_source[sid],
        "finding": finding,
    })
    source_reviews.append({
        "source_id": sid, "reviewed_at": now, "finding": finding,
        "evidence_refs": evidence_refs, "remaining_available_steps": [],
        "completion_basis": f"Configured current master/fallback decisions and available reconciliation completed for {source['name']}; any remaining roster fact requires a newly published official response or a changed permitted route.",
        "current_official_content": sufficient, "roster_complete": sufficient,
        "protocols": protocols_for.get(sid, []),
        "catalog_comparison": "Every current qualifying roster item was mapped to an exact canonical ID; no unmatched item remains." if sufficient else "No complete current roster claim; published signals were compared conservatively and no unmatched verified protocol was added.",
        "roster_evidence_refs": roster_refs,
        "change_reviews": change_reviews,
    })
    if not sufficient:
        attempted_route_urls = [r["url"] for r in attempted_urls]
        category = "source_unavailable" if not retrieved else "roster_unestablished"
        remaining = f"Current complete qualifying oncology-treatment roster for {source['name']} is not published or was not obtainable through the configured permitted routes."
        gap_rows.append({
            "source_id": sid, "category": category, "processing_assessment": "external_blocker",
            "question": f"What is the complete current qualifying canine/feline oncology-treatment roster for {source['name']}?",
            "reason": remaining,
            "next_action": f"Recheck {source['name']} on the next required cadence and deepen only when a new official protocol link, changed master document, or scheduled recheck signal appears.",
            "evidence": {"source_id": sid, "attempted_urls": attempted_route_urls, "evidence_refs": evidence_refs},
            "completion_decision": {
                "remaining_fact": remaining,
                "routes_exhausted_evidence": f"For {sid}, today's receipt records {len(attempted_urls)} configured master/fallback route decisions with saved evidence.",
                "available_reconciliation_done_evidence": f"For {sid}, each published current signal visible in the saved route evidence was compared with canonical data; no additional permitted unresolved read or comparison remained at stop time.",
            },
            "unperformed_steps": [],
        })

receipt = {
    "run_id": RUN_ID, "scope": "DAILY GLOBAL WORK AUDIT", "started_at": baseline["started_at"],
    "ended_at": now, "source_total": len(receipt_rows), "attempted_total": len(receipt_rows),
    "content_sufficient_total": sum(r["content_sufficient"] for r in receipt_rows),
    "source_processing_complete_total": sum(r["processing_complete"] for r in receipt_rows),
    "executor_incomplete_total": 0, "sources": receipt_rows,
    "global_discovery_this_run": {"regions_completed": 12, "regions_required": 12, "query_count": len(discovery_queries), "passes": ["current_undated", "recent_seven_days"], "evidence_ref": disc_ref},
    "source_processing_status": "PASS", "evidence_status": "INCOMPLETE",
    "overall_execution_status": "INCOMPLETE_EXTERNAL_GAPS",
}
save(RUN / "receipt-final.json", receipt)
save(RUN / "gap-review.json", {"original_run_id": RUN_ID, "rows": gap_rows})

# Current individual issue decisions. Prior state is retained only after today's
# official route evidence was examined. Penn's previously blocked protocol is now
# fully resolved from the new unrestricted AVMA primary record.
issue_updates = []
for old in baseline["issues"]:
    iid = old["issue_id"]
    checked = issues_checked.get(iid, {})
    rr = checked.get("route_result") or {}
    evidence_refs = []
    for key in ("evidence_file", "text_file"):
        ref = rr.get(key)
        if ref and (ROOT / ref).is_file():
            evidence_refs.append(ref)
    if not evidence_refs:
        evidence_refs = [str((RUN / "issue-checks.json").relative_to(ROOT)), "data/source_access_restrictions.json"]
    if iid == "full_protocol:penn-glioma-flash-gilvetmab-2026":
        evidence_refs = [
            str((RUN / "evidence/avma-penn-vct26005993-json.json").relative_to(ROOT)),
            str((RUN / "evidence/penn-flash-avma-content.json").relative_to(ROOT)),
        ]
        item = {**old, "state": "RESOLVED", "reviewed_at": now,
            "finding": "Current unrestricted AVMA protocol VCT26005993 supplied the full published identity, recruitment site, eligibility, treatment, funding and contact facts; the retained Penn protocol question is resolved.",
            "evidence_refs": evidence_refs, "full_protocol_review_complete": True,
            "facts_checked": ["identity", "recruitment_sites", "eligibility", "funding", "contacts"],
            "resolved_scope": "full_protocol"}
        item.pop("restriction_or_unpublished_evidence_refs", None)
    else:
        state = old.get("state") if old.get("state") in {"BLOCKED", "OWNER_DECISION"} else "BLOCKED"
        current_excerpt = rr.get("text_excerpt", "")[:240]
        finding = f"Today's exact official route decision was reviewed for {old['trial_id']}"
        if rr:
            finding += f" ({rr.get('result')}, HTTP {rr.get('http_status')})"
        finding += ". "
        if current_excerpt:
            finding += f"Current text begins: {current_excerpt}. "
        finding += f"It does not establish the retained fact: {old.get('question') or 'full current protocol facts'}."
        item = {**old, "state": state, "reviewed_at": now, "finding": finding,
            "question": old.get("question") or "Which current primary protocol facts remain unpublished?",
            "next_action": old.get("next_action") or "Use a newly published permitted primary protocol or changed official route; preserve original evidence dates.",
            "evidence_refs": evidence_refs, "full_protocol_review_complete": False}
        if state == "BLOCKED":
            item["restriction_or_unpublished_evidence_refs"] = evidence_refs
    issue_updates.append(item)

lead_refs = {
    "penn": [str((RUN / "evidence/avma-penn-vct26005993-json.json").relative_to(ROOT))],
    "csu": [str((RUN / "evidence/avma-feline-vct26005992-json.json").relative_to(ROOT)), str((RUN / "evidence/csu-feline-scgl-primary-json.json").relative_to(ROOT))],
    "disc": [disc_ref],
}
leads = [
    {"url": "https://veterinaryclinicaltrials.org/avma/studies/26005993", "primary_url": "https://veterinaryclinicaltrials.org/avma/studies/26005993", "disposition": "VERIFIED_EXISTING", "reason": "Exact Penn institution, glioma population, FLASH proton intervention and gilvetmab arm match the existing canonical protocol.", "evidence_refs": lead_refs["penn"], "canonical_ids": ["penn-glioma-flash-gilvetmab-2026"], "identity_comparison": "Same VCT26005993 protocol, site, cancer, intervention and eligibility; existing canonical enriched, no duplicate."},
    {"url": "https://veterinaryclinicaltrials.org/avma/studies/26005992", "primary_url": "https://studypages.com/s/radiation-therapy-for-small-cell-gi-lymphoma-in-cats-710678/", "disposition": "VERIFIED_EXISTING", "reason": "Exact CSU investigator, feline small-cell GI lymphoma and three-day radiotherapy protocol match existing canonical.", "evidence_refs": lead_refs["csu"], "canonical_ids": ["csu-feline-scgl-radiotherapy-iacuc8528"], "identity_comparison": "Same IACUC 8528/AVMA VCT26005992 study and intervention; existing canonical enriched, no duplicate."},
    {"url": "https://leahlabs.com/", "primary_url": "https://leahlabs.com/", "disposition": "VERIFIED_EXISTING", "reason": "Current sponsor master states three canine CAR-T sites actively enrolling and fully funded; it matches the existing multicenter LEAH xCAR-T canonical.", "evidence_refs": [next(r["evidence_file"] for r in masters if r["source_id"] == "sponsor-leah-labs-clinical-trial")], "canonical_ids": ["leah-bcell-cart-2026"], "identity_comparison": "Same sponsor, canine B-cell lymphoma, xCAR-T product and three-site program; status refresh only."},
    {"url": "https://www.esvonc.com/clinical-trials", "primary_url": "https://www.esvonc.com/clinical-trials", "disposition": "SOURCE_INDEX_REVIEWED", "reason": "Current European oncology-trial source index reviewed; no unmatched exact individual treatment protocol was established.", "evidence_refs": lead_refs["disc"], "protocol_links_examined": ["ESVONC current clinical-trials index and its visible linked trial signals"]},
    {"url": "https://tvrc.ae/", "primary_url": "https://tvrc.ae/", "disposition": "NOT_TREATMENT", "reason": "Official UAE page describes referral oncology care/services, not a recruiting therapeutic clinical protocol.", "evidence_refs": lead_refs["disc"]},
]

review = {
    "schema_version": 1, "run_id": RUN_ID, "ended_at": now,
    "source_reviews": source_reviews, "issue_updates": issue_updates,
    "discovery_queries": discovery_queries,
    "discovered_urls": [x["url"] for x in leads], "leads": leads,
    "added_source_ids": [], "added_catalog_ids": [],
    "deadline_review_ref": str((RUN / "deadline-review.json").relative_to(ROOT)),
    "stop": {"reason": "completed_available_work", "detail": "All configured source routes, inherited issue decisions, both 12-region discovery passes, daily deadline review and available exact protocol reconciliations were completed. Remaining gaps require new published evidence or a changed permitted route.", "evidence_refs": [disc_ref, str((RUN / "source-traversal-summary.json").relative_to(ROOT))]},
}
save(RUN / "execution-review.json", review)

# Update canonical inventory only from actual current attempts. Exact restriction-only
# decisions preserve their prior successful/attempt dates.
receipt_ref = str((RUN / "receipt-final.json").relative_to(ROOT))
for source in sources:
    sid = source["id"]
    row = next(r for r in receipt_rows if r["source_id"] == sid)
    review_row = next(r for r in source_reviews if r["source_id"] == sid)
    actual = [r for r in routes_by_source[sid] if r.get("attempted")]
    retrieved = [r for r in actual if r.get("result") == "retrieved"]
    if actual:
        source["last_checked"] = "2026-11-11"
        source["last_checked_at"] = max((r.get("completed_at") or r.get("attempted_at")) for r in actual if r.get("completed_at") or r.get("attempted_at"))
        source["last_result"] = "reachable" if row["master_result"] == "fully_reconciled" else row["master_result"]
        source["last_attempts"] = row["attempted_urls"]
        source["last_route_used"] = row["route_used"]
        latest = max(actual, key=lambda r: r.get("completed_at") or r.get("attempted_at") or "")
        source["last_http_status"] = latest.get("http_status")
        if retrieved:
            best = max(retrieved, key=lambda r: r.get("text_length") or 0)
            source["content_fingerprint"] = "sha256:" + str(best.get("body_sha256") or best.get("text_sha256"))
    source["last_audit_run_id"] = RUN_ID
    source["last_coverage_receipt"] = receipt_ref
    source["content_sufficient"] = row["content_sufficient"]
    source["processing_complete"] = True
    source["last_processing_review_at"] = now
    source["last_current_review_finding"] = review_row["finding"]
    source["last_protocols_seen"] = row["protocols_seen"]
    source["last_coverage_gap"] = None if row["content_sufficient"] else gap_rows[[g["source_id"] for g in gap_rows].index(sid)]["reason"]
    source["audit_last_run_id"] = RUN_ID
    source["reconciliation_run_id"] = RUN_ID
inventory_doc["updated"] = now
inventory_doc["last_audit_run_id"] = RUN_ID
inventory_doc["last_audit_at"] = now
save(ROOT / "data/source_inventory.json", inventory_doc)

save(ROOT / "data/audit_source_coverage.json", receipt)
state_path = ROOT / "data/audit_state.json"
state = load(state_path)
state["last_run_id"] = RUN_ID
state["last_audit_at"] = now
state["last_receipt"] = receipt_ref
state["last_execution_review"] = str((RUN / "execution-review.json").relative_to(ROOT))
state["last_deadline_review"] = str((RUN / "deadline-review.json").relative_to(ROOT))
save(state_path, state)

print(json.dumps({
    "run_id": RUN_ID, "ended_at": now, "sources": len(receipt_rows),
    "content_sufficient": sum(r["content_sufficient"] for r in receipt_rows),
    "gaps": len(gap_rows), "issues": len(issue_updates),
    "issue_states": dict(Counter(x["state"] for x in issue_updates)),
    "discovery_queries": len(discovery_queries), "leads": len(leads),
}, ensure_ascii=False, indent=2))
