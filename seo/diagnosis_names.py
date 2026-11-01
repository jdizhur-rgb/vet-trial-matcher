"""Owner-facing search wording; these labels never change diagnosis matching.

Broad anatomy terms retain the exact subtype after a colon. They are not
synonyms that allow another bone, liver, brain or mouth tumor into a trial.
"""

OWNER_NAMES = {
    'osteosarcoma': 'Bone cancer: osteosarcoma',
    'hepatocellular carcinoma': 'Liver cancer: hepatocellular carcinoma',
    'mammary carcinoma': 'Breast cancer: mammary carcinoma',
    'glioma': 'Brain tumor: glioma',
    'meningioma': 'Brain tumor: meningioma',
    'nasal tumor': 'Nose cancer (nasal tumors)',
    'primary lung tumor': 'Primary lung cancer',
    'oral melanoma': 'Mouth cancer: oral melanoma',
    'oral squamous cell carcinoma': 'Mouth cancer: oral squamous cell carcinoma',
    'thyroid carcinoma': 'Thyroid cancer (thyroid carcinoma)',
    'urothelial carcinoma': 'Bladder cancer (urothelial carcinoma)',
}

# Primary references reviewed 2026-11-01. These support terminology only,
# not protocol access, recruitment, eligibility, or clinical efficacy.
NAME_SOURCES = {
    'osteosarcoma': 'https://www.acvs.org/small-animal/bone-tumors-in-cats-and-dogs/',
    'hepatocellular carcinoma': 'https://www.acvs.org/small-animal/liver-tumors/',
    'mammary carcinoma': 'https://www.vet.cornell.edu/departments-centers-and-institutes/riney-canine-health-center/canine-health-information/mammary-cancer',
    'glioma': 'https://nutrition.vetmed.ucdavis.edu/news/clinical-trials-dogs-glioma-brain-tumors',
    'meningioma': 'https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/neurological-disorders',
    'nasal tumor': 'https://synergy.vetmed.ucdavis.edu/clinical-advance-spring-2020',
    'primary lung tumor': 'https://www.acvs.org/small-animal/lung-lobe-tumors/',
    'oral melanoma': 'https://www.acvs.org/small-animal/oral-tumors/',
    'oral squamous cell carcinoma': 'https://www.acvs.org/small-animal/oral-tumors/',
    'thyroid carcinoma': 'https://www.acvs.org/small-animal/thyroid-tumors/',
    'urothelial carcinoma': 'https://vet.purdue.edu/wcorc/clinical-trials/canine-urinary-bladder-cancer.php',
}


def owner_diagnosis_name(key: str) -> str:
    return OWNER_NAMES.get(key, key.capitalize())


def diagnosis_title(key: str, species: str) -> str:
    if key == 'urothelial carcinoma':
        terms = 'TCC / urothelial carcinoma' if species == 'dogs' else 'urothelial carcinoma'
        return f'Bladder cancer clinical trials for {species} ({terms})'
    return f'{owner_diagnosis_name(key)} clinical trials for {species}'
