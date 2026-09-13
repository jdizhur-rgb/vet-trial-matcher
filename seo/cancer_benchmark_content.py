"""High-depth owner-guide content used by the shared cancer-page renderer.

Histiocytic sarcoma is the quality benchmark: it lives in the same architecture as
other diagnoses, but keeps its diagnosis-specific depth. Other diagnoses can add
waiting/questions here only when the copy is genuinely disease-specific.
"""

CANINE_PRACTICAL = {
    'histiocytic sarcoma': {
        'prognosis': (
            'HS is serious, but the outlook varies a lot. In published groups of dogs, '
            'median survival has been roughly 2–3 months for disseminated disease. '
            'Longer survival, around 13–19 months, has been reported in some published '
            'groups with particular localized forms treated aggressively, but those '
            'results should not be read as the expected outcome for every dog with '
            'localized HS. Some dogs do much better or worse than these numbers, and no '
            'statistic can predict an individual dog. The practical point is that the '
            'extent and location of disease matter greatly and time matters.'
        ),
        'next': (
            'Once the diagnosis is confirmed, the next decisions depend on whether HS is '
            'localized or disseminated, whether a localized tumor can be controlled '
            'completely, and whether systemic treatment should be discussed because HS '
            'can spread beyond the original site. If surgery has already been done, '
            'review the measured margins together with staging. Before another major '
            'treatment step, it is also worth checking whether a clinical trial requires '
            'measurable disease or limits previous treatment.'
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
            'or another oncology center if the appointment is far away. Gather the '
            'pathology report and any completed staging, arrange missing staging that '
            'your veterinary team recommends, and check clinical trials before the next '
            'treatment decision. Some trials require a tumor to still be measurable or '
            'exclude certain previous chemotherapy or radiation. Checking early does not '
            'commit you to a trial; it shows what options exist before one is accidentally '
            'closed.'
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
         'Get the pathology report and check the measured margin status. Clean removal can solve the local problem, but it does not by itself eliminate the risk that HS may spread elsewhere. The next questions are whether staging shows disease elsewhere and whether systemic treatment is recommended. Additional treatment to the surgical site is not automatic just because the diagnosis is HS; it depends on the margins, location and whether meaningful residual local disease is suspected.'),
        ('The cancer has spread or cannot be removed',
         'Surgery may no longer be the main decision. Ask about systemic treatment, local treatment for a tumor that is causing problems, and clinical trials that accept measurable or metastatic disease.'),
        ('My dog is already in treatment',
         'You may still have trial options. Look specifically for studies that allow previous surgery, chemotherapy, or radiation, and ask what options remain if the current treatment stops working.'),
    ],
}
