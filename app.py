import streamlit as st
from datetime import date

st.set_page_config(page_title='Vet Cancer Trial Finder — Beta', page_icon='🐾', layout='centered')

TRIALS = [
    {
        'id':'osu-sts-nk','title':'NK-cell / anti-MIC immunotherapy for canine soft tissue sarcoma','center':'The Ohio State University','country':'USA','cancers':['Soft tissue sarcoma','Spindle cell sarcoma'],'status':'Recruiting','species':'Dog',
        'url':'https://vmc.vet.osu.edu/clinical-trials/targeting-mic-augment-adoptive-nk-therapy-using-canine-soft-tissue-sarcoma-model',
        'contacts':'Dr. Shay Bracha — bracha.2@osu.edu · Clinical Trials Office — CVM-ClinicalTrials@osu.edu',
        'funding':'Trial-related procedures are covered; confirm current details with the study team.',
        'requires':{'localized':True,'confirmed':True}, 'excludes':{'prior_local_radiation':True,'immunosuppressive':True},
        'notes':'For localized cytologically or histologically confirmed soft-tissue sarcoma. Final eligibility is determined by the investigators.'
    },
    {
        'id':'uf-mct','title':'Toceranib resistance / molecular analysis in canine mast cell tumors','center':'University of Florida','country':'USA','cancers':['Mast cell tumor'],'status':'Recruiting','species':'Dog',
        'url':'https://research.vetmed.ufl.edu/comparative-molecular-analysis-for-acquired-toceranib-resistance-in-dogs-with-mast-cell-tumors-mcts/',
        'contacts':'UF Veterinary Hospitals Oncology — 352-392-2235 · Study interest/referral via the official page',
        'funding':'See the current study page for covered procedures and costs.',
        'requires':{'confirmed':True}, 'excludes':{},
        'notes':'Confirmed cutaneous MCT. Post-resection eligibility and tissue requirements need confirmation with the study team.'
    },
    {
        'id':'uf-hs-trametinib','title':'Phase II trametinib for dogs with histiocytic sarcoma','center':'University of Florida','country':'USA','cancers':['Histiocytic sarcoma'],'status':'Recruiting','species':'Dog',
        'url':'https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/',
        'contacts':'UF Veterinary Hospitals Oncology — 352-392-2235 · Referring veterinarian can use the Oncology Referral Form',
        'funding':'See the current study page for current financial support.',
        'requires':{'confirmed':True}, 'excludes':{},
        'notes':'Listed by UF as enrolling. Detailed protocol eligibility must be confirmed with the study team.'
    },
]

CANCERS = ['Mast cell tumor','Soft tissue sarcoma','Spindle cell sarcoma','Histiocytic sarcoma','Lymphoma','Osteosarcoma','Hemangiosarcoma','Oral melanoma','Other / not sure']
UNKNOWN = "I don't know"

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

st.header('2. Location & travel')
country = st.selectbox('Country', ['USA','Canada','Australia','United Kingdom','Other'])
location = st.text_input('ZIP / postal code / city (optional)')
travel = st.selectbox('How far could you travel for a trial?', ['Local only','Up to 100 miles','Up to 300 miles','Anywhere in the U.S.','International if needed'])

st.header('3. Diagnosis')
diagnosis_status = st.selectbox('How certain is the diagnosis?', ['Confirmed by pathology/cytology','Suspected / not confirmed',UNKNOWN])
cancer = st.selectbox('Cancer type', CANCERS)
subtype = st.text_input('Exact wording from pathology/cytology, if known')
grade = st.text_input('Grade, if known')

st.header('4. Disease right now')
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

st.header('5. Treatment history')
surgery = st.selectbox('Surgery', ['No','Yes',UNKNOWN])
chemo = st.selectbox('Chemotherapy', ['Never','Currently receiving','Previously received',UNKNOWN])
chemo_details = st.text_input('Chemotherapy drugs + last treatment date, if known')
radiation = st.selectbox('Radiation to this tumor', ['Never','Previously received','Currently receiving',UNKNOWN])
steroids = st.selectbox('Prednisone / other corticosteroids', ['Never / no','Prescribed but NOT started','Currently taking','Previously took',UNKNOWN])
steroid_details = st.text_input('Steroid name, dose, first/last dose date, if known')
immunosuppressive = st.selectbox('Other immunosuppressive medication', ['No','Yes',UNKNOWN])
archived_tissue = st.selectbox('Is archived tumor tissue available?', ['Yes','No',UNKNOWN])

st.header('6. What would you consider?')
prefs = st.multiselect('Select all that you would consider', ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug','Observational / sample-only study'], default=['Immunotherapy','Targeted therapy','Experimental drug'])
radiation_affordability = st.selectbox('If radiation is relevant', ['Would consider radiation','Would consider it if trial-funded','Would not consider radiation',UNKNOWN])

st.header('7. Anything important we missed?')
notes = st.text_area('Optional notes', placeholder='Other illnesses, medications, staging results, pathology details, etc.')

search_clicked = st.button('Find potential trials', type='primary', use_container_width=True)

if search_clicked:
    if diagnosis_status != 'Confirmed by pathology/cytology':
        st.warning('We cannot make a reliable treatment-trial match until the cancer diagnosis is confirmed. Save the pathology/cytology result and search again after confirmation.')
    elif species != 'Dog':
        st.info('This early beta catalog currently contains canine trials only. Feline oncology trials are planned for the expanded catalog.')
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
            if excluded:
                continue
            reasons.append(f'{cancer} matches the study disease category')
            reasons.append('diagnosis reported as confirmed')
            if tumor_status == 'Tumor still present / measurable': reasons.append('gross/measurable tumor reported')
            if tumor_status in ['Completely removed — clean margins','Removed — incomplete/dirty margins','Removed — margins unknown','No evidence of disease (NED)']:
                unknown.append('whether this study accepts patients after tumor removal / without measurable disease')
            confidence='Likely match' if not unknown else 'Possible match'
            matches.append((confidence,tr,reasons,unknown))

        st.header('Results')
        if not matches:
            st.warning('No potential matches were found in this **small beta catalog**. This does not mean no suitable clinical trial exists. The catalog is still being expanded.')
        else:
            st.success(f'{len(matches)} trial(s) may be worth contacting')
            for confidence,tr,reasons,unknown in matches:
                with st.container(border=True):
                    st.markdown(f"### {confidence} · {tr['center']}")
                    st.markdown(f"**{tr['title']}**")
                    st.markdown('**Why it may fit:** ' + '; '.join(reasons) + '.')
                    if unknown:
                        st.markdown('⚠️ **Need to confirm:** ' + '; '.join(unknown) + '.')
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
