"""Small evidence-driven corrections found during the English cancer-page audit.

Keep these narrow: this file is for statements that were misleading, over-broad or
unnecessarily repetitive in the generated owner pages.
"""

CANINE_PRACTICAL_OVERRIDES = {
    'glioma': {
        'prognosis': (
            'Radiation can provide meaningful control for canine glioma, but published outcomes vary by '
            'case selection, radiation protocol and whether the diagnosis is presumed on MRI or confirmed '
            'with tissue. A recent stereotactic-radiation series reported a median overall survival of about '
            '349 days. It is more useful to discuss the individual tumor location, neurologic status and '
            'treatment plan than to quote a broad 12–23 month range as though it applies to every dog.'
        ),
        'next': (
            'Control seizures or brain swelling when present, then decide whether MRI alone is sufficient '
            'for treatment planning or whether biopsy or surgery would change the plan. If a brain-tumor '
            'trial is realistic, check its tissue and prior-treatment requirements before definitive treatment '
            'when medically safe.'
        ),
    },
    'hemangiosarcoma': {
        'prognosis': (
            'Visceral hemangiosarcoma is aggressive and can bleed suddenly. One retrospective study of 37 dogs '
            'reported median survival of 66 days with surgery alone and 274 days with surgery followed by '
            'doxorubicin, but only 14 dogs received chemotherapy and the study population was selected. These '
            'figures show that chemotherapy can improve control in some dogs; they should not be presented as '
            'a universal expectation. Stage, primary site and whether rupture or metastasis is present remain '
            'major determinants of outcome.'
        ),
    },
}

FELINE_PRACTICAL_OVERRIDES = {
    'osteosarcoma': {
        'prognosis': (
            'Feline osteosarcoma often has a longer course than the typical canine disease, but metastasis '
            'is not rare and should not be minimized. A 2026 multicenter study of appendicular feline '
            'osteosarcoma reported a median survival of about 469 days and metastasis in about 36% of cats. '
            'In cats without lung metastasis before surgery, adjuvant chemotherapy was associated with longer '
            'survival in that retrospective study. Site, visible metastasis and local control remain major '
            'prognostic factors.'
        ),
        'next': (
            'Separate appendicular from axial disease, control pain and assess fracture risk, and stage the '
            'chest before treatment. For a resectable limb tumor, amputation is usually the main local '
            'treatment. Discuss whether adjuvant chemotherapy is reasonable for this cat based on stage and '
            'pathology instead of assuming that surgery alone is always sufficient.'
        ),
    },
    'thyroid carcinoma': {
        'prognosis': (
            'Feline thyroid carcinoma is rare, so the evidence base is small. In a series of eight cats with '
            'functional thyroid carcinoma treated with high-dose radioactive iodine, treatment was successful '
            'in six and survival ranged from 181 to 2,381 days. That small series supports the possibility of '
            'long control in selected iodine-responsive tumors, but it is not a general survival estimate for '
            'all feline thyroid carcinomas.'
        ),
        'next': (
            'First distinguish suspected carcinoma from ordinary benign feline hyperthyroidism, then define '
            'local invasion, metastatic stage and whether the tumor is functional and potentially iodine-avid. '
            'Those findings determine whether surgery, radioactive iodine, radiation or another approach is '
            'realistic.'
        ),
    },
    'prostate cancer': {
        'prognosis': (
            'Feline prostate cancer is exceptionally rare. Published evidence consists mostly of case reports '
            'and very small series, so there is no reliable feline median survival or established standard '
            'treatment. Reported tumors are often locally aggressive and may metastasize, but an exceptional '
            'long-surviving case should not be used as the expected outcome.'
        ),
        'next': (
            'The immediate question is whether the mass is interfering with urination or defecation and '
            'whether metastatic disease is present. Inability to pass urine is an emergency. Once the cat is '
            'stable, define the local anatomy before deciding whether surgery, a procedure to maintain urine '
            'flow, systemic treatment or supportive care is realistic.'
        ),
    },
    'oral melanoma': {
        'prognosis': (
            'Feline oral melanoma is rare and published outcome data are sparse. Small retrospective series '
            'suggest aggressive behavior, but they are too small for a single survival number to be treated as '
            'a dependable prediction. Diagnostic certainty, local extent and metastatic stage matter more than '
            'borrowing canine melanoma expectations.'
        ),
        'next': (
            'Confirm the diagnosis, especially for poorly pigmented tumors, then define local invasion and '
            'metastatic stage. Eating, oral pain and bleeding should be managed alongside decisions about '
            'surgery, radiation or another local treatment.'
        ),
    },
}
