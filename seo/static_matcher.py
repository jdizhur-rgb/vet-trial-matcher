#!/usr/bin/env python3
"""Build the no-server clinical trial matcher inside the static website."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).resolve().parent / "matcher"

CANCERS = [
    'Acute myeloid leukemia', 'Adrenal tumor', 'Anal sac adenocarcinoma (AGASACA)',
    'B-cell lymphoma', 'Brain tumor / glioma', 'Chemodectoma', 'Chondrosarcoma',
    'Colorectal / rectal cancer', 'Cutaneous epitheliotropic lymphoma', 'Esophageal cancer',
    'Feline injection-site sarcoma', 'Feline mammary carcinoma', 'Fibrosarcoma',
    'Gallbladder carcinoma', 'Gastric / stomach cancer', 'Gastrointestinal stromal tumor (GIST)',
    'Hemangiosarcoma', 'Hepatocellular carcinoma', 'Histiocytic sarcoma', 'Insulinoma',
    'Intestinal carcinoma', 'Leiomyosarcoma', 'Liposarcoma', 'Lymphoma — other',
    'Mammary carcinoma', 'Mammary tumor — other', 'Mast cell tumor', 'Melanoma — other',
    'Multiple myeloma / plasma cell cancer', 'Nasal tumor / nasal cancer',
    'Ocular melanoma / iris melanocytic tumor', 'Oral melanoma', 'Oral squamous cell carcinoma',
    'Oral tumor — other', 'Osteosarcoma', 'Other bone tumor', 'Other liver tumor',
    'Other sarcoma', 'Other solid tumor', 'Pancreatic carcinoma',
    'Peripheral nerve sheath tumor', 'Primary lung tumor', 'Prostate cancer', 'Renal tumor',
    'Rhabdomyosarcoma', 'Salivary gland cancer', 'Sinonasal carcinoma', 'Soft tissue sarcoma',
    'Spindle cell sarcoma', 'Squamous cell carcinoma', 'Squamous cell carcinoma — other',
    'T-cell lymphoma', 'Thymoma / thymic tumor', 'Thyroid carcinoma',
    'Thyroid tumor / carcinoma', 'Urothelial / transitional cell carcinoma',
    'Urothelial carcinoma', 'Cancer — any type', 'Other / not sure',
    "My cancer type isn't listed",
]


def options(values: list[str]) -> str:
    return ''.join(f'<option value="{g.esc(value)}">{g.esc(value)}</option>' for value in values)


def select(name: str, label: str, values: list[str], *, row: str = '', help_text: str = '') -> str:
    help_html = f'<small>{g.esc(help_text)}</small>' if help_text else ''
    return f'<label class="field {row}" data-field="{name}"><span>{g.esc(label)}</span><select name="{name}">{options(values)}</select>{help_html}</label>'


def sanitize_trial(row: dict) -> dict:
    public_keys = {
        'id', 'title', 'center', 'country', 'species', 'cancers', 'broad_disease_families',
        'study_type', 'status', 'status_confidence', 'requires', 'excludes', 'intervention',
        'notes', 'funding', 'contacts', 'contact', 'sites', 'registry_url', 'url', 'verified',
        'early_phase', 'special_requirement', 'owner_prescreen_required',
        'broad_disease_fallback', 'requires_site_screening', 'freshness_unresolved',
    }
    return {key: row[key] for key in public_keys if key in row}


def build(root: Path) -> None:
    rows = json.loads((ROOT / 'data' / 'trials_base.json').read_text(encoding='utf-8'))
    rows = [
        sanitize_trial(row) for row in rows
        if row.get('available_for_matching', True)
        and row.get('status_confidence') in {'current', 'confirmed_current'}
        and row.get('study_type', 'treatment') in {'treatment', 'other_treatment_access'}
    ]
    countries = sorted({str(row.get('country') or 'USA') for row in rows}, key=lambda x: (x != 'USA', x))

    pet = select('species', 'Species', ['Dog', 'Cat']) + select(
        'sex', 'Sex', ["I don't know", 'Female — spayed', 'Female — intact', 'Male — neutered', 'Male — intact']
    )
    diagnosis = select(
        'diagnosis_status', 'How certain is the diagnosis?',
        ['Confirmed by pathology/cytology', 'Suspected / not confirmed', "I don't know"]
    ) + select('cancer', 'Cancer type', CANCERS)
    disease = ''.join([
        select('tumor_status', 'Current tumor status', ['Tumor still present / measurable', 'Completely removed — clean margins', 'Removed — incomplete/dirty margins', 'Removed — margins unknown', 'Local recurrence', 'No evidence of disease (NED)', "I don't know"], row='solid-only'),
        select('metastasis', 'Metastases', ['No known metastases', 'Confirmed metastases', 'Suspected / staging incomplete', "I don't know"], row='solid-only'),
        select('localized', 'Has your veterinarian said the disease is localized?', ['Yes', 'No', "I don't know"], row='solid-only'),
        select('brain_present', 'Is the brain tumor currently present on imaging?', ['Yes', 'No visible tumor', "I don't know"], row='brain-only'),
        select('lymphoma_type', 'Lymphoma type', ['B-cell', 'T-cell', 'Other', "I don't know"], row='lymphoma-only'),
        select('lymphoma_response', 'Response/status', ['Newly diagnosed / untreated', 'Complete remission', 'Partial response', 'Progression during treatment', 'First relapse after remission', 'More than one relapse', "I don't know"], row='lymphoma-only'),
        select('leukemia_status', 'Leukemia status', ['Newly diagnosed / untreated', 'Responding to treatment / remission', 'Relapsed', 'Refractory / progressive', "I don't know"], row='aml-only'),
        select('mct_grade', 'Mast cell tumor grade', ['Low grade / Kiupel low', 'High grade / Kiupel high', 'Patnaik grade 1', 'Patnaik grade 2', 'Patnaik grade 3', "I don't know"], row='mct-only'),
        select('node_status', 'Regional lymph node status', ['Negative', 'Positive', 'Not sampled/tested', "I don't know"], row='mct-only'),
        select('osa_location', 'Primary osteosarcoma location', ['Appendicular — limb bone', 'Axial — skull, spine, rib, or pelvis', 'Other', "I don't know"], row='osa-only'),
        select('hsa_site', 'Primary hemangiosarcoma site', ['Spleen', 'Heart / right atrium', 'Other', "I don't know"], row='hsa-only'),
        select('standard_therapy_unavailable', 'Is standard anticancer treatment no longer appropriate or not feasible?', ['Yes', 'No', "I don't know"], row='protocol protocol-standard'),
        select('large_inoperable_or_rt_preferred', 'For a large tumor: is it inoperable, or is radiotherapy being chosen instead of surgery?', ['Yes', 'No', "I don't know"], row='protocol protocol-large'),
        select('surgery_or_rt_not_possible', 'Are curative surgery and radiotherapy no longer possible for this tumor?', ['Yes', 'No', "I don't know"], row='protocol protocol-no-local'),
        select('ct_and_current_biopsy', 'Can current CT imaging and a current tumor biopsy be provided/performed?', ['Yes', 'No', "I don't know"], row='protocol protocol-ct-biopsy'),
    ])
    treatment = ''.join([
        select('surgery', 'Surgery', ['No', 'Yes', "I don't know"]),
        select('prior_procedure', 'Cancer surgery performed', ['Other', 'Amputation', 'Limb-sparing surgery', 'Splenectomy', "I don't know"], row='procedure-only'),
        select('chemo', 'Chemotherapy', ['Never', 'Currently receiving', 'Previously received', "I don't know"]),
        select('immunotherapy_history', 'Prior or current cancer immunotherapy', ['Never', 'Currently receiving', 'Previously received', "I don't know"]),
        select('radiation', 'Radiation to this tumor', ['Never', 'Previously received', 'Currently receiving', "I don't know"]),
        select('steroids', 'Prednisone / other corticosteroids', ['Never / no', 'Prescribed but NOT started', 'Currently taking', 'Previously took', "I don't know"], row='steroids-only'),
        select('immunosuppressive', 'Other immunosuppressive medication', ['No', 'Yes', "I don't know"], row='immunosuppressive-only'),
    ])
    modality_checks = ''.join(
        f'<label class="check"><input type="checkbox" name="prefs" value="{g.esc(value)}" checked><span>{g.esc(value)}</span></label>'
        for value in ['Chemotherapy', 'Radiation', 'Surgery', 'Immunotherapy', 'Targeted therapy', 'Experimental drug']
    )

    body = f'''<article class="matcher-page">
<p class="eyebrow">Free clinical trial search for dogs and cats</p><h1>Vet Cancer Trial Finder</h1>
<p class="lead">Answer what you know. It is completely fine to choose <strong>I don’t know</strong>.</p>
<div class="matcher-notice">This finder identifies potentially relevant cancer treatment options. It does not determine eligibility. Final decisions belong to the treating or research team.</div>
<details class="before"><summary>Before you start</summary><p>Helpful records, if you have them: pathology or cytology, surgery report, recent imaging, bloodwork, and treatment dates. You do not need all of these to search.</p></details>
<form id="matcher-form">
<fieldset><legend>1. Your pet</legend><div class="form-grid">{pet}<label class="field"><span>Age</span><span class="input-line"><input type="checkbox" name="age_known" checked> I know the age</span><input type="number" name="age" min="0" max="30" step="0.5" value="8"></label><label class="field"><span>Weight</span><span class="input-line"><input type="checkbox" name="weight_known"> I know the weight</span><span class="split"><input type="number" name="weight" min="0.1" max="250" step="0.1" value="44"><select name="weight_unit"><option>lb</option><option>kg</option></select></span></label><label class="field wide"><span>Country / region</span><select name="country">{options(['Europe — all countries'] + countries)}</select></label></div></fieldset>
<fieldset><legend>2. Diagnosis</legend><div class="form-grid">{diagnosis}<label class="field wide unlisted-only"><span>Diagnosis as written in the pathology report</span><input type="text" name="unlisted_diagnosis"></label></div></fieldset>
<fieldset><legend>3. Current disease</legend><p class="browse-note" hidden></p><div class="form-grid">{disease}</div></fieldset>
<fieldset class="specific-only"><legend>4. Treatment</legend><div class="form-grid">{treatment}</div></fieldset>
<fieldset><legend>5. Treatment options</legend><p>Select all that you would consider.</p><div class="checks">{modality_checks}</div>{select('radiation_affordability', 'If radiation is required by a study', ['Would consider radiation', 'Would consider it if trial-funded', 'Would not consider radiation', "I don't know"], row='radiation-plan-only')}</fieldset>
<button class="matcher-submit" type="submit">Find potential trials</button>
</form><section id="matcher-results" class="matcher-results" aria-live="polite"></section>
<p class="urgent"><strong>Urgent symptoms come first.</strong> Difficulty breathing, collapse, uncontrolled bleeding, severe pain, or another emergency should be assessed by a veterinarian immediately.</p>
</article><link rel="stylesheet" href="./matcher.css"><script>window.MATCHER_DATA_URL='./trials.json';</script><script src="./matcher.js" defer></script>'''

    destination = root / 'matcher'
    destination.mkdir(parents=True, exist_ok=True)
    page = g.page(
        'Vet Cancer Trial Finder | Find Clinical Trials for Dogs and Cats',
        'Free searchable matcher for current veterinary cancer clinical trials and treatment programs for dogs and cats.',
        body, f'{SITE}/matcher/'
    )
    (destination / 'index.html').write_text(page, encoding='utf-8')
    (destination / 'trials.json').write_text(json.dumps(rows, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    shutil.copy2(SOURCE / 'matcher.js', destination / 'matcher.js')
    shutil.copy2(SOURCE / 'matcher.css', destination / 'matcher.css')
