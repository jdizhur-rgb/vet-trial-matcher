"""Cross-check all browser disease gates with Python and generated-page logic."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from matcher_taxonomy import FAMILIES, diagnosis_match, protocol_screening

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
print(f'MATCHER_SELECTION_PARITY_OK public={len(matrix)} disease_checks={checks}')
