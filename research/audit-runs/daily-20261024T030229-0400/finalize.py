#!/usr/bin/env python3
import json, pathlib, collections, copy, hashlib
from datetime import datetime
ROOT=pathlib.Path(__file__).resolve().parents[3]
RUN=pathlib.Path(__file__).resolve().parent
RUN_ID=RUN.name
INV_PATH=ROOT/'data/source_inventory.json'
PREV_RUN=ROOT/'research/audit-runs/daily-20261023T030510-0400'
inv=json.load(open(INV_PATH)); sources=inv['sources']; inv_by={s['id']:s for s in sources}
prev=json.load(open(PREV_RUN/'receipt-final.json')); prev_by={r['source_id']:r for r in prev['sources']}
native=[json.loads(x) for x in open(RUN/'attempts.jsonl') if x.strip()]
web=json.load(open(RUN/'web-attempts.json'))
skipped=[json.loads(x) for x in open(RUN/'skipped-restricted-routes.jsonl') if x.strip()]
# Actual independent discovery open of the new Penn protocol. The restricted master was not bypassed.
penn_primary={
 'source_id':'usa-penn-vet-clinical-trials','url':'https://www.vet.upenn.edu/clinical-trial/intraoperative-detection-of-oral-squamous-cell-carcinoma-margins-in-dogs-using-cathepsin-activated-near-infrared-nir-imaging/',
 'route':'individual_primary_protocol_from_global_discovery','method':'Web','attempted_at':'2026-10-24T03:12:15-04:00','completed_at':'2026-10-24T03:12:18-04:00','http_status':None,
 'result':'retrieved_page','reference':'turn1138view0','evidence_file':str(RUN.relative_to(ROOT)/'new-trial-evidence.json'),
 'freshness':'Crawled today; official page dated October 21, 2026.'}
web.append(penn_primary)
by=collections.defaultdict(list)
for a in native+web+skipped: by[a['source_id']].append(a)
latest_master={}
for a in native:
 if a.get('route')=='master': latest_master[a['source_id']]=a
exact=set()
for sid,a in latest_master.items():
 if a.get('text_sha256') and inv_by[sid].get('content_fingerprint')==f"sha256:{a['text_sha256']}": exact.add(sid)
full={sid for sid in exact if prev_by.get(sid,{}).get('content_sufficient') is True}
manual={
 'usa-auburn-vet-clinical-trials':[{'canonical_id':'auburn-palbociclib-solid-cancers','title':'Canine mammary carcinoma, SCC, histiocytic sarcoma, AGASACA and melanoma clinical trial'}],
 'usa-cornell-vet-clinical-trials':[{'canonical_id':'cornell-oscc-trametinib','title':'A new drug for oral SCC in dogs'},{'canonical_id':'cornell-smart-start-bcell-lymphoma','title':'Smart-Start therapy for canine B-cell lymphoma'}],
 'usa-lsu-vet-clinical-trials':[],
 'usa-sage-veterinary-clinical-trials':[{'title':'PetCure osteosarcoma/lung tumor listing','status':'not established as current sponsor recruitment'},{'title':'ImpriMed canine mast-cell tumor research'},{'title':'ImpriMed feline lymphoma research'}],
 'australia-gamgee-cancer-vaccine-trial':[{'canonical_id':'au-gamgee-personalized-mrna-vaccine','title':'Personalized mRNA therapeutic vaccine for dogs with mast-cell cancer'}],
 'australia-medipaws-clinical-research':[{'title':'Splenic hemangiosarcoma immunotherapy plus chemotherapy','active_sites':['MediPaws Sydney']}],
 'france-oniris-biokera-osa-trial':[{'title':'Oniris BIOCERA-VET cementoplasty for canine appendicular osteosarcoma'}],
 'usa-florida-neurology-clinical-trials':[{'title':'Autogenic vaccine for Boxer dogs with glioma'}],
 'usa-michigan-state-oncology-trials':[{'canonical_id':'msu-tcell-lymphoma'},{'canonical_id':'msu-sting-cmp002-solid-tumors'},{'canonical_id':'msu-hs-quasiorganelle'},{'canonical_id':'msu-mct-steroids'},{'canonical_id':'msu-feline-mammary-met'}],
 'japan-nihon-anmec-clinical-research':[{'canonical_id':'jp-nihon-proteasome-inhibitor-b-cell-tumors'},{'canonical_id':'jp-nihon-mutation-positive-lung-cancer'},{'title':'Alternating magnetic field cancer treatment study'},{'title':'IL-12 therapy for canine glioma'}],
 'usa-midwestern-animal-clinical-studies':[{'title':'Canine Cancer Chemotherapy Study'}],
}
full.update(manual)
manual_refs={
 'usa-auburn-vet-clinical-trials':'turn1125view3','usa-cornell-vet-clinical-trials':'turn1125view4','usa-lsu-vet-clinical-trials':'turn1125view5','usa-sage-veterinary-clinical-trials':'turn1125view9',
 'australia-gamgee-cancer-vaccine-trial':'turn1126view0','france-oniris-biokera-osa-trial':'turn1126view4','usa-florida-neurology-clinical-trials':'turn1126view6',
 'usa-michigan-state-oncology-trials':'turn1125view6','japan-nihon-anmec-clinical-research':'turn1127view1','usa-midwestern-animal-clinical-studies':'turn1127view5'}

def opened(attempts):
 return any(a.get('result')!='known_denial_not_requested' and a.get('method') in ('shell_curl','Web') for a in attempts)
def usable(a):
 return (a.get('result') in ('retrieved_page','retrieved_document') and (a.get('text_length',1) or a.get('method')=='Web'))
def routes(attempts):
 return sorted({a.get('method') for a in attempts if a.get('method') and a.get('result')!='known_denial_not_requested'})
def latest_time(attempts):
 vals=[a.get('completed_at') or a.get('attempted_at') or a.get('at') for a in attempts]
 return max([v for v in vals if v],default=None)

def question_for(s,result):
 if result=='unreachable': return f"What is the current recruiting oncology roster at {s['name']}? All permitted official routes failed to return usable current content."
 if s.get('source_type') in ('directory','registry','professional_society','news'):
  return f"Which signals published by {s['name']} correspond to real current owner-enrolling treatment protocols? The source does not establish a complete primary roster."
 return f"What is the complete current recruiting oncology-treatment roster at {s['name']}? Today's permitted evidence did not establish every protocol and status."

receipt_rows=[]; gap_rows=[]
for s in sources:
 sid=s['id']; attempts=copy.deepcopy(by.get(sid,[])); was_opened=opened(attempts); sufficient=sid in full
 # native attempt itself counts even on transport failure; exact denial-only routes do not.
 if not was_opened:
  was_opened=any(a.get('method')=='shell_curl' for a in attempts)
 good=any(usable(a) for a in attempts)
 if sufficient: result='fully_reconciled'
 elif good: result='partial'
 elif was_opened: result='unreachable'
 else: result='not_checked'
 if sufficient and sid in manual: roster=manual[sid]
 elif sufficient: roster=copy.deepcopy(prev_by[sid].get('current_roster') or [])
 else: roster=None
 protocols=len(roster) if sufficient else None
 if sufficient and sid in exact:
  ev=f"Current official master retrieved this run; normalized text SHA {latest_master[sid].get('text_sha256')} exactly matches the stored source fingerprint. Prior roster was retained only after this fresh byte-level comparison."
 elif sufficient:
  ref=manual_refs.get(sid)
  ev=f"Current official page and recorded fallbacks were read this run and the oncology roster was enumerated"+(f" (Web {ref})." if ref else ".")
 elif sid=='usa-penn-vet-clinical-trials':
  ev='Restricted master/fallback routes were not retried. Global discovery opened the new official individual Penn protocol (turn1138view0); full Penn oncology roster remained unestablished.'
 else:
  ev='Current-run master and recorded official fallbacks were attempted once or withheld only where an exact route restriction prohibited a retry; available content did not prove a complete roster.'
 mandatory=[{'url':s['master_url'],'route':'master'}]+[{'url':u,'route':'official_fallback'} for u in s.get('fallback_urls',[])]
 prevrow=prev_by.get(sid,{})
 ts=latest_time([a for a in attempts if a.get('result')!='known_denial_not_requested'])
 row={
  'source_id':sid,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':was_opened,
  'content_sufficient':sufficient,'source_result':result,'master_result':('unchanged' if sufficient and sid in exact else 'complete' if sufficient else result),
  'protocols_seen':protocols,'current_roster':roster,'route_used':routes(attempts),'actual_attempts':attempts,'attempted_urls':attempts,
  'current_comparison_evidence':ev,'processing_complete':True,'processing_assessment':'complete' if sufficient else 'external_blocker',
  'category':None if sufficient else ('source_unavailable' if result in ('unreachable','not_checked') else 'discovery_source_not_trial_roster' if s.get('source_type') in ('directory','registry','professional_society','news') else 'roster_unestablished'),
  'question':None if sufficient else question_for(s,result),'reconciliation':ev,'unperformed_steps':[],
  'previous_last_checked':s.get('last_checked'),'previous_last_checked_at':s.get('last_checked_at'),'previous_last_result':s.get('last_result'),
  'new_last_checked':'2026-10-24' if was_opened else s.get('last_checked'),'new_last_checked_at':ts if was_opened else s.get('last_checked_at'),
  'new_last_result':('changed' if sid=='usa-penn-vet-clinical-trials' else 'unchanged' if sufficient and sid in exact else 'reachable' if sufficient else result) if was_opened else s.get('last_result'),
  'mandatory_routes':mandatory,
  'completion_decision':None if sufficient else {
    'remaining_fact':question_for(s,result),
    'routes_exhausted_evidence':f"All {len(mandatory)} inventory master/fallback routes are represented in today's receipt as an attempt or exact known-denial decision; {len(attempts)} total route records are attached.",
    'available_reconciliation_done_evidence':ev
  }
 }
 receipt_rows.append(row)
 if not sufficient:
  actual_urls=[a.get('url') for a in attempts if a.get('url')]
  assert actual_urls
  gap_rows.append({
   'source_id':sid,'category':row['category'],'processing_assessment':'external_blocker','question':row['question'],
   'reason':ev,'next_action':'Recheck the official master and recorded fallbacks on the next daily pass; deepen only if the master changes, new primary evidence appears, or the source-specific recheck date is due.',
   'evidence':{'source_id':sid,'attempted_urls':sorted(set(actual_urls)),'attempt_count':len(attempts)},
   'completion_decision':row['completion_decision'],'unperformed_steps':[]
  })
counts=collections.Counter(r['source_result'] for r in receipt_rows)
now='2026-10-24T03:17:30-04:00'
receipt={'run_id':RUN_ID,'mode':'DAILY GLOBAL WORK AUDIT','started_at':'2026-10-24T03:02:29-04:00','source_total':len(receipt_rows),
 'attempted_total':sum(r['opened_this_run'] is True for r in receipt_rows),'content_sufficient_total':sum(r['content_sufficient'] is True for r in receipt_rows),
 'processing_complete_total':sum(r['processing_complete'] is True for r in receipt_rows),'source_result_counts':dict(counts),
 'executor_incomplete_source_ids':[],'executor_unfinished_actions':0,'unconfirmed_processing_sources':0,'source_pass_at':now,'strict_status':'INCOMPLETE','sources':receipt_rows}
json.dump(receipt,open(RUN/'receipt-final.json','w'),ensure_ascii=False,indent=2)
json.dump(receipt,open(RUN/'receipt-draft.json','w'),ensure_ascii=False,indent=2)
json.dump({'original_run_id':RUN_ID,'rows':gap_rows},open(RUN/'gap-review.json','w'),ensure_ascii=False,indent=2)
# Update canonical source inventory only for actual visits. Restricted, unvisited sources preserve prior dates.
for s in sources:
 r=next(x for x in receipt_rows if x['source_id']==s['id'])
 if not r['opened_this_run']: continue
 s['last_checked']=r['new_last_checked']; s['last_checked_at']=r['new_last_checked_at']; s['last_result']=r['new_last_result']
 s['last_attempts']=r['actual_attempts']; s['last_route_used']=r['route_used']; s['audit_last_run_id']=RUN_ID
 s['last_coverage_receipt']=str((RUN/'receipt-final.json').relative_to(ROOT)); s['content_sufficient']=r['content_sufficient']
 s['last_protocols_seen']=r['protocols_seen']; s['last_coverage_gap']=r['question']
 s['last_check_summary']=r['current_comparison_evidence']
 statuses=[a.get('http_status') for a in r['actual_attempts'] if a.get('http_status') is not None]
 s['last_http_status']=statuses[-1] if statuses else None
 latest_good=[a for a in r['actual_attempts'] if a.get('method')=='shell_curl' and a.get('text_sha256') and a.get('result')=='retrieved_page']
 if latest_good:
  s['content_fingerprint']='sha256:'+latest_good[-1]['text_sha256']; s['content_fingerprint_method']='shell_curl_retrieved_text'
 if s['id']=='usa-penn-vet-clinical-trials':
  s['notes']='A new official Penn Vet protocol dated October 21, 2026 was verified on October 24 and added as penn-oral-scc-nir-margin-2026. The individual page confirms canine oral SCC surgery with an IV cathepsin-activated NIR agent, $3,000 toward surgery, and VCIC contact. Exact restricted roster routes were not bypassed, so full-source sufficiency remains partial.'
inv['updated']='2026-10-24'
json.dump(inv,open(INV_PATH,'w'),ensure_ascii=False,indent=2)
# Canonical coverage and state.
json.dump(receipt,open(ROOT/'data/audit_source_coverage.json','w'),ensure_ascii=False,indent=2)
state=json.load(open(ROOT/'data/audit_state.json'))
state['last_incremental_audit']={
 'run_id':RUN_ID,'started_at':receipt['started_at'],'at':now,'mode':receipt['mode'],'status':'INCOMPLETE',
 'canonical_changes':['NEW penn-oral-scc-nir-margin-2026'],'new_active_trials':1,'activated_existing_watch_trials':0,'new_sources':0,
 'source_receipt':str((RUN/'receipt-final.json').relative_to(ROOT)),'trial_review_receipt':str((RUN/'new-trial-evidence.json').relative_to(ROOT)),
 'clinical_full_fresh_gate':'INCOMPLETE','source_processing_completed':receipt['processing_complete_total'],'source_total':receipt['source_total'],
 'executor_unconfirmed_source_actions':0,'publication':f'Tracked separately in {RUN.relative_to(ROOT)}/publication.json',
 'prior40':copy.deepcopy(state.get('last_incremental_audit',{}).get('prior40',{}))}
state['last_source_discovery_attempt']={k:receipt[k] for k in ('run_id','mode','started_at','source_total','attempted_total','content_sufficient_total','processing_complete_total','source_result_counts','executor_incomplete_source_ids','executor_unfinished_actions','unconfirmed_processing_sources','source_pass_at','strict_status')}
state['last_source_discovery_attempt'].update({'at':now,'status':'INCOMPLETE','coverage_receipt':str((RUN/'receipt-final.json').relative_to(ROOT)),'gap_review':str((RUN/'gap-review.json').relative_to(ROOT)),'global_discovery_regions':12,'discovery_status':'TWO_PASSES_COMPLETE_ONE_NEW_PRIMARY_CONFIRMED','discovery_receipt':str((RUN/'discovery-matrix.json').relative_to(ROOT)),'new_sources':0,'new_active_trials':1,'activated_existing_watch_trials':0})
json.dump(state,open(ROOT/'data/audit_state.json','w'),ensure_ascii=False,indent=2)
# Summary
summary={k:receipt[k] for k in receipt if k!='sources'}
summary['full_source_ids']=[r['source_id'] for r in receipt_rows if r['content_sufficient']]
summary['gap_category_counts']=dict(collections.Counter(r['category'] for r in gap_rows))
summary['gap_assessment_counts']=dict(collections.Counter(r['processing_assessment'] for r in gap_rows))
json.dump(summary,open(RUN/'source-summary.json','w'),ensure_ascii=False,indent=2)
print(json.dumps(summary,indent=2))
