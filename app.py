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
        title="Cancer",
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

if page.title == "Oncology Tools":
    if st.button(
        "← Back to cancer trial finder",
        key="back_to_cancer_finder",
        use_container_width=False,
    ):
        st.switch_page("pages/1_Clinical_Trial_Finder.py")

page.run()
