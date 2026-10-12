#!/usr/bin/env python3
"""B01: branch identity, modality scope and current credential regression."""
import json
from pathlib import Path
from build_oncology_center_catalog import center_match
ROOT = Path(__file__).resolve().parents[1]
centers = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
ledger = json.loads((ROOT / 'research/audit-runs/B01-20261012/B01-applied_changes.json').read_text())
ids = {r['source_id'] for r in ledger['reviews']}
rows = [c for c in centers if c.get('source_id') in ids]
assert len(ids) == 25 and len(rows) == 26
by_slug = {c['website'].rstrip('/').split('/')[-1]: c for c in rows}
hospital = by_slug['malvern-pa']
radiation = by_slug['bluepearl-veterinary-cyberknife-cancer-center']
assert hospital['street'].startswith('40 ') and radiation['street'].startswith('50 ')
assert hospital['phone'] == radiation['phone']
assert not center_match(hospital, radiation) and not center_match(radiation, hospital)
assert 'Radiation therapy' not in hospital['services']
assert radiation['services'] == ['Radiation therapy']
for slug in ('midtown-nyc', 'brentwood-tn', 'cary-nc', 'vsec-levittown-pa', 'maitland-fl'):
    assert 'Radiation therapy' in by_slug[slug]['services'], slug
for slug in ('augusta-ga', 'brandon-fl', 'clearwater-fl', 'durham-nc', 'fort-myers-fl', 'nashville-tn', 'northfield-il', 'port-washington-wi'):
    assert 'Radiation therapy' not in by_slug[slug]['services'], slug
    assert 'Radiation therapy' in by_slug[slug]['unresolved_services'], slug
for slug in ('arden-hills-mn', 'auburn-hills-mi', 'fort-myers-fl', 'lafayette-co', 'northfield-il'):
    assert 'ECT' in by_slug[slug]['services'], slug
assert 'Surgery' not in by_slug['auburn-hills-mi']['services']
assert 'Surgery' in by_slug['framingham-ma']['services']
assert 'Immunotherapy' in by_slug['cary-nc']['services']
assert 'inference' in by_slug['cary-nc']['availability_note']
assert by_slug['durham-nc']['oncologist_count'] == 2
assert by_slug['vsec-levittown-pa']['oncologist_count'] == 1
assert by_slug['cary-nc']['oncologist_count'] == 3
assert not any('Goodson' in x for x in by_slug['maitland-fl']['oncologists'])
assert 'unresolved' in by_slug['maitland-fl']['availability_note']
assert by_slug['summerville-sc']['phone'] == '843-216-1331'
assert by_slug['northfield-il']['phone'] == '847-564-5775'
assert all(c['verification_evidence'] and c['location_type'] == 'physical' for c in rows)
print('B01_CARE_REGRESSION_OK 25 sources, 26 sites, Malvern separation, branch modalities, credentials and contacts')
