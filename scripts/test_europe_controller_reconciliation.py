"""Preserve the actual independently verified controller cards after assembly."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = 'europe-controller-20261016T092604-0400'
supp = json.loads((ROOT / 'data/oncology_centers_supplemental.json').read_text())['centers']
public = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
applied_ids = set()
for receipt in (ROOT / 'research/audit-runs' / RUN).glob('integration-*.json'):
    for package in json.loads(receipt.read_text())['packages']:
        applied_ids.update(c['source_id'] for c in package['applied'] if c['operation'] == 'NEW')
expected = [r for r in supp if r.get('source_id') in applied_ids]
assert {r['source_id'] for r in expected} == applied_ids
assert expected, 'Controller checkpoint missing'
for row in expected:
    matches = [r for r in public if r.get('source_id') == row['source_id']]
    assert len(matches) == 1, (row['source_id'], len(matches))
    for field in ('name', 'street', 'city', 'phone', 'services', 'latitude', 'longitude', 'coordinates_unknown'):
        assert matches[0].get(field) == row.get(field), (row['source_id'], field)
print(f'EUROPE_CONTROLLER_IDENTITIES_OK {len(expected)} independently preserved cards')
