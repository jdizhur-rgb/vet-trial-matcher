"""Cross-check all browser disease gates with Python and generated-page logic."""
import json
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
print(f'MATCHER_SELECTION_PARITY_OK public={len(matrix)} disease_checks={checks}')
