"""Publish one owner-approved upcoming protocol with literal primary criteria."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, subprocess

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
ID='illinois-fam010-splenic-hemangiosarcoma'
URL='https://familiartx.com/studies/fam-010'
path=ROOT/'data/trials_base.json'
rows=read(path)
assert ID not in {r['id'] for r in rows}, 'Do not append the same protocol twice'
assert not [r for r in rows if 'fam-010' in json.dumps(r).lower() or 'familiartx.com/studies/fam-010' in json.dumps(r).lower()]
(RUN/'before-trials_base.json').write_bytes(path.read_bytes())
record={
 'id':ID,
 'title':'FAM-010 chemotherapy for canine splenic hemangiosarcoma — enrolling soon',
 'center':'University of Illinois Veterinary Teaching Hospital',
 'country':'USA','state':'Illinois','species':'Dog','cancers':['Hemangiosarcoma'],
 'study_type':'treatment','available_for_matching':True,
 'status':'Enrolling soon; study inquiries accepted through the sponsor form. Confirm the next dose-group opening with the study team.',
 'status_confidence':'current',
 'status_confidence_basis':'Current published protocol and observed functioning inquiry form; owner explicitly approved this upcoming listing. This does not confirm that treatment enrollment is open.',
 'recruitment_status':'enrolling_soon',
 'url':URL,
 'contacts':'Use Contact the study team on the official Familiar study page. The form connects eligible inquiries with the Illinois team; confirm when a dose group can start.',
 'funding_status':'Study care funded; travel owner-paid',
 'funding':'Familiar covers study screening, FAM-010 treatment and study follow-up care. Owners pay travel to and from Urbana. Coverage of the preceding splenectomy or unrelated care is not specified.',
 'funding_source':URL,'funding_verified':'2026-10-23','verified':'2026-10-23','protocol_reviewed_at':now(),
 'intervention':'Investigational albumin-linked doxorubicin (FAM-010), given by intravenous infusion every three weeks. Six treatments are planned initially; some dogs may receive up to twelve. All study dogs receive FAM-010; no placebo.',
 'treatments':['Chemotherapy','Experimental drug'],
 'treatment_approaches':['chemotherapy'],
 'requires':{
  'splenic_primary':True,
  'planned_doxorubicin':True,
  'eligible_cohorts':[
   {'surgery':['Yes'],'prior_procedure':['Splenectomy']},
   {'required_preferences':['Surgery']}
  ]
 },
 'excludes':{'prior_chemo':True,'prior_local_radiation':True},
 'owner_prescreen_required':True,
 'special_requirement':'Enrollment is announced as enrolling soon; ask about the next dose group before arranging care. Splenic hemangiosarcoma must be confirmed by pathology before joining, but owners awaiting results or with splenectomy scheduled may inquire now. The first dose must be possible within 21 days after splenectomy. No previous chemotherapy, radiation or other investigational drug; no intended breeding. Regular Urbana visits are required. This initial study establishes dose and side effects; improved survival and reduced heart toxicity are not established. Permanent infertility is expected in intact male dogs.',
 'notes':'FAM-010 links doxorubicin to albumin to investigate whether drug delivery and heart safety can be improved. This first canine study focuses on dose and tolerability; it does not establish better survival or cardiac safety. Eligible dogs have splenic hemangiosarcoma and recent or planned splenectomy. Pathology can be pending at inquiry but must confirm the diagnosis before enrollment. The first dose must fit within 21 days after surgery; entry may be delayed between small dose groups. Previous chemotherapy, radiation or another investigational drug excludes entry. Dogs intended for breeding are excluded; permanent infertility is expected in intact males. The sponsor covers study screening, drug treatment and study follow-up; travel is owner-paid, and prior surgery coverage is not stated.',
 'sites':[{'hospital':'University of Illinois Veterinary Teaching Hospital','name':'University of Illinois Veterinary Teaching Hospital','city':'Urbana','state':'IL','source_url':URL}],
 'sponsor':'Familiar Therapeutics',
 'protocol_id':'FAM-010',
 'owner_publication_decision':{'date':'2026-10-23','instruction':'Публикуй урбану','scope':'Publish this dose-finding protocol as an upcoming opportunity with the sponsor inquiry route and explicit uncertainty disclosures. Not a blanket exception for future pipeline or safety-only programs.','evidence':str((RUN/'primary-review.json').relative_to(ROOT))}
}
rows.append(record);write(path,rows)
base=read(RUN/'before-trials_base.json')
assert all(a==b for a,b in zip(base,rows[:-1])) and len(rows)==len(base)+1
cases=[]
def add(name,patient,expected='review',terms=None):
 c={'name':name,'patient':dict(species='Dog',country='USA',cancer='Hemangiosarcoma',**patient),'expected':expected}
 if terms:c['unknown_contains']=terms
 cases.append(c)
add('post-splenectomy candidate, no previous systemic treatment',{'hsa_site':'Spleen','surgery':'Yes','prior_procedure':'Splenectomy','chemo':'Never','radiation':'Never'},terms=['21 days','enrolling soon'])
add('pathology pending may inquire',{'diagnosis_status':'Suspected / not confirmed','surgery':'Yes','prior_procedure':'Splenectomy'},terms=['pathology'])
add('scheduled splenectomy inquiry before surgery',{'surgery':'No','prefs':['Surgery','Chemotherapy']},terms=['splenectomy'])
add('surgery already completed does not require accepting a second operation',{'surgery':'Yes','prior_procedure':'Splenectomy','prefs':['Chemotherapy']})
add('no prior surgery and surgery declined',{'surgery':'No','prefs':['Chemotherapy']},'exclude')
add('other surgery does not establish splenectomy when surgery declined',{'surgery':'Yes','prior_procedure':'Other','prefs':['Chemotherapy']},'exclude')
add('other previous surgery with planned splenectomy requires review',{'surgery':'Yes','prior_procedure':'Other','prefs':['Surgery','Chemotherapy']})
add('cardiac hemangiosarcoma excluded',{'hsa_site':'Heart / right atrium'},'exclude')
add('other non-splenic primary excluded',{'hsa_site':'Other'},'exclude')
add('previous chemotherapy excluded',{'chemo':'Previously received'},'exclude')
add('current chemotherapy excluded',{'chemo':'Currently receiving'},'exclude')
add('previous radiation excluded',{'radiation':'Previously received'},'exclude')
add('current radiation excluded',{'radiation':'Currently receiving'},'exclude')
add('chemotherapy declined',{'prefs':['Surgery','Immunotherapy']},'exclude')
add('unknown site and history remain screening questions',{},terms=['splenic','21 days','infertility'])
for name,changes in [('wrong species',{'species':'Cat'}),('wrong country',{'country':'Japan'}),('different sarcoma',{'cancer':'Histiocytic sarcoma'})]:
 c=dict(species='Dog',country='USA',cancer='Hemangiosarcoma');c.update(changes);cases.append({'name':name,'patient':c,'expected':'exclude'})
baseline=read(ROOT/'data/protocol_selection_baseline.json')
signature=hashlib.sha256(json.dumps({k:record.get(k) for k in baseline['signature_fields']},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
review={'trial_id':ID,'source_url':URL,'reviewed_at':now(),'criteria':'Current individual sponsor protocol: splenic canine HSA, splenectomy completed or scheduled, first dose within21days, no previous chemo/radiation/other investigational drugs, no breeding. Pathology may be pending at inquiry. Owner approves upcoming dose-finding listing; functioning inquiry form observed, not confirmed open treatment enrollment.','cases':cases,'selection_sha256':signature}
p=ROOT/'data/protocol_selection_cases.json';d=read(p);assert ID not in {r['trial_id'] for r in d['reviews']};d['reviews'].append(review);write(p,d)
write(RUN/'record.json',record)
write(RUN/'primary-review.json',dict(reviewed_at=now(),primary_urls=[URL,'https://familiartx.com/pipeline'],Web_references=['turn1124view0','turn1124view1'],native_shell='Three connect-timeout attempts, actual receipts preserved. Same URLs read by Web; browser independently verified the live inquiry form.',status='Owner-approved upcoming public listing; not confirmed open dose-group enrollment.',contact_route='Contact the study team opens a three-step inquiry form, step1 name/email/phone/ZIP and consent; observed2026-10-23T10:21:31.570Z. No information entered or sent.',institution_index='Supporting Illinois index does not yet name FAM-010. Sponsor is the direct protocol and enrollment-inquiry primary.',owner_scope='Specific owner request to publish after reading dose/safety and enrolling-soon limitations; no other inactive program promoted.',dedupe='Full canonical311 reviewed by protocol id, sponsor, intervention, site, diagnosis and source. No FAM-010 identity; other Illinois and splenic-HSA protocols have different interventions.',unpublished=['Exact start date and next open dose group','Histologic/metastatic and organ-function criteria not stated beyond public page','Coverage of prior splenectomy and unrelated care'],no_inference=['No demonstrated survival or heart-toxicity advantage','No blanket no-cost surgery','No submission, contact or enrollment performed'],source_review=review))
print('ADDED',ID,'canonical',len(rows),'independent cases',len(cases),'selection SHA',signature)
