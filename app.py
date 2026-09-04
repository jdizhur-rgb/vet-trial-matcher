import streamlit as st
from contextlib import contextmanager
import json
import urllib.error
import urllib.request

st.set_page_config(page_title="Vet Cancer Treatment Finder", page_icon="🐾", layout="wide")
PAGES=[st.Page("pages/1_Clinical_Trial_Finder.py",title="Clinical Trial Finder",icon="🐾",default=True),st.Page("pages/2_Additional_Oncology_Options.py",title="Additional Oncology Options",icon="🧬")]
page=st.navigation(PAGES,position="hidden")

st.markdown("""
<style>
.stMainBlockContainer,div[data-testid="stMainBlockContainer"]{max-width:1240px!important;padding:1.25rem 2rem 2.5rem!important}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]){gap:.65rem!important;margin:0 0 .8rem!important}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div{min-width:0!important;flex:1 1 50%!important;width:50%!important}
div[data-testid="stPageLink"]{margin:0!important;padding:0!important}
div[data-testid="stPageLink"] a{min-height:2.55rem;display:flex;align-items:center;justify-content:center;border:1px solid rgba(100,160,220,.22)!important;border-radius:.7rem!important;padding:.3rem .8rem!important}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div:nth-child(1) a{background:#eee8ff!important;color:#3b237a!important}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"])>div:nth-child(2) a{background:#e8f3ff!important;color:#155ca8!important}
div[data-testid="stPageLink"] p{font-size:.95rem!important;font-weight:700!important;color:inherit!important;white-space:nowrap!important}
@media(max-width:900px){.stMainBlockContainer,div[data-testid="stMainBlockContainer"]{padding:4.1rem 1rem 2rem!important;max-width:none!important}div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]){gap:0!important;border:1px solid rgba(100,160,220,.24);border-radius:1rem;overflow:hidden}div[data-testid="stPageLink"] a{border:0!important;border-radius:0!important}}
</style>
""",unsafe_allow_html=True)
left,right=st.columns(2,gap="small")
with left:st.page_link("pages/1_Clinical_Trial_Finder.py",label="Clinical Trials",icon="🐾",use_container_width=True)
with right:st.page_link("pages/2_Additional_Oncology_Options.py",label="Other Options",icon="🧬",use_container_width=True)

_original_markdown=st.markdown;_original_title=st.title;_original_header=st.header;_original_selectbox=st.selectbox;_original_expander=st.expander;_original_link_button=st.link_button;_original_write=st.write
_pending={"contact":None,"sites":None,"url":None};_treatment_section={"pending":False,"shown":False};_deferred_diagnosis={"args":None,"kwargs":None};_selected_region={"value":None}
_europe_regions={"Europe — all countries","UK","United Kingdom","France","Belgium","Netherlands","The Netherlands","Italy","Portugal","Spain","Sweden","Switzerland","Germany","Austria","Czechia","Czech Republic","Poland","Denmark","Finland","Norway","Ireland","Hungary","Slovenia","Cyprus"}
_treatment_history_labels={"Surgery","Osteosarcoma surgery","Hemangiosarcoma surgery","Chemotherapy","Prior or current cancer immunotherapy","Radiation to this tumor","Prednisone / other corticosteroids","Other immunosuppressive medication"}
_feedback_text="If a trial team says your pet is not eligible, please save the reason. Those real-world exclusions are especially useful for improving the matcher. Do not post private medical or contact information publicly."
_SUPABASE_URL="https://bvghrabcfrexvynlyhqb.supabase.co";_SUPABASE_KEY="sb_publishable_Ah5rszPGl4kp5cL8h7ZydA_021AmfKV"
def submit_feedback(trial_center,exclusion_reason):
    payload=json.dumps({"trial_center":trial_center.strip(),"exclusion_reason":exclusion_reason.strip()}).encode("utf-8");req=urllib.request.Request(f"{_SUPABASE_URL}/rest/v1/eligibility_feedback",data=payload,method="POST",headers={"apikey":_SUPABASE_KEY,"Authorization":f"Bearer {_SUPABASE_KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
    with urllib.request.urlopen(req,timeout=10) as response:return 200<=response.status<300
def compact_title(body,*args,**kwargs):
    if isinstance(body,str) and "Vet Cancer Trial Finder" in body:return _original_title("🐾 Clinical Trial Finder")
    return _original_title(body,*args,**kwargs)
def dynamic_header(body,*args,**kwargs):
    if body=="4. Treatment":_treatment_section["pending"]=True;_treatment_section["shown"]=False;return None
    if body=="5. Treatment options":
        number="5" if _treatment_section["shown"] else "4";_treatment_section["pending"]=False;return _original_header(f"{number}. Treatment options",*args,**kwargs)
    return _original_header(body,*args,**kwargs)
def dynamic_selectbox(label,*args,**kwargs):
    if label=="Country / region":
        options=list(args[0] if args else kwargs.get("options",[]));priority=["USA","UK","United Kingdom","Europe — all countries"];ordered=[]
        for item in priority:
            if item in options and item not in ordered:ordered.append(item)
        ordered.extend(item for item in options if item not in ordered)
        if args:args=(ordered,*args[1:])
        else:kwargs=dict(kwargs);kwargs["options"]=ordered
        result=_original_selectbox(label,*args,**kwargs);_selected_region["value"]=result;return result
    if label=="How certain is the diagnosis?":
        _deferred_diagnosis["args"]=args;_deferred_diagnosis["kwargs"]=dict(kwargs);options=args[0] if args else kwargs.get("options",[]);return st.session_state.get("diagnosis_confirmation",options[0] if options else None)
    if label=="Cancer type":
        result=_original_selectbox(label,*args,**kwargs)
        if _deferred_diagnosis["args"] is not None:
            dkwargs=dict(_deferred_diagnosis["kwargs"] or {});dkwargs["key"]="diagnosis_confirmation";_original_selectbox("How certain is the diagnosis?",*_deferred_diagnosis["args"],**dkwargs);_deferred_diagnosis.update(args=None,kwargs=None)
        return result
    if _treatment_section["pending"] and label in _treatment_history_labels:_original_header("4. Treatment");_treatment_section["pending"]=False;_treatment_section["shown"]=True
    return _original_selectbox(label,*args,**kwargs)
def compact_result_markdown(body,*args,**kwargs):
    if isinstance(body,str):
        if body.startswith("### ") and " · " in body:
            confidence,center=body[4:].split(" · ",1)
            if confidence=="Potential broad-treatment trial — prescreening required":confidence="Prescreening required"
            elif confidence=="Trial to review — cancer type not specified":confidence="Trial to review"
            _original_markdown(f"### {confidence}");st.caption(center);return None
        if body.startswith("**Study type:**"):return None
        if body.startswith("**Why it may fit:**"):return _original_markdown("**Why:** "+body.replace("**Why it may fit:**","",1).strip().rstrip(".")+".")
        if body.startswith("**Needs confirmation:**"):return _original_markdown("**Confirm:** "+body.replace("**Needs confirmation:**","",1).strip().rstrip(".")+".")
        if body.startswith("**Contact:**"):_pending["contact"]=body.replace("**Contact:**","",1).strip();return None
        if body.startswith("**Participating sites:**"):_pending["sites"]=body.replace("**Participating sites:**","",1).strip();return None
    return _original_markdown(body,*args,**kwargs)
def feedback_write(body,*args,**kwargs):
    if body==_feedback_text:
        _original_write("If a trial team says your pet is not eligible, you can share the reason without providing your name or email.")
        with st.expander("Share eligibility feedback"):
            with st.form("eligibility_feedback_form",clear_on_submit=True):
                trial=st.text_input("Trial / center",max_chars=300);reason=st.text_area("Reason the trial team said your pet was not eligible",max_chars=2000);st.caption("No name or email is required. Please do not include names, contact information, addresses, medical records, or other identifying information.");sent=st.form_submit_button("Submit feedback",use_container_width=True)
                if sent:
                    if not trial.strip() or not reason.strip():st.warning("Please enter the trial / center and the reason given by the trial team.")
                    else:
                        try:
                            if submit_feedback(trial,reason):st.success("Thank you. Your feedback was submitted.")
                            else:st.error("Feedback could not be submitted. Please try again later.")
                        except (urllib.error.URLError,urllib.error.HTTPError,TimeoutError):st.error("Feedback could not be submitted. Please try again later.")
        return None
    return _original_write(body,*args,**kwargs)
def compact_link_button(label,url,*args,**kwargs):
    if label=="Official study page":_pending["url"]=url;return None
    return _original_link_button(label,url,*args,**kwargs)
@contextmanager
def compact_expander(label,*args,**kwargs):
    if label=="Study details":
        with _original_expander("Details & contact",*args,**kwargs):
            if _selected_region["value"] in _europe_regions:_original_markdown("**Enrollment:** European trials often recruit through the investigator or referral center without a separate online enrollment form. Contact the study team to confirm that enrollment/slots are currently open.")
            if _pending["contact"]:_original_markdown(f"**Contact:** {_pending['contact']}")
            if _pending["sites"]:_original_markdown(f"**Participating sites:** {_pending['sites']}")
            if _pending["url"]:_original_link_button("Official study page",_pending["url"],use_container_width=True)
            _pending.update(contact=None,sites=None,url=None);yield
    else:
        with _original_expander(label,*args,**kwargs):yield
st.title=compact_title;st.header=dynamic_header;st.selectbox=dynamic_selectbox;st.markdown=compact_result_markdown;st.expander=compact_expander;st.link_button=compact_link_button;st.write=feedback_write
try:page.run()
finally:st.title=_original_title;st.header=_original_header;st.selectbox=_original_selectbox;st.markdown=_original_markdown;st.expander=_original_expander;st.link_button=_original_link_button;st.write=_original_write
