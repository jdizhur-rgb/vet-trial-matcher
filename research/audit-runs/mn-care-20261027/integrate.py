import copy,hashlib,json,pathlib,re,urllib.parse
from prepare_records import ROOT,OUT,RUN,DATE,read,write,digest
paths=['data/oncology_centers.json','data/oncology_centers_supplemental.json','data/oncology_care_source_inventory.json']
baseline={p:read(p) for p in paths}
assert not (OUT/'baseline-snapshot.json').exists(), 'Do not overwrite a prior integration baseline'
write('research/audit-runs/'+RUN+'/baseline-snapshot.json',baseline)
supp=baseline[paths[1]]
new=read('research/audit-runs/'+RUN+'/proposed-records.json')
for r in new:
 if r['source_id']=='mn-rum-river-veterinary-clinic':r['supporting_urls'].append('https://rumrivervet.com/contact/')
supp['centers']+=copy.deepcopy(new)
updated=[]
ids={'Allied Veterinary Emergency & Referral':'allied-veterinary-emergency-referral','Animal Emergency & Referral Center of Minnesota – Oakdale':'animal-emergency-referral-center-of-minnesota-oakdale','VCA Cascade Animal Medical Center & Inn':'vca-cascade-animal-medical-center-inn'}
for r in supp['centers']:
 if r in new or r.get('country')!='USA' or r.get('region')!='MN':continue
 r['source_id']=r.get('source_id') or ids[r['name']]
 r.update(last_verified=DATE,audit_run_id=RUN,review_reference='research/audit-runs/'+RUN+'/evidence.json')
 if r['source_id']=='animal-emergency-referral-center-of-minnesota-oakdale':
  r.update(oncologist_count=2,oncologists=['Briana Keller — DVM, DACVIM (Oncology), cHPV','Sam Keepman — DVM, MPH, DACVIM (Oncology)'],supporting_urls=['https://www.aercmn.com/staff/'],availability_note='Oncology appointments and chemotherapy are offered at Oakdale. The current team lists Briana Keller and Sam Keepman. The separate St. Paul emergency branch is not an oncology appointment location; radiation is referred externally.')
 if r['source_id']=='allied-veterinary-emergency-referral':
  r.update(oncologist_count=1,oncologists=['Amber Wolf-Ringwall — DVM, PhD, DACVIM (Oncology)'],supporting_urls=['https://www.alliedervet.com/team/dr-wolf-ringwall/','https://www.alliedervet.com/locations/brooklyn-park/'],availability_note='The current oncology service appointment link directs to Brooklyn Park. Call 763-463-9800 to arrange oncology care. A network blog mentions chemotherapy access at Eden Prairie, but the assigned oncology appointment location there remains to be confirmed; other network hospitals are not separate confirmed oncology sites.')
 if r['source_id']=='north-shore-veterinary-hospital':r['verification_url']='https://nsvh.com/oncology-services/'
 if r['source_id']=='university-of-minnesota':
  r['services']=list(dict.fromkeys(r['services']+['Surgical oncology']))
  r['review_questions']=['Confirm the clinician assigned to radiation appointments and current scheduling when booking.']
 if r['source_id']=='vca-cascade-animal-medical-center-inn':r['supporting_urls']=['https://vcahospitals.com/cascade/services/advanced-care/chemotherapy','https://vcahospitals.com/cascade/team','https://vcahospitals.com/cascade/contact-us']
 updated.append(copy.deepcopy(r))
assert len(updated)==6,len(updated)
write(paths[1],supp)
pages=[json.loads(f.read_text()) for f in (OUT/'pages').glob('*.json')]
attempts=[{k:v for k,v in r.items() if k not in ['text','links']} for r in pages]
write('research/audit-runs/'+RUN+'/request-receipts.json',attempts)
inventory=baseline[paths[2]]
existing={r['id']:r for r in inventory['sources']}
evidence=[]
for r in new+updated:
 sid=r['source_id'];src=existing.get(sid)
 if not src:
  src={'id':sid,'name':r['name'],'source_type':'center','required_cadence':'weekly'};inventory['sources'].append(src)
 before=copy.deepcopy(existing.get(sid))
 urls=set([r['verification_url'],r['website']]+r.get('supporting_urls',[]))
 owned=[x for x in pages if x['url'] in urls]
 good=[x for x in owned if x.get('result')=='readable']
 src.update(master_url=r['verification_url'],supporting_urls=r.get('supporting_urls',[]),last_checked=DATE,last_result='success',working_url=r['verification_url'],content_sufficient=True,last_run_id=RUN,last_review_run_id=RUN,last_reviewed_at=DATE,last_review_note=r.get('availability_note','Existing service/contact/clinician facts reviewed.'),review_reference='research/audit-runs/'+RUN+'/evidence.json',needs_recheck=False,review_questions=[])
 if good:
  chosen=next((x for x in good if x['url']==r['verification_url']),good[0]);src.update(last_checked_at=chosen['attempted_at'],http_status=200,fingerprint_sha256=hashlib.sha256(chosen['text'].encode()).hexdigest(),fingerprint_method='sha256-extracted-visible-text-mn');src.pop('successful_review_date_precision',None)
 else:
  src.pop('last_checked_at',None);src.pop('http_status',None);src.update(fingerprint_sha256=digest({'url':r['verification_url'],'services':r['services'],'contact':[r['street'],r['city'],r['phone']],'clinicians':r.get('care_clinicians',r.get('oncologists',[]))}),fingerprint_method='sha256-reviewed-facts-web-date-only',successful_review_date_precision='date_only')
 evidence.append({'source_id':sid,'name':r['name'],'decision':'new_verified_listing' if r in new else 'existing_reconciliation','review_date':DATE,'service_url':r['verification_url'],'services':r['services'],'clinicians':r.get('care_clinicians',r.get('oncologists',r.get('clinician_review'))),'contact':{k:r.get(k) for k in ['street','city','postal_code','phone','email']},'location_type':r.get('location_type','physical'),'source_urls':sorted(urls),'literal_scope':r.get('availability_note',r.get('service_scope_provenance','Branch service list and clinician roster reviewed; no additional treatment tags inferred.')),'native_requests':[x['key'] for x in owned],'date_precision':'actual_native_request_timestamp' if good else 'Web review date only; native failures remain separately recorded','before_source_metadata':{k:before.get(k) for k in ['last_checked','last_checked_at','last_result']} if before else None})
write(paths[2],inventory)
write('research/audit-runs/'+RUN+'/evidence.json',evidence)
write('research/audit-runs/'+RUN+'/published-records.json',new)
write('research/audit-runs/'+RUN+'/existing-updates.json',updated)
print('Integrated',len(new),'new and',len(updated),'existing supplemental rows; rebuild required')
