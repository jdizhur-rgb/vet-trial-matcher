#!/usr/bin/env python3
"""C01 regression: builder must not restore stale locations or unsupported filters."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from generate_oncology_center_finder import card

rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
review = json.loads((ROOT / 'research/audit-runs/c01-approved-20261011/review.json').read_text())
ids = set(review['assigned_source_ids']) - {'network-vca-sitemap'}
scoped = [r for r in rows if r.get('source_id') in ids]
assert len(scoped) == len(ids) == 24, (len(scoped), len(ids))
byid = {r['source_id']: r for r in scoped}

abq = byid['vca-9377c919']
assert abq['street'] == '8850 Holly Avenue NE, Suite K'
assert abq['postal_code'] == '87122' and abq['phone'] == '505-292-5353'
assert (abq['latitude'], abq['longitude']) == (35.1757504523688, -106.54533385766976)
assert not any('Montgomery' in r['street'] and r['city'] == 'Albuquerque' and r['name'].startswith('VCA') for r in rows)
assert not any(r['name'] == 'VCA' and r['city'] in {'Albuquerque', 'San Francisco'} for r in rows)
sage = byid['vca']
assert sage['name'] == 'SAGE Veterinary Centers - San Francisco'
assert len(sage['oncologists']) == 2 and 'Andres' not in ' '.join(sage['oncologists'])
assert {'Fenger', 'Trang-Hoang'} <= {word for c in sage['oncologists'] for word in re.findall(r'[A-Za-z-]+', c)}

seven = ['vca-aledo-animal-hospital', 'vca-alpine-animal-hospital',
         'vca-amherst-animal-hospital', 'vca-animal-care-clinic',
         'vca-animal-medical-center', 'vca-bath-animal-hospital',
         'vca-boonsboro-animal-hospital']
for sid in seven:
    r = byid[sid]
    assert r['services'] == ['Local oncology care'], (sid, r['services'])
    rendered = card(r)
    filters = re.search(r'data-filters="([^"]*)"', rendered)[1].split('|')
    assert 'local oncology care' in filters and 'chemotherapy' not in filters

five = ['vca-airport-irvine-animal-hospital', 'vca-amherst-animal-hospital-9fbf208f',
        'vca-animal-medical-center-of-ne-alabama', 'vca-aventura-animal-hospital-and-pet-resort',
        'vca-bering-sea-animal-hospital']
assert all('Chemotherapy' in byid[sid]['services'] for sid in five)
assert 'Chemotherapy' not in byid['vca-amherst-animal-hospital']['services']
assert 'Chemotherapy' in byid['vca-amherst-animal-hospital-9fbf208f']['services']
for sid in ['vca-advanced-veterinary-care-center', 'vca-aurora-animal-hospital', 'vca-9377c919']:
    assert 'radiation oncology' in re.search(r'data-filters="([^"]*)"', card(byid[sid]))[1].split('|')
la = byid['vca-animal-specialty-group-los-angeles']
assert {'ECT', 'Surgical oncology', 'Targeted therapy', 'Chemotherapy'} <= set(la['services'])
assert 'radiation oncology' not in re.search(r'data-filters="([^"]*)"', card(la))[1].split('|')
assert la['local_radiation_available'] is False
assert byid['vca-animal-specialty-group']['named_treatments'] == ['ONCEPT']
assert 'ONCEPT' not in byid['vca-baring-boulevard-animal-hospital']['services']
for sid in ['vca-alameda-east-veterinary-hospital', 'vca-arboretum-view-animal-hospital']:
    assert 'DACVIM' not in ' '.join(byid[sid]['oncologists'])
    assert 'board certification not stated' in byid[sid]['oncologists'][0]
assert not any(r.get('source_id') == 'network-vca-sitemap' for r in rows)
identities = [(r['country'], r['region'], r['city'].casefold(), re.sub(r'\W', '', r['street']).casefold()) for r in scoped]
assert len(identities) == len(set(identities))
print('C01_CARE_REGRESSION_OK 24 unique branches, corrected coordinates/identity, conservative filters, credentials and named treatments')
