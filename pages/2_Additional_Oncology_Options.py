import streamlit as st
from pathlib import Path
import runpy, importlib.util

# Navigation is rendered once globally by app.py.
if "main_treatment_route" not in st.session_state:
    st.session_state.main_treatment_route="centers"

route=st.session_state.main_treatment_route
if route=="centers":
    helper=Path(__file__).with_name("_oncology_center_finder.py")
    spec=importlib.util.spec_from_file_location("oncology_center_finder",helper)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
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
    _markdown=st.markdown
    _write=st.write
    def _section_markdown(body,*args,**kwargs):
        if isinstance(body,str) and "💊 More Treatment Options" in body:
            label="🧬 Advanced Treatments" if route=="advanced" else "🧪 Expanded Access"
            body=f"<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>{label}</div>"
        return _markdown(body,*args,**kwargs)
    def _section_write(body,*args,**kwargs):
        if body=="Explore treatment access beyond standard clinical trials.":
            body="Explore advanced and less-common cancer treatment options." if route=="advanced" else "Explore compassionate and expanded-access treatment pathways."
        return _write(body,*args,**kwargs)
    st.markdown=_section_markdown
    st.write=_section_write
    try:runpy.run_path(str(Path(__file__).with_name("_additional_oncology_legacy.py")),run_name="__main__")
    finally:
        st.markdown=_markdown
        st.write=_write
