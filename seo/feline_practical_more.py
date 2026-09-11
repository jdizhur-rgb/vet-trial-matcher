"""Additional feline-only guidance for rare cancers with sparse literature."""

FELINE_MORE = {
    'histiocytic sarcoma': {
        'prognosis': 'Feline histiocytic sarcoma is rare and often aggressive. In a study that recorded outcomes for feline histiocytic neoplasms, median survival for histiocytic sarcoma was 150 days, while disseminated and hemophagocytic disease had the shortest outcomes. Rare localized cases can behave very differently, so the site and whether disease is confined to one area matter.',
        'next': 'Confirm the diagnosis with histopathology and immunohistochemistry and determine whether disease is localized or disseminated before borrowing expectations from canine HS. If there is one resectable lesion, local treatment may be useful; disseminated disease generally requires a systemic discussion. Because published feline experience is small, trial or specialty-center review can be especially valuable.',
        'tests': 'Ask whether the pathology panel adequately confirms histiocytic origin and whether imaging, CBC/chemistry and site-specific sampling are needed to look for additional disease. Preserve pathology blocks and slides because expert review or research enrollment may require them.'
    },
    'glioma': {
        'prognosis': 'Primary feline glioma is uncommon, so there is not a reliable feline glioma survival median to quote. A multicenter radiation series of 22 cats with several types of intracranial tumors reported median progression-free survival of 510 days and overall survival of 515 days, but only one cat in that group had a glioma; those numbers therefore should not be presented as a glioma-specific prognosis. Individual outcome depends on tumor location, neurologic status and treatment options.',
        'next': 'Control seizures, brain swelling and other neurologic problems first, then use MRI findings to discuss whether biopsy, surgery, radiation or medical management is realistic. Do not apply canine glioma survival figures to a cat. A radiation oncologist or neurologist can help interpret whether the lesion is safely treatable without tissue confirmation.',
        'tests': 'MRI is the central imaging test. Ask how confident the imaging diagnosis is, whether biopsy would change treatment, and whether cerebrospinal fluid sampling is safe or useful for this lesion. Keep the exact steroid and anti-seizure drug doses because they affect neurologic assessment.'
    },
    'chemodectoma': {
        'prognosis': 'Chemodectoma, or aortic-body paraganglioma, is exceptionally rare in cats, so there is no dependable feline median survival. Published cases range from rapidly progressive metastatic disease to prolonged control: one cat treated with surgery followed by toceranib was euthanized 31 months after diagnosis. That is a single case, not an expected survival time.',
        'next': 'First define what the heart-base mass is doing mechanically: pleural or pericardial fluid, obstruction of blood flow and invasion of major vessels can matter more immediately than the tumor label. Stabilization comes first when fluid or cardiovascular compromise is present. Once stable, CT and echocardiography can help determine whether surgery, radiation, medical treatment or monitoring is realistic.',
        'tests': 'Echocardiography and thoracic CT can define the mass, effusion, vascular invasion and other thoracic disease. Tissue diagnosis can be difficult or risky at the heart base, so ask whether sampling will actually change management and how it can be obtained safely. Histopathology and immunohistochemistry are needed to distinguish chemodectoma from other heart-base tumors when tissue is available.'
    },
}

SOURCES = {
    'histiocytic sarcoma': ['PMID:25665137', 'PMID:32885737', 'PMID:41585534'],
    'glioma': ['PMID:30339060', 'PMID:23651604'],
    'chemodectoma': ['PMID:35811937', 'PMID:34399378', 'PMID:37533454', 'PMID:38706413'],
}
