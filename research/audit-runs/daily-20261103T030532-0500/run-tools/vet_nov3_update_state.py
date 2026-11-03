import json,pathlib,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
at=datetime.now(ZoneInfo('America/New_York')).isoformat();rec=rd(R/'receipt-final.json');I=rd(R/'baseline-source_inventory.json');S={x['source_id']:x for x in rec['sources']};dates=[]
for s in I['sources']:
 d=S[s['id']];old={k:s.get(k) for k in ['last_checked','last_checked_at','last_result','content_fingerprint']}
 if d['opened_this_run']:
  s.update(last_checked=d['new_last_checked'],last_checked_at=d['new_last_checked_at'],last_result='reachable' if d['content_sufficient'] else d['master_result'],last_attempts=d['attempted_urls'],last_route_used=d['route_used'],notes=d['finding'],last_check_summary=d['finding'],last_coverage_gap=None if d['content_sufficient'] else d['catalog_comparison'])
  if d['current_evidence_sha256']:s['content_fingerprint']='sha256:'+d['current_evidence_sha256'];s['fingerprint_method']='Digest of hashes of actual current retrieved native documents; not proof of roster or clinical review.'
  http=[a for a in d['attempted_urls'] if a.get('http_status') and a.get('new_source_visit')]
  if http:
   h=max(http,key=lambda x:x['completed_at']);s['last_http_status']=h['http_status'];s['last_http_status_at']=h['completed_at']
 s.update(last_audit_run_id=R.name,last_processing_review_at=at,last_coverage_receipt=str((R/'receipt-final.json').relative_to(ROOT)),last_protocols_seen=d['protocols_seen'],content_sufficient=d['content_sufficient'],processing_complete=d['processing_complete'],last_current_review_finding=d['finding'])
 dates.append({'source_id':s['id'],'previous':old,'new':{k:s.get(k) for k in old},'actual_new_visit':d['opened_this_run'],'restriction_review_only':not d['opened_this_run'],'evidence_refs':[a['evidence_file'] for a in d['attempted_urls']]})
I['updated']='2026-11-03';wr(ROOT/'data/source_inventory.json',I);wr(R/'source-date-readback-local.json',{'at':at,'rows':dates,'source_inventory_sha256':hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),'pass':all(x['actual_new_visit'] or x['previous']==x['new'] for x in dates)})
wr(ROOT/'data/audit_source_coverage.json',rec)
state=rd(ROOT/'data/audit_state.json');state['last_incremental_audit']={'run_id':R.name,'started_at':rec['started_at'],'at':at,'mode':rec['mode'],'receipt':str((R/'receipt-final.json').relative_to(ROOT)),'execution_review':str((R/'execution-review.json').relative_to(ROOT)),'content_sufficient_total':rec['content_sufficient_total'],'source_total':157,'processing_complete_total':rec['processing_complete_total'],'status':'INCOMPLETE','scope':'Current source traversal, full daily deadline comparison, global country/language discovery and five due full protocol reviews; unresolved access/clinical/owner issues retained.'};state['last_source_discovery_attempt']={'run_id':R.name,'at':at,'regions':12,'queries':148,'countries':75,'languages':38,'status':'INCOMPLETE','lead_ledger':str((R/'lead-decisions.json').relative_to(ROOT))};state['protocol_selection_review']['last_current_run_id']=R.name;state['protocol_selection_review']['current_full_reviews_ref']=str((R/'completed-clinical-reviews.json').relative_to(ROOT));wr(ROOT/'data/audit_state.json',state)
# Keep known explicit cutoff separate from record-title synonyms.
dl=rd(R/'deadline-review.json')
for x in dl['rows']:
 if x['record_id']=='ncsu-canine-ucc-il12':x['comparison_result']='EXPIRED_2026_09_30_NO_PRIMARY_EXTENSION_CONFIRMED';x['question']='Exact primary extension of Enrollment Finish09/30/2026 remains not confirmed; generic index/registry Recruiting cannot extend this cohort.'
 if x['record_id']=='jp-tokyo-feline-tcc-lapatinib':x['comparison_result']='PRIMARY_FULLY_ENROLLED_AND_RESEARCH_ENDED_2026_10_31_INACTIVE_PRESERVED'
wr(R/'deadline-review.json',dl)
print('Source dates preserved for restriction-only',sum(not x['actual_new_visit'] for x in dates),'updated realvisits',sum(x['actual_new_visit'] for x in dates))
