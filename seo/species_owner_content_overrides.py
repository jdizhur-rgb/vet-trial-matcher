"""Species-specific owner-page content overrides for production SEO pages."""

CANINE_OWNER_CONTENT = {
    "lymphoma": (
        "Lymphoma is a cancer of lymphocytes, a type of immune cell. It can involve lymph nodes, blood, spleen, liver, gastrointestinal tract, skin or other organs. In dogs, behavior and treatment differ substantially by anatomic form, grade and immunophenotype, especially B-cell versus T-cell disease.",
        "For most dogs with high-grade multicentric lymphoma, systemic multi-drug chemotherapy such as a CHOP-based protocol is a common first-line treatment. Other chemotherapy drugs and newer targeted or immune-based approaches may be used in selected cases or after relapse. Radiation or surgery has a role in selected localized forms.",
        "Important treatment factors include B-cell versus T-cell type, grade, anatomic form, stage, previous chemotherapy, response or relapse history, organ involvement and the dog’s general health.",
    ),
    "mammary carcinoma": (
        "Canine mammary carcinoma is a malignant tumor of mammary tissue. Behavior varies widely with tumor size, histologic type and grade, lymphovascular invasion, lymph-node involvement, surgical margins and metastatic stage.",
        "Surgery is the main treatment for localized canine mammary carcinoma. The extent of surgery depends on the number and distribution of masses and the draining lymph nodes. Additional systemic treatment is considered selectively for higher-risk, node-positive or metastatic disease.",
        "Tumor size and number, histologic type and grade, surgical margins, lymphovascular invasion, lymph-node involvement, distant metastasis and relevant biomarker information when it will change management can affect treatment choices.",
    ),
    "meningioma": (
        "Meningioma is a tumor arising from the membranes surrounding the brain or spinal cord. In dogs, clinical impact depends on location, compression of nervous tissue, neurologic signs and whether the tumor can be safely treated locally.",
        "Radiation is a common definitive local treatment for canine intracranial meningioma, particularly when surgery is not feasible or complete removal is unlikely. Surgery may be appropriate for selected accessible tumors. Medications can control seizures, inflammation or other neurologic symptoms but do not replace tumor-directed treatment.",
        "Tumor location and size, neurologic status, MRI characteristics, surgical accessibility, previous treatment and anesthesia risk are central to treatment planning.",
    ),
    "nasal tumor": (
        "Nasal tumors are locally invasive cancers of the nasal cavity and sinuses. In dogs they commonly cause persistent nasal discharge, bleeding, sneezing or facial changes. For many canine nasal cancers, local progression is the main clinical problem before distant metastasis becomes dominant.",
        "Radiation therapy is the main definitive local treatment for most canine nasal cancers because complete surgical removal is rarely practical. Conventionally fractionated and stereotactic radiation are both used. Chemotherapy or targeted treatment may be added for selected histologies or more advanced disease.",
        "Histologic type, local extent, bone or cribriform-plate involvement, lymph-node or distant metastasis, prior treatment and overall health guide treatment planning.",
    ),
    "oral squamous cell carcinoma": (
        "Canine oral squamous cell carcinoma is a locally invasive cancer arising from the lining of the mouth. It can involve the gingiva, jaw, tongue or other oral tissues. Exact site, tumor size, bone invasion and metastatic stage strongly influence whether complete local control is feasible.",
        "Surgery offers the best chance of durable local control when complete excision is anatomically feasible, especially for resectable non-tonsillar oral SCC. Radiation can be used for incompletely excised, unresectable or palliative cases. Systemic treatment is considered selectively according to stage and histologic behavior.",
        "Exact oral site, tumor size, bone invasion, regional lymph-node status, distant metastasis, surgical feasibility, margins and previous treatment are the main factors guiding therapy.",
    ),
    "squamous cell carcinoma": (
        "Squamous cell carcinoma is a cancer of squamous epithelial cells and can arise in the skin, mouth, nasal tissues and other sites. In dogs, biologic behavior varies substantially by primary site, so a cutaneous lesion and an oral or nasal tumor should not be treated as one disease.",
        "Local treatment may include surgery, radiation or another site-specific approach. Systemic treatment is considered for selected advanced or metastatic cases. Recommendations should be based on the exact primary site, depth, local invasion and stage rather than on the label ‘SCC’ alone.",
        "Primary site, tumor size and depth, pathology, surgical margins, local invasion, lymph-node or distant spread and previous treatment are the main factors guiding therapy.",
    ),
}

FELINE_OWNER_CONTENT = {
    "hemangiosarcoma": (
        "Feline hemangiosarcoma is a malignant tumor of vascular endothelial cells. It can arise in the skin, subcutaneous tissue, spleen or other internal organs. Behavior differs markedly by site: superficial cutaneous disease can be more controllable, while visceral disease is often aggressive and may bleed.",
        "Treatment depends strongly on site. Complete surgery is the main local treatment for resectable disease when the cat is stable enough for surgery. Evidence for additional drug treatment in cats is limited, so systemic treatment should be individualized rather than copied directly from canine protocols.",
        "Primary site, bleeding, resectability, surgical margins, metastatic stage, anemia and the cat’s overall condition are central to treatment planning.",
    ),
    "hepatocellular carcinoma": (
        "Feline hepatocellular carcinoma is a primary cancer of liver cells. In cats, a solitary resectable liver mass can have a very different outlook from multifocal, diffuse or invasive disease. Imaging is important for defining how much of the liver is involved and whether surgery appears feasible.",
        "Liver lobectomy is the main treatment for a resectable solitary hepatocellular carcinoma and can provide prolonged control in selected cats. Multifocal, diffuse, unresectable or metastatic disease requires an individualized plan.",
        "Number and location of liver lesions, involvement of major vessels, surgical resectability, liver function, pathology and metastatic stage are central to treatment planning.",
    ),
    "histiocytic sarcoma": (
        "Feline histiocytic sarcoma is a rare malignant cancer of histiocytic cells. It may appear as a localized lesion or involve multiple organs, and published feline experience is limited. Confirming the diagnosis with histopathology and appropriate immunohistochemistry is especially important.",
        "For localized resectable disease, surgery may provide local control and radiation can be considered when complete surgery is not feasible. There is no well-established feline systemic standard for disseminated histiocytic sarcoma, so treatment is individualized.",
        "Localized versus disseminated disease, primary site, surgical margins, measurable disease, metastatic stage, previous treatment and the cat’s overall health drive treatment decisions.",
    ),
    "lymphoma": (
        "Feline lymphoma is a cancer of lymphocytes and is not one single disease. Intestinal, nasal, mediastinal, renal, multicentric and other forms can behave differently, and grade is often as important as anatomic site when discussing prognosis and treatment.",
        "Treatment depends on form and grade. Some low-grade gastrointestinal lymphomas can be controlled for long periods with oral chemotherapy and corticosteroids, while high-grade disease usually needs multi-agent systemic chemotherapy. Radiation can be very useful for selected localized forms such as nasal lymphoma, and surgery has a role in selected focal gastrointestinal disease.",
        "Anatomic form, low- versus high-grade disease, stage, previous treatment, response or relapse history, organ involvement and the cat’s general health are important treatment factors.",
    ),
    "mast cell tumor": (
        "Feline mast cell tumors arise from mast cells but differ biologically from canine mast cell tumors. Cats commonly develop cutaneous tumors, while splenic and intestinal mast cell disease also occur. Prognosis and treatment depend heavily on the anatomic form rather than on canine grading systems.",
        "Surgery is usually the main treatment for a solitary removable cutaneous mast cell tumor. Splenectomy can provide meaningful control for splenic mast cell disease in appropriate cats. Intestinal, disseminated, recurrent or unresectable disease may require systemic therapy, but evidence is more limited and treatment is individualized.",
        "Cutaneous versus splenic versus intestinal disease, number of lesions, resectability, metastatic stage, blood or marrow involvement when relevant, previous treatment and the cat’s overall health guide management.",
    ),
    "multiple myeloma": (
        "Multiple myeloma is a plasma-cell cancer that can affect bone marrow, bones, kidneys and blood proteins. In cats it is uncommon, and diagnosis relies on a combination of monoclonal protein, marrow or tumor findings and associated organ effects rather than on any single test.",
        "Systemic therapy is standard because myeloma is generally disseminated. Alkylating chemotherapy with a corticosteroid is commonly considered, with other drugs used according to response and tolerance. Radiation can help control painful focal bone lesions or other sites needing local treatment.",
        "Bone-marrow involvement, monoclonal protein burden, kidney function, calcium level, anemia or other cytopenias, bone lesions, hyperviscosity and previous treatment influence management.",
    ),
    "nasal tumor": (
        "Feline nasal tumors are locally invasive cancers of the nasal cavity or sinuses. They can cause chronic nasal discharge, bleeding, facial change or breathing difficulty. Histology matters because lymphoma, carcinoma and other tumor types can require very different treatment.",
        "Radiation is an important local treatment for many feline nasal carcinomas and other non-lymphoid nasal tumors. Nasal lymphoma is generally approached as a lymphoma and may be treated with radiation, systemic chemotherapy or both depending on extent. Surgery has a limited role for most diffuse intranasal cancers.",
        "Histologic type, local extent, bone or cribriform-plate involvement, lymph-node or distant metastasis, respiratory function, prior treatment and overall health guide treatment planning.",
    ),
    "oral melanoma": (
        "Feline oral melanoma is rare. It arises from melanocytes in the mouth and can be locally invasive and metastatic, but the feline evidence base is much smaller than the canine literature. Poorly pigmented tumors may require immunohistochemistry for confident diagnosis.",
        "When anatomically feasible, surgery is used for local control. Radiation can be considered when complete excision is not possible or for palliation. There is no well-established feline systemic standard, so systemic or immune-based approaches should be discussed as individualized or investigational options rather than assumed from canine melanoma data.",
        "Exact oral site, tumor size, bone invasion, regional lymph-node status, distant metastasis, diagnostic certainty, surgical feasibility and previous treatment guide management.",
    ),
    "osteosarcoma": (
        "Feline osteosarcoma is a primary bone cancer that often behaves less aggressively than the canine form, but metastasis is not rare. Appendicular and axial tumors should be considered separately because site, resectability and metastatic risk strongly affect treatment choices.",
        "For a resectable appendicular osteosarcoma, amputation is the main local treatment and provides pain relief as well as tumor control. Recent feline data support discussing additional drug treatment in some nonmetastatic cats rather than automatically omitting it. Radiation and pain control are options when surgery is not feasible.",
        "Tumor location, resectability, visible lung or other metastasis, pathologic fracture, pain and mobility, histologic diagnosis, previous therapy and the cat’s ability to tolerate treatment are key factors.",
    ),
    "prostate cancer": (
        "Feline prostate cancer is exceptionally rare. Reported tumors can interfere with urination or defecation and may spread to regional lymph nodes, lungs or bone. Because the literature consists mostly of small series and case reports, canine expectations should not be imported automatically.",
        "There is no established standard treatment for feline prostate cancer. Management is individualized and may include local treatment, systemic treatment, procedures to maintain urine flow and supportive care. The immediate priority is relief of obstruction or other mechanical complications when present.",
        "Urinary function, exact local anatomy, histologic type, metastatic stage, pain, previous treatment and whether local therapy can be delivered safely determine the realistic options.",
    ),
    "urothelial carcinoma": (
        "Feline urothelial carcinoma is an uncommon malignant tumor of the urinary tract, most often involving the bladder or urethra. Local progression can interfere with urine flow, and metastatic spread can occur. Published feline treatment data are far more limited than the canine literature.",
        "There is no single established feline standard. Surgery may be useful for selected favorably located tumors, while medical therapy, radiation or interventional procedures can be considered according to anatomy, urinary obstruction and stage. Drug choices should be based on feline safety and evidence rather than copied directly from canine protocols.",
        "Exact bladder or urethral location, ability to urinate, local invasion, metastatic stage, kidney function, previous drugs, measurable disease and the cat’s overall condition guide treatment.",
    ),
}
