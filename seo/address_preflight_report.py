#!/usr/bin/env python3
import json
import generate_seo_strict as s

rows=s.g.load_effective()
report=s.preflight(rows)
print('MISSING_CENTER_ADDRESSES='+json.dumps(report['missing_center_addresses'],ensure_ascii=False,sort_keys=True))
print('MISSING_SITE_ADDRESSES='+json.dumps(report['missing_participating_site_addresses'],ensure_ascii=False,sort_keys=True))
