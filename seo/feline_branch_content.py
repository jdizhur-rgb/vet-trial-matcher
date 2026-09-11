"""Diagnosis-specific decision branches for feline cancer owner guides.

Only branches that materially change the next action are kept. Generic staging and
trial boilerplate belongs in the surrounding page, not repeated inside accordions.
"""

FELINE_BRANCHES = {
    'lymphoma': [
        ('Low-grade intestinal lymphoma', 'Confirm that the diagnosis really fits low-grade intestinal lymphoma and discuss whether oral therapy is appropriate. Track weight, appetite, vomiting or diarrhea, and laboratory changes rather than judging response only by whether a mass is visible.'),
        ('High-grade or systemic lymphoma', 'This usually needs a more urgent systemic-treatment discussion than low-grade intestinal disease. Sampling, subtype, and the cat’s clinical condition determine how quickly treatment should start.'),
        ('Steroids or chemotherapy have already started', 'Keep exact drug names, doses, and dates. Do not stop steroids abruptly without instructions. Prior treatment and the quality and duration of response matter if lymphoma progresses or a trial is considered.'),
    ],
    'mast cell tumor': [
        ('There are multiple or recurrent skin tumors', 'Multiple skin lesions are not automatically the same as visceral dissemination, but they justify a closer review of pathology and whether additional staging or a different local strategy is warranted.'),
        ('The spleen is involved', 'Splenic mast cell tumor behaves differently from a routine skin tumor. Ask whether splenectomy is feasible and whether there is disease elsewhere before applying expectations from cutaneous MCT.'),
        ('There is intestinal or disseminated disease', 'This is a different risk category from a solitary skin tumor. Stabilize gastrointestinal or systemic problems and discuss systemic treatment and realistic goals separately from local skin-tumor management.'),
    ],
    'soft tissue sarcoma': [
        ('This may be an injection-site sarcoma', 'Do not treat it like an ordinary superficial lump. Biopsy and imaging may change the first definitive surgery, and referral before excision can matter because local recurrence after marginal surgery is difficult to control.'),
        ('It was removed with incomplete margins', 'Do not automatically wait for visible recurrence. Ask whether wider re-excision and/or radiation is feasible while the disease burden is still microscopic.'),
        ('It is recurrent, unresectable, or metastatic', 'Re-image the local site and stage the chest before repeating surgery. Radiation, systemic treatment, or an investigational local approach may be more useful than another marginal excision.'),
    ],
    'osteosarcoma': [
        ('The tumor is axial or cannot be completely removed', 'Local control can be much harder than for a removable limb tumor. Ask about radiation, surgical feasibility, pain control, and whether systemic treatment has a realistic role for this site and stage.'),
        ('Metastases are present', 'Visible metastasis changes the more favorable assumptions sometimes quoted for feline osteosarcoma. Treatment should be individualized around sites of spread, pain, respiratory status, and expected benefit.'),
        ('Amputation or local surgery is already done', 'Review pathology and staging rather than assuming surgery automatically ends the discussion. Newer feline data support considering adjuvant treatment in selected nonmetastatic cats, especially when other risk factors are present.'),
    ],
    'oral squamous cell carcinoma': [
        ('Complete surgery is not feasible', 'Discuss radiation, investigational treatment, and symptom control together. The plan should explicitly address pain, eating, hydration, and tumor bleeding because local progression is often the immediate problem.'),
        ('Eating or drinking is becoming difficult', 'Do not wait for the next routine oncology slot if the cat cannot maintain nutrition, hydration, or comfort. Supportive care may need to start before the definitive cancer plan is finalized.'),
        ('Surgery has already been done', 'Review measured margins, bone involvement, and postoperative function. Incomplete removal may justify another local-control discussion rather than waiting for obvious regrowth.'),
    ],
    'squamous cell carcinoma': [
        ('The SCC is on sun-exposed skin', 'A small superficial lesion on the pinna, nasal planum, or eyelid can be primarily a local-control problem. Earlier treatment can be easier than treating a large invasive lesion.'),
        ('The SCC is oral', 'Use the oral-SCC pathway instead. Feline oral SCC is much more aggressive locally than many cutaneous SCCs and should not inherit the prognosis of a small sun-induced skin lesion.'),
        ('The lesion is extensive or recurrent', 'Define whether the main problem is local invasion or true distant spread. Local treatment may still improve comfort and function even when cure is unrealistic.'),
    ],
    'urothelial carcinoma': [
        ('Urination is becoming difficult', 'Repeated straining, a weak stream, or inability to pass urine can become urgent. Ask early how urine flow will be maintained if obstruction worsens.'),
        ('Medical treatment has started', 'Track symptoms and imaging measurements together. Stable disease may still be clinically useful; record exact drugs because feline safety and prior treatment matter.'),
        ('The disease is metastatic or obstructive', 'Systemic treatment, urine-flow management, and comfort need to be planned together. Interventional procedures may help selected cats even when the tumor itself cannot be removed.'),
    ],
    'hepatocellular carcinoma': [
        ('Liver lobectomy has already been done', 'Review histopathology, margins, and staging. Follow-up should be based on the actual tumor type and completeness of removal rather than assuming every liver carcinoma needs chemotherapy.'),
        ('There are multiple or diffuse liver lesions', 'The favorable assumptions from a solitary resectable mass do not apply. Confirm diagnosis and liver function before considering biopsy, systemic treatment, or supportive care.'),
        ('The mass is not resectable', 'Ask why: location, vascular invasion, multifocal disease, metastasis, or the cat’s overall condition. Those reasons lead to different realistic alternatives.'),
    ],
    'mammary carcinoma': [
        ('Surgery has already been done', 'Review tumor size, grade, measured margins, lymphovascular invasion, and lymph-node status. Those findings determine recurrence risk and whether additional treatment is worth discussing.'),
        ('A regional lymph node is positive', 'Nodal metastasis is an important adverse finding. Complete staging and discuss systemic treatment; make sure the sampled node actually drains the affected mammary region.'),
        ('There is metastatic, ulcerated, or recurrent disease', 'Systemic treatment and comfort become central. Local surgery or radiation may still help selected painful, infected, ulcerated, or bleeding lesions when the expected benefit justifies recovery.'),
    ],
    'thyroid carcinoma': [
        ('The mass is fixed or invasive', 'Cross-sectional imaging can help define invasion and whether surgery is realistic. Radiation, radioactive iodine in selected iodine-avid tumors, or other treatment may be more appropriate than a high-risk operation.'),
        ('Surgery has already been done', 'Review histopathology, margins, and evidence of vascular invasion or spread. A removed thyroid carcinoma does not automatically need additional treatment.'),
        ('There is metastatic or recurrent disease', 'Confirm sites of spread and whether the tumor is iodine-avid or otherwise targetable before choosing treatment. Do not borrow expectations from ordinary benign feline hyperthyroidism.'),
    ],
    'primary lung tumor': [
        ('Lung lobectomy has already been done', 'Review histologic type, grade, margins, and lymph-node findings. These details are more useful than the phrase “lung cancer” alone for deciding whether monitoring or additional treatment is reasonable.'),
        ('There are multiple lung nodules', 'First determine whether this is truly a primary lung cancer rather than metastases from another tumor or a non-neoplastic process. Surgery outcomes for a solitary primary mass do not apply to diffuse pulmonary disease.'),
        ('The tumor is unresectable or metastatic', 'Discuss systemic or palliative options and respiratory comfort. The diagnosis and primary site should be secure before using canine or human lung-cancer expectations.'),
    ],
    'melanoma': [
        ('The melanoma is on the eye', 'Ocular melanoma has its own staging and treatment considerations. Ophthalmic assessment matters because timing of local treatment can depend on progression, glaucoma, pain, and metastatic risk.'),
        ('The melanoma is oral', 'Feline oral melanoma is rare and published data are sparse. Confirm the diagnosis carefully and stage the regional nodes and lungs rather than borrowing canine oral-melanoma outcomes.'),
        ('There is recurrence or metastatic disease', 'Re-stage and discuss realistic local and systemic options. Canine vaccine or drug outcomes should not be presented as feline evidence.'),
    ],
    'oral melanoma': [
        ('The diagnosis is uncertain', 'Feline oral melanoma is rare, so pathology review and immunohistochemistry can be worthwhile when morphology is not classic before committing to an aggressive treatment plan.'),
        ('The tumor was already removed', 'Review measured margins and complete staging if it was not done. A clean-looking mouth does not answer the question of regional or distant spread.'),
        ('There is nodal or distant spread', 'Separate control of the oral tumor from the systemic problem. Local treatment may still help pain, bleeding, or eating even when metastatic disease is present.'),
    ],
    'meningioma': [
        ('Seizures or neurologic signs are active', 'Control seizures and brain swelling while definitive planning is underway. Worsening consciousness, repeated seizures, or inability to walk or eat can justify urgent neurologic assessment.'),
        ('Surgery has already been done', 'Ask whether gross removal was achieved and what follow-up imaging is recommended. Histopathology confirms the diagnosis and can identify less typical behavior.'),
        ('Surgery is not feasible or disease recurs', 'Radiation may be an option depending on location and prior treatment. Medical therapy can control symptoms but should not be mistaken for tumor-directed treatment.'),
    ],
    'nasal tumor': [
        ('There is a nasal mass but no tissue diagnosis yet', 'Imaging can define local invasion, but biopsy is usually needed because carcinoma, lymphoma, and other nasal diseases require different treatment.'),
        ('Breathing or nosebleeds are worsening', 'Heavy bleeding, marked breathing difficulty, or inability to eat warrants earlier assessment. Symptom control can start while definitive treatment is arranged.'),
        ('Radiation is complete or the tumor has recurred', 'Track the duration of response and repeat imaging only when it will change the next decision. Re-irradiation or systemic treatment may be possible in selected cats depending on histology and prior dose.'),
    ],
    'leukemia': [
        ('Acute leukemia is suspected or confirmed', 'Acute leukemia can progress quickly. Cytopenias, infection, bleeding, and weakness may need immediate supportive care while chemotherapy options and prognosis are discussed.'),
        ('Chronic leukemia is suspected or confirmed', 'Some chronic leukemias behave more slowly, so treatment urgency depends on subtype, blood counts, progression, and clinical signs. Do not apply acute-leukemia survival expectations to a stable chronic case.'),
        ('Treatment has already started', 'Keep serial CBC results, drug doses, and transfusion or supportive-care history. Response in blood and marrow, treatment tolerance, and infections guide the next step.'),
    ],
    'multiple myeloma': [
        ('There is kidney injury, high calcium, or severe anemia', 'These complications can be more immediately important than tumor burden itself. Stabilization and supportive treatment should happen alongside the cancer plan.'),
        ('There is painful bone disease', 'Treat pain and assess fracture or spinal risk. Local radiation can sometimes help a focal painful lesion while systemic therapy addresses the plasma-cell disease.'),
        ('Systemic treatment has started', 'Track the monoclonal protein or other disease markers together with blood counts, kidney values, and clinical response. Feline evidence is limited, so the individual cat’s response matters heavily.'),
    ],
    'glioma': [
        ('Seizures or brain-swelling signs are active', 'Control seizures and intracranial inflammation first. Repeated seizures, worsening consciousness, or rapid neurologic decline can require urgent neurologic care.'),
        ('Biopsy, surgery, or radiation is being considered', 'The lesion’s location and accessibility determine what is realistic. Ask what information biopsy adds and what risks it carries before pursuing tissue solely for certainty.'),
        ('Treatment has already started', 'Track neurologic function, seizure frequency, steroid dose, and follow-up MRI together. Published feline outcome data are too sparse for a single reliable survival expectation.'),
    ],
    'prostate cancer': [
        ('Urination is difficult or impossible', 'Inability to pass urine is an emergency. Stabilization and restoration of urine flow come before a long-term cancer plan; ask whether catheterization, stenting, or another diversion procedure is feasible.'),
        ('Surgery is being considered or already done', 'Ask exactly what procedure is possible and what urinary complications are expected. Keep the full histopathology because published feline experience includes different carcinoma subtypes.'),
        ('Metastatic disease is present', 'Discuss symptom control and systemic options with the understanding that feline evidence is extremely sparse. Individual case reports should not be treated as a standard expected outcome.'),
    ],
    'hemangiosarcoma': [
        ('There is internal bleeding or suspected rupture', 'Pale gums, collapse, marked weakness, a distended abdomen, or breathing difficulty can be urgent. Stabilization and control of bleeding come before the long-term cancer plan.'),
        ('The tumor was already removed', 'Review the exact primary site, pathology, margins, and staging. Feline hemangiosarcoma behavior differs by site, so a superficial cutaneous tumor and visceral disease should not be given the same expectations.'),
        ('Visceral or metastatic disease is present', 'Systemic evidence in cats is limited. Focus the discussion on the sites causing clinical problems, realistic treatment goals, and whether any systemic option has feline-specific support.'),
    ],
    'histiocytic sarcoma': [
        ('The lesion has already been removed', 'Review margins and immunohistochemistry, then complete staging if it was not done. Preserve blocks or slides because rare-tumor expert review or research may require them.'),
        ('Several organs or sites are involved', 'This is a systemic problem rather than simply a margin problem. Discuss systemic treatment, symptom control, and realistic goals; canine histiocytic-sarcoma outcomes should not be substituted.'),
        ('The diagnosis is uncertain', 'Because feline histiocytic sarcoma is rare, pathology review and appropriate immunohistochemistry are especially important before committing to aggressive treatment.'),
    ],
    'chemodectoma': [
        ('There is pericardial or pleural fluid', 'Breathing difficulty, collapse, or cardiovascular compromise requires stabilization first. Fluid management and cardiology assessment come before debating long-term tumor therapy.'),
        ('The mass is growing or causing compression', 'Echocardiography and CT can define anatomy and help determine whether radiation, surgery, or medical treatment is realistic. Sampling a heart-base mass may carry risk, so tissue should have a clear purpose.'),
        ('Metastatic disease is present', 'Treatment is individualized because there is no dependable feline standard. Discuss mechanical local problems, systemic disease, and quality of life separately rather than relying on a single case report.'),
    ],
}
