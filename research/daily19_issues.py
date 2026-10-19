"""Preserve inherited unresolved history, dates and due dates; no automatic closure."""
from daily19 import ROOT,RUN,OLD,read,write,now
import copy,json
cat={r['id']:r for r in read(ROOT/'data/trials_base.json')};old=read(OLD/'issues.json');rows=copy.deepcopy(old['issues'])
for r in rows:
 r['inherited_from_run']=OLD.name;r['not_a_new_primary_visit']=True;r['daily_queue_reentry']=False
 r['current_record_states']=[{k:cat[tid].get(k) for k in ['id','available_for_matching','status','status_confidence','verified','funding_verified']} for tid in r.get('record_ids',[]) if tid in cat]
 r['historical_public_before_after_fields_not_current_snapshot']=True
 if 'penn-anti-pd1-urothelial-carcinoma' in r.get('record_ids',[]):
  r['current_access_disposition']='Confirmed closed by exact sponsor/AVMA identity; retained site-page conflict. Detailed historical eligibility is not newly reviewed.'
  r['current_access_evidence']=['vgs002-completed-amendment.json','vgs002-site-conflict.json'];r['owner_action_required']=False
for iid,question,ev in [('apavac-commercial-access-evidence','Does current commercial MARS APAVAC access have sufficient independent protocol-level clinical evidence and published owner costs for treatment-access inclusion? Not an enrolling trial.','web-05-leads.json'),('hokkaido-feline-aml-azacitidine','Does the2026 feline AML/azacitidine project currently invite owner enrollment, and under which intervention, eligibility, funding and contact? Programme title alone is not a patient protocol.','receipt-final.json')]:
 rows.append({'issue_id':iid,'kind':'discovery_watch','question':question,'first_seen':'2026-10-19','recorded_at':now(),'evidence':str((RUN/ev).relative_to(ROOT)),'decision':'watch_not_matchable','owner_action_required':False,'daily_queue_reentry':False,'recheck_after':'2026-10-26','next_action':'Specific deeper read on new primary protocol/content signal or due date; daily master visits remain mandatory. No outreach.'})
write(RUN/'issues.json',{'run_id':RUN.name,'recorded_at':now(),'inherited_issue_count':len(old['issues']),'inherited_dates_and_due_dates_preserved':True,'original_issue_file':str((OLD/'issues.json').relative_to(ROOT)),'separate_from_daily_traversal_queue':True,'issues':rows})
write(RUN/'segment-research-publication.json',{'run_id':RUN.name,'at':now(),'immutable_segment':True,'source_processing':'119/120; one Cambridge alias NOT VERIFIED','source_sufficiency':'56fully_reconciled/47partial/2unreachable/15not_checked','discovery':'85queries,12regions,bothpasses; primary signal adjudication retained','clinical_full_fresh_gate_remaining':33,'publication_data_commit':'99d76c53051bda21c88da3bd46dd46caff250a39','production_byte_readback':'PASS','live_searches':read(RUN/'live-search-evidence.json'),'pending_work':'Receipt bookkeeping/result parity correction and final report preservation/readback; not another source traversal.','budget':'Before06:00 America/New_York; deploy wait bounded10minutes.'})
print('inherited issues',len(old['issues']),'new watches2; original dates and due dates retained')
