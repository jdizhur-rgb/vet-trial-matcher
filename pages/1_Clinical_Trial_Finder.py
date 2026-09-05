# EU cancer-by-cancer gap audit completed 2026-09-04: all UI cancer categories rechecked; no unverified lead promoted to matching.
import streamlit as st
import streamlit.components.v1 as components

CANCER_ALIASES = {
    # UI labels and protocol labels are not always identical. Keep these mappings
    # deliberately conservative: aliases mean the same disease family, not merely
    # a vaguely related cancer.
    'B-cell lymphoma': ['Lymphoma', 'Lymphoma — other'],
    'T-cell lymphoma': ['Lymphoma', 'Lymphoma — other', 'Enteropathy-associated T-cell lymphoma'],
    'Lymphoma — other': ['Lymphoma', 'Gastrointestinal lymphoma', 'Large cell lymphoma'],
    'Brain tumor / glioma': ['Brain tumor', 'Glioma'],
    'Feline mammary carcinoma': ['Mammary carcinoma', 'Mammary tumor'],
    'Mammary carcinoma': ['Mammary tumor'],
    'Mammary tumor — other': ['Mammary tumor'],
    'Urothelial / transitional cell carcinoma': ['Urothelial carcinoma', 'Transitional cell carcinoma'],
    'Urothelial carcinoma': ['Urothelial / transitional cell carcinoma', 'Transitional cell carcinoma', 'Bladder cancer'],
    'Thyroid tumor / carcinoma': ['Thyroid carcinoma'],
    'Thyroid carcinoma': ['Thyroid tumor / carcinoma'],
    'Hepatocellular carcinoma': ['Hepatic carcinoma'],
    'Primary lung tumor': ['Pulmonary carcinoma'],
    'Oral squamous cell carcinoma': ['Feline oral SCC'],
    'Squamous cell carcinoma — other': ['Squamous cell carcinoma'],
    'Oral tumor — other': ['Oral tumor'],
    'Ocular melanoma / iris melanocytic tumor': ['Ocular melanoma', 'Iris melanocytic tumor'],
    'Chemodectoma': ['Aortic body tumor', 'Aortic body tumors', 'Heart-base tumor', 'Heart base tumor', 'Paraganglioma', 'Non-chromaffin paraganglioma'],
}

LYMPHOMA_CANCERS = {'B-cell lymphoma', 'T-cell lymphoma', 'Lymphoma — other'}

st.set_page_config(page_title='Vet Cancer Trial Finder — Beta', page_icon='🐾', layout='centered')


def _render_result_save_controls(matches):
    import io, json
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch

    lines = ["Clinical Trial Finder Results"]
    for confidence, tr, reasons, unknown in matches:
        lines += ["", confidence, tr.get("center", ""), tr.get("title", "")]
        if reasons:
            lines.append("Why: " + "; ".join(str(x) for x in reasons) + ".")
        if unknown:
            lines.append("Confirm: " + "; ".join(dict.fromkeys(str(x) for x in unknown)) + ".")
        lines.append("Contact: " + tr.get("contacts", tr.get("contact", "Contact the study team through the official study page")))
        if tr.get("sites"):
            lines.append("Participating sites: " + "; ".join(f"{x['hospital']} — {x['city']}, {x['state']}" for x in tr["sites"]))
        if tr.get("url"):
            lines.append("Study page: " + tr["url"])
        lines.append("What the study says: " + tr.get("notes", ""))
        lines.append("Status: " + tr.get("status", "") + " · Last verified: " + tr.get("verified", "date not recorded"))
    lines += ["", "Recruitment and eligibility can change; confirm current status with the study team."]
    report_text = "\n".join(lines)

    cols = st.columns(2, gap="small")
    payload = json.dumps(report_text)
    with cols[0]:
        st.html(f"""<button id="copy-results-native" style="width:100%;padding:9px 12px;border:1px solid #d8d3cf;border-radius:9px;background:white;font-weight:600;color:#4b4642;cursor:pointer">📋 Copy results</button><div id="copy-msg" style="font:12px Arial;color:#55745d;margin-top:4px;min-height:14px"></div><script>(()=>{{const text={payload};const b=document.getElementById('copy-results-native'),m=document.getElementById('copy-msg');b.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(text);m.textContent='Results copied.';return}}catch(e){{}}const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{{document.execCommand('copy');m.textContent='Results copied.'}}catch(e){{m.textContent='Copy is blocked by this browser.'}}ta.remove()}})}})();</script>""", unsafe_allow_javascript=True)

    buf = io.BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=.55*inch, leftMargin=.55*inch, topMargin=.55*inch, bottomMargin=.55*inch)
    story = []
    for i, line in enumerate(lines):
        if not line:
            story.append(Spacer(1, 8))
        else:
            style = styles["Title"] if i == 0 else styles["BodyText"]
            safe = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            story.append(Paragraph(safe, style))
            story.append(Spacer(1, 4))
    doc.build(story)
    with cols[1]:
        st.download_button("📄 Save as PDF", data=buf.getvalue(), file_name="clinical_trial_results.pdf", mime="application/pdf", use_container_width=True, on_click="ignore")


# Catalog data is stored separately from the Streamlit page.
from pathlib import Path as _Path
import json as _json

def _load_trials():
    _root = _Path(__file__).resolve().parents[1]
    with (_root / "data" / "trials_base.json").open(encoding="utf-8") as _fh:
        _base = _json.load(_fh)
    _by_id = {t["id"]: t for t in _base}
    _updates_path = _root / "data" / "trial_updates.json"
    if _updates_path.exists():
        with _updates_path.open(encoding="utf-8") as _fh:
            _doc = _json.load(_fh)
        for _trial_id in _doc.get("delete", []):
            _by_id.pop(_trial_id, None)
        for _patch in _doc.get("upsert", []):
            _trial_id = _patch["id"]
            if _trial_id in _by_id:
                _by_id[_trial_id].update(_patch)
            else:
                _by_id[_trial_id] = _patch
    return list(_by_id.values())

TRIALS = _load_trials()

# 2026-09-03 private-referral / institutional-registry / local-language deep pass


# 2026-09-03 regulatory / CRO / sponsor-development pass

CANCERS = ['Acute myeloid leukemia', 'Adrenal tumor', 'Anal sac adenocarcinoma (AGASACA)', 'B-cell lymphoma', 'Brain tumor / glioma', 'Chemodectoma', 'Chondrosarcoma', 'Colorectal / rectal cancer', 'Cutaneous epitheliotropic lymphoma', 'Esophageal cancer', 'Feline injection-site sarcoma', 'Feline mammary carcinoma', 'Fibrosarcoma', 'Gallbladder carcinoma', 'Gastric / stomach cancer', 'Gastrointestinal stromal tumor (GIST)', 'Hemangiosarcoma', 'Hepatocellular carcinoma', 'Histiocytic sarcoma', 'Insulinoma', 'Intestinal carcinoma', 'Leiomyosarcoma', 'Liposarcoma', 'Lymphoma — other', 'Mammary carcinoma', 'Mammary tumor — other', 'Mast cell tumor', 'Melanoma — other', 'Multiple myeloma / plasma cell cancer', 'Nasal tumor / nasal cancer', 'Ocular melanoma / iris melanocytic tumor', 'Oral melanoma', 'Oral squamous cell carcinoma', 'Oral tumor — other', 'Osteosarcoma', 'Other bone tumor', 'Other liver tumor', 'Other sarcoma', 'Other solid tumor', 'Pancreatic carcinoma', 'Peripheral nerve sheath tumor', 'Primary lung tumor', 'Prostate cancer', 'Renal tumor', 'Rhabdomyosarcoma', 'Salivary gland cancer', 'Sinonasal carcinoma', 'Soft tissue sarcoma', 'Spindle cell sarcoma', 'Squamous cell carcinoma', 'Squamous cell carcinoma — other', 'T-cell lymphoma', 'Thymoma / thymic tumor', 'Thyroid carcinoma', 'Thyroid tumor / carcinoma', 'Urothelial / transitional cell carcinoma', 'Urothelial carcinoma', 'Cancer — any type', 'Other / not sure', "My cancer type isn't listed"]
DIAGNOSIS_FAMILIES = {
    'Gastric / stomach cancer': {'solid_tumor','carcinoma'},
    'Colorectal / rectal cancer': {'solid_tumor','carcinoma'},
    'Salivary gland cancer': {'solid_tumor','carcinoma'},
    'Esophageal cancer': {'solid_tumor','carcinoma'},
    'Thymoma / thymic tumor': {'solid_tumor'},
    'Gastrointestinal stromal tumor (GIST)': {'solid_tumor','sarcoma'},
    'Peripheral nerve sheath tumor': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},
    'Leiomyosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},
    'Fibrosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},
    'Liposarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},
    'Rhabdomyosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},
    'Chondrosarcoma': {'solid_tumor','sarcoma'},
    'Nasal tumor / nasal cancer': {'solid_tumor','nasal_tumor'},
    'Multiple myeloma / plasma cell cancer': {'hematologic'},
}
UNLISTED_CANCER = "My cancer type isn't listed"
TREATMENT_OPTIONS = ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug']
UNKNOWN = "I don't know"

# Enrollment-status normalization. Older audited records use 'current'; some
# newer confirmed records use 'confirmed_current'. Both mean the study may be
# considered by the patient-facing matcher. Watch/planned/reconfirmation rows
# remain excluded.
CURRENT_STATUS_CONFIDENCE = {'current', 'confirmed_current'}
def is_current_trial(tr):
    return tr.get('status_confidence') in CURRENT_STATUS_CONFIDENCE

def trial_accepts_diagnosis(tr, diagnosis):
    tc = set(tr.get('cancers', []))

    # First preserve the original exact/alias matching behavior.
    exact = {diagnosis, *CANCER_ALIASES.get(diagnosis, [])}
    if diagnosis == 'Spindle cell sarcoma':
        exact.add('Soft tissue sarcoma')

    if exact.intersection(tc):
        return True, False

    # Broad-family matching is only a fallback for diagnoses that
    # explicitly have a taxonomy-family mapping. Established diagnoses
    # keep the original exact/alias semantics and must not automatically
    # match generic basket / "all tumors" studies.
    fam = DIAGNOSIS_FAMILIES.get(diagnosis)
    if not fam:
        return False, False

    broad = set(tr.get('broad_disease_families', []))

    if 'all_tumors' in broad or 'Cancer — any type' in tc:
        return True, True

    if fam.intersection(broad):
        return True, True

    return False, False

st.markdown('''
<style>
h1 { font-size: 2.15rem !important; line-height: 1.08 !important; }
h2 { font-size: 1.55rem !important; line-height: 1.18 !important; margin-top: 1.35rem !important; }
h3 { font-size: 1.30rem !important; line-height: 1.22 !important; }
label, [data-testid="stWidgetLabel"] p {
    font-size: 1.08rem !important;
    line-height: 1.35 !important;
}
[data-baseweb="select"] div,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    font-size: 1.05rem !important;
}
</style>
''', unsafe_allow_html=True)

st.title('🐾 Vet Cancer Trial Finder')
st.markdown('**Beta prototype.** Answer what you know. It is completely fine to choose **I don’t know**.')
st.info('This tool screens for clinical trials that may be worth contacting. It does not determine eligibility and does not replace your veterinarian or oncologist.')

with st.expander('Before you start', expanded=False):
    st.write('Helpful records, if you have them: pathology/cytology report, surgery report, recent imaging/staging, bloodwork, and names/dates of cancer treatments. You do not need all of these to search.')

st.header('1. Your pet')
c1, c2 = st.columns(2)
with c1:
    species = st.selectbox('Species', ['Dog','Cat'])
    age_known = st.checkbox('I know the age', value=True)
    age = st.number_input('Age (years)', 0.0, 30.0, 8.0, 0.5, disabled=not age_known)
with c2:
    weight_known = st.checkbox('I know the weight')
    weight_unit = st.radio('Weight unit', ['lb', 'kg'], horizontal=True, disabled=not weight_known)
    if weight_unit == 'kg':
        weight_value = st.number_input('Weight (kg)', 0.1, 113.5, 20.0, 0.1, disabled=not weight_known)
        weight_kg = weight_value if weight_known else None
        weight_lb = weight_value * 2.2046226218 if weight_known else None
    else:
        weight_value = st.number_input('Weight (lb)', 0.2, 250.0, 44.0, 0.5, disabled=not weight_known)
        weight_lb = weight_value if weight_known else None
        weight_kg = weight_value / 2.2046226218 if weight_known else None
    sex = st.selectbox('Sex', [UNKNOWN,'Female — spayed','Female — intact','Male — neutered','Male — intact'])

trial_countries = sorted({t.get('country', 'USA') for t in TRIALS}, key=lambda x: (x != 'USA', x))
EUROPE_COUNTRIES = {
    'UK', 'United Kingdom', 'France', 'Italy', 'Portugal', 'Switzerland',
    'Netherlands', 'The Netherlands', 'Belgium', 'Sweden', 'Slovenia',
    'Spain', 'Germany', 'Cyprus', 'Austria', 'Poland', 'Norway',
    'Denmark', 'Finland', 'Ireland', 'Czech Republic', 'Czechia',
    'Hungary', 'Greece', 'Romania', 'Croatia', 'Estonia', 'Latvia',
    'Lithuania', 'Luxembourg', 'Iceland'
}
country_options = ['Europe — all countries'] + trial_countries
country = st.selectbox('Country / region', country_options)

def country_matches(trial_country, selected_country):
    if selected_country == 'Europe — all countries':
        return trial_country in EUROPE_COUNTRIES
    return trial_country == selected_country

st.header('2. Diagnosis')
diagnosis_status = st.selectbox('How certain is the diagnosis?', ['Confirmed by pathology/cytology','Suspected / not confirmed',UNKNOWN])
cancer = st.selectbox('Cancer type', CANCERS)
unlisted_mode = cancer == UNLISTED_CANCER
unlisted_diagnosis = st.text_input('Enter the diagnosis as written in the pathology report, if known') if unlisted_mode else ''

# Build the owner form from criteria that can actually affect matching for this
# species/disease. Irrelevant disease-status rows stay visible but disabled so
# the form does not jump around when the cancer type changes.
accepted_for_form = {cancer, *CANCER_ALIASES.get(cancer, [])}
_form_trials = []
for _tr in TRIALS:
    if not _tr.get('available_for_matching', True) or not is_current_trial(_tr):
        continue
    if _tr.get('study_type', 'treatment') != 'treatment' or species not in str(_tr.get('species', '')).split('/'):
        continue
    if not country_matches(_tr.get('country', 'USA'), country):
        continue
    # 'Cancer — any type' selected by the owner is a wildcard: do not filter by diagnosis.
    # A trial-side 'Cancer — any type' is likewise a basket-trial wildcard.
    if cancer == 'Cancer — any type' or (unlisted_mode and ('all_tumors' in _tr.get('broad_disease_families', []) or 'Cancer — any type' in _tr.get('cancers', []))) or (not unlisted_mode and trial_accepts_diagnosis(_tr, cancer)[0]):
        _form_trials.append(_tr)
_form_req_keys = {k for t in _form_trials for k in t.get('requires', {})}
_form_exc_keys = {k for t in _form_trials for k in t.get('excludes', {})}

st.header('3. Current disease')
hematologic = cancer in (LYMPHOMA_CANCERS | {'Cutaneous epitheliotropic lymphoma', 'Acute myeloid leukemia'})
brain_tumor = cancer == 'Brain tumor / glioma'
any_cancer_browse = cancer == 'Cancer — any type'

if any_cancer_browse or unlisted_mode:
    st.caption('Browse mode: disease-specific eligibility is not used until a cancer type is selected.' if any_cancer_browse else 'Unlisted diagnosis: only genuinely all-tumor treatment programs will be shown for investigator review.')
    tumor_status = metastasis = localized = UNKNOWN
elif hematologic:
    st.selectbox('Current tumor status', ['Not applicable'], disabled=True, key='na_tumor_status')
    st.selectbox('Metastases', ['Not applicable'], disabled=True, key='na_metastases')
    st.selectbox('Has your veterinarian said the disease is localized?', ['Not applicable'], disabled=True, key='na_localized')
    tumor_status = metastasis = localized = UNKNOWN
elif brain_tumor:
    brain_present = st.selectbox('Is the brain tumor currently present on imaging?', ['Yes','No visible tumor',UNKNOWN])
    tumor_status = 'Tumor still present / measurable' if brain_present == 'Yes' else ('No evidence of disease (NED)' if brain_present == 'No visible tumor' else UNKNOWN)
    st.selectbox('Metastases', ['Not applicable'], disabled=True, key='na_brain_metastases')
    st.selectbox('Has your veterinarian said the disease is localized?', ['Not applicable'], disabled=True, key='na_brain_localized')
    metastasis = localized = UNKNOWN
else:
    # Solid tumors: always collect the core disease-state facts. They are
    # clinically meaningful across solid-tumor oncology and frequently determine
    # trial eligibility even when a public trial page has incomplete metadata.
    # Disabling these fields based on the currently selected trial subset caused
    # valid cancers (for example soft-tissue sarcoma) to lose essential answers.
    tumor_status = st.selectbox('Current tumor status', ['Tumor still present / measurable','Completely removed — clean margins','Removed — incomplete/dirty margins','Removed — margins unknown','Local recurrence','No evidence of disease (NED)',UNKNOWN])
    metastasis = st.selectbox('Metastases', ['No known metastases','Confirmed metastases','Suspected / staging incomplete',UNKNOWN])
    localized = st.selectbox('Has your veterinarian said the disease is localized?', ['Yes','No',UNKNOWN])

if cancer in LYMPHOMA_CANCERS or cancer == 'Cutaneous epitheliotropic lymphoma':
    if cancer == 'Cutaneous epitheliotropic lymphoma':
        lymphoma_type = 'T-cell'
    else:
        default_lymphoma_type = {'B-cell lymphoma': 0, 'T-cell lymphoma': 1, 'Lymphoma — other': 2}[cancer]
        lymphoma_type = st.selectbox('Lymphoma type', ['B-cell','T-cell','Other',UNKNOWN], index=default_lymphoma_type)
    lymphoma_response = st.selectbox('Response/status', ['Newly diagnosed / untreated','Complete remission','Partial response','Progression during treatment','First relapse after remission','More than one relapse',UNKNOWN])
    if lymphoma_response in ['Newly diagnosed / untreated','Partial response','Progression during treatment','First relapse after remission','More than one relapse']:
        tumor_status = 'Tumor still present / measurable'
    elif lymphoma_response == 'Complete remission':
        tumor_status = 'No evidence of disease (NED)'
else:
    lymphoma_type = lymphoma_response = UNKNOWN

if cancer == 'Acute myeloid leukemia':
    leukemia_status = st.selectbox('Leukemia status', ['Newly diagnosed / untreated','Responding to treatment / remission','Relapsed','Refractory / progressive',UNKNOWN])
    if leukemia_status in ['Newly diagnosed / untreated','Relapsed','Refractory / progressive']:
        tumor_status = 'Tumor still present / measurable'
    elif leukemia_status == 'Responding to treatment / remission':
        tumor_status = 'No evidence of disease (NED)'
else:
    leukemia_status = UNKNOWN

if cancer == 'Mast cell tumor':
    mct_grade = st.selectbox('Mast cell tumor grade', ['Low grade / Kiupel low','High grade / Kiupel high','Patnaik grade 1','Patnaik grade 2','Patnaik grade 3',UNKNOWN])
    node_status = st.selectbox('Regional lymph node status', ['Negative','Positive','Not sampled/tested',UNKNOWN])
else:
    mct_grade = node_status = UNKNOWN

if cancer == 'Osteosarcoma':
    osa_location = st.selectbox('Primary osteosarcoma location', ['Appendicular — limb bone','Axial — skull, spine, rib, or pelvis','Other',UNKNOWN])
else:
    osa_location = UNKNOWN

if cancer == 'Hemangiosarcoma':
    hsa_site = st.selectbox('Primary hemangiosarcoma site', ['Spleen','Heart / right atrium','Other',UNKNOWN])
else:
    hsa_site = UNKNOWN

# Protocol-specific disease constraints used by broad Zurich basket/local-therapy trials.
standard_therapy_unavailable = st.selectbox(
    'Is standard anticancer treatment no longer appropriate or not feasible?',
    ['Yes','No',UNKNOWN],
    help='Includes cases where standard therapy is no longer indicated, the tumor is inoperable/metastatic, or standard treatment cannot be performed.'
) if (not any_cancer_browse and not unlisted_mode and 'standard_therapy_unavailable' in _form_req_keys) else UNKNOWN

large_inoperable_or_rt_preferred = st.selectbox(
    'For a large tumor: is it inoperable, or is radiotherapy being chosen instead of surgery?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'large_inoperable_or_rt_preferred' in _form_req_keys) else UNKNOWN

surgery_or_rt_not_possible = st.selectbox(
    'Are curative surgery and radiotherapy no longer possible for this tumor?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'surgery_or_rt_not_possible' in _form_req_keys) else UNKNOWN

ct_and_current_biopsy = st.selectbox(
    'Can current CT imaging and a current tumor biopsy be provided/performed?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'ct_and_current_biopsy' in _form_req_keys) else UNKNOWN

st.header('4. Treatment')
# Core cancer-treatment history must not depend on how completely individual
# trial metadata happen to be populated.  Earlier dynamic gating could make the
# entire Treatment section disappear for a diagnosis (for example HS) and then
# prevent the matcher from applying treatment-history exclusions.  Keep the four
# core oncology history questions stable for every specific diagnosis.
_specific_diagnosis = not any_cancer_browse and not unlisted_mode
surgery_relevant = _specific_diagnosis
chemo_relevant = _specific_diagnosis
radiation_relevant = _specific_diagnosis
immunotherapy_relevant = _specific_diagnosis

# Medication questions remain protocol-driven because they are not universal
# cancer-treatment history and otherwise add noise to most searches.
steroids_relevant = _specific_diagnosis and ('current_steroids' in _form_exc_keys or 'steroid_washout_days' in _form_req_keys)
immunosuppressive_relevant = _specific_diagnosis and ('immunosuppressive' in _form_exc_keys)

surgery = st.selectbox('Surgery', ['No','Yes',UNKNOWN]) if surgery_relevant else UNKNOWN
prior_procedure = UNKNOWN
if surgery == 'Yes' and cancer == 'Osteosarcoma':
    prior_procedure = st.selectbox('Osteosarcoma surgery', ['Amputation','Limb-sparing surgery','Other',UNKNOWN])
elif surgery == 'Yes' and cancer == 'Hemangiosarcoma':
    prior_procedure = st.selectbox('Hemangiosarcoma surgery', ['Splenectomy','Other',UNKNOWN])
chemo = st.selectbox('Chemotherapy', ['Never','Currently receiving','Previously received',UNKNOWN]) if chemo_relevant else UNKNOWN
immunotherapy_history = st.selectbox('Prior or current cancer immunotherapy', ['Never','Currently receiving','Previously received',UNKNOWN]) if immunotherapy_relevant else UNKNOWN
radiation = st.selectbox('Radiation to this tumor', ['Never','Previously received','Currently receiving',UNKNOWN]) if radiation_relevant else UNKNOWN
steroids = st.selectbox('Prednisone / other corticosteroids', ['Never / no','Prescribed but NOT started','Currently taking','Previously took',UNKNOWN]) if steroids_relevant else UNKNOWN
immunosuppressive = st.selectbox('Other immunosuppressive medication', ['No','Yes',UNKNOWN]) if immunosuppressive_relevant else UNKNOWN

st.header('5. Treatment options')
prefs = st.multiselect('Select all that you would consider', TREATMENT_OPTIONS, default=TREATMENT_OPTIONS)
if not any_cancer_browse and 'planned_radiation' in _form_req_keys:
    radiation_affordability = st.selectbox('If radiation is relevant', ['Would consider radiation','Would consider it if trial-funded','Would not consider radiation',UNKNOWN])
else:
    radiation_affordability = UNKNOWN

def trial_modalities(tr):
    """Return broad treatment modalities offered by a treatment study.

    Used only for the owner's 'would consider' filter. Multiple selected owner
    preferences are OR choices, never an AND requirement.
    """
    text = ' '.join(str(tr.get(k, '')) for k in ('title','intervention','notes')).lower()
    req = tr.get('requires', {})
    mods = set()
    if req.get('planned_surgery') or req.get('planned_amputation') or req.get('planned_amputation_and_chemo') or any(x in text for x in ('surgery','surgical','mastectom','amputation')):
        mods.add('Surgery')
    if req.get('planned_radiation') or any(x in text for x in ('radiotherapy','radiation','sbrt','flash','lattice','radiosensiti','proton')):
        mods.add('Radiation')
    if req.get('planned_doxorubicin') or req.get('planned_amputation_and_chemo') or any(x in text for x in ('chemotherapy','doxorubicin','carboplatin','lomustine','vinorelbine','toceranib','tigilanol','chemoembol')):
        mods.add('Chemotherapy')
    if any(x in text for x in ('immunotherap','vaccine','car-t','car t','interleukin','il-2','checkpoint','pd-1','pd-l1','oncolytic','tlr agonist','bcg')):
        mods.add('Immunotherapy')
    if any(x in text for x in ('targeted','toceranib','kinase inhibitor','adam-12','versican','antibody','radioimmunotherap','nanobody')):
        mods.add('Targeted therapy')
    # Novel study drugs/local investigational agents count as Experimental drug.
    if any(x in text for x in ('phase i','phase 1','phase ii','phase 2','experimental','investigational','tigilanol','oXC-101'.lower(),'rimcazole','gcn2','oncofap','nebumet','cantrixil')):
        mods.add('Experimental drug')
    # Treatment records with no confidently inferred class should not disappear
    # because metadata are sparse; leave them unclassified for owner prescreen.
    return mods

search_clicked = st.button('Find potential trials', type='primary', use_container_width=True)


if search_clicked:
    matches=[]
    for tr in TRIALS:
        if not tr.get('available_for_matching', True):
            continue
        # A trial with unresolved current enrollment is catalog/reference data,
        # not a patient-facing match. Reconfirm it before turning matching back on.
        if not is_current_trial(tr):
            continue
        if species not in str(tr.get('species', '')).split('/'):
            continue
        if not country_matches(tr.get('country', 'USA'), country):
            continue

        # Owner-facing matcher is treatment-only.
        if tr.get('study_type', 'treatment') != 'treatment':
            continue

        broad_match = False
        if unlisted_mode:
            if 'all_tumors' not in tr.get('broad_disease_families', []) and 'Cancer — any type' not in tr.get('cancers', []):
                continue
            broad_match = True
        elif cancer != 'Cancer — any type':
            accepted, broad_match = trial_accepts_diagnosis(tr, cancer)
            if not accepted:
                continue

        # Treatment preferences are alternatives (OR): a study remains eligible if
        # it offers at least one modality the owner selected. Never require a trial
        # to satisfy every selected chip. Sparse/unclassified legacy records are kept
        # for prescreen rather than silently lost.
        tr_mods = trial_modalities(tr)
        if prefs and tr_mods and not tr_mods.intersection(prefs):
            continue

        # Never surface studies that are explicitly not accepting patients.
        status_text = str(tr.get('status', '')).lower()
        blocked_statuses = ('on hold', 'completed', 'closed enrollment', 'enrollment closed', 'closed for data review', 'suspended', 'past clinical study', 'not accepting', 'paused', 'not on current', 'do not match', 'coming soon', 'not yet independently confirmed', 'enrollment not confirmed', 'reconfirm before matching', 'previously active recruitment', 'sponsor page still lists study', 'current oncology archive listing', 'recent active trial; enrollment must be reconfirmed', 'patients needed; current enrollment should be reconfirmed', 'funded active-study evidence', 'current funded translational research')
        if any(x in status_text for x in blocked_statuses):
            continue

        # Cancer — any type is a browse mode, not an eligibility prescreen.
        # Only universal filters are allowed to exclude a study here: geography,
        # species, treatment preference, age and weight. Disease state, staging,
        # treatment history and protocol-specific requirements are left for review.
        if unlisted_mode:
            req = tr.get('requires', {})
            min_age=req.get('min_age_years'); max_age=req.get('max_age_years')
            if min_age is not None and age_known and age < min_age: continue
            if max_age is not None and age_known and age > max_age: continue
            min_lb=req.get('min_weight_lb')
            if min_lb is None and req.get('min_weight_kg') is not None: min_lb=req['min_weight_kg']*2.2046226218
            if min_lb is not None and weight_known and weight_lb < min_lb: continue
            shown = unlisted_diagnosis.strip() or 'unlisted diagnosis'
            matches.append(('Trial to review — diagnosis requires prescreening', tr, [f'{shown} has not been mapped to a trial disease category'], ['investigator must confirm diagnosis-specific eligibility']))
            continue

        if cancer == 'Cancer — any type':
            req = tr.get('requires', {})
            min_age = req.get('min_age_years')
            max_age = req.get('max_age_years')
            if min_age is not None and age_known and age < min_age:
                continue
            if max_age is not None and age_known and age > max_age:
                continue
            min_lb = req.get('min_weight_lb')
            if min_lb is None and req.get('min_weight_kg') is not None:
                min_lb = req['min_weight_kg'] * 2.2046226218
            max_lb = req.get('max_weight_lb')
            if max_lb is None and req.get('max_weight_kg') is not None:
                max_lb = req['max_weight_kg'] * 2.2046226218
            if min_lb is not None and weight_known and weight_lb < min_lb:
                continue
            if max_lb is not None and weight_known and weight_lb > max_lb:
                continue
            reasons = ['cancer type not specified — study shown for diagnosis review']
            if age_known:
                reasons.append('age is within any published study limit')
            if weight_known:
                reasons.append('weight is within any published study limit')
            unknown = ['disease-specific and protocol-specific eligibility requires prescreening']
            matches.append(('Trial to review — cancer type not specified', tr, reasons, unknown))
            continue

        trial_text = (str(tr.get('title','')) + ' ' + str(tr.get('notes',''))).lower()
        if ('epitheliotropic' in trial_text or 'cutaneous lymphoma' in trial_text) and cancer != 'Cutaneous epitheliotropic lymphoma':
            continue

        req = tr.get('requires', {})
        exc = tr.get('excludes', {})
        reasons=[]; unknown=[]; excluded=False

        # Diagnosis certainty is protocol-specific: most treatment trials require
        # pathology/cytology confirmation, while some screening/observational studies do not.
        if req.get('confirmed'):
            if diagnosis_status == 'Suspected / not confirmed':
                excluded=True
            elif diagnosis_status == UNKNOWN:
                unknown.append('pathology/cytology confirmation of the diagnosis')

        # Never surface studies that are explicitly not accepting patients.
        status_text = str(tr.get('status', '')).lower()
        blocked_statuses = ('on hold', 'completed', 'closed enrollment', 'enrollment closed', 'closed for data review', 'suspended', 'past clinical study', 'not accepting', 'paused', 'not on current', 'do not match', 'coming soon', 'not yet independently confirmed', 'enrollment not confirmed', 'reconfirm before matching', 'previously active recruitment', 'sponsor page still lists study', 'current oncology archive listing', 'recent active trial; enrollment must be reconfirmed', 'patients needed; current enrollment should be reconfirmed', 'funded active-study evidence', 'current funded translational research')
        if any(x in status_text for x in blocked_statuses):
            continue

        if req.get('active_treatment_target'):
            if tumor_status in ['Completely removed — clean margins', 'No evidence of disease (NED)']:
                excluded=True
            elif tumor_status in [UNKNOWN, 'Removed — margins unknown', 'Removed — incomplete/dirty margins']:
                unknown.append('whether an active treatment target is present')
        if req.get('measurable_or_lung_metastasis'):
            if tumor_status not in ['Tumor still present / measurable', 'Local recurrence'] and metastasis == 'No known metastases':
                excluded=True
            elif tumor_status == UNKNOWN or metastasis in [UNKNOWN, 'Suspected / staging incomplete']:
                unknown.append('whether measurable disease or lung metastasis is present')
        if req.get('standard_therapy_unavailable'):
            if standard_therapy_unavailable == 'No':
                excluded=True
            elif standard_therapy_unavailable == UNKNOWN:
                unknown.append('whether standard anticancer treatment is no longer appropriate or feasible')
        if req.get('large_inoperable_or_rt_preferred'):
            if large_inoperable_or_rt_preferred == 'No':
                excluded=True
            elif large_inoperable_or_rt_preferred == UNKNOWN:
                unknown.append('whether the tumor is large/inoperable or radiotherapy is preferred to surgery')
        if req.get('surgery_or_rt_not_possible'):
            if surgery_or_rt_not_possible == 'No':
                excluded=True
            elif surgery_or_rt_not_possible == UNKNOWN:
                unknown.append('whether curative surgery/radiotherapy is no longer possible')
        if req.get('ct_and_current_biopsy'):
            if ct_and_current_biopsy == 'No':
                excluded=True
            elif ct_and_current_biopsy == UNKNOWN:
                unknown.append('whether current CT and biopsy requirements can be met')

        # Explicit exclusions.
        if exc.get('prior_local_radiation') and radiation in ['Previously received','Currently receiving']:
            excluded=True
        elif exc.get('prior_local_radiation') and radiation == UNKNOWN:
            unknown.append('whether prior local radiation is excluded')
        if exc.get('immunosuppressive') and immunosuppressive == 'Yes':
            excluded=True
        elif exc.get('immunosuppressive') and immunosuppressive == UNKNOWN:
            unknown.append('whether immunosuppressive medication is excluded')
        if exc.get('prior_surgery') and surgery == 'Yes':
            excluded=True
        elif exc.get('prior_surgery') and surgery == UNKNOWN:
            unknown.append('whether prior surgery is excluded')
        if exc.get('prior_chemo') and chemo in ['Previously received','Currently receiving']:
            excluded=True
        elif exc.get('prior_chemo') and chemo == UNKNOWN:
            unknown.append('whether prior chemotherapy is excluded')
        if exc.get('prior_immunotherapy') and immunotherapy_history in ['Previously received','Currently receiving']:
            excluded=True
        elif exc.get('prior_immunotherapy') and immunotherapy_history == UNKNOWN:
            unknown.append('whether prior immunotherapy is excluded')
        # Current treatment is a hard NO only when the stored protocol says it is a
        # permanent exclusion. A washout is potentially satisfiable and stays Possible.
        if exc.get('current_chemo') and chemo == 'Currently receiving':
            if req.get('chemo_washout_days'):
                unknown.append(f"chemotherapy washout of {req['chemo_washout_days']} days")
            else:
                excluded=True
        elif exc.get('current_chemo') and chemo == UNKNOWN:
            unknown.append('whether current chemotherapy is excluded')
        if exc.get('current_steroids') and steroids == 'Currently taking':
            if req.get('steroid_washout_days'):
                unknown.append(f"steroid washout of {req['steroid_washout_days']} days")
            else:
                excluded=True
        elif exc.get('current_steroids') and steroids == UNKNOWN:
            unknown.append('whether current corticosteroid use is excluded')
        if exc.get('current_radiation') and radiation == 'Currently receiving':
            if req.get('radiation_washout_days'):
                unknown.append(f"radiation washout of {req['radiation_washout_days']} days")
            else:
                excluded=True
        elif exc.get('current_radiation') and radiation == UNKNOWN:
            unknown.append('whether current radiation is excluded')

        # Treatment-history / planned-treatment requirements represented in the form.
        if req.get('prior_radiation') is False and radiation in ['Previously received','Currently receiving']:
            excluded=True
        elif req.get('prior_radiation') is False and radiation == UNKNOWN:
            unknown.append('whether prior radiation is excluded')
        if req.get('prior_radiation') is True and radiation == 'Never':
            excluded=True
        elif req.get('prior_radiation') is True and radiation == UNKNOWN:
            unknown.append('whether prior radiation is required')
        if req.get('planned_surgery') or req.get('planned_amputation') or req.get('planned_amputation_and_chemo'):
            if 'Surgery' not in prefs:
                excluded=True
            else:
                unknown.append('required study surgery/amputation has not yet been confirmed')
        if req.get('planned_radiation'):
            if 'Radiation' not in prefs or radiation_affordability == 'Would not consider radiation':
                excluded=True
            else:
                unknown.append('required study radiation has not yet been confirmed')
        if req.get('planned_doxorubicin') or req.get('planned_amputation_and_chemo'):
            if 'Chemotherapy' not in prefs:
                excluded=True
            else:
                unknown.append('required study chemotherapy/doxorubicin has not yet been confirmed')

        # Sex is intentionally retained in the matcher even though the current
        # verified catalog has no sex-specific oncology protocol. Future records
        # can use requires.sex = 'Male'/'Female' or a list of allowed values.
        sex_req = req.get('sex')
        if sex_req:
            allowed = {sex_req} if isinstance(sex_req, str) else set(sex_req)
            if sex == UNKNOWN:
                unknown.append('sex requirement')
            elif not any(sex.startswith(x) for x in allowed):
                excluded=True

        if req.get('localized'):
            if localized == 'No': excluded=True
            elif localized == UNKNOWN: unknown.append('whether the disease is localized')
            else: reasons.append('localized disease reported')

        # Research-only studies are shown only after the explicit observational opt-in
        # handled above; do not silently discard them after the user opted in.

        # Tumor/staging requirements. A measurable-tumor protocol requires gross
        # disease now; microscopic dirty margins are not measurable disease.
        if req.get('measurable'):
            if tumor_status not in ['Tumor still present / measurable', 'Local recurrence']:
                if tumor_status == UNKNOWN:
                    unknown.append('whether measurable disease is present')
                else:
                    excluded=True
        if req.get('metastatic'):
            if metastasis == 'No known metastases':
                excluded=True
            elif metastasis in [UNKNOWN, 'Suspected / staging incomplete']:
                unknown.append('whether metastasis is confirmed')
        if req.get('no_metastasis'):
            if metastasis == 'Confirmed metastases':
                excluded=True
            elif metastasis in [UNKNOWN, 'Suspected / staging incomplete']:
                unknown.append('whether staging confirms no metastasis')

        # Age requirements. Unknown age stays Possible.
        min_age=req.get('min_age_years')
        max_age=req.get('max_age_years')
        if min_age is not None:
            if age_known and age < min_age: excluded=True
            elif not age_known: unknown.append(f'minimum age of {min_age:g} years')
        if max_age is not None:
            if age_known and age > max_age: excluded=True
            elif not age_known: unknown.append(f'maximum age of {max_age:g} years')

        # Weight requirements. Unknown weight stays Possible, never excluded.
        min_lb=req.get('min_weight_lb')
        if min_lb is None and req.get('min_weight_kg') is not None:
            min_lb=req['min_weight_kg']*2.2046226218
        max_lb=req.get('max_weight_lb')
        if max_lb is None and req.get('max_weight_kg') is not None:
            max_lb=req['max_weight_kg']*2.2046226218
        if min_lb is not None:
            if weight_known and weight_lb < min_lb: excluded=True
            elif not weight_known: unknown.append(f'minimum weight of {min_lb:.1f} lb')
        if max_lb is not None:
            if weight_known and weight_lb > max_lb: excluded=True
            elif not weight_known: unknown.append(f'maximum weight of {max_lb:.1f} lb')

        # Treatment-history requirements.
        if req.get('prior_chemo') is False and chemo in ['Previously received','Currently receiving']:
            excluded=True
        elif req.get('prior_chemo') is False and chemo == UNKNOWN:
            unknown.append('whether prior chemotherapy is excluded')
        if req.get('prior_chemo') is True and chemo == 'Never':
            excluded=True
        elif req.get('prior_chemo') is True and chemo == UNKNOWN:
            unknown.append('whether prior chemotherapy is required')
        if req.get('prior_surgery') is True and surgery == 'No':
            excluded=True
        elif req.get('prior_surgery') is True and surgery == UNKNOWN:
            unknown.append('whether prior surgery is required')
        if req.get('prior_surgery') is False and surgery == 'Yes':
            excluded=True
        elif req.get('prior_surgery') is False and surgery == UNKNOWN:
            unknown.append('whether prior surgery is excluded')

        # Requirements not fully answerable by the short owner form must never
        # silently count as satisfied. Keep the study Possible pending prescreen.
        if req.get('post_splenectomy'):
            if surgery == 'No': excluded=True
            elif surgery == UNKNOWN: unknown.append('whether splenectomy has been performed')
            elif prior_procedure == 'Other': excluded=True
            elif prior_procedure != 'Splenectomy': unknown.append('whether the prior surgery was splenectomy')
        if req.get('post_amputation'):
            if surgery == 'No': excluded=True
            elif surgery == UNKNOWN: unknown.append('whether amputation has been performed')
            elif prior_procedure in ['Limb-sparing surgery','Other']: excluded=True
            elif prior_procedure != 'Amputation': unknown.append('whether the prior surgery was amputation')
        if req.get('pretreatment_biopsy'):
            unknown.append('pretreatment biopsy requirement')
        if req.get('resectable_or_minimal'):
            unknown.append('whether disease is resectable/minimal as required')
        if req.get('progressive'):
            if cancer in LYMPHOMA_CANCERS and lymphoma_response != 'Progression during treatment':
                if lymphoma_response == UNKNOWN: unknown.append('whether disease is progressive')
                else: excluded=True
            elif cancer not in LYMPHOMA_CANCERS:
                unknown.append('whether disease is progressive')
        if req.get('relapsed_or_refractory'):
            if cancer in LYMPHOMA_CANCERS:
                if lymphoma_response not in ['Progression during treatment','First relapse after remission','More than one relapse']:
                    if lymphoma_response == UNKNOWN: unknown.append('whether lymphoma is relapsed/refractory')
                    else: excluded=True
            else:
                unknown.append('whether disease is relapsed/refractory')

        if excluded:
            continue

        if cancer == 'Cancer — any type':
            reasons.append('cancer type not specified — study shown for diagnosis review')
        else:
            reasons.append('broad disease-family eligibility supports investigator review' if broad_match else f'{cancer} matches the study disease category')
        if diagnosis_status == 'Confirmed by pathology/cytology':
            reasons.append('diagnosis reported as confirmed')
        if tumor_status == 'Tumor still present / measurable':
            reasons.append('gross/measurable tumor reported')

        # "Likely" only when every stored owner-answerable key criterion is
        # positively satisfied. Unknowns and special prescreens stay Possible.
        key_checks=[]

        if req.get('active_treatment_target'):
            key_checks.append(tumor_status in ['Tumor still present / measurable', 'Local recurrence'])
        if req.get('localized'):
            key_checks.append(localized == 'Yes')
        if req.get('measurable'):
            key_checks.append(tumor_status in ['Tumor still present / measurable', 'Local recurrence'])
        if min_age is not None:
            key_checks.append(age_known and age >= min_age)
        if max_age is not None:
            key_checks.append(age_known and age <= max_age)
        if req.get('metastatic'):
            key_checks.append(metastasis == 'Confirmed metastases')
        if req.get('no_metastasis'):
            key_checks.append(metastasis == 'No known metastases')
        if min_lb is not None:
            key_checks.append(weight_known and weight_lb >= min_lb)
        if max_lb is not None:
            key_checks.append(weight_known and weight_lb <= max_lb)
        if req.get('prior_chemo') is False:
            key_checks.append(chemo == 'Never')
        if req.get('prior_chemo') is True:
            key_checks.append(chemo in ['Previously received','Currently receiving'])
        if req.get('prior_surgery') is True:
            key_checks.append(surgery == 'Yes')
        if req.get('prior_surgery') is False:
            key_checks.append(surgery == 'No')

        special_requirement = tr.get('special_requirement')
        if special_requirement:
            unknown.append(str(special_requirement))

        # Any unresolved owner-answerable or site-screening criterion caps the
        # result at Possible; unknown facts must never silently become Likely.
        criteria_complete = bool(req) and bool(key_checks) and all(key_checks) and not unknown
        confidence = 'Likely match' if criteria_complete else 'Possible match'
        # Without a specific cancer diagnosis we cannot claim disease-level matching.
        # Surface eligible records as review candidates rather than Possible/Likely matches.
        if cancer == 'Cancer — any type':
            confidence = 'Trial to review — cancer type not specified'

        # Enrollment uncertainty or eligibility that the short owner form
        # cannot establish must never be presented as Likely.
        if (
            tr.get('status_confidence') == 'needs_reconfirmation'
            or tr.get('owner_prescreen_required')
            or tr.get('broad_disease_fallback')
            or tr.get('requires_site_screening')
            or tr.get('freshness_unresolved')
        ):
            if cancer != 'Cancer — any type':
                confidence = 'Potential broad-treatment trial — prescreening required' if broad_match else 'Possible match'

        matches.append((confidence,tr,reasons,unknown))

    matches.sort(key=lambda x: (0 if x[0] == 'Likely match' else 1 if x[0] == 'Possible match' else 2, 1 if x[1].get('early_phase') else 0))
    st.header('Results')
    if not matches:
        st.info(
            'No plausible matches were found among the currently verified trials. '
            'This does not mean that no suitable study exists — recruitment and eligibility can change. '
            'Review the treatment options you selected or check again as recruitment changes.'
        )
    else:
        st.success(f'{len(matches)} trial(s) may be worth contacting')
        for confidence,tr,reasons,unknown in matches:
            with st.container(border=True):
                st.markdown(f"### {confidence} · {tr['center']}")
                st.markdown(f"**{tr['title']}**")
                st.markdown('**Study type:** ' + tr.get('study_type', 'treatment').replace('_', ' ').title())
                st.markdown('**Why it may fit:** ' + '; '.join(reasons) + '.')
                if unknown:
                    unresolved = list(dict.fromkeys(str(x) for x in unknown))
                    st.markdown('**Needs confirmation:** ' + '; '.join(unresolved) + '.')
                st.write(
                    '**Contact:** ' + tr.get(
                        'contacts',
                        tr.get('contact', 'Contact the study team through the official study page')
                    )
                )
                if tr.get('sites'):
                    site_text = '; '.join(
                        f"{x['hospital']} — {x['city']}, {x['state']}" for x in tr['sites']
                    )
                    st.write('**Participating sites:** ' + site_text)
                st.link_button('Study page / enrollment', tr.get('url', ''), use_container_width=True)
                with st.expander('Study information'):
                    if tr.get('intervention'):
                        st.write('**Study intervention:** ' + tr['intervention'])
                    st.write('**What the study says:** ' + tr['notes'])
                    st.write('**Trial funding:** ' + tr.get('funding', 'Ask the study team about covered study costs'))
                    st.caption(f"Status: {tr['status']} · Last verified: {tr.get('verified', 'date not recorded')}")

    _render_result_save_controls(matches)
    with st.expander('Help us improve this beta'):
        st.write('If a trial team says your pet is not eligible, please save the reason they gave. This helps improve the matcher. Do not post private medical or contact information publicly.')

st.divider()
st.markdown('**Urgent symptoms come first.** Difficulty breathing, collapse, uncontrolled bleeding, severe pain, or another emergency should be assessed by a veterinarian immediately rather than delayed for a clinical-trial search.')
st.caption('Beta: trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research team.')


st.markdown("---")
st.caption("Verified treatment trials and experimental treatment programs • U.S. + Europe/UK • Last deep audit: September 4, 2026")
st.caption("This finder identifies potentially relevant clinical trials; it does not determine eligibility. Final eligibility is determined by the study investigators. It is not a substitute for veterinary advice.")
