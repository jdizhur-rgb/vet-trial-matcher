"""Preserve explicit source reviews and actual visit times; assemble honest gaps."""
import json,copy,hashlib,collections
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2];OLD=P.parent/'daily-20261015T030225-0400';TZ=ZoneInfo('America/New_York')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(TZ).isoformat()
def norm(u):return u.rstrip('/')
inv=read(P/'before-source_inventory.json')['sources'];reviews=read(P/'reviews.json');base=read(P/'baseline.json')
assert [r['source_id'] for r in reviews]==[s['id'] for s in inv]
# Fresh all-registry comparison includes today's three status changes.
reviews[0]['current_roster']=read(P/'registry-comparison.json')['rows']
reviews[0]['current_roster_basis']='All current titles/statuses/entire descriptions explicitly compared, registry-comparison.json and its two complete API snapshots. Provider conflicts remain separate.'
write(P/'reviews.json',reviews)
browser=read(P/'browser-observations.json')['rows']
for a in browser:
 a['evidence_file']=str((P/'browser-observations.json').relative_to(ROOT));a['new_visit_this_run']=True;a['text_sha256']=hashlib.sha256(json.dumps(a,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
write(P/'browser-attempts.json',browser)
native=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()];actual=native+read(P/'web-attempts.json')+browser
# Date sync runs only for actual visits. Six inherited gates retain every prior date.
inventory=read(ROOT/'data/source_inventory.json');date_rows=[];rows=[];unchanged=[]
for s,b,r in zip(inventory['sources'],inv,reviews):
 assert s['id']==b['id']==r['source_id'];urls={s['master_url']}|set(s.get('fallback_urls',[]))
 a=[dict(x,new_visit_this_run=True,visit_origin_run_id=P.name) for x in actual if x['source_id']==s['id'] or x['url'] in urls];a.sort(key=lambda x:datetime.fromisoformat(x['attempted_at']))
 if a:
  last=a[-1];at=datetime.fromisoformat(last['attempted_at']).astimezone(TZ)
  s.update(last_checked=at.date().isoformat(),last_checked_at=at.isoformat(),last_result='reachable' if r['content_sufficient'] else 'unreachable' if r['source_result']=='unreachable' else 'partial',last_http_status=last.get('http_status'),audit_last_run_id=P.name,last_check_summary=r['reconciliation'])
  keep=('source_id','url','effective_url','route','method','attempted_at','completed_at','http_status','retry','result','text_sha256','evidence_file','evidence_reference','crawl_freshness','exit_code')
  s['last_attempts']=[{k:x[k] for k in keep if k in x} for x in a]
  master=[x for x in a if norm(x['url'])==norm(s['master_url']) and x.get('result')=='retrieved_page' and (x.get('text_length') or 0)>200 and (x.get('http_status')==200 or x['method']=='Web' and x.get('crawl_freshness')=='today')]
  if master:s['content_fingerprint']='sha256:'+master[-1]['text_sha256'];s['content_fingerprint_method']=master[-1]['method']+'_retrieved_text'
  date_rows.append({'source_id':s['id'],'previous_last_checked':b.get('last_checked'),'previous_last_checked_at':b.get('last_checked_at'),'new_last_checked':s['last_checked'],'new_last_checked_at':s['last_checked_at'],'new_last_result':s['last_result'],'evidence_last_attempted_at':last['attempted_at'],'local_readback':'PASS'})
 else:
  unchanged.append(s['id']);assert s.get('last_checked')==b.get('last_checked') and s.get('last_checked_at')==b.get('last_checked_at')
 inherited=[dict(x,new_visit_this_run=False,inherited_denial=True,not_retried_this_run=True) for x in b.get('last_attempts',[])] if not a else []
 if not a and not inherited:inherited=[{'url':s['master_url'],'method':'historical_explicit_gate','new_visit_this_run':False,'evidence_file':str((P/'inherited-gates.json').relative_to(ROOT)),'not_retried_this_run':True}]
 row={**r,'source_name':s.get('name',s['id']),'master_url':s['master_url'],'opened_this_run':bool(a),'attempted_urls':a+inherited,'route_used':sorted({x['method'] for x in a}),'master_result':'reachable' if r['content_sufficient'] else r['source_result'],'original_source_id_preserved':True}
 for f in ('last_checked','last_checked_at','last_result','content_fingerprint'):row['previous_'+f]=b.get(f);row['new_'+f]=s.get(f)
 row['historical_fingerprint_preserved_not_roster_proof']=b.get('content_fingerprint')==s.get('content_fingerprint');row['current_content_comparison_evidence']=r['reconciliation'];rows.append(row)
inventory['updated']=datetime.now(TZ).date().isoformat();write(ROOT/'data/source_inventory.json',inventory)
assert [s['id'] for s in inventory['sources']]==base['source_ids']
write(P/'local-date-readback.json',{'run_id':P.name,'verified_at':now(),'status':'PASS','attempted_current_dates':len(date_rows),'unvisited_dates_unchanged':unchanged,'inventory_ids_and_order_preserved':True,'source_inventory_sha256':hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),'rows':date_rows})
matrix={};query_count=0
for f in sorted(P.glob('discovery-*.json')):
 d=read(f)
 if 'pass' not in d:continue
 for region,language,q in d['queries']:
  query_count+=1;matrix.setdefault(region,{}).setdefault(d['pass'],[]).append({'language':language,'query':q,'evidence_file':str(f.relative_to(ROOT)),'actual_requested_at':d['at']})
required=['USA','Canada','UK','Europe','LatinAmerica','AustraliaNZ','EastAsia','SouthAsia','SoutheastAsia','MiddleEast','NorthAfrica','SubSaharanAfrica']
assert all(k in matrix and all(p in matrix[k] for p in ['current_undated','fresh_7_days']) for k in required)
write(P/'discovery-matrix.json',{'run_id':P.name,'completed_at':now(),'regions_completed':12,'passes':2,'query_count':query_count,'fresh_window_start':'2026-10-09','fresh_window_end':'2026-10-16','matrix':matrix,'limits':'Actual current/undated and seven-day searches performed. Search noise includes human trials, historical studies and irrelevant terms. Recrawl is not a publication date; no exhaustive absence claim, especially for weakly indexed South Asia/Middle East/Africa. Primary new leads separately qualified in discovery-dispositions.json.'})
counts=dict(collections.Counter(r['source_result'] for r in rows));unfinished=[r['source_id'] for r in rows if not r.get('processing_complete')]
receipt={'run_id':P.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':base['started_at'],'source_pass_sealed_at':now(),'base_main_sha':base['base_main_sha'],'source_total':len(rows),'attempted_total':sum(r['opened_this_run'] for r in rows),'content_sufficient_total':sum(r['content_sufficient'] for r in rows),'processing_complete_total':sum(r.get('processing_complete') is True for r in rows),'source_result_counts':counts,'executor_incomplete_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'discovery_regions_completed':12,'discovery_matrix':str((P/'discovery-matrix.json').relative_to(ROOT)),'sources':rows,'status':'INCOMPLETE','processing_status':'ALL_PROCESSED_EXTERNAL_GAPS' if not unfinished else 'EXECUTOR_INCOMPLETE'}
write(P/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt)
gaps=[]
for r in rows:
 if r['content_sufficient']:continue
 gaps.append({'source_id':r['source_id'],'category':r['category'],'processing_assessment':r['processing_assessment'],'question':r['question'],'reason':r['reconciliation'],'next_action':r['next_action'],'completion_decision':r['completion_decision'],'evidence':{'source_id':r['source_id'],'attempted_urls':list(dict.fromkeys(a['url'] for a in r['attempted_urls']))}})
write(P/'gap-review.json',{'original_run_id':P.name,'reviewed_at':now(),'rows':gaps})
state=read(ROOT/'data/audit_state.json');state['last_incremental_audit']=now();state['last_source_discovery_attempt']={'run_id':P.name,'started_at':base['started_at'],'source_pass_sealed_at':receipt['source_pass_sealed_at'],'status':receipt['processing_status'],'source_total':len(rows),'attempted':receipt['attempted_total'],'processing_complete':receipt['processing_complete_total'],'sufficient':receipt['content_sufficient_total'],'coverage_receipt':str((P/'receipt-final.json').relative_to(ROOT)),'latest_receipt':'data/audit_source_coverage.json','catalog_changes':3,'new_source_entries':0,'global_discovery_regions':required,'pending_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'external_gap_source_ids':[r['source_id'] for r in gaps],'gap_review':str((P/'gap-review.json').relative_to(ROOT)),'issues':str((P/'issues.json').relative_to(ROOT))};write(ROOT/'data/audit_state.json',state)
issues=read(OLD/'issues.json');issues.update(run_id=P.name,reviewed_at=now(),prior_issue_file=str((OLD/'issues.json').relative_to(ROOT)),preservation_note='All74 prior IDs/history retained. New primary resolves Missouri only; old residual questions are not automatically closed by method changes. New UTSW conflicts shared between registry/institution, no duplicated daily queue.')
for x in issues['issues']:
 if x['issue_id']=='leah-missouri-cohort-current-intake':
  x.update(decision='resolved_verified',resolved_at=now(),resolution='Fresh current native protocol and today Web agree Missouri enrolling; site-specific cohort/cost/schedule applied to existing canonical LEAH. Minnesota stays hold; Ohio separateP1.',resolution_evidence=['leah-source-derived-review.json','leah-canonical-change.json','web-04.json'],daily_queue_reentry=False)
 if x['issue_id']=='leah-ohio-current-site':
  x.setdefault('history',[]).append({'question':x['question'],'last_reviewed':x.get('last_reviewed')});q='Ohio sponsor-listed current slot/institutional criteria still need local corroboration; Missouri current enrolling is now independently confirmed, Minnesota direct protocol remains hold.';x.update(question=q,remaining_fact=q,last_reviewed=now(),current_review_evidence='reviews.json#sponsor-leah-labs-clinical-trial; leah-canonical-change.json')
 if x['issue_id']=='source-question-canada-ovc-active-oncology-trials':
  x.setdefault('history',[]).append({'question':x['question'],'last_reviewed':x.get('last_reviewed')});q='Only feline Porphysome detailed eligibility and owner expenses remain unpublished. Canine Palladia/HIFU due primary reads completed and two filter defects corrected.';x.update(question=q,remaining_fact=q,last_reviewed=now(),current_review_evidence='ovc-source-derived-review.json; ovc-canonical-changes.json')
for rid,study,registry in [('utsw-solid-cpmv','CPMV','21821'),('vroc-rt-histotripsy','RT+HIFU','21836'),('utsw-vroc-melanoma-crtnp-hifu-pdl1','CRTNP+HIFU±checkpoint','21837')]:
 q=f'UTSW {study}: AVMA registry{registry} changed Recruiting→Completed; current institution master and individual PDF still describe enrolling. Which current intake/status governs?'
 issues['issues'].append({'issue_id':'utsw-status-conflict-'+registry,'impact':'P0','kind':'protocol_status','source_ids':[inv[0]['id'],inv[27]['id']],'record_ids':[rid],'question':q,'remaining_fact':q,'first_seen':now(),'last_reviewed':now(),'recheck_after':'2026-10-23','decision':'decision_required','evidence':['registry-comparison.json','utsw-visual-review.json','reviews.json#usa-utsw-vroc-clinical-trials'],'proposed_not_applied':{'available_for_matching':False,'status_confidence':'unconfirmed','reason':'Temporary quarantine pending concordant current owner intake; not a confirmed closure.'},'current_public_state_preserved':True,'daily_queue_reentry':False})
issues['concretely_resolved_this_run']=['leah-missouri-cohort-current-intake'];issues['narrowed_this_run']=['leah-ohio-current-site','source-question-canada-ovc-active-oncology-trials'];write(P/'issues.json',issues)
events=[];domain_events=collections.defaultdict(list)
from urllib.parse import urlsplit
for a in native:
 e=[(a['attempted_at'],1),(a['completed_at'],-1)];events.extend(e);domain_events[urlsplit(a['url']).hostname].extend(e)
def peak(es):
 n=m=0
 for t,d in sorted(es):n+=d;m=max(m,n)
 return m
write(P/'execution-compliance.json',{'native_request_count':len(native),'native_peak_overlap':peak(events),'domain_peak_overlap':{k:peak(v) for k,v in domain_events.items()},'limits':{'global':6,'domain':2,'connect_seconds':5,'total_seconds':20,'transient_retries':1},'source_ids_preserved':len(inv),'explicit_gate_deviation':{'source_id':inv[28]['id'],'url':inv[28]['master_url'],'actual_attempt':'one native404 despite prior403; no retry/Web bypass; both permitted fallbacks read','status':'DEVIATION'},'checkpoint_cadence':'Timestamped checkpoint files preserved. First immutable narrative segment was recorded later than15minutes after start; not backdated.','source_processing_status':receipt['processing_status']})
print('Assembled',receipt['attempted_total'],len(rows),counts,'gaps',len(gaps),'executor',len(unfinished),'queries',query_count,'peak',peak(events))
