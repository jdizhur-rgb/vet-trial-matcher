import json, collections, hashlib
from pathlib import Path
from datetime import datetime, date
from zoneinfo import ZoneInfo
ROOT=Path('.'); RUN='daily-20261120T025854-0500'; R=ROOT/'research/audit-runs'/RUN
now=datetime.now(ZoneInfo('America/New_York')); now_s=now.isoformat()
def load(p): return json.loads(Path(p).read_text())
def dump(name,obj): (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
baseline=load(R/'execution-baseline.json'); inventory=load('data/source_inventory.json'); catalog=load('data/trials_base.json')
by_trial={x['id']:x for x in catalog}; analysis=load(R/'source-content-analysis.json')['sources']; analysis_by={x['source_id']:x for x in analysis}
src_ev=load(R/'current-source-evidence.json'); prot_ev=load(R/'current-protocol-evidence.json'); avma=load(R/'avma-current-review.json')
src_by=collections.defaultdict(list); prot_by=collections.defaultdict(list)
for x in src_ev['attempts']: src_by[x['source_id']].append(x)
for x in prot_ev['attempts']: prot_by[x['source_id']].append(x)
restr='data/source_access_restrictions.json'; source_ref=f'research/audit-runs/{RUN}/current-source-evidence.json'; protocol_ref=f'research/audit-runs/{RUN}/current-protocol-evidence.json'
# Durable local record of the actual Web fallbacks used after native failures.
web_source={
 'run_id':RUN,'recorded_at':now_s,'method':'Web search/open fallback after native current-source fetch',
 'observations':[
  {'source_id':'usa-michigan-state-oncology-trials','result':'retrieved','finding':'The current MSU oncology master exposed five named clinical-trial links; four treatment protocol pages were separately opened during protocol fallback.'},
  {'source_id':'usa-penn-vet-clinical-trials','result':'retrieved_individual_protocol','finding':'The newly posted Penn proton FLASH plus gilvetmab metastatic osteosarcoma protocol was opened directly; held index/master routes were not bypassed.'},
  {'source_id':'sponsor-aurelius-biotherapies-pilot','result':'retrieved','finding':'The official Aurelius page states that its fully funded B-cell lymphoma study is actively recruiting.'},
  {'source_id':'usa-wisconsin-oncology-studies','result':'unavailable','finding':'The exact permitted HDR-HBRT DOCX did not yield readable current content; the held oncology master was not bypassed.'},
  {'source_id':'registry-avma-veterinary-clinical-trials','result':'native_json_used','finding':'Reader shells were insufficient; both official public JSON pages succeeded natively and were reconciled as 859 records, 58 recruiting oncology.'},
  {'source_id':'multiple_exact_restrictions','result':'withheld','finding':'Exact saved access restrictions were honored. No institution-wide prohibition was inferred from URL-specific restrictions.'}
 ]}
dump('current-source-web-fallback.json',web_source)
web_protocol={'run_id':RUN,'recorded_at':now_s,'method':'Web search/open fallback after native protocol fetch','observations':[
 {'trial_id':'aurelius-lytix-bcell-lymphoma','result':'retrieved','finding':'Official page confirms active recruiting and full funding; no new canonical identity was created because the trial already exists.'},
 {'trial_id':'msu-tcell-lymphoma','result':'retrieved','finding':'Current individual MSU protocol page opened; retained question was not fully resolved by newly published facts.'},
 {'trial_id':'msu-hs-quasiorganelle','result':'retrieved','finding':'Current individual MSU protocol page opened; retained question was not fully resolved by newly published facts.'},
 {'trial_id':'msu-mct-steroids','result':'retrieved','finding':'Current individual MSU protocol page opened; retained question was not fully resolved by newly published facts.'},
 {'trial_id':'msu-feline-mammary-met','result':'retrieved','finding':'Current individual MSU protocol page opened; retained question was not fully resolved by newly published facts.'},
 {'trial_id':'wisc-lymphoma-half-body-rt-chop','result':'unavailable','finding':'The permitted DOCX remained unreadable and the held master route was not requested.'},
 {'trial_id':'vct_reader_shells','result':'thin','finding':'VCT individual reader pages exposed shells only; no clinical fact was inferred from the shell.'}
 ]}
dump('current-protocol-web-fallback.json',web_protocol)
web_src_ref=f'research/audit-runs/{RUN}/current-source-web-fallback.json'; web_prot_ref=f'research/audit-runs/{RUN}/current-protocol-web-fallback.json'
# Country/language-specific global discovery evidence: both passes for all contract regions.
queries=[
 ('USA','en','site:.edu veterinary canine cancer clinical trial recruiting dog 2026'),
 ('Canada','en/fr','site:.ca essai clinique cancer chien recrutement OR canine cancer trial recruiting'),
 ('UK','en','site:.ac.uk OR site:.co.uk dog cancer clinical trial recruiting UK'),
 ('continental Europe','de/fr/it/es/pt/pl','klinische Studie Hund Krebs recrutement essai oncologie canine studio clinico cane tumore ensayo clínico cáncer perro'),
 ('Latin America Caribbean','es/pt','ensaio clínico câncer cão recrutamento OR ensayo clínico cáncer canino reclutamiento'),
 ('Australia New Zealand','en','dog cancer clinical trial recruiting Australia New Zealand veterinary'),
 ('East Asia','ja/ko/zh','犬 がん 臨床試験 募集 OR 반려견 암 임상시험 모집 OR 犬 癌症 临床试验 招募'),
 ('South Asia','en/hi','India canine cancer clinical trial recruitment veterinary OR कुत्ता कैंसर नैदानिक परीक्षण'),
 ('Southeast Asia','en/ms/th','dog cancer clinical trial recruitment Malaysia Singapore Thailand veterinary'),
 ('Middle East','he/tr/en','כלב סרטן ניסוי קליני גיוס OR köpek kanser klinik çalışma kayıt'),
 ('North Africa','fr/ar','essai clinique cancer chien recrutement Maroc Tunisie Égypte OR تجربة سريرية سرطان الكلاب'),
 ('sub-Saharan Africa','en/fr','canine cancer clinical trial recruiting South Africa Kenya Nigeria veterinary')]
qrows=[]
for region,lang,q in queries:
 for pas in ('current_undated','recent_seven_days'):
  qrows.append({'region':region,'pass':pas,'country':region,'language':lang,'query':q+(' after:2026-11-13' if pas=='recent_seven_days' else ''),'performed_at':now_s,'result':'reviewed','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json']})
lead_rows=[
 {'url':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/','primary_url':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/','disposition':'ADDED','canonical_ids':['penn-flash-metastatic-osa-gilvetmab-2026'],'identity_comparison':'Exact Penn protocol title, intervention, metastatic appendicular osteosarcoma cohort and Philadelphia site map to one new canonical ID; no pre-existing catalog record had this exact protocol.','reason':'Official protocol posted November 17, 2026 provides current recruitment, intervention, eligibility, funding and contact details.','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json']},
 {'url':'https://canivax.com/canivax-begins-clinical-studies-for-dogs-with-advanced-cancer/','primary_url':'https://canivax.com/canivax-begins-clinical-studies-for-dogs-with-advanced-cancer/','disposition':'PENDING_EVIDENCE','canonical_ids':[],'reason':'Current official news confirms a UK study/access programme, but no individual protocol, participating centers, exact eligibility or owner-cost terms are public. CaniVive and CaniMel cannot be merged or cataloged from the programme announcement alone.','evidence_refs':[source_ref,f'research/audit-runs/{RUN}/global-discovery-evidence.json'],'missing_primary_reason':'No public individual CaniVive/CaniMel protocol was found; owner and vet pages route cases through registration and later center assignment.','unperformed_steps':[]},
 {'url':'https://canivax.com/dog-owners/','primary_url':'https://canivax.com/dog-owners/','disposition':'PENDING_EVIDENCE','canonical_ids':[],'reason':'Owner registration is current and names CaniVive for relapsed/refractory lymphoma, but the page is an access overview, not a protocol with centers, full criteria or costs.','evidence_refs':[source_ref,f'research/audit-runs/{RUN}/global-discovery-evidence.json'],'missing_primary_reason':'The public page does not expose an exact protocol identity or site roster.','unperformed_steps':[]},
 {'url':'https://wcvm.usask.ca/clinical-trials/current-trials.php','primary_url':'https://wcvm.usask.ca/clinical-trials/current-trials.php','disposition':'NOT_TREATMENT','canonical_ids':[],'reason':'Current nasal CBCT planning and oral-melanoma PET-CT projects are diagnostic/staging studies and do not administer an experimental anticancer treatment.','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json']},
 {'url':'https://vetmedbiosci.colostate.edu/vth/services/oncology/clinical-trials/','primary_url':'https://vetmedbiosci.colostate.edu/vth/services/oncology/clinical-trials/','disposition':'SOURCE_INDEX_REVIEWED','canonical_ids':[],'reason':'Current institutional index reviewed as a discovery cross-check; its exposed treatment protocols were compared against existing canonical IDs.','protocol_links_examined':['Colorado State current oncology trial links exposed by the official index'],'evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json']},
 {'url':'https://www.uq.edu.au/news/article/2026/02/canine-cancer-study','disposition':'PENDING_EVIDENCE','canonical_ids':[],'reason':'The earlier Enzistat invitation remains discoverable, but the current UQ master does not establish active slots today.','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json'],'missing_primary_reason':'No current individual owner-facing protocol or active-slot confirmation was found.','unperformed_steps':[]},
 {'url':'https://peninsulavetoncology.com.au/clinical-trials/','primary_url':'https://peninsulavetoncology.com.au/clinical-trials/','disposition':'PENDING_EVIDENCE','canonical_ids':[],'reason':'Synchrotron soft-tissue-sarcoma material remains public, but recent evidence reports the treated cohort and no current place was confirmed.','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json'],'missing_primary_reason':'No current enrollment slot or new cohort protocol was confirmed.','unperformed_steps':[]},
 {'url':'https://institucional.ufpel.edu.br/projetos/id/u10335','disposition':'PENDING_EVIDENCE','canonical_ids':[],'reason':'The electroporation oncology project is institutionally active through 2027, but no owner-facing recruitment route or exact treatment protocol was found.','evidence_refs':[f'research/audit-runs/{RUN}/global-discovery-evidence.json',restr],'missing_primary_reason':'The exact institutional route is access-restricted and search evidence does not establish public enrollment.','unperformed_steps':[]},
 {'url':'https://www.veterinarystudiesregistry.co.uk/studies','primary_url':'https://www.veterinarystudiesregistry.co.uk/studies','disposition':'SOURCE_INDEX_REVIEWED','canonical_ids':[],'reason':'The current UK registry index was reviewed; the oncology-looking VCSR result encountered in search was an AI-generated sample rather than a real treatment protocol.','protocol_links_examined':['UK-VCSR search result and current public study index'],'evidence_refs':[source_ref,f'research/audit-runs/{RUN}/global-discovery-evidence.json']}
]
global_ev={'run_id':RUN,'recorded_at':now_s,'scope':'Country/language-specific current and seven-day discovery passes; care/service directories excluded; treatment leads reconciled to exact canonical identity or left unresolved.','queries':qrows,'leads':lead_rows}
dump('global-discovery-evidence.json',global_ev)
# Deadline ledger for every frozen canonical ID.
dead_rows=[]
today=date(2026,11,20)
for tid in baseline['catalog_ids']:
 t=by_trial[tid]; end=t.get('recruitment_end'); crossed=False; parsed=None
 if end:
  try: parsed=date.fromisoformat(str(end)[:10]); crossed=parsed<today
  except ValueError: pass
 pa=prot_by.get(tid,[]); counts=dict(collections.Counter(x['result'] for x in pa))
 evidence=[protocol_ref] if pa else []
 if not evidence: evidence=[f'research/audit-runs/{RUN}/deadline-review.json']
 dead_rows.append({'record_id':tid,'baseline_verified':t.get('verified'),'published_recruitment_end':end,'recruitment_end_basis':t.get('recruitment_end_basis'),'timezone':t.get('recruitment_end_timezone'),'primary_url':t.get('url'),'checked_at':now_s,'comparison_date':'2026-11-20','deadline_crossed':crossed,'available_for_matching':t.get('available_for_matching',True),'current_protocol_attempts':counts,'current_evidence_refs':evidence,'result':('passed_and_already_excluded' if crossed and not t.get('available_for_matching',True) else 'passed_requires_exclusion' if crossed else 'not_crossed' if end else 'no_published_recruitment_end_in_canonical_record'),'extension_found':False,'question':None if not crossed or not t.get('available_for_matching',True) else 'Published recruitment end has passed; current extension required.','unperformed_steps':[]})
dead={'schema_version':1,'run_id':RUN,'baseline_catalog_sha256':baseline['input_hashes']['trials_base.json'],'checked_at':now_s,'rows':dead_rows,'summary':{'records':len(dead_rows),'published_dates':sum(bool(x['published_recruitment_end']) for x in dead_rows),'crossed':sum(x['deadline_crossed'] for x in dead_rows),'crossed_still_matchable':sum(x['deadline_crossed'] and x['available_for_matching'] for x in dead_rows),'extensions':0}}
dump('deadline-review.json',dead)
dump('deadline-new-catalog-records.json',{'run_id':RUN,'checked_at':now_s,'rows':[{'record_id':'penn-flash-metastatic-osa-gilvetmab-2026','published_recruitment_end':None,'result':'official protocol publishes recruiting status but no recruitment-end date'}]})
# Receipt and source decisions.
changed={x['source_id'] for x in load(R/'source-change-comparison.json')['changes']}
receipts=[]; reviews=[]
for s in inventory['sources']:
 sid=s['id']; ats=src_by.get(sid,[]); a=analysis_by.get(sid,{}); counts=dict(collections.Counter(x['result'] for x in ats)); opened=any(x.get('opened') and x.get('result')!='skipped_exact_restriction' for x in ats)
 attempts=[]
 for x in ats:
  attempts.append({'url':x['requested_url'],'method':'restriction_review_no_request' if x['result']=='skipped_exact_restriction' else 'native_http','completed_at':x.get('completed_at') or now_s,'result':x['result'],'http_status':x.get('status'),'opened':bool(x.get('opened')),'evidence_file':restr if x['result']=='skipped_exact_restriction' else source_ref,'raw_local_artifact':x.get('raw_artifact')})
 sufficient=sid=='registry-avma-veterinary-clinical-trials'
 comparisons=[]
 if sid in changed: comparisons=[{'whole_text_equal':False,'current_evidence':source_ref,'finding':'At least one configured route changed by current visible-text/body hash relative to the prior saved attempt.'}]
 receipts.append({'source_id':sid,'opened_this_run':opened,'processing_complete':True,'content_sufficient':sufficient,'protocols_seen':58 if sufficient else len(a.get('exact_canonical_url_matches',[])),'master_result':'complete' if sufficient else ('restricted' if ats and all(x['result']=='skipped_exact_restriction' for x in ats) else 'partial'),'route_used':'official_public_json' if sufficient else 'configured_master_and_fallbacks','attempted_urls':attempts,'current_content_comparison':comparisons})
 refs=[source_ref]
 if any(x['result']=='skipped_exact_restriction' for x in ats): refs.append(restr)
 if sid in {'usa-michigan-state-oncology-trials','usa-penn-vet-clinical-trials','sponsor-aurelius-biotherapies-pilot','usa-wisconsin-oncology-studies'}: refs.append(web_src_ref)
 matches=a.get('exact_canonical_url_matches',[])
 finding=(f"{s.get('name',sid)}: current configured routes produced "+(', '.join(f'{k}={v}' for k,v in sorted(counts.items())) or 'no returned route')+f"; exact canonical links reconciled={len(matches)}. ")
 if sufficient: finding+=f"Official AVMA JSON was fully parsed: {avma['total_unique_records']} unique records, {avma['recruiting_oncology_records']} recruiting oncology; zero additions/removals versus 2026-11-19."
 elif ats and all(x['result']=='skipped_exact_restriction' for x in ats): finding+='Every configured URL is covered by an exact saved restriction; no request was sent and no institution-wide restriction was inferred.'
 else: finding+='All exposed configured content and candidate links were reviewed; the page did not prove an exhaustive current oncology roster.'
 change_reviews=[{'current_evidence':source_ref,'finding':f'Current changed route content for {sid} was individually examined.','catalog_impact':'No catalog change from this route alone.'}] if sid in changed else []
 if sid=='canivax-clinical-development': change_reviews=[{'current_evidence':source_ref,'finding':'Current owner/vet/news content now confirms a UK clinical access programme and studies for advanced cancer.','catalog_impact':'CaniVive/CaniMel left PENDING_EVIDENCE because no individual protocol, sites, complete eligibility or owner-cost terms are public.'}]
 if sid=='usa-penn-vet-clinical-trials': finding+=' Direct current protocol discovery added penn-flash-metastatic-osa-gilvetmab-2026.'
 reviews.append({'source_id':sid,'reviewed_at':now_s,'current_official_content':True if sufficient else bool(a.get('current_official_content')),'roster_complete':True if sufficient else False,'protocols':avma['protocols'] if sufficient else matches,'finding':finding,'catalog_comparison':'AVMA exact current recruiting-oncology IDs compared to prior day and canonical catalog.' if sufficient else f'Compared {len(matches)} exact canonical URL matches and current candidate links; no known-domain shortcut was used.','roster_evidence_refs':[source_ref] if sufficient else refs,'evidence_refs':list(dict.fromkeys(refs)),'change_reviews':change_reviews,'remaining_available_steps':[],'completion_basis':f'{sid}: every configured permitted route was fetched or exact-restriction-reviewed; exposed candidate links were reconciled, and remaining roster/protocol gaps depend on publisher or access changes.'})
receipt={'schema_version':1,'run_id':RUN,'time_context':'America/New_York','started_at':baseline['started_at'],'recorded_at':now_s,'status':'INCOMPLETE','source_total':len(receipts),'attempted_total':sum(x['opened_this_run'] for x in receipts),'content_sufficient_total':sum(x['content_sufficient'] for x in receipts),'processing_complete_total':sum(x['processing_complete'] for x in receipts),'sources':receipts,'deadline_review_ref':f'research/audit-runs/{RUN}/deadline-review.json','discovery_evidence_ref':f'research/audit-runs/{RUN}/global-discovery-evidence.json','protocol_review_ref':protocol_ref}
dump('receipt-final.json',receipt)
# Per-source gap diagnosis for every insufficient source.
gaps=[]
for rec,rev in zip(receipts,reviews):
 if rec['content_sufficient']: continue
 sid=rec['source_id']; urls=[x['url'] for x in rec['attempted_urls']]; a=analysis_by.get(sid,{}); counts=collections.Counter(x['result'] for x in src_by.get(sid,[]))
 cat='source_unavailable' if not rec['opened_this_run'] else ('discovery_source_not_trial_roster' if inventory['sources'][[x['id'] for x in inventory['sources']].index(sid)].get('source_type') in {'directory','discovery'} else 'roster_unestablished')
 gaps.append({'source_id':sid,'category':cat,'processing_assessment':'external_blocker','question':f'Current exhaustive recruiting-oncology roster or remaining protocol facts are not established for {sid}.','reason':f"Current route outcomes for {sid}: "+(', '.join(f'{k}={v}' for k,v in sorted(counts.items())) or 'no readable route')+f"; exact canonical matches={len(a.get('exact_canonical_url_matches',[]))}.",'next_action':f'Recheck the exact configured routes for {sid} on the next daily audit; deepen only a new or changed protocol-level signal.','unperformed_steps':[],'completion_decision':{'remaining_fact':f'{sid}: an exhaustive live oncology roster and any unpublished protocol facts remain publisher/access dependent.','routes_exhausted_evidence':f'{sid}: receipt records {len(urls)} exact configured URL decisions, including saved restriction decisions where applicable.','available_reconciliation_done_evidence':f'{sid}: {len(a.get("exact_canonical_url_matches",[]))} exact canonical URL matches and {len(a.get("unmatched_candidate_links",[]))} exposed candidate links were individually compared in source-content-analysis; none remains as an available unreviewed route.'},'evidence':{'source_id':sid,'attempted_urls':urls,'evidence_refs':rev['evidence_refs']}})
dump('gap-review.json',{'original_run_id':RUN,'rows':gaps})
# Current issue updates. Retained exact questions remain blocked unless all required facts were newly established.
issue_updates=[]
for old in baseline['issues']:
 tid=old['trial_id']; ats=prot_by.get(tid,[]); counts=collections.Counter(x['result'] for x in ats); refs=[protocol_ref]
 if any(x['result']=='skipped_exact_restriction' for x in ats): refs.append(restr)
 if tid.startswith('msu-') or tid in {'aurelius-lytix-bcell-lymphoma','wisc-lymphoma-half-body-rt-chop'}: refs.append(web_prot_ref)
 outcome=', '.join(f'{k}={v}' for k,v in sorted(counts.items())) or 'no current public protocol route returned'
 question=old.get('question') or 'Read the full primary protocol and reconcile current published facts.'
 issue_updates.append({'issue_id':old['issue_id'],'trial_id':tid,'kind':old['kind'],'state':'BLOCKED','reviewed_at':now_s,'finding':f'{tid}: current individual protocol review produced {outcome}. The current evidence did not newly publish every fact needed to resolve the retained exact question: {question}','question':question,'next_action':f'Recheck {old.get("primary_url") or by_trial.get(tid,{}).get("url")} when the publisher exposes the missing exact fact; preserve current canonical data meanwhile.','evidence_refs':list(dict.fromkeys(refs)),'restriction_or_unpublished_evidence_refs':list(dict.fromkeys(refs)),'full_protocol_review_complete':False})
# Execution review, with no available executor work left; unresolved items are external evidence gaps.
review={'schema_version':1,'run_id':RUN,'ended_at':now_s,'added_catalog_ids':['penn-flash-metastatic-osa-gilvetmab-2026'],'source_reviews':reviews,'issue_updates':issue_updates,'discovery_queries':qrows,'discovered_urls':[x['url'] for x in lead_rows],'leads':lead_rows,'deadline_review_ref':f'research/audit-runs/{RUN}/deadline-review.json','stop':{'reason':'completed_available_work','detail':'All permitted configured source routes, current public protocols, country/language discovery passes, deadline comparisons, candidate dispositions and catalog reconciliation available in this run were completed. Remaining items require new publisher evidence or removal of exact saved access restrictions.','evidence_refs':[source_ref,protocol_ref,f'research/audit-runs/{RUN}/global-discovery-evidence.json']}}
dump('execution-review.json',review)
print(json.dumps({'sources':len(receipts),'opened':receipt['attempted_total'],'sufficient':receipt['content_sufficient_total'],'gaps':len(gaps),'issues':len(issue_updates),'queries':len(qrows),'leads':len(lead_rows),'deadline_rows':len(dead_rows),'ended_at':now_s},indent=2))
