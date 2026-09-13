"""Species-specific owner-page content overrides for English cancer pages."""

# Canine overrides are retained for diagnoses where the shared source previously mixed
# species. Other canine diagnoses can safely use the canine-oriented base content.
CANINE_OWNER_CONTENT = {
    'lymphoma': (
        'Lymphoma is a cancer of lymphocytes and can involve lymph nodes, blood, spleen, liver, gastrointestinal tract, skin or other organs. In dogs, behavior and treatment differ substantially by anatomic form, grade and immunophenotype, especially B-cell versus T-cell disease.',
        'For most dogs with high-grade multicentric lymphoma, systemic multi-drug chemotherapy such as a CHOP-based protocol is a common first-line treatment. Other drugs or immune-based approaches may be used after relapse, while radiation or surgery has a role in selected localized forms.',
        ''),
    'mammary carcinoma': (
        'Canine mammary carcinoma is a malignant tumor of mammary tissue. Behavior varies widely with tumor size, histologic type and grade, lymphovascular invasion, lymph-node involvement and metastatic stage.',
        'Surgery is the main treatment for localized canine mammary carcinoma. Additional systemic treatment is considered selectively for higher-risk, node-positive or metastatic disease.',
        ''),
    'meningioma': (
        'Meningioma arises from the membranes surrounding the brain or spinal cord. In dogs, clinical impact depends on location, compression of nervous tissue, neurologic signs and whether the tumor can be safely treated locally.',
        'Radiation is a common definitive local treatment for canine intracranial meningioma, especially when surgery is not feasible or complete removal is unlikely. Surgery is appropriate for selected accessible tumors; medications control symptoms but do not replace tumor-directed treatment.',
        ''),
    'nasal tumor': (
        'Nasal tumors are locally invasive cancers of the nasal cavity and sinuses. In dogs they commonly cause persistent nasal discharge, bleeding, sneezing or facial changes, and local progression is often the main clinical problem before distant spread becomes dominant.',
        'Radiation therapy is the main definitive local treatment for most canine nasal cancers because complete surgical removal is rarely practical. Chemotherapy or targeted treatment may be added for selected histologies or more advanced disease.',
        ''),
    'oral squamous cell carcinoma': (
        'Canine oral squamous cell carcinoma is a locally invasive cancer of the mouth. Exact site, tumor size, bone invasion and stage strongly influence whether complete local control is feasible.',
        'Surgery offers the best chance of durable local control when complete excision is anatomically feasible. Radiation can be used for incompletely excised, unresectable or palliative cases; systemic treatment is considered selectively according to stage and histologic behavior.',
        ''),
    'squamous cell carcinoma': (
        'Squamous cell carcinoma can arise in the skin, mouth, nasal tissues and other sites. In dogs, biologic behavior varies substantially by primary site, so a cutaneous lesion and an oral or nasal tumor should not be treated as one disease.',
        'Local treatment may include surgery, radiation or another site-specific approach. Systemic treatment is considered for selected advanced or metastatic cases.',
        ''),
}

FELINE_OWNER_CONTENT = {
    'lymphoma': (
        'Feline lymphoma is a cancer of lymphocytes and is not one single disease. Intestinal, nasal, mediastinal, renal, multicentric and other forms can behave differently, and grade is often as important as anatomic site.',
        'Treatment depends on form and grade. Some low-grade gastrointestinal lymphomas can be controlled with oral chemotherapy and corticosteroids, while high-grade disease usually needs multi-agent systemic chemotherapy. Radiation can be very useful for selected localized forms such as nasal lymphoma.',
        ''),
    'mast cell tumor': (
        'Feline mast cell tumors differ biologically from canine mast cell tumors. Cats commonly develop cutaneous tumors, while splenic and intestinal mast cell disease also occur, and prognosis depends heavily on the anatomic form rather than canine grading rules.',
        'Surgery is usually the main treatment for a solitary removable skin tumor. Splenectomy can provide meaningful control for splenic mast cell disease in appropriate cats. Intestinal, disseminated, recurrent or unresectable disease may require systemic treatment, but feline evidence is more limited.',
        ''),
    'soft tissue sarcoma': (
        'Feline soft tissue sarcoma includes ordinary soft tissue sarcomas and injection-site sarcomas. Injection-site sarcoma is particularly important because microscopic local extension can be substantial and a poorly planned first surgery can make later control harder.',
        'Wide planned surgery is the main treatment when complete removal is feasible. Radiation is often considered when margins are incomplete or when local anatomy makes another surgery difficult. Systemic treatment is used selectively for higher-risk or metastatic disease.',
        ''),
    'hemangiosarcoma': (
        'Feline hemangiosarcoma is a malignant tumor of vascular endothelial cells. It can arise in the skin, subcutaneous tissue, spleen or other internal organs. Superficial cutaneous disease can behave differently from visceral disease, which may bleed and can be aggressive.',
        'Complete surgery is the main local treatment for resectable disease when the cat is stable enough for surgery. Evidence for additional drug treatment in cats is limited, so systemic treatment should be individualized rather than copied directly from canine protocols.',
        ''),
    'osteosarcoma': (
        'Feline osteosarcoma is a primary bone cancer. It often has a longer course than canine osteosarcoma, especially in the limbs, but metastasis is not rare and appendicular and axial tumors should not be given the same expectations.',
        'For a resectable limb tumor, amputation is the main local treatment and provides pain relief as well as tumor control. Recent feline data support discussing additional drug treatment in selected nonmetastatic cats rather than automatically assuming surgery is always enough. Radiation and pain control are options when surgery is not feasible.',
        ''),
    'oral melanoma': (
        'Feline oral melanoma is rare. It can be locally invasive and metastatic, but the feline evidence base is much smaller than the canine literature. Poorly pigmented tumors may need immunohistochemistry for confident diagnosis.',
        'When anatomically feasible, surgery is used for local control. Radiation can be considered when complete excision is not possible or for palliation. There is no well-established feline systemic standard, so systemic or immune-based approaches should be described as individualized or investigational rather than borrowed from canine melanoma data.',
        ''),
    'melanoma': (
        'Melanoma is uncommon in cats and its behavior depends strongly on where it starts. Ocular, oral, cutaneous and other melanocytic tumors should not be treated as one disease, and poorly pigmented tumors can require additional pathology work to confirm the diagnosis.',
        'Surgery is the main local treatment for many resectable melanomas. Ocular disease often requires ophthalmic decision-making, while oral or metastatic disease may need radiation or individualized systemic treatment. Canine melanoma vaccine or drug outcomes should not be presented as feline evidence.',
        ''),
    'oral squamous cell carcinoma': (
        'Feline oral squamous cell carcinoma is usually an aggressive local cancer of the mouth. Many tumors are advanced when diagnosed, and pain, eating difficulty, tongue or jaw involvement and bone invasion can become the immediate clinical problems.',
        'Surgery offers the best chance of durable local control only when complete removal is anatomically realistic. Radiation, palliative local treatment and investigational approaches may be considered when surgery cannot achieve useful margins. Support for nutrition and pain control is often part of treatment from the start.',
        ''),
    'squamous cell carcinoma': (
        'Feline squamous cell carcinoma behaves very differently by site. Small sun-associated lesions of the pinnae, eyelids or nasal planum can be primarily local-control problems, while oral SCC is a much more aggressive disease and should be considered separately.',
        'Surgery, radiation, cryotherapy and electrochemotherapy can all have roles in selected cutaneous cases depending on site and stage. Oral disease follows a different treatment pathway, and systemic treatment has a limited evidence base in cats.',
        ''),
    'urothelial carcinoma': (
        'Feline urothelial carcinoma is an uncommon malignant tumor of the urinary tract, most often involving the bladder or urethra. Local progression can interfere with urine flow and metastatic spread can occur, but published feline treatment data are much smaller than the canine literature.',
        'There is no single established feline standard. Surgery may be useful for selected favorably located tumors, while medical therapy, radiation or procedures to maintain urine flow can be considered according to anatomy, obstruction and stage. Drug choices should be based on feline safety and evidence.',
        ''),
    'hepatocellular carcinoma': (
        'Feline hepatocellular carcinoma is a primary cancer of liver cells. A solitary resectable liver mass can have a very different outlook from multifocal, diffuse or invasive disease, so imaging and surgical anatomy matter greatly.',
        'Liver lobectomy is the main treatment for a resectable solitary hepatocellular carcinoma and can provide prolonged control in selected cats. Multifocal, diffuse, unresectable or metastatic disease requires an individualized plan.',
        ''),
    'mammary carcinoma': (
        'Feline mammary carcinoma is usually biologically aggressive. Tumor size, histologic grade, lymphovascular invasion, regional lymph-node involvement and metastatic stage are especially important when estimating risk.',
        'Surgery is the main treatment for localized disease and feline surgical planning is usually more extensive than simply removing one visible nodule. Chemotherapy may be discussed for higher-risk, node-positive or metastatic disease, although expected benefit varies.',
        ''),
    'thyroid carcinoma': (
        'Feline thyroid carcinoma is rare, and most feline thyroid disease is benign hyperplasia or adenoma rather than cancer. A suspected carcinoma should therefore be distinguished from ordinary hyperthyroidism and assessed for local invasion and metastasis.',
        'Surgery can be appropriate for a localized removable tumor. Radioactive iodine may be useful for selected iodine-avid tumors, while radiation or other treatment can be considered for invasive, recurrent or metastatic disease.',
        ''),
    'prostate cancer': (
        'Feline prostate cancer is exceptionally rare. Reported tumors can interfere with urination or defecation and may spread to regional lymph nodes, lungs or bone. The literature is too sparse to import canine expectations automatically.',
        'There is no established feline standard treatment. Management is individualized and may include local treatment, systemic treatment, procedures to maintain urine flow and supportive care. Relief of obstruction or other mechanical complications can be the immediate priority.',
        ''),
    'primary lung tumor': (
        'Primary lung tumors arise from lung tissue rather than representing cancer that has spread to the lungs from another site. In cats, a solitary resectable mass can have a very different outlook from nodal, pleural or multifocal disease.',
        'Lung lobectomy is the main local treatment for a solitary resectable primary tumor when staging does not show prohibitive spread. Additional systemic treatment is considered selectively according to pathology, lymph-node involvement and metastatic stage.',
        ''),
    'glioma': (
        'Feline glioma is a rare primary brain tumor arising from glial cells. It can cause seizures, behavior changes, weakness or other neurologic signs. MRI can suggest the diagnosis, but feline outcome data are sparse and should not be replaced with canine survival estimates.',
        'Radiation is a common local treatment when feasible. Surgery or biopsy may be possible for selected lesions, and medications are used to control seizures or brain swelling. Treatment decisions are highly dependent on location and neurologic status.',
        ''),
    'meningioma': (
        'Feline intracranial meningioma is one of the more surgically treatable primary brain tumors in cats. Many tumors are relatively well circumscribed, but location and the cat’s neurologic condition still determine whether surgery is realistic.',
        'Surgical removal is often a strong option for accessible feline meningiomas and can provide long control in selected cats. Radiation is useful when surgery is not feasible, incomplete or declined, or when disease recurs.',
        ''),
    'nasal tumor': (
        'Feline nasal tumors are locally invasive cancers of the nasal cavity or sinuses. Histology matters because lymphoma, carcinoma and other tumor types can look similar clinically but require very different treatment.',
        'Radiation is an important local treatment for many feline nasal carcinomas and other non-lymphoid tumors. Nasal lymphoma is treated as lymphoma and may use radiation, systemic chemotherapy or both depending on extent.',
        ''),
    'leukemia': (
        'Feline leukemia is a cancer of blood-forming cells and is not the same diagnosis as feline leukemia virus infection, although FeLV can be associated with some leukemias and lymphomas. Acute and chronic forms have very different behavior and urgency.',
        'Acute leukemias generally need systemic chemotherapy and substantial supportive care, while some chronic leukemias can be managed less intensively for longer periods. Treatment depends on cell lineage, blood counts and the cat’s clinical stability.',
        ''),
    'multiple myeloma': (
        'Multiple myeloma is a plasma-cell cancer that can affect bone marrow, bones, kidneys and blood proteins. In cats it is uncommon, and diagnosis relies on several findings together rather than on any single abnormal protein value.',
        'Systemic therapy is the main treatment because myeloma is generally disseminated. Alkylating chemotherapy with a corticosteroid is commonly considered, while radiation can help control painful focal bone lesions or other sites needing local treatment.',
        ''),
    'chemodectoma': (
        'Chemodectoma is a heart-base tumor and is very rare in cats. It can cause problems through compression, pericardial or pleural fluid, arrhythmia or metastatic spread, but feline outcome data are extremely limited.',
        'Treatment is individualized. Radiation, surgery in selected anatomy, medical management and procedures to control fluid may be considered, but there is no dependable feline standard that should be inferred from canine series.',
        ''),
    'histiocytic sarcoma': (
        'Feline histiocytic sarcoma is a rare malignant cancer of histiocytic cells. It may appear as a localized lesion or involve several organs, and confirming the diagnosis with histopathology and appropriate immunohistochemistry is especially important.',
        'For localized resectable disease, surgery may provide local control and radiation can be considered when complete surgery is not feasible. There is no well-established feline systemic standard for disseminated histiocytic sarcoma, so treatment is individualized.',
        ''),
}
