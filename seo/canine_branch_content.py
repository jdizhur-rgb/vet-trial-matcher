"""Diagnosis-specific owner decision branches for canine cancer pages.

Only branches that materially change the next decision belong here. Generic staging,
trial-checking, and treatment boilerplate is intentionally omitted.
"""

ADDITIONAL_BRANCHES = {
    'lymphoma': [
        ('Prednisone has already been started', 'Tell the oncologist the exact dose and start date, and do not stop it abruptly without instructions. Prednisone can alter lymphoma cells and may affect later diagnostics, drug response, or trial eligibility.'),
        ('Chemotherapy has already started or lymphoma has returned', 'Keep the protocol, doses, dates, and response together. The drugs already used and the length of the first remission help determine rescue treatment and trial eligibility.'),
        ('My dog is getting sick while we wait', 'Poor appetite, marked weakness, repeated vomiting, breathing difficulty, fever, or rapidly enlarging nodes can justify earlier assessment rather than waiting for a routine oncology slot.'),
    ],
    'mast cell tumor': [
        ('The tumor was removed with incomplete margins', 'A dirty margin does not automatically mean the same next step for every mast cell tumor. Re-excision, radiation, monitoring, or systemic treatment depend on grade, site, measured margin, and nodal status.'),
        ('A regional lymph node is positive', 'Nodal spread raises risk but is not the same as widespread metastatic disease. Ask whether the involved node should be treated locally and whether systemic therapy is recommended for this grade and stage.'),
        ('The tumor is recurrent or cannot be completely removed', 'Reassess local-control options rather than assuming another marginal surgery is best. Radiation, systemic therapy, and selected investigational local treatments may have different roles depending on site and measurable disease.'),
    ],
    'soft tissue sarcoma': [
        ('It was removed with clean margins', 'Grade still matters. Many low- or intermediate-grade soft tissue sarcomas need no automatic chemotherapy after complete excision; use grade and other pathology features to decide whether staging or additional treatment adds value.'),
        ('It was removed with incomplete margins', 'Do not wait automatically for visible regrowth. Re-excision is often considered when feasible; radiation or another local-control method may be reasonable when wider surgery would be difficult.'),
        ('It has recurred or cannot be widely removed', 'Re-image the local site and restage before simply repeating surgery. Radiation, systemic treatment, electrochemotherapy, or a trial may be considered according to grade, anatomy, and measurable disease.'),
    ],
    'hemangiosarcoma': [
        ('A splenic or abdominal mass is bleeding or may have ruptured', 'Pale gums, collapse, marked weakness, a distended abdomen, or breathing trouble can be urgent. Stabilization and control of bleeding come before a long-term cancer plan, and a suspected splenic mass is not yet a confirmed hemangiosarcoma until pathology establishes it.'),
        ('The spleen or primary tumor was already removed', 'Confirm the pathology diagnosis and stage, and note whether rupture or abdominal bleeding occurred. Those details help frame the discussion about adjuvant chemotherapy and expected risk.'),
        ('A right-atrial or cardiac mass is suspected', 'Echocardiography helps define the mass and whether pericardial fluid is present. Collapse or breathing difficulty with fluid around the heart can require urgent treatment; cardiac hemangiosarcoma is a different local problem from splenic disease.'),
        ('Metastases are already visible', 'Systemic treatment and symptom control become central. Ask what treatment is realistically expected to accomplish and which disease site is most likely to cause the next clinical problem.'),
    ],
    'osteosarcoma': [
        ('Amputation or local surgery is already done', 'Review pathology and chest staging, then discuss systemic treatment. Clear lung imaging does not rule out microscopic metastatic disease, so local control and metastatic-risk treatment remain separate decisions.'),
        ('Amputation is not an option', 'Make pain control and fracture risk explicit. Palliative or stereotactic radiation and other local approaches may help selected dogs even when definitive surgery is not possible.'),
        ('Metastases are already visible', 'Treatment becomes individualized around pain, mobility, breathing, and the sites of spread. Visible metastasis changes prognosis and some trial criteria but does not make every treatment option meaningless.'),
    ],
    'oral melanoma': [
        ('The oral tumor was already removed', 'Get the measured margins, original tumor size, and staging results. A visually clean mouth does not answer the metastatic-risk question; lymph-node and lung status still matter.'),
        ('A regional lymph node is positive', 'A positive node changes stage and prognosis. Ask whether local treatment of the node is appropriate and how systemic options fit with control of the primary site.'),
        ('There is distant metastatic disease', 'The emphasis shifts toward systemic control and comfort while local mouth treatment may still help bleeding, pain, or function. Use the actual stage rather than the diagnosis name alone when considering trials.'),
    ],
    'melanoma': [
        ('The melanoma is on a toe or nail bed', 'Digital melanoma carries more metastatic risk than many ordinary cutaneous melanomas. Regional lymph-node evaluation and chest staging become more relevant, and local control often requires definitive treatment of the digit.'),
        ('The melanoma is oral or another mucosal site', 'Treat it as a higher-risk melanoma until staging says otherwise. Local control and metastatic staging both matter, and prognosis should not be borrowed from low-risk cutaneous melanoma.'),
        ('It has recurred or spread', 'Re-stage before simply repeating the previous plan. Systemic or immune-based options may become more relevant, while local treatment can still help pain, bleeding, or function at a troublesome site.'),
    ],
    'oral squamous cell carcinoma': [
        ('The tumor was removed with incomplete margins', 'Review measured margins and whether bone was involved. A wider resection or radiation may offer better local control than waiting for visible regrowth, depending on anatomy and expected morbidity.'),
        ('Complete surgery is not feasible', 'Radiation or another local treatment may still provide control or palliation. Eating, pain, bleeding, and oral function should be part of the treatment decision rather than treated as separate problems.'),
        ('Nodes or distant metastases are present', 'Confirm whether spread is regional or distant and what it actually changes. Local treatment may still be useful for the mouth while systemic options are considered separately.'),
    ],
    'squamous cell carcinoma': [
        ('The SCC is oral or nasal', 'Use site-specific guidance rather than a generic SCC prognosis. Oral and nasal tumors have different local anatomy, staging needs, and treatment options from a small cutaneous SCC.'),
        ('The lesion was already removed', 'Review the exact primary site, depth, subtype, and measured margins. Incomplete margins may justify additional local treatment depending on anatomy and expected behavior.'),
        ('It is extensive, recurrent, or metastatic', 'Separate the local-control problem from the systemic one. Treatment that improves function or comfort at the primary site can still be worthwhile even when distant disease is present.'),
    ],
    'urothelial carcinoma': [
        ('Urination is becoming difficult', 'A weak stream, repeated straining, or inability to pass urine can become urgent. Ask early how urine flow will be maintained if obstruction worsens rather than waiting for complete blockage.'),
        ('Treatment has already started', 'Track symptoms together with imaging measurements and exact drug dates. Stable disease can be a meaningful response in urothelial carcinoma; lack of complete tumor disappearance does not automatically mean treatment has failed.'),
        ('The cancer has spread', 'Systemic treatment becomes central, while local measures may still be needed for urine flow or pain. Previous drugs and metastatic sites help determine what remains reasonable.'),
    ],
    'hepatocellular carcinoma': [
        ('Liver surgery has already been done', 'Review final pathology, margins, and whether staging showed additional lesions. A completely resected solitary massive hepatocellular carcinoma can behave very differently from multifocal disease and does not automatically require chemotherapy.'),
        ('There are multiple or diffuse liver lesions', 'Do not apply favorable surgery statistics from solitary massive hepatocellular carcinoma. Confirm the diagnosis, liver function, and distribution of disease before deciding whether biopsy, systemic treatment, or supportive care is useful.'),
        ('The mass cannot be removed', 'Ask why it is unresectable: vascular involvement, central location, multifocal disease, metastasis, or overall health. Those reasons lead to different realistic alternatives.'),
    ],
    'mammary carcinoma': [
        ('Surgery has already been done', 'Use tumor size, grade, measured margins, lymphovascular invasion, and lymph-node status to decide whether surgery alone is reasonable or an oncology discussion is warranted.'),
        ('A regional lymph node is positive', 'Nodal metastasis raises the risk of distant disease and can change staging and systemic-treatment recommendations. Confirm that the sampled node actually drains the affected mammary region.'),
        ('There is metastatic, ulcerated, or recurrent disease', 'Systemic treatment and comfort become more important. Local surgery or radiation may still help selected painful, infected, ulcerated, or bleeding lesions when the expected benefit justifies recovery.'),
    ],
    'thyroid carcinoma': [
        ('The mass is fixed or invasive', 'Fixed tumors can involve major vessels and surrounding structures. Radiation, radioactive iodine in selected tumors, or systemic treatment may be more realistic than attempting a high-morbidity surgery.'),
        ('Surgery has already been done', 'Review margins, vascular invasion, histologic findings, and staging. A removed thyroid carcinoma does not automatically need more treatment; the next step depends on residual disease and metastatic risk.'),
        ('Metastatic disease is present', 'Ask whether the tumor is iodine-avid and whether local neck control is still needed. The best systemic option depends on where disease has spread and whether it is progressing.'),
    ],
    'prostate cancer': [
        ('Urination is difficult or blocked', 'Urinary obstruction can become urgent. Restoring urine flow may need to come before the longer-term cancer plan, and interventional procedures can sometimes be part of that strategy.'),
        ('There is pelvic or bone pain', 'Prostatic carcinoma can invade locally and spread to bone. Make pain control explicit and ask whether imaging the painful area would change radiation or systemic treatment.'),
        ('Treatment has already started or disease has spread', 'Keep a clear record of NSAIDs, chemotherapy, radiation, and response. Prior treatment and metastatic sites affect what systemic or local options remain reasonable.'),
    ],
    'primary lung tumor': [
        ('The lung mass was already removed', 'Review the exact histology, grade or differentiation when reported, surgical margins, and lymph-node status. Those findings help determine whether surveillance alone or additional systemic treatment is reasonable.'),
        ('There are multiple lung nodules', 'Multiple nodules raise the possibility of metastatic disease from another primary cancer or multifocal lung disease. Do not apply surgery outcomes from a solitary primary mass until the diagnosis is secure.'),
        ('The tumor is unresectable or metastatic', 'Systemic treatment, radiation for selected lesions, and symptom-directed care may all have roles. Breathing comfort and the actual pace of progression should stay central to the plan.'),
    ],
    'glioma': [
        ('My dog is having seizures', 'Seizure control is an immediate part of care. Keep a seizure log and medication list, and ask what change in seizure frequency or duration should prompt urgent reassessment.'),
        ('Biopsy or surgery is being considered', 'Ask what information tissue will add, what the procedural risk is, and whether the result will actually change treatment or trial access. A presumed glioma on MRI and a tissue-confirmed glioma are not always interchangeable.'),
        ('Radiation or another treatment has already started', 'Track steroid dose, seizure medications, neurologic changes, and treatment dates. Later MRI changes can reflect tumor, treatment effect, or inflammation, so interpretation often requires the full treatment timeline.'),
    ],
    'meningioma': [
        ('My dog is having seizures or other neurologic signs', 'Control symptoms while the definitive plan is arranged. Worsening seizures, inability to walk, severe disorientation, or rapidly changing neurologic signs can justify earlier reassessment.'),
        ('Surgery has already been done', 'Review the pathology grade when available and whether residual tumor remains on postoperative imaging. Radiation may be discussed for incomplete removal, recurrence, or higher-risk pathology.'),
        ('The tumor cannot be removed safely', 'Definitive or stereotactic radiation can provide meaningful control in selected dogs. Ask what outcome is realistic for this location and whether tissue confirmation is necessary before treatment.'),
    ],
    'nasal tumor': [
        ('Biopsy is not done yet', 'Several tumor types can look similar in the nose, so imaging alone should not be used to choose a cancer-specific treatment when a biopsy can be obtained safely.'),
        ('Nosebleeds or airflow problems are worsening', 'Local progression can become the immediate problem before distant spread. Worsening bleeding or breathing may justify accelerating local treatment rather than waiting through a routine queue.'),
        ('Radiation has already been given or the tumor has recurred', 'Re-irradiation, systemic treatment, or a trial may be possible in selected cases, but the previous radiation dose and field matter. Keep the treatment summary because a new center will need it.'),
    ],
    'leukemia': [
        ('Acute leukemia is suspected or confirmed', 'Acute leukemia can worsen quickly because normal blood-cell production is affected. Severe anemia, bleeding, infection risk, or weakness may need supportive care while systemic treatment is being planned.'),
        ('Chronic leukemia is suspected or confirmed', 'Some chronic leukemias can be followed or treated less intensively for longer periods. Urgency depends on cell type, blood counts, symptoms, progression, and organ involvement.'),
        ('Treatment has already started', 'Track blood counts, drug doses, and response over time. For relapsed or resistant disease, the exact leukemia type and drugs already used are essential for the next decision.'),
    ],
    'multiple myeloma': [
        ('Kidney injury, high calcium, or anemia is present', 'These complications can be as important as the tumor burden itself. Supportive care and systemic treatment may need to start promptly rather than waiting only for a specialist visit.'),
        ('There is painful bone disease', 'Radiation can be useful for selected painful focal lesions while systemic treatment addresses disease throughout the body. Pain control and fracture or spinal risk should be explicit parts of the plan.'),
        ('Treatment has already started', 'Follow the monoclonal protein or other disease marker together with blood counts, kidney values, calcium, and clinical signs. Response helps determine whether a treatment change is actually needed.'),
    ],
    'chemodectoma': [
        ('There is fluid around the heart', 'Pericardial effusion can cause weakness, collapse, or breathing problems and may need urgent management. Treating the fluid problem and deciding whether to control the tumor are related but separate decisions.'),
        ('The mass is growing or causing compression', 'Radiation or targeted therapy may be considered in selected dogs. The decision depends on growth, compression, cardiac function, metastasis, and symptoms rather than the presence of a mass alone.'),
        ('Metastases are present', 'Metastatic disease does not automatically mean the primary heart-base mass is the most urgent problem. Ask which site is driving symptoms and what treatment is expected to improve control or quality of life.'),
    ],
}
