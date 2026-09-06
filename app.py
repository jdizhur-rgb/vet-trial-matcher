import streamlit as st
from visit_counter import record_visit

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="wide")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Oncology Options", icon="🧬"),
    st.Page("pages/3_Private_Stats.py", title="Visit Stats", url_path="private-stats-9f4c2"),
]

page = st.navigation(PAGES, position="hidden")
if getattr(page, "url_path", "") != "private-stats-9f4c2":
    record_visit()

st.markdown("""
<style>
.stMainBlockContainer, div[data-testid="stMainBlockContainer"] {
    max-width: 1120px !important;
    padding: 3.4rem 1.5rem 2rem !important;
}
@media(max-width:900px) {
    .stMainBlockContainer, div[data-testid="stMainBlockContainer"] {
        padding: 4.1rem 1rem 2rem !important;
        max-width: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

page.run()
