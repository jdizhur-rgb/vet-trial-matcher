import streamlit as st
from contextlib import contextmanager

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
    /* Pull the whole app upward; Streamlit's default top padding is excessive on phones. */
    .stMainBlockContainer,
    div[data-testid="stMainBlockContainer"] {
        padding-top: 2.25rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
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
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stHorizontalBlock"] div[data-testid="stPageLink"]) {
        margin-bottom: -1.8rem !important;
    }
    @media (max-width: 480px) {
        .stMainBlockContainer,
        div[data-testid="stMainBlockContainer"] {
            padding-top: 1rem !important;
        }
        div[data-testid="stPageLink"] a {
            min-height: 3.2rem;
            padding: .45rem .12rem !important;
        }
        div[data-testid="stPageLink"] p {
            font-size: .94rem !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stHorizontalBlock"] div[data-testid="stPageLink"]) {
            margin-bottom: -2.35rem !important;
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

# Presentation-only transforms for the large Clinical Trial Finder page.
# The trial catalog and all matching/eligibility logic remain untouched.
_original_markdown = st.markdown
_original_title = st.title
_original_expander = st.expander
_original_link_button = st.link_button
_pending = {"contact": None, "sites": None, "url": None}


def compact_title(body, *args, **kwargs):
    if isinstance(body, str) and "Vet Cancer Trial Finder" in body:
        return _original_markdown("## 🐾 Clinical Trial Finder")
    return _original_title(body, *args, **kwargs)


def compact_result_markdown(body, *args, **kwargs):
    if isinstance(body, str):
        if body.startswith("### ") and " · " in body:
            heading = body[4:]
            confidence, center = heading.split(" · ", 1)
            if confidence == "Potential broad-treatment trial — prescreening required":
                confidence = "Prescreening required"
            elif confidence == "Trial to review — cancer type not specified":
                confidence = "Trial to review"
            _original_markdown(f"### {confidence}")
            st.caption(center)
            return None
        if body.startswith("**Study type:**"):
            return None
        if body.startswith("**Why it may fit:**"):
            text = body.replace("**Why it may fit:**", "", 1).strip().rstrip(".")
            return _original_markdown(f"**Why:** {text}.")
        if body.startswith("**Needs confirmation:**"):
            text = body.replace("**Needs confirmation:**", "", 1).strip().rstrip(".")
            return _original_markdown(f"**Confirm:** {text}.")
        if body.startswith("**Contact:**"):
            _pending["contact"] = body.replace("**Contact:**", "", 1).strip()
            return None
        if body.startswith("**Participating sites:**"):
            _pending["sites"] = body.replace("**Participating sites:**", "", 1).strip()
            return None
    return _original_markdown(body, *args, **kwargs)


def compact_link_button(label, url, *args, **kwargs):
    if label == "Official study page":
        _pending["url"] = url
        return None
    return _original_link_button(label, url, *args, **kwargs)


@contextmanager
def compact_expander(label, *args, **kwargs):
    if label == "Study details":
        with _original_expander("Details & contact", *args, **kwargs):
            if _pending["contact"]:
                _original_markdown(f"**Contact:** {_pending['contact']}")
            if _pending["sites"]:
                _original_markdown(f"**Participating sites:** {_pending['sites']}")
            if _pending["url"]:
                _original_link_button("Official study page", _pending["url"], use_container_width=True)
            _pending.update(contact=None, sites=None, url=None)
            yield
    else:
        with _original_expander(label, *args, **kwargs):
            yield


st.title = compact_title
st.markdown = compact_result_markdown
st.expander = compact_expander
st.link_button = compact_link_button
try:
    page.run()
finally:
    st.title = _original_title
    st.markdown = _original_markdown
    st.expander = _original_expander
    st.link_button = _original_link_button
