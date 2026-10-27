"""Apply individually read primary decisions, never infer completion from retrieval."""
import copy
import hashlib
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PARENT = ROOT / 'research/audit-runs/daily-20261026T030132-0400'
def read(p): return json.loads(p.read_text())
def write(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
at = datetime.now(ZoneInfo('America/New_York')).isoformat()
day = at[:10]
attempts = [json.loads(x) for x in (RUN/'attempts.jsonl').read_text().splitlines()]
old = read(PARENT/'receipt-final.json')
catalog = read(ROOT/'data/trials_base.json')
write(RUN/'before-trials_base.json', catalog)
by_id = {r['id']: r for r in catalog}
source_facts = {
 'usa-auburn-vet-clinical-trials': {
   'roster': ['auburn-palbociclib-solid-cancers'],
   'facts': ['The saved Ongoing Clinical Trials section contains exactly one named oncology protocol, with the direct official palbociclib link.', 'Fresh full protocol confirms five canine tumor groups, measurable progressive disease, allowed prior therapy, owner-paid initial screening and up to two months funded treatment; contact onco@auburn.edu.', 'The dose-finding purpose is retained explicitly; no new broader Phase I inclusion exception is made.'],
   'scope': 'One published oncology protocol; full protocol reread and canonical comparison completed.'},
 'usa-cornell-vet-clinical-trials': {
   'roster': ['cornell-oscc-trametinib','cornell-smart-start-bcell-lymphoma'],
   'facts': ['The saved current canine roster contains two oncology treatment protocols: oral SCC and Smart-Start B-cell lymphoma; other named trials concern non-oncology conditions, stem-cell treatment or pain management.', 'Fresh oral-SCC protocol confirms daily trametinib, visits through day 126, free study drug/visits/procedures and $1,000 standard-care credit on completion.', 'Fresh Smart-Start protocol confirms B-cell lymphoma, no prior treatment except prednisolone, mandatory CHOP, assigned pretreatment/no placebo, 10% standard-care discount and $1,000 chemotherapy support.'],
   'scope': 'Both published oncology protocols fully reread; exact URLs, costs, eligibility and contact match canonical.'},
 'usa-illinois-clinical-trials': {
   'roster': ['illinois-daunomustine-multicentric-lymphoma','illinois-oral-melanoma-il12-il15','ill-osa-il12-rt-current','illinois-osa-sbrt-dc-homing-hydrogel','ill-osa-z007-current','illinois-sts-surgery','illinois-sts-treatment','illinois-ucc-gilvetmab-epacadostat'],
   'facts': ['The saved Oncology section links eight distinct current protocols, and all eight exact linked PDFs were freshly read in full.', 'Kept separate OSA cohorts: JEN-101 plus radiation with mandatory amputation and up to $2,500 surgery support; SBRT/DC-homing hydrogel without mandatory amputation; Z-007 for pulmonary metastases.', 'Kept separate STS cohorts: resectable tumor 1–5 cm plus surgery at Illinois, and previously excised recurrent STS >2 cm with six-week chemo/radiation washout.', 'Confirmed daunomustine untreated peripheral-node multicentric lymphoma, oral-melanoma IL12/IL15 with radiation, and bladder UCC gilvetmab/epacadostat with cytology OR BRAF plus visible bladder mass.', 'All eight funding, contact and treatment-backbone statements compared to full canonical records. FAM-010 remains a separate sponsor-listed upcoming protocol; absence from this university index is not closure evidence.'],
   'scope': 'Eight current master-linked protocols reread and reconciled; no new treatment identity or eligibility change.'},
 'usa-lsu-vet-clinical-trials': {
   'roster': [],
   'facts': ['The saved Clinical Trials page enumerates a healthy-dog dermatitis/heavy-metal sampling study and puppy osteopathy/vaccination research; neither is oncology treatment.', 'The exposed official Oncology navigation was freshly followed; it describes medical/radiation clinical services, named staff and patient appointments, but no named recruiting trial or extra current-trial link.', 'Zero is limited to oncology trials on these published routes, not a claim that no unpublished LSU research exists. Historical nonmatchable LSU records are preserved.'],
   'scope': 'Published index and exposed oncology route reconciled; verified zero published oncology protocol on these routes.'},
 'australia-gamgee-cancer-vaccine-trial': {
   'roster': ['au-gamgee-personalized-mrna-vaccine'],
   'facts': ['Fresh official page explicitly says Trial now recruiting, Australia, and names one personalized mRNA vaccine trial for dogs with mast cell cancer.', 'Registration is interest/prescreening, not guaranteed enrollment; existing veterinary care continues. No osteosarcoma cohort is published.', 'Exact funding/medical screening details remain for the authorized study team; the canonical card already discloses unknown costs. No invented protocol detail or new full-protocol verification date.'],
   'scope': 'One published owner-interest protocol reconciled; no exhaustive multicenter hospital list is published here.'},
 'japan-university-of-tokyo-vmc-clinical-research': {
   'roster': ['jp-tokyo-histiocytic-sarcoma-anti-pd1-2026','jp-tokyo-organoid-guided-targeted-therapy-2026','jp-tokyo-canine-bladder-ido1-inhibitor','jp-tokyo-macromolecular-pirarubicin-solid-tumors'],
   'facts': ['Read all seven listed clinical-research sections: one non-oncology enteropathy study and six oncology identities, including two explicitly recruitment-completed studies.', 'Four current treatment invitations remain: canine HS anti-PD1, dog/cat organoid-guided targeted therapy, canine bladder IDO1 inhibitor and canine polymer-pirarubicin. Published species, excluded hematologic disease, sampling, visit schedule, drug funding and contacts match canonical.', 'Feline lapatinib section explicitly says target enrollment reached and trial ends October 31, 2026; paid use of the drug remains available. The older canine bladder/prostate study explicitly ended December 1, 2021 and is not a new active trial.', 'The exact fresh shell page repeats the closure notice already present in the morning snapshot. Web reader returned an older version without the feline closure notice; that discrepant cache is retained as freshness conflict, not used to override explicit organizer closure.'],
   'scope': 'Whole published research page reconciled; four active protocol identities, one newly corrected completed-enrollment record, one historical closed canine protocol excluded.'},
}
reviews=[]
for sid, fact in source_facts.items():
 inherited = next(r for r in old['sources'] if r['source_id']==sid)
 evidence = inherited['actual_attempts'] + [a for a in attempts if a['source_id']==sid]
 evidence_files = sorted({a['evidence_file'] for a in evidence if a.get('evidence_file')})
 reviews.append({'source_id':sid,'reviewed_at':at,'processing_complete':True,'decision':'resolved_verified','current_roster':fact['roster'],'protocols_seen':len(fact['roster']),'observed_facts':fact['facts'],'reconciliation':fact['scope'],'inherited_run_id':old['run_id'],'evidence_files':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in evidence_files],'unperformed_steps':[]})
write(RUN/'reviews.json',reviews)

full_ids = source_facts['usa-auburn-vet-clinical-trials']['roster']+source_facts['usa-cornell-vet-clinical-trials']['roster']+source_facts['usa-illinois-clinical-trials']['roster']+source_facts['japan-university-of-tokyo-vmc-clinical-research']['roster']
trial_reviews=[]
for tid in full_ids:
 t=by_id[tid]; before=copy.deepcopy(t)
 fresh=[a for a in attempts if a['url']==t['url'] or tid.startswith('jp-tokyo-') and a['source_id']=='japan-university-of-tokyo-vmc-clinical-research']
 assert fresh,tid
 t['verified']=day
 t['protocol_reviewed_at']=at
 if t.get('funding_status')!='Contact center':t['funding_verified']=day
 trial_reviews.append({'trial_id':tid,'reviewed_at':at,'scope':['current access','species/disease','eligibility','treatment/backbone','published funding','contact','site'],'primary_attempts':fresh,'before':before,'after':copy.deepcopy(t),'clinical_changes':[]})

t=by_id['jp-tokyo-feline-tcc-lapatinib']; before=copy.deepcopy(t)
t.update(available_for_matching=False,status_confidence='closed',recruitment_status='fully_enrolled',status='Target enrollment reached; trial scheduled to end October 31, 2026. Paid lapatinib treatment remains available through Tokyo.',verified=day,protocol_reviewed_at=at)
t['notes'] += ' The current official organizer notice states that the target case count has been reached and the trial will end on October 31, 2026. It separately offers drug use at owner expense. Preserve this as treatment-access information, not an open recruiting study; no separate access record is created without evaluating that category.'
t['status_source']=t['url'];t['status_verified_at']=at
trial_reviews.append({'trial_id':t['id'],'reviewed_at':at,'decision':'confirmed_enrollment_complete','primary_attempts':[a for a in attempts if a['source_id']=='japan-university-of-tokyo-vmc-clinical-research'],'inherited_missed_evidence':'research/audit-runs/daily-20261026T030132-0400/evidence/c5412abb663bd2b441.json','web_conflict':'turn1165view0 omitted the feline closure paragraph; cached reader version retained as conflict','before':before,'after':copy.deepcopy(t)})
write(RUN/'trial-reviews.json',trial_reviews)
write(ROOT/'data/trials_base.json',catalog)

# Historical morning files remain immutable. This documentary amendment preserves
# original attempt timestamps and withdraws unsupported completion assertions.
corrected=copy.deepcopy(old)
corrected['finalized_by_run_id']=RUN.name
corrected['amended_at']=at
corrected['mode']='TARGETED GAP RECOVERY / DOCUMENTARY AMENDMENT'
for row in corrected['sources']:
 sid=row['source_id']; row['inherited_visit_run_id']=old['run_id']
 if row['content_sufficient']:continue
 extra=[a for a in attempts if a['source_id']==sid]
 row['actual_attempts']+=extra;row['attempted_urls']+=extra
 if sid in source_facts:
  fact=source_facts[sid]
  row.update(processing_complete=True,processing_assessment='complete',content_sufficient=True,source_result='fully_reconciled',master_result='reconciled',protocols_seen=len(fact['roster']),current_roster=fact['roster'],current_comparison_evidence=' '.join(fact['facts']),reconciliation=fact['scope'],unperformed_steps=[],completion_decision=None,question=None)
  row['individual_review']=str((RUN/'reviews.json').relative_to(ROOT))
 else:
  row.update(processing_complete=False,processing_assessment='not_established',completion_decision=None)
  row['unperformed_steps']=['Independently inspect retrieved body and exposed navigation; reconcile real protocol identities and record effects before assigning terminal completion.']
corrected['processing_complete_total']=sum(r['processing_complete'] for r in corrected['sources'])
corrected['content_sufficient_total']=sum(r['content_sufficient'] for r in corrected['sources'])
corrected['unconfirmed_processing_sources']=sum(r['processing_assessment']=='not_established' for r in corrected['sources'])
corrected['executor_incomplete_source_ids']=[r['source_id'] for r in corrected['sources'] if not r['processing_complete']]
corrected['executor_unfinished_actions']=None
corrected['executor_unfinished_note']='At least one required independent reconciliation per unconfirmed source; exact action total is not yet established.'
from collections import Counter
corrected['source_result_counts']=dict(Counter(r['source_result'] for r in corrected['sources']))
write(RUN/'receipt-final.json',corrected)
gaps=read(PARENT/'gap-review.json')
gaps['finalized_by_run_id']=RUN.name
gaps['rows']=[g for g in gaps['rows'] if g['source_id'] not in source_facts]
for g in gaps['rows']:
 g.update(processing_assessment='not_established',completion_decision=None,reason='The prior automatic external-blocker/completion assertion lacks an individual semantic review. Preserved attempts establish retrieval/restriction history only.',next_action='Inspect the saved source content and exposed permitted official navigation, map protocol identity to canonical records, then record a source-specific terminal decision.',unperformed_steps=['Individual content, navigation and canonical reconciliation.'])
write(RUN/'gap-review.json',gaps)
write(ROOT/'data/audit_source_coverage.json',corrected)
inventory=read(ROOT/'data/source_inventory.json')
for s in inventory['sources']:
 sid=s['id']
 if sid not in source_facts: continue
 row=next(r for r in corrected['sources'] if r['source_id']==sid)
 fresh=[a for a in attempts if a['source_id']==sid]
 if fresh:
  latest=max(a['completed_at'] for a in fresh)
  s['last_checked']=latest[:10];s['last_checked_at']=latest
  s['last_attempts']=row['actual_attempts']
  row['new_last_checked']=latest[:10];row['new_last_checked_at']=latest
 s['last_result']='changed' if 'tokyo' in sid else 'unchanged';row['new_last_result']=s['last_result']
 s['last_coverage_receipt']=str((RUN/'receipt-final.json').relative_to(ROOT))
 s['content_sufficient']=True;s['last_protocols_seen']=len(source_facts[sid]['roster'])
 s['last_coverage_gap']=None;s['last_check_summary']=' '.join(source_facts[sid]['facts'])
 s['audit_last_run_id']=RUN.name
write(ROOT/'data/source_inventory.json',inventory)
write(RUN/'receipt-final.json',corrected)
write(ROOT/'data/audit_source_coverage.json',corrected)
state=read(ROOT/'data/audit_state.json')
state['last_gap_recovery']={'run_id':RUN.name,'at':at,'parent_run_id':old['run_id'],'reviewed_sources':list(source_facts),'confirmed_enrollment_complete':['jp-tokyo-feline-tcc-lapatinib'],'unconfirmed_processing_sources':corrected['unconfirmed_processing_sources'],'status':'INCOMPLETE'}
state['last_incremental_audit']['completion_claim_superseded_by']=RUN.name
state['last_incremental_audit']['processing_completion']='NOT_VERIFIED'
state['last_incremental_audit']['unconfirmed_processing_sources']=corrected['unconfirmed_processing_sources']
write(ROOT/'data/audit_state.json',state)
print(json.dumps({'reviewed_sources':len(reviews),'full_protocol_reviews':len(trial_reviews),'unconfirmed_processing_sources':corrected['unconfirmed_processing_sources'],'original_full_retained_not_independently_reaudited':47}))
