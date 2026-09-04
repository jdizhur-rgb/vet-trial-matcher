import streamlit as st

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="centered")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Oncology Options", icon="🧬"),
]

page = st.navigation(PAGES, position="hidden")

# Mobile-first segmented navigation: one compact row, large enough to notice and tap.
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 0 .65rem 0 !important;
        border: 1px solid rgba(100,160,220,.32);
        border-radius: 1.15rem;
        overflow: hidden;
        background: rgba(35,48,65,.55);
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) > div {
        min-width: 0 !important;
        flex: 1 1 50% !important;
        width: 50% !important;
    }
    div[data-testid="stPageLink"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stPageLink"] a {
        min-height: 3.45rem;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 !important;
        padding: .55rem .25rem !important;
        border: 0 !important;
        border-radius: 0 !important;
        background: transparent;
        white-space: nowrap;
    }
    div[data-testid="stPageLink"] a:hover {
        background: rgba(70,130,210,.22);
    }
    div[data-testid="stPageLink"] p {
        font-size: 1.02rem !important;
        line-height: 1.1 !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }
    @media (max-width: 480px) {
        div[data-testid="stPageLink"] a {
            min-height: 3.2rem;
            padding: .45rem .12rem !important;
        }
        div[data-testid="stPageLink"] p {
            font-size: .94rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap=None)
with left:
    st.page_link("pages/1_Clinical_Trial_Finder.py", label="Clinical Trials", icon="🐾", use_container_width=True)
with right:
    st.page_link("pages/2_Additional_Oncology_Options.py", label="Other Options", icon="🧬", use_container_width=True)

# Compact the existing Clinical Trial Finder result cards without touching its
# large curated trial catalog or matching logic. Only the exact result-card
# labels used by that page are transformed; the Additional Options page is
# unaffected.
_original_markdown = st.markdown


def compact_result_markdown(body, *args, **kwargs):
    if isinstance(body, str):
        if body.startswith("### ") and " · " in body:
            heading = body[4:]
            confidence, center = heading.split(" · ", 1)
            _original_markdown(f"### {confidence}")
            st.caption(center)
            return None
        if body.startswith("**Study type:**"):
            st.caption(body.replace("**Study type:**", "Study type:", 1).strip())
            return None
        if body.startswith("**Why it may fit:**"):
            text = body.replace("**Why it may fit:**", "", 1).strip()
            with st.expander("Why it fits"):
                st.write(text)
            return None
        if body.startswith("**Needs confirmation:**"):
            text = body.replace("**Needs confirmation:**", "", 1).strip()
            with st.expander("Eligibility to confirm"):
                st.write(text)
            return None
        if body.startswith("**Contact:**"):
            text = body.replace("**Contact:**", "", 1).strip()
            with st.expander("Contact"):
                st.write(text)
            return None
        if body.startswith("**Participating sites:**"):
            text = body.replace("**Participating sites:**", "", 1).strip()
            with st.expander("Participating sites"):
                st.write(text)
            return None
    return _original_markdown(body, *args, **kwargs)


st.markdown = compact_result_markdown
try:
    page.run()
finally:
    st.markdown = _original_markdown
