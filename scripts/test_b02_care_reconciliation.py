#!/usr/bin/env python3
"""B02 regression: no stale locations, unsupported RT or credential promotion."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
centers = json.loads((ROOT/'data/oncology_centers.json').read_text())['centers']
inventory = json.loads((ROOT/'data/oncology_care_source_inventory.json').read_text())['sources']
def one(source_id):
    found = [c for c in centers if c.get('source_id') == source_id]
    assert len(found) == 1, (source_id, len(found))
    return found[0]

for sid in ('bluepearl-pet-hospital-raleigh',
            'bluepearl-specialty-and-emergency-hospital-jacksonville',
            'bluepearl-veterinary-specialists-grand-rapids'):
    row = one(sid)
    assert 'Chemotherapy' in row['services']
    assert not {'Radiation oncology','Radiation therapy','SRT'} & set(row['services'])
    assert row['unresolved'], sid
for sid in ('bluepearl-pet-hospital-raleigh','bluepearl-pet-hospital-sandy-springs',
            'bluepearl-pet-hospital-studio-city-los-angeles'):
    assert 'Immunotherapy' not in one(sid)['services']
rockville = one('bluepearl-pet-hospital-rockville')
assert 'Electrochemotherapy' in rockville['services']
assert 'Radiation oncology' not in rockville['services']
for sid in ('bluepearl-pet-hospital-sandy-springs',
            'bluepearl-pet-hospital-studio-city-los-angeles',
            'bluepearl-specialty-emergency-medicine-for-pets-mi',
            'bluepearl-veterinary-partners'):
    assert 'Radiation oncology' in one(sid)['services']
southfield = one('bluepearl-specialty-emergency-medicine-for-pets-mi')
assert southfield['phone'] == '248-354-6640'
assert 'Josephine Gendler — DVM, surgery resident' in southfield['clinician_review']
assert 'conflicting' not in southfield['clinician_review']

tacoma = one('bluepearl-pet-hospital-tacoma-lakewood')
assert not any('BluePearl' in c['name'] and c['street']=='5608 S Durango St' for c in centers)
assert not any(c.get('source_id')=='bluepearl-pet-hospital-tacoma' for c in centers)
assert tacoma['city']=='Lakewood' and tacoma['postal_code']=='98499'
assert {'Electrochemotherapy','Immunotherapy','Targeted therapy','Stelfonta'} <= set(tacoma['services'])
virginia = one('bluepearl-virginia')
assert virginia['street']=='364 S Independence Blvd.' and virginia['city']=='Virginia Beach'
assert virginia['postal_code']=='23452' and virginia['phone']=='757-499-5463'
assert (virginia['latitude'],virginia['longitude'])==(36.8348,-76.0961)
assert not any(c['name']=='BluePearl Virginia' and c['city']=='Chesapeake' for c in centers)
ids=[s['id'] for s in inventory]
assert len(ids)==len(set(ids))
network=next(s for s in inventory if s['id']=='network-bluepearl')
assert network['source_type']=='network_master'
assert not any(c.get('source_id')=='network-bluepearl' for c in centers)
assert next(s for s in inventory if s['id']=='bluepearl-pet-hospital-tacoma')['canonical_source_id']=='bluepearl-pet-hospital-tacoma-lakewood'
page=(ROOT/'seo/static/matcher/centers/index.html').read_text()
assert '5608 S Durango St' not in page
assert '364 S Independence Blvd.' in page
print('B02_CARE_REGRESSION_OK branch modalities, credentials, aliases, relocation coordinates, network scope')
