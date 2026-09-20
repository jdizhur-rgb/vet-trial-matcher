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
        "pages/4_Osteoarthritis_Trial_Finder.py",
        title="Osteoarthritis / joint pain",
        icon="🦴",
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

if page.title == "Cancer":
    active_finder = "Cancer"
elif page.title == "Osteoarthritis / joint pain":
    active_finder = "Osteoarthritis / joint pain"
else:
    active_finder = None

selected_finder = st.segmented_control(
    "Find trials for",
    ["Cancer", "Osteoarthritis / joint pain"],
    default=active_finder,
    key="condition_navigation_tools" if active_finder is None else "condition_navigation",
    label_visibility="collapsed",
)
if selected_finder != active_finder:
    if selected_finder == "Cancer":
        st.switch_page("pages/1_Clinical_Trial_Finder.py")
    elif selected_finder == "Osteoarthritis / joint pain":
        st.switch_page("pages/4_Osteoarthritis_Trial_Finder.py")

page.run()
