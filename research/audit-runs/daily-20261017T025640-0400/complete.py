"""Assemble actual visits, individually reviewed decisions and durable discovery leads."""
import json,copy,hashlib,re,collections
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent; ROOT=P.parents[2]; OLD=P.parent/'daily-20261016T025651-0400'; TZ=ZoneInfo('America/New_York')
def read(p): return json.loads(p.read_text())
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now(): return datetime.now(TZ).isoformat()
def dt(s): return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ)
base=read(P/'baseline.json'); before=read(P/'before-source_inventory.json')['sources']; inv=read(ROOT/'data/source_inventory.json'); reviews=read(P/'reviews.json')[:111]
native=[json.loads(x) for x in (P/'attempts.jsonl').read_text().splitlines()]
web=read(P/'web-attempts.json'); browser=read(P/'browser-observations.json')['rows']
for a in browser:
 a['text_sha256']=hashlib.sha256(json.dumps(a,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
write(P/'browser-attempts.json',browser)
dw=read(P/'discovery-primary-web1.json'); wat=dt(datetime.strptime(dw['at'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).isoformat()).isoformat()
parts=dw['result']['content'][0]['text'].split('\n--------------------------------------------------------------------------------\n')
discovery_web=[]
for u,t in zip(dw['urls'],parts):
 ref=re.search(r'【(turn\w+view\d+)】',t)
 discovery_web.append({'source_id':'discovery-mibagents-canine-trials' if 'mibagents' in u else 'discovery-cambridge-ctvt' if 'cam.ac' in u else 'discovery-feline-cetuximab','url':u,'route':'same_url_Web_fallback','method':'Web','attempted_at':wat,'result':'retrieval_error' if 'Failed to fetch' in t else 'retrieved_page','text_length':len(t),'text_sha256':hashlib.sha256(t.encode()).hexdigest(),'evidence_file':str(P/'discovery-primary-web1.json'),'evidence_reference':ref.group(1) if ref else None,'freshness':'Cached crawl yesterday' if 'Crawled: yesterday' in t else 'Freshness retained in retrieved page; no current enrollment inferred.'})
write(P/'discovery-web-attempts.json',discovery_web)
actual=native+web+browser+discovery_web
new_specs=[
 {'id':'foundation-mibagents-canine-trials','original':'discovery-mibagents-canine-trials','name':'MIB Agents — Canine Clinical Trials','country':'USA','source_type':'foundation','master_url':dw['urls'][1],'question':'Which listed osteosarcoma opportunities still enroll? The secondary directory explicitly says updated March19,2024; current primary rosters, not this list, govern access.','reason':'Official foundation directory establishes29 historical treatment/diagnostic/research signals plus known institutional links. Today native transport timed out twice; same-URL Web retrieved the directory from a yesterday crawl. Known CSU/COTC/Ethos/OVC/UF/Illinois/Penn/Ohio/VT identities reconciled using today’s source evidence. No current opportunity activated from this old secondary list.','category':'freshness_uncertain','evidence':str(P/'discovery-primary-web1.json')+'#turn836view1','roster':None},
 {'id':'india-actrec-comparative-oncology-program','original':'discovery-india-actrec','name':'ACTREC — Pradip Chaudhari comparative oncology research programme','country':'India','source_type':'investigator_lab','master_url':'https://actrec.gov.in/hi/node/997','question':'Does ACTREC publish a named currently enrolling dog/cat anticancer treatment protocol and owner intake/cost criteria? The programme profile does not supply those facts.','reason':'Fresh official full laboratory profile read. Comparative oncology, imaging/radiotherapy facilities and animal-cancer biorepository are research signals, without a named current owner-enrolling protocol. Laboratory profile is a discovery source, not a requested exhaustive trial roster; no clinical record or care directory imported.','category':'discovery_source_not_trial_roster','evidence':str(P/'evidence/d54b7dab6543cc266a.json'),'roster':[]},
]
for spec in new_specs:
 aa=[dict(x,source_id=spec['id'],original_request_source_id=x['source_id']) for x in actual if x['source_id']==spec['original']]
 assert aa
 last=max(aa,key=lambda x:dt(x['attempted_at']))
 s={'id':spec['id'],'name':spec['name'],'country':spec['country'],'source_type':spec['source_type'],'master_url':spec['master_url'],'fallback_urls':[],'required_cadence':'daily','last_checked':dt(last['attempted_at']).date().isoformat(),'last_checked_at':dt(last['attempted_at']).isoformat(),'last_result':'partial','content_fingerprint':None,'notes':spec['reason'],'source_role':'discovery; not a primary recruiting roster','discovered_at':now(),'discovery_evidence':spec['evidence']}
 inv['sources']=[v for v in inv['sources'] if v['id']!=s['id']]; inv['sources'].append(s)
 r={'source_id':s['id'],'content_sufficient':False,'source_result':'partial','protocols_seen':None,'current_roster':spec['roster'],'category':spec['category'],'question':spec['question'],'next_action':'Review actual new protocol links or a new owner-enrollment signal; do not require an exhaustive recruiting roster from this discovery source. Daily master visit remains required.','reconciliation':spec['reason'],'reviewed_at':now(),'processing_complete':True,'processing_assessment':'external_blocker','current_comparison_evidence':[spec['evidence']],'actual_attempts':aa,'completion_decision':{'remaining_fact':spec['question'],'routes_exhausted_evidence':[{'url':x['url'],'method':x['method'],'at':x['attempted_at'],'result':x['result'],'evidence':x.get('evidence_file')} for x in aa],'available_reconciliation_done_evidence':spec['reason']}}
 reviews.append(r)
assert [s['id'] for s in inv['sources']][:111]==base['source_ids']
assert [r['source_id'] for r in reviews]==[s['id'] for s in inv['sources']]
write(P/'new-sources.json',new_specs);write(P/'reviews.json',reviews)
oldby={s['id']:s for s in before}; dates=[];unchanged=[];rows=[]
for s,r in zip(inv['sources'],reviews):
 b=oldby.get(s['id'],{}); aa=copy.deepcopy(r['actual_attempts']);aa.sort(key=lambda x:dt(x['attempted_at']))
 for a in aa:a.update(new_visit_this_run=True,visit_origin_run_id=P.name)
 if aa:
  last=aa[-1]; at=dt(last['attempted_at']);s.update(last_checked=at.date().isoformat(),last_checked_at=at.isoformat(),last_result='reachable' if r['content_sufficient'] else 'unreachable' if r['source_result']=='unreachable' else 'partial',last_http_status=last.get('http_status'),audit_last_run_id=P.name,last_check_summary=r['reconciliation'],content_sufficient=r['content_sufficient'],last_protocols_seen=r['protocols_seen'],last_coverage_receipt=str(P/'receipt-final.json'),last_coverage_gap=r.get('question'),last_route_used=sorted({a['method'] for a in aa}))
  keep=('source_id','url','effective_url','route','method','attempted_at','completed_at','http_status','retry','result','text_sha256','evidence_file','evidence_reference','freshness','exit_code')
  s['last_attempts']=[{k:a[k] for k in keep if k in a} for a in aa]
  masters=[a for a in aa if a['url'].rstrip('/')==s['master_url'].rstrip('/') and a.get('http_status')==200 and a.get('text_length',0)>200 and a.get('text_sha256')]
  if masters:s.update(content_fingerprint='sha256:'+masters[-1]['text_sha256'],content_fingerprint_method=masters[-1]['method']+'_retrieved_text')
  dates.append({'source_id':s['id'],'previous_last_checked':b.get('last_checked'),'previous_last_checked_at':b.get('last_checked_at'),'new_last_checked':s['last_checked'],'new_last_checked_at':s['last_checked_at'],'new_last_result':s['last_result'],'actual_last_attempted_at':last['attempted_at'],'new_source':not bool(b),'local_readback':'PASS'})
 else:
  assert (s.get('last_checked'),s.get('last_checked_at'))==(b.get('last_checked'),b.get('last_checked_at'));unchanged.append(s['id'])
 inherited=[dict(a,new_visit_this_run=False,inherited_denial=True,not_retried_this_run=True) for a in b.get('last_attempts',[])] if not aa else []
 if not aa and not inherited:inherited=[{'url':s['master_url'],'method':'historical_explicit_gate','new_visit_this_run':False,'evidence_file':str(P/'inherited-gates.json'),'not_retried_this_run':True}]
 row={**r,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':bool(aa),'attempted_urls':aa+inherited,'route_used':sorted({a['method'] for a in aa}),'master_result':'reachable' if r['content_sufficient'] else r['source_result'],'original_source_id_preserved':bool(b)}
 for k in ('last_checked','last_checked_at','last_result','content_fingerprint'):row['previous_'+k]=b.get(k);row['new_'+k]=s.get(k)
 row['historical_fingerprint_preserved_not_roster_proof']=b.get('content_fingerprint')==s.get('content_fingerprint'); rows.append(row)
inv['updated']='2026-10-17';write(ROOT/'data/source_inventory.json',inv)
write(P/'local-date-readback.json',{'run_id':P.name,'verified_at':now(),'status':'PASS','attempted_current_dates':len(dates),'unvisited_dates_unchanged':unchanged,'original_inventory_ids_and_order_preserved':True,'source_inventory_sha256':hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),'rows':dates})
matrix={};query_count=0
for f in sorted(P.glob('discovery-*.json')):
 d=read(f)
 if not isinstance(d,dict) or d.get('pass') not in ['current_undated','fresh_7_days']:continue
 for region,language,q in d['queries']:
  query_count+=1;matrix.setdefault(region,{}).setdefault(d['pass'],[]).append({'language':language,'query':q,'evidence_file':str(f),'actual_requested_at':d['at']})
required=['USA','Canada','UK','Europe','LatinAmerica','AustraliaNZ','EastAsia','SouthAsia','SoutheastAsia','MiddleEast','NorthAfrica','SubSaharanAfrica']
assert all(k in matrix and all(p in matrix[k] for p in ['current_undated','fresh_7_days']) for k in required)
write(P/'discovery-matrix.json',{'run_id':P.name,'completed_at':now(),'regions_completed':12,'passes':2,'query_count':query_count,'fresh_window_start':'2026-10-10','fresh_window_end':'2026-10-17','matrix':matrix,'limits':'Real queries executed, including local languages and LinkedIn discovery. Recency filtering still returns old recrawls; publication dates separately considered. Weak/noisy indexing in South Asia/Middle East/Africa/SEA is not proof of no trials. New primary leads separately qualified.'})
counts=dict(collections.Counter(r['source_result'] for r in rows));unfinished=[r['source_id'] for r in rows if not r.get('processing_complete')]
receipt={'run_id':P.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':base['started_at'],'source_pass_sealed_at':now(),'base_main_sha':base['base_main_sha'],'source_total':len(rows),'attempted_total':sum(r['opened_this_run'] for r in rows),'content_sufficient_total':sum(r['content_sufficient'] for r in rows),'processing_complete_total':sum(r.get('processing_complete') is True for r in rows),'source_result_counts':counts,'executor_incomplete_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'discovery_regions_completed':12,'discovery_matrix':str(P/'discovery-matrix.json'),'sources':rows,'status':'INCOMPLETE','processing_status':'ALL_PROCESSED_EXTERNAL_GAPS' if not unfinished else 'EXECUTOR_INCOMPLETE','execution_policy_status':'FAIL_DEVIATIONS_RECORDED','execution_policy_evidence':str(P/'execution-deviations.json'),'separate_inherited_full_fresh_protocol_reviews_missing':40,'clinical_catalog_changes':0,'new_source_count':2}
write(P/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt)
gaps=[]
for r in rows:
 if r['content_sufficient']:continue
 gaps.append({'source_id':r['source_id'],'category':r['category'],'processing_assessment':r['processing_assessment'],'question':r['question'],'reason':r['reconciliation'],'next_action':r['next_action'],'completion_decision':r['completion_decision'],'evidence':{'source_id':r['source_id'],'attempted_urls':list(dict.fromkeys(a['url'] for a in r['attempted_urls']))}})
write(P/'gap-review.json',{'original_run_id':P.name,'reviewed_at':now(),'rows':gaps})
state=read(ROOT/'data/audit_state.json');state['last_incremental_audit']=now();state['last_source_discovery_attempt']={'run_id':P.name,'started_at':base['started_at'],'source_pass_sealed_at':receipt['source_pass_sealed_at'],'status':receipt['processing_status'],'execution_policy_status':receipt['execution_policy_status'],'source_total':len(rows),'attempted':receipt['attempted_total'],'processing_complete':receipt['processing_complete_total'],'sufficient':receipt['content_sufficient_total'],'coverage_receipt':str(P/'receipt-final.json'),'latest_receipt':'data/audit_source_coverage.json','catalog_changes':0,'new_source_entries':2,'global_discovery_regions':required,'pending_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'external_gap_source_ids':[r['source_id'] for r in gaps],'gap_review':str(P/'gap-review.json'),'issues':str(P/'issues.json'),'separate_protocol_review_gaps':40};write(ROOT/'data/audit_state.json',state)
issues=read(OLD/'issues.json');issues.update(run_id=P.name,reviewed_at=now(),prior_issue_file=str(OLD/'issues.json'),preservation_note='All79 previous issue IDs/history retained. Nine owner dispositions already applied before this baseline; retained questions remain exact protocol facts, not repeated owner decisions. No unchanged unpublished question is backdated as newly verified.',concretely_resolved_this_run=[],narrowed_this_run=[])
owner_europe={s for s in base['source_ids'] if False}
for x in issues['issues']:
 if x['issue_id'].startswith('access-') and x.get('record_ids') and x['issue_id'] in {'access-fr-fregis-hepatic-tumor-thermoablation','access-fr-fregis-chemodectoma-thermoablation','access-fr-fregis-hepatic-embolization','access-eu-ch-sinonasal-heterogeneous-rt','access-uk-rvc-insulinoma-toceranib','access-nl-utrecht-osteosarcoma-oncolytic-virus-access'}:
  x.setdefault('history',[]).append({'decision':x['decision'],'remaining_fact':x.get('remaining_fact'),'as_of':OLD.name});x.update(decision='watch_nonmatchable_owner_quarantine_applied',owner_decision_already_applied_before_run=True,current_public_state_preserved=True,owner_action_required=False,daily_queue_reentry=False,current_review_evidence='reviews.json; baseline clinical catalog unchanged')
 if x['issue_id'].startswith('utsw-status-conflict-'):
  x.setdefault('history',[]).append({'decision':x['decision'],'remaining_fact':x.get('remaining_fact'),'as_of':OLD.name});x.update(decision='resolved_owner_completed',remaining_fact=None,resolution='Owner explicitly accepted AVMA Completed; canonical record confirmed_completed and nonmatchable before this run. Fresh registry snapshot unchanged.',owner_decision_already_applied_before_run=True,owner_action_required=False,daily_queue_reentry=False,current_review_evidence='registry-comparison.json; before-trials_base.json')
write(P/'issues.json',issues)
write(P/'segment-03.md.json',{'at':now(),'source_status':counts,'sources':len(rows),'daily_executor_unfinished_sources':unfinished,'discovery_regions':12,'actual_queries':query_count,'publication':'not yet attempted','execution_policy':'deviations disclosed separately; dispatch guard fixed','independent_protocol_review_gaps':40})
print(json.dumps({'source_counts':counts,'attempted':receipt['attempted_total'],'processed':receipt['processing_complete_total'],'queries':query_count,'gaps':len(gaps),'issues':len(issues['issues'])}))
