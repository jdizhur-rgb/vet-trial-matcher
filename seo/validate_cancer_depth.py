"""Semantic coverage checks for source layers and the built owner cancer guides."""
import html
import re
from pathlib import Path

from cancer_owner_depth import DOG_DEPTH, CAT_DEPTH
from cancer_treatment_factors import DOG_FACTORS, CAT_FACTORS
from canine_branch_content import ADDITIONAL_BRANCHES
from feline_branch_content import FELINE_BRANCHES
from cancer_benchmark_content import CANINE_PRACTICAL as BENCHMARK
from owner_friendly_descriptions import DOG as DOG_DESCRIPTIONS, CAT as CAT_DESCRIPTIONS
from owner_friendly_prognosis import DOG as DOG_PROGNOSIS, CAT as CAT_PROGNOSIS
from owner_friendly_next_steps import DOG as DOG_NEXT_STEPS, CAT as CAT_NEXT_STEPS
from owner_friendly_treatment_tests import DOG_TREATMENT, CAT_TREATMENT, DOG_TESTS, CAT_TESTS
from owner_friendly_factors import DOG as DOG_OWNER_FACTORS, CAT as CAT_OWNER_FACTORS
from owner_diagnostic_context import DOG_REPORT, CAT_REPORT, DOG_SIGNS, CAT_SIGNS

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


def _validate_factors(name, data):
    assert set(data) == CANONICAL, f'{name} factor coverage mismatch: missing={sorted(CANONICAL-set(data))}, extra={sorted(set(data)-CANONICAL)}'
    for diagnosis, text in data.items():
        assert text.strip(), f'{name} {diagnosis}: empty treatment factors'


def _validate_owner_layers():
    dog_expected = CANONICAL - {'histiocytic sarcoma'}
    for name, data in (
        ('dog descriptions', DOG_DESCRIPTIONS), ('dog prognosis', DOG_PROGNOSIS),
        ('dog next steps', DOG_NEXT_STEPS), ('dog treatment', DOG_TREATMENT),
        ('dog tests', DOG_TESTS), ('dog owner factors', DOG_OWNER_FACTORS),
    ):
        assert set(data) == dog_expected, f'{name} coverage mismatch'
    for name, data in (
        ('cat descriptions', CAT_DESCRIPTIONS), ('cat prognosis', CAT_PROGNOSIS),
        ('cat next steps', CAT_NEXT_STEPS), ('cat treatment', CAT_TREATMENT),
        ('cat tests', CAT_TESTS), ('cat owner factors', CAT_OWNER_FACTORS),
    ):
        assert set(data) == CANONICAL, f'{name} coverage mismatch'
    for name, data in (
        ('dog report context', DOG_REPORT), ('cat report context', CAT_REPORT),
        ('dog home signs', DOG_SIGNS), ('cat home signs', CAT_SIGNS),
    ):
        assert set(data) == CANONICAL, f'{name} coverage mismatch'
        assert all(text.strip() for text in data.values()), f'{name} contains empty copy'


def _plain(raw):
    raw = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', raw, flags=re.I | re.S)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', raw)).split())


def _expected_layers(species, key):
    if species == 'dogs' and key == 'histiocytic sarcoma':
        item = BENCHMARK[key]
        return {'prognosis': item['prognosis'], 'next': item['next']}
    sources = (
        (DOG_DESCRIPTIONS, DOG_PROGNOSIS, DOG_NEXT_STEPS, DOG_TREATMENT, DOG_OWNER_FACTORS, DOG_TESTS)
        if species == 'dogs' else
        (CAT_DESCRIPTIONS, CAT_PROGNOSIS, CAT_NEXT_STEPS, CAT_TREATMENT, CAT_OWNER_FACTORS, CAT_TESTS)
    )
    names = ('description', 'prognosis', 'next', 'treatment', 'factors', 'tests')
    return dict(zip(names, (source[key] for source in sources)))


def validate_built_site(root=Path('seo/site')):
    import generate_seo as generated

    required = (
        'What does the prognosis look like?', 'What matters next', 'Where are you now?',
        'If you are waiting for oncology', 'Questions to ask your oncologist',
        'How it is usually treated', 'What can affect treatment choices',
        'How the diagnosis may appear in the record', 'Changes to watch for at home',
    )
    generic_questions = GENERIC_QUESTIONS - {
        'Could treatment we start now affect clinical-trial eligibility later?'
    }
    literature_review_phrases = ('six-cat series', 'median survival was', 'range of 1 to', 'small published group')
    checked = 0
    # Only the reviewed North American cancer-page family is published. Useful
    # international institutions remain available through the center directory.
    for region in ('north-america',):
        for species in ('dogs', 'cats'):
            other_species = 'cats' if species == 'dogs' else 'dogs'
            for key in sorted(CANONICAL):
                page = root / region / species / generated.slugify(key) / 'index.html'
                assert page.exists(), f'missing built page: {page}'
                raw = page.read_text(encoding='utf-8', errors='strict')
                text = _plain(raw)
                assert 'class="disease owner-guide"' in raw, f'missing owner guide: {page}'
                for marker in required:
                    assert marker in text, f'{page}: missing {marker}'
                expected_layers = _expected_layers(species, key)
                if 'tests' in expected_layers:
                    assert 'Tests that may matter' in text, f'{page}: missing Tests that may matter'
                else:
                    assert 'Tests that may matter' not in text, f'{page}: empty test section should be omitted'
                for expected in expected_layers.values():
                    assert ' '.join(expected.split()) in text, f'{page}: owner-friendly layer was overridden'
                for question in generic_questions:
                    assert question not in text, f'{page}: legacy generic question survived'
                for phrase in literature_review_phrases:
                    assert phrase not in text.lower(), f'{page}: literature-review phrasing survived: {phrase}'
                assert not re.search(r'<(?:p|li|summary)\b[^>]*>\s*</(?:p|li|summary)>', raw, re.I), f'{page}: empty block'
                paragraphs = [' '.join(html.unescape(x).split()) for x in re.findall(r'<p\b[^>]*>(.*?)</p>', raw, re.I | re.S)]
                for first, second in zip(paragraphs, paragraphs[1:]):
                    assert not first or first != second, f'{page}: consecutive duplicate paragraph'

                # A species page must not contain a different counterpart layer verbatim.
                other_layers = _expected_layers(other_species, key)
                for name in expected_layers.keys() & other_layers.keys():
                    ours, theirs = expected_layers[name], other_layers[name]
                    if ours != theirs:
                        assert ' '.join(theirs.split()) not in text, f'{page}: {other_species} content contamination'

                cards = re.findall(r'<article class="card"><h3>(.*?)</h3>', raw, re.S)
                count = re.search(r'<p class="option-count">(\d+) options? currently in our catalog\.</p>', raw)
                zero = 'No active listings in our catalog right now.' in raw
                if cards:
                    assert count and int(count.group(1)) == len(cards), f'{page}: trial card count mismatch'
                    assert not zero, f'{page}: cards and empty state both shown'
                else:
                    assert not count and zero, f'{page}: empty trial state mismatch'
                checked += 1
    assert checked == 44, f'expected 44 built pages, checked {checked}'
    return checked


def validate():
    _validate_depth('dog', DOG_DEPTH)
    _validate_depth('cat', CAT_DEPTH)
    _validate_factors('dog', DOG_FACTORS)
    _validate_factors('cat', CAT_FACTORS)
    dog_branches = set(ADDITIONAL_BRANCHES) | {'histiocytic sarcoma'}
    assert dog_branches == CANONICAL, f'dog branch coverage mismatch: missing={sorted(CANONICAL-dog_branches)}'
    assert set(FELINE_BRANCHES) == CANONICAL, f'cat branch coverage mismatch: missing={sorted(CANONICAL-set(FELINE_BRANCHES))}'
    _validate_owner_layers()
    return True


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path, help='also validate a completed candidate build')
    args = parser.parse_args()
    validate()
    print('CANCER_DEPTH_VALIDATION_OK', len(CANONICAL), 'diagnoses x 2 species')
    if args.site:
        print('CANCER_PAGE_SEMANTIC_BUILD_OK', validate_built_site(args.site), 'generated pages')
