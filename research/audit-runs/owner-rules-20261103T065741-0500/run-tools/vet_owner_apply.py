import pathlib,json,re,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/owner-rules-20261103');R=ROOT/pathlib.Path('/tmp/vet-owner-rules-path').read_text();OLD=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103/research/audit-runs/daily-20261103T030532-0500')
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(p):return str(p.relative_to(ROOT))
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
at=now();C=rd(ROOT/'data/trials_base.json');T={t['id']:t for t in C};B={t['id']:t for t in rd(R/'baseline-trials_base.json')};E=[rd(p) for p in (OLD/'evidence').glob('*.json')];registry=[]
for i in [1,2]:registry+=rd(R/f'evidence/avma-page-{i}.json')['studies']
assert len({a['id'] for a in registry})==856
closed=next(a for a in registry if a['id']==22208);assert closed['vct_code']=='VCT25005914' and closed['status']=='Completed'
wr(R/'evidence/penn-current-registry-record.json',{'url':closed['absolute_url'],'retrieved_at':rd(R/'evidence/avma-page-1-receipt.json')['retrieved_at'],'source_response':ref(R/'evidence/avma-page-1.json'),'record':closed})
penn=T['penn-bcell-car-t-registry'];penn.update(available_for_matching=False,status_confidence='completed',status='Completed — recruitment closed in AVMA VCT25005914',registry_status='Completed',avma_vct_code='VCT25005914',registry_url_verified=at[:10],registry_status_checked_at=rd(R/'evidence/avma-page-1-receipt.json')['retrieved_at'],closure_reason='avma_closed')
penn['notes']='Historical autologous CAR-T treatment for canine B-cell lymphoma or leukemia. The current AVMA record VCT25005914/public999878, coordinated by Nicola Mason at Penn, marks this exact cohort Completed. Recruitment is closed and the record is retained outside current matching.'
penn['status_evidence_refs']=[ref(R/'evidence/penn-current-registry-record.json'),ref(R/'evidence/penn-individual.json')]
dates={
'wsu-sts-local-immunotherapy':('2027-07-30','America/Los_Angeles'),
'ucd-pdl1-metastatic':('2027-09-10','America/Los_Angeles'),
'ucd-oral-margin':('2028-06-30','America/Los_Angeles'),
'csu-brain-cart-verdinexor':('2028-12-31','America/Denver'),
'ucd-care-canine-glioma':('2028-01-04','America/Los_Angeles'),
'ucd-prism-canine-glioma':('2031-08-13','America/Los_Angeles'),
'csu-aml-trametinib':('2028-03-31','America/Denver'),
'utsw-hsa-temozolomide-propranolol':('2028-01-08','America/Chicago'),
'jp-nvlu-survivin-peptide-vaccine-2026':('2027-03-31','Asia/Tokyo')}
recon=rd(OLD/'avma-active-reconciliation.json')['rows'];date_rows=[];months=['January','February','March','April','May','June','July','August','September','October','November','December']
def normalize(x):return re.sub(r'[^\w]','',str(x)).lower()
for tid,(end,tz) in dates.items():
 t=T[tid];assert t.get('available_for_matching') is not False
 avma_refs={r for a in recon if tid in a.get('canonical_ids',[]) for r in a.get('primary_evidence_refs',[])}
 es=[e for e in E if (tid=='jp-nvlu-survivin-peptide-vaccine-2026' and e['url']=='https://www.nvlu.ac.jp/amedical/clinical-research/index.html') or e.get('source_id')==tid or e.get('url','').split('?')[0].rstrip('/') in {str(t.get(k,'')).split('?')[0].rstrip('/') for k in ['url','registry_url']} or e['evidence_file'] in avma_refs]
 y,m,d=map(int,end.split('-'));variants=[end,f'{y}年{m}月{d}日',f'{months[m-1]} {d}, {y}',f'{months[m-1][:3]}. {d}, {y}'];matched=[]
 for e in es:
  if e.get('result')!='retrieved_page':continue
  body=normalize(json.dumps({k:e.get(k) for k in ['text','clinical_text','public_content']},ensure_ascii=False))
  if any(normalize(v) in body for v in variants):matched.append(e)
 if not matched:raise RuntimeError('No actual saved protocol end-date body for '+tid)
 evidence_refs=[]
 for e in matched:
  dest=R/'evidence'/('inherited-'+hashlib.sha256(e['url'].encode()).hexdigest()[:20]+'.json')
  if not dest.exists():wr(dest,{'method':'inherited_saved_primary_evidence','reused_at':at,'original_read_at':e['completed_at'],'original_evidence_ref':e['evidence_file'],'url':e['url'],'original_evidence':e,'new_source_visit':False})
  evidence_refs.append(ref(dest))
 primary=next((e for e in matched if 'api/v1/studycontent' in e['url']),matched[0])
 t['recruitment_end']=end;t['recruitment_end_timezone']=tz;t['recruitment_end_basis']={'rule':'study_end_as_recruitment_end','policy_ref':'data/audit_owner_policy.json','published_study_end':end,'primary_url':primary['url'],'original_read_at':primary['completed_at'],'scope':'same published protocol/cohort; no site activation inferred','enrollment_condition':'Existing recruiting/public claim retained; current local slots and all other source gaps remain as recorded.','evidence_refs':evidence_refs,'decision_recorded_at':at}
 date_rows.append({'trial_id':tid,'previous_recruitment_end':B[tid].get('recruitment_end'),'recruitment_end':end,'timezone':tz,'basis':t['recruitment_end_basis'],'verified_preserved':t.get('verified')==B[tid].get('verified'),'funding_verified_preserved':t.get('funding_verified')==B[tid].get('funding_verified')})
oral=T['ucd-oral-margin'];old='Recruitment period: 2026-06-30 through 2028-06-29.';assert old in oral['notes'];oral['notes']=oral['notes'].replace(old,'Published study period: July 1, 2026 through June 30, 2028. Enrollment ends June 30, 2028.')
explicit={'ncsu-liver-inspire':'2027-07-01','ncsu-mammary-inspire':'2027-07-01','ncsu-canine-sts-xcsgel':'2027-08-31','ncsu-feline-oral-pivot-c':'2027-12-31'}
for tid,end in explicit.items():
 t=T[tid];t['recruitment_end']=end;t['recruitment_end_timezone']='America/New_York';t['recruitment_end_basis']={'rule':'explicit_enrollment_cutoff','primary_url':t['url'],'canonical_evidence_date':B[tid].get('verified'),'evidence_refs':[ref(R/'baseline-trials_base.json')],'source_freshness':'Existing explicit primary-derived canonical cutoff; no new visit to a held individual route claimed.'}
 date_rows.append({'trial_id':tid,'previous_recruitment_end':B[tid].get('recruitment_end'),'recruitment_end':end,'timezone':'America/New_York','basis':t['recruitment_end_basis'],'verified_preserved':True,'funding_verified_preserved':True})
assert all(t.get('verified')==B[t['id']].get('verified') and t.get('funding_verified')==B[t['id']].get('funding_verified') for t in C)
wr(ROOT/'data/trials_base.json',C);wr(R/'date-decisions.json',{'recorded_at':at,'policy_ref':'data/audit_owner_policy.json','rows':date_rows,'no_new_full_clinical_reviews':True})
queue=rd(ROOT/'data/audit_execution_queue.json');baseline_queue={x['issue_id']:x for x in rd(R/'baseline-audit_execution_queue.json')['issues']};resolutions=[]
date_ids=['ucd-oral-margin','csu-brain-cart-verdinexor','jp-nvlu-survivin-peptide-vaccine-2026']
for item in queue['issues']:
 tid=item['trial_id']
 if item['issue_id'] not in {'full_protocol:'+x for x in date_ids+['penn-bcell-car-t-registry']}:continue
 assert item['state']=='OWNER_DECISION';original=baseline_queue[item['issue_id']];item['previous_owner_question']=item['question'];item['previous_reviewed_at']=item.get('reviewed_at');item.update(state='POLICY_RESOLVED',reviewed_at=at,full_protocol_review_complete=False,previous_verified=B[tid].get('verified'))
 if tid=='penn-bcell-car-t-registry':
  item.update(resolved_scope='current_access',finding='Owner rule applied to current exact AVMA22208/VCT25005914 Completed record; this cohort is now nonmatchable. This is closure, not a five-fact clinical reread.',policy_resolution={'rule':'avma_closed','registry_status':'Completed','avma_vct_code':'VCT25005914','identity_comparison':'Canonical registry URL public999878 and VCT25005914 identify the same Penn/Nicola Mason autologous B-cell lymphoma/leukemia CAR-T cohort; no other Penn CAR-T cohort closed.','evidence_refs':penn['status_evidence_refs']})
 else:
  basis=T[tid]['recruitment_end_basis'];item.update(resolved_scope='deadline_interpretation',finding='Owner rule applies the published study end '+T[tid]['recruitment_end']+' as recruitment end for this currently public/recruiting cohort. Original clinical and funding dates preserved.',policy_resolution={'rule':'study_end_as_recruitment_end','published_study_end':T[tid]['recruitment_end'],'identity_comparison':'Exact canonical '+tid+' and its own saved primary study-period date; no grant/ethics/sidebar or other cohort substituted.','evidence_refs':basis['evidence_refs']})
 item['evidence_refs']=list(dict.fromkeys(item.get('evidence_refs',[])+item['policy_resolution']['evidence_refs']+['data/audit_owner_policy.json']));resolutions.append({'previous':original,'current':item})
assert len(resolutions)==4;queue['last_daily_run_id']=queue.get('last_daily_run_id') or queue.get('last_run_id');queue.update(last_run_id=R.name,last_update_scope='targeted_owner_policy',last_updated_at=at);wr(ROOT/'data/audit_execution_queue.json',queue);wr(R/'issue-resolutions.json',{'recorded_at':at,'rows':resolutions,'full_clinical_reviews_completed':0})
state=rd(ROOT/'data/audit_state.json');state['last_owner_policy_application']={'run_id':R.name,'at':at,'receipt':ref(R/'issue-resolutions.json'),'rules':'data/audit_owner_policy.json','scope':'One exact AVMA closure, known recruitment cutoffs and4owner-policy resolutions; not a repeated daily audit.'};wr(ROOT/'data/audit_state.json',state)
# Actual current AVMA requests refresh only that source's attempt metadata.
I=rd(ROOT/'data/source_inventory.json');source=next(s for s in I['sources'] if s['id']=='registry-avma-veterinary-clinical-trials');attempts=[]
for i in [1,2]:
 a=rd(R/f'evidence/avma-page-{i}-receipt.json');attempts.append({'url':a['url'],'method':'shell_curl','route':'official_fallback_targeted_status_reconciliation','attempted_at':a['attempts'][0]['started_at'],'completed_at':a['attempts'][-1]['completed_at'],'http_status':200,'result':'retrieved_page','new_source_visit':True,'evidence_file':ref(R/f'evidence/avma-page-{i}.json'),'text_sha256':a['sha256']})
a=rd(R/'evidence/penn-individual.json');attempts.append({'url':a['url'],'method':'shell_curl','route':'individual_registry_protocol','attempted_at':a['started_at'],'completed_at':a['completed_at'],'http_status':int(a['status']),'result':'retrieved_page' if a['status']=='200' else 'request_failed','new_source_visit':True,'evidence_file':ref(R/'evidence/penn-individual.json')})
last=max(attempts,key=lambda a:a['completed_at']);source.update(last_checked=last['completed_at'][:10],last_checked_at=last['completed_at'],last_result='partial',last_audit_run_id=R.name,last_attempts=attempts,last_check_summary='Targeted owner-policy reconciliation of the exact current AVMA Penn B-cell cohort: Completed. Both registry JSON pages read; no repeated global discovery, institution roster or full protocol-review claim.',last_coverage_receipt=ref(R/'source-attempt-receipt.json'));source['content_fingerprint']='sha256:'+hashlib.sha256(json.dumps([a.get('text_sha256') for a in attempts]).encode()).hexdigest();I['updated']=at[:10];wr(ROOT/'data/source_inventory.json',I);wr(R/'source-attempt-receipt.json',{'run_id':R.name,'scope':'Targeted AVMA status requests, not a full daily-source receipt','source_id':source['id'],'previous':next(s for s in rd(R/'baseline-source_inventory.json')['sources'] if s['id']==source['id']),'new':source,'attempted_urls':attempts})
print('closed1; study-end decisions',len(dates),'explicit cutoffs',len(explicit),'policy issues resolved',len(resolutions))
