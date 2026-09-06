import json
from pathlib import Path

p = Path('data/trial_updates.json')
doc = json.loads(p.read_text(encoding='utf-8'))
upserts = doc.setdefault('upsert', [])
by_id = {x['id']: x for x in upserts}

new = [
  {
    "id": "aurelius-lytix-bcell-lymphoma",
    "title": "Aurelius/Lytix oncolytic peptide plus adoptive T-cell immunotherapy for canine B-cell lymphoma",
    "center": "Aurelius Biotherapeutics",
    "country": "USA",
    "state": "Washington",
    "species": "Dog",
    "cancers": ["B-cell lymphoma"],
    "status": "Actively recruiting — confirmed on Aurelius current pilot-study page",
    "url": "https://aureliusbio.com/",
    "contacts": "Theresa Westfall, DVM — info@aureliusbio.com; (360) 961-3529 or (360) 734-0720",
    "funding": "Fully funded; Aurelius states there is no additional expense to owners for the trial.",
    "requires": {"confirmed": True, "active_treatment_target": True, "previously_untreated": True},
    "excludes": {"prior_cancer_treatment": True},
    "notes": "Initial pilot study combining an oncolytic peptide with adoptive T-cell immunotherapy for previously untreated stage 3–5(a) canine B-cell lymphoma. Almost all study treatment is performed in Bellingham, Washington; initial treatment requires about three days, followed by at least two later visits approximately a month afterward.",
    "verified": "2026-09-06",
    "study_type": "treatment",
    "available_for_matching": True,
    "status_confidence": "confirmed_current",
    "owner_prescreen_required": True
  },
  {
    "id": "umn-trike-sarcoma-2026",
    "title": "TriKE immunotherapy plus hypofractionated radiation for canine sarcoma",
    "center": "University of Minnesota College of Veterinary Medicine",
    "country": "USA",
    "state": "Minnesota",
    "species": "Dog",
    "cancers": ["Soft tissue sarcoma", "Other sarcoma"],
    "status": "Open and enrolling — confirmed on University of Minnesota current clinical-trial page",
    "url": "https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/trike-new",
    "contacts": "Amber Winter, CVT — 612-624-1352; contact through the official University of Minnesota study page",
    "funding": "Once enrolled, the study covers participation costs including blood/urine testing, imaging, radiation planning and treatment, TriKE immunotherapy and follow-up exams. Initial staging is also covered if performed at the Veterinary Medical Center.",
    "requires": {"confirmed": True, "active_treatment_target": True, "measurable": True, "min_tumor_cm": 2, "min_weight_kg": 7, "no_metastasis": True},
    "excludes": {"current_chemo": True, "current_radiation": True, "prior_immunotherapy": True},
    "notes": "Dose-finding treatment study of TriKE immunotherapy with hypofractionated radiation in companion dogs with sarcoma. Local/regional lymph-node involvement may be accepted at investigator discretion; prior chemotherapy or radiation may be allowed after washout.",
    "verified": "2026-09-06",
    "study_type": "treatment",
    "available_for_matching": True,
    "status_confidence": "confirmed_current",
    "owner_prescreen_required": True
  },
  {
    "id": "purdue-aks619d-solid-tumors",
    "title": "AKS-619d PD-L1-directed Ambifect immunotherapy for canine cancers",
    "center": "Purdue University Veterinary Hospital",
    "country": "USA",
    "state": "Indiana",
    "species": "Dog",
    "cancers": ["T-cell lymphoma", "Hepatocellular carcinoma", "Mammary carcinoma", "Squamous cell carcinoma", "Soft tissue sarcoma", "Melanoma — other", "Oral melanoma", "Osteosarcoma", "Mast cell tumor"],
    "status": "Ongoing proof-of-concept study in client-owned dogs — Purdue Oncology screening confirmed in current sponsor disclosures",
    "url": "https://www.akstonbio.com/in-the-news/akston-pioneers-a-new-generation-of-cancer-therapy-for-dogs-in-clinical-trial-launch/",
    "contacts": "Purdue University Veterinary Hospital Oncology Service — owner prescreening through Purdue Oncology",
    "funding": "Confirm study-covered and owner-paid costs with Purdue Oncology.",
    "requires": {"confirmed_or_suspected": True, "active_treatment_target": True},
    "excludes": {"bladder_cancer": True},
    "notes": "Independent Purdue proof-of-concept study of intramuscular AKS-619d, designed to induce antibodies targeting PD-L1. Public sponsor disclosures state client-owned dogs presenting to Purdue Oncology are screened for eligibility. The solid-tumor study excludes bladder cancer to avoid competing with the separate AKS-701d urothelial-carcinoma study.",
    "verified": "2026-09-06",
    "study_type": "treatment",
    "available_for_matching": True,
    "status_confidence": "confirmed_current",
    "owner_prescreen_required": True
  }
]

# Known older duplicate ID for the same UMN TriKE protocol is explicitly suppressed.
deletes = doc.setdefault('delete', [])
if 'umn-trike-sarcoma' not in deletes:
    deletes.append('umn-trike-sarcoma')

for row in new:
    by_id[row['id']] = row

doc['upsert'] = list(by_id.values())
p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Promoted', len(new), 'verified company/developer-sourced treatment opportunities')
