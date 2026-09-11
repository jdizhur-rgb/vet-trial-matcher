"""Diagnosis-specific owner decision branches for canine cancer pages."""

ADDITIONAL_BRANCHES = {
    'thyroid carcinoma': [
        ('The thyroid mass is movable and appears resectable', 'A freely movable thyroid mass is often the setting where surgery has the strongest role. Ask whether vascular invasion or bilateral disease is present and whether chest staging changes the plan before assuming the neck mass is a simple surgery.'),
        ('The mass is fixed or invasive', 'Fixed tumors can involve major vessels and surrounding structures. Radiation, radioactive iodine in selected tumors, targeted treatment, or combinations may be more realistic than attempting a high-morbidity surgery.'),
        ('Surgery has already been done', 'Review margins, vascular invasion, histologic findings and staging. A removed thyroid carcinoma does not automatically need additional therapy; the next step depends on residual disease and metastatic risk.'),
        ('Metastatic disease is present', 'Ask whether the tumor is iodine-avid and whether local neck control is still needed. Systemic or targeted options and trials may become more important, but treatment depends on where the disease has spread and whether it is progressing.')],
    'prostate cancer': [
        ('Urination is still normal', 'Use this window to define local extent and stage lymph nodes, lungs and bone as appropriate. Treatment planning is easier before obstruction or severe pain develops.'),
        ('Urination is difficult or blocked', 'Urinary obstruction can become urgent. Ask about procedures that can restore urine flow and how radiation or other local treatment fits with systemic therapy; symptom relief may need to come before the longer-term cancer plan.'),
        ('There is pelvic or bone pain', 'Prostatic carcinoma can invade locally and spread to bone. Make pain control explicit and ask whether imaging of painful areas would change radiation, systemic treatment or trial choices.'),
        ('Treatment has already started or disease has spread', 'Keep a clear record of NSAIDs, chemotherapy, radiation and response. Prior treatment and metastatic sites affect both the next standard option and trial eligibility.')],
    'primary lung tumor': [
        ('There is one lung mass', 'First decide whether this is likely a primary lung tumor and whether it can be removed with a lung lobectomy. Chest CT and intrathoracic lymph-node assessment are especially useful when surgery is being considered.'),
        ('The lung mass was already removed', 'Review the exact histology, grade or differentiation when reported, surgical margins and lymph-node status. Those findings help determine whether surveillance alone or additional systemic treatment is reasonable.'),
        ('There are multiple lung nodules', 'Multiple nodules raise the possibility of metastatic disease from another primary cancer or multifocal lung disease. Confirm the diagnosis before treating the lungs as one resectable primary tumor.'),
        ('The tumor is unresectable or metastatic', 'Systemic treatment, radiation for selected lesions, and trials may be considered depending on pathology and symptoms. Breathing comfort and the actual pace of progression should stay central to the plan.')],
    'glioma': [
        ('MRI suggests a glioma and treatment has not started', 'Control seizures and brain swelling when needed, then compare radiation, surgery or biopsy-based approaches. If a brain-tumor trial is realistic, check its tissue and prior-treatment requirements before starting an irreversible treatment when medically safe.'),
        ('My dog is having seizures', 'Seizure control is an immediate part of care. Keep a seizure log and medication list, and ask what change in seizure frequency or duration should prompt urgent reassessment rather than waiting for the oncology appointment.'),
        ('Biopsy or surgery is being considered', 'Ask what information tissue will add, what the procedural risk is, and whether the result will change treatment or trial access. A presumed glioma on MRI and a tissue-confirmed glioma are not always interchangeable for studies.'),
        ('Radiation or another treatment has already started', 'Track steroid dose, seizure medications, neurologic changes and treatment dates. Later MRI changes can reflect tumor, treatment effect or inflammation, so interpretation often needs the full treatment timeline.')],
    'meningioma': [
        ('The tumor was found on MRI', 'The next decision is usually based on location, size, neurologic signs and whether surgery is realistically accessible. Radiation may be appropriate even for an operable tumor, so compare both options rather than assuming surgery is automatically best.'),
        ('My dog is having seizures or other neurologic signs', 'Control symptoms while the definitive plan is arranged. Worsening seizures, inability to walk, severe disorientation or rapidly changing neurologic signs can justify earlier reassessment.'),
        ('Surgery has already been done', 'Review the pathology grade when available and whether residual tumor remains on postoperative imaging. Radiation may be discussed for incomplete removal, recurrence or higher-risk pathology.'),
        ('The tumor cannot be removed safely', 'Definitive or stereotactic radiation can provide meaningful control in selected dogs. Ask what outcome is realistic for this tumor location and whether tissue confirmation is necessary before treatment.')],
    'nasal tumor': [
        ('Biopsy is not done yet', 'CT and tissue diagnosis usually belong together in planning. Several tumor types can look similar in the nose, so avoid choosing a cancer-specific treatment from imaging alone when a biopsy can be obtained safely.'),
        ('The diagnosis is confirmed and radiation is being planned', 'Ask what the CT shows about cribriform-plate involvement, orbit or surrounding structures, and lymph nodes. Those details help frame prognosis and the choice between conventional and stereotactic radiation approaches.'),
        ('Nosebleeds or airflow problems are worsening', 'Local progression can become the immediate problem even before distant spread. Ask whether timing of radiation or another local measure should be accelerated rather than waiting through a long routine queue.'),
        ('Radiation has already been given or the tumor has recurred', 'Re-irradiation, systemic treatment or a trial may be possible in selected cases, but prior dose and field matter. Keep the radiation summary because a new center will need it to judge what can be done safely.')],
    'leukemia': [
        ('The type of leukemia is not clear yet', 'Do not let “leukemia” remain the whole diagnosis. Acute versus chronic and lymphoid versus myeloid disease can mean very different urgency, treatment and prognosis, so immunophenotyping and marrow testing may be important.'),
        ('Acute leukemia is suspected or confirmed', 'Acute leukemia can worsen quickly because normal blood-cell production is affected. Severe anemia, bleeding, infection risk or weakness may need supportive care while systemic treatment is being planned.'),
        ('Chronic leukemia is suspected or confirmed', 'Some chronic leukemias can be followed or treated less intensively for longer periods. The decision depends on cell type, blood counts, symptoms, progression and organ involvement rather than the diagnosis name alone.'),
        ('Treatment has already started', 'Track blood counts, drug doses and response over time. For relapsed or resistant disease, the exact leukemia type and previous drugs are essential for rescue treatment or trial matching.')],
    'multiple myeloma': [
        ('Diagnosis is suspected but not complete', 'The diagnosis usually comes from several pieces together: abnormal proteins, marrow findings, bone lesions and related organ effects. Ask which criteria are already met and which tests would actually change treatment.'),
        ('Kidney injury, high calcium or anemia is present', 'These complications can be as important as the tumor burden itself. Supportive care and systemic treatment may need to start promptly rather than waiting only for a specialist visit.'),
        ('There is painful bone disease', 'Radiation can be useful for selected painful focal lesions while systemic treatment addresses the disease throughout the body. Make pain control part of the cancer plan from the start.'),
        ('Treatment has already started', 'Follow the monoclonal protein, blood counts, kidney values, calcium and clinical signs over time. Response is an important prognostic marker and helps decide when a treatment change is actually needed.')],
    'chemodectoma': [
        ('The heart-base mass was just found', 'Ask whether it is causing compression, arrhythmia or fluid around the heart and whether serial imaging shows active growth. Some heart-base tumors grow slowly enough that immediate treatment is not always necessary.'),
        ('There is fluid around the heart', 'Pericardial effusion can cause weakness, collapse or breathing problems and may need urgent management. Treating the fluid problem and deciding how to control the tumor are related but separate decisions.'),
        ('The mass is growing or causing symptoms', 'Radiation or targeted therapy such as toceranib may be considered in selected dogs. The choice depends on size, compression, cardiac function, metastasis and prior treatment.'),
        ('Metastases are present', 'Metastatic disease does not automatically mean the primary heart-base mass must be treated immediately. Ask which site is actually driving symptoms and what treatment is expected to improve control or quality of life.')],
}
