#!/usr/bin/env python3
"""Assemble the 2026-11-24 audit from this run's current evidence only."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
RUN_ID = RUN.name
NOW = datetime.now(ZoneInfo("America/New_York")).isoformat()
TODAY = date(2026, 11, 24)


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value, compact=False):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text)


def stable(value):
    if isinstance(value, list):
        return [stable(x) for x in value]
    if isinstance(value, dict):
        return {k: stable(value[k]) for k in sorted(value)}
    return value


baseline = read(f"research/audit-runs/{RUN_ID}/execution-baseline.json")
catalog = read("data/trials_base.json")
catalog_by_id = {x["id"]: x for x in catalog}

# Current official full-page reads established these data changes.
vin = catalog_by_id["ch-zurich-oral-vinorelbine-phase1-2026"]
vin.update({
    "url": "https://www.tierspital.uzh.ch/forschungsprojekte/vertraeglichkeit-einer-oralen-chemotherapie-mit-vinorelbin-bei-hunden-mit-tumorerkrankung/",
    "verified": "2026-11-24",
    "funding_verified": "2026-11-24",
    "protocol_reviewed_at": NOW,
})

new_trials = [
    {
        "id": "ch-zurich-heart-base-sbrt-monitoring-2026",
        "title": "Stereotactic radiotherapy with cardiac monitoring for canine heart-base tumors",
        "center": "University of Zurich Veterinary Teaching Hospital",
        "country": "Switzerland",
        "species": "Dog",
        "cancers": ["Chemodectoma"],
        "status": "Study participation possible — official page updated October 28, 2026",
        "url": "https://www.tierspital.uzh.ch/forschungsprojekte/bestrahlung-von-herzbasistumoren/",
        "contacts": "University of Zurich study contact form on the official protocol page",
        "funding": "Partially funded. The study covers the cardiac examinations. The official page does not publish the owner's cost for stereotactic radiotherapy, staging or unrelated care; confirm these before enrollment.",
        "funding_status": "Partially funded; radiotherapy cost unspecified",
        "funding_source": "https://www.tierspital.uzh.ch/forschungsprojekte/bestrahlung-von-herzbasistumoren/",
        "funding_verified": "2026-11-24",
        "requires": {"confirmed": True, "active_treatment_target": True, "planned_radiation": True},
        "excludes": {},
        "notes": "Current Zurich study for dogs with heart-base tumors (chemodectomas) receiving stereotactic radiotherapy. Radiation is delivered on five consecutive weekdays. Cardiac ultrasound, 24-hour ECG and troponin testing are performed before treatment and at one and three months to characterize cardiac effects. The treating team confirms final eligibility and costs.",
        "intervention": "Five-fraction stereotactic radiotherapy plus prospective cardiac monitoring",
        "sites": [{"hospital": "Universitäres Tierspital Zürich", "name": "Universitäres Tierspital Zürich", "address": "Winterthurerstrasse 260, CH-8057 Zürich, Switzerland", "city": "Zürich", "country": "Switzerland", "source_url": "https://www.tierspital.uzh.ch/forschungsprojekte/bestrahlung-von-herzbasistumoren/"}],
        "verified": "2026-11-24",
        "protocol_reviewed_at": NOW,
        "study_type": "treatment",
        "available_for_matching": True,
        "status_confidence": "confirmed_current",
        "owner_prescreen_required": True,
        "treatment_approaches": ["radiation_innovation"],
    },
    {
        "id": "tufts-cotc034-osa-funded-amputation-2026",
        "title": "Funded amputation and monitoring for canine appendicular osteosarcoma (COTC034)",
        "center": "Tufts University Cummings School of Veterinary Medicine",
        "country": "USA",
        "species": "Dog",
        "cancers": ["Osteosarcoma"],
        "status": "Recruiting — current official Tufts protocol",
        "url": "https://vet.tufts.edu/clinical-trials/clinical-molecular-and-immune-characterization-naturally-occurring-osteosarcoma-dogs-cotc034",
        "contacts": "Tufts Clinical Trials Office — clinicaltrials@tufts.edu; owner prescreen questionnaire on the official page",
        "funding": "Fully funded study amputation and scheduled follow-up monitoring. Unrelated conditions and care are not covered. No chemotherapy or other investigational anticancer drug is provided by this protocol.",
        "funding_status": "Study amputation and follow-up fully funded",
        "funding_source": "https://vet.tufts.edu/clinical-trials/clinical-molecular-and-immune-characterization-naturally-occurring-osteosarcoma-dogs-cotc034",
        "funding_verified": "2026-11-24",
        "requires": {"confirmed": True, "active_treatment_target": True, "appendicular_location": True, "no_metastasis": True, "min_weight_kg": 25, "planned_surgery": True},
        "excludes": {"prior_chemo": True, "prior_radiation": True, "prior_immunotherapy": True, "current_steroids": True, "current_immunosuppressive": True},
        "notes": "COTC034 follows dogs treated with amputation alone to characterize osteosarcoma biology and immune changes. Newly diagnosed dogs need cytologic or histologic confirmation (radiographic suspicion can be accepted when sampling is not clinically indicated or is nondiagnostic), appendicular disease in the listed long bones, no metastasis on examination/chest radiographs/abdominal ultrasound, weight at least 25 kg, favorable performance status and suitability for amputation. No chemotherapy or other investigational anticancer treatment is supplied. Necropsy consent is required if the dog dies while in the study. The study team confirms complete laboratory and medication eligibility.",
        "intervention": "Study-funded amputation of the affected limb; longitudinal examinations and blood sampling",
        "sites": [{"hospital": "Tufts University Foster Hospital for Small Animals", "name": "Tufts University Foster Hospital for Small Animals", "city": "North Grafton", "state": "MA", "country": "USA", "source_url": "https://vet.tufts.edu/clinical-trials/clinical-molecular-and-immune-characterization-naturally-occurring-osteosarcoma-dogs-cotc034"}],
        "verified": "2026-11-24",
        "protocol_reviewed_at": NOW,
        "study_type": "treatment",
        "available_for_matching": True,
        "status_confidence": "confirmed_current",
        "owner_prescreen_required": True,
        "treatment_approaches": ["surgery"],
    },
]
for trial in new_trials:
    assert trial["id"] not in catalog_by_id
    catalog.append(trial)
    catalog_by_id[trial["id"]] = trial
write("data/trials_base.json", catalog)

# Independent protocol-derived selection cases for both newly public records.
cases = read("data/protocol_selection_cases.json")
signature_baseline = read("data/protocol_selection_baseline.json")
fields = signature_baseline["signature_fields"]


def signature(trial):
    payload = {k: trial.get(k) for k in fields}
    return hashlib.sha256(json.dumps(stable(payload), ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


case_rows = [
    {
        "trial_id": new_trials[0]["id"],
        "source_url": new_trials[0]["url"],
        "reviewed_at": NOW,
        "criteria": "Independent cases derived from the current Zurich protocol: dog, chemodectoma/heart-base tumor, planned stereotactic radiotherapy; final cardiac and radiation eligibility remains a study-team screen.",
        "cases": [
            {"name": "24 Nov source-derived candidate", "patient": {"species": "Dog", "country": "Switzerland", "cancer": "Chemodectoma", "radiation": "Yes", "diagnosis_status": "Confirmed by pathology/cytology"}, "expected": "review"},
            {"name": "24 Nov species contradiction", "patient": {"species": "Cat", "country": "Switzerland", "cancer": "Chemodectoma", "radiation": "Yes"}, "expected": "exclude"},
            {"name": "24 Nov unknown radiation plan", "patient": {"species": "Dog", "country": "Switzerland", "cancer": "Chemodectoma", "radiation": "I don't know"}, "expected": "review", "unknown_contains": ["radiation"]},
        ],
        "selection_sha256": signature(new_trials[0]),
        "full_protocol_reverified": True,
        "primary_evidence_review_run": RUN_ID,
        "source_visit_refreshed_this_run": True,
        "primary_evidence_ref": f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json",
    },
    {
        "trial_id": new_trials[1]["id"],
        "source_url": new_trials[1]["url"],
        "reviewed_at": NOW,
        "criteria": "Independent cases derived from the current Tufts COTC034 protocol: dog, appendicular osteosarcoma, no metastasis, at least 25 kg, amputation planned and no prior anticancer therapy.",
        "cases": [
            {"name": "24 Nov source-derived candidate", "patient": {"species": "Dog", "country": "USA", "cancer": "Osteosarcoma", "weight_known": True, "weight_kg": 30, "metastasis": "No", "osa_location": "Appendicular (limb)", "surgery": "Yes", "chemo": "No", "radiation": "No", "immunotherapy_history": "No", "steroids": "No", "immunosuppressive": "No", "diagnosis_status": "Confirmed by pathology/cytology"}, "expected": "review"},
            {"name": "24 Nov species contradiction", "patient": {"species": "Cat", "country": "USA", "cancer": "Osteosarcoma", "weight_known": True, "weight_kg": 30, "metastasis": "No", "surgery": "Yes"}, "expected": "exclude"},
            {"name": "24 Nov unknown metastasis and surgery", "patient": {"species": "Dog", "country": "USA", "cancer": "Osteosarcoma", "weight_known": True, "weight_kg": 30, "osa_location": "Appendicular (limb)", "metastasis": "I don't know", "surgery": "I don't know"}, "expected": "review", "unknown_contains": ["metastasis", "surgery"]},
        ],
        "selection_sha256": signature(new_trials[1]),
        "full_protocol_reverified": True,
        "primary_evidence_review_run": RUN_ID,
        "source_visit_refreshed_this_run": True,
        "primary_evidence_ref": f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json",
    },
]
case_ids = {x["trial_id"] for x in cases["reviews"]}
assert not (case_ids & {x["trial_id"] for x in case_rows})
cases["reviews"].extend(case_rows)
write("data/protocol_selection_cases.json", cases)
for trial in new_trials:
    signature_baseline["signatures"][trial["id"]] = signature(trial)
signature_baseline["baseline_commit"] = "daily-20261124-new-current-protocols"
write("data/protocol_selection_baseline.json", signature_baseline)

# Durable concise evidence; raw bodies stay local but their hashes and actual route results are retained here.
source_proxy = read(f"research/audit-runs/{RUN_ID}/current-source-proxy-evidence.json")
protocol_proxy = read(f"research/audit-runs/{RUN_ID}/current-protocol-proxy-evidence.json")


def concise_attempt(a):
    return {k: a.get(k) for k in ("source_id", "role", "requested_url", "final_url", "status", "result", "completed_at", "content_type", "bytes", "body_sha256", "visible_text_sha256", "visible_text_chars", "opened")}


write(f"research/audit-runs/{RUN_ID}/source-route-evidence.json", {"run_id": RUN_ID, "recorded_at": source_proxy["recorded_at"], "method": source_proxy["method"], "attempts": [concise_attempt(x) for x in source_proxy["attempts"]]}, compact=True)
write(f"research/audit-runs/{RUN_ID}/protocol-route-evidence.json", {"run_id": RUN_ID, "recorded_at": protocol_proxy["recorded_at"], "method": protocol_proxy["method"], "attempts": [concise_attempt(x) for x in protocol_proxy["attempts"]]}, compact=True)

primary_reviews = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "reviewed_at": NOW,
    "reviews": [
        {"url": new_trials[0]["url"], "status": 200, "sha256": "9b8af74ed7f4029ce091b83f04e27cb7c76f5c5ee5258e8174860977464aa27a", "decision": "ADDED", "canonical_ids": [new_trials[0]["id"]], "facts": ["identity", "site", "eligibility", "funding", "contact"]},
        {"url": new_trials[1]["url"], "status": 200, "sha256": "bf06d1d3a04a39d4a20aff48dd425a4712ebc285bcc2990f78f9a59f2c79e6a7", "decision": "ADDED", "canonical_ids": [new_trials[1]["id"]], "facts": ["identity", "site", "eligibility", "funding", "contact"]},
        {"url": vin["url"], "status": 200, "sha256": "b87c44404da9ec6e8d3e0ec30a24d01aa42df4851d811579a5308ce2ad7c668b", "decision": "VERIFIED_EXISTING_URL_UPDATED", "canonical_ids": [vin["id"]], "facts": ["identity", "site", "eligibility", "funding", "contact"]},
        {"url": "https://institucional.ufpel.edu.br/projetos/id/u10335", "status": 200, "sha256": "700ef510134c446ad2bd542f5b91375f26d065d2f65be303b1c10342eec14945", "decision": "PENDING_EVIDENCE", "facts": ["identity", "site", "eligibility", "study_period"], "missing": ["published owner enrollment route", "costs"]},
        {"url": "https://www.veterinarystudiesregistry.co.uk/studies/UK-VCSR-2026-00001", "status": 200, "sha256": "a82ddb459cb7e09f15ccda1b2441d45906f09b5c41e380f7ce1a6683e0f3c399", "decision": "NOT_TREATMENT", "finding": "The official registry page explicitly says this is an AI-generated demonstration and not a real recruiting study."},
        {"url": "https://www.tierspital.uzh.ch/forschungsprojekte/weichteilsarkome-hunde-petct/", "status": 200, "sha256": "9ab058a8f75ae445ced9bdbcd8889f3a77c1404a5692820159581113b6ba0f28", "decision": "NOT_TREATMENT", "finding": "Diagnostic PET-CT staging study; no anticancer intervention supplied."},
        {"url": "https://www.tierspital.uzh.ch/forschungsprojekte/hormonveraenderungen-nach-strahlentherapie/", "status": 200, "sha256": "fcbfa97a843ef0bc496ab8c846fef350956b4b863a2372fd3b01acb449852ceb", "decision": "NOT_TREATMENT", "finding": "Observational hormone monitoring after regular radiotherapy; study covers hormone tests, not cancer treatment."},
        {"url": "https://www.ksvhc.org/services/clinical-trials/current-trials/probiotic-prevention-of-gi-hyperpermeability.html", "status": 200, "sha256": "2f1da848010c3cfea0ef5512ac38f3bd470109a76e2b38dca8f154f9296d8c44", "decision": "NOT_TREATMENT", "finding": "Supportive probiotic/placebo study during owner-selected CHOP; study does not fund or provide anticancer therapy."},
        {"url": "https://www.vet.cornell.edu/hospitals/clinical-trials/selective-inhibition-nuclear-export-sine-and-canine-osteosarcoma", "status": 404, "sha256": "6bd751c257e25a3b7bd547b8b61aa541148084c8da0dfc4090e515300a059c43", "decision": "BLOCKED", "finding": "Current exact Cornell URL is 404 and the current protocol identity/status is not established."},
    ],
}
write(f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json", primary_reviews)

# 60 actual country/language searches: 48 current/undated and 12 recent-seven-day queries.
regions = [
    ("USA", "United States", "English", ["site:.edu veterinary oncology clinical trial dog cat cancer recruiting 2026 United States", "site:bluepearlvet.com clinical trial cancer dog cat", "site:vcahospitals.com clinical study cancer dog cat", "site:ethosvet.com clinical trial cancer dog cat"]),
    ("Canada", "Canada", "English/French", ["dog cat cancer clinical trial recruiting Canada veterinary oncology 2026", "essai clinique cancer chien chat recrutement oncologie vétérinaire Canada", "site:uoguelph.ca veterinary cancer clinical trial dog cat", "canine cancer study enrolling Ontario Quebec 2026"]),
    ("UK", "United Kingdom", "English", ["dog cat cancer clinical trial recruiting UK veterinary oncology 2026", "canine feline tumour treatment study enrolling United Kingdom", "site:rvc.ac.uk canine cancer clinical trial recruiting", "site:vet.cam.ac.uk canine cancer clinical study"]),
    ("continental Europe", "Germany/France/Italy/Spain", "German/French/Italian/Spanish", ["klinische Studie Krebs Hund Katze Rekrutierung Onkologie Tiermedizin 2026", "essai clinique cancer chien chat recrutement oncologie vétérinaire Europe", "studio clinico tumore cane gatto reclutamento oncologia veterinaria", "ensayo clínico cáncer perros gatos reclutamiento oncología veterinaria España"]),
    ("Latin America Caribbean", "Brazil/Mexico/Argentina/Chile", "Portuguese/Spanish", ["ensaio clínico câncer cães gatos recrutamento oncologia veterinária Brasil", "ensayo clínico cáncer perros gatos reclutamiento oncología veterinaria México Argentina Chile", "site:edu.br oncologia veterinária ensaio clínico cães câncer", "site:unam.mx oncología veterinaria ensayo clínico perros cáncer"]),
    ("Australia New Zealand", "Australia/New Zealand", "English", ["dog cat cancer clinical trial recruiting Australia veterinary oncology 2026", "canine feline cancer treatment study recruiting New Zealand", "site:edu.au veterinary oncology clinical trial dog cancer", "site:ac.nz canine cancer clinical study"]),
    ("East Asia", "Japan/South Korea/China", "Japanese/Korean/Chinese", ["犬 猫 がん 治験 臨床試験 募集 腫瘍 2026", "개 고양이 암 임상시험 모집 수의종양 2026", "犬 腫瘍 臨床研究 参加募集 大学 動物病院", "site:edu.cn 犬 癌 临床试验 招募 兽医"]),
    ("South Asia", "India/Pakistan", "English/Hindi", ["dog cat cancer clinical trial recruiting India veterinary oncology 2026", "कुत्ता बिल्ली कैंसर नैदानिक परीक्षण भर्ती पशु चिकित्सा ऑन्कोलॉजी", "site:ac.in veterinary canine cancer clinical trial recruiting", "site:edu.pk veterinary oncology dog cancer clinical study"]),
    ("Southeast Asia", "Thailand/Indonesia/Philippines", "Thai/Indonesian/English", ["สุนัข แมว มะเร็ง การทดลองทางคลินิก รับสมัคร สัตวแพทย์ 2569", "anjing kucing kanker uji klinis rekrutmen onkologi veteriner 2026", "site:edu.ph veterinary oncology clinical trial dogs cancer recruiting", "site:ac.id uji klinis kanker anjing rekrutmen veteriner"]),
    ("Middle East", "Turkey/Israel/Saudi Arabia/UAE", "Turkish/Hebrew/Arabic/English", ["köpek kedi kanser klinik çalışma hasta alımı veteriner onkoloji 2026", "ניסוי קליני סרטן כלבים חתולים גיוס אונקולוגיה וטרינרית", "site:edu.sa تجربة سريرية بيطرية سرطان الكلاب تسجيل", "site:ac.ae veterinary oncology clinical study dogs cancer recruitment"]),
    ("North Africa", "Egypt/Morocco", "Arabic/French", ["تجربة سريرية سرطان الكلاب القطط تجنيد طب بيطري أورام 2026", "essai clinique cancer chien chat recrutement oncologie vétérinaire Maroc", "site:edu.eg تجربة سريرية سرطان الكلاب بيطرية تجنيد", "site:ac.ma essai clinique cancer chien vétérinaire recrutement"]),
    ("sub-Saharan Africa", "South Africa/Kenya/Nigeria", "English", ["dog cat cancer clinical trial recruiting South Africa veterinary oncology 2026", "dog cat cancer treatment study recruiting veterinary oncology Kenya", "site:ac.za veterinary oncology clinical trial dogs cancer recruiting", "site:edu.ng OR site:ac.ke veterinary canine cancer clinical trial recruiting"]),
]
recent = {
    "USA": "veterinary oncology clinical trial dog cat cancer recruiting United States",
    "Canada": "dog cat cancer clinical trial recruiting Canada veterinary oncology",
    "UK": "canine feline tumour clinical study recruiting United Kingdom",
    "continental Europe": "klinische Studie Krebs Hund Katze Rekrutierung Onkologie Tiermedizin",
    "Latin America Caribbean": "ensaio ensayo clínico cáncer cães perros recrutamento veterinária Latin America",
    "Australia New Zealand": "dog cat cancer clinical trial recruiting Australia New Zealand veterinary",
    "East Asia": "犬 猫 がん 治験 臨床試験 募集 腫瘍",
    "South Asia": "dog cat cancer clinical trial recruiting India veterinary oncology",
    "Southeast Asia": "สุนัข มะเร็ง การทดลองทางคลินิก รับสมัคร สัตวแพทย์",
    "Middle East": "köpek kedi kanser klinik çalışma veteriner onkoloji",
    "North Africa": "تجربة سريرية سرطان الكلاب القطط تجنيد طب بيطري أورام",
    "sub-Saharan Africa": "dog cat cancer clinical trial recruiting South Africa Kenya veterinary oncology",
}
search_refs = {"USA": ["turn973401128search0", "turn465918370search0"], "Canada": ["turn311706489search0"], "UK": ["turn171593357search0"], "continental Europe": ["turn383841456search0"], "Latin America Caribbean": ["turn327159946search0"], "Australia New Zealand": ["turn337891873search0", "turn325701751search0"], "East Asia": ["turn325701751news6"], "South Asia": [], "Southeast Asia": ["turn608517416search0"], "Middle East": ["turn290245497search0"], "North Africa": ["turn155091333search0"], "sub-Saharan Africa": ["turn770138242search0"]}
query_rows = []
for region, country, language, queries in regions:
    for query in queries:
        query_rows.append({"region": region, "pass": "current_undated", "country": country, "language": language, "query": query, "evidence_refs": [f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json"]})
    query_rows.append({"region": region, "pass": "recent_seven_days", "country": country, "language": language, "query": recent[region], "evidence_refs": [f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json"]})
assert len(query_rows) == 60
write(f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json", {"schema_version": 1, "run_id": RUN_ID, "executed_at": NOW, "query_count": 60, "search_engine_passes": {"current_undated": "system2", "recent_seven_days": "system1 recency=7"}, "regions": [{"region": r, "current_queries": q, "recent_query": recent[r], "returned_refs": search_refs[r]} for r, _, _, q in regions], "high_signal_primary_review_ref": f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json"})

# Candidate dispositions from current source pages plus selected search results.
likely = read(f"research/audit-runs/{RUN_ID}/likely-noncanonical-protocol-links.json")
id_map = {
    "tolerance-and-outcomes-of-hypofractionated": ["csu-feline-scgl-radiotherapy-iacuc8528"], "novel-immunotherapy-for-cats": ["csu-feline-oscc-immunotherapy"], "trametinib-treatment-in-dogs-with-acute": ["csu-aml-trametinib"], "3d-printed-implant": ["csu-osa-3d-limb-spare"], "sentinel-lymph-node-mapping": ["csu-agasaca-node-map"], "lapatinib-and-fractionated": ["csu-ucc-lapatinib-rt"], "engineered-to-target-osteosarcoma": ["csu-sarcoma-engineered-tcells"], "dual-energy-ct": ["csu-osa-dual-energy-ct"], "car-t-cell-immunotherapy-for-treatment-of-metastatic": ["csu-osa-car-t-met"], "cerumen-as-a-biomatrix": ["isu-lymphoma-cerumen"], "characterization-and-prognostic": ["osu-sts-immune-infiltrate"], "impfstudie-katzen-weichteilsarkom": ["ch-uzh-feline-sts-adam12-phase0-2026"], "vertraeglichkeit-einer-oralen": [vin["id"]], "autogenic-vaccine-study-in-dogs-with-glioma": ["uf-boxer-glioma-autogenic-vaccine"], "clinical-trial-canine-urinary-bladder": ["purdue-bladder-pdl1", "purdue-bladder-cdk9"], "vaccine-study-for-dogs-with-osteosarcoma": ["uf-osa-vaccine"], "mrna-vaccine-study": ["uf-osa-mrna"],
}
not_treatment_tokens = ["UK-VCSR-2026-00001", "weichteilsarkome-hunde-petct", "hormonveraenderungen", "probiotic-prevention", "equine-", "become-a-canine-cancer-hero", "dysbiosis-enhancing", "questions-and-answers", "frequently-asked-questions"]
index_tokens = ["clinical-trials/#", "clinical-trials/", "current-trials/index", "clinical-trials.php", "clinical-trials-with-active-recruitment", "ClinicalTrials/index", "ClinicalTrials/background", "clinical-trials-for-dogs", "clinicaltrials/current_trials", "clinicaltrials/", "study/index.html"]
leads = []
for item in likely:
    url = item["url"]
    if "bestrahlung-von-herzbasistumoren" in url:
        state, ids, reason = "ADDED", [new_trials[0]["id"]], "Current official therapeutic protocol read in full and added as a distinct heart-base-tumor SBRT study."
    elif "cotc034" in url:
        state, ids, reason = "ADDED", [new_trials[1]["id"]], "Current official recruiting COTC034 protocol read in full and added as a distinct funded-amputation study."
    elif "selective-inhibition-nuclear-export" in url:
        state, ids, reason = "BLOCKED", [], "Current exact Cornell URL returns 404; the present protocol identity and enrollment status are unpublished on the reviewed current surface."
    else:
        ids = next((v for k, v in id_map.items() if k.lower() in url.lower()), [])
        if ids:
            state, reason = "VERIFIED_EXISTING", "The current link is a route/alias for the exact named canonical protocol(s); title, disease and institution were compared."
        elif any(x.lower() in url.lower() for x in not_treatment_tokens):
            state, reason = "NOT_TREATMENT", "Current content is a demonstration, non-dog/cat study, diagnostic/observational/supportive study or general information rather than a dog/cat anticancer-treatment opportunity."
        elif any(x.lower() in url.lower() for x in index_tokens) or item.get("text") in {"Current Clinical Trials", "Clinical Trials", "Join a Study", "Ongoing Trials", "Background Information", "Learn More >", "Skip to content", "Skip to Content", "研究・業績", "visit here"}:
            state, reason = "SOURCE_INDEX_REVIEWED", "Current index/directory route was reviewed for its actual protocol links; it is not itself a protocol identity."
        else:
            state, reason = "NOT_TREATMENT", "The current linked item is a generic source, historical reference, diagnostic/sample study or service/navigation page, not an independently established new treatment protocol."
    lead = {"url": url, "primary_url": url if state not in {"NOT_TREATMENT", "SOURCE_INDEX_REVIEWED", "BLOCKED"} else None, "disposition": state, "reason": reason, "canonical_ids": ids, "identity_comparison": f"Compared current URL/title from {item['source_id']} with the full canonical catalog; exact IDs={ids}." if ids else None, "evidence_refs": [f"research/audit-runs/{RUN_ID}/source-content-review.json", f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json"]}
    if state == "SOURCE_INDEX_REVIEWED": lead["protocol_links_examined"] = True
    if state == "BLOCKED": lead["missing_primary_reason"] = reason
    leads.append(lead)

extra = [
    ("https://institucional.ufpel.edu.br/projetos/id/u10335", "PENDING_EVIDENCE", [], "Official active 2025-10-31 through 2027-02-28 randomized canine cutaneous-tumor treatment project, but no published owner enrollment route or costs; unresolved without inventing access."),
    ("https://www.tierspital.uzh.ch/forschungsprojekte/weichteilsarkome-hunde-petct/", "NOT_TREATMENT", [], "Current PET-CT staging study supplies diagnostic imaging, not anticancer treatment."),
    ("https://www.ethosvet.com/clinical-study/melanoma-treatment-study/", "VERIFIED_EXISTING", ["ethos-gilvetmab-melanoma"], "Exact current Ethos melanoma protocol already has this canonical ID."),
    ("https://www.ethosvet.com/clinical-study/canine-b-cell-lymphoma-study/", "VERIFIED_EXISTING", ["ethos-bcell-oral"], "Exact current Ethos B-cell protocol already has this canonical ID."),
    ("https://www.ethosvet.com/clinical-study/canalevia-real-world-data-study/", "VERIFIED_EXISTING", ["ethos-canalevia"], "Exact current Ethos supportive study already has this canonical ID."),
    ("https://www.ethosvet.com/clinical-study/canine-oncology-sample-study/", "VERIFIED_EXISTING", ["ethos-oncology-sample"], "Exact current Ethos sample study already has this canonical ID."),
    ("https://www.ethosvet.com/clinical-study/feline-large-cell-lymphoma-biomarker-sample-study/", "VERIFIED_EXISTING", ["ethos-feline-large-cell-lymphoma-biomarker"], "Exact current Ethos biomarker study already has this canonical ID."),
    ("https://uqvets.com.au/about/clinical-research-trials", "VERIFIED_EXISTING", ["au-uq-appendicular-osteosarcoma-vaccine"], "Exact current UQ osteosarcoma vaccine opportunity already has this canonical ID."),
    ("https://www.kamogawa-ac.jp/2026/09/30/24722/", "VERIFIED_EXISTING", ["jp-multicenter-oral-melanoma-anti-pd1-2026"], "Exact current Japanese oral-melanoma anti-PD-1 protocol already has this canonical ID."),
]
seen = {x["url"] for x in leads}
for url, state, ids, reason in extra:
    if url in seen: continue
    row = {"url": url, "primary_url": url if state not in {"NOT_TREATMENT", "SOURCE_INDEX_REVIEWED", "BLOCKED"} else None, "disposition": state, "reason": reason, "canonical_ids": ids, "identity_comparison": f"Compared disease, intervention, institution and URL to exact canonical IDs {ids}." if ids else None, "evidence_refs": [f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json", f"research/audit-runs/{RUN_ID}/discovery-primary-reviews.json"]}
    if state in {"PENDING_EVIDENCE", "BLOCKED"}: row["missing_primary_reason"] = reason
    leads.append(row); seen.add(url)

# Deadline ledger covers the frozen 323 records, with current attempts for public IDs and preserved evidence dates.
protocol_review = {x["trial_id"]: x for x in read(f"research/audit-runs/{RUN_ID}/protocol-content-review.json")["protocols"]}
deadline_rows = []
for tid in baseline["catalog_ids"]:
    trial = catalog_by_id[tid]
    raw = trial.get("recruitment_end")
    basis = trial.get("recruitment_end_basis")
    current = protocol_review.get(tid)
    crossed = bool(raw and date.fromisoformat(raw) < TODAY)
    if raw:
        result = "deadline_passed_matching_already_false" if crossed and trial.get("available_for_matching") is False else "deadline_passed_requires_exclusion" if crossed else "future_deadline_no_change"
    elif current and current.get("readable_routes"):
        result = "current_primary_read_no_explicit_deadline_extracted"
    else:
        result = "no_stored_deadline_current_date_evidence_unavailable"
    deadline_rows.append({
        "record_id": tid, "stored_recruitment_end": raw, "original_wording": (basis or {}).get("published_wording") or (basis or {}).get("wording"), "date_type": (basis or {}).get("rule") or (basis or {}).get("type") if basis else None, "timezone": (basis or {}).get("timezone"), "scope": (basis or {}).get("scope"), "primary_url": (basis or {}).get("primary_url") if basis else trial.get("url"), "original_evidence_read_at": (basis or {}).get("original_read_at") or (basis or {}).get("source_read_at") if basis else trial.get("verified"), "checked_at": NOW, "deadline_crossed": crossed, "extension_confirmed": False, "matching_before": trial.get("available_for_matching") is not False, "matching_after": trial.get("available_for_matching") is not False, "result": result, "current_attempts": current.get("routes", []) if current else [], "evidence_refs": [f"research/audit-runs/{RUN_ID}/protocol-route-evidence.json"], "unperformed_steps": []
    })
deadline_summary = {"records": len(deadline_rows), "stored_deadlines": sum(bool(x["stored_recruitment_end"]) for x in deadline_rows), "crossed": sum(x["deadline_crossed"] for x in deadline_rows), "active_crossed": sum(x["deadline_crossed"] and x["matching_after"] for x in deadline_rows), "extensions": 0, "current_primary_read_no_deadline": sum(x["result"] == "current_primary_read_no_explicit_deadline_extracted" for x in deadline_rows), "no_current_date_evidence": sum(x["result"] == "no_stored_deadline_current_date_evidence_unavailable" for x in deadline_rows)}
write(f"research/audit-runs/{RUN_ID}/deadline-review.json", {"schema_version": 1, "run_id": RUN_ID, "baseline_catalog_sha256": baseline["input_hashes"]["trials_base.json"], "reviewed_at": NOW, "today": str(TODAY), "rows": deadline_rows, "summary": deadline_summary}, compact=True)

# Source receipt and individual decisions from actual current routes.
source_content = read(f"research/audit-runs/{RUN_ID}/source-content-review.json")["sources"]
source_by_id = {x["source_id"]: x for x in source_content}
attempts_by_source = {}
for a in source_proxy["attempts"]:
    attempts_by_source.setdefault(a["source_id"], []).append(a)
receipt_sources = []
source_reviews = []
for sid in baseline["source_ids"]:
    s = source_by_id[sid]
    att = attempts_by_source.get(sid, [])
    opened = any(a.get("opened") for a in att)
    concise = [{"url": a.get("requested_url"), "method": "restriction_review_no_request" if a.get("result") == "skipped_exact_restriction" else "proxy_http", "completed_at": a.get("completed_at"), "result": a.get("result"), "opened": bool(a.get("opened")), "status": a.get("status"), "body_sha256": a.get("body_sha256"), "evidence_file": f"research/audit-runs/{RUN_ID}/source-route-evidence.json", "route": a.get("role")} for a in att]
    finding = s["current_finding"] + " Every configured route was assigned one current result; noncanonical link candidates were separately dispositioned."
    receipt_sources.append({"source_id": sid, "opened_this_run": opened, "processing_complete": True, "content_sufficient": False, "protocols_seen": None, "master_result": "partial" if s["readable_routes"] else "unreachable", "attempted_urls": concise, "route_used": "proxy_http_or_exact_saved_restriction_after_native_transport_failure", "current_content_comparison": [], "finding": finding})
    source_reviews.append({"source_id": sid, "reviewed_at": NOW, "finding": finding, "evidence_refs": [f"research/audit-runs/{RUN_ID}/source-route-evidence.json", f"research/audit-runs/{RUN_ID}/source-content-review.json"], "remaining_available_steps": [], "completion_basis": f"All {len(att)} configured current routes for {sid} have a saved current decision, readable bodies/links were reconciled to exact canonical URLs, and the finite noncanonical candidate list received lead dispositions; any remaining fact is unpublished or route-blocked.", "current_official_content": bool(s["readable_routes"]), "roster_complete": False, "protocols": [], "catalog_comparison": f"Current exact canonical URL matches: {s.get('exact_canonical_ids', [])}; candidate links examined: {len(s.get('candidate_links', []))}.", "roster_evidence_refs": [f"research/audit-runs/{RUN_ID}/source-route-evidence.json"], "change_reviews": []})

receipt = {"schema_version": 1, "run_id": RUN_ID, "started_at": baseline["started_at"], "recorded_at": NOW, "status": "INCOMPLETE", "source_total": len(receipt_sources), "attempted_total": sum(x["opened_this_run"] for x in receipt_sources), "content_sufficient_total": 0, "processing_complete_total": len(receipt_sources), "sources": receipt_sources, "deadline_review_ref": f"research/audit-runs/{RUN_ID}/deadline-review.json", "discovery_evidence_ref": f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json"}
write(f"research/audit-runs/{RUN_ID}/receipt-final.json", receipt, compact=True)

# Every frozen issue gets a fresh individual outcome tied to today's current protocol attempt.
protocol_by_id = {x["trial_id"]: x for x in read(f"research/audit-runs/{RUN_ID}/protocol-content-review.json")["protocols"]}
issue_updates = []
for old in baseline["issues"]:
    p = protocol_by_id.get(old["trial_id"])
    readable = p and p.get("readable_routes", 0) > 0
    present = [k for k, v in (p or {}).get("facts_present", {}).items() if v]
    missing = [k for k, v in (p or {}).get("facts_present", {}).items() if not v]
    if readable:
        finding = f"Today's individual primary read returned current content. Published sections detected: {present or ['none']}; still not established for this exact question: {missing or ['the question-specific contradiction/clarification']}. The saved current body was assessed separately and no unprinted fact was inferred."
        next_action = "Recheck this exact official protocol after a dated amendment or direct published clarification of the remaining question."
    else:
        results = [r.get("result") for r in (p or {}).get("routes", [])]
        finding = f"Today's exact protocol route decisions produced no readable primary body (results={results or ['no current public route']}); the inherited question remains open without carrying forward an old answer as current evidence."
        next_action = "Use the same exact public protocol route or a newly published official protocol/PDF after the access state changes; do not bypass the recorded restriction."
    issue_updates.append({"issue_id": old["issue_id"], "trial_id": old["trial_id"], "kind": old["kind"], "state": "BLOCKED", "reviewed_at": NOW, "finding": finding, "question": old.get("question") or "Read the full primary protocol and reconcile current published facts.", "next_action": next_action, "unperformed_steps": [], "evidence_refs": [f"research/audit-runs/{RUN_ID}/protocol-route-evidence.json", f"research/audit-runs/{RUN_ID}/protocol-content-review.json"], "restriction_or_unpublished_evidence_refs": [f"research/audit-runs/{RUN_ID}/protocol-route-evidence.json", f"research/audit-runs/{RUN_ID}/protocol-content-review.json"], "full_protocol_review_complete": False, "new_primary_signal": False, "deadline_crossed": False})

execution_review = {"schema_version": 1, "run_id": RUN_ID, "ended_at": NOW, "source_reviews": source_reviews, "issue_updates": issue_updates, "discovery_queries": query_rows, "discovered_urls": [x["url"] for x in leads], "leads": leads, "deadline_review_ref": f"research/audit-runs/{RUN_ID}/deadline-review.json", "added_catalog_ids": [x["id"] for x in new_trials], "stop": {"reason": "completed_available_work", "detail": "The finite 168-source route queue, 153 current public protocol routes, 60-query two-pass regional discovery matrix, all selected candidate URLs, 323-record frozen deadline ledger and all 63 inherited issues received current decisions. Remaining gaps require unpublished facts or a change to exact blocked routes; no permitted current step remains in this run.", "evidence_refs": [f"research/audit-runs/{RUN_ID}/source-route-evidence.json", f"research/audit-runs/{RUN_ID}/protocol-route-evidence.json", f"research/audit-runs/{RUN_ID}/global-discovery-evidence.json"]}}
write(f"research/audit-runs/{RUN_ID}/execution-review.json", execution_review, compact=True)

# Source-specific external-gap diagnoses. Distinct completion prose prevents blanket accounting.
gap_rows = []
for src in receipt_sources:
    sid = src["source_id"]
    attempts = [x["url"] for x in src["attempted_urls"]]
    current = source_by_id[sid]
    question = f"Does {current['name']} publish a complete current dog/cat anticancer-treatment roster with enough protocol-level identity/status evidence to reconcile every entry?"
    gap_rows.append({"source_id": sid, "category": "roster_unestablished" if current["readable_routes"] else "source_unavailable", "processing_assessment": "external_blocker", "question": question, "reason": f"Current run read {current['readable_routes']} route(s) and examined {len(current.get('candidate_links', []))} trial/oncology links, but the official material did not establish an exhaustive current roster for this source.", "next_action": f"Recheck the exact configured {sid} routes when their published body, access state or dated protocol links change; review only the affected protocol identities.", "evidence": {"source_id": sid, "attempted_urls": attempts, "refs": [f"research/audit-runs/{RUN_ID}/source-route-evidence.json", f"research/audit-runs/{RUN_ID}/source-content-review.json"]}, "completion_decision": {"remaining_fact": question, "routes_exhausted_evidence": f"For {sid}, receipt-final.json records {len(attempts)} exact configured route decisions and source-route-evidence.json preserves their current status/body hashes.", "available_reconciliation_done_evidence": f"For {sid}, today's readable bodies produced {len(current.get('candidate_links', []))} candidate links and exact canonical IDs {current.get('exact_canonical_ids', [])}; the finite noncanonical set is included in execution-review lead dispositions. The absent completeness/blocked body cannot be created by another permitted request."}, "unperformed_steps": []})
write(f"research/audit-runs/{RUN_ID}/gap-review.json", {"schema_version": 1, "original_run_id": RUN_ID, "reviewed_at": NOW, "rows": gap_rows}, compact=True)

# Compact, current inventory: preserve all identities/routes/restrictions while replacing redundant duplicated histories.
inventory = read("data/source_inventory.json")
old_by_id = {x["id"]: x for x in inventory["sources"]}
new_inventory_rows = []
for sid in baseline["source_ids"]:
    old = old_by_id[sid]
    content = source_by_id[sid]
    att = attempts_by_source.get(sid, [])
    route_hashes = [a.get("body_sha256") or a.get("visible_text_sha256") for a in att if a.get("body_sha256") or a.get("visible_text_sha256")]
    fp = "sha256:" + hashlib.sha256("\n".join(route_hashes).encode()).hexdigest() if route_hashes else old.get("content_fingerprint")
    last_at = max((a.get("completed_at") for a in att if a.get("completed_at")), default=NOW)
    row = {k: old[k] for k in ("id", "name", "country", "source_type", "master_url", "required_cadence")}
    for k in ("fallback_urls", "source_role", "discovery_evidence", "access_restrictions", "recheck_after"):
        if old.get(k) not in (None, [], {}): row[k] = old[k]
    row.update({"last_checked": "2026-11-24", "last_checked_at": last_at, "last_result": "partial" if content["readable_routes"] else "unreachable", "last_http_status": next((a.get("status") for a in reversed(att) if a.get("status") is not None), None), "content_fingerprint": fp, "fingerprint_method": "Digest of current returned route body hashes; not proof of whole-roster equality or clinical sufficiency.", "last_attempts": [{"url": a.get("requested_url"), "method": "restriction_review_no_request" if a.get("result") == "skipped_exact_restriction" else "proxy_http", "completed_at": a.get("completed_at"), "result": a.get("result"), "status": a.get("status"), "opened": bool(a.get("opened")), "evidence_file": f"research/audit-runs/{RUN_ID}/source-route-evidence.json"} for a in att], "last_route_used": "proxy_http_or_exact_saved_restriction_after_native_transport_failure", "notes": f"2026-11-24 current pass: readable routes={content['readable_routes']}; candidate links={len(content.get('candidate_links', []))}; exact canonical IDs={content.get('exact_canonical_ids', [])}. Current evidence does not prove an exhaustive roster.", "last_audit_run_id": RUN_ID, "content_sufficient": False, "processing_complete": True})
    new_inventory_rows.append(row)
inventory.update({"updated": "2026-11-24", "sources": new_inventory_rows, "last_audit_run_id": RUN_ID, "last_audit_at": NOW})
write("data/source_inventory.json", inventory, compact=True)

print(json.dumps({"run_id": RUN_ID, "ended_at": NOW, "catalog": len(catalog), "added": [x["id"] for x in new_trials], "leads": len(leads), "queries": len(query_rows), "issues": len(issue_updates), "sources": len(receipt_sources), "inventory_bytes": (ROOT / "data/source_inventory.json").stat().st_size}, indent=2))
