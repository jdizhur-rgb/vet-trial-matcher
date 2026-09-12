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

# Shared presentation only. Keep this layer deliberately passive: no monkey-
# patching Streamlit functions, no component interception, and no dependence on
# generated class names or internal widget order.
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
    </style>
    """,
    unsafe_allow_html=True,
)

page.run()
