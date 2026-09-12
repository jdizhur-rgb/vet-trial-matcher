from pathlib import Path
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

css_path = Path(__file__).resolve().parent / "styles" / "app.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

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

# Small compatibility shim around the legacy matcher page only:
# 1) keep USA as the default country;
# 2) render Cancer type before diagnosis certainty without changing matching logic.
_original_selectbox = st.selectbox
_DIAGNOSIS_OPTIONS = [
    "Confirmed by pathology/cytology",
    "Suspected / not confirmed",
    "I don't know",
]
_DIAGNOSIS_KEY = "diagnosis_certainty_reordered"


def _matcher_selectbox(label, options, *args, **kwargs):
    if label == "Country / region" and "index" not in kwargs:
        values = list(options)
        if "USA" in values:
            kwargs = dict(kwargs, index=values.index("USA"))

    if label == "How certain is the diagnosis?":
        values = list(options)
        if _DIAGNOSIS_KEY not in st.session_state:
            index = kwargs.get("index", 0)
            st.session_state[_DIAGNOSIS_KEY] = values[index]
        return st.session_state[_DIAGNOSIS_KEY]

    if label == "Cancer type":
        cancer_value = _original_selectbox(label, options, *args, **kwargs)
        _original_selectbox(
            "How certain is the diagnosis?",
            _DIAGNOSIS_OPTIONS,
            key=_DIAGNOSIS_KEY,
        )
        return cancer_value

    return _original_selectbox(label, options, *args, **kwargs)


st.selectbox = _matcher_selectbox
try:
    page.run()
finally:
    st.selectbox = _original_selectbox
