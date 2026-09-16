import streamlit as st

st.set_page_config(
    page_title="Vet Treatment Trial Finder",
    page_icon="🐾",
    layout="wide",
)

PAGES = [
    st.Page(
        "pages/1_Clinical_Trial_Finder.py",
        title="Cancer Trial Finder",
        icon="🐾",
        default=True,
    ),
    st.Page(
        "pages/4_Osteoarthritis_Trial_Finder.py",
        title="Osteoarthritis Trial Finder",
        icon="🦴",
    ),
    st.Page(
        "pages/2_Additional_Oncology_Options.py",
        title="More Oncology Options",
        icon="💊",
    ),
]

page = st.navigation(PAGES)
page.run()
