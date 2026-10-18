from reconcile import *
import copy
rel=str(P.relative_to(ROOT));now=datetime.now(ZoneInfo('America/New_York')).isoformat();receipt=read(P/'receipt-final.json');inv=read(ROOT/'data/source_inventory.json');rows=receipt['sources'];allattempts=native+web
extra={'usa-purdue-wcorc-clinical-trials':['https://www.vet.purdue.edu/wcorc/clinical-trials/canine-t-cell-lymphoma.php'],'usa-illinois-clinical-trials':['https://vetmed.illinois.edu/wp-content/uploads/2026/01/RT-Gilvetmab-Oligomets-Jan-2026.pdf'],'india-actrec-comparative-oncology-program':['https://actrec.gov.in/node/1401']}
for r,s in zip(rows,inv['sources']):
 for u in extra.get(r['source_id'],[]):
  for a in allattempts:
   if key(a['url'])==key(u) and not any(x['evidence_file']==a['evidence_file'] and x['url']==a['url'] for x in r['actual_attempts']):r['actual_attempts'].append(a)
 if r['source_id']=='new-zealand-kode-veterinary-sciences-trials':r['current_roster']=[{'canonical_id':'nz-kvs-kv9-solid-tumor-pilot','sites':read(P/'new-kv9-trial.json')['record']['sites']}];r['reconciliation']+=' Eight physical-site addresses separately verified from official contact pages; Napier relocation resolves old210maplabel to170, and Remuera23Ascot is not the similar236Orakei hospital. See kv9-site-addresses.json.'
 if r['source_id']=='australia-anzcvs-oncology-research-news':r['category']='discovery_source_not_trial_roster'
 if r['actual_attempts']:
  latest=max(r['actual_attempts'],key=lambda a:a['attempted_at']);r['actual_last_attempt_at']=latest['attempted_at'];r['new_last_checked_at']=latest['attempted_at'];r['new_last_checked']=latest['attempted_at'][:10];r['attempted_urls']=r['actual_attempts'];s['last_checked_at']=r['new_last_checked_at'];s['last_checked']=r['new_last_checked'];s['last_attempts']=[{k:v for k,v in a.items() if k not in ('retrieved_text','raw_file','stderr')} for a in r['actual_attempts']]
 r['route_used']=sorted({a['method'] for a in r['actual_attempts']});s['last_check_summary']=r['reconciliation'] if r['opened_this_run'] else s.get('last_check_summary');
 if not r['content_sufficient']:r['completion_decision']['remaining_fact']=r['question'];r['completion_decision']['available_reconciliation_done_evidence']={'source_specific_reconciliation':r['reconciliation'],'current_full_comparisons':r.get('current_comparison_evidence',[]),'actual_attempts':[{k:a.get(k) for k in ['url','attempted_at','method','result','evidence_file']} for a in r['actual_attempts']]}
write(ROOT/'data/source_inventory.json',inv);receipt['source_pass_sealed_at']=now;write(P/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt);write(P/'reviews.json',rows)
gap=read(P/'gap-review.json')
for g in gap['rows']:
 r=next(r for r in rows if r['source_id']==g['source_id']);g['category']=r['category'];g['completion_decision']=r['completion_decision'];g['evidence']={'source_id':r['source_id'],'attempted_urls':[a['url'] for a in r['attempted_urls']],'current_attempts':r['actual_attempts'],'mandatory_routes':r['mandatory_routes']}
write(P/'gap-review.json',gap)
rb=read(P/'local-date-readback.json');rb['rows']=[{k:r.get(k) for k in ['source_id','opened_this_run','previous_last_checked','new_last_checked','previous_last_checked_at','new_last_checked_at','previous_last_result','new_last_result']} for r in rows];rb['source_inventory_sha256']=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest();rb['unvisited_dates_retained']=all(r['previous_last_checked_at']==r['new_last_checked_at'] for r in rb['rows'] if not r['opened_this_run']);assert rb['unvisited_dates_retained'];write(P/'local-date-readback.json',rb)
# Exact member gate persists; no host-wide restriction from a single route or method failure.
restr=read(ROOT/'data/source_access_restrictions.json');u='https://www.anzcvs.org.au/chapters/veterinary%2Boncology/documentlibrary'
if key(u) not in {key(x['url']) for x in restr['routes']}:restr['routes'].append({'url':u,'do_not_retry':True,'observed_at':'2026-10-18T04:01:20-04:00','method':'Web','reason':'Explicit Chapter Members only login gate','origin':rel+'/discovery-primary-recovery-3.json'})
write(ROOT/'data/source_access_restrictions.json',restr)
# Portable references for new artifacts only; historical frozen snapshots remain exact historical data.
for name in ['source_inventory.json','audit_state.json']:
 f=ROOT/'data'/name;data=read(f)
 def portable(v):
  if isinstance(v,dict):return {k:portable(x) for k,x in v.items()}
  if isinstance(v,list):return [portable(x) for x in v]
  if isinstance(v,str) and v.startswith('/workspace/') and '/research/' in v:return 'research/'+v.split('/research/',1)[1]
  return v
 write(f,portable(data))
rb['source_inventory_sha256']=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest();write(P/'local-date-readback.json',rb)
state=read(ROOT/'data/audit_state.json');state['last_source_discovery_attempt']['source_pass_sealed_at']=now;write(ROOT/'data/audit_state.json',state)
write(P/'execution-policy.json',{'status':'PASS','finite_single_pass':True,'native_requests':len(native),'Web_URL_reads':len(web),'explicit_prior_restricted_routes_not_retried':62,'mandatory_unperformed_source_actions':0,'full_discovery_regions':12,'no_same_run_partial_requeue':True,'known_tool_method_failure_is_not_access_denial':rel+'/nonretryable-Web-method-failures.json','new_actual_denials':read(ROOT/'data/source_access_restrictions.json')['routes'][-3:],'clinical_incomplete_is_separate':34,'new_site_address_retrieval_scope':'Eight explicitly named Kv9 trial sites only; no care inventory edits.'})
print('Final source evidence sealed',receipt['source_result_counts'])
