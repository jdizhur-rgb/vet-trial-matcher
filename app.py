import streamlit as st
from visit_counter import record_visit

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="wide")

PAGES = [
    st.Page("pages/1_Clinical_Trial_Finder.py", title="Clinical Trial Finder", icon="🐾", default=True),
    st.Page("pages/2_Additional_Oncology_Options.py", title="Additional Oncology Options", icon="🧬"),
    st.Page("pages/3_Private_Stats.py", title="Visit Stats", url_path="private-stats-9f4c2"),
]
page = st.navigation(PAGES, position="hidden")
if getattr(page, "url_path", "") != "private-stats-9f4c2":
    record_visit()

# 1.58-safe presentation layer only: CSS + stable widget wrappers.
# Deliberately avoids st.columns(..., wrap=...), st.html JS injection,
# and components monkey-patching used by the newer Streamlit build.
st.markdown("""
<style>
.stMainBlockContainer, div[data-testid="stMainBlockContainer"] {
    max-width: 1120px !important;
    padding: 3.25rem 1.5rem 2rem !important;
}
.nav-title {font-size:1.55rem;line-height:1.08;font-weight:700;margin:.45rem 0 .12rem;color:#55483f}
.nav-title .paw {color:#9a6a43;font-family:Arial,sans-serif}
.nav-subtitle {font-size:.92rem;color:#6f6a66;margin:0 0 .35rem}
.beta-corner {display:none}
.intro-answer {font-size:.94rem;color:#45414a;margin:.25rem 0 .55rem}
.desktop-section-title {font-size:1rem;font-weight:700;margin:.3rem 0 .05rem}
div[data-testid="stAlert"] {background:#edf7ef!important;border:0!important;box-shadow:none!important;color:#285b38!important}
div[data-testid="stAlert"]>div {background:transparent!important;border:0!important;box-shadow:none!important}
div[data-testid="stAlert"] p {color:#285b38!important}
@media(min-width:901px) {
  div[data-testid="stMainBlockContainer"] h1 {font-size:1.55rem!important;line-height:1.08!important;margin:.1rem 0 .15rem!important;color:#55483f!important}
  div[data-testid="stMainBlockContainer"] h2 {font-size:1.12rem!important;line-height:1.15!important;margin:.4rem 0 .1rem!important}
  div[data-testid="stMainBlockContainer"] h3 {font-size:1.02rem!important}
  div[data-testid="stMainBlockContainer"] p {line-height:1.28!important}
  div[data-testid="stMainBlockContainer"] [data-testid="stAlert"] {margin:.15rem 0!important;padding:.28rem .55rem!important;font-size:.84rem!important}
  div[data-testid="stMainBlockContainer"] [data-testid="stAlert"] p {font-size:.84rem!important;line-height:1.22!important}
  div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] {margin:.12rem 0 .22rem!important}
  div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] details summary {min-height:2.15rem!important;padding:.2rem .55rem!important}
  div[data-testid="stMainBlockContainer"] div[data-testid="stVerticalBlock"] {gap:.35rem!important}
  div[data-testid="stMainBlockContainer"] label p,
  div[data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] p {font-size:.9rem!important;line-height:1.2!important}
  div[data-testid="stMainBlockContainer"] [data-baseweb="select"]>div,
  div[data-testid="stMainBlockContainer"] [data-testid="stNumberInput"] input,
  div[data-testid="stMainBlockContainer"] [data-testid="stTextInput"] input {min-height:2.1rem!important;font-size:.9rem!important}
  div[data-testid="stMainBlockContainer"] [data-testid="stCheckbox"] {min-height:1.75rem!important}
  div.st-key-pet_age_known, div.st-key-pet_weight_known {margin-top:-.62rem!important;margin-bottom:-.2rem!important}
  div.st-key-weight_unit_compact [role="radiogroup"] {display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;gap:.55rem!important;align-items:center!important}
  div.st-key-weight_unit_compact [role="radiogroup"] label {margin:0!important;white-space:nowrap!important}
}
@media(max-width:900px) {
  .stMainBlockContainer, div[data-testid="stMainBlockContainer"] {padding:4rem 1rem 2rem!important;max-width:none!important}
  .nav-title {font-size:1.4rem}
  .nav-subtitle {font-size:.86rem}
}
</style>
""", unsafe_allow_html=True)

_orig = {name: getattr(st, name) for name in [
    "markdown", "title", "header", "selectbox", "checkbox", "number_input",
    "radio", "text_input", "multiselect"
]}
_layout = {"section": None, "slots": [], "extra": 0, "treatment": False,
           "age_value": None, "weight_unit": None, "weight_value": None}
_deferred = {"args": None, "kwargs": None}
_treatment_labels = {
    "Surgery", "Osteosarcoma surgery", "Hemangiosarcoma surgery", "Chemotherapy",
    "Prior or current cancer immunotherapy", "Radiation to this tumor",
    "Prednisone / other corticosteroids", "Other immunosuppressive medication"
}

def _columns(spec):
    # Streamlit 1.58 supports gap, but not wrap.
    return st.columns(spec, gap="small")

def _section(name, title, spec):
    _orig["markdown"](f'<div class="desktop-section-title">{title}</div>', unsafe_allow_html=True)
    _layout.update(section=name, slots=_columns(spec), extra=0)

def _extra(n):
    i = _layout["extra"]
    if i and i % n == 0:
        _layout["slots"] = _columns(n)
    target = _layout["slots"][i % n]
    _layout["extra"] += 1
    return target

def _target(label):
    section, slots = _layout["section"], _layout["slots"]
    if section == "pet" and slots:
        mapping = {"Species": 0, "Sex": 3, "Country / region": 4}
        return slots[mapping[label]] if label in mapping else None
    if section == "diagnosis" and slots:
        return slots[0] if label == "Cancer type" or label.startswith("Enter the diagnosis") else slots[1]
    if section == "disease" and slots:
        mapping = {"Current tumor status": 0, "Is the brain tumor currently present on imaging?": 0,
                   "Metastases": 1, "Has your veterinarian said the disease is localized?": 2}
        return slots[mapping[label]] if label in mapping else _extra(3)
    if section == "treatment":
        return _extra(4)
    if section == "options" and slots:
        return slots[0]
    return None

def _render(kind, label, *args, **kwargs):
    target = _target(label)
    return getattr(target, kind)(label, *args, **kwargs) if target is not None else _orig[kind](label, *args, **kwargs)

def title(body, *args, **kwargs):
    if isinstance(body, str) and "Vet Cancer Trial Finder" in body:
        _orig["markdown"]('<div class="nav-title"><span class="paw">🐾︎</span> Clinical Trial Finder</div><div class="nav-subtitle">Find treatment-focused veterinary cancer trials for dogs and cats.</div>', unsafe_allow_html=True)
        return None
    return _orig["title"](body, *args, **kwargs)

def header(body, *args, **kwargs):
    if body == "1. Your pet": _section("pet", "1. Your pet", [1.15,1.15,1.4,1.2,1.35]); return
    if body == "2. Diagnosis": _section("diagnosis", "2. Diagnosis", [1.65,1]); return
    if body == "3. Current disease": _section("disease", "3. Current disease", 3); return
    if body == "4. Treatment": _layout["section"] = "treatment_pending"; return
    if body == "5. Treatment options": _section("options", "5. Treatment options" if _layout["treatment"] else "4. Treatment options", 1); return
    return _orig["header"](body, *args, **kwargs)

def selectbox(label, *args, **kwargs):
    if label in _treatment_labels and _layout["section"] == "treatment_pending":
        _section("treatment", "4. Treatment", 4); _layout["treatment"] = True
    if label == "Country / region":
        options = list(args[0] if args else kwargs.get("options", []))
        priority = ["USA", "UK", "United Kingdom", "Europe — all countries"]
        ordered = [x for x in priority if x in options] + [x for x in options if x not in priority]
        if args: args = (ordered, *args[1:])
        else: kwargs = dict(kwargs, options=ordered)
        return _render("selectbox", label, *args, **kwargs)
    if label == "How certain is the diagnosis?":
        _deferred.update(args=args, kwargs=dict(kwargs))
        options = args[0] if args else kwargs.get("options", [])
        return st.session_state.get("diagnosis_confirmation", options[0] if options else None)
    if label == "Cancer type":
        result = _render("selectbox", label, *args, **kwargs)
        if _deferred["args"] is not None:
            kw = dict(_deferred["kwargs"] or {}, key="diagnosis_confirmation")
            _target("How certain is the diagnosis?").selectbox("How certain is the diagnosis?", *_deferred["args"], **kw)
            _deferred.update(args=None, kwargs=None)
        return result
    return _render("selectbox", label, *args, **kwargs)

def checkbox(label, *args, **kwargs):
    if _layout["section"] == "pet" and label == "I know the age":
        with _layout["slots"][1]:
            kwargs = dict(kwargs, key="pet_age_known")
            result = _orig["checkbox"]("Age", *args, **kwargs)
            _layout["age_value"] = st.empty()
            return result
    if _layout["section"] == "pet" and label == "I know the weight":
        with _layout["slots"][2]:
            kwargs = dict(kwargs, key="pet_weight_known")
            result = _orig["checkbox"]("Weight", *args, **kwargs)
            row = _columns([1.15,1.55])
            _layout["weight_unit"], _layout["weight_value"] = row[0].empty(), row[1].empty()
            return result
    return _render("checkbox", label, *args, **kwargs)

def number_input(label, *args, **kwargs):
    if _layout["section"] == "pet" and label == "Age (years)" and _layout["age_value"] is not None:
        kwargs = dict(kwargs, label_visibility="collapsed")
        with _layout["age_value"].container(): return _orig["number_input"](label, *args, **kwargs)
    if _layout["section"] == "pet" and label in {"Weight (lb)", "Weight (kg)"} and _layout["weight_value"] is not None:
        kwargs = dict(kwargs, label_visibility="collapsed")
        with _layout["weight_value"].container(): return _orig["number_input"](label, *args, **kwargs)
    return _render("number_input", label, *args, **kwargs)

def radio(label, *args, **kwargs):
    if _layout["section"] == "pet" and label == "Weight unit" and _layout["weight_unit"] is not None:
        kwargs = dict(kwargs, horizontal=True, label_visibility="collapsed", key="weight_unit_compact")
        with _layout["weight_unit"].container(): return _orig["radio"](label, *args, **kwargs)
    return _render("radio", label, *args, **kwargs)

def text_input(label, *args, **kwargs): return _render("text_input", label, *args, **kwargs)
def multiselect(label, *args, **kwargs): return _render("multiselect", label, *args, **kwargs)

def markdown(body, *args, **kwargs):
    if isinstance(body, str):
        if body.startswith("Answer what you know."):
            _orig["markdown"](f'<div class="intro-answer">{body}</div>', unsafe_allow_html=True)
            return
        if body.startswith("### ") and " · " in body:
            confidence, center = body[4:].split(" · ", 1)
            confidence = {"Potential broad-treatment trial — prescreening required":"Prescreening required", "Trial to review — cancer type not specified":"Trial to review"}.get(confidence, confidence)
            _orig["markdown"](f"### {confidence}"); st.caption(center); return
        if body.startswith("**Study type:**"): return
        if body.startswith("**Why it may fit:**"):
            return _orig["markdown"]("**Why:** " + body.replace("**Why it may fit:**", "", 1).strip().rstrip(".") + ".")
        if body.startswith("**Needs confirmation:**"):
            return _orig["markdown"]("**Confirm:** " + body.replace("**Needs confirmation:**", "", 1).strip().rstrip(".") + ".")
    return _orig["markdown"](body, *args, **kwargs)

st.title = title
st.header = header
st.selectbox = selectbox
st.checkbox = checkbox
st.number_input = number_input
st.radio = radio
st.text_input = text_input
st.multiselect = multiselect
st.markdown = markdown

page.run()
