#!/usr/bin/env python3
import json
import generate_seo_strict as s
from center_directory import addresses_for

rows=s.g.load_effective()
report=s.preflight(rows)
centers={}
for r in rows:
    name=str(r.get('center') or '').strip()
    if name:
        centers.setdefault(name,str(r.get('country') or ''))
unresolved=[]
for name,country in sorted(centers.items()):
    if not addresses_for(name) and not s.is_composite_center(name):
        unresolved.append({'name':name,'country':country})
print('MISSING_CENTER_ADDRESSES='+json.dumps(report['missing_center_addresses'],ensure_ascii=False,sort_keys=True))
print('MISSING_SITE_ADDRESSES='+json.dumps(report['missing_participating_site_addresses'],ensure_ascii=False,sort_keys=True))
print('UNRESOLVED_CENTER_DIRECTORY_ENTRIES='+json.dumps(unresolved,ensure_ascii=False,sort_keys=True))
