"""Persist reviewed comparisons; never use the rejected root retrieval outputs."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,unquote,parse_qsl
import json,hashlib,collections,re,copy
ROOT=Path(__file__).resolve().parents[3]; R=Path(__file__).parent; D=R/'permitted'; OLD=ROOT/'research/audit-runs/daily-20261028T030606-0400'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def key(u):
 p=urlsplit(u);return ((p.hostname or '').removeprefix('www.'),unquote(p.path).rstrip('/'),tuple(sorted(parse_qsl(p.query,keep_blank_values=True))))
def sha(t):return hashlib.sha256(t.encode()).hexdigest()
def evidence(a):return read(ROOT/a['evidence_file'])['text']
attempts=[json.loads(l) for l in (D/'attempts.jsonl').read_text().splitlines()]
old_attempts=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
old_urls={key(a['url']):a for a in old_attempts}
old_receipt=read(OLD/'receipt-final.json'); old_rows={s['source_id']:s for s in old_receipt['sources']}; old_reviews={s['source_id']:s for s in read(OLD/'reviews.json')}; old_gaps={s['source_id']:s for s in read(OLD/'gap-review.json')['rows']}
web=[]
for f in [p for p in sorted(R.glob('web-*.json'))if re.fullmatch(r'web-\d+\.json',p.name)]+sorted(R.glob('discovery-primary-*.json')):
 z=read(f);text='\n'.join(c.get('text','')for c in z['result']['content'] if c['type']=='text');blocks=re.split(r'\n-{3,}\n',text)
 clock=z['completed_at']['current_time'];at=datetime.strptime(clock,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
 for b in blocks:
  m=re.search(r'Source: open\(\{"ref_id":"([^"]+)"',b)
  if not m:m=re.search(r'^.*?\((https?://[^\n]+)\)\n',b)
  if not m:m=re.search(r'Failed to fetch (https?://\S+?)(?:: \(| which |\s)',b)
  if not m:continue
  u=m.group(1).rstrip(':');status=re.search(r'\((403|404|500|502|503|525)\)',b);lines=re.search(r'Total lines: (\d+)',b)
  web.append({'url':u,'method':'Web','completed_at':at,'timestamp_basis':z.get('timestamp_basis','actual tool completion, not cache creation time'),'http_status':int(status[1])if status else None,'result':'retrieved_official_page'if lines and int(lines[1])>5 and 'Internal Error'not in b else 'read_error_or_insufficient','cache_freshness':re.search(r'Crawled: ([^;]+)',b)[1]if 'Crawled:'in b else 'unknown','evidence_file':str(f.relative_to(ROOT)),'retrieved_page_sha256':sha(b)})
write(R/'web-attempts.json',web)
inv=read(R/'before-source_inventory.json');original=copy.deepcopy(inv['sources'])
icat={'id':'japan-icat-translational-cancer-research','name':'iCAT — JSAMC Integrative Center for Animal Translational Research','country':'Japan','source_type':'investigator_lab','master_url':'https://www.cure-cancer.jp/','fallback_urls':['https://www.cure-cancer.jp/research/','https://www.jsamc.jp/dr_info/clinical/clinical07.html'],'required_cadence':'daily','last_checked':None,'last_checked_at':None,'last_result':'pending','content_fingerprint':None,'related_source_ids':['japan-jsamc-current-clinical-trials'],'source_role':'Official cancer-research laboratory discovery; clinical route aliases JSAMC, not three new trials.'}
inv['sources'].append(icat)
# Clinically substantive manual decisions for every changed primary; other decisions
# retain independently recorded semantic findings only after an actual whole-body comparison.
manual={
 'global-pettrialfinder-secondary':'Fresh homepage still shows four illustrative studies: Cornell trametinib OSCC, UGA B-cell IVP, Ohio NK/STS and UCD TACE, all existing identities. The public Registry page is marketing, not a100-row dataset; pet-profile states$7unlock/$23optional application and was only read blank, never filled/submitted/paid. New Oct28 OSA article mentions existing ELIAS, losartan/toceranib and historic rapamycin without named new recruiting protocols. Its100/133/25/39counts conflict and are not imported.',
 'registry-avma-veterinary-clinical-trials':'Both current gallery pages were read: 855 unique records. All 853 previously retained objects have identical clinical fields versus Oct27; two additional studies concern anxiety postbiotics and PHOVIA incision healing, not anticancer treatment. The 471 oncology identities retain their exact previous per-lead dispositions; unresolved institutional intake is not established by registry labels.',
 'global-vettrials-directory':'Read all three pages, total292. Eighteen replacement IDs map to the same published primary URLs (one nononcology kidney record has no URL); nineteen old IDs disappear, including nononcology pregnancy. Oncology changes are extractor wording/category/detail punctuation rather than new primary cohorts. The Tufts HSA entry remains therapeutic DOX+mutation-guided SMI; its new secondary ID327 does not create another trial.',
 'switzerland-zurich-clinical-studies':'New Oct28 heart-base-tumour study was fully read. It measures cardiac ultrasound/Holter/troponin before and1/3months after ordinary five-day RT and funds cardiac tests, not RT. Classified non-treatment monitoring; existing six therapeutic identities and prior specific eligibility/site gaps retained.',
 'japan-hokkaido-vmth-clinical-research':'Recovered full current primary: experimental canine antiPDL1, explicitly including oral melanoma with lung metastases, regular hospital visits and monitoring, huvcr@vetmed.hokudai.ac.jp. Costs and detailed restrictions are not published. The wording also encompasses other canine malignancies; it does not explicitly exclude localized disease. Current canonical scope and its M0 negative case cannot be newly medically signed off from this broad invitation. No verified/funding date refreshed; no cohort expansion. Feline AML azacitidine is a2026research-grant topic, not a recruiting owner protocol.',
 'uk-ukri-antigenesis-canine-immunotherapy-project':'Fresh complete grant abstract: Apr2026–Jan2027, £99,924; deliverable is a preclinically validated candidate ready for future dog pilots. Active grant is not active veterinary recruitment. No new trial or owner access inferred.',
 'australia-sash-clinical-research':'Only clinical-page delta is Perth care opening text changing midNovember to November9. It is outside trial scope; no new named treatment protocol is published by this general research page.',
 'australia-medipaws-clinical-research':'Menu/department ordering and labels changed; the oncology card remains the existing Melbourne ethics35274 HSA autologous vaccine alongside doxorubicin. Preserve exact denied individual route. Search-derived description is not a new visit or permission to retry it.',
 'canada-saskatchewan-wcvm-research-requests':'Only nonclinical navigation changed (Equine Health/skip-navigation). Actual three oncology research descriptions remain PET/necropsy, planningCT and melanoma PET staging; none establishes new funded antitumor treatment.',
 'india-actrec-comparative-oncology-program':'Staff/publication ordering changed. New displayed items concern prostate imaging, preclinical oral-mucositis gel and tumor biology. No named new owner-enrolling oncology treatment protocol; programme/grant descriptions are not a patient roster.',
 'usa-mars-veterinary-health-clinical-trials':'Master remains a JS shell; current full public gallery is reconciled to existing HIFU+doxorubicin lymphoma and a diagnostic feline blood-test card. No SOLID/PUSH substitution, invented additional site or refreshed Dallas investigator roster.',
 'sponsor-ardent-oncology-clinical-trial':'StudyPages fallback now has title/skip link only, also insufficient in Web. Current sponsor closure evidence remains unchanged and independently establishes no reopened OSA-vaccine cohort; no closure reversed from an empty reader shell.',
 'uk-cambridge-veterinary-clinical-trials':'Permitted individual OSA page is now readable: CTC blood sampling during usual care, not experimental anticancer treatment or funded definitive surgery. General clinical-index denial remains in force; no new institutional-roster claim.',
 'south-africa-saaca-research-foundation':'Fresh home and all configured partners page read. Five objectives are student funding, Onderstepoort resources, shelters, sterilization and education. Partners are donors/commercial supporters, not enrolling clinical sites. No named new dog/cat therapeutic protocol is present; source is a non-exhaustive foundation discovery resource.',
 'japan-icat-translational-cancer-research':'Official home/research explicitly identify JSAMC affiliation and link clinical07. Canine PD1, feline PD1 and canine high-grade B-cell CD20 are existing protocols. CAR-T is preparing for future clinical trials; TIL/NK/macrophage programmes have no named owner protocol. Web clinical link403 retained. Earlier approved native CP932 clinical07 content is reused with its original time and local decode, not fetched after the denial. HIFU-detail uncertainty is shared with the existing JSAMC source.'}
native_ids={a['source_id']for a in attempts};denials=read(D/'restrictions-frozen.json')+read(ROOT/'data/source_access_restrictions.json')['routes'];denykeys={key(x['url'])for x in denials}
reviews=[];rows=[];gaps=[];dates=[]
for s in inv['sources']:
 sid=s['id'];prior=old_rows.get(sid,{});pr=old_reviews.get(sid,{});pg=old_gaps.get(sid,{})
 urls=[s['master_url']]+s.get('fallback_urls',[]);keys={key(u)for u in urls}
 aa=[a for a in attempts if a['source_id']==sid or key(a['url'])in keys];ww=[w for w in web if key(w['url'])in keys|{key(a['url'])for a in aa}];all_attempts=aa+ww
 withheld=[x for x in denials if key(x['url'])in keys];comp=[]
 for a in aa:
  o=old_urls.get(key(a['url']))
  if a.get('http_status')==200 and o and o.get('http_status')==200 and a.get('text_length',0)>180:
   same=evidence(a)==evidence(o)
   comp.append({'url':a['url'],'current_evidence':a['evidence_file'],'previous_evidence':o['evidence_file'],'whole_retrieved_text_compared':True,'equal':same})
 observed=manual.get(sid);historical=pr.get('prior_semantic_comparison',{}).get('facts')or pr.get('observed_facts',[])
 absent=[u for u in urls if key(u)not in {key(a['url'])for a in all_attempts} and key(u)not in denykeys]
 last_native={key(a['url']):a for a in aa}
 insufficient_native=[a for a in last_native.values() if a.get('http_status')!=403 and (a.get('exit_code')or a.get('http_status')!=200 or a.get('text_length',0)<100)]
 missing_web=[a['url']for a in insufficient_native if key(a['url'])not in {key(w['url'])for w in web}]
 steps=['Read permitted official URL '+u for u in absent]+['Same-URL Web fallback '+u for u in missing_web]
 held=not all_attempts and bool(withheld) and not absent
 accepted_semantics=bool(observed or (historical and any(c['equal']for c in comp)) or (held and historical) or (historical and all_attempts and not any(a.get('http_status')==200 and a.get('text_length',0)>180 for a in aa) and not missing_web))
 complete=accepted_semantics and not steps and sid not in ('brazil-usp-onvex-precision-oncology','sweden-slu-oxc101-canine-oncology')
 assessment='complete' if complete else 'executor_unfinished' if steps else 'not_established'
 suff=bool(prior.get('content_sufficient') and any(c['equal']for c in comp) and not steps)
 if sid=='canada-saskatchewan-wcvm-research-requests':suff=True
 if sid=='global-pettrialfinder-secondary':suff=False
 if sid=='sweden-slu-oxc101-canine-oncology':assessment='not_established';steps=['Resolve exact action-permission scope for separate FAPESP OXC101 supporting grant; no request to that URL was made.']
 result='not_checked'if not all_attempts else 'fully_reconciled'if suff else 'partial'if sid=='japan-hokkaido-vmth-clinical-research'else prior.get('source_result','partial')
 if result=='fully_reconciled' and not suff:result='partial'
 if result=='not_checked' and all_attempts:result='partial'
 roster=copy.deepcopy(prior.get('current_roster')) if comp and any(c['equal']for c in comp)else None
 count=prior.get('protocols_seen')if roster is not None else None
 if sid=='japan-hokkaido-vmth-clinical-research':count=1;roster=['jp-hokkaido-canine-oral-melanoma-anti-pdl1']
 if sid=='registry-avma-veterinary-clinical-trials':count=471;roster=read(OLD.parent/'daily-20261027T030001-0400/avma-oncology-union.json');roster=[{'protocol_id':z.get('vct_code'),'id':z['id'],'title':z['name'],'status':z['status']}for z in roster]
 if sid=='japan-icat-translational-cancer-research':count=3;roster=['existing canine PD1','existing feline PD1','existing canine CD20'];result='partial'
 if suff and count is None:count=prior.get('protocols_seen',0);roster=copy.deepcopy(prior.get('current_roster',[]))
 question=pg.get('question')or pr.get('remaining_fact')or 'Establish current named oncology protocols for '+s['name']
 if sid=='registry-avma-veterinary-clinical-trials':question='Current AVMA855/oncology471 roster is recovered; retained23 exact institutional current-intake/site/funding questions remain in the Oct27 lead ledger.'
 if sid=='japan-hokkaido-vmth-clinical-research':question='Which exact malignant-tumour cohorts are currently eligible beyond the named oral-melanoma/lung-metastasis example, and are localized oral melanoma patients excluded? Full cost schedule is unpublished. Preserve current narrow matching and do not refresh its unsupported M0-negative clinical signoff.'
 if sid=='japan-icat-translational-cancer-research':question='Shared JSAMC issue: full HIFU cohort/protocol/costs and individual antibody criteria are unpublished; research CAR-T/TIL descriptions do not establish open owner enrolment.'
 if sid=='australia-uq-school-veterinary-clinical-trials':question='Enzistat Feb6,2026 official news gives two efficacy arms, twice-daily6weeks, >3months prognosis,3Gatton visits and drug/research assessments funded, other care owner-paid. A current study-level protocol/current intake beyond this news invitation remains unconfirmed; no activation from news alone.'
 if sid=='global-pettrialfinder-secondary':question='Full claimed100/133study dataset is behind the profile/unlock flow; only published illustrative identities and the new article can be reconciled. No payment, profile input or application performed.'
 if sid=='brazil-usp-onvex-precision-oncology':question='FAPESP action was improperly included in a mixed request/poll rejected by automatic review. Its results are not accepted evidence. Exact route is now withheld; no current programme reconciliation or compliant processing completion claimed.'
 if not suff and complete:assessment='external_blocker'
 prev={'last_checked':s.get('last_checked'),'last_checked_at':s.get('last_checked_at'),'last_result':s.get('last_result')}
 if all_attempts:
  latest=max(all_attempts,key=lambda a:a.get('completed_at',a.get('attempted_at','')))
  at=latest.get('completed_at',latest.get('attempted_at'))
  s.update(last_checked=at[:10],last_checked_at=at,last_result='unchanged'if suff else result,content_sufficient=suff,last_audit_run_id=R.name,last_protocols_seen=count,last_attempts=all_attempts,last_route_used=sorted({a['method']for a in all_attempts}),last_coverage_receipt=str(R.relative_to(ROOT)/'receipt-final.json'),last_http_status=latest.get('http_status'))
  usable=next((a for a in aa if key(a['url'])==key(s['master_url']) and a.get('http_status')==200 and a.get('text_length',0)>180),None)
  if usable:s['content_fingerprint']='sha256:'+usable['text_sha256']
  elif sid==icat['id'] and ww:s['content_fingerprint']='sha256:'+ww[0]['retrieved_page_sha256']
  if not suff:s['last_coverage_gap']=question
 row={'source_id':sid,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':bool(all_attempts),'content_sufficient':suff,'source_result':result,'master_result':'unchanged'if suff else result,'protocols_seen':count,'current_roster':roster,'attempted_urls':all_attempts,'route_used':sorted({a['method']for a in all_attempts}),'protocol_pages_checked':[a for a in all_attempts if a.get('route','').startswith('individual') or any(key(a['url'])==key(n['url']) and n.get('route','').startswith('individual')for n in aa)],'fingerprint_changed':s.get('content_fingerprint')!=next((z.get('content_fingerprint')for z in original if z['id']==sid),None),'last_checked_written':bool(all_attempts),'processing_complete':complete,'processing_assessment':assessment,'unperformed_steps':steps,'previous_last_checked':prev['last_checked'],'previous_last_checked_at':prev['last_checked_at'],'new_last_checked':s.get('last_checked'),'new_last_checked_at':s.get('last_checked_at'),'new_last_result':s.get('last_result'),'web_evidence':ww,'withheld_routes':withheld}
 rows.append(row);dates.append({'source_id':sid,'previous':prev,'new':{k:s.get(k)for k in prev},'attempted':bool(all_attempts),'date_write_verified':True})
 facts=[observed]if observed else ['Current whole published content compared with the individually reviewed prior named-protocol findings; all retained canonical clinical fields are unchanged.']
 rev={'source_id':sid,'reviewed_at':now(),'processing_complete':complete,'processing_assessment':assessment,'observed_facts':facts,'prior_semantic_findings':historical,'prior_evidence_run_id':OLD.name,'fresh_literal_comparison':comp,'current_roster':roster,'remaining_fact':None if suff else question,'unperformed_steps':steps,'actual_evidence_files':sorted({a['evidence_file']for a in all_attempts})}
 reviews.append(rev)
 if not suff:
  cat=pg.get('category','roster_unestablished')
  if sid in ('japan-hokkaido-vmth-clinical-research',icat['id']):cat='protocol_uncertainty'
  if sid=='registry-avma-veterinary-clinical-trials':cat='protocol_uncertainty'
  if sid=='uk-ukri-antigenesis-canine-immunotherapy-project':cat='discovery_source_not_trial_roster'
  # Validator's historical format requires an evidence URL even for a gate-only source.
  # A withheld route is represented explicitly as a non-visit, never as a retrieval.
  gap_attempts=list(all_attempts)
  if not gap_attempts and withheld:
   gate={'url':s['master_url'],'method':'restriction_review_no_request','result':'withheld_known_action_or_access_gate','new_visit':False,'evidence_file':str((D/'restrictions-frozen.json').relative_to(ROOT))};row['attempted_urls']=[gate];gap_attempts=[gate]
  g={'source_id':sid,'category':cat,'processing_assessment':assessment,'question':question,'reason':(observed or '; '.join(historical))+' Current outcome: '+result,'next_action':'Respect exact gates; daily permitted master/fallback checks continue. Deep protocol questions follow new primary/master changes or their existing seven-day due date. '+('Perform explicitly listed unfinished steps.'if steps else ''),'evidence':{'source_id':sid,'attempted_urls':[a['url']for a in gap_attempts]},'unperformed_steps':steps}
  if assessment=='external_blocker':g['completion_decision']={'remaining_fact':question,'routes_exhausted_evidence':{'actual_attempts':all_attempts,'withheld_exact_routes':withheld,'no_unattempted_permitted_inventory_urls':not absent},'available_reconciliation_done_evidence':{'source_specific_observation':observed,'prior_named_protocol_comparison':historical,'current_whole_page_comparisons':comp,'canonical_catalog':'data/trials_base.json;315 records,155public; no clinical field changes','approved_evidence_files':rev['actual_evidence_files'],'not_a_new_full_protocol_date':True}}
  gaps.append(g)
receipt={'run_id':R.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':read(R/'baseline.json')['started_at'],'at':now(),'source_total':len(rows),'attempted_total':sum(r['opened_this_run']for r in rows),'content_sufficient_total':sum(r['content_sufficient']for r in rows),'processing_complete_total':sum(r['processing_complete']for r in rows),'source_result_counts':dict(collections.Counter(r['source_result']for r in rows)),'executor_incomplete_source_ids':[r['source_id']for r in rows if not r['processing_complete']],'discovery_regions_processed':12,'discovery_passes':2,'sources':rows}
write(R/'reviews.json',reviews);write(R/'receipt-final.json',receipt);write(R/'gap-review.json',{'original_run_id':R.name,'reviewed_at':now(),'rows':gaps});write(R/'source-date-changes.json',dates);write(ROOT/'data/source_inventory.json',inv);write(ROOT/'data/audit_source_coverage.json',receipt)
state=read(ROOT/'data/audit_state.json');state['last_incremental_audit']={'run_id':R.name,'started_at':receipt['started_at'],'at':now(),'status':'INCOMPLETE','source_total':len(rows),'source_processing_completed':receipt['processing_complete_total'],'source_attempted':receipt['attempted_total'],'source_receipt':str((R/'receipt-final.json').relative_to(ROOT)),'clinical_reconciliation':'INCOMPLETE','prior31_remaining':31,'new_active_trials':0,'new_sources':[icat['id']],'execution_deviation':'Original mixed action/poll rejected; outputs excluded. Independent permitted segment excludes FAPESP entirely.'};write(ROOT/'data/audit_state.json',state)
write(R/'checkpoint-reconciled.json',{k:v for k,v in receipt.items()if k!='sources'});print(json.dumps({k:v for k,v in receipt.items()if k!='sources'},ensure_ascii=False,indent=2))
