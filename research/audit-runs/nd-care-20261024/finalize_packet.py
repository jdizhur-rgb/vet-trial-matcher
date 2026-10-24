"""Seal field deltas and recovered request metadata; page bodies remain scratch-only."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
RUN=BASE.name
def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
before=read(ROOT.parent/'nd-baseline-before.json')
manifest={'run_id':RUN,'collections':{}}
for path,key in [('data/oncology_centers.json','centers'),('data/oncology_centers_supplemental.json','centers'),('data/oncology_care_source_inventory.json','sources')]:
 old=before[path][key]; now=read(ROOT/path)[key]; ik='id' if key=='sources' else 'source_id'
 assert [r for r in old if not r.get(ik)]==[r for r in now if not r.get(ik)]
 om={r[ik]:r for r in old if r.get(ik)}; nm={r[ik]:r for r in now if r.get(ik)}
 assert set(om)<=set(nm)
 changes=[dict(id=k,before=om.get(k),after_sha256=sha(v)) for k,v in nm.items() if om.get(k)!=v]
 manifest['collections'][path]=dict(key=ik,before_count=len(old),after_count=len(now),changes=changes)
write(BASE/'baseline-projection.json',manifest)
d=read(BASE/'dispositions.json')
for r in d['reviewed_without_new_public_card']:
 if r['name']=='Devils Lake Animal Clinic':r['url']='https://www.dlanimalclinic.com/our-services.html'
 if r['name']=='Valley City Veterinary Hospital':r['url']='https://valleycityvet.com/'
 if r['name'].startswith('West River'):
  r['url']='https://www.westrivervet.com/services.html'
  r['outcome']='Exact services page HTTP403 through native and Web requests planned in the same batch; no requests after restriction observed. Local cancer treatment remains unknown.'
write(BASE/'dispositions.json',d)
web=read(ROOT.parent/'nd-web-all.json'); receipts=[]
for group,v in web.items():
 if not isinstance(v,dict):continue
 for c in v.get('content',[]):
  for b in c.get('text','').split('--------------------------------------------------------------------------------'):
   ref=re.search(r'【([^】]+)】',b); url=re.search(r'\((https?://[^\n]+)\)\n',b)
   if not url:continue
   source='Source: ' in b
   receipts.append(dict(group=group,reference=ref.group(1) if ref else None,url=url.group(1),title=b.strip().split('\n')[0],date='2026-10-24',precision='date_only',method='Web source read' if source else 'Web search result',result='explicit_http403' if re.search(r'403[: ]+Forbidden',b) else 'security_challenge' if 'One moment, please' in b else 'tool_returned',primary_review_not_implied=not source))
for filename in ['nd-native1.json','nd-native2.json','nd-native3.json']:
 for r in read(ROOT.parent/filename):receipts.append({k:v for k,v in r.items() if k not in ['text','links']})
write(BASE/'request-receipts.json',dict(run_id=RUN,note='Recovered actual source locators and native receipts. Repeated visits retained. A search-result locator does not establish a primary review; Web has date-only precision. No copied page bodies.',attempts=receipts))
write(BASE/'queries.json',dict(run_id=RUN,recovered_query_groups={k:v for k,v in web.items() if k.startswith('ndq')},additional_exact_queries=['veterinary chemotherapy oncology North Dakota Harvey Garrison Lisbon Wahpeton','veterinary tumor removal cancer surgery North Dakota New Town Bowman Hettinger','"Knife River Veterinary" veterinarian doctor','veterinary oncologist North Dakota chemotherapy Bismarck Minot','veterinary chemotherapy North Dakota clinic -site:catvetfinder.com -site:yellowpages.com','veterinary tumor removal Sheridan Harvey Garrison North Dakota','veterinary oncology cancer treatment Williston Minot Bismarck'],limitation='Some earlier query request strings were not separately retained; source result locators remain available. Not a statewide census.'))
restr=[]
for r in receipts:
 if r.get('status')==403 or r.get('result') in ['explicit_http403','security_challenge']:
  restr.append(dict(url=r['url'],observed_date='2026-10-24',status=r.get('status',r.get('result')),scope='Exact route including www/trailing-slash aliases; no retry/bypass. Not closure or absent service.',origin=f'research/audit-runs/{RUN}/request-receipts.json'))
for url in ['https://cassvetservice.com/about-us/team/','https://cassvetservice.com/careers/','https://pinkertonanimalhospital.com/','https://heartriver.net/services/surgical-laser/']:
 if not any(r['url']==url for r in restr):restr.append(dict(url=url,observed_date='2026-10-24',status='security_challenge' if 'surgical-laser' in url else 403,scope='Exact observed route; no retry or bypass. Not closure or absent service.',origin=f'research/audit-runs/{RUN}/request-receipts.json'))
write(BASE/'access-restrictions.json',dict(run_id=RUN,restrictions=restr,parallel_transport_note='Some native/Web requests were scheduled before either response was inspected; no later retry after observed explicit403/challenge. Earlier successful Web reads precede later native403 for Petcetera and Grand Valley.'))
p=ROOT/'research/oncology-care-queue/access-restriction-index.json'; idx=read(p);idx['north_dakota_exact_routes_20261024']=restr;write(p,idx)
p=ROOT/'research/oncology-care-queue/territories.json';q=read(p);nd=next(r for r in q['territories'] if r['territory']=='ND');nd.update(status='dense_primary_candidate_pass_complete_state_discovery_partial',completed=False,last_run=RUN,result_reference=f'research/audit-runs/{RUN}/result.json',remaining=['Four named discovery-only clinics need current owned primary sources; retain candidate-specific access/service questions in dispositions.json.','Continue systematic rural locality screening; secondary directories are not a complete current census.'],remaining_leads=d['discovery_only_unfinished']);write(p,q)
write(BASE/'result.json',dict(run_id=RUN,territory='ND',baseline_sha='57f60022bdcad97c8ab5a1d580fb2de42376f28e',status='VERIFIED_PACKAGE_PENDING_BUILD_AND_PUBLICATION',single_executor=True,new_confirmed_physical=12,new_network_contacts=1,new_physical_surgery_locations=8,new_limited_local_care_locations=4,new_chemotherapy_services_existing=1,new_specialist_oncologists=0,before_ND_physical=3,after_ND_physical=15,after_ND_network_contacts=1,red_river_accepting_new_oncology_patients=False,territory_complete=False,reviewed_nonpublication_candidate_groups=len(d['reviewed_without_new_public_card']),own_remaining=d['discovery_only_unfinished'],verification_dates=dict(inventory_rows_reviewed=16,precision='date_only',date='2026-10-24',remote_verified=False),publication='pending',limitations=['No new board-certified oncology service established.','No route-by-route driving times calculated; three-hour gaps are not assigned to specific origins.','Dense candidate review, not exhaustive statewide census.']))
print('Sealed field deltas, source locators, restrictions and unfinished frontier.')
