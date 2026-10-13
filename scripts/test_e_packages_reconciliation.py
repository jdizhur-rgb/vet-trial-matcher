#!/usr/bin/env python3
"""Guard branch scope, stale imports and explicit unknown states after E audits."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from generate_oncology_center_finder import card

rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
byid = {r.get('source_id'): r for r in rows}
run = ROOT / 'research/audit-runs/e-packages-publish-20261012'
review = json.loads((run / 'integration.json').read_text())
assigned = {r['source_id'] for r in review['source_reviews']}
inventory = json.loads((ROOT / 'data/oncology_care_source_inventory.json').read_text())['sources']
assert len(assigned) == 127
assert len({r['id'] for r in inventory}) == len(inventory)
assert all(r['last_review_run_id'] == run.name for r in inventory if r['id'] in assigned)

tmc = byid['animal-cancer-and-referral-center']
assert tmc['city'] == 'Houston' and tmc['postal_code'] == '77030'
assert tmc['services'] == ['Medical oncology'], tmc['services']
assert 'Brittanie Partridge' in json.dumps(tmc['oncology_clinicians'])
assert 'Caitlin' not in json.dumps(tmc['clinician_review'])
assert byid['woodlands-animal-cancer-and-referral-center']['city'] == 'Spring'
assert 'partner-veterinary-emergency-specialty-center' not in byid
assert byid['partner-veterinary-emergency-and-specialty-center']['city'] == 'Frederick'

sd = byid['veterinary-emergency-specialty-hospital-south-deerfield']
ws = byid['veterinary-emergency-specialty-hospital-west-springfield']
assert sd['street'] == '141 Greenfield Road' and sd['services'] == []
assert ws['street'] == '134 Capital Drive, Suite A' and 'Chemotherapy' in ws['services']
assert byid['veritas-veterinary-partners']['name'] == 'Wheat Ridge Animal Hospital'
assert byid['vmc']['name'] == 'Veterinary Medical Center of Central New York'
assert byid['veterinary-referral-associates']['postal_code'] == '20877'
assert byid['wisconsin-veterinary-referral-center-waukesha']['postal_code'] == '53188'
assert 'Radiation oncology' not in byid['virginia-veterinary-centers']['services']

mobile = byid['veterinary-cancer-services']
assert mobile['location_type'] == 'mobile' and not mobile['street'] and not mobile['postal_code']
assert mobile['latitude'] is None and mobile['longitude'] is None
assert 'data-lat=""' in card(mobile)
assert not any('Carnation' in r['street'] for r in rows if r['name'] == mobile['name'])
for r in rows:
    if r.get('coordinates_unknown'):
        assert r['latitude'] is None and r['longitude'] is None
        assert r.get('location_type') != 'mobile' and r['street'] and r.get('coordinate_source')
        assert 'data-lat=""' in card(r)
    if not r['services']:
        assert r['services_confirmation_status'] == 'unconfirmed'

assert byid['caldwell-mill-animal-clinic']['services'] == ['Local oncology care']
concord = byid['one-cancer-care-for-pets-concord']
assert 'Radiation therapy' in concord['services'] and 'Chemotherapy' not in concord['services']
north = byid['one-cancer-care-for-pets-north-shore-veterinary-hospital']
assert 'Chemotherapy' in north['services'] and 'Radiation therapy' not in north['services']
identities = [(r['country'], r['region'], re.sub(r'\W', '', r['city']).casefold(),
               re.sub(r'\W', '', r['street']).casefold()) for r in rows]
assert len(identities) == len(set(identities))
print('E_PACKAGES_REGRESSION_OK 127 reviewed identities; branch scope, stale imports, mobile and explicit unknown states')
