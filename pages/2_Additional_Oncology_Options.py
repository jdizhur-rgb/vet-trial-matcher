import streamlit as st
from pathlib import Path
import runpy, importlib.util

# Navigation is rendered only once, globally, in app.py.
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

    # Legacy renderer still contains its old ECT / Advanced / Expanded route buttons.
    # Suppress exactly those controls so only app.py owns site navigation.
    _markdown=st.markdown
    _write=st.write
    _button=st.button

    def _section_markdown(body,*args,**kwargs):
        if isinstance(body,str) and "💊 More Treatment Options" in body:
            label="🧬 Advanced Treatments" if route=="advanced" else "🧪 Expanded Access"
            body=f"<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>{label}</div>"
        return _markdown(body,*args,**kwargs)

    def _section_write(body,*args,**kwargs):
        if body=="Explore treatment access beyond standard clinical trials.":
            body="Explore advanced and less-common cancer treatment options." if route=="advanced" else "Explore compassionate and expanded-access treatment pathways."
        return _write(body,*args,**kwargs)

    def _legacy_button(label,*args,**kwargs):
        if label in {
            "⚡ Electrochemotherapy (ECT)",
            "🧬 Advanced / Novel Treatments",
            "🧪 Compassionate / Expanded Access",
        }:
            return False
        return _button(label,*args,**kwargs)

    st.markdown=_section_markdown
    st.write=_section_write
    st.button=_legacy_button
    st.session_state._hide_legacy_route_buttons=True
    try:
        runpy.run_path(str(Path(__file__).with_name("_additional_oncology_legacy.py")),run_name="__main__")
    finally:
        st.markdown=_markdown
        st.write=_write
        st.button=_button
        st.session_state.pop("_hide_legacy_route_buttons",None)

    if route=="compassionate":
        with st.container(border=True):
            st.markdown("### VMD Sciences — Veterinary Managed / Expanded Access")
            st.write("**Dogs and cats · multiple conditions · veterinarian-requested global treatment access**")
            st.write("A current managed-access pathway for veterinarians seeking a specific treatment that is not available in the patient's region. VMD Sciences helps navigate regulatory approval, sourcing, importation and delivery of eligible veterinary medicines and investigational or specialized therapies.")
            st.write("**Access:** a licensed veterinarian submits the request for the individual patient. Availability is treatment- and country-specific and is not guaranteed. This is an access pathway, not a clinical trial or a promise that a requested drug can be obtained.")
            st.link_button("VMD Sciences treatment access", "https://www.vmdsciences.com/find-a-global-treatment", use_container_width=True)
            st.link_button("Veterinarian importation request", "https://www.vmdsciences.com/veterinarians", use_container_width=True)
