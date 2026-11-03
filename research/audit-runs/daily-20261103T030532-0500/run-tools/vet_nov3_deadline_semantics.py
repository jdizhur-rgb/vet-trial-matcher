import pathlib,json,re,datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
at=datetime.datetime.now(ZoneInfo('America/New_York')).isoformat();D=rd(R/'deadline-review.json');E=[rd(p) for p in (R/'evidence').glob('*.json')];byref={e['evidence_file']:e for e in E};C={t['id']:t for t in rd(R/'baseline-trials_base.json')};done={t['trial_id']:t for t in rd(R/'completed-clinical-reviews.json')}
for row in D['rows']:
 tid=row['record_id'];row['compared_at']=at;row['excluded_date_candidates']=[]
 if tid in done:
  have={e['evidence_ref'] for e in row['current_primary_evidence']}
  for r in done[tid]['evidence_refs']:
   if r in byref and r not in have:
    e=byref[r];row['current_primary_evidence'].append({'url':e['url'],'evidence_ref':r,'original_read_at':e['completed_at'],'method':e['method']})
 if tid=='mexico-ensenada-silver-nanoparticle-cancer-2026':
  row['excluded_date_candidates']=[{**d,'exclusion_reason':'Unrelated political appointment or theater/sidebar event; not this veterinary protocol or recruitment.'} for d in row['dates']];row['dates']=[]
 if tid in ['barc-gold-nanoparticle-photothermal-2026','barc-scc-intratumoral-carboplatin-2026']:
  row['excluded_date_candidates']=[{**d,'exclusion_reason':'Anticipated September2026 opening belongs to the distinct TLR agonist program on the shared page, not this gold nanoparticle/SCC cohort.'} for d in row['dates']];row['dates']=[]
 for d in row['dates']:
  if tid=='barc-tlr789-cat-coming-soon':d['type']='anticipated_opening_not_cutoff';d['scope']='BARC TLR agonist coming-soon cohort only'
  if tid=='bluepearl-hsa-paccal':d['type']='historical_approximate_study_period_year_not_enrollment_cutoff';d['scope']='Paccal canine study; current sponsor says EnrollmentCompleted, already inactive'
  if tid=='eu-nl-cimcure-hsa-vaccine-watch':d['type']='historical_first_patient_enrollment_signal_not_cutoff'
  raw=d.get('raw_text','');matches=[]
  for p in row['current_primary_evidence']:
   if p['evidence_ref'] not in byref:continue
   e=byref[p['evidence_ref']];text=(e.get('clinical_text') or e.get('text') or '')
   if re.sub(r'\s+','',raw) in re.sub(r'\s+','',text):matches.append({'url':e['url'],'evidence_ref':e['evidence_file'],'actual_read_at':e['completed_at']})
  d['current_exact_text_confirmations']=matches
 # Previously known cutoffs absent from yesterday's ledger are retained as canonical claims, not invented fresh primary reads.
 known={'ncsu-mammary-inspire':('2027-07-01','Enrollment through July1,2027'),'ncsu-canine-sts-xcsgel':('2027-08-31','Enrollment finish August31,2027'),'ncsu-feline-oral-pivot-c':('2027-12-31','Enrollment finish December31,2027')}
 if tid in known:
  date,raw=known[tid];row['dates'].append({'raw_text':raw,'normalized_date':date,'type':'historical_canonical_enrollment_cutoff_current_primary_restricted','scope':tid,'timezone':'America/New_York; date only, no published hour','evidence_refs':[str((R/'baseline-trials_base.json').relative_to(ROOT))],'original_evidence_date':C[tid].get('verified'),'current_exact_text_confirmations':[]});row['comparison_result']='KNOWN_FUTURE_CUTOFF_CLOCK_REVIEWED_CURRENT_PRIMARY_NOT_VERIFIED'
 if tid=='ucd-prostate-liquid-treatment':row['dates'].append({'raw_text':'2017-01-08 through2019-01-08','normalized_date':'2019-01-08','type':'historical_study_period_sampling_only_not_treatment','scope':tid,'evidence_refs':[str((R/'baseline-trials_base.json').relative_to(ROOT))],'original_evidence_date':C[tid].get('verified')});row['comparison_result']='HISTORICAL_SAMPLING_STUDY_ALREADY_NONMATCHABLE_NO_REACTIVATION'
 if tid=='ncsu-feline-cancer-legacy-tissue':row['dates'].append({'raw_text':'Canonical status September30,2026 conflicts with notes enrollment09/23/2025–09/18/2027','type':'historical_conflicting_canonical_dates_nontherapeutic_sampling','scope':tid,'evidence_refs':[str((R/'baseline-trials_base.json').relative_to(ROOT))],'original_evidence_date':C[tid].get('verified')});row['comparison_result']='DIAGNOSTIC_TISSUE_ONLY_ALREADY_NONMATCHABLE_DATE_CONFLICT_NOT_USED_FOR_TREATMENT'
 row['all_known_date_semantics_reviewed_at']=at
wr(R/'deadline-review.json',D)
review=rd(R/'execution-review.json')
new=[('ucd-oral-margin','Current UC Davis public protocol API start_date2026-07-01/end_date2028-06-30 is a study-period field, while canonical notes promise Recruitment period2026-06-30 through2028-06-29. The one-day difference and enrollment-versus-study semantics are not silently corrected.','Юля: approve wording that distinguishes study period from confirmed recruitment, and resolve the one-day date interpretation without inventing a cutoff.'),('csu-brain-cart-verdinexor','Current CSU protocol API end_date2028-12-31 is a study-period field. Canonical notes say recruits through December31,2028; no explicit guaranteed enrollment cutoff is established by this generic end_date.','Юля: approve removing the guaranteed recruitment-through implication while retaining the current independently supported active cohort.')]
for tid,finding,question in new:
 iid='full_protocol:'+tid
 if any(x['issue_id']==iid for x in review['issue_updates']):continue
 es=[e for e in E if e.get('source_id')==tid];refs=[e['evidence_file'] for e in es];review['issue_updates'].append({'issue_id':iid,'trial_id':tid,'kind':'full_protocol','state':'OWNER_DECISION','reviewed_at':at,'finding':finding,'question':question,'next_action':question,'primary_url':C[tid]['url'],'previous_verified':C[tid].get('verified'),'evidence_refs':refs,'due_reason':'new_current_date_semantics_question','original_evidence_dates':[e['completed_at'] for e in es],'clinical_full_review_claimed':False})
wr(R/'execution-review.json',review);wr(R/'date-semantics-owner-questions.json',{'reviewed_at':at,'new_questions':[x for x in review['issue_updates'] if x.get('due_reason')=='new_current_date_semantics_question'],'scope':'Current page persistence and generic study-period fields never guarantee enrollment. No canonical text or public matching state changed for these owner questions.'})
print('deadline315;newownerquestions',len(new))
