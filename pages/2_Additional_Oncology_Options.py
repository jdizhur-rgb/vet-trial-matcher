import streamlit as st
from pathlib import Path
import runpy

st.markdown("""<style>
.st-key-main_route_centers button{background-color:#e7f2fa!important;border-color:#bfd8e9!important;color:#285b7a!important}
.st-key-main_route_advanced button{background-color:#d6e9f6!important;border-color:#a9cce3!important;color:#245674!important}
.st-key-main_route_compassionate button{background-color:#c5dfef!important;border-color:#91bdd8!important;color:#1f4f6c!important}
.st-key-main_route_centers button,.st-key-main_route_advanced button,.st-key-main_route_compassionate button{border-radius:12px!important;min-height:3.25rem!important;font-weight:500!important}
/* The preserved legacy renderer still contains its old route controls. Hide them; this page owns navigation now. */
.st-key-route_ect,.st-key-route_advanced,.st-key-route_compassionate{display:none!important}
</style>""",unsafe_allow_html=True)

if "main_treatment_route" not in st.session_state:
    st.session_state.main_treatment_route="centers"

c1,c2,c3=st.columns(3)
with c1:
    if st.button("🏥 Find an Oncology Center",use_container_width=True,key="main_route_centers"):
        st.session_state.main_treatment_route="centers"
with c2:
    if st.button("🧬 Advanced / Novel Treatments",use_container_width=True,key="main_route_advanced"):
        st.session_state.main_treatment_route="advanced"
with c3:
    if st.button("🧪 Compassionate / Expanded Access",use_container_width=True,key="main_route_compassionate"):
        st.session_state.main_treatment_route="compassionate"

route=st.session_state.main_treatment_route
if route=="centers":
    from _oncology_center_finder import render
    render()
else:
    # Reuse the last known-good implementation for the two existing treatment sections.
    st.session_state.treatment_option_route=(
        "🧬 Advanced / Novel Treatments" if route=="advanced" else "🧪 Compassionate / Expanded Access"
    )
    runpy.run_path(str(Path(__file__).with_name("_additional_oncology_legacy.py")),run_name="__main__")
