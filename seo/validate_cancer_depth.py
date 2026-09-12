"""Static semantic coverage checks for reviewed owner cancer guides."""
from cancer_owner_depth import DOG_DEPTH, CAT_DEPTH
from canine_branch_content import ADDITIONAL_BRANCHES
from feline_branch_content import FELINE_BRANCHES

CANONICAL = {
'histiocytic sarcoma','lymphoma','mast cell tumor','soft tissue sarcoma','hemangiosarcoma',
'osteosarcoma','oral melanoma','melanoma','oral squamous cell carcinoma','squamous cell carcinoma',
'urothelial carcinoma','hepatocellular carcinoma','mammary carcinoma','thyroid carcinoma',
'prostate cancer','primary lung tumor','glioma','meningioma','nasal tumor','leukemia',
'multiple myeloma','chemodectoma'
}

GENERIC_QUESTIONS = {
'What exact subtype, grade and stage do we know?',
'Is anything important still missing before we choose treatment?',
'What is the goal of treatment: cure, long-term control, slowing spread, or symptom control?',
'What would make you change this plan?',
'Could treatment we start now affect clinical-trial eligibility later?',
}


def _validate_depth(name, data):
    assert set(data) == CANONICAL, f'{name} depth coverage mismatch: missing={sorted(CANONICAL-set(data))}, extra={sorted(set(data)-CANONICAL)}'
    for diagnosis, item in data.items():
        waiting = item.get('waiting','').strip()
        questions = item.get('questions',[])
        assert waiting, f'{name} {diagnosis}: missing waiting guidance'
        assert len(questions) >= 3, f'{name} {diagnosis}: fewer than 3 specific questions'
        assert not GENERIC_QUESTIONS.intersection(questions), f'{name} {diagnosis}: legacy generic question survived'
        assert len(set(questions)) == len(questions), f'{name} {diagnosis}: duplicate questions'


def validate():
    _validate_depth('dog', DOG_DEPTH)
    _validate_depth('cat', CAT_DEPTH)
    dog_branches = set(ADDITIONAL_BRANCHES) | {'histiocytic sarcoma'}
    assert dog_branches == CANONICAL, f'dog branch coverage mismatch: missing={sorted(CANONICAL-dog_branches)}'
    assert set(FELINE_BRANCHES) == CANONICAL, f'cat branch coverage mismatch: missing={sorted(CANONICAL-set(FELINE_BRANCHES))}'
    return True


if __name__ == '__main__':
    validate()
    print('CANCER_DEPTH_VALIDATION_OK', len(CANONICAL), 'diagnoses x 2 species')
