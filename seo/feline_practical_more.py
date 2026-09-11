"""Additional feline-only guidance for rare cancers with sparse literature."""

FELINE_MORE = {
    'histiocytic sarcoma': {
        'prognosis': 'Feline histiocytic sarcoma is rare and often aggressive. In a study that recorded outcomes for feline histiocytic neoplasms, median survival for histiocytic sarcoma was 150 days. Rare localized cases can behave very differently, so the site and whether disease is confined to one area matter.',
        'next': 'Confirm the diagnosis with histopathology and immunohistochemistry and determine whether disease is localized or disseminated before borrowing expectations from canine HS. If there is one resectable lesion, local treatment may be useful; disseminated disease generally requires a systemic discussion. Because published feline experience is small, trial or specialty-center review can be especially valuable.',
        'tests': 'Ask whether the pathology panel adequately confirms histiocytic origin and whether imaging, CBC/chemistry and site-specific sampling are needed to look for additional disease. Preserve pathology blocks and slides because expert review or research enrollment may require them.'
    },
    'glioma': {
        'prognosis': 'Primary feline glioma is uncommon, so there is not a reliable feline glioma survival median to quote. A multicenter radiation series of cats with several types of intracranial tumors cannot be used as a glioma-specific prognosis because very few cats had glioma. Individual outcome depends on tumor location, neurologic status and treatment options.',
        'next': 'Control seizures, brain swelling and other neurologic problems first, then use MRI findings to discuss whether biopsy, surgery, radiation or medical management is realistic. Do not apply canine glioma survival figures to a cat. A radiation oncologist or neurologist can help interpret whether the lesion is safely treatable without tissue confirmation.',
        'tests': 'MRI is the central imaging test. Ask how confident the imaging diagnosis is, whether biopsy would change treatment, and whether cerebrospinal fluid sampling is safe or useful for this lesion. Keep the exact steroid and anti-seizure drug doses because they affect neurologic assessment.'
    },
    'chemodectoma': {
        'prognosis': 'Chemodectoma, or aortic-body paraganglioma, is exceptionally rare in cats, so there is no dependable feline median survival. Published experience consists largely of individual cases, so a long-surviving case should not be presented as an expected outcome.',
        'next': 'First define what the heart-base mass is doing mechanically: pleural or pericardial fluid, obstruction of blood flow and invasion of major vessels can matter more immediately than the tumor label. Stabilization comes first when fluid or cardiovascular compromise is present. Once stable, CT and echocardiography can help determine whether surgery, radiation, medical treatment or monitoring is realistic.',
        'tests': 'Echocardiography and thoracic CT can define the mass, effusion, vascular invasion and other thoracic disease. Tissue diagnosis can be difficult or risky at the heart base, so ask whether sampling will actually change management and how it can be obtained safely. Histopathology and immunohistochemistry are needed to distinguish chemodectoma from other heart-base tumors when tissue is available.'
    },
    'prostate cancer': {
        'prognosis': 'Prostate cancer is exceptionally rare in cats, so there is no reliable feline median survival or established standard treatment. Most published feline cases have behaved aggressively and many reported cats survived less than three months, but the literature is dominated by case reports. Exceptional longer survivors have been reported after surgery, including one cat alive two years after prostatectomy for a low-grade sarcomatoid carcinoma. Those individual cases should not be treated as an expected outcome.',
        'next': 'The immediate practical question is whether the mass is interfering with urination or defecation and whether there is metastatic disease. Inability to pass urine is an emergency. Once the cat is stable, define the tumor location and extent before deciding whether surgery, a urine-diversion procedure, medical treatment or supportive care is realistic. Do not borrow canine prostate-cancer drug expectations or survival figures.',
        'tests': 'Abdominal ultrasound or CT can define the prostate, urethra, bladder and regional lymph nodes. Chest imaging is reasonable because lung metastasis has been reported. Cytology or histopathology is needed to establish the tumor type when a sample can be obtained safely; ask whether sampling will change the treatment plan before an invasive procedure.'
    },
}

SOURCES = {
    'histiocytic sarcoma': ['PMID:32885737', 'PMID:33282334', 'PMID:36366728'],
    'glioma': ['PMID:30339060', 'PMID:23651604'],
    'chemodectoma': ['PMID:35811937', 'PMID:34399378', 'PMID:37533454', 'PMID:38706413'],
    'prostate cancer': ['PMID:19740688', 'PMID:15546773', 'PMID:12322712'],
}

# Importing this module activates only these independently reviewed feline entries.
from feline_practical_content import FELINE_PRACTICAL
FELINE_PRACTICAL.update(FELINE_MORE)
