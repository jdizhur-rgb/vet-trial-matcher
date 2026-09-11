"""Practical owner guidance for cancer pages.

Copy is intentionally conservative. Prognosis numbers are contextualized to the
published populations they came from; they are not predictions for an individual pet.
Primary evidence was checked against PubMed/peer-reviewed veterinary oncology reports.
"""

PRACTICAL = {
'lymphoma': {
 'prognosis':'For dogs with common high-grade nodal B-cell lymphoma treated with CHOP, recent large studies report median survival around 10–11 months; T-cell and other lymphoma forms can behave differently. Cats vary even more by anatomic form and grade. These are group statistics, not a clock for one pet.',
 'next':'Confirm the lymphoma type before assuming one prognosis. Immunophenotyping (B-cell versus T-cell), grade and anatomic form can change both treatment and trial eligibility. Because lymphoma is usually systemic, treatment decisions are generally made in days to a few weeks rather than after a long wait.',
 'tests':'Ask whether flow cytometry, PARR or immunohistochemistry would change the diagnosis or treatment. Baseline CBC/chemistry and staging are commonly useful. If a trial is possible, check whether starting prednisone or chemotherapy first would make the pet ineligible.'},
'mast cell tumor': {
 'prognosis':'Mast cell tumor prognosis ranges from excellent local control to aggressive metastatic disease. Grade alone is not enough: in one study of completely staged dogs with solitary stage-I Kiupel high-grade tumors, median survival was 1,046 days, while nodal metastasis and higher mitotic count were important adverse factors.',
 'next':'Get the pathology details: Kiupel grade, mitotic count and margins. Decide whether the regional lymph node needs sampling even if it feels normal. A small removable low-grade tumor and a high-grade or node-positive tumor are very different situations.',
 'tests':'For higher-risk tumors, ask whether regional lymph-node cytology and KIT/c-kit testing would change treatment or selection of a targeted drug. Keep the pathology block/slides available if additional testing or a trial may be considered.'},
'soft tissue sarcoma': {
 'prognosis':'Many low- and intermediate-grade canine soft tissue sarcomas can be controlled for years when local treatment is successful. High grade, large size, recurrence and metastasis worsen the outlook. Published studies are too heterogeneous for one honest survival number to represent every STS.',
 'next':'The first surgery matters because these tumors can extend microscopically beyond what can be seen. If the mass is still present and surgery is planned, ask whether biopsy or imaging would change the surgical plan. If it was already removed, grade and margin status become the key pieces of the pathology report.',
 'tests':'Ask for histologic grade and measured margins. Imaging is chosen according to grade, size and site. If tissue may be useful for a trial or molecular testing, ask the pathology lab to retain the block/slides.'},
'hemangiosarcoma': {
 'prognosis':'Visceral hemangiosarcoma is aggressive and can bleed suddenly. In a retrospective series, median survival was 66 days with surgery alone and 274 days with surgery followed by doxorubicin; individual dogs varied widely. Superficial skin hemangiosarcoma can behave very differently and should not be given the same prognosis.',
 'next':'For a splenic, cardiac or other visceral tumor, determine whether there is active bleeding and complete staging promptly. If surgery has already happened, pathology, stage and whether rupture occurred help frame the next decision. This is not a cancer where a months-long oncology wait is ideal.',
 'tests':'CBC/chemistry and chest/abdominal staging are commonly useful; echocardiography is relevant when a cardiac lesion is suspected. Ask whether any additional tumor assay would actually change treatment now before paying for it.'},
'osteosarcoma': {
 'prognosis':'For appendicular osteosarcoma without visible metastasis, amputation alone historically gives median survival around 3–4 months; amputation plus platinum-based chemotherapy commonly produces medians around 9–11 months. Some dogs live much longer. Axial sites, visible metastasis and other factors change these numbers.',
 'next':'Pain control is immediate. Staging the lungs and assessing the affected bone help determine whether amputation, limb-sparing treatment, radiation or another approach is realistic. A painful bone at risk of fracture should not be left untreated just to preserve trial eligibility.',
 'tests':'Ask whether chest CT versus radiographs would change the plan, and whether alkaline phosphatase or biopsy/pathology information affects prognosis. Before definitive local treatment, check trials because some require an intact measurable primary tumor.'},
'oral melanoma': {
 'prognosis':'Canine oral melanoma is strongly stage-dependent. Published radiation-treated groups reported median survival about 758 days for stage I, 278 days for stage II, 163 days for stage III and 80 days for stage IV. Other treatment series differ, so stage matters more than quoting one melanoma number.',
 'next':'Measure and stage the primary tumor and evaluate regional lymph nodes and lungs. Local control with surgery or radiation matters, but metastatic risk also has to be addressed. Check trials before removing a measurable tumor when doing so will not delay medically necessary care.',
 'tests':'Ask whether lymph-node sampling is indicated even when nodes are not obviously enlarged. Histopathology, mitotic activity and stage are useful. Molecular testing should have a clear treatment or trial purpose before it is ordered.'},
'melanoma': {
 'prognosis':'The word melanoma is not enough to predict behavior. Canine cutaneous melanomas are often much less aggressive than oral or digital melanomas; digital disease is intermediate in many series. Prognosis should be based on the primary site, pathology and stage rather than borrowing oral-melanoma statistics.',
 'next':'Confirm exactly where the melanoma originated and whether it is cutaneous, digital/nail-bed, oral or another mucosal form. That determines how urgently staging and systemic options need to be considered.',
 'tests':'Pathology should include features relevant to biologic behavior. For aggressive sites, regional lymph-node evaluation and chest staging may matter. Preserve tissue if a trial requires confirmation or additional testing.'},
'oral squamous cell carcinoma': {
 'prognosis':'Species changes this diagnosis dramatically. In dogs with resectable non-tonsillar oral SCC, surgery can produce long control and high one-year survival in published series. Feline oral SCC is usually much harder to control; radiation/chemotherapy series often report median survival measured in only a few months.',
 'next':'Determine exact site, size, bone involvement and whether complete surgery is feasible. In cats especially, eating, pain and local tumor control need attention quickly. Do not use canine prognosis numbers for a cat.',
 'tests':'Biopsy confirmation and imaging of local extent are important before major jaw surgery or radiation. Ask whether regional nodes should be sampled and whether the pathology subtype changes expected behavior.'},
'squamous cell carcinoma': {
 'prognosis':'SCC behaves very differently by site and species. A small cutaneous lesion, a canine gingival SCC and a feline oral SCC do not share one prognosis. The useful prediction comes from the exact primary site, depth/invasion, stage and ability to obtain local control.',
 'next':'First identify the primary site and local extent. If the tumor is still present, plan the first local treatment carefully; if it has been removed, review margins and pathology before deciding whether more local treatment is needed.',
 'tests':'Biopsy/pathology and site-appropriate imaging matter more than a generic cancer panel. Regional lymph-node assessment is useful for higher-risk sites. Ask whether additional testing will change treatment or trial eligibility.'},
'urothelial carcinoma': {
 'prognosis':'Canine urothelial carcinoma is usually managed rather than cured, but meaningful control is possible. Published drug studies report median survival roughly 6–18 months depending on tumor location, treatment sequence and study population; prostatic involvement and obstruction are adverse features.',
 'next':'Protect urine flow first. Determine whether the tumor involves the bladder trigone, urethra or prostate and whether there is obstruction or metastasis. Medical treatment is common because complete surgery is often not feasible.',
 'tests':'Urinalysis/culture, urinary-tract imaging and staging are useful. Ask whether a urine-based BRAF test helps confirm the diagnosis in this case, and whether tissue is still required before treatment or trial enrollment.'},
'hepatocellular carcinoma': {
 'prognosis':'A solitary resectable canine hepatocellular carcinoma can have a surprisingly favorable outlook. In a classic surgical series, median survival after liver lobectomy exceeded 1,460 days, compared with 270 days in the small nonsurgical group. Multifocal, diffuse or unresectable disease is a different problem.',
 'next':'The crucial question is whether this is a solitary surgically removable mass and how it relates to major vessels and central liver structures. Do not apply the prognosis of a resectable massive HCC to diffuse liver cancer.',
 'tests':'High-quality abdominal imaging and liver-function/chemistry assessment guide surgical planning. Cytology can miss HCC; ask whether biopsy or surgical pathology is needed for a definitive diagnosis.'},
'mammary carcinoma': {
 'prognosis':'Mammary carcinoma prognosis varies widely. In dogs, stage, lymphatic invasion, ulceration and complete margins are important; one series reported median survival of 1,098 days without lymphatic invasion versus 179 days when it was present. Feline mammary carcinoma is generally more aggressive, with size, grade, lymphovascular invasion and nodal spread strongly affecting outcome.',
 'next':'Stage before assuming surgery alone is enough. Record tumor number and size, evaluate regional nodes and lungs, and plan the appropriate extent of surgery for the species.',
 'tests':'Pathology should report histologic type/grade, margins and lymphovascular invasion. Ask whether lymph-node sampling is indicated. Hormone-receptor or other testing is useful only when it will change a decision.'},
'thyroid carcinoma': {
 'prognosis':'Many canine thyroid carcinomas are treatable for years. A large thyroidectomy series reported median survival of 802 days, and reviews report survival beyond three years in selected dogs with mobile surgically treated tumors. Fixed invasive, bilateral or metastatic tumors require a different plan.',
 'next':'Determine whether the mass is freely movable or invasive/fixed and whether major vessels are involved. That distinction often determines surgery versus radiation, radioactive iodine or systemic options.',
 'tests':'Thyroid hormone testing, cervical imaging and metastatic staging may matter. Ask whether iodine avidity testing would change the use of radioactive iodine.'},
'prostate cancer': {
 'prognosis':'Canine prostatic carcinoma is aggressive, but outcome depends heavily on extent and treatment. A multi-institutional medical-treatment series reported median survival of 82 days overall, while a selected group receiving definitive radiation had median survival of 563 days. Those populations are not interchangeable.',
 'next':'Urinary function and pain come first. Stage lymph nodes, lungs and bone as appropriate, and determine whether local treatment can safely control the prostate/urethra. Obstruction may require an interventional procedure.',
 'tests':'Urinary imaging, renal values and metastatic staging are important. If diagnosis is uncertain, ask what sample is safest and sufficient before treatment.'},
'primary lung tumor': {
 'prognosis':'A solitary resectable primary lung tumor can have meaningful survival after lobectomy. In a contemporary series, dogs without intrathoracic nodal metastasis had median survival of 456 days versus 167 days with positive nodes, although the difference was not statistically significant in that small cohort.',
 'next':'First confirm that this is likely a primary lung tumor rather than metastasis from another cancer. For a solitary lesion, surgical resectability and intrathoracic lymph-node status are central decisions.',
 'tests':'Chest CT can define the lesion and nodes better than radiographs for surgical planning. Ask whether lymph-node biopsy will be done at surgery and whether pathology indicates a need for systemic treatment.'},
'glioma': {
 'prognosis':'Modern radiation has improved reported outcomes for canine glioma. Recent stereotactic and definitive-radiation series report median survival around 12–23 months in selected dogs, while older series were shorter. MRI appearance, neurologic condition and whether the diagnosis is presumed or biopsy-confirmed matter.',
 'next':'Control seizures or brain swelling first when present, then discuss MRI-based diagnosis, radiation and whether biopsy/surgery is feasible or needed. Brain-tumor trials may require tissue or specific prior-treatment status, so check them before treatment when medically safe.',
 'tests':'MRI is central. Ask whether biopsy would change treatment enough to justify its risk, and whether the trial under consideration requires histologic confirmation.'},
'meningioma': {
 'prognosis':'Canine intracranial meningioma often has a longer treatment horizon than many aggressive cancers. A 2025 multicenter study of presumed meningioma reported median survival of 696 days after radiation versus 297 days after surgery, but treatment selection and tumor characteristics can bias retrospective comparisons.',
 'next':'Stabilize neurologic signs, then discuss radiation versus surgery based on location, accessibility and the individual dog. Do not assume surgery is automatically superior simply because the mass is operable.',
 'tests':'MRI is the main planning test. Histopathology gives grade when tissue is obtained; ask whether tissue confirmation would change treatment or trial access.'},
'nasal tumor': {
 'prognosis':'For canine nasal tumors treated with radiation, published median survival is commonly around 8–18 months, with wide variation by histology and CT extent. A 2026 series found 468 days without cribriform-plate destruction versus 191 days when it was present.',
 'next':'CT extent and biopsy diagnosis matter before choosing treatment. Radiation is commonly the main local therapy. Nosebleeds, airflow problems or neurologic signs can make timing more urgent.',
 'tests':'CT of the nasal cavity and biopsy are central. Ask specifically whether the cribriform plate is involved and whether regional lymph nodes need sampling.'},
'leukemia': {
 'prognosis':'Acute and chronic leukemia must not be lumped together. In a canine acute-leukemia series, treated dogs had median survival of only 55 days, while chronic leukemias can sometimes be controlled much longer. The first job is to establish which leukemia this is.',
 'next':'Acute leukemia can deteriorate quickly because normal blood-cell production is affected. CBC, blood smear, marrow evaluation and immunophenotyping may be needed promptly. Chronic disease may allow more time for characterization and treatment planning.',
 'tests':'Ask whether flow cytometry/immunophenotyping and bone-marrow sampling are needed to distinguish acute versus chronic and lymphoid versus myeloid disease. Blood counts also determine immediate supportive-care needs.'},
'multiple myeloma': {
 'prognosis':'Canine multiple myeloma is systemic but often treatment-responsive. A classic treated series reported median survival of about 540 days; response to therapy was strongly associated with outcome, while hypercalcemia and light-chain proteinuria were adverse features.',
 'next':'Assess the problems the abnormal plasma cells/proteins are causing now: anemia, kidney injury, high calcium, bone pain or hyperviscosity. Systemic drug treatment is usually the main approach.',
 'tests':'CBC/chemistry, calcium, serum/urine protein studies, imaging for bone lesions and bone-marrow evaluation may all contribute to diagnosis and monitoring.'},
'chemodectoma': {
 'prognosis':'Many canine heart-base tumors grow slowly enough for meaningful control. Toceranib series report median survival around 16–26 months in treated dogs; an SBRT series reported about 13 months. These are retrospective selected populations, not a guarantee for an individual dog.',
 'next':'Determine whether the mass is causing pericardial fluid, vessel/airway compression or arrhythmia and whether it is actually progressing. Treatment may include targeted therapy, radiation or management of complications rather than surgery.',
 'tests':'Echocardiography and cross-sectional imaging help define size and compression. Ask whether tissue confirmation is necessary or safe and whether serial imaging shows true growth before committing to treatment.'},
}

# Evidence anchors used when drafting the owner copy. Kept here for maintenance/audit.
SOURCES = {
 'lymphoma':['PMID:39422460','PMID:36503518'], 'mast cell tumor':['PMID:31916687','PMID:35733233'],
 'soft tissue sarcoma':['PMID:26808432','PMID:39241800'], 'hemangiosarcoma':['PMID:30197439'],
 'osteosarcoma':['PMID:8683484','PMID:21488959'], 'oral melanoma':['PMID:26517618','PMID:32323424'],
 'melanoma':['PMID:31262050'], 'oral squamous cell carcinoma':['PMID:23971850','PMID:40183472'],
 'urothelial carcinoma':['PMID:27376143','PMID:25619518'], 'hepatocellular carcinoma':['PMID:15521445','PMID:33898296'],
 'mammary carcinoma':['PMID:24735412','PMID:40150308'], 'thyroid carcinoma':['PMID:36852498','PMID:17591293'],
 'prostate cancer':['PMID:29806232','PMID:31811693'], 'primary lung tumor':['PMID:33195509'],
 'glioma':['PMID:37423611','PMID:40852884'], 'meningioma':['PMID:39968764','PMID:42379561'],
 'nasal tumor':['PMID:39175976','PMID:42276122'], 'leukemia':['PMID:27402031'],
 'multiple myeloma':['PMID:3721983'], 'chemodectoma':['PMID:31069932','PMID:32078943'],
 'squamous cell carcinoma':['PMID:23971850','PMID:40183472']}
