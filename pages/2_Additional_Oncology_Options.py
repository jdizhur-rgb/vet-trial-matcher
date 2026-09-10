import streamlit as st
from pathlib import Path
import runpy, importlib.util

st.markdown("""<style>
/* Secondary navigation inside More Treatment Options: compact tabs, visually
   subordinate to the two main site buttons. Keep all three in one row on mobile. */
div[data-testid="stHorizontalBlock"]:has(.st-key-main_route_centers){
  display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;
  gap:.38rem!important;align-items:stretch!important;margin:.05rem 0 .55rem!important;
}
div[data-testid="stHorizontalBlock"]:has(.st-key-main_route_centers) > div[data-testid="stColumn"]{
  width:auto!important;min-width:0!important;flex:1 1 0!important;
}
.st-key-main_route_centers button,.st-key-main_route_advanced button,.st-key-main_route_compassionate button{
  width:100%!important;min-height:2.35rem!important;padding:.28rem .42rem!important;
  border-radius:10px!important;font-size:.82rem!important;line-height:1.08!important;
  font-weight:600!important;white-space:normal!important;box-shadow:none!important;
}
.st-key-main_route_centers button{background-color:#eef6fb!important;border-color:#cadfeb!important;color:#285b7a!important}
.st-key-main_route_advanced button{background-color:#e8f2f8!important;border-color:#c2d9e7!important;color:#245674!important}
.st-key-main_route_compassionate button{background-color:#e1edf4!important;border-color:#b8d1df!important;color:#1f4f6c!important}
@media(max-width:520px){
 .st-key-main_route_centers button,.st-key-main_route_advanced button,.st-key-main_route_compassionate button{
   min-height:2.55rem!important;padding:.24rem .25rem!important;font-size:.74rem!important;
 }
}
.st-key-route_ect,.st-key-route_advanced,.st-key-route_compassionate{display:none!important}
</style>""",unsafe_allow_html=True)

if "main_treatment_route" not in st.session_state: st.session_state.main_treatment_route="centers"
c1,c2,c3=st.columns(3,gap="small")
with c1:
    if st.button("🏥 Oncology Centers",use_container_width=True,key="main_route_centers"):st.session_state.main_treatment_route="centers"
with c2:
    if st.button("🧬 Advanced Treatments",use_container_width=True,key="main_route_advanced"):st.session_state.main_treatment_route="advanced"
with c3:
    if st.button("🧪 Expanded Access",use_container_width=True,key="main_route_compassionate"):st.session_state.main_treatment_route="compassionate"

route=st.session_state.main_treatment_route
if route=="centers":
    helper=Path(__file__).with_name("_oncology_center_finder.py")
    spec=importlib.util.spec_from_file_location("oncology_center_finder",helper)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    # The external locator's current HTML can merge several hospital cards into one.
    # Public results use only individually curated/verified center records until that
    # feed can be normalized offline.
    mod._locator_centers=lambda: []
    mod.EXTRAS.extend([
        {"center":"San Francisco Animal Medical Center","address":"2343 Fillmore St","city":"San Francisco","region":"CA","zip":"94115","phone":"415-465-6291","website":"https://www.sfamc.com/specialty-care/oncology","services":["Medical oncology","ECT"]},
        {"center":"Animal Cancer Care Clinic – Melbourne","address":"901 Jordan Blass Dr","city":"Melbourne","region":"FL","zip":"32940","phone":"407-930-6679","website":"https://animalcancercareclinic.com/","services":["Medical oncology","Chemotherapy","ECT","Immunotherapy","Surgical oncology"]},
        {"center":"BluePearl Pet Hospital – Arden Hills","address":"1285 Grey Fox Rd Suite 100","city":"Arden Hills","region":"MN","zip":"55112","phone":"763-754-5000","website":"https://bluepearlvet.com/hospital/arden-hills-mn/specialties-services/oncology/","services":["Medical oncology","ECT"]},
        {"center":"Veterinary Oncology Services – Manhattan","address":"700 Columbus Ave","city":"New York","region":"NY","zip":"10025","phone":"888-658-6568","website":"https://petcancerinformation.com/areas-we-serve/manhattan","services":["Medical oncology","Chemotherapy","ECT","Immunotherapy","Gene-electrotransfer","T-cell therapy"]}
    ])
    try:mod.load_centers.clear()
    except Exception:pass
    mod.render()
else:
    st.session_state.treatment_option_route=("🧬 Advanced / Novel Treatments" if route=="advanced" else "🧪 Compassionate / Expanded Access")
    runpy.run_path(str(Path(__file__).with_name("_additional_oncology_legacy.py")),run_name="__main__")
