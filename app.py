import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="wide")

root = Path(__file__).resolve().parent
with (root / "data" / "trials_base.json").open(encoding="utf-8") as fh:
    base = json.load(fh)
by_id = {t["id"]: t for t in base}
updates_path = root / "data" / "trial_updates.json"
if updates_path.exists():
    with updates_path.open(encoding="utf-8") as fh:
        doc = json.load(fh)
    for trial_id in doc.get("delete", []):
        by_id.pop(trial_id, None)
    for patch in doc.get("upsert", []):
        trial_id = patch["id"]
        if trial_id in by_id:
            by_id[trial_id].update(patch)
        else:
            by_id[trial_id] = patch

st.title("🐾 Clinical Trial Finder")
st.caption("Find treatment-focused veterinary cancer trials for dogs and cats.")
st.info("Answer what you know. It is completely fine to choose I don’t know.")

species = st.selectbox("Species", ["Dog", "Cat"])
cancer = st.text_input("Cancer type", placeholder="e.g. lymphoma, mast cell tumor, osteosarcoma")
country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Europe", "Other"])
location = st.text_input("City / state / province (optional)")
stage_known = st.radio("Do you know the stage?", ["I don’t know", "Yes", "No"], horizontal=True)
prior_treatment = st.multiselect("Treatments already received (optional)", ["Surgery", "Chemotherapy", "Radiation", "Immunotherapy", "Other"])

st.success(f"Form rendered. Catalog available: {len(by_id)} records")
st.caption("Matching/results are intentionally disabled in this diagnostic test.")
