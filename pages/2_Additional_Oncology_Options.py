import streamlit as st

st.set_page_config(page_title="Additional Oncology Options", page_icon="🧬", layout="centered")

OPTIONS = [
    {
        "id": "hsa-fidocure-genomic-guidance",
        "species": "Dog",
        "cancers": ["Hemangiosarcoma"],
        "situation": "Splenic hemangiosarcoma",
        "title": "Tumor genomic profiling to guide targeted therapy (FidoCure)",
        "access": "USA — ordered and managed through the treating veterinarian/oncologist; FFPE tumor tissue can be used.",
        "evidence": "Retrospective real-world comparative evidence. A 2025 Scientific Reports study analyzed 508 dogs with splenic hemangiosarcoma; treatment records were available for 421 dogs from 257 U.S. veterinary practices. In stage II disease, median overall survival was 249 days with chemotherapy plus targeted therapy versus 141 days with chemotherapy; in stage III, 139 versus 89 days. This is not a randomized trial, so the association should not be presented as proof that profiling itself caused the survival difference.",
        "evidence_level": "Comparative real-world clinical evidence",
        "sample": "FFPE tumor tissue / pathology material",
        "travel": "No research-center travel inherently required",
        "url": "https://www.nature.com/articles/s41598-025-89862-9",
        "access_url": "https://fidocure.com/for-veterinarians/",
        "limitations": "Retrospective observational data; treatment selection and other confounding factors may influence outcomes. Do not generalize this HSA evidence to other cancers.",
    },
    {
        "id": "bcell-lymphoma-apavac-vaxkit",
        "species": "Dog",
        "cancers": ["B-cell lymphoma"],
        "situation": "B-cell lymphoma",
        "title": "APAVAC / Vaxkit autologous tumor vaccine added to chemotherapy",
        "access": "North America / Europe — veterinarian-directed autologous vaccine platform. North American access is marketed as Vaxkit; European access as APAVAC.",
        "evidence": "Comparative clinical cohort evidence. A published series compared 152 dogs receiving chemotherapy plus APAVAC with 148 dogs receiving chemotherapy alone. Reported lymphoma-specific median survival was 401 versus 220 days; in DLBCL, one-year survival was 51% versus 20%.",
        "evidence_level": "Comparative clinical cohort evidence",
        "sample": "Adequate fresh/autologous tumor or lymph-node tissue is required for vaccine preparation; confirm collection requirements before biopsy/excision.",
        "travel": "Potentially usable through the treating veterinarian; confirm current U.S./European distribution before tissue collection.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6554898/",
        "access_url": "https://vaxkit.com/",
        "limitations": "Not a randomized contemporary standard-of-care trial. Evidence should not be extrapolated to solid tumors simply because the platform is commercially offered for other cancers.",
    },
    {
        "id": "gilvetmab-mct",
        "species": "Dog",
        "cancers": ["Mast cell tumor"],
        "situation": "Canine mast cell tumor — licensed indication",
        "title": "Gilvetmab (anti-PD-1 immunotherapy)",
        "access": "USA — available through veterinary oncology specialists under USDA conditional licensure.",
        "evidence": "Prospective multicenter clinical efficacy data support activity in mast cell tumors. Gilvetmab is included here because it is an officially available regulated veterinary oncology therapy, not because uncontrolled data prove superiority over standard treatment.",
        "evidence_level": "Regulated veterinary therapy + prospective clinical data",
        "sample": "No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.",
        "travel": "Usually through a veterinary oncology specialist in the USA",
        "url": "https://pubmed.ncbi.nlm.nih.gov/42247661/",
        "access_url": "https://www.merck-animal-health-usa.com/hub/gilvetmab/",
        "limitations": "The published efficacy study was single-arm. This card is not a claim that gilvetmab is superior to surgery, radiation, chemotherapy, or targeted therapy for an individual dog.",
    },
    {
        "id": "gilvetmab-melanoma",
        "species": "Dog",
        "cancers": ["Oral melanoma", "Melanoma — other"],
        "situation": "Canine malignant melanoma — licensed indication",
        "title": "Gilvetmab (anti-PD-1 immunotherapy)",
        "access": "USA — available through veterinary oncology specialists under USDA conditional licensure.",
        "evidence": "Prospective multicenter clinical efficacy data support activity in malignant melanoma. Gilvetmab is included because it is an officially available regulated veterinary oncology therapy.",
        "evidence_level": "Regulated veterinary therapy + prospective clinical data",
        "sample": "No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.",
        "travel": "Usually through a veterinary oncology specialist in the USA",
        "url": "https://pubmed.ncbi.nlm.nih.gov/42247661/",
        "access_url": "https://www.merck-animal-health-usa.com/hub/gilvetmab/",
        "limitations": "The published efficacy study was single-arm. Do not infer superiority over appropriate local control or other standard treatment from response-rate data alone.",
    },
]

st.title("🧬 Additional Options to Discuss With Your Oncologist")
st.write(
    "A deliberately short list of treatment options that are currently accessible in the U.S. or Europe and have enough clinical evidence to justify a specialist discussion. "
    "This is separate from the Clinical Trial Finder. It is not a list of everything experimental that has ever been tried."
)
st.info(
    "Experimental/off-label ideas are not included without meaningful comparative clinical evidence. Regulated veterinary oncology therapies may be included without a comparator when they have prospective clinical efficacy data and a real specialist-access pathway. Options shown to perform worse than an appropriate standard treatment are excluded."
)

species = st.selectbox("Species", ["Dog", "Cat"])
cancer_choices = sorted({c for x in OPTIONS if x["species"] == species for c in x["cancers"]})
cancer = st.selectbox("Cancer type", ["Select cancer type"] + cancer_choices)

if cancer != "Select cancer type":
    matches = [x for x in OPTIONS if x["species"] == species and cancer in x["cancers"]]
    if not matches:
        st.info("No additional evidence-screened option is currently in this category. This does not mean there are no standard treatments or clinical trials.")
    else:
        for x in matches:
            with st.container(border=True):
                st.subheader(x["title"])
                st.markdown(f"**Situation:** {x['situation']}")
                st.markdown(f"**Current access:** {x['access']}")
                st.markdown(f"**Evidence level:** {x['evidence_level']}")
                st.write(x["evidence"])
                st.markdown(f"**Sample requirement:** {x['sample']}")
                st.markdown(f"**Travel/access:** {x['travel']}")
                st.markdown(f"**Important limitations:** {x['limitations']}")
                c1, c2 = st.columns(2)
                with c1:
                    st.link_button("Clinical evidence", x["url"], use_container_width=True)
                with c2:
                    st.link_button("Current access", x["access_url"], use_container_width=True)

st.divider()
st.caption(
    "Evidence and access change. These cards are discussion prompts for a veterinary oncologist, not treatment recommendations or eligibility determinations. "
    "Clinical trials remain in the separate Trial Finder. Last evidence review: September 4, 2026."
)
