"""Mechanical assembly preserves manual decisions and actual visit provenance."""
import json,hashlib,collections
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2];TZ=ZoneInfo('America/New_York')
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=lambda:datetime.now(TZ).isoformat()
inv=read(ROOT/'data/source_inventory.json')['sources'];before=read(P/'before-source_inventory.json')['sources'];base=read(P/'baseline.json');reviews={x['source_id']:x for x in read(P/'reviews.json')}
assert len(reviews)==len(inv)==111
browser=read(P/'browser-observations.json')['rows'];pet=read(P/'browser-pettrials.json');browser.append({'source_id':pet['source_id'],'url':pet['url'],'method':'browser_DOM','route':'actual_rendered_trial_cards','attempted_at':pet['observed_at_browser_utc'],'result':'retrieved_page','evidence_file':str((P/'browser-pettrials.json').relative_to(ROOT)),'text_length':None,'reconciliation':pet['note']})
for x in browser:
 x.setdefault('evidence_file',str((P/'browser-observations.json').relative_to(ROOT)));x['text_sha256']=hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest();x['new_visit_this_run']=True
write(P/'browser-attempts.json',browser)
native=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()];actual=native+read(P/'web-attempts.json')+browser
prior=read(ROOT/'research/audit-runs/finalize-68-20261014T185109-0400/receipt-final.json');priorrows={x['source_id']:x for x in prior['sources']}
denials=read(ROOT/'research/audit-runs/finalize-68-20261014T185109-0400/inherited-denials.json')
rows=[]
for s,b in zip(inv,before):
 sid=s['id'];urls={s['master_url']}|set(s.get('fallback_urls',[]));a=[dict(x,new_visit_this_run=True,visit_origin_run_id=P.name) for x in actual if x['source_id']==sid or x['url'] in urls];a.sort(key=lambda x:datetime.fromisoformat(x['attempted_at']))
 inherited=[]
 if not a:
  inherited=[dict(x,new_visit_this_run=False,inherited_denial=True,not_retried_this_run=True) for x in b.get('last_attempts',[])]
  inherited += [dict(x,method='historical_denial_record',new_visit_this_run=False,inherited_denial=True,not_retried_this_run=True) for x in denials if x['source_id']==sid and not any(t['url']==x['url'] for t in inherited)]
 row={**reviews[sid],'source_name':s.get('name',sid),'master_url':s['master_url'],'opened_this_run':bool(a),'attempted_urls':a+inherited,'route_used':sorted({x['method'] for x in a}),'master_result':'reachable' if reviews[sid]['content_sufficient'] else reviews[sid]['source_result'],'original_source_id_preserved':True}
 for f in ('last_checked','last_checked_at','last_result','content_fingerprint'):
  row['previous_'+f]=b.get(f);row['new_'+f]=s.get(f)
 row['historical_fingerprint_preserved_not_roster_proof']=b.get('content_fingerprint')==s.get('content_fingerprint');row['current_content_comparison_evidence']=reviews[sid]['reconciliation'];rows.append(row)
discoveryfiles=sorted(P.glob('discovery-*.json'));matrix={}
for f in discoveryfiles:
 d=read(f)
 for q in d.get('queries',[]):matrix.setdefault(q[0],{}).setdefault(d['pass'],[]).append({'language':q[1],'query':q[2],'evidence_file':str(f.relative_to(ROOT)),'actual_requested_at':d['at']})
required=['USA','Canada','UK','Europe','LatinAmerica','AustraliaNZ','EastAsia','SouthAsia','SoutheastAsia','MiddleEast','NorthAfrica','SubSaharanAfrica']
assert all('current_undated' in matrix[k] and 'fresh_7_days' in matrix[k] for k in required)
write(P/'discovery-matrix.json',{'run_id':P.name,'completed_at':now(),'regions_completed':12,'passes':2,'fresh_window_start':'2026-10-08','matrix':matrix,'limits':'Actual searches performed; recency filters sometimes return old documents/current recrawls. Publication dates checked, recrawl dates never treated as new studies. No exhaustive absence claim.'})
counts=dict(collections.Counter(x['source_result'] for x in rows));unfinished=[x['source_id'] for x in rows if not x.get('processing_complete')]
receipt={'run_id':P.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':base['started_at'],'source_pass_sealed_at':now(),'base_main_sha':base['base_main_sha'],'source_total':111,'attempted_total':sum(x['opened_this_run'] for x in rows),'content_sufficient_total':sum(x['content_sufficient'] for x in rows),'processing_complete_total':sum(x.get('processing_complete') is True for x in rows),'source_result_counts':counts,'executor_incomplete_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'discovery_regions_completed':12,'discovery_matrix':str((P/'discovery-matrix.json').relative_to(ROOT)),'sources':rows,'status':'INCOMPLETE','processing_status':'ALL_PROCESSED_EXTERNAL_GAPS' if not unfinished else 'EXECUTOR_INCOMPLETE'}
write(P/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt)
gaps=[]
for x in rows:
 if x['content_sufficient']:continue
 gaps.append({'source_id':x['source_id'],'category':x['category'],'processing_assessment':x['processing_assessment'],'question':x['question'],'reason':x['reconciliation'],'next_action':x['next_action'],'completion_decision':x.get('completion_decision',{}),'evidence':{'source_id':x['source_id'],'attempted_urls':list(dict.fromkeys(a['url'] for a in x['attempted_urls']))}})
write(P/'gap-review.json',{'original_run_id':P.name,'reviewed_at':now(),'rows':gaps})
state=read(ROOT/'data/audit_state.json');state['last_incremental_audit']=now();state['last_source_discovery_attempt']={'run_id':P.name,'started_at':base['started_at'],'source_pass_sealed_at':receipt['source_pass_sealed_at'],'status':receipt['processing_status'],'source_total':111,'attempted':receipt['attempted_total'],'processing_complete':receipt['processing_complete_total'],'sufficient':receipt['content_sufficient_total'],'coverage_receipt':str((P/'receipt-final.json').relative_to(ROOT)),'latest_receipt':'data/audit_source_coverage.json','catalog_changes':0,'new_source_entries':0,'global_discovery_regions':required,'pending_source_ids':unfinished,'executor_unfinished_actions':len(unfinished),'external_gap_source_ids':[x['source_id'] for x in gaps],'gap_review':str((P/'gap-review.json').relative_to(ROOT)),'issues':str((P/'issues.json').relative_to(ROOT))};write(ROOT/'data/audit_state.json',state)
# Preserve all unresolved issue identities/history; no automatic closure on method changes.
issues=read(P/'issues.json') if (P/'issues.json').exists() else read(ROOT/'research/audit-runs/finalize-68-20261014T185109-0400/issues.json');issues['run_id']=P.name;issues['reviewed_at']=now();issues['prior_issue_file']='research/audit-runs/finalize-68-20261014T185109-0400/issues.json';issues['preservation_note']='Original unresolved IDs/first-seen/dates retained. Source-scope recovery is not automatic clinical issue closure. New questions below are separate from completed daily queue.'
existing={x['issue_id'] for x in issues['issues']}
new=[('leah-missouri-cohort-current-intake','P0',[inv[11]['id'],inv[93]['id']],['leah-bcell-cart-2026'],'Missouri changed enrolling cohort (>10kg/72h/seven visits21days) versus UMN hold and sponsor three-site invitation; current site/cohort not reconciled. Preserve existing Ohio-only matching.'),('jhu-if7-sn38-current-intake','P2',[inv[7]['id']],[],'Undated IF7-SN38 brain/metastatic labels share one primary PDF; actual current owner intake/funding not established.'),('jsamc-suizenji-hifu-primary-protocol','P2',[inv[69]['id']],[],'Bare HIFU dog/cat malignant-tumour heading has no public individual protocol/criteria/funding; not a new active trial.'),('ghent-nanobody-versus-flim-protocol-identity','P2',[inv[100]['id']],[],'Clarify distinct nanobody head/neck surgical fluorescence invitation versus existing FLIM ICG protocol; avoid semantic duplicate.'),('murdoch-solid-tumour-immunotherapy-coming-soon','P2',[inv[48]['id']],[],'PetTrials COMING SOON/TBC2026 points to generic internal-medicine service, not current individual enrollment.')]
for iid,impact,sids,rids,q in new:
 if iid not in existing:issues['issues'].append({'issue_id':iid,'impact':impact,'source_ids':sids,'record_ids':rids,'question':q,'remaining_fact':q,'first_seen':now(),'last_reviewed':now(),'recheck_after':'2026-10-22','decision':'unresolved','evidence':[{'file':'reviews.json','source_ids':sids}],'daily_queue_reentry':False})
write(P/'issues.json',issues)
# Measure actual native overlaps; do not conceal historical runner batching deviations.
events=[]
for a in native:
 events.extend([(a['attempted_at'],1),(a['completed_at'],-1)])
events.sort();n=0;peak=0
for t,delta in events:n+=delta;peak=max(peak,n)
write(P/'execution-compliance.json',{'native_request_count':len(native),'native_peak_overlap':peak,'global_limit':6,'batch_lock_added':'approximately03:59EDT; subsequent native batches serialized','immutable_segment_cadence_note':'Segment04 was recorded later than 15 minutes after segment03. No timestamps backdated.','source_ids_preserved':111,'current_catalog_unchanged':(ROOT/'data/trials_base.json').read_bytes()==(P/'before-trials_base.json').read_bytes()})
print('RECEIPT',receipt['attempted_total'],counts,'gaps',len(gaps),'executor',len(unfinished),'native_peak',peak)
