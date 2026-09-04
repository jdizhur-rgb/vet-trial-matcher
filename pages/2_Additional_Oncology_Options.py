import streamlit as st

OPTIONS = [
    {"id":"hsa-fidocure-genomic-guidance","species":"Dog","cancers":["Hemangiosarcoma"],"situations":["Splenic hemangiosarcoma"],"name":"FidoCure genomic guidance","summary":"Tumor genomic profiling to guide targeted therapy after splenic hemangiosarcoma diagnosis.","access":"USA — ordered and managed through the treating veterinarian/oncologist; FFPE tumor tissue can be used.","evidence":"Retrospective real-world comparative evidence. A 2025 Scientific Reports study analyzed 508 dogs with splenic hemangiosarcoma; treatment records were available for 421 dogs from 257 U.S. veterinary practices. In stage II disease, median overall survival was 249 days with chemotherapy plus targeted therapy versus 141 days with chemotherapy; in stage III, 139 versus 89 days.","evidence_level":"Comparative real-world clinical evidence","sample":"FFPE tumor tissue / pathology material","travel":"No research-center travel inherently required","url":"https://www.nature.com/articles/s41598-025-89862-9","access_url":"https://fidocure.com/for-veterinarians/","limitations":"Retrospective observational data; treatment selection and other confounding factors may influence outcomes. Do not generalize this HSA evidence to other cancers."},
    {"id":"bcell-lymphoma-apavac-vaxkit","species":"Dog","cancers":["B-cell lymphoma"],"situations":["Newly diagnosed / treatment planning","Tumor or lymph-node tissue available"],"name":"APAVAC / Vaxkit","summary":"Personalized autologous tumor vaccine used alongside chemotherapy for B-cell lymphoma.","access":"North America / Europe — veterinarian-directed autologous vaccine platform. North American access is marketed as Vaxkit; European access as APAVAC.","evidence":"Comparative clinical cohort evidence. A published series compared 152 dogs receiving chemotherapy plus APAVAC with 148 dogs receiving chemotherapy alone. Reported lymphoma-specific median survival was 401 versus 220 days; in DLBCL, one-year survival was 51% versus 20%.","evidence_level":"Comparative clinical cohort evidence","sample":"Adequate fresh/autologous tumor or lymph-node tissue is required for vaccine preparation. Confirm collection requirements before biopsy/excision.","travel":"Potentially usable through the treating veterinarian; confirm current U.S./European distribution before tissue collection.","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC6554898/","access_url":"https://vaxkit.com/","limitations":"Not a randomized contemporary standard-of-care trial. Evidence should not be extrapolated to solid tumors simply because the platform is commercially offered for other cancers."},
    {"id":"gilvetmab-mct","species":"Dog","cancers":["Mast cell tumor"],"situations":["Stage I–III mast cell tumor"],"name":"Gilvetmab","summary":"Anti-PD-1 immunotherapy available through veterinary oncology specialists for canine mast cell tumor.","access":"USA — available through veterinary oncology specialists under USDA conditional licensure.","evidence":"Prospective multicenter clinical efficacy data support activity in mast cell tumors. Gilvetmab is included here because it is an officially available regulated veterinary oncology therapy, not because uncontrolled data prove superiority over standard treatment.","evidence_level":"Regulated veterinary therapy + prospective clinical data","sample":"No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.","travel":"Usually through a veterinary oncology specialist in the USA","url":"https://pubmed.ncbi.nlm.nih.gov/42247661/","access_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","limitations":"The published efficacy study was single-arm. This is not evidence that gilvetmab is superior to appropriate surgery, radiation, chemotherapy, or targeted therapy for an individual dog."},
    {"id":"gilvetmab-melanoma","species":"Dog","cancers":["Oral melanoma","Melanoma — other"],"situations":["Stage II–III malignant melanoma"],"name":"Gilvetmab","summary":"Anti-PD-1 immunotherapy available through veterinary oncology specialists for canine malignant melanoma.","access":"USA — available through veterinary oncology specialists under USDA conditional licensure.","evidence":"Prospective multicenter clinical efficacy data support activity in malignant melanoma. Gilvetmab is included because it is an officially available regulated veterinary oncology therapy.","evidence_level":"Regulated veterinary therapy + prospective clinical data","sample":"No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.","travel":"Usually through a veterinary oncology specialist in the USA","url":"https://pubmed.ncbi.nlm.nih.gov/42247661/","access_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","limitations":"The published efficacy study was single-arm. Do not infer superiority over appropriate local control or other standard treatment from response-rate data alone."},
]

st.markdown("## 🧬 Other Options")
st.write("A short list of non-routine treatment options with enough clinical evidence and current access to be worth discussing with a veterinary oncologist.")
with st.expander("How options qualify"):
    st.write("Experimental, off-label, precision, or research-derived ideas are not shown without meaningful comparative clinical evidence. A regulated veterinary oncology therapy may be included without a comparator when it has prospective clinical efficacy data and a real specialist-access pathway. Options shown to perform worse than an appropriate standard treatment are excluded.")

species=st.selectbox("1. Species",["Dog","Cat"])
available_cancers=sorted({c for x in OPTIONS if x["species"]==species for c in x["cancers"]})
cancer=st.selectbox("2. Cancer type",["Select cancer type"]+available_cancers)
if cancer=="Select cancer type":
    if species=="Cat": st.info("No cat-specific additional option currently passes this evidence and access screen. Clinical trials and standard oncology care may still be available.")
    else: st.caption("Choose a cancer type to continue.")
else:
    cancer_matches=[x for x in OPTIONS if x["species"]==species and cancer in x["cancers"]]
    situations=sorted({s for x in cancer_matches for s in x["situations"]})
    situation=st.selectbox("3. Clinical situation",["Show all relevant situations"]+situations)
    matches=cancer_matches if situation=="Show all relevant situations" else [x for x in cancer_matches if situation in x["situations"]]
    if not matches:
        st.info("No additional evidence-screened option currently matches this situation. This does not mean there are no standard treatments or clinical trials.")
    else:
        st.success(f"{len(matches)} additional option{'s' if len(matches)!=1 else ''} found to discuss with a veterinary oncologist.")
        for x in matches:
            with st.container(border=True):
                st.subheader(x["name"])
                st.write(x["summary"])
                st.caption("Best match: "+" · ".join(x["situations"]))
                with st.expander("Evidence"):
                    st.markdown(f"**Evidence level:** {x['evidence_level']}")
                    st.write(x["evidence"])
                    st.link_button("Clinical evidence",x["url"],use_container_width=True)
                with st.expander("Access & sample"):
                    st.markdown(f"**Current access:** {x['access']}")
                    st.markdown(f"**Sample:** {x['sample']}")
                    st.markdown(f"**Travel:** {x['travel']}")
                    st.link_button("How to access",x["access_url"],use_container_width=True)
                with st.expander("Limitations"):
                    st.write(x["limitations"])

st.caption("Discussion prompts for a veterinary oncologist, not treatment recommendations or eligibility determinations. Evidence and access can change. Last review: September 4, 2026.")