import streamlit as st

OPTIONS = [
    {"id":"hsa-fidocure-genomic-guidance","species":"Dog","countries":["USA"],"cancers":["Hemangiosarcoma"],"situations":["Splenic hemangiosarcoma"],"name":"FidoCure genomic guidance","summary":"Tumor genomic profiling to guide targeted therapy after splenic hemangiosarcoma diagnosis.","access":"USA — ordered and managed through the treating veterinarian/oncologist; FFPE tumor tissue can be used.","evidence":"Retrospective real-world comparative evidence. A 2025 Scientific Reports study analyzed 508 dogs with splenic hemangiosarcoma; treatment records were available for 421 dogs from 257 U.S. veterinary practices. In stage II disease, median overall survival was 249 days with chemotherapy plus targeted therapy versus 141 days with chemotherapy; in stage III, 139 versus 89 days.","evidence_level":"Comparative real-world clinical evidence","sample":"FFPE tumor tissue / pathology material","travel":"No research-center travel inherently required","url":"https://www.nature.com/articles/s41598-025-89862-9","provider_url":"https://fidocure.com/","access_url":"https://fidocure.com/pet-parents/","access_label":"Start with FidoCure","contact_email":"support@fidocure.com","contact_phone":"855-701-8047","contact_note":"Pet owners can start on FidoCure's current Pet Parents page or ask their veterinarian/oncologist to enroll the patient. FidoCure works directly with the veterinary care team.","limitations":"Retrospective observational data; treatment selection and other confounding factors may influence outcomes. Do not generalize this HSA evidence to other cancers. Current public FidoCure material does not establish a Canadian treatment-access pathway, so Canada is not shown for this option."},
    {"id":"bcell-lymphoma-apavac-vaxkit","species":"Dog","countries":["USA","Canada","Europe"],"cancers":["B-cell lymphoma"],"situations":["Newly diagnosed / treatment planning","Tumor or lymph-node tissue available"],"name":"APAVAC / Vaxkit","summary":"Personalized autologous tumor vaccine used alongside chemotherapy for B-cell lymphoma.","access":"USA / Canada / Europe — veterinarian-directed autologous vaccine platform. Vaxkit is the North American distributor for the U.S. and Canada; European access is through Hastim under the APAVAC name.","evidence":"Comparative clinical evidence includes a randomized placebo-controlled double-blind study in canine DLBCL and a larger comparative clinical cohort. A published series compared 152 dogs receiving chemotherapy plus APAVAC with 148 dogs receiving chemotherapy alone; reported lymphoma-specific median survival was 401 versus 220 days, and in DLBCL one-year survival was 51% versus 20%.","evidence_level":"Randomized clinical evidence + comparative clinical cohort evidence","sample":"Adequate fresh/autologous tumor or lymph-node tissue is required for vaccine preparation. Confirm collection requirements before biopsy/excision.","travel":"Potentially usable through the treating veterinarian. Confirm logistics before tissue collection.","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC6554898/","provider_url":"https://vaxkit.com/","access_url":"https://vaxkit.com/","access_label":"Vaxkit access & contact","contact_email":"info@vaxkit.com","contact_email_europe":"contact@hastim.fr","contact_note":"USA/Canada: contact Vaxkit for access and ordering logistics. Europe: contact Hastim directly for APAVAC. Confirm tissue collection requirements before biopsy/excision.","limitations":"Not a contemporary standard-of-care replacement. Evidence should not be extrapolated to solid tumors simply because the platform is commercially offered for other cancers."},
    {"id":"gilvetmab-mct","species":"Dog","countries":["USA"],"cancers":["Mast cell tumor"],"situations":["Stage I–III mast cell tumor"],"name":"Gilvetmab","summary":"Anti-PD-1 immunotherapy available through veterinary oncology specialists for canine mast cell tumor.","access":"USA — available through specialists practicing veterinary oncology under USDA conditional licensure.","evidence":"Prospective multicenter clinical efficacy data support activity in mast cell tumors.","evidence_level":"Regulated veterinary therapy + prospective clinical data","sample":"No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.","travel":"Treatment is administered intravenously in a veterinary clinic; Merck's current Gilvetmab page directs owners to veterinary oncology specialists.","url":"https://pubmed.ncbi.nlm.nih.gov/42247661/","provider_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","access_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","access_label":"Gilvetmab access / oncologist","contact_phone":"800-521-5767","contact_note":"Gilvetmab is supplied through veterinary oncology specialists. Use Merck's current Gilvetmab page for the specialist-access route; Merck Animal Health Customer Service can answer U.S. product/access questions.","limitations":"The published efficacy study was single-arm. This is not evidence that gilvetmab is superior to appropriate surgery, radiation, chemotherapy, or targeted therapy for an individual dog."},
    {"id":"gilvetmab-melanoma","species":"Dog","countries":["USA"],"cancers":["Oral melanoma","Melanoma — other"],"situations":["Stage II–III malignant melanoma"],"name":"Gilvetmab","summary":"Anti-PD-1 immunotherapy available through veterinary oncology specialists for canine malignant melanoma.","access":"USA — available through specialists practicing veterinary oncology under USDA conditional licensure.","evidence":"Prospective multicenter clinical efficacy data support activity in malignant melanoma.","evidence_level":"Regulated veterinary therapy + prospective clinical data","sample":"No special tumor-manufacturing sample required; oncologist determines diagnostic/staging requirements.","travel":"Treatment is administered intravenously in a veterinary clinic; Merck's current Gilvetmab page directs owners to veterinary oncology specialists.","url":"https://pubmed.ncbi.nlm.nih.gov/42247661/","provider_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","access_url":"https://www.merck-animal-health-usa.com/hub/gilvetmab/","access_label":"Gilvetmab access / oncologist","contact_phone":"800-521-5767","contact_note":"Gilvetmab is supplied through veterinary oncology specialists. Use Merck's current Gilvetmab page for the specialist-access route; Merck Animal Health Customer Service can answer U.S. product/access questions.","limitations":"The published efficacy study was single-arm. Do not infer superiority over appropriate local control or other standard treatment from response-rate data alone."},
    {"id":"torigen-vimclara-cat-solid-tumors","species":"Cat","countries":["USA"],"cancers":["Adenocarcinoma","Solid tumor — other"],"situations":["Tumor tissue available after biopsy or surgery","Post-surgical treatment planning"],"name":"Torigen VimClara autologous cancer vaccine","summary":"Personalized autologous immunotherapy prepared in-clinic from the cat’s own tumor tissue using the VimClara veterinary kit.","access":"USA — veterinarian-directed point-of-care treatment. Ask the treating veterinarian/oncologist to contact Torigen before tissue collection when possible; Torigen supplies VimClara kits and clinic training for dogs, cats and horses.","evidence":"Published feline data primarily establish safety rather than anticancer efficacy. Torigen also cites broader veterinary autologous cancer-vaccine literature, but efficacy for an individual feline tumor type remains uncertain.","evidence_level":"Available veterinary advanced treatment; limited tumor-specific efficacy evidence","sample":"Approximately 5 g of fresh, unfixed tumor tissue is requested in Torigen's current owner/veterinarian material. Confirm collection, storage and timing requirements with Torigen before biopsy/surgery when possible, and before tissue is discarded or fixed.","travel":"May be prepared and administered through a participating/trained veterinary clinic; a university trial center is not inherently required.","url":"https://clinics.torigen.com/hubfs/Torigen%20Literature%202025/VimClara-Only%20Distributor%20Detailer.pdf","provider_url":"https://torigen.com/","access_url":"https://torigen.com/","access_label":"Torigen website","contact_email":"info@torigen.com","contact_phone":"860-519-9956","contact_note":"Veterinarian/clinic should contact Torigen directly to discuss the case, order a VimClara kit and arrange training.","limitations":"VimClara is a veterinary-use point-of-care kit, not a licensed cancer vaccine or a clinical trial. Evidence of efficacy in cats and for specific tumor types such as adenocarcinoma is limited. It should not be presented as a proven replacement for indicated surgery, chemotherapy or radiation. Torigen states it can be used alongside chemotherapy or radiation when clinically appropriate."},
]

def contact_line(x, country):
    parts=[]
    if x.get("provider_url"): parts.append(f"🌐 [Official website]({x['provider_url']})")
    if x.get("contact_email"): parts.append(f"✉️ [{x['contact_email']}](mailto:{x['contact_email']})")
    if x.get("contact_email_europe") and country=="Europe": parts.append(f"✉️ [{x['contact_email_europe']}](mailto:{x['contact_email_europe']})")
    if x.get("contact_phone"): parts.append(f"☎️ [{x['contact_phone']}](tel:{x['contact_phone'].replace('-', '')})")
    return "    ".join(parts)

st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>🧬 Other Options</div>", unsafe_allow_html=True)
st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)
st.write("A short list of non-routine treatment options with current access and enough evidence or clinical relevance to be worth discussing with a veterinary oncologist.")
with st.expander("How options qualify"):
    st.write("This section can include regulated, experimental, off-label, precision, or personalized anticancer treatments with a real current access pathway. The evidence level and limitations are shown explicitly; inclusion does not mean the treatment is proven superior to standard care.")

species=st.selectbox("1. Species",["Dog","Cat"])
country=st.selectbox("2. Country / region",["USA","Canada","Europe"])
country_options=[x for x in OPTIONS if x["species"]==species and country in x.get("countries",[])]
available_cancers=sorted({c for x in country_options for c in x["cancers"]})
cancer=st.selectbox("3. Cancer type",["Select cancer type"]+available_cancers)
if cancer=="Select cancer type":
    if not country_options:
        st.info(f"No {species.lower()}-specific additional option currently passes the evidence and access screen for {country}. Clinical trials and standard oncology care may still be available.")
    else:
        st.caption("Choose a cancer type to continue.")
else:
    cancer_matches=[x for x in country_options if cancer in x["cancers"]]
    situations=sorted({s for x in cancer_matches for s in x["situations"]})
    situation=st.selectbox("4. Clinical situation",["Show all relevant situations"]+situations)
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
                contacts=contact_line(x,country)
                if contacts:
                    st.markdown("**Contact / next step**")
                    st.markdown(contacts)
                with st.expander("Evidence"):
                    st.markdown(f"**Evidence level:** {x['evidence_level']}")
                    st.write(x["evidence"])
                    st.link_button("Clinical evidence",x["url"],use_container_width=True)
                with st.expander("Access & sample"):
                    st.markdown(f"**Current access:** {x['access']}")
                    if x.get("contact_note"):
                        st.markdown(f"**Next step:** {x['contact_note']}")
                    if contacts:
                        st.markdown("**Contact:** "+contacts)
                    st.markdown(f"**Sample:** {x['sample']}")
                    st.markdown(f"**Travel:** {x['travel']}")
                    if x.get("access_url"):
                        st.link_button(x.get("access_label","How to access"),x["access_url"],use_container_width=True)
                with st.expander("Limitations"):
                    st.write(x["limitations"])

st.caption("Discussion prompts for a veterinary oncologist, not treatment recommendations or eligibility determinations. Evidence and access can change. Last review: September 5, 2026.")