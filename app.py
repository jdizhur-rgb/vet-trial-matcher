import streamlit as st
from contextlib import contextmanager
import json, urllib.error, urllib.request

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="wide")
PAGES=[st.Page("pages/1_Clinical_Trial_Finder.py",title="Clinical Trial Finder",icon="🐾",default=True),st.Page("pages/2_Additional_Oncology_Options.py",title="Additional Oncology Options",icon="🧬")]
page=st.navigation(PAGES,position="hidden")
st.markdown("""<style>
.stMainBlockContainer,div[data-testid="stMainBlockContainer"]{max-width:1120px!important;padding:1rem 1.5rem 2rem!important}
.nav-row{margin-bottom:.65rem}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]){gap:.55rem!important;margin:0 0 .65rem!important}div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div{min-width:0!important;flex:1 1 50%!important;width:50%!important}div[data-testid="stPageLink"]{margin:0!important;padding:0!important}div[data-testid="stPageLink"] a{min-height:2.35rem;display:flex;align-items:center;justify-content:center;border:1px solid rgba(100,130,190,.24)!important;border-radius:.65rem!important;padding:.22rem .65rem!important}div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div:nth-child(1) a{background:#eee8ff!important;color:#3b237a!important}div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div:nth-child(2) a{background:#e8f3ff!important;color:#155ca8!important}div[data-testid="stPageLink"] p{font-size:.9rem!important;font-weight:700!important;color:inherit!important;white-space:nowrap!important}
@media(min-width:901px){
 div[data-testid="stMainBlockContainer"] h1{font-size:1.85rem!important;line-height:1.1!important;margin:.15rem 0 .2rem!important}
 div[data-testid="stMainBlockContainer"] h2{font-size:1.18rem!important;line-height:1.15!important;margin:.45rem 0 .12rem!important}
 div[data-testid="stMainBlockContainer"] h3{font-size:1.05rem!important}
 div[data-testid="stMainBlockContainer"] p{line-height:1.3!important}
 div[data-testid="stMainBlockContainer"] [data-testid="stAlert"]{margin:.2rem 0!important;padding:.42rem .65rem!important}
 div[data-testid="stMainBlockContainer"] [data-testid="stExpander"]{margin:.15rem 0 .25rem!important}
 div[data-testid="stMainBlockContainer"] [data-testid="stExpander"] details summary{min-height:2.25rem!important;padding:.25rem .6rem!important}
 div[data-testid="stMainBlockContainer"] div[data-testid="stVerticalBlock"]{gap:.38rem!important}
 div[data-testid="stMainBlockContainer"] label p,div[data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] p{font-size:.9rem!important;line-height:1.2!important}
 div[data-testid="stMainBlockContainer"] [data-baseweb="select"]>div,div[data-testid="stMainBlockContainer"] [data-testid="stNumberInput"] input,div[data-testid="stMainBlockContainer"] [data-testid="stTextInput"] input{min-height:2.15rem!important;font-size:.9rem!important}
 div[data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]{min-height:1.8rem!important}
 .desktop-section-title{font-size:1rem;font-weight:700;margin:.3rem 0 .05rem}
}
@media(max-width:900px){.stMainBlockContainer,div[data-testid="stMainBlockContainer"]{padding:4.1rem 1rem 2rem!important;max-width:none!important}div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]){gap:0!important;border:1px solid rgba(100,160,220,.24);border-radius:1rem;overflow:hidden}div[data-testid="stPageLink"] a{border:0!important;border-radius:0!important}}
</style>""",unsafe_allow_html=True)
nav_left,nav_right=st.columns(2,gap="small")
with nav_left:st.page_link("pages/1_Clinical_Trial_Finder.py",label="Clinical Trials",icon="🐾",use_container_width=True)
with nav_right:st.page_link("pages/2_Additional_Oncology_Options.py",label="Other Options",icon="🧬",use_container_width=True)

_orig={n:getattr(st,n) for n in ["markdown","title","header","selectbox","checkbox","number_input","radio","text_input","multiselect","expander","link_button","write"]}
_layout={"section":None,"slots":[],"extra":0,"treatment":False};_pending={"contact":None,"sites":None,"url":None};_selected_region={"value":None};_deferred={"args":None,"kwargs":None}
_treatment_labels={"Surgery","Osteosarcoma surgery","Hemangiosarcoma surgery","Chemotherapy","Prior or current cancer immunotherapy","Radiation to this tumor","Prednisone / other corticosteroids","Other immunosuppressive medication"}
_europe={"Europe — all countries","UK","United Kingdom","France","Belgium","Netherlands","The Netherlands","Italy","Portugal","Spain","Sweden","Switzerland","Germany","Austria","Czechia","Czech Republic","Poland","Denmark","Finland","Norway","Ireland","Hungary","Slovenia","Cyprus"}
_feedback_text="If a trial team says your pet is not eligible, please save the reason. Those real-world exclusions are especially useful for improving the matcher. Do not post private medical or contact information publicly."
_SUPABASE_URL="https://bvghrabcfrexvynlyhqb.supabase.co";_SUPABASE_KEY=st.secrets.get("SUPABASE_KEY","")

def _section(name,title,spec):
    _orig["markdown"](f'<div class="desktop-section-title">{title}</div>',unsafe_allow_html=True);_layout.update(section=name,slots=st.columns(spec,gap="small",wrap=True),extra=0)
def _extra(n):
    i=_layout["extra"]
    if i and i%n==0:_layout["slots"]=st.columns(n,gap="small",wrap=True)
    t=_layout["slots"][i%n];_layout["extra"]+=1;return t
def _target(label):
    s=_layout["section"];a=_layout["slots"]
    if s=="pet" and a:
        m={"Species":0,"I know the age":1,"Age (years)":1,"I know the weight":2,"Weight unit":2,"Weight (lb)":2,"Weight (kg)":2,"Sex":3,"Country / region":4};return a[m[label]] if label in m else None
    if s=="diagnosis" and a:return a[0] if label=="Cancer type" or label.startswith("Enter the diagnosis") else a[1]
    if s=="disease" and a:
        m={"Current tumor status":0,"Is the brain tumor currently present on imaging?":0,"Metastases":1,"Has your veterinarian said the disease is localized?":2};return a[m[label]] if label in m else _extra(3)
    if s=="treatment":return _extra(4)
    if s=="options" and a:return a[0]
    return None
def _render(kind,label,*args,**kwargs):
    t=_target(label);return getattr(t,kind)(label,*args,**kwargs) if t is not None else _orig[kind](label,*args,**kwargs)
def title(body,*a,**k):return _orig["title"]("🐾 Clinical Trial Finder" if isinstance(body,str) and "Vet Cancer Trial Finder" in body else body,*a,**k)
def header(body,*a,**k):
    if body=="1. Your pet":_section("pet","1. Your pet",[1,1,1.15,1.2,1.35]);return
    if body=="2. Diagnosis":_section("diagnosis","2. Diagnosis",[1.65,1]);return
    if body=="3. Current disease":_section("disease","3. Current disease",3);return
    if body=="4. Treatment":_layout["section"]="treatment_pending";return
    if body=="5. Treatment options":_section("options","5. Treatment options" if _layout["treatment"] else "4. Treatment options",1);return
    return _orig["header"](body,*a,**k)
def selectbox(label,*args,**kwargs):
    if label in _treatment_labels and _layout["section"]=="treatment_pending":_section("treatment","4. Treatment",4);_layout["treatment"]=True
    if label=="Country / region":
        opts=list(args[0] if args else kwargs.get("options",[]));priority=["USA","UK","United Kingdom","Europe — all countries"];ordered=[x for x in priority if x in opts];ordered += [x for x in opts if x not in ordered]
        if args:args=(ordered,*args[1:])
        else:kwargs=dict(kwargs,options=ordered)
        r=_render("selectbox",label,*args,**kwargs);_selected_region["value"]=r;return r
    if label=="How certain is the diagnosis?":_deferred.update(args=args,kwargs=dict(kwargs));opts=args[0] if args else kwargs.get("options",[]);return st.session_state.get("diagnosis_confirmation",opts[0] if opts else None)
    if label=="Cancer type":
        r=_render("selectbox",label,*args,**kwargs)
        if _deferred["args"] is not None:
            kw=dict(_deferred["kwargs"] or {},key="diagnosis_confirmation");_target("How certain is the diagnosis?").selectbox("How certain is the diagnosis?",*_deferred["args"],**kw);_deferred.update(args=None,kwargs=None)
        return r
    return _render("selectbox",label,*args,**kwargs)
def checkbox(label,*a,**k):return _render("checkbox",label,*a,**k)
def number_input(label,*a,**k):return _render("number_input",label,*a,**k)
def radio(label,*a,**k):return _render("radio",label,*a,**k)
def text_input(label,*a,**k):return _render("text_input",label,*a,**k)
def multiselect(label,*a,**k):return _render("multiselect",label,*a,**k)
def markdown(body,*a,**k):
    if isinstance(body,str):
        if body.startswith("### ") and " · " in body:
            confidence,center=body[4:].split(" · ",1);confidence={"Potential broad-treatment trial — prescreening required":"Prescreening required","Trial to review — cancer type not specified":"Trial to review"}.get(confidence,confidence);_orig["markdown"](f"### {confidence}");st.caption(center);return
        if body.startswith("**Study type:**"):return
        if body.startswith("**Why it may fit:**"):return _orig["markdown"]("**Why:** "+body.replace("**Why it may fit:**","",1).strip().rstrip(".")+".")
        if body.startswith("**Needs confirmation:**"):return _orig["markdown"]("**Confirm:** "+body.replace("**Needs confirmation:**","",1).strip().rstrip(".")+".")
        if body.startswith("**Contact:**"):_pending["contact"]=body.replace("**Contact:**","",1).strip();return
        if body.startswith("**Participating sites:**"):_pending["sites"]=body.replace("**Participating sites:**","",1).strip();return
    return _orig["markdown"](body,*a,**k)
def write(body,*a,**k):
    if body==_feedback_text:
        _orig["write"]("If a trial team says your pet is not eligible, you can share the reason without providing your name or email.")
        with st.expander("Share eligibility feedback"):
            with st.form("eligibility_feedback_form",clear_on_submit=True):
                trial=_orig["text_input"]("Trial / center",max_chars=300);reason=st.text_area("Reason the trial team said your pet was not eligible",max_chars=2000);st.caption("No name or email is required. Please do not include identifying information.");sent=st.form_submit_button("Submit feedback",use_container_width=True)
                if sent:
                    if not trial.strip() or not reason.strip():st.warning("Please enter the trial / center and the reason given by the trial team.")
                    elif not _SUPABASE_KEY:st.error("Feedback service is not configured.")
                    else:
                        try:
                            data=json.dumps({"trial_center":trial.strip(),"exclusion_reason":reason.strip()}).encode();req=urllib.request.Request(f"{_SUPABASE_URL}/rest/v1/eligibility_feedback",data=data,method="POST",headers={"apikey":_SUPABASE_KEY,"Content-Type":"application/json","Prefer":"return=minimal"});urllib.request.urlopen(req,timeout=10);st.success("Thank you. Your feedback was submitted.")
                        except Exception:st.error("Feedback could not be submitted. Please try again later.")
        return
    return _orig["write"](body,*a,**k)
def link_button(label,url,*a,**k):
    if label=="Official study page":_pending["url"]=url;return
    return _orig["link_button"](label,url,*a,**k)
@contextmanager
def expander(label,*a,**k):
    if label=="Study details":
        with _orig["expander"]("Details & contact",*a,**k):
            if _selected_region["value"] in _europe:_orig["markdown"]("**Enrollment:** European trials often recruit through the investigator or referral center without a separate online enrollment form. Contact the study team to confirm that enrollment/slots are currently open.")
            if _pending["contact"]:_orig["markdown"](f"**Contact:** {_pending['contact']}")
            if _pending["sites"]:_orig["markdown"](f"**Participating sites:** {_pending['sites']}")
            if _pending["url"]:_orig["link_button"]("Official study page",_pending["url"],use_container_width=True)
            _pending.update(contact=None,sites=None,url=None);yield
    else:
        with _orig["expander"](label,*a,**k):yield
st.title=title;st.header=header;st.selectbox=selectbox;st.checkbox=checkbox;st.number_input=number_input;st.radio=radio;st.text_input=text_input;st.multiselect=multiselect;st.markdown=markdown;st.write=write;st.link_button=link_button;st.expander=expander
try:page.run()
finally:
    for n,v in _orig.items():setattr(st,n,v)
