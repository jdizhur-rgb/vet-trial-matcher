"""Feline-specific practical cancer guidance. Never substitute canine outcome data."""

FELINE_PRACTICAL = {
    'lymphoma': {
        'prognosis': 'Feline lymphoma is not one disease, so one survival number would be misleading. Low-grade intestinal lymphoma can often be controlled much longer than aggressive high-grade disease. In one selected series of cats with discrete high-grade gastrointestinal lymphoma treated with surgery followed by CHOP chemotherapy, median survival was 417 days. Site, grade, stage and response to treatment matter greatly.',
        'next': 'Confirm the anatomic form and whether the lymphoma is low-grade or high-grade before assuming a prognosis or treatment plan. Intestinal, nasal, mediastinal, renal and multicentric lymphoma can behave differently. Treatment decisions for high-grade disease generally should not wait for months.',
        'tests': 'Ask whether cytology or biopsy is sufficient to establish grade and whether flow cytometry, PARR or immunohistochemistry would change treatment. CBC/chemistry and site-appropriate staging are commonly useful. Before starting steroids or chemotherapy, check whether a trial requires untreated measurable disease or a diagnostic sample.'},
    'mast cell tumor': {
        'prognosis': 'Feline mast cell tumors behave very differently by location. A solitary cutaneous mast cell tumor is often cured by surgery, while splenic, intestinal, multiple or disseminated disease needs a different discussion. In a 64-cat splenic mast cell tumor study, median tumor-specific survival was 856 days in cats that underwent splenectomy versus 342 days in cats that did not; another splenectomy series reported overall median survival of 390 days.',
        'next': 'First establish whether this is a solitary skin tumor or whether the spleen, intestine, lymph nodes or multiple skin sites are involved. Do not apply canine mast-cell grading rules to a cat. For splenic disease, splenectomy can be an important treatment decision when the cat is an appropriate surgical candidate.',
        'tests': 'For a solitary skin tumor, pathology after removal may be enough. With multiple, recurrent or visceral disease, ask what staging will change management. CBC, abdominal imaging and sampling of suspicious spleen or lymph nodes may be useful depending on the presentation.'},
    'oral squamous cell carcinoma': {
        'prognosis': 'Feline oral squamous cell carcinoma is usually aggressive locally and is often difficult to control because it is advanced when found. Published outcomes vary by site and treatment: one study reported median survival from about 33–51 days for mandibular, sublingual and maxillary tumors and 151 days for oropharyngeal tumors; a prospective radiation-plus-carboplatin study reported median survival of 163 days. A few cats do substantially better, especially when a small tumor can be completely controlled locally.',
        'next': 'This is a diagnosis where weeks can matter. Determine the exact site, tumor size and bone involvement and whether complete surgery or radiation is realistic. Eating, pain and hydration deserve attention at the same time as cancer treatment planning.',
        'tests': 'Biopsy confirmation and imaging of local extent are important before major jaw surgery or radiation. CT is often useful for defining bone invasion and treatment planning. Ask whether regional lymph nodes need sampling and whether any additional assay would actually change treatment or trial eligibility.'},
    'mammary carcinoma': {
        'prognosis': 'Feline mammary carcinoma is usually biologically aggressive, but outcome varies substantially with tumor size, stage and pathology. Tumors larger than 3 cm, lymph-node metastasis, lymphovascular invasion, ulceration and higher histologic grade are repeatedly associated with shorter survival. Because published cohorts and stages differ, a single median survival number is less useful than these individual findings.',
        'next': 'Measure and stage the disease before assuming surgery alone is enough. Record how many glands are involved, evaluate regional lymph nodes and lungs, and discuss the appropriate extent of feline mammary surgery. Pathology after surgery should guide whether additional treatment is worth considering.',
        'tests': 'Pathology should report histologic grade, margins and lymphovascular invasion when assessable. Ask whether regional lymph nodes should be sampled and whether chest imaging is adequate for staging. Biomarker testing should have a clear treatment or trial purpose before you pay for it.'},
}

SOURCES = {
    'lymphoma': ['PMID:26333999'],
    'mast cell tumor': ['PMID:28168776', 'PMID:26083443', 'PMID:30244666'],
    'oral squamous cell carcinoma': ['PMID:31113565', 'PMID:21539605', 'PMID:41158948'],
    'mammary carcinoma': ['PMID:40150308', 'PMID:31113336', 'PMID:24741029'],
}
