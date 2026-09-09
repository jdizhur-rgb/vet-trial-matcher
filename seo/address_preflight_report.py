#!/usr/bin/env python3
"""Catalog-wide address coverage guard.

Every real owner-facing center must resolve through center_directory.py. The
only allowed unresolved center labels are umbrella/research labels with no
single public patient location.
"""
import json
import generate_seo_strict as s
from center_directory import addresses_for, normalize

ALLOWED_NO_SINGLE_LOCATION = {
    normalize('Ethos Veterinary Health'),
    normalize('MedVet Clinical Studies Center'),
    normalize('Zhongnong Dongjun Laboratory'),
}

rows=s.g.load_effective()
report=s.preflight(rows)
centers={}
for r in rows:
    name=str(r.get('center') or '').strip()
    if name:
        centers.setdefault(name,str(r.get('country') or ''))

unresolved=[]
for name,country in sorted(centers.items()):
    if addresses_for(name) or s.is_composite_center(name):
        continue
    if normalize(name) in ALLOWED_NO_SINGLE_LOCATION:
        continue
    unresolved.append({'name':name,'country':country})

print('MISSING_CENTER_ADDRESSES='+json.dumps(report['missing_center_addresses'],ensure_ascii=False,sort_keys=True))
print('MISSING_SITE_ADDRESSES='+json.dumps(report['missing_participating_site_addresses'],ensure_ascii=False,sort_keys=True))
print('UNRESOLVED_PHYSICAL_CENTERS='+json.dumps(unresolved,ensure_ascii=False,sort_keys=True))
assert not report['missing_center_addresses'], report['missing_center_addresses']
assert not report['missing_participating_site_addresses'], report['missing_participating_site_addresses']
assert not unresolved, unresolved
print('ADDRESS_COVERAGE_OK')
