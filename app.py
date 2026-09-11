import streamlit as st

st.set_page_config(
    page_title="Vet Cancer Treatment Finder",
    page_icon="🐾",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stMainBlockContainer, div[data-testid="stMainBlockContainer"] {
        max-width: 1120px !important;
        padding: 2.2rem 1.2rem 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

st.markdown("### 🐾 Cancer Clinical Trial Finder for Dogs & Cats")
st.caption("Find cancer clinical trials, research studies, and investigational treatment options.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🐾 Clinical Trials", use_container_width=True, key="nav_trials"):
        st.switch_page("pages/1_Clinical_Trial_Finder.py")
with c2:
    if st.button("🏥 Oncology Centers", use_container_width=True, key="nav_centers"):
        st.session_state.main_treatment_route = "centers"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c3:
    if st.button("🧬 Advanced Treatments", use_container_width=True, key="nav_advanced"):
        st.session_state.main_treatment_route = "advanced"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c4:
    if st.button("🧪 Expanded Access", use_container_width=True, key="nav_expanded"):
        st.session_state.main_treatment_route = "compassionate"
        st.switch_page("pages/2_Additional_Oncology_Options.py")

page.run()

st.markdown("[Follow us on Facebook](https://www.facebook.com/share/1YmSPexTr1/)")
