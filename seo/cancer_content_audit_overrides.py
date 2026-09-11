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
}

FELINE_PRACTICAL_OVERRIDES = {
    'osteosarcoma': {
        'prognosis': (
            'Feline osteosarcoma often has a longer course than the typical canine disease, but metastasis '
            'is not rare and should not be minimized. A recent multicenter study of appendicular feline '
            'osteosarcoma reported a median survival of about 469 days. Site, visible metastasis and local '
            'control remain major prognostic factors, and the role of adjuvant chemotherapy deserves an '
            'individual discussion rather than being dismissed automatically.'
        ),
        'next': (
            'Separate appendicular from axial disease, control pain and assess fracture risk, and stage the '
            'chest before treatment. For a resectable limb tumor, amputation is usually the main local '
            'treatment. Discuss whether adjuvant chemotherapy is reasonable for this cat based on stage and '
            'pathology instead of assuming that cats never benefit from systemic treatment.'
        ),
    },
}
