import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾")
st.title("Catalog test")

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

st.success(f"Catalog loaded: {len(by_id)} records")
st.write("If you can see this, the JSON catalog is not causing the blank screen.")
