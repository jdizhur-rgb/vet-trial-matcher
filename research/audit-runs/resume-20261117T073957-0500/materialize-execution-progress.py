"""Prepare current durable accounting; no prior attempt is credited as a new visit."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import json,sys,hashlib
r=Path(sys.argv[1]); old=Path('research/audit-runs/daily-20261117T030023-0500')
def load(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ref(k):return str(r/k)
def key(u):return hashlib.sha256(u.encode()).hexdigest()[:20]
def evidence(u):
 for folder in ('evidence','structured','pdf-ocr'):
  p=r/folder/(key(u)+'.json')
  if p.exists():return str(p),load(p)
 return None,None
b=load(r/'execution-baseline.json'); earlier=load(r/'morning-accounting/execution-review.json')
queue={i['issue_id']:i for i in b['issues']}
review=load(r/'execution-review.json')
dates=load(r/'confirmed-protocol-reviews.json')
working=load(r/'unfinished-protocol-plan.json')
independent=load(r/'missing-independent-plan.json')
coverage=load(r/'receipt-progress.json')
decisions=load(r/'source-decisions-progress.json')
at=datetime.now(ZoneInfo('America/New_York')).isoformat()
catalog={x['id']:x for x in load(Path('data/trials_base.json'))}
exact_gaps={
 'eu-ch-large-tumor-lattice-sbrt':('Current clinical page confirms dog eligibility and five randomized visits; whether earlier funding terms remain valid requires its exact restricted PDF. Cat generic header does not broaden protocol.', ['evidence/af16ea15fa638d9f65e6.json','evidence/4c7679ff9ee73849f0d3.json']),
 'ch-zurich-feline-oscc-flash-proton-rt':('Current protocol confirms three sessions and hospital/PSI responsibilities, but current page only states reduced price; exact held flyer is needed for the coproportion explicitly stored.', ['evidence/118bc72c9be46c47b6c5.json','evidence/bcf1911c4f86004a7d97.json']),
 'taiwan-protect-pt001-oral-melanoma':('Eight exact listed sites manually matched. October 2025 notice lacks a cutoff or costs, and current site enrollment and cost sharing are unpublished.', ['evidence/8fc101495f13cfc62c6e.json','web-additional-source-leads.json']),
 'uk-liverpool-dogfight-glioma-ferumoxytol-rt':('Investigator still lists this exact intervention and distinguishes two prior cohorts. No currently stated site-level admission, eligibility cutoff or funding on permitted university pages.', ['evidence/b5603cc64a9c09af2918.json','web-additional-source-leads.json']),
 'uk-edinburgh-oral-melanoma-tigilanol-tiglate':('Current university clinical programme has historical research links only; still no current intake, eligibility or coverage for exact tigilanol oral melanoma cohort.', ['evidence/c8e43af41d7600c96430.json','web-later8.json']),
 'csu-osa-carboplatin-pain':('Exact registry VCT22005582 confirmed completed; secondary mirror recruiting does not establish any continuing enrollment. No new dated clinical review.', ['lead-remaining-avma-transport.txt']),
 'osu-sts-mic-nk':('Same Shay Bracha anti-MIC/NK study in both official sources. Current HTML says $700 and 2025-12-17 PDF says $800 on completion; do not silently overwrite existing value.', ['evidence/d939dae51905f6432474.json','evidence/54ae4877092cd6544c6f.json']),
}
new=[]
for item in queue.values():
 tid=item['trial_id']; iid=item['issue_id']; row={**item,'reviewed_at':at,'previous_issue_reviewed_at':item.get('reviewed_at'),'full_protocol_review_complete':False}
 valid_evs=[evidence(u) for u in dict.fromkeys((independent.get(tid) or [])+(working.get(tid) or [])+[item.get('primary_url') or catalog[tid].get('url','')]) if u]
 valid_evs=[(rp,o) for rp,o in valid_evs if o]
 held=[(rp,o) for rp,o in valid_evs if o.get('restriction')]
 retrieved=[(rp,o) for rp,o in valid_evs if o.get('result')=='retrieved']
 plan=ref('unfinished-protocol-plan.json')
 if tid=='anivive-sine-osa-carboplatin' and iid.startswith('full_protocol'):
  p=ref('evidence/cornell-sine-avma-vct24005828.json')
  row.update(state='POLICY_RESOLVED',finding='Exact Cornell VCT24005828 concluded; removed from matching. Status-only review.',evidence_refs=[p],resolved_scope='current_access',policy_resolution={'rule':'avma_closed','avma_vct_code':'VCT24005828','registry_status':'Completed','evidence_refs':[p],'identity_comparison':'Kelly Hume/Cornell, post-amputation SINE/verdinexor plus carboplatin for canine appendicular osteosarcoma, exact VCT24005828.'})
 elif tid in exact_gaps:
  f,rr=exact_gaps[tid]; pp=[ref(z) for z in rr if (r/z).exists()]
  row.update(state='BLOCKED',finding=f,evidence_refs=pp,restriction_or_unpublished_evidence_refs=pp,question=item.get('question') or 'Confirm the missing clinical terms described in finding.',next_action='Use a newly published permitted exact protocol or dated corroboration; preserve original verification until then.')
 elif held and (tid in independent or not retrieved):
  refs=[rp for rp,_ in held]+['data/source_access_restrictions.json']
  row.update(state='BLOCKED',finding='Reviewed exact saved hold on '+ '; '.join(o['url'] for _,o in held)+'. No request was sent by the held route; did not convert prior record or index into a full review.',evidence_refs=refs,restriction_or_unpublished_evidence_refs=refs,question=item.get('question') or 'Confirm five clinical fields for this exact trial.',next_action='Check an independently published official alternate for the identical trial; do not retry listed holds.')
 else:
  row.update(state='OPEN_AVAILABLE',finding=('Current transport artifacts exist for '+', '.join(o['url'] for _,o in retrieved)+'. Full disposition is pending; transport is not factual sufficiency.' if retrieved else 'No current individual clinical disposition recorded for this remaining issue. Exact issue retained, with prior evidence dates preserved.'),evidence_refs=[rp for rp,_ in valid_evs] or [plan,ref('execution-baseline.json')],question=item.get('question') or 'Confirm five clinical fields for this exact trial.',next_action='Read the exact primary document and applicable official alternate, compare the disputed facts and write the actual outcome.')
 new.append(row)
ids={x['issue_id'] for x in new}
for d in dates:
 tid=d['trial_id']; f=ref('confirmed-protocol-reviews.json')
 for kind in ('full_protocol','independent_selection'):
  iid=kind+':'+tid
  row={'issue_id':iid,'kind':kind,'trial_id':tid,'state':'RESOLVED','reviewed_at':d['reviewed_at'] if kind=='full_protocol' else d['independent_case_tested_at'],'finding':'The named exact current primary protocol and the independently generated selection case outcomes are recorded with per-record dates and proof.','evidence_refs':[f]}
  if kind=='full_protocol':row.update(facts_checked=d['facts_checked'],full_protocol_review_complete=True)
  else:row.update(cases_checked=['positive','negative','unknown'],evidence_refs=[f,ref('independent-results.json')])
  if iid in ids:new=[x for x in new if x['issue_id']!=iid]
  new.append(row)
review.update(source_reviews=decisions,issue_updates=new,discovery_queries=earlier['discovery_queries'],discovered_urls=earlier['discovered_urls'],leads=earlier['leads'],deadline_review_ref=ref('deadline-continuation-latest.json'),ended_at=None)
review['predecessor_discovery_provenance']=str(old/'discovery-query-evidence.ndjson')
review['updated_at']=at
write(r/'execution-review.json',review)
