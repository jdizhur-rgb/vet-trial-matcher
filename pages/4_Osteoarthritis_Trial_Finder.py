import json
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from oa_matcher import UNKNOWN, PatientProfile, find_matches

st.set_page_config(page_title="Osteoarthritis / joint pain trial finder", page_icon="🦴", layout="centered")

with (ROOT / "data" / "oa_trials.json").open(encoding="utf-8") as fh:
    TRIALS = json.load(fh)

st.title("Osteoarthritis / joint pain trial finder")
st.caption(f"{len(TRIALS)} current treatment protocols")
st.write("Answer what you know. Choosing **I don't know** keeps a study for review instead of excluding it.")
st.info("This tool compares public criteria only. The study team determines final eligibility.")

st.header("1. Your pet")
c1, c2 = st.columns(2)
with c1:
    species = st.selectbox("Species", ["Dog", "Cat"])
    age = st.number_input("Age (years, optional)", 0.0, 30.0, value=None, step=0.5)
with c2:
    weight_unit = st.radio("Weight unit", ["lb", "kg"], horizontal=True)
    weight = st.number_input(f"Weight ({weight_unit}, optional)", 0.1, 250.0, value=None, step=0.5)
    weight_kg = None if weight is None else (weight if weight_unit == "kg" else weight / 2.2046226218)

st.header("2. Joint problem")
diagnosis = st.selectbox("Has osteoarthritis been diagnosed?", ["Yes", "No", UNKNOWN], index=2)
xray = st.selectbox("Has osteoarthritis been confirmed on X-rays?", ["Yes", "No", UNKNOWN], index=2)
joints = st.multiselect("Affected joint(s), if known", ["Shoulder", "Elbow", "Hip", "Stifle / knee", "Carpus / wrist", "Tarsus / ankle", "Multiple / other", UNKNOWN])
lameness = st.selectbox("Does your pet have visible lameness?", ["Yes", "No", UNKNOWN], index=2)
mobility = st.selectbox("Does your pet have noticeable mobility problems?", ["Yes", "No", UNKNOWN], index=2)
symptom_months = st.number_input("Months with pain, lameness or mobility problems (optional)", 0, 240, value=None)
hip_dysplasia = st.selectbox("If hip arthritis: has hip dysplasia been diagnosed?", ["Yes", "No", UNKNOWN]) if "Hip" in joints else UNKNOWN

st.header("3. Current and previous treatment")
librela = st.selectbox("Has your dog ever received Librela?", ["Yes", "No", UNKNOWN], index=2) if species == "Dog" else "No"
solensia = st.selectbox("If your cat receives Solensia, has the dose been stable for at least 3 months?", ["Not receiving", "Yes", "No", UNKNOWN]) if species == "Cat" else "Not receiving"
current_meds = st.multiselect("Current pain / arthritis treatment", ["NSAID", "Gabapentin", "Other pain medication", "Joint supplement", "Steroid", "Rehabilitation", "None", UNKNOWN])
prior_joint_surgery = st.selectbox("Previous surgery on an affected joint?", ["Yes", "No", UNKNOWN], index=2)
prior_joint_injection = st.selectbox("Previous injection into an affected joint?", ["Yes", "No", UNKNOWN], index=2)
prior_prp_or_stem_cells = st.selectbox("Previous PRP or stem-cell treatment in an affected joint?", ["Yes", "No", UNKNOWN], index=2)

st.header("4. Other eligibility questions")
other_ortho = st.selectbox("Another orthopedic problem affecting walking?", ["Yes", "No", UNKNOWN], index=2)
neurologic = st.selectbox("Neurologic disease affecting walking (for example IVDD)?", ["Yes", "No", UNKNOWN], index=2)
immune = st.selectbox("Immune-mediated joint or systemic disease?", ["Yes", "No", UNKNOWN], index=2)
indoor_only = st.selectbox("Does your cat live indoors only?", ["Yes", "No", UNKNOWN]) if species == "Cat" else "Yes"
pregnant = st.selectbox("Is your pet pregnant?", ["Yes", "No", UNKNOWN], index=2)
oral_medication = st.selectbox("Can your pet take oral medication without major stress?", ["Yes", "No", UNKNOWN], index=2)

if st.button("Find potential trials", type="primary", use_container_width=True):
    profile = PatientProfile(
        species=species, age_years=age, weight_kg=weight_kg,
        diagnosis=diagnosis, xray=xray, joints=tuple(joints), lameness=lameness,
        mobility=mobility, symptom_months=symptom_months,
        hip_dysplasia=hip_dysplasia, librela=librela, solensia=solensia,
        current_meds=tuple(current_meds), prior_joint_surgery=prior_joint_surgery,
        prior_joint_injection=prior_joint_injection, prior_prp_or_stem_cells=prior_prp_or_stem_cells,
        other_ortho=other_ortho, neurologic=neurologic, immune=immune,
        indoor_only=indoor_only, pregnant=pregnant, oral_medication=oral_medication,
    )
    matches = find_matches(TRIALS, profile)
    if not matches:
        st.warning("No current study in this prototype matches the information entered. Criteria and enrollment can change.")
    else:
        st.success(f"{len(matches)} potential or possible matches")
        for result in matches:
            tr = result.trial
            with st.container(border=True):
                st.subheader(tr["title"])
                st.write(f"**{result.confidence}**")
                st.write(f"**Center:** {tr['center']}")
                st.write(f"**Treatment:** {tr.get('intervention', 'See study page')}")
                st.write("**Why it may fit:** " + "; ".join(result.reasons) + ".")
                if result.confirmations:
                    st.write("**Needs confirmation:** " + "; ".join(result.confirmations) + ".")
                if tr.get("sites"):
                    site_names = "; ".join(site["hospital"] for site in tr["sites"])
                    st.write(f"**Study site(s):** {site_names}")
                st.write(tr.get("notes", ""))
                st.link_button("Official study page", tr["url"], use_container_width=True)
                st.caption(f"Status: {tr.get('status', '')} · Last verified: {tr.get('verified', '')}")
