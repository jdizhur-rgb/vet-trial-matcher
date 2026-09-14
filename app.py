from pathlib import Path
import streamlit as st

# Preview deployment refresh: compact save controls

st.set_page_config(
    page_title="Vet Cancer Treatment Finder",
    page_icon="🐾",
    layout="wide",
)

PAGES = [
    st.Page(
        "pages/1_Clinical_Trial_Finder.py",
        title="Clinical Trial Finder",
        icon="🐾",
        default=True,
    ),
    st.Page(
        "pages/2_Additional_Oncology_Options.py",
        title="Oncology Tools",
        icon="🏥",
    ),
]

page = st.navigation(PAGES, position="hidden")

css_path = Path(__file__).resolve().parent / "styles" / "app.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("🐾︎ Clinical Trials", key="nav_trials", use_container_width=True):
    st.switch_page("pages/1_Clinical_Trial_Finder.py")

c1, c2, c3 = st.columns(3, gap="small")
with c1:
    if st.button("🏥 Oncology Centers", key="nav_centers", use_container_width=True):
        st.session_state.main_treatment_route = "centers"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c2:
    if st.button("🧬 Advanced Treatments", key="nav_advanced", use_container_width=True):
        st.session_state.main_treatment_route = "advanced"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c3:
    if st.button("🧪 Expanded Access", key="nav_expanded", use_container_width=True):
        st.session_state.main_treatment_route = "compassionate"
        st.switch_page("pages/2_Additional_Oncology_Options.py")

page.run()
