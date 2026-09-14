# EU cancer-by-cancer gap audit completed 2026-09-04: all UI cancer categories rechecked; no unverified lead promoted to matching.
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from location_sort import sort_matches_by_distance
from matcher_engine import SearchAnswers, match_trials as _engine_match_trials
from result_actions import contact_actions, verification_label
from search_telemetry import record_search_outcome, tumor_size_bucket
from trial_catalog import (
    CANCER_ALIASES,
    CANCERS,
    is_current_trial,
    load_trials,
    species_matches,
    trial_accepts_diagnosis,
    trial_modalities,
)

LYMPHOMA_CANCERS = {'B-cell lymphoma', 'T-cell lymphoma', 'Lymphoma — other'}
UMAMI_WEBSITE_ID = '20597fc4-68b1-4552-94c8-0771d1d74673'


def _track_umami_pageview_once():
    """Count one matcher visit per Streamlit session, not every widget rerun."""
    if st.session_state.get('_umami_matcher_visit_tracked'):
        return
    components.html(f'''
<script defer src="https://cloud.umami.is/script.js"
        data-website-id="{UMAMI_WEBSITE_ID}"
        data-auto-pageview="false"
        onload="umami.track({{website: '{UMAMI_WEBSITE_ID}', hostname: 'c-trials.streamlit.app', url: '/matcher', title: 'Vet Cancer Trial Finder'}})"></script>
''', height=0, width=0)
    st.session_state['_umami_matcher_visit_tracked'] = True


def _track_umami_search():
    """Record a search without sending diagnosis, location, or form answers."""
    components.html(f'''
<script defer src="https://cloud.umami.is/script.js"
        data-website-id="{UMAMI_WEBSITE_ID}"
        data-auto-pageview="false"
        onload="umami.track('matcher-search')"></script>
''', height=0, width=0)

st.set_page_config(page_title='Vet Cancer Treatment Finder', page_icon='🐾', layout='centered')
_track_umami_pageview_once()


def _render_result_save_controls(matches):
    import io, json
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch

    lines = ["Clinical Trial Finder Results"]
    for match in matches:
        tr = match.trial
        lines += ["", match.label, tr.get("center", ""), tr.get("title", "")]
        if match.reasons:
            lines.append("Why: " + "; ".join(match.reasons) + ".")
        if match.needs_confirmation:
            lines.append("Confirm: " + "; ".join(dict.fromkeys(match.needs_confirmation)) + ".")
        lines.append("Contact: " + tr.get("contacts", tr.get("contact", "Contact the study team through the official study page")))
        if tr.get("sites"):
            lines.append("Participating sites: " + "; ".join(f"{x['hospital']} — {x['city']}, {x['state']}" for x in tr["sites"]))
        details_url = tr.get("registry_url") or tr.get("url")
        if details_url:
            lines.append("Full study details: " + details_url)
        lines.append("What the study says: " + tr.get("notes", ""))
        lines.append("Status: " + tr.get("status", "") + " · Last verified: " + tr.get("verified", "date not recorded"))
    lines += ["", "Recruitment and eligibility can change; confirm current status with the study team."]
    report_text = "\n".join(lines)

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
    payload = json.dumps(report_text)
    with st.container(key="result_save_actions"):
        cols = st.columns(2, gap="small")
        with cols[0]:
            st.html(f"""<button id="copy-results-native" style="width:100%;padding:9px 12px;border:1px solid #d8d3cf;border-radius:9px;background:white;font-weight:600;color:#4b4642;cursor:pointer">📋 Copy results</button><div id="copy-msg" style="font:12px Arial;color:#55745d;margin-top:4px;min-height:14px"></div><script>(()=>{{const text={payload};const b=document.getElementById('copy-results-native'),m=document.getElementById('copy-msg');b.addEventListener('click',async()=>{{try{{await navigator.clipboard.writeText(text);m.textContent='Results copied.';return}}catch(e){{}}const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.focus();ta.select();try{{document.execCommand('copy');m.textContent='Results copied.'}}catch(e){{m.textContent='Copy is blocked by this browser.'}}ta.remove()}})}})();</script>""", unsafe_allow_javascript=True)
        with cols[1]:
            st.download_button("📄 Save as PDF", data=buf.getvalue(), file_name="clinical_trial_results.pdf", mime="application/pdf", use_container_width=True, on_click="ignore")


TRIALS = load_trials()

# 2026-09-03 private-referral / institutional-registry / local-language deep pass


# 2026-09-03 regulatory / CRO / sponsor-development pass

UNLISTED_CANCER = "My cancer type isn't listed"
TREATMENT_OPTIONS = ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug']
UNKNOWN = "I don't know"

_CONFIRMATION_PRIORITY = (
    "pathology/cytology", "active treatment target", "measurable disease",
    "minimum weight", "maximum weight", "visible tumor", "tumor location",
    "current chemotherapy", "current radiation", "current steroid",
)


def _compact_confirmations(items, limit=3):
    unique = list(dict.fromkeys(item.strip() for item in items if item.strip()))

    def rank(item):
        lowered = item.casefold()
        for index, phrase in enumerate(_CONFIRMATION_PRIORITY):
            if phrase in lowered:
                return index, unique.index(item)
        return len(_CONFIRMATION_PRIORITY), unique.index(item)

    visible_raw = sorted(unique, key=rank)[:limit]
    visible_set = set(visible_raw)
    visible = [
        'whether the tumor is currently present'
        if item == 'whether an active treatment target is present'
        else item
        for item in visible_raw
    ]
    return visible, [item for item in unique if item not in visible_set]


def _unknown_selectbox(label, options, **kwargs):
    """Render a medical question without silently asserting a clinical fact."""
    return st.selectbox(label, options, index=options.index(UNKNOWN), **kwargs)

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
.finder-note {
    background: #f5f8f9;
    border: 1px solid #e5ebed;
    border-radius: .55rem;
    color: #45484b;
    font-size: .93rem;
    line-height: 1.35;
    margin: .45rem 0 .6rem;
    padding: .55rem .7rem;
}
.finder-intro {
    font-size: 1rem;
    line-height: 1.4;
    margin: .55rem 0 .15rem;
}
.finder-intro strong { font-weight: 700; }
.result-actions {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .45rem;
    margin-top: .35rem;
}
.result-actions a {
    align-items: center;
    border: 1px solid #d8d3cf;
    border-radius: .55rem;
    color: #35383b;
    display: flex;
    justify-content: center;
    min-height: 2.65rem;
    padding: .42rem .55rem;
    text-align: center;
    text-decoration: none;
}
.result-actions a:last-child:nth-child(odd) { grid-column: 1 / -1; }
.st-key-result_save_actions [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: .45rem !important;
}
.st-key-result_save_actions [data-testid="stColumn"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    width: 50% !important;
}
@media (max-width: 600px) {
    div[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: .55rem !important;
    }
    div[data-testid="stMainBlockContainer"] h2 {
        margin-top: .65rem !important;
    }
    div[data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] {
        margin-bottom: .15rem !important;
    }
    .finder-note {
        font-size: .86rem;
        line-height: 1.3;
        margin: .25rem 0 .35rem;
        padding: .48rem .6rem;
    }
    .finder-intro {
        margin: .55rem 0 .2rem;
    }
    div[data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {
        margin-bottom: 0 !important;
    }
    div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] {
        margin-top: .6rem !important;
        margin-bottom: .2rem !important;
    }
}
</style>
''', unsafe_allow_html=True)

st.title('🐾 Vet Cancer Trial Finder')

# SAFE_DATABASE_STATS_V1
# Read-only summary of the catalog already loaded into TRIALS.
_stats_trials = [
    t for t in TRIALS
    if t.get('available_for_matching', True)
    and is_current_trial(t)
    and t.get('study_type', 'treatment') in {'treatment', 'other_treatment_access'}
]
_stats_centers = {str(t.get('center', '')).strip() for t in _stats_trials if str(t.get('center', '')).strip()}
_stats_excluded_cancers = {'Cancer — any type', 'Other / not sure', UNLISTED_CANCER}
_stats_cancers = {
    c for c in CANCERS
    if c not in _stats_excluded_cancers
    and any(trial_accepts_diagnosis(t, c)[0] for t in _stats_trials)
}
_stats_country_aliases = {'United Kingdom': 'UK', 'The Netherlands': 'Netherlands', 'Czech Republic': 'Czechia'}
_stats_countries = {
    _stats_country_aliases.get(str(t.get('country', 'USA')).strip(), str(t.get('country', 'USA')).strip())
    for t in _stats_trials
    if str(t.get('country', 'USA')).strip()
}
st.caption(
    f"{len(_stats_trials)} active treatment opportunities · "
    f"{len(_stats_centers)} centers · "
    f"{len(_stats_cancers)} cancer types · "
    f"{len(_stats_countries)} countries"
)

st.markdown(
    '<div class="finder-note">This finder suggests potentially relevant options; '
    'the treating or study team confirms eligibility. It is not veterinary advice.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="finder-intro">Answer what you know. It is completely fine to choose '
    '“I don’t know”.</div>',
    unsafe_allow_html=True,
)

with st.expander('Before you start', expanded=False):
    st.write('Helpful records, if you have them: pathology/cytology report, surgery report, recent imaging/staging, bloodwork, and names/dates of cancer treatments. You do not need all of these to search.')

st.header('1. Your pet')
c1, c2 = st.columns(2)
with c1:
    species = st.selectbox('Species', ['Dog','Cat'])
    age = st.number_input('Age (years, optional)', 0.0, 30.0, value=None, step=0.5)
with c2:
    weight_unit = st.radio('Weight unit', ['lb', 'kg'], horizontal=True)
    if weight_unit == 'kg':
        weight_value = st.number_input('Weight (kg, optional)', 0.1, 113.5, value=None, step=0.1)
        weight_kg = weight_value
        weight_lb = weight_value * 2.2046226218 if weight_value is not None else None
    else:
        weight_value = st.number_input('Weight (lb, optional)', 0.2, 250.0, value=None, step=0.5)
        weight_lb = weight_value
        weight_kg = weight_value / 2.2046226218 if weight_value is not None else None
    sex = UNKNOWN

trial_countries = sorted({t.get('country', 'USA') for t in TRIALS}, key=lambda x: (x != 'USA', x))
EUROPE_COUNTRIES = {
    'UK', 'United Kingdom', 'France', 'Italy', 'Portugal', 'Switzerland',
    'Netherlands', 'The Netherlands', 'Belgium', 'Sweden', 'Slovenia',
    'Spain', 'Germany', 'Cyprus', 'Austria', 'Poland', 'Norway',
    'Denmark', 'Finland', 'Ireland', 'Czech Republic', 'Czechia',
    'Hungary', 'Greece', 'Romania', 'Croatia', 'Estonia', 'Latvia',
    'Lithuania', 'Luxembourg', 'Iceland'
}
region_choice = st.selectbox(
    'Country / region',
    ['USA', 'Canada', 'Europe', 'Other countries', 'All countries'],
)
if region_choice == 'Europe':
    european_countries = sorted({value for value in trial_countries if value in EUROPE_COUNTRIES})
    european_country = st.selectbox('European country', ['All Europe'] + european_countries)
    country = 'Europe — all countries' if european_country == 'All Europe' else european_country
elif region_choice == 'Other countries':
    other_countries = sorted({
        value for value in trial_countries
        if value not in EUROPE_COUNTRIES and value not in {'USA', 'Canada'}
    })
    country = st.selectbox('Country', other_countries)
else:
    country = region_choice

if region_choice == 'USA':
    zip_code = st.text_input(
        'ZIP code (optional)',
        max_chars=10,
        placeholder='e.g. 01095',
        help='Used only to put closer studies first. It does not exclude distant studies.',
    )
else:
    zip_code = ''

def country_matches(trial_country, selected_country):
    if selected_country == 'All countries':
        return True
    if selected_country == 'Europe — all countries':
        return trial_country in EUROPE_COUNTRIES
    return trial_country == selected_country

st.header('2. Diagnosis')
cancer = st.selectbox('Cancer type', CANCERS, index=None, placeholder='Select cancer type')
diagnosis_status = st.selectbox(
    'How certain is the diagnosis?',
    ['Confirmed by pathology/cytology','Suspected / not confirmed',UNKNOWN],
    index=2,
)
unlisted_mode = cancer == UNLISTED_CANCER
unlisted_diagnosis = st.text_input('Enter the diagnosis as written in the pathology report, if known') if unlisted_mode else ''

# Build the owner form from criteria that can actually affect matching for this
# species/disease. Irrelevant disease-status rows stay visible but disabled so
# the form does not jump around when the cancer type changes.
_form_trials = []
for _tr in TRIALS:
    if not _tr.get('available_for_matching', True) or not is_current_trial(_tr):
        continue
    if _tr.get('study_type', 'treatment') != 'treatment' or not species_matches(_tr.get('species', ''), species):
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

if cancer is None:
    st.caption('Select a cancer type to continue.')
    st.selectbox('Current tumor status', ['Select a cancer type first'], disabled=True, key='no_cancer_tumor_status')
    st.selectbox('Metastases', ['Select a cancer type first'], disabled=True, key='no_cancer_metastases')
    st.selectbox('Has your veterinarian said the disease is localized?', ['Select a cancer type first'], disabled=True, key='no_cancer_localized')
    tumor_status = metastasis = localized = UNKNOWN
elif any_cancer_browse or unlisted_mode:
    st.caption('Browse mode: disease-specific eligibility is not used until a cancer type is selected.' if any_cancer_browse else 'Unlisted diagnosis: only genuinely all-tumor treatment programs will be shown for investigator review.')
    tumor_status = metastasis = localized = UNKNOWN
elif hematologic:
    st.selectbox('Current tumor status', ['Not applicable'], disabled=True, key='na_tumor_status')
    st.selectbox('Metastases', ['Not applicable'], disabled=True, key='na_metastases')
    st.selectbox('Has your veterinarian said the disease is localized?', ['Not applicable'], disabled=True, key='na_localized')
    tumor_status = metastasis = localized = UNKNOWN
elif brain_tumor:
    brain_present = _unknown_selectbox('Is the brain tumor currently present on imaging?', ['Yes','No visible tumor',UNKNOWN])
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
    tumor_status = _unknown_selectbox('Current tumor status', ['Tumor still present / measurable','Completely removed — clean margins','Removed — incomplete/dirty margins','Removed — margins unknown','Local recurrence','No evidence of disease (NED)',UNKNOWN])
    metastasis = _unknown_selectbox('Metastases', ['No known metastases','Confirmed metastases','Suspected / staging incomplete',UNKNOWN])
    localized = _unknown_selectbox('Has your veterinarian said the disease is localized?', ['Yes','No',UNKNOWN])

if cancer in LYMPHOMA_CANCERS or cancer == 'Cutaneous epitheliotropic lymphoma':
    if cancer == 'Cutaneous epitheliotropic lymphoma':
        lymphoma_type = 'T-cell'
    else:
        default_lymphoma_type = {'B-cell lymphoma': 0, 'T-cell lymphoma': 1, 'Lymphoma — other': 2}[cancer]
        lymphoma_type = st.selectbox('Lymphoma type', ['B-cell','T-cell','Other',UNKNOWN], index=default_lymphoma_type)
    lymphoma_response = _unknown_selectbox('Response/status', ['Newly diagnosed / untreated','Complete remission','Partial response','Progression during treatment','First relapse after remission','More than one relapse',UNKNOWN])
    if lymphoma_response in ['Newly diagnosed / untreated','Partial response','Progression during treatment','First relapse after remission','More than one relapse']:
        tumor_status = 'Tumor still present / measurable'
    elif lymphoma_response == 'Complete remission':
        tumor_status = 'No evidence of disease (NED)'
else:
    lymphoma_type = lymphoma_response = UNKNOWN

if cancer == 'Acute myeloid leukemia':
    leukemia_status = _unknown_selectbox('Leukemia status', ['Newly diagnosed / untreated','Responding to treatment / remission','Relapsed','Refractory / progressive',UNKNOWN])
    if leukemia_status in ['Newly diagnosed / untreated','Relapsed','Refractory / progressive']:
        tumor_status = 'Tumor still present / measurable'
    elif leukemia_status == 'Responding to treatment / remission':
        tumor_status = 'No evidence of disease (NED)'
else:
    leukemia_status = UNKNOWN

if cancer == 'Mast cell tumor':
    mct_grade = _unknown_selectbox('Mast cell tumor grade', ['Low grade / Kiupel low','High grade / Kiupel high','Patnaik grade 1','Patnaik grade 2','Patnaik grade 3',UNKNOWN])
    node_status = _unknown_selectbox('Regional lymph node status', ['Negative','Positive','Not sampled/tested',UNKNOWN])
else:
    mct_grade = node_status = UNKNOWN

if cancer == 'Osteosarcoma':
    osa_location = _unknown_selectbox('Primary osteosarcoma location', ['Appendicular — limb bone','Axial — skull, spine, rib, or pelvis','Other',UNKNOWN])
else:
    osa_location = UNKNOWN

if cancer == 'Hemangiosarcoma':
    hsa_site = _unknown_selectbox('Primary hemangiosarcoma site', ['Spleen','Heart / right atrium','Other',UNKNOWN])
else:
    hsa_site = UNKNOWN

# A compact adaptive layer for criteria that can safely be answered by owners.
# These fields appear only when at least one otherwise relevant trial uses them.
if {'min_tumor_cm', 'max_tumor_cm'}.intersection(_form_req_keys):
    tumor_size_known = st.checkbox('I know the tumor size')
    tumor_size_cm = st.number_input(
        'Largest tumor measurement (cm)',
        min_value=0.1,
        max_value=100.0,
        value=2.0,
        step=0.1,
        disabled=not tumor_size_known,
    ) if tumor_size_known else None
else:
    tumor_size_cm = None

_location_keys = {
    'cutaneous_sts', 'extremity_sts',
    'superficial_accessible_tumor', 'superficial_or_oral_tumor',
}
if _location_keys.intersection(_form_req_keys):
    tumor_location = _unknown_selectbox(
        'Where is the tumor located?',
        [
            'Skin / subcutaneous tissue — limb',
            'Skin / subcutaneous tissue — other area',
            'Deeper soft tissue — limb',
            'Deeper soft tissue — other area',
            'Mouth / oral cavity',
            'Internal organ / body cavity',
            'Other / not sure',
            UNKNOWN,
        ],
    )
    if tumor_location in {
        'Skin / subcutaneous tissue — limb',
        'Skin / subcutaneous tissue — other area',
        'Mouth / oral cavity',
    }:
        surface_or_oral_accessible = 'Yes'
    elif tumor_location in {
        'Deeper soft tissue — limb',
        'Deeper soft tissue — other area',
        'Internal organ / body cavity',
    }:
        surface_or_oral_accessible = 'No'
    else:
        surface_or_oral_accessible = UNKNOWN
else:
    tumor_location = UNKNOWN
    surface_or_oral_accessible = UNKNOWN

# Protocol-specific disease constraints used by broad Zurich basket/local-therapy trials.
standard_therapy_unavailable = _unknown_selectbox(
    'Is standard anticancer treatment no longer appropriate or not feasible?',
    ['Yes','No',UNKNOWN],
    help='Includes cases where standard therapy is no longer indicated, the tumor is inoperable/metastatic, or standard treatment cannot be performed.'
) if (not any_cancer_browse and not unlisted_mode and 'standard_therapy_unavailable' in _form_req_keys) else UNKNOWN

large_inoperable_or_rt_preferred = _unknown_selectbox(
    'For a large tumor: is it inoperable, or is radiotherapy being chosen instead of surgery?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'large_inoperable_or_rt_preferred' in _form_req_keys) else UNKNOWN

surgery_or_rt_not_possible = _unknown_selectbox(
    'Are curative surgery and radiotherapy no longer possible for this tumor?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'surgery_or_rt_not_possible' in _form_req_keys) else UNKNOWN

ct_and_current_biopsy = _unknown_selectbox(
    'Can current CT imaging and a current tumor biopsy be provided/performed?',
    ['Yes','No',UNKNOWN]
) if (not any_cancer_browse and not unlisted_mode and 'ct_and_current_biopsy' in _form_req_keys) else UNKNOWN

st.header('4. Treatment')
# Core cancer-treatment history must not depend on how completely individual
# trial metadata happen to be populated.  Earlier dynamic gating could make the
# entire Treatment section disappear for a diagnosis (for example HS) and then
# prevent the matcher from applying treatment-history exclusions.  Keep the four
# core oncology history questions stable for every specific diagnosis.
_specific_diagnosis = cancer is not None and not any_cancer_browse and not unlisted_mode
surgery_relevant = _specific_diagnosis
chemo_relevant = _specific_diagnosis
radiation_relevant = _specific_diagnosis
immunotherapy_relevant = _specific_diagnosis

# Medication questions remain protocol-driven because they are not universal
# cancer-treatment history and otherwise add noise to most searches.
steroids_relevant = _specific_diagnosis and ('current_steroids' in _form_exc_keys or 'steroid_washout_days' in _form_req_keys)
immunosuppressive_relevant = _specific_diagnosis and ('immunosuppressive' in _form_exc_keys)

surgery = _unknown_selectbox('Surgery', ['No','Yes',UNKNOWN]) if surgery_relevant else UNKNOWN
prior_procedure = UNKNOWN
if surgery == 'Yes' and cancer == 'Osteosarcoma':
    prior_procedure = _unknown_selectbox('Osteosarcoma surgery', ['Amputation','Limb-sparing surgery','Other',UNKNOWN])
elif surgery == 'Yes' and cancer == 'Hemangiosarcoma':
    prior_procedure = _unknown_selectbox('Hemangiosarcoma surgery', ['Splenectomy','Other',UNKNOWN])
chemo = _unknown_selectbox('Chemotherapy', ['Never','Currently receiving','Previously received',UNKNOWN]) if chemo_relevant else UNKNOWN
immunotherapy_history = _unknown_selectbox('Prior or current cancer immunotherapy', ['Never','Currently receiving','Previously received',UNKNOWN]) if immunotherapy_relevant else UNKNOWN
radiation = _unknown_selectbox('Radiation to this tumor', ['Never','Previously received','Currently receiving',UNKNOWN]) if radiation_relevant else UNKNOWN
steroids = _unknown_selectbox('Prednisone / other corticosteroids', ['Never / no','Prescribed but NOT started','Currently taking','Previously took',UNKNOWN]) if steroids_relevant else UNKNOWN
immunosuppressive = _unknown_selectbox('Other immunosuppressive medication', ['No','Yes',UNKNOWN]) if immunosuppressive_relevant else UNKNOWN

st.header('5. Treatment options')
prefs = st.multiselect('Select all that you would consider', TREATMENT_OPTIONS, default=TREATMENT_OPTIONS)
if not any_cancer_browse and 'planned_radiation' in _form_req_keys:
    radiation_affordability = _unknown_selectbox('If radiation is relevant', ['Would consider radiation','Would consider it if trial-funded','Would not consider radiation',UNKNOWN])
else:
    radiation_affordability = UNKNOWN

search_clicked = st.button(
    'Find potential trials',
    type='primary',
    use_container_width=True,
    disabled=cancer is None,
)


if search_clicked:
    _track_umami_search()
    _answers = SearchAnswers(
        species=species,
        cancer=cancer,
        diagnosis_status=diagnosis_status,
        age=age,
        weight_lb=weight_lb,
        sex=sex,
        tumor_status=tumor_status,
        metastasis=metastasis,
        localized=localized,
        lymphoma_response=lymphoma_response,
        surgery=surgery,
        prior_procedure=prior_procedure,
        chemo=chemo,
        immunotherapy_history=immunotherapy_history,
        radiation=radiation,
        steroids=steroids,
        immunosuppressive=immunosuppressive,
        preferences=frozenset(prefs),
        radiation_affordability=radiation_affordability,
        standard_therapy_unavailable=standard_therapy_unavailable,
        large_inoperable_or_rt_preferred=large_inoperable_or_rt_preferred,
        surgery_or_rt_not_possible=surgery_or_rt_not_possible,
        ct_and_current_biopsy=ct_and_current_biopsy,
        tumor_size_cm=tumor_size_cm,
        osa_location=osa_location,
        tumor_location=tumor_location,
        surface_or_oral_accessible=surface_or_oral_accessible,
        unlisted_diagnosis=unlisted_diagnosis,
    )
    _engine_matches = _engine_match_trials(
        TRIALS,
        _answers,
        accepts_diagnosis=trial_accepts_diagnosis,
        trial_modalities=trial_modalities,
        country_matches=lambda trial_country: country_matches(trial_country, country),
    )
    _distance_context = None
    if zip_code.strip():
        _engine_matches, _distance_context = sort_matches_by_distance(_engine_matches, zip_code)

    record_search_outcome(
        result_count=len(_engine_matches),
        fields={
            'species': species,
            'cancer': cancer,
            'country': country,
            'diagnosis_status': diagnosis_status,
            'tumor_status': tumor_status,
            'metastasis': metastasis,
            'localized': localized,
            'tumor_size_bucket': tumor_size_bucket(tumor_size_cm),
            'tumor_location': tumor_location,
        },
    )

    st.header('Results')
    if zip_code.strip() and _distance_context is None:
        st.warning('ZIP code not recognized. Results are shown in their usual order.')
    elif _distance_context:
        st.caption(
            f"Sorted by approximate straight-line distance from "
            f"{_distance_context['city']}, {_distance_context['state']}. "
            "Distance does not affect eligibility."
        )

    if not _engine_matches:
        st.info(
            'No plausible matches were found among the currently verified trials. '
            'This does not mean that no suitable study exists — recruitment and eligibility can change.'
        )
    else:
        st.success(f'{len(_engine_matches)} oncology opportunity(ies) may be worth contacting')
        _distances = (_distance_context or {}).get('distances', {})
        for _match in _engine_matches:
            tr = _match.trial
            with st.container(border=True):
                st.markdown(f"### {_match.label} · {tr['center']}")
                st.markdown(f"**{tr['title']}**")
                if tr.get('sites'):
                    st.markdown('**Where:** ' + '; '.join(
                        f"{site['hospital']} — {site['city']}, {site['state']}" for site in tr['sites']
                    ))
                elif tr.get('city') or tr.get('state'):
                    st.markdown('**Where:** ' + ', '.join(
                        value for value in (tr.get('city'), tr.get('state')) if value
                    ))
                else:
                    st.markdown('**Where:** ' + ', '.join(
                        value for value in (tr.get('center'), tr.get('country')) if value
                    ))
                if tr.get('intervention'):
                    st.markdown('**What is offered:** ' + tr['intervention'])
                if tr.get('funding'):
                    # Dollar amounts must stay plain text; otherwise Markdown
                    # treats the text between two $ signs as inline mathematics.
                    funding_text = str(tr['funding']).lstrip('🟢🟡🟠🔴️ ').replace(chr(36), chr(92) + chr(36))
                    st.markdown('**Costs / coverage:** ' + funding_text)
                if tr['id'] in _distances:
                    st.markdown(f"**Approximate distance:** {_distances[tr['id']]:.0f} miles")
                st.markdown('**Why it may fit:** ' + '; '.join(_match.reasons) + '.')
                visible_confirmations, additional_confirmations = _compact_confirmations(
                    _match.needs_confirmation
                )
                if visible_confirmations:
                    st.markdown('**Needs confirmation:** ' + '; '.join(visible_confirmations) + '.')
                st.caption(verification_label(tr.get('verified')))
                contact_text = tr.get('contacts', tr.get('contact', 'Contact the study team through the official study page'))
                st.write('**Contact:** ' + contact_text)
                details_url = tr.get('registry_url') or tr.get('url', '')
                email, phone = contact_actions(contact_text)
                actions = []
                if email:
                    actions.append(('Email study team', f'mailto:{email}'))
                if phone:
                    actions.append(('Call', f'tel:{phone}'))
                if details_url:
                    actions.append(('Official study', details_url))
                if actions:
                    links = ''.join(
                        f'<a href="{escape(target, quote=True)}"'
                        + (' target="_blank" rel="noopener"' if label == 'Official study' else '')
                        + f'>{escape(label)}</a>'
                        for label, target in actions
                    )
                    st.markdown(f'<div class="result-actions">{links}</div>', unsafe_allow_html=True)
                with st.expander('Study information'):
                    if additional_confirmations:
                        st.markdown(
                            '**Additional eligibility questions:**\n- '
                            + '\n- '.join(additional_confirmations)
                        )
                    if tr.get('intervention'):
                        st.write('**Study intervention:** ' + tr['intervention'])
                    if tr.get('notes'):
                        st.write('**What the study says:** ' + tr['notes'])
                    st.caption(f"Status: {tr['status']}")
        _render_result_save_controls(_engine_matches)
        with st.expander('Help us improve this finder'):
            st.write('If a trial team says your pet is not eligible, please save the reason they gave. This helps improve the matcher. Do not post private medical or contact information publicly.')

st.divider()
st.markdown('**Urgent symptoms come first.** Difficulty breathing, collapse, uncontrolled bleeding, severe pain, or another emergency should be assessed by a veterinarian immediately rather than delayed for a clinical-trial search.')
st.caption('Trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research or treatment team.')


st.markdown("---")
st.caption("Verified treatment trials and experimental treatment programs • International coverage • Updated daily")
st.caption("This finder identifies potentially relevant cancer treatment options. It does not determine eligibility. Final eligibility and treatment decisions are determined by the treating or research team. It is not a substitute for veterinary advice.")
