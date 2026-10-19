"""Exact sponsor closure; preserve historical clinical/funding verification dates."""
from daily19 import ROOT,RUN,read,write,now
import json,copy
from pathlib import Path
cat=read(ROOT/'data/trials_base.json');tid='penn-anti-pd1-urothelial-carcinoma';r=next(r for r in cat if r['id']==tid);before=copy.deepcopy(r)
assert r['available_for_matching'] is True
attempts=[json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]
a=next(x for x in attempts if x['route']=='new_official_master' and 'vetigenics.com/' in x['url'])
text=read(ROOT/a['evidence_file'])['text'];assert 'PD-1 (VGS-002)' in text and 'Ethos Veterinary Health – Closed' in text and 'Bridge Animal Referral Center (BARC) – Closed' in text
identity='Fully canine anti-PD1, urothelial carcinoma, Nicola Mason/Ethos coordination, and exact CASE Boulder plus VSH-North County San Marcos treating sites match the sponsor November2,2023 protocol identity. This is VGS-002, not Purdue anti-PDL1/AKS-701d, not CHECKMATE-K9 combination therapy, and not commercial antibody access. Current sponsor lists BOTH VGS-002 provider groups Ethos and BARC as Closed; historical institution invitation is retained as provenance, not current recruitment.'
r.update(available_for_matching=False,status_confidence='confirmed_enrollment_closed',status='Enrollment closed — VGS-002 sponsor lists Ethos and BARC as Closed',status_source=a['url'],status_verified_at=a['attempted_at'],status_decision_at=now(),status_decision_note=identity)
assert r['verified']==before['verified'] and r['funding_verified']==before['funding_verified']
write(ROOT/'data/trials_base.json',cat)
write(RUN/'vgs002-closure.json',{'trial_id':tid,'identity_reconciliation':identity,'source_attempt':a,'primary_identity_url':'https://vetigenics.com/latest-news/first-canine-patient-receives-vetigenics-fully-canine-anti-ctla4-monoclonal-antibody-for-oral-melanoma/','prior_institution_route_not_retried':'Saved explicit gate; current independent sponsor evidence, not circumvention of the institutional gate.','before':before,'after':r,'clinical_eligibility_rereview_complete':False,'disposition':'CLOSED_CONFIRMED (enrollment only; not a claim that follow-up/study analysis is complete)','independent_negative_cases':[{'name':'Otherwise nominal dog bladder cohort','patient':{'species':'Dog','country':'USA','cancer_type':'Urothelial / transitional cell carcinoma','weight_known':True,'weight_kg':20},'expected':'exclude'},{'name':'Browse mode must not resurrect closed enrollment','patient':{'species':'Dog','country':'USA','cancer_type':'Cancer — any type'},'expected':'exclude'},{'name':'Unknown medical answers do not override closed intake','patient':{'species':'Dog','country':'USA','cancer_type':'Bladder cancer'},'expected':'exclude'}]})
print('Confirmed exact VGS-002 enrollment closure applied; historical criteria and dates retained.')
