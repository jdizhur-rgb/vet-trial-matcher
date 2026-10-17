#!/usr/bin/env python3
"""Network service evidence must not become branch locations or proximity pins."""
import copy
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_oncology_center_catalog import center_match
from seo.generate_oncology_center_finder import card
rows=json.loads((ROOT/'data/oncology_centers.json').read_text())['centers']
network=[r for r in rows if r.get('source_id')=='de-filu-network-germany']
assert len(network)==1
r=network[0]
assert r['location_type']=='network' and r['service_scope']=='network'
assert r['services']==['Surgery'] and r['branch_availability']=='confirm_before_booking'
assert all(not r.get(k) for k in ('street','city','postal_code','phone'))
assert r['latitude'] is None and r['longitude'] is None
assert r['email']=='service@filu.vet' and r['booking_url']=='https://my.filu.vet/book'
assert len([x for x in rows if 'filu' in x.get('source_id','')])==1
branch=copy.deepcopy(r);branch.update(location_type='physical',source_id='test-filu-branch',street='A clinic street')
assert not center_match(branch,r) and not center_match(r,branch)
assert center_match(r,copy.deepcopy(r))
other=copy.deepcopy(r);other['source_id']='test-other-network'
assert not center_match(r,other)
other=copy.deepcopy(r);other['country']='USA'
assert not center_match(r,other)
markup=card(r)
for text in ('Network contact · Germany','Confirm which branch provides it','Find a branch','Book through the network','mailto:service@filu.vet','data-location-type="network"','data-filters="cancer surgery"'):
 assert text in markup,text
assert 'Maria-Theresia' not in markup and '☎' not in markup
# A malformed coordinate must still be rejected by the fixed-location predicate.
assert "c.dataset.locationType!=='network'" in (ROOT/'seo/static/matcher/centers/index.html').read_text()
print('NETWORK_CARE_OK one network route; no branch clones, office address, phone invention or physical identity merge')
