import json
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path.cwd()
RUN=Path(__file__).resolve().parent
now=datetime.now(timezone.utc).isoformat()
baseline=json.loads((RUN/'run.json').read_text())['baseline_sha']
def read(p):return json.loads((ROOT/p).read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
centers = read('data/oncology_centers.json')['centers']
inventory = read('data/oncology_care_source_inventory.json')['sources']
states = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR'.split()
coverage = []
for state in states:
    rows = [c for c in centers if c.get('country') == 'USA' and c.get('region') == state]
    mobile = [c for c in rows if c.get('location_type') == 'mobile']
    physical = [c for c in rows if c not in mobile]
    limited = [c for c in physical if c.get('available_for_care') is False or c.get('availability_status') == 'unconfirmed' or 'closed' in str(c.get('operating_status', '')).lower() or 'closed' in str(c.get('availability_status', '')).lower()]
    usable = [c for c in physical if c not in limited]
    modalities = ['Chemotherapy', 'Radiation therapy', 'Radiation oncology', 'Surgical oncology', 'Surgery', 'ECT', 'Immunotherapy', 'Targeted therapy', 'ONCEPT']
    coverage.append({'territory': state, 'listed_address_records': len(physical), 'not_flagged_closed_or_unconfirmed': len(usable), 'explicit_active_status': sum(c.get('operating_status') == 'active' for c in usable), 'operation_status_not_explicit': sum(c.get('operating_status') != 'active' for c in usable), 'limited_or_operation_unconfirmed': [c['name'] for c in limited], 'city_distribution': dict(Counter(c.get('city', '').casefold() for c in usable)), 'catalog_confirmed_service_tags': {m: sum(m in c.get('services', []) for c in usable) for m in modalities}, 'without_specific_treatment_tag': sum(not set(modalities).intersection(c.get('services', [])) for c in usable), 'mobile_service_records': [{'name': c['name'], 'source_id': c.get('source_id'), 'service_area': c.get('service_area'), 'services': c.get('services')} for c in mobile], 'visiting_or_remote_supported_records': [{'name': c['name'], 'care_delivery': c.get('care_delivery'), 'availability_note': c.get('availability_note')} for c in usable if any(t in str([c.get('care_delivery'),c.get('availability_note'),c.get('access_note')]).lower() for t in ['visiting','remote','monthly','partner'])], 'geographic_coverage_complete': False})
write(RUN/'us-coverage-baseline.json', {'baseline_sha':baseline, 'computed_at':now, 'method':'Complete generated care catalog; counts reflect saved tags, not fresh source verification. Unknown service/operation remains unknown; Surgery is retained legacy label, not a new certification assertion.', 'states':coverage})
