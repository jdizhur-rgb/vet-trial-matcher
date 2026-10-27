"""Cross-check all browser disease gates with Python and generated-page logic."""
import json
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from matcher_taxonomy import FAMILIES, diagnosis_match, protocol_screening, universal_limits_pass

rows = json.loads((ROOT / 'data/trials_base.json').read_text())
by_id = {t['id']: t for t in rows}
matrix = json.loads(subprocess.check_output(['node', 'scripts/test_matcher_selection.js', '--matrix'], cwd=ROOT, text=True))
checks = 0
for entry in matrix:
    t = by_id[entry['id']]
    for species in ('Dog', 'Cat'):
        expected = [c for c in FAMILIES if diagnosis_match(t, c, species)[0]]
        assert expected == entry['diagnoses'][species], (t['id'], species)
        checks += len(FAMILIES)

# Criteria without an owner form answer must remain visible screening items.
for group, key in [('requires', 'anesthesia_candidate'), ('excludes', 'coagulation_disorder')]:
    excluded, unknown = protocol_screening({group: {key: True}}, {})
    assert not excluded and unknown
assert protocol_screening({'requires': {'appendicular_location': True}}, {'osa_location': 'Axial — skull, spine, rib, or pelvis'})[0]
assert protocol_screening({'requires': {'planned_surgical_resection': True}}, {'prefs': {'Chemotherapy'}})[0]
# Primary CAALM and VROC brochures use strict bounds, unlike inclusive limits.
caalm = by_id['ucd-pdl1-metastatic']['requires']
for kg, accepted in [(14.9, False), (15, False), (15.1, True), (35.9, True), (36, False), (36.1, False)]:
    assert universal_limits_pass(caalm, {'weight_known': True, 'weight_lb': kg * 2.2046226218}) == accepted
assert universal_limits_pass(caalm, {'weight_known': False})
assert not universal_limits_pass(by_id['utsw-vroc-compassionate-advanced-unresectable']['requires'], {'weight_known': True, 'weight_lb': 2.5 * 2.2046226218})
assert not universal_limits_pass(by_id['ucd-oral-margin']['requires'], {'age_known': True, 'age': 1})
assert universal_limits_pass({'min_weight_kg': 15, 'max_weight_kg': 36}, {'weight_known': True, 'weight_lb': 15 * 2.2046226218})
# Vaxcell's approved mammary indication is postoperative adjuvant use as well
# as use alongside planned surgery. A completed mastectomy is not another
# future operation; unknown history remains a screening question.
vax = by_id['korea-vaxleukin15-mammary-2026']
for surgery, prefs, expected_excluded, needs_screening in [
    ('Yes', {'Immunotherapy'}, False, False),
    ('No', {'Immunotherapy'}, True, False),
    ("I don't know", {'Immunotherapy'}, False, True),
    ('No', {'Surgery', 'Immunotherapy'}, False, True),
]:
    excluded, unknown = protocol_screening(vax, {'cancer': 'Mammary carcinoma', 'surgery': surgery, 'prefs': prefs})
    assert excluded == expected_excluded, (surgery, prefs, excluded)
    assert bool(unknown) == needs_screening, (surgery, prefs, unknown)
assert not protocol_screening(vax, {'cancer': 'B-cell lymphoma', 'surgery': 'No', 'prefs': {'Chemotherapy', 'Immunotherapy'}})[0]
assert protocol_screening(vax, {'cancer': 'T-cell lymphoma', 'prefs': {'Immunotherapy'}})[0]
# Exercise the real legacy preference classifier without executing Streamlit.
module = ast.parse((ROOT / 'pages/1_Clinical_Trial_Finder.py').read_text())
fn = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'trial_modalities')
namespace = {}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<legacy modalities>', 'exec'), namespace)
assert 'Immunotherapy' in namespace['trial_modalities'](vax)
medvet = by_id['medvet-egfr-her2-vaccine-2026']
for cancer, location, expected in [
    ('Osteosarcoma', 'Appendicular — limb bone', False),
    ('Osteosarcoma', 'Axial — skull, spine, rib, or pelvis', True),
    ('Urothelial carcinoma', "I don't know", True),
]:
    assert protocol_screening(medvet, {'cancer': cancer, 'osa_location': location, 'diagnosis_status': 'Suspected / not confirmed'})[0] == expected
print(f'MATCHER_SELECTION_PARITY_OK public={len(matrix)} disease_checks={checks}')

# Source-derived Tufts cohort cases exercise the shared legacy screening path.
for case in next(r for r in json.loads((ROOT / 'data/protocol_selection_cases.json').read_text())['reviews'] if r['trial_id'] == 'tufts-osa-actionable-targets-2026')['cases'][3:]:
    patient = {**case['patient'], 'prefs': set(case['patient'].get('prefs', ['Surgery', 'Targeted therapy']))}
    excluded, _ = protocol_screening(by_id['tufts-osa-actionable-targets-2026'], patient)
    assert excluded == (case['expected'] == 'exclude'), case['name']
print('TUFTS_OSA_COHORT_PARITY_OK cases=8')

# Primary-site and lineage answers must affect the real shared Python gate.
for trial_id in ['uf-hsa-vaccine', 'tufts-hsa-liquid', 'ethos-epush-hsa', 'au-melbourne-hsa-autologous-vaccine-multicenter']:
    trial = by_id[trial_id]
    assert protocol_screening(trial, {'hsa_site': 'Heart / right atrium', 'prefs': {'Surgery', 'Chemotherapy'}})[0]
    assert not protocol_screening(trial, {'hsa_site': "I don't know", 'prefs': {'Surgery', 'Chemotherapy'}})[0]
nihon = by_id['jp-nihon-proteasome-inhibitor-b-cell-tumors']
petcura = by_id['china-petcura-personalized-mrna-iit-2026']
for trial in [nihon, petcura]:
    assert protocol_screening(trial, {'cancer': 'Lymphoma — other', 'lymphoma_type': 'T-cell'})[0]
assert not protocol_screening(nihon, {'cancer': 'Multiple myeloma / plasma cell cancer', 'lymphoma_type': 'T-cell'})[0]
assert not protocol_screening(petcura, {'cancer': 'Soft tissue sarcoma', 'lymphoma_type': 'T-cell'})[0]
preop = by_id['ethos-epush-hsa']
assert protocol_screening(preop, {'surgery': 'Yes', 'prior_procedure': 'Splenectomy'})[0]
assert not protocol_screening(preop, {'surgery': 'No', 'prior_procedure': 'Splenectomy'})[0]
print('PRIMARY_SITE_LINEAGE_PHASE_PARITY_OK')
