import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="centered")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Oncology Options", icon="🧬"),
]

page = st.navigation(PAGES, position="hidden")

# Compact, always-visible navigation. Keep both choices on one row on mobile,
# but make the labels easier to notice and tap than the default page links.
st.markdown(
    """
    <style>
    div[data-testid="stPageLink"] a {
        min-height: 3.15rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.08rem;
        font-weight: 650;
        padding: 0.55rem 0.65rem;
        border: 1px solid rgba(128,128,128,.32);
        border-radius: 0.65rem;
        white-space: nowrap;
    }
    div[data-testid="stPageLink"] p {
        font-size: 1.08rem;
        font-weight: 650;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="small")
with left:
    st.page_link("pages/1_Clinical_Trial_Finder.py", label="Clinical Trials", icon="🐾", use_container_width=True)
with right:
    st.page_link("pages/2_Additional_Oncology_Options.py", label="Other Options", icon="🧬", use_container_width=True)

page.run()