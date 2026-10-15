#!/usr/bin/env python3
"""A02 regression: real clinic identities, access limits and coordinate moves."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
centers = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
def one(name):
    found = [c for c in centers if c['name'] == name]
    assert len(found) == 1, (name, len(found))
    return found[0]

for retired in ('North Coast Veterinary Specialist', 'Platt Park Veterinary Hospital',
                'Northwest Veterinary Oncology Services'):
    assert not any(c['name'] == retired for c in centers), retired
assert 'Chemotherapy' not in one('Mount Anthony Veterinary Hospital')['services']
voc = one('Veterinary Oncology Center')
assert voc['street'] == '636 Shattuck Avenue S' and voc['phone'] == '425-242-7005'
assert not {'ECT', 'Surgical oncology', 'Radiation therapy'} & set(voc['services'])
assert 'Oral chemotherapy only' in voc['availability_note']
hosts = [c for c in centers if c.get('source_id') == 'northwest-veterinary-oncology-services']
assert {c['city'] for c in hosts} == {'Gig Harbor', 'Puyallup'}
assert all(c['latitude'] is not None and c['street'] != '25228 Baker St' for c in hosts)
assert all('ECT' not in c['services'] for c in hosts)
pompano = one('Pompano Veterinary Oncology')
assert pompano['location_type'] == 'mobile'
assert pompano['latitude'] is None and pompano['longitude'] is None
assert not pompano['street'] and not pompano['postal_code']
assert 'Radiation therapy' in pompano['services']
assert 'superficial SRT-100' in pompano['availability_note']
prism = one('Prism Integrative Veterinary Health')
assert prism['street'] == '33 Newman Springs Road'
assert (prism['latitude'], prism['longitude']) == (40.2926, -74.0734)
assert 'Chemotherapy' not in prism['services']
assert one('Orchard Park Veterinary Medical Center')['street'] == '3930 North Buffalo Street'
assert one('Portland Veterinary Emergency and Specialty Care')['oncologist_count'] == 3
rise = one('RISE Pet Health')
assert rise['oncologist_count'] == 2 and {'Chemotherapy', 'ONCEPT'} <= set(rise['services'])
hauss = one('Pacific CARE Pet Emergency + Specialty')['oncologists'][0]
assert 'board certification not stated' in hauss and 'DACVIM' not in hauss
assert 'which branch' in one('Parkersburg Veterinary Hospital')['availability_note']
assert not any(c['name'] == 'Parkersburg Veterinary Hospital — Vienna' for c in centers)
assert one('Red River Animal Emergency Hospital & Referral Center')['accepting_new_patients'] is False
for name in ('Pet Cancer Group', 'Pet Cancer Group — Broward'):
    c = one(name)
    assert {'Chemotherapy', 'ECT', 'Immunotherapy', 'Targeted therapy'} <= set(c['services'])
    assert 'owner decision' in c['service_scope_provenance']

# Distinct practice/location identity remains distinct after builder dedupe.
keys = [(c['name'].casefold(), c['city'].casefold(), c['street'].casefold()) for c in centers]
assert len(keys) == len(set(keys))
tree = ast.parse((ROOT / 'seo/oncology_teleconsultations.py').read_text())
rows = next(ast.literal_eval(node.value) for node in tree.body
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROWS' for t in node.targets))
nw = [r for r in rows if r[2] == 'Northwest Veterinary Oncology Services']
sarbu = [r for r in rows if r[2] == 'Veterinary Oncology Center / Hope4Pets']
assert len(nw) == len(sarbu) == 1 and nw[0][5].startswith('Owner') and sarbu[0][5] == 'Vet only'
assert len(rows) == 61
assert not any(r[2] == 'Dr Sarah Boston Telemedicine' for r in rows)
page = (ROOT / 'seo/site/matcher/centers/index.html').read_text()
assert 'North Coast Veterinary Specialist' not in page and 'Platt Park Veterinary Hospital' not in page
assert '636 Shattuck Avenue S' in page and 'Old Growth' in page
print('A02_CARE_REGRESSION_OK identities, retired/watchlist exclusion, local modality limits, mobile coordinates, doctor credentials, remote audiences')
