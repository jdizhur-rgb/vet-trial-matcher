import streamlit as st

st.set_page_config(
    page_title="Vet Treatment Trial Finder",
    page_icon="🐾",
    layout="wide",
)

PAGES = {
    "Find trials for": [
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
    ],
    "Cancer resources": [
        st.Page(
            "pages/2_Additional_Oncology_Options.py",
            title="More oncology options",
            icon="💊",
        ),
    ],
}

page = st.navigation(PAGES)
page.run()
