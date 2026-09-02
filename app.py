import streamlit as st
from datetime import date

st.set_page_config(page_title='Vet Cancer Trial Finder — Beta', page_icon='🐾', layout='centered')

TRIALS = [{'id': 'osu-sts-nk', 'title': 'NK-cell / anti-MIC immunotherapy for canine soft tissue sarcoma', 'center': 'The Ohio State University', 'country': 'USA', 'cancers': ['Soft tissue sarcoma', 'Spindle cell sarcoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://vmc.vet.osu.edu/clinical-trials/targeting-mic-augment-adoptive-nk-therapy-using-canine-soft-tissue-sarcoma-model', 'contacts': 'Blue Buffalo Clinical Trials Office — cvm-clinicaltrials@osu.edu', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Canine soft tissue sarcoma immunotherapy study.'}, {'id': 'uf-mct', 'title': 'Toceranib resistance study for canine mast cell tumors', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Mast cell tumor'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — referring veterinarian completes Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Comparative molecular analysis for acquired toceranib resistance.'}, {'id': 'uf-osa-vaccine', 'title': 'Vaccine study for dogs with appendicular osteosarcoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Appendicular osteosarcoma vaccine study.'}, {'id': 'uf-osa-mrna', 'title': 'mRNA vaccine study for dogs with appendicular osteosarcoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Appendicular osteosarcoma mRNA vaccine study.'}, {'id': 'uf-hsa-vaccine', 'title': 'Vaccine study for dogs with splenic hemangiosarcoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Hemangiosarcoma'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Splenic hemangiosarcoma vaccine study.'}, {'id': 'uf-melanoma', 'title': 'Vaccine study for dogs with melanoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Oral melanoma', 'Melanoma — other'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'UF currently lists a canine melanoma vaccine study.'}, {'id': 'uf-hs-trametinib', 'title': 'Phase II trametinib for dogs with histiocytic sarcoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Histiocytic sarcoma'], 'status': 'Currently enrolling', 'species': 'Dog', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/', 'contacts': 'UF Veterinary Hospitals Oncology — Oncology Referral Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Multicenter Phase II trametinib study.'}, {'id': 'uf-feline-oscc', 'title': 'RNA nanoparticle vaccine for feline oral squamous cell carcinoma', 'center': 'University of Florida', 'country': 'USA', 'cancers': ['Oral squamous cell carcinoma'], 'status': 'Limited enrollment', 'species': 'Cat', 'url': 'https://research.vetmed.ufl.edu/research-programs/clinical-trials/small-animal/oncology/', 'contacts': 'UF Veterinary Clinical Studies Program — Study Interest Form', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Feline oral SCC vaccine study.'}, {'id': 'umn-melanoma-aav', 'title': 'AAV vaccine for dogs with malignant oral melanoma', 'center': 'University of Minnesota', 'country': 'USA', 'cancers': ['Oral melanoma'], 'status': 'Open and enrolling', 'species': 'Dog', 'url': 'https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/new-vaccine', 'contacts': 'University of Minnesota Clinical Investigation Center', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Open and enrolling oral melanoma vaccine study.'}, {'id': 'umn-feline-mammary', 'title': 'Olaparib + meloxicam for feline mammary carcinoma', 'center': 'University of Minnesota', 'country': 'USA', 'cancers': ['Mammary carcinoma'], 'status': 'Open and enrolling', 'species': 'Cat', 'url': 'https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/olaparib', 'contacts': 'University of Minnesota Clinical Investigation Center', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Open and enrolling feline mammary carcinoma study.'}, {'id': 'umn-lyra3', 'title': 'LYRA 3 blood collection study for lymphoma risk/early detection', 'center': 'University of Minnesota', 'country': 'USA', 'cancers': ['Lymphoma'], 'status': 'Open and enrolling', 'species': 'Dog', 'url': 'https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials', 'contacts': 'University of Minnesota Clinical Investigation Center', 'funding': 'See official study page.', 'requires': {}, 'excludes': {}, 'notes': 'For healthy dogs at least 5 years old; included in catalog but not intended as treatment for a dog already diagnosed with lymphoma.', 'research_only': True}, {'id': 'ill-melanoma', 'title': 'IL-12 / IL-15 treatment study for canine oral melanoma', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Oral melanoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Treatment of canine patients with oral melanoma.'}, {'id': 'ill-osa-immuno', 'title': 'Immunotherapy for canine appendicular osteosarcoma', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Appendicular osteosarcoma immunotherapy study.'}, {'id': 'ill-osa-pulm', 'title': 'Treatment study for appendicular osteosarcoma with pulmonary metastasis', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True, 'metastatic': True}, 'excludes': {}, 'notes': 'For canine appendicular osteosarcoma with pulmonary metastasis.'}, {'id': 'ill-osa-rt', 'title': 'Radiation therapy study for canine appendicular osteosarcoma', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Radiation therapy study.'}, {'id': 'ill-sts-surg', 'title': 'Study for canine soft tissue sarcoma amenable to surgical removal', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Soft tissue sarcoma', 'Spindle cell sarcoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'For STS amenable to surgical removal.'}, {'id': 'ill-sts', 'title': 'Treatment study for canine soft tissue sarcoma', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Soft tissue sarcoma', 'Spindle cell sarcoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Canine STS treatment study.'}, {'id': 'ill-uc', 'title': 'Gilvetmab / epacadostat for canine urothelial carcinoma of the bladder', 'center': 'University of Illinois', 'country': 'USA', 'cancers': ['Urothelial / transitional cell carcinoma'], 'status': 'Funded current study', 'species': 'Dog', 'url': 'https://vetmed.illinois.edu/research/clinical-trials/', 'contacts': 'University of Illinois Veterinary Teaching Hospital Oncology', 'funding': 'Funded study.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Canine bladder urothelial carcinoma study.'}, {'id': 'auburn-palbociclib', 'title': 'Palbociclib study for multiple canine cancers', 'center': 'Auburn University', 'country': 'USA', 'cancers': ['Mammary carcinoma', 'Oral squamous cell carcinoma', 'Squamous cell carcinoma — other', 'Anal sac adenocarcinoma (AGASACA)', 'Histiocytic sarcoma', 'Oral melanoma', 'Melanoma — other'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vetmed.auburn.edu/research/clinical-trials/mammary-carcinoma-squamous-cell-carcinoma-agasaca-and-melanoma-clinical-trial/', 'contacts': 'Auburn Oncology Service — onco@auburn.edu · 334-844-4690', 'funding': 'After screening, trial is funded for up to 2 months of treatment; see official page.', 'requires': {'confirmed': True, 'measurable': True}, 'excludes': {}, 'notes': 'Prior cancer treatment allowed, but disease must be progressing at enrollment.'}, {'id': 'vt-thyroid', 'title': 'Histotripsy for canine thyroid tumors', 'center': 'Virginia Tech', 'country': 'USA', 'cancers': ['Thyroid tumor / carcinoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://research.vetmed.vt.edu/clinical-trials/current-studies.html', 'contacts': 'Virginia Tech Veterinary Clinical Research Office', 'funding': 'See official study page.', 'requires': {}, 'excludes': {}, 'notes': 'Non-invasive histotripsy treatment study.'}, {'id': 'vt-osa-standard', 'title': 'Amputation and chemotherapy study for canine osteosarcoma', 'center': 'Virginia Tech', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://research.vetmed.vt.edu/clinical-trials/current-studies.html', 'contacts': 'Virginia Tech Veterinary Clinical Research Office', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'For owners who have chosen standard-of-care amputation and chemotherapy.'}, {'id': 'penn-mammary-margin', 'title': 'Intraoperative molecular imaging of margins in dogs with mammary tumors', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Mammary carcinoma', 'Mammary tumor — other'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vet.upenn.edu/veterinary_specialty/oncology/', 'contacts': 'Penn Vet Veterinary Clinical Investigations Center — 215-573-0302 · vcic@vet.upenn.edu', 'funding': 'See official study page.', 'requires': {}, 'excludes': {}, 'notes': 'Near-infrared imaging agent applied during simulated breast-conserving surgery.'}, {'id': 'penn-flash-sts', 'title': 'Proton FLASH-RT for canine extremity soft tissue sarcoma', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Soft tissue sarcoma', 'Spindle cell sarcoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vet.upenn.edu/clinical-trial/evaluation-of-proton-flash-rt-in-naturally-occurring-canine-extremity-sarcoma/', 'contacts': 'Penn Vet Veterinary Clinical Investigations Center', 'funding': 'See official study page.', 'requires': {'confirmed': True, 'measurable': True}, 'excludes': {}, 'notes': 'Extremity STS where surgery is not feasible or has been declined.'}, {'id': 'penn-osa-carinkt', 'title': 'CAR-iNKT cell therapy for metastatic canine osteosarcoma', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Osteosarcoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vet.upenn.edu/clinical-trial/cell-therapy-for-metastatic-osteosarcoma/', 'contacts': 'Mary Beth Boland — mboland@vet.upenn.edu', 'funding': 'Treatment costs are covered.', 'requires': {'confirmed': True, 'metastatic': True, 'min_weight_lb': 39.7}, 'excludes': {}, 'notes': 'Requires B7-H3+ appendicular OSA, prior amputation and 4–6 carboplatin doses; final screening by Penn.'}, {'id': 'penn-prostate', 'title': 'PSMA ligand-based theranostic for canine prostatic cancer', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Prostate cancer'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vet.upenn.edu/clinical-trial/psma-ligand-based-theranostic-to-treat-canine-prostatic-cancer/', 'contacts': 'Penn Vet VCIC — 215-573-0302 · vcic@vet.upenn.edu', 'funding': 'Study-related diagnostics, treatment, hospitalization and specified rechecks covered.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'For local or metastatic canine prostate cancer.'}, {'id': 'penn-feline-oscc', 'title': 'Palliative radiation + frunevetmab for feline bone-invasive oral SCC', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Oral squamous cell carcinoma'], 'status': 'Recruiting', 'species': 'Cat', 'url': 'https://www.vet.upenn.edu/clinical-trial/pilot-study-of-frunevetmab-solensia-and-meloxicam-for-palliative-therapy-of-feline-bone-invasive-oral-squamous-cell-carcinomas/', 'contacts': 'Penn Vet Veterinary Clinical Investigations Center', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Pilot palliative study for feline bone-invasive oral SCC.'}, {'id': 'penn-hcc', 'title': 'Embolization vs chemoembolization for canine hepatocellular carcinoma', 'center': 'University of Pennsylvania', 'country': 'USA', 'cancers': ['Hepatocellular carcinoma'], 'status': 'Recruiting', 'species': 'Dog', 'url': 'https://www.vet.upenn.edu/clinical-trial/embolization-or-chemoembolization-in-dogs-with-hepatocellular-carcinoma-and-utility-of-contrast-enhanced-ultrasound-versus-ct-angiogram-in-post-embolization-assessment/', 'contacts': 'Penn Vet Veterinary Clinical Investigations Center — 215-573-0302 · vcic@vet.upenn.edu', 'funding': 'See official study page.', 'requires': {'confirmed': True}, 'excludes': {}, 'notes': 'Compares embolization and chemoembolization.'}]

CANCERS = ['Anal sac adenocarcinoma (AGASACA)', 'Hemangiosarcoma', 'Hepatocellular carcinoma', 'Histiocytic sarcoma', 'Lymphoma', 'Mammary carcinoma', 'Mammary tumor — other', 'Mast cell tumor', 'Melanoma — other', 'Oral melanoma', 'Oral squamous cell carcinoma', 'Osteosarcoma', 'Prostate cancer', 'Soft tissue sarcoma', 'Spindle cell sarcoma', 'Squamous cell carcinoma — other', 'Thyroid tumor / carcinoma', 'Urothelial / transitional cell carcinoma', 'Other / not sure']
UNKNOWN = "I don't know"

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
    weight_lb = st.number_input('Weight (lb)', 0.2, 250.0, 44.0, 0.5, disabled=not weight_known)
    weight_kg = weight_lb / 2.2046226218 if weight_known else None
    sex = st.selectbox('Sex', [UNKNOWN,'Female — spayed','Female — intact','Male — neutered','Male — intact'])

st.header('2. Location')
country = st.selectbox('Country', ['USA','Canada','Australia','United Kingdom','Other'])
location = st.text_input('ZIP / postal code / city (optional)')
travel = st.selectbox('How far could you travel for a trial?', ['Local only','Up to 100 miles','Up to 300 miles','Anywhere in the U.S.','International if needed'])

st.header('3. Diagnosis')
diagnosis_status = st.selectbox('How certain is the diagnosis?', ['Confirmed by pathology/cytology','Suspected / not confirmed',UNKNOWN])
cancer = st.selectbox('Cancer type', CANCERS)
subtype = st.text_input('Exact wording from pathology/cytology, if known')
grade = st.text_input('Grade, if known')

st.header('4. Current disease')
tumor_status = st.selectbox('Current tumor status', ['Tumor still present / measurable','Completely removed — clean margins','Removed — incomplete/dirty margins','Removed — margins unknown','Local recurrence','No evidence of disease (NED)',UNKNOWN])
metastasis = st.selectbox('Metastases', ['No known metastases','Confirmed metastases','Suspected / staging incomplete',UNKNOWN])
localized = st.selectbox('Has your veterinarian said the disease is localized?', ['Yes','No',UNKNOWN])

if cancer == 'Lymphoma':
    lymphoma_type = st.selectbox('Lymphoma type', ['B-cell','T-cell','Other',UNKNOWN])
    lymphoma_response = st.selectbox('Response/status', ['Newly diagnosed / untreated','Complete remission','Partial response','Progression during treatment','First relapse after remission','More than one relapse',UNKNOWN])
else:
    lymphoma_type = lymphoma_response = UNKNOWN

if cancer == 'Mast cell tumor':
    mct_grade = st.selectbox('Mast cell tumor grade', ['Low grade / Kiupel low','High grade / Kiupel high','Patnaik grade 1','Patnaik grade 2','Patnaik grade 3',UNKNOWN])
    node_status = st.selectbox('Regional lymph node status', ['Negative','Positive','Not sampled/tested',UNKNOWN])
else:
    mct_grade = node_status = UNKNOWN

st.header('5. Treatment')
surgery = st.selectbox('Surgery', ['No','Yes',UNKNOWN])
chemo = st.selectbox('Chemotherapy', ['Never','Currently receiving','Previously received',UNKNOWN])
chemo_details = st.text_input('Chemotherapy drugs + last treatment date, if known')
radiation = st.selectbox('Radiation to this tumor', ['Never','Previously received','Currently receiving',UNKNOWN])
steroids = st.selectbox('Prednisone / other corticosteroids', ['Never / no','Prescribed but NOT started','Currently taking','Previously took',UNKNOWN])
steroid_details = st.text_input('Steroid name, dose, first/last dose date, if known')
immunosuppressive = st.selectbox('Other immunosuppressive medication', ['No','Yes',UNKNOWN])
archived_tissue = st.selectbox('Is archived tumor tissue available?', ['Yes','No',UNKNOWN])

st.header('6. Treatment options')
prefs = st.multiselect('Select all that you would consider', ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug','Observational / sample-only study'], default=['Immunotherapy','Targeted therapy','Experimental drug'])
radiation_affordability = st.selectbox('If radiation is relevant', ['Would consider radiation','Would consider it if trial-funded','Would not consider radiation',UNKNOWN])

st.header('7. Other details')
notes = st.text_area('Optional notes', placeholder='Other illnesses, medications, staging results, pathology details, etc.')

search_clicked = st.button('Find potential trials', type='primary', use_container_width=True)

if search_clicked:
    if diagnosis_status != 'Confirmed by pathology/cytology':
        st.warning('We cannot make a reliable treatment-trial match until the cancer diagnosis is confirmed. Save the pathology/cytology result and search again after confirmation.')
    else:
        matches=[]
        for tr in TRIALS:
            if tr['species'] != species:
                continue
            if cancer not in tr['cancers']:
                if not (cancer == 'Spindle cell sarcoma' and 'Soft tissue sarcoma' in tr['cancers']):
                    continue
            reasons=[]; unknown=[]; excluded=False
            if tr['excludes'].get('prior_local_radiation') and radiation in ['Previously received','Currently receiving']:
                excluded=True
            if tr['excludes'].get('immunosuppressive') and immunosuppressive == 'Yes':
                excluded=True
            if tr['requires'].get('localized'):
                if localized == 'No': excluded=True
                elif localized == UNKNOWN: unknown.append('whether the disease is localized')
                else: reasons.append('localized disease reported')
            if tr.get('research_only'):
                continue
            req = tr.get('requires', {})
            if req.get('measurable') and tumor_status in ['Completely removed — clean margins','No evidence of disease (NED)']:
                excluded = True
            if req.get('metastatic') and metastasis == 'No known metastases':
                excluded = True
            if req.get('no_metastasis') and metastasis == 'Confirmed metastases':
                excluded = True
            if req.get('min_weight_lb') and weight_known and weight_lb < req['min_weight_lb']:
                excluded = True
            if excluded:
                continue
            reasons.append(f'{cancer} matches the study disease category')
            reasons.append('diagnosis reported as confirmed')
            if tumor_status == 'Tumor still present / measurable':
                reasons.append('gross/measurable tumor reported')

            # Conservative confidence rule:
            # "Likely" only when every key eligibility criterion stored for the
            # study can be positively confirmed from the owner's answers.
            # Otherwise keep the study visible as "Possible".
            key_checks = []

            if req.get('measurable'):
                key_checks.append(tumor_status == 'Tumor still present / measurable')

            if req.get('metastatic'):
                key_checks.append(metastasis == 'Confirmed metastases')

            if req.get('no_metastasis'):
                key_checks.append(metastasis == 'No known metastases')

            if req.get('min_weight_lb'):
                key_checks.append(weight_known and weight_lb >= req['min_weight_lb'])

            # For studies where the catalog currently has only diagnosis-level
            # criteria, do not imply eligibility: there may be center-specific
            # staging, lab, treatment-history or performance-status criteria.
            criteria_complete = bool(req) and bool(key_checks) and all(key_checks)

            confidence = 'Likely match' if criteria_complete else 'Possible match'
            matches.append((confidence,tr,reasons,unknown))

        matches.sort(key=lambda x: 0 if x[0] == 'Likely match' else 1)
        st.header('Results')
        if not matches:
            st.warning('No potential matches were found in this **currently verified catalog**. This does not mean no suitable clinical trial exists. The catalog is still being expanded.')
        else:
            st.success(f'{len(matches)} trial(s) may be worth contacting')
            for confidence,tr,reasons,unknown in matches:
                with st.container(border=True):
                    st.markdown(f"### {confidence} · {tr['center']}")
                    st.markdown(f"**{tr['title']}**")
                    st.markdown('**Why it may fit:** ' + '; '.join(reasons) + '.')
                    st.markdown('**Contact:** ' + tr['contacts'])
                    st.link_button('Official study page', tr['url'])
                    with st.expander('Study details'):
                        st.write('**What the study says:** ' + tr['notes'])
                        st.write('**Trial funding:** ' + tr['funding'])
                        st.caption(f"Status in beta catalog: {tr['status']} · Record reviewed {date.today().isoformat()}")

        with st.expander('Help us improve this beta'):
            st.write('If a trial team says your pet is not eligible, please save the reason. Those real-world exclusions are especially useful for improving the matcher. Do not post private medical or contact information publicly.')

st.divider()
st.markdown('**Urgent symptoms come first.** Difficulty breathing, collapse, uncontrolled bleeding, severe pain, or another emergency should be assessed by a veterinarian immediately rather than delayed for a clinical-trial search.')
st.caption('Beta: trial information can change. Always confirm recruiting status, eligibility, costs, travel requirements, and treatment details directly with the research team.')
