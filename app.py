import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="centered")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Oncology Options", icon="🧬"),
]

page = st.navigation(PAGES, position="hidden")

# Compact, always-visible mobile navigation.
left, right = st.columns(2, gap="small")
with left:
    st.page_link("pages/1_Clinical_Trial_Finder.py", label="Trials", icon="🐾", use_container_width=True)
with right:
    st.page_link("pages/2_Additional_Oncology_Options.py", label="Other options", icon="🧬", use_container_width=True)

page.run()