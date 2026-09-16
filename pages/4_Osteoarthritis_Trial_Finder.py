import json
from pathlib import Path
import streamlit as st

UNKNOWN = "I don't know"

st.set_page_config(page_title="Osteoarthritis Trial Finder", page_icon="🐾", layout="centered")

with (Path(__file__).resolve().parents[1] / "data" / "oa_trials.json").open(encoding="utf-8") as fh:
    TRIALS = json.load(fh)

st.title("🐾 Osteoarthritis & joint pain trial finder")
st.caption(f"{len(TRIALS)} current treatment protocols in this research prototype")
st.write("Answer what you know. Choosing **I don't know** keeps a study for review instead of excluding it.")
st.info("This prototype identifies potentially relevant studies from public criteria. The study team determines final eligibility.")

st.header("1. Your pet")
c1, c2 = st.columns(2)
with c1:
    species = st.selectbox("Species", ["Dog", "Cat"])
    age_known = st.checkbox("I know the age", value=True)
    age = st.number_input("Age (years)", 0.0, 30.0, 8.0, 0.5, disabled=not age_known)
with c2:
    weight_known = st.checkbox("I know the weight")
    weight_unit = st.radio("Weight unit", ["lb", "kg"], horizontal=True, disabled=not weight_known)
    weight = st.number_input(f"Weight ({weight_unit})", 0.1, 250.0, 40.0, 0.5, disabled=not weight_known)
    weight_kg = None if not weight_known else (weight if weight_unit == "kg" else weight / 2.2046226218)

st.header("2. Joint problem")
diagnosis = st.selectbox("Has osteoarthritis been diagnosed?", ["Yes", "Suspected / mobility problem only", UNKNOWN])
xray = st.selectbox("Has osteoarthritis been confirmed on X-rays?", ["Yes", "No", UNKNOWN])
joints = st.multiselect("Affected joint(s), if known", ["Shoulder", "Elbow", "Hip", "Stifle / knee", "Carpus / wrist", "Tarsus / ankle", "Multiple / other", UNKNOWN])
lameness = st.selectbox("Does your pet have visible lameness?", ["Yes", "No", UNKNOWN])
mobility = st.selectbox("Does your pet have noticeable mobility problems?", ["Yes", "No", UNKNOWN])
duration_known = st.checkbox("I know roughly how long symptoms have been present")
symptom_months = st.number_input("Months with pain / lameness / mobility problems", 0, 240, 6, disabled=not duration_known)
hip_dysplasia = st.selectbox("If hip arthritis: has hip dysplasia been diagnosed?", ["Yes", "No", UNKNOWN]) if "Hip" in joints else UNKNOWN

st.header("3. Current and previous treatment")
librela = st.selectbox("Has your dog ever received Librela?", ["Yes", "No", UNKNOWN], disabled=species != "Dog") if species == "Dog" else "No"
current_meds = st.multiselect("Current pain / arthritis treatment", ["NSAID", "Gabapentin", "Other pain medication", "Joint supplement", "Steroid", "Joint injection / PRP / stem cells", "Rehabilitation", "None", UNKNOWN])
prior_joint_procedure = st.selectbox("Previous joint surgery or joint injection?", ["Yes", "No", UNKNOWN])

st.header("4. Other health issues")
other_ortho = st.selectbox("Another orthopedic problem affecting walking?", ["Yes", "No", UNKNOWN])
neurologic = st.selectbox("Neurologic disease affecting walking (for example IVDD)?", ["Yes", "No", UNKNOWN])
immune = st.selectbox("Immune-mediated joint/systemic disease?", ["Yes", "No", UNKNOWN])
indoor_only = st.selectbox("For cats: does your cat live indoors only?", ["Yes", "No", UNKNOWN], disabled=species != "Cat") if species == "Cat" else "Yes"


def evaluate(tr):
    if tr.get("species") != species or tr.get("status_confidence") != "current":
        return None
    req = tr.get("requires", {})
    exc = tr.get("excludes", {})
    reasons, unknown = [], []

    min_age, max_age = req.get("min_age_years"), req.get("max_age_years")
    if min_age is not None:
        if age_known and age < min_age: return None
        if not age_known: unknown.append(f"minimum age {min_age:g} years")
    if max_age is not None:
        if age_known and age > max_age: return None
        if not age_known: unknown.append(f"maximum age {max_age:g} years")
    min_w, max_w = req.get("min_weight_kg"), req.get("max_weight_kg")
    if min_w is not None:
        if weight_known and weight_kg < min_w: return None
        if not weight_known: unknown.append(f"minimum weight {min_w:g} kg")
    if max_w is not None:
        if weight_known and weight_kg > max_w: return None
        if not weight_known: unknown.append(f"maximum weight {max_w:g} kg")

    if req.get("radiographic_oa"):
        if xray == "No": unknown.append("OA must be confirmed radiographically at screening")
        elif xray == UNKNOWN: unknown.append("radiographic OA confirmation")
        else: reasons.append("OA reported as confirmed on X-rays")
    if req.get("oa_or_mobility_problem"):
        if diagnosis == "Yes" or mobility == "Yes": reasons.append("OA or mobility problem reported")
        elif diagnosis == UNKNOWN or mobility == UNKNOWN: unknown.append("OA or qualifying mobility problem")
        else: return None
    if req.get("lameness"):
        if lameness == "No": return None
        if lameness == UNKNOWN: unknown.append("required lameness")
        else: reasons.append("lameness reported")
    if req.get("mobility_problem"):
        if mobility == "No": return None
        if mobility == UNKNOWN: unknown.append("required mobility impairment")
        else: reasons.append("mobility impairment reported")

    allowed_joints = req.get("affected_joint")
    known_joints = [j for j in joints if j != UNKNOWN]
    if allowed_joints:
        if known_joints and not set(known_joints).intersection(allowed_joints): return None
        if not known_joints: unknown.append("affected joint requirement: " + ", ".join(allowed_joints))
        else: reasons.append("affected joint matches the public criteria")

    if req.get("hip_dysplasia_related"):
        if hip_dysplasia == "No": return None
        if hip_dysplasia == UNKNOWN: unknown.append("hip dysplasia as the cause of hip OA")
        else: reasons.append("hip dysplasia reported")
    if req.get("min_symptom_months"):
        need = req["min_symptom_months"]
        if duration_known and symptom_months < need: return None
        if not duration_known: unknown.append(f"symptoms present for at least {need} months")
        else: reasons.append(f"symptom duration meets the published minimum ({need} months)")
    if req.get("indoor_only"):
        if indoor_only == "No": return None
        if indoor_only == UNKNOWN: unknown.append("indoor-only requirement")
        else: reasons.append("indoor-only requirement reported as met")
    if req.get("decreased_muscle_mass"):
        unknown.append("decreased muscle mass must be confirmed by the study team")
    if req.get("supplement_washout_days") and "Joint supplement" in current_meds:
        unknown.append(f"joint-supplement washout of about {req['supplement_washout_days']} days")

    if exc.get("prior_librela"):
        if librela == "Yes": return None
        if librela == UNKNOWN: unknown.append("whether previous Librela excludes participation")
    if exc.get("joint_instability") or exc.get("other_orthopedic_disease") or exc.get("non_oa_gait_problem"):
        if other_ortho == "Yes": return None
        if other_ortho == UNKNOWN: unknown.append("other orthopedic causes of gait problems")
    if exc.get("neurologic_gait_disease"):
        if neurologic == "Yes": return None
        if neurologic == UNKNOWN: unknown.append("neurologic disease affecting gait")
    if exc.get("immune_mediated_disease"):
        if immune == "Yes": return None
        if immune == UNKNOWN: unknown.append("immune-mediated disease exclusion")

    if not reasons:
        reasons.append("no known public criterion rules this study out")
    confidence = "Potential match" if not unknown else "Possible match — needs confirmation"
    return confidence, tr, reasons, list(dict.fromkeys(unknown))


if st.button("Find potential trials", type="primary", use_container_width=True):
    matches = [m for tr in TRIALS if (m := evaluate(tr)) is not None]
    if not matches:
        st.warning("No current study in this prototype matches the information entered. This does not mean no study exists; criteria and enrollment can change.")
    else:
        matches.sort(key=lambda x: (x[0] != "Potential match", x[1]["center"]))
        st.success(f"{len(matches)} potential or possible matches")
        for confidence, tr, reasons, unknown in matches:
            with st.container(border=True):
                st.subheader(tr["title"])
                st.write(f"**{confidence}**")
                st.write(f"**Center:** {tr['center']}")
                st.write(f"**Treatment:** {tr.get('intervention', 'See study page')}")
                st.write("**Why it may fit:** " + "; ".join(reasons) + ".")
                if unknown:
                    st.write("**Needs confirmation:** " + "; ".join(unknown) + ".")
                st.write(tr.get("notes", ""))
                st.link_button("Official study page", tr["url"], use_container_width=True)
                st.caption(f"Status: {tr.get('status', '')} · Last verified: {tr.get('verified', '')}")

st.caption("Research prototype on the OA branch. The cancer matcher and production data are unchanged.")
