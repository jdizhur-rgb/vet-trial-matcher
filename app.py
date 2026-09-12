import streamlit as st

st.set_page_config(
    page_title="Vet Cancer Treatment Finder",
    page_icon="🐾",
    layout="wide",
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

# Shared presentation only. No monkey-patching Streamlit functions or component
# interception; navigation uses ordinary Streamlit buttons and switch_page.
st.markdown(
    """
    <style>
    .stMainBlockContainer,
    div[data-testid="stMainBlockContainer"] {
        max-width: 1120px !important;
        padding: 3.4rem 1.5rem 2rem !important;
    }

    div[data-testid="stMainBlockContainer"] h1 {
        color: #55483f !important;
        font-size: 1.55rem !important;
        line-height: 1.08 !important;
        margin: .1rem 0 .15rem !important;
    }

    div[data-testid="stMainBlockContainer"] h2 {
        font-size: 1.12rem !important;
        line-height: 1.15 !important;
        margin: .55rem 0 .12rem !important;
    }

    div[data-testid="stMainBlockContainer"] h3 {
        font-size: 1.02rem !important;
        line-height: 1.16 !important;
        margin: .15rem 0 .1rem !important;
    }

    div[data-testid="stMainBlockContainer"] p {
        line-height: 1.32 !important;
        margin-top: .18rem !important;
        margin-bottom: .34rem !important;
    }

    div.st-key-nav_trials button {
        min-height: 2.9rem !important;
        width: 100% !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border-radius: .8rem !important;
        background: #eee8ff !important;
        color: #3b237a !important;
        border: 1px solid #ddd2ff !important;
        box-shadow: none !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.st-key-nav_centers) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: .38rem !important;
        align-items: stretch !important;
        margin: .45rem 0 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.st-key-nav_centers) > div[data-testid="stColumn"] {
        width: auto !important;
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    .st-key-nav_centers button,
    .st-key-nav_advanced button,
    .st-key-nav_expanded button {
        width: 100% !important;
        min-height: 2.55rem !important;
        padding: .28rem .35rem !important;
        border-radius: 10px !important;
        font-size: .82rem !important;
        line-height: 1.08 !important;
        font-weight: 600 !important;
        white-space: normal !important;
        box-shadow: none !important;
    }

    .st-key-nav_centers button {
        background: #eef6fb !important;
        border-color: #cadfeb !important;
        color: #285b7a !important;
    }

    .st-key-nav_advanced button {
        background: #e8f2f8 !important;
        border-color: #c2d9e7 !important;
        color: #245674 !important;
    }

    .st-key-nav_expanded button {
        background: #e1edf4 !important;
        border-color: #b8d1df !important;
        color: #1f4f6c !important;
    }

    div[data-testid="stAlert"] {
        background: #edf7ef !important;
        border: 0 !important;
        box-shadow: none !important;
        color: #285b38 !important;
    }

    div[data-testid="stAlert"] p {
        color: #285b38 !important;
    }

    div[data-testid="stMainBlockContainer"] label p,
    div[data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] p {
        font-size: .92rem !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stMainBlockContainer"] [data-baseweb="select"] > div,
    div[data-testid="stMainBlockContainer"] [data-testid="stNumberInput"] input,
    div[data-testid="stMainBlockContainer"] [data-testid="stTextInput"] input {
        min-height: 2.15rem !important;
        font-size: .92rem !important;
    }

    div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] {
        margin: .14rem 0 .24rem !important;
    }

    div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] details summary {
        min-height: 2.2rem !important;
        padding: .22rem .58rem !important;
    }

    @media (max-width: 900px) {
        .stMainBlockContainer,
        div[data-testid="stMainBlockContainer"] {
            max-width: none !important;
            padding: 4.1rem 1rem 2rem !important;
        }
    }

    @media (max-width: 520px) {
        .st-key-nav_centers button,
        .st-key-nav_advanced button,
        .st-key-nav_expanded button {
            min-height: 3.15rem !important;
            padding: .22rem .2rem !important;
            font-size: .76rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button("🐾︎ Clinical Trials", key="nav_trials", use_container_width=True):
    st.switch_page("pages/1_Clinical_Trial_Finder.py")

c1, c2, c3 = st.columns(3, gap="small")
with c1:
    if st.button("🏥 Oncology Centers", key="nav_centers", use_container_width=True):
        st.session_state.main_treatment_route = "centers"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c2:
    if st.button("🧬 Advanced Treatments", key="nav_advanced", use_container_width=True):
        st.session_state.main_treatment_route = "advanced"
        st.switch_page("pages/2_Additional_Oncology_Options.py")
with c3:
    if st.button("🧪 Expanded Access", key="nav_expanded", use_container_width=True):
        st.session_state.main_treatment_route = "compassionate"
        st.switch_page("pages/2_Additional_Oncology_Options.py")

page.run()
