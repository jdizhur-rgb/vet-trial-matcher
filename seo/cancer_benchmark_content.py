"""High-depth owner-guide content used by the shared cancer-page renderer.

Histiocytic sarcoma is the quality benchmark: it lives in the same architecture as
other diagnoses, but keeps its diagnosis-specific depth. Other diagnoses can add
waiting/questions here only when the copy is genuinely disease-specific.
"""

CANINE_PRACTICAL = {
    'histiocytic sarcoma': {
        'prognosis': (
            'HS is serious, but the outlook varies a lot. In published groups of dogs, '
            'median survival has been roughly 2–3 months for disseminated disease and '
            'about 13–19 months in some dogs with localized HS treated aggressively. '
            'Some dogs do much better or worse than these numbers. No statistic can '
            'predict your dog. The practical point is that time matters.'
        ),
        'next': (
            'An important next step is usually staging — checking whether cancer is '
            'present anywhere else in the body. This commonly includes chest imaging '
            'and abdominal imaging; other tests depend on where the original tumor was '
            'found. With HS, it makes sense to move the process along rather than simply '
            'wait for the next routine appointment.'
        ),
        'tests': (
            'There is no single cancer test that tells every dog with HS which treatment '
            'will work. If additional tumor testing or genomic profiling is available, '
            'ask whether the result will change treatment or trial eligibility now. If '
            'testing may be useful later, ask whether the pathology lab can retain the '
            'tumor block or slides from surgery.'
        ),
        'waiting': (
            'Waiting does not mean there is nothing to do. Ask about a cancellation list '
            'or another oncology center if the appointment is far away. Complete '
            'recommended staging if your veterinary team can arrange it, and check '
            'clinical trials before the next treatment decision. Some trials require a '
            'tumor to still be measurable or exclude certain previous chemotherapy or '
            'radiation. Checking early does not commit you to a trial; it shows what '
            'options exist before one is accidentally closed.'
        ),
        'questions': [
            'Is this localized HS or is there evidence that it has spread?',
            'Is the staging we have enough, or is anything important still missing?',
            'If surgery was done, are the margins adequate and does the site need more local treatment?',
            'Do you recommend systemic treatment now, and what are the realistic options?',
            'Could treatment we start now affect eligibility for a clinical trial later?',
        ],
    },
}

CANINE_BRANCHES = {
    'histiocytic sarcoma': [
        ('The tumor is still there',
         'If surgery is possible, ask whether it can realistically be removed with clean margins. Surgery is often the best local treatment for a removable localized tumor. If clean margins are unlikely, ask what other local-control options are reasonable. It is also worth checking trials before surgery when there is time to do so safely because some studies require a measurable tumor, biopsy, or direct treatment of the tumor. This is not a reason to delay surgery your veterinary team considers necessary.'),
        ('The tumor was already removed',
         'Get the pathology report and check the margin status. The next questions are whether staging shows disease elsewhere, whether the surgical site needs more local treatment, and whether systemic treatment is recommended because HS can spread microscopically.'),
        ('The cancer has spread or cannot be removed',
         'Surgery may no longer be the main decision. Ask about systemic treatment, local treatment for a tumor that is causing problems, and clinical trials that accept measurable or metastatic disease.'),
        ('My dog is already in treatment',
         'You may still have trial options. Look specifically for studies that allow previous surgery, chemotherapy, or radiation, and ask what options remain if the current treatment stops working.'),
    ],
}
