"""Field-scoped accepted Massachusetts records, against fresh main."""
import copy,datetime as dt,hashlib,json,pathlib,re,subprocess,sys,urllib.parse
from prepare_records import ROOT,OUT,CACHE,DATE,RUN,read,write,digest
paths=['data/oncology_centers.json','data/oncology_centers_supplemental.json','data/oncology_care_source_inventory.json']
snapshot=CACHE/'integration-baseline.json'
if snapshot.exists():
 assert '--reapply-reviewed' in sys.argv,'Do not overwrite integration baseline'
 baseline=json.loads(snapshot.read_text())
 # Reapply only this run's own staged records after source QA/geocoding. Never
 # discard a concurrent record change outside the reviewed scope.
 for path in paths:
  current=read(path);field='sources' if 'inventory' in path else 'centers'
  def outside(r):
   return not (r.get('audit_run_id')==RUN or r.get('last_run_id')==RUN or (r.get('country')=='USA' and r.get('region')=='MA'))
  old=[r for r in baseline[path][field] if outside(r)]
  now=[r for r in current[field] if outside(r)]
  if 'inventory' in path:
   scope={r['id'] for r in current[field] if r.get('last_run_id')==RUN}
   old=[r for r in old if r['id'] not in scope]
  assert digest(old)==digest(now),path
else:
 baseline={p:read(p) for p in paths}
 snapshot.write_text(json.dumps(baseline,ensure_ascii=False))
 (OUT/'baseline-sha.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True))
supp=copy.deepcopy(baseline[paths[1]])
inv=copy.deepcopy(baseline[paths[2]])
proposals=read('research/audit-runs/'+RUN+'/proposed-records.json')
pages=[json.loads(f.read_text()) for f in CACHE.glob('*.json') if f.name!='integration-baseline.json']
pages=[r for r in pages if 'url' in r]
byurl={r['url']:r for r in pages}
new=[];updates=[];evidence=[]
def source_for(r):
 def host(u):return urllib.parse.urlsplit(u or '').netloc.lower().removeprefix('www.')
 hosts={host(u) for u in [r.get('website'),r.get('verification_url')]+r.get('supporting_urls',[]) if u}
 return next((s for s in inv['sources'] if s['id']==r.get('source_id')),None) or next((s for s in inv['sources'] if s['name']==r['name'] and host(s.get('master_url')) in hosts),None)
def reviewed(r,decision,prior=None):
 urls=list(dict.fromkeys([r['verification_url']]+r.get('supporting_urls',[])))
 attempts=[x for x in pages if x['url'] in urls]
 good=[x for x in attempts if x.get('result')=='readable']
 assert good,r['name']
 chosen=next((x for x in good if x['url']==r['verification_url']),good[0])
 s=source_for(r)
 if s is None:
  s={'id':r['source_id'],'name':r['name'],'source_type':'center','required_cadence':'weekly'};inv['sources'].append(s)
 before=copy.deepcopy(s)
 s.update(master_url=r['verification_url'],supporting_urls=r.get('supporting_urls',[]),last_checked=DATE,last_checked_at=chosen['attempted_at'],last_result='success',working_url=r['verification_url'],content_sufficient=True,last_run_id=RUN,last_review_run_id=RUN,last_reviewed_at=DATE,last_review_note=r['availability_note'],review_reference='research/audit-runs/'+RUN+'/evidence.json',fingerprint_sha256=hashlib.sha256(chosen.get('text','').encode()).hexdigest(),fingerprint_method='sha256-extracted-reviewed-primary-content',http_status=200)
 s.pop('successful_review_date_precision',None)
 if not r.get('review_questions'):s.update(needs_recheck=False,review_questions=[])
 evidence.append({'source_id':r['source_id'],'name':r['name'],'decision':decision,'review_date':DATE,'services':r['services'],'contact':{k:r.get(k) for k in ['street','city','postal_code','phone','email']},'location_type':r.get('location_type','physical'),'clinicians':r.get('care_clinicians',r.get('oncologists',r.get('clinician_review'))),'source_urls':urls,'request_keys':[x.get('key') for x in attempts],'scope':r['availability_note'],'before_last_verified':prior.get('last_verified') if prior else None,'before_source_metadata':{k:before.get(k) for k in ['last_checked','last_checked_at','last_result']},'actual_primary_request':chosen['attempted_at']})
for p in proposals:
 old=next((r for r in supp['centers'] if r['name']==p['name'] and r.get('country')=='USA' and r.get('region')=='MA' and r.get('postal_code')==p['postal_code']),None)
 if old:
  before=copy.deepcopy(old);s=source_for(old);p['source_id']=old.get('source_id') or (s['id'] if s else p['source_id'])
  old.update({k:v for k,v in p.items() if k not in ['services','source']});old['services']=list(dict.fromkeys(before['services']+p['services']))
  old['source']=before.get('source','')+'; Massachusetts current primary review '+DATE
  updates.append(copy.deepcopy(old));reviewed(old,'existing_branch_surgery_confirmed',before)
 else:
  supp['centers'].append(copy.deepcopy(p));new.append(copy.deepcopy(p));reviewed(p,'new_verified_listing')
held={'animal-cancer-care-specialists','integrity-veterinary-center'}
already={r['source_id'] for r in updates}
for r in supp['centers']:
 if r.get('country')!='USA' or r.get('region')!='MA' or r.get('audit_run_id')==RUN:continue
 s=source_for(r)
 sid=r.get('source_id') or (s['id'] if s else None)
 assert sid,r['name']
 if sid in held:continue
 before=copy.deepcopy(r);r['source_id']=sid
 r.update(last_verified=DATE,audit_run_id=RUN,review_reference='research/audit-runs/'+RUN+'/evidence.json')
 if sid=='mspca-angell-animal-medical-center':
  r.update(verification_url='https://www.mspca.org/veterinarycare/hospital-locations/oncology/',oncologist_count=3,oncologists=['Sarah Adrianowycz, DVM, DACVIM — medical oncology','Kristine Burgess, DVM, MS, DACVIM — medical oncology','Gretchen McLinden, DVM, DACVIM — medical oncology'],availability_note='Boston provides medical, radiation and surgical oncology. The current service roster lists three board-certified medical oncologists; surgical oncologist Megan Cray and trainees are separate. Request an appointment and confirm the assigned clinician and treatment schedule.')
 elif sid=='massachusetts-veterinary-referral-hospital':
  r.update(verification_url='https://www.massvethospital.com/services/oncology',oncologist_count=2,oncologists=['Mitchell Kaye — DVM, DACVIM (Oncology)','Katie Matthews — VMD, DACVIM (Oncology)'],availability_note='Current Woburn oncology team lists Mitchell Kaye and Katie Matthews as DACVIM oncologists, and Kirsten Andersson as DVM following her oncology residency. Board certification for Andersson is not asserted. Confirm assigned clinician, regimen and appointment; interventional radiology is not local radiation therapy.')
 elif sid=='tufts-university':
  r.update(oncologist_count=3,availability_note='Foster Hospital oncology faculty include Heather Gardner, Cheryl London and Carrie Wood, each DACVIM (Oncology), with radiation faculty and residents separately listed. Faculty listing is not a guarantee of the assigned clinician. Appointments: 508-839-5395; actual hospital entrance is 55 Willard Street, North Grafton. Confirm referral and treatment schedule.')
 elif sid=='ally-veterinary-speciality-center':
  r['services']=list(dict.fromkeys(r['services']+['Targeted therapy']));r['verification_url']='https://www.allyvetspecialist.com/services-4';r['availability_note']='The clinic currently lists chemotherapy, immunotherapy and targeted therapies at 16 Mill Street, Lincoln. Michelle Custead is the practice oncologist. Confirm the regimen, appointment and assigned clinician.'
 elif sid=='veterinary-emergency-specialty-hospital-south-deerfield':
  r.update(services=['Surgery'],services_confirmation_status='confirmed',verification_url='https://www.veshmass.com/services/surgery',availability_note='South Deerfield has a local surgery department and the current surgical service lists tumor-removal procedures. John A. Benson is listed as DVM, DACVS; Emily Pearce is practice-limited to surgery without an inferred board credential. Local medical oncology and chemotherapy remain unconfirmed; Gina Olmsted is listed at the separate West Springfield branch.',review_questions=['Confirm any local chemotherapy or visiting medical oncologist at South Deerfield.'])
  r.pop('unconfirmed_services_note',None);r['supporting_urls']=list(dict.fromkeys(r.get('supporting_urls',[])+['https://www.veshmass.com/services/surgery']))
 elif sid=='advanced-veterinary-specialty-center-of-new-england':
  r['supporting_urls']=list(dict.fromkeys(r.get('supporting_urls',[])+['https://www.avscvets.com/assets/MedicalOncology-DYOJ2Iw4.js','https://www.avscvets.com/assets/RadiationOncology-ChbLOZz2.js','https://www.avscvets.com/assets/OurDoctors-CH3HkPQO.js','https://www.avscvets.com/assets/Appointments-DLOgdMYj.js']))
  r['availability_note']='Current public service and doctor route modules confirm the Walpole oncology services. Jillian Walz is DACVIM (Oncology), DACVR (Radiation Oncology); Michele Keyerleber is DACVR (Radiation Oncology); Richard Segaloff is listed DVM. Confirm the assigned clinician and appointment.'
 elif sid=='veterinary-cancer-specialists-of-new-england':
  r['verification_url']='https://www.vcsnewengland.com/services/';r['supporting_urls']=list(dict.fromkeys(r.get('supporting_urls',[])+['https://www.vcsnewengland.com/about/','https://www.vcsnewengland.com/contact/']));r['availability_note']='Andrew H. Abbo leads the current medical-oncology practice at 50 Cohasset Avenue, Buzzards Bay. Chemotherapy, immunotherapy and ECT are listed; CT/MRI and radiation are referred externally. Call 508-276-0836 to confirm the regimen and appointment.'
 else:
  r.setdefault('verification_url',r['website']);r.setdefault('availability_note','Current clinic service, clinician and contact information reviewed. Confirm the assigned veterinarian, treatment suitability and appointment directly with the clinic.')
 # Ordinary natural-page route may remain a JS shell; its actual route modules
 # above are the successful clinical evidence, not an invented rendered visit.
 updates.append(copy.deepcopy(r));reviewed(r,'existing_primary_reconciliation',before)
write(paths[1],supp)
# Preserve successful clinical verification dates for held sources; a current
# failed request is not a new successful verification.
held_reviews=[]
for sid in held:
 s=next(x for x in inv['sources'] if x['id']==sid)
 if sid=='integrity-veterinary-center':
  attempts=[x for x in pages if 'integrityvetcenter.com' in x['url']]
  last=max(attempts,key=lambda x:x['attempted_at'])
  s.update(last_checked=DATE,last_checked_at=last['attempted_at'],last_result='unreachable',content_sufficient=False,last_run_id=RUN,last_review_run_id=RUN,needs_recheck=True,last_review_note='Exact current primary routes returned 403. Preserve prior clinical facts and successful verification date; do not infer closure or absent services.',review_reference='research/audit-runs/'+RUN+'/remaining.json')
  held_reviews.append({'source_id':sid,'result':'current_primary_403','attempts':[x['url'] for x in attempts],'successful_verification_date_refreshed':False})
 else:held_reviews.append({'source_id':sid,'result':'preserved_prior_exact_live_403_scope','attempts':[],'successful_verification_date_refreshed':False,'remaining':'Current clinical source review deferred under the recorded exact-route restriction; no retry or fabricated date.'})
write(paths[2],inv)
write('research/audit-runs/'+RUN+'/published-records.json',new)
write('research/audit-runs/'+RUN+'/existing-updates.json',updates)
write('research/audit-runs/'+RUN+'/evidence.json',evidence)
write('research/audit-runs/'+RUN+'/held-existing.json',held_reviews)
print('Integrated supplemental:',len(new),'new',len(updates),'existing; held',len(held_reviews))
