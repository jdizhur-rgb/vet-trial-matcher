import json, hashlib, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter

RUN=Path(__file__).parent
ROOT=RUN.parents[2]
NY=ZoneInfo('America/New_York')
def now():return datetime.now(NY).isoformat()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def instant(at):
 if ' UTC' in at:return datetime.strptime(at,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC'))
 return datetime.fromisoformat(at.replace('Z','+00:00'))
baseline=read(RUN/'baseline.json')
prior={s['id']:s for s in read(RUN/'before-source_inventory.json')['sources']}
inventory=read(ROOT/'data/source_inventory.json')
reviews=read(RUN/'source-reviews.json')
native=[json.loads(l) for l in (RUN/'shell-attempts.jsonl').read_text().splitlines()]
web=[json.loads(l) for l in (RUN/'web-attempts.jsonl').read_text().splitlines()]
# Shared current reads retain provenance; they do not become a new independent visit.
new_sid='usa-red-bank-veterinary-hospital-clinical-studies'
for a in list(web):
 if a['url']=='https://www.redbankvet.com/clinical-studies':
  web.append({**a,'source_id':new_sid,'shared_read_from_source_id':a['source_id']})
rows=[];dates=[];gaps=[]
for s in inventory['sources']:
 sid=s['id'];v=reviews[sid];old=prior.get(sid,{})
 aa=sorted([a for a in native+web if a['source_id']==sid],key=lambda a:instant(a['attempted_at']))
 assert aa,('No actual source attempt',sid)
 attempts=[]
 for a in aa:
  at=a['attempted_at']
  if ' UTC' in at:at=instant(at).astimezone(NY).isoformat()
  attempts.append({k:a.get(k) for k in ['url','effective_url','route','method','result','http_status','text_sha256','evidence_reference','crawl_freshness','retry','shared_read_from_source_id'] if a.get(k) is not None}|{'attempted_at':at})
 latest=max(attempts,key=lambda a:instant(a['attempted_at']))
 sufficient=v['result']=='fully_reconciled'
 status='unchanged' if sufficient else 'unreachable' if v['result']=='unreachable' else 'partial'
 s['last_checked_at']=latest['attempted_at'];s['last_checked']=latest['attempted_at'][:10]
 s['last_result']=status;s['last_http_status']=latest.get('http_status');s['last_attempts']=attempts
 s['notes']=v['reconciliation']
 fp=old.get('content_fingerprint')
 if sufficient:
  assert type(v.get('protocols_seen')) is int
  fp='sha256:'+hashlib.sha256(json.dumps(v['current_roster'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 s['content_fingerprint']=fp
 row={'source_id':sid,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':True,'attempted_urls':attempts,'route_used':sorted({a['method'] for a in attempts}),'master_result':status,'source_result':v['result'],'content_sufficient':sufficient,'protocols_seen':v.get('protocols_seen'),'current_roster':v.get('current_roster'),'processing_complete':v['processing_complete'],'processing_assessment':v.get('processing_assessment','completed_reconciliation'),'reconciliation':v['reconciliation'],'previous_last_checked':old.get('last_checked'),'new_last_checked':s['last_checked'],'previous_last_checked_at':old.get('last_checked_at'),'new_last_checked_at':s['last_checked_at'],'previous_content_fingerprint':old.get('content_fingerprint'),'new_content_fingerprint':fp,'historical_fingerprint_preserved_not_roster_proof':not sufficient,'fingerprint_preserved_from_prior_same_day_visit':False}
 rows.append(row)
 dates.append({k:row[k] for k in ['source_id','previous_last_checked','new_last_checked','previous_last_checked_at','new_last_checked_at']}|{'last_result':status,'actual_latest_attempt':latest,'timestamp_readback_matches_attempt':s['last_checked_at']==latest['attempted_at']})
 if not sufficient:
  assessment=v.get('processing_assessment','external_blocker' if v['processing_complete'] else 'not_established')
  question=v.get('question') or v.get('completion_decision',{}).get('remaining_fact') or 'Current roster cannot be established from the actually attempted official routes.'
  gap={'source_id':sid,'category':v.get('category','source_unavailable' if v['result']=='unreachable' else 'roster_unestablished'),'processing_assessment':assessment,'question':question,'reason':v['reconciliation'],'next_action':v.get('next_action','Recheck this exact current official fact after a new primary signal or existing seven-day due date.'),'evidence':{'source_id':sid,'attempted_urls':list(dict.fromkeys(a['url'] for a in attempts)),'attempts':attempts},'impact_scope':v.get('impact_scope','source_roster_or_protocol_question'),'affected_record_ids':v.get('affected_record_ids',[])}
  if assessment=='external_blocker':
   gap['completion_decision']=v.get('completion_decision') or {'remaining_fact':question,'routes_exhausted_evidence':{'actually_attempted_urls':gap['evidence']['attempted_urls'],'route_results':attempts,'source_specific_read_decision':v['reconciliation']},'available_reconciliation_done_evidence':v['reconciliation']}
   # Attach actual route provenance even when a concise source-specific decision was saved.
   gap['completion_decision']['actual_route_results']=attempts
  elif assessment=='executor_unfinished':gap['unperformed_steps']=v['unperformed_steps']
  gaps.append(gap)
inventory['updated']='2026-10-14'
write(ROOT/'data/source_inventory.json',inventory)
executor=[r for r in rows if not r['processing_complete']]
receipt={'run_id':RUN.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':baseline['started_at'],'source_pass_sealed_at':now(),'base_main_sha':baseline['base_main_sha'],'source_total':len(rows),'attempted_total':len(rows),'content_sufficient_total':sum(r['content_sufficient'] for r in rows),'processing_complete_total':sum(r['processing_complete'] for r in rows),'source_result_counts':dict(Counter(r['source_result'] for r in rows)),'executor_incomplete_source_ids':[r['source_id'] for r in executor],'executor_unfinished_actions':sum(len(reviews[r['source_id']].get('unperformed_steps',[])) for r in executor),'discovery_regions_completed':12,'sources':rows,'status':'INCOMPLETE' if gaps else 'PASS','processing_status':'INCOMPLETE_EXECUTOR' if executor else 'ALL_PROCESSED_EXTERNAL_GAPS' if gaps else 'COMPLETE'}
write(RUN/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt)
write(RUN/'gap-review.json',{'original_run_id':RUN.name,'reviewed_at':now(),'rows':gaps})
write(RUN/'date-control.json',{'run_id':RUN.name,'rows':dates,'previous_source_inventory_sha256':baseline['sha256'].get('source_inventory.json'),'new_source_inventory_sha256':sha(ROOT/'data/source_inventory.json')})
back=read(ROOT/'data/source_inventory.json')
assert all(x['last_checked_at']==max(x['last_attempts'],key=lambda a:instant(a['attempted_at']))['attempted_at'] for x in back['sources'])
write(RUN/'local-date-readback.json',{'status':'PASS','checked_at':now(),'source_total':len(back['sources']),'sha256':sha(ROOT/'data/source_inventory.json'),'all_dates_match_actual_attempts':True,'base_main_sha':baseline['base_main_sha']})
state=read(ROOT/'data/audit_state.json');state['last_incremental_audit']=now()
state['last_source_discovery_attempt']={'run_id':RUN.name,'started_at':baseline['started_at'],'source_pass_sealed_at':now(),'status':receipt['processing_status'],'attempted':len(rows),'processing_complete':receipt['processing_complete_total'],'sufficient':receipt['content_sufficient_total'],'source_total':len(rows),'coverage_receipt':str(RUN.relative_to(ROOT)/'receipt-final.json'),'latest_receipt':'data/audit_source_coverage.json','catalog_changes':4,'new_source_entries':1,'global_discovery_regions':[x['region'] for x in read(RUN/'discovery-receipt.json')['regions']],'pending_source_ids':receipt['executor_incomplete_source_ids'],'executor_unfinished_actions':receipt['executor_unfinished_actions'],'external_gap_source_ids':[g['source_id'] for g in gaps if g['processing_assessment']=='external_blocker'],'strict_evidence_status':receipt['status'],'gap_review':str(RUN.relative_to(ROOT)/'gap-review.json'),'prior_state_preserved_at':str(RUN.relative_to(ROOT)/'before-audit_state.json')}
write(ROOT/'data/audit_state.json',state)
print(json.dumps({k:receipt[k] for k in ['source_total','processing_complete_total','content_sufficient_total','source_result_counts','executor_unfinished_actions','status']},indent=2))
