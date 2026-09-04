import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="centered")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Treatment Options", icon="🧬"),
]

page = st.navigation(PAGES, position="hidden")

# Always-visible navigation for mobile users. Do not rely on the collapsed sidebar.
left, right = st.columns(2)
with left:
    st.page_link("pages/1_Clinical_Trial_Finder.py", label="Clinical Trials", icon="🐾", use_container_width=True)
with right:
    st.page_link("pages/2_Additional_Oncology_Options.py", label="Additional Options", icon="🧬", use_container_width=True)

st.divider()
page.run()
