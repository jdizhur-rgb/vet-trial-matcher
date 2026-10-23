from daily23 import *
import collections,hashlib
D=read(RUN/'discovery-ledger.json');review=read(RUN/'primary-lead-review.json');rel=str(RUN.relative_to(ROOT))
groups={
'EXCLUDED_HISTORICAL_DOCUMENT_RESEARCH_NOT_CURRENT_ACCESS':[36,37,38,178,219,332,694,755],
'EXCLUDED_DIAGNOSTIC_SAMPLE_OR_PREDICTION_SERVICE':[88,93,96,151,649,677,681,682,689,690,693,710],
'EXCLUDED_CARE_GENERAL_EDUCATION_JOBS_OR_FINANCIAL_AID':[101,157,159,547,577,598,623,641,652,667,715,718,737,750,756,772],
'KNOWN_INSTITUTION_PROTOCOL_OR_PUBLISHED_RESULT_NO_NEW_INTAKE':[90,97,134,181,226,228,231,299,321,616,673,692,702,708,730,738,739,749,752,764]
}
manual={i:k for k,ii in groups.items() for i in ii};decisions=[]
for i,r in enumerate(D['leads']):
 if r['disposition']=='NEEDS_FINAL_CONTEXT_REVIEW' and i in manual:
  r.update(disposition=manual[i],reason='Exact returned title/date/full available search context explicitly reviewed in this immutable URL map. '+{'EXCLUDED_HISTORICAL_DOCUMENT_RESEARCH_NOT_CURRENT_ACCESS':'Dated CV, old institutional flyer/report, published case results, historical study update or all-status registry announcement, not current enrollment.','EXCLUDED_DIAGNOSTIC_SAMPLE_OR_PREDICTION_SERVICE':'Imaging, biobanking, drug-response prediction, liquidbiopsy or canineolfaction; no anticancer therapeutic trial invitation.','EXCLUDED_CARE_GENERAL_EDUCATION_JOBS_OR_FINANCIAL_AID':'Care/services, education, staff advert, advice, general history or retiredworkingdog financialaid; outside current therapeutic-trial discovery.','KNOWN_INSTITUTION_PROTOCOL_OR_PUBLISHED_RESULT_NO_NEW_INTAKE':'Programme identity compared with today institutional source evidence and retained specific questions. ICAT is JSAMC already freshly read; past UQ immunotherapy/news and Vivesto completion not new trials. UC Davis fluorophore-bound study is current679907, whose complete individual public protocol was read. No alias/snippet used as fresh primary proof.'}[manual[i]])
  decisions.append(dict(index=i,url=r['url'],title=r['title'],disposition=r['disposition'],evidence=r['search_hits'][0]['evidence'],reason=r['reason']))
remaining=[dict(index=i,title=r['title'],url=r['url']) for i,r in enumerate(D['leads']) if r['disposition']=='NEEDS_FINAL_CONTEXT_REVIEW'];assert not remaining,remaining
D['summary'].update(executor_unadjudicated_returned_urls=0,dispositions=dict(collections.Counter(r['disposition'] for r in D['leads'])),reviewed_at=now(),qualification_limit='All returned signals screened; actual permitted primary requests performed for new/ambiguous candidate facts. Restricted/unavailable primary clinical papers and unpublished current access remain unresolved; no claim all clinical evidence confirmed.')
write(RUN/'discovery-ledger.json',D);review['final_context_url_decisions']=decisions;review['ledger_url_dispositions']=[dict(index=i,url=r['url'],disposition=r['disposition']) for i,r in enumerate(D['leads'])];write(RUN/'primary-lead-review.json',review)
write(RUN/'discovery-primary-notes.json',dict(at=now(),reviews=[dict(signal='UF LSD1',facts='Full official page explicitly Enrollment Paused despite generic currentlyrecruiting introduction. RadiationSOC before oralLSD1, samplebeforeRT, noothermajorillness, fundedbiopsies/drug/studyvisits/$1000adverseevents; ownerinitialdiagnosis/nonstudycare. Not a new active cohort; no merger with CSU watch from shareddrugclass.',url='https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/'),dict(signal='Morris oral cancer',facts='Full officialD15FE020researchaward: COMPLETE,startOctober1,2014,UniversityMinnesotaErinDickerson,$102469,2019MCT1/4inhibitorpublication. Completed research grant, not present owner trial or confirmed closure of anothercanonical.',url='https://www.morrisanimalfoundation.org/study/investigating-new-treatment-oral-cancers')],no_new_active_records=True))
for r in review['reviews']:
 if r['signal_id']=='uf-lsd1':r.update(disposition='PRIMARY_EXPLICITLY_PAUSED',primary_facts='Full official individual page says Enrollment Paused despite generic recruiting intro. No new active record or institution merger; detailed criteria/costs in discovery-primary-notes.json.',remaining_question=None)
 if r['signal_id']=='morris-oral':r.update(disposition='EXCLUDED_COMPLETED_2014_RESEARCH_GRANT',primary_facts='Full primary D15FE020, startOctober2014, COMPLETE; 2019MCT1/4paper. Not current trial.',remaining_question=None)
write(RUN/'primary-lead-review.json',review)
print(D['summary']);print('explicit final contexts',len(decisions))
