import streamlit as st

PAGES = [
    st.Page(
        "pages/1_Clinical_Trial_Finder.py",
        title="Clinical Trial Finder",
        icon="🐾",
        default=True,
    ),
    st.Page(
        "pages/2_Additional_Oncology_Options.py",
        title="More Treatment Options",
        icon="💊",
    ),
]

page = st.navigation(PAGES, position="hidden")
page.run()
