"""Conservative receipts. Rejected fallback output is never consumed as evidence."""
from daily19 import ROOT,RUN,OLD,read,write,now,m
import json,copy,collections,hashlib,re
from datetime import datetime
from zoneinfo import ZoneInfo
rel=str(RUN.relative_to(ROOT));inv=read(RUN/'before-source_inventory.json');prior={r['source_id']:r for r in read(RUN/'previous-receipt.json')['sources']}
# Only the already returned master-stage metadata is selected. No fallback result,
# body, or comparison from the rejected batch is read or used for sign-off.
master=[]
for line in (RUN/'attempts.jsonl').read_text().splitlines():
 if '"route": "master"' in line:master.append(json.loads(line))
proto=[json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]
source_native=[a for a in proto if not a['source_id'].startswith('protocol:')]
write(RUN/'accepted-master-attempts.json',master)
web=[]
for f in sorted(RUN.glob('web-*.json')):
 d=read(f)
 if not isinstance(d,dict) or 'result' not in d or 'urls' not in d:continue
 text='\n'.join(c.get('text','') for c in d['result'].get('content',[]) if c.get('type')=='text');blocks=re.split(r'\n-{20,}\n',text)
 at=datetime.strptime(d['at']['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
 for u,b in zip(d['urls'],blocks):
  denial=bool(re.search(r'\(403\)|Forbidden|Access Denied|CAPTCHA',b,re.I));error='Internal Error' in b[:100] or 'not accessible via this tool' in b
  ref=re.search(r'【([^】]+)】',b);fresh=re.search(r'Crawled:[^;\n]+',b)
  web.append({'url':u,'method':'Web','attempted_at':at,'result':'access_denied' if denial else 'retrieval_error' if error else 'retrieved_page','http_status':403 if denial else None,'evidence_file':str(f.relative_to(ROOT)),'reference':ref.group(1) if ref else None,'freshness':fresh.group(0) if fresh else 'not established','text_length':len(b),'retrieved_text':b})
write(RUN/'accepted-Web-attempts.json',web)
restrictions=read(RUN/'restrictions-frozen.json')+[{'url':w['url'],'do_not_retry':True,'observed_at':w['attempted_at'],'method':'Web','http_status':403,'origin':w['evidence_file']} for w in web if w['result']=='access_denied'];denied={m.route_key(r['url']):r for r in restrictions}
write(RUN/'web-denials.json',[r for r in restrictions if r.get('method')=='Web' and r.get('observed_at','').startswith('2026-10-19')])
oldnative=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()];oldby={m.route_key(a['url']):a for a in oldnative if a.get('http_status')==200 and a.get('text_length',0)>100}
comps=[]
def links(v):return sorted(l['url'].split('#')[0] if '/cdn-cgi/l/email-protection#' in l['url'] else l['url'] for l in v['links'])
for a in master:
 b=oldby.get(m.route_key(a['url']))
 if not b or a.get('http_status')!=200 or a['text_length']<100:continue
 x=read(ROOT/a['evidence_file']);y=read(ROOT/b['evidence_file']);comps.append({'source_id':a['source_id'],'url':a['url'],'actual_attempt':a,'prior_evidence':b['evidence_file'],'same_entire_text':x['text']==y['text'],'same_entire_semantic_linkset':links(x)==links(y),'ignored_link_change':'Only Cloudflare randomized email fragment; actual complete link differences separately reviewed.'})
write(RUN/'accepted-master-comparisons.json',comps)
newid='sponsor-vetigenics-clinical-trials';newa=[a for a in proto if a['source_id']==newid]
inv['sources'].append({'id':newid,'name':'Vetigenics official clinical-trial pipeline','country':'USA','source_type':'cro_sponsor','master_url':newa[0]['url'],'required_cadence':'daily','last_checked':None,'last_result':'pending','content_fingerprint':None,'notes':'Official named VGS-001, VGS-002 and CHECKMATE-K9 protocol/site closure roster. Not a care directory. Sponsor identity source and current entire roster reconciled October19; no active intake inferred from historical announcements.'})
rows=[];gaps=[]
for s in inv['sources']:
 sid=s['id'];old=prior.get(sid,{});routes=[s['master_url']]+s.get('fallback_urls',[]);keys={m.route_key(u) for u in routes}
 aa=[a for a in master+source_native+web if m.route_key(a['url']) in keys or a.get('source_id')==sid and a in source_native]
 cc=[c for c in comps if c['source_id']==sid];same=any(c['same_entire_text'] and c['same_entire_semantic_linkset'] for c in cc)
 sufficient=bool(old.get('content_sufficient') and same and old.get('current_roster') is not None)
 roster=copy.deepcopy(old.get('current_roster')) if same else None;count=old.get('protocols_seen') if roster is not None else None
 # A generic unchanged index cannot replace the missing paginated roster.
 if sid in ['usa-uc-davis-vcct','usa-mars-veterinary-health-clinical-trials','global-vettrials-directory','registry-avma-veterinary-clinical-trials','usa-colorado-state-vth-clinical-trials']:sufficient=False;roster=None;count=None
 portal_names={'registry-avma-veterinary-clinical-trials':'avma','usa-colorado-state-vth-clinical-trials':'csu','usa-uc-davis-vcct':'ucd','usa-mars-veterinary-health-clinical-trials':'mars','global-vettrials-directory':'vettrials'}
 portal=None
 if sid in portal_names:
  portal=read(RUN/(portal_names[sid]+'-comparison.json'))
  assert not portal['changed'] and not portal['added'] and not portal['missing']
  roster=copy.deepcopy(old.get('current_roster'));count=old.get('protocols_seen');sufficient=old.get('content_sufficient',False)
  if sid=='global-vettrials-directory':roster=[x for x in portal['whole_current_roster'] if x.get('conditionCategory')=='oncology'];count=len(roster)
 if sid==newid:
  sufficient=True;count=3;roster=[{'protocol':'VGS-001','disease':'canine oral melanoma','sites':['NC State Closed','Missouri Closed']},{'protocol':'VGS-002','disease':'canine urothelial carcinoma','sites':['Ethos Closed','BARC Closed'],'canonical_id':'penn-anti-pd1-urothelial-carcinoma','decision':'Enrollment closed; matching disabled'},{'protocol':'CHECKMATE-K9','disease':'canine cancer combination CTLA4+PD1','sites':['Wisconsin Closed','BARC Closed','Illinois Closed','Tufts Closed','Missouri Closed'],'status':'Fully Enrolled'}]
 if sid=='directory-veterinary-cancer-society':roster=None;count=None
 result='fully_reconciled' if sufficient else 'partial' if aa else 'not_checked'
 usable=any(a.get('http_status')==200 and a.get('text_length',0)>500 or a.get('method')=='Web' and a['result']=='retrieved_page' and a['text_length']>1000 for a in aa)
 if aa and not usable and sid in ['usa-anivive-trials','usa-oklahoma-state-clinical-trials']:result='unreachable'
 missing=[u for u in routes if not any(m.route_key(a['url'])==m.route_key(u) for a in aa) and m.route_key(u) not in denied]
 # If master establishes the complete roster, redundant fallbacks are not mandatory.
 if sufficient:missing=[]
 banned_all=all(m.route_key(u) in denied for u in routes)
 complete=sufficient or (not missing and (same or banned_all or sid in ['usa-anivive-trials','usa-oklahoma-state-clinical-trials','new-zealand-kode-veterinary-sciences-trials']))
 assessment='external_blocker' if complete else 'executor_unfinished' if missing else 'not_established'
 category=old.get('category') or ('source_unavailable' if not usable else 'roster_unestablished')
 question=old.get('question') or 'Current complete institutional roster and study-level access are not established by today\'s permitted evidence.'
 if sid=='directory-veterinary-cancer-society':category='discovery_source_not_trial_roster';question='Which current protocol routes follow the VCS resource links? Directory role was read; no exhaustive recruiting roster is demanded. Guardian/GCVS searches exposed no oncology trial, which is not proof of absence.'
 if sid=='japan-hokkaido-vmth-clinical-research':question='Does the newly listed2026 feline AML/azacitidine research project offer current owner enrollment? No protocol invitation/costs/contact specific to this project are published in the current programme list.'
 if portal:
  category=old.get('category') or 'protocol_uncertainty';question=old.get('question') or question
 narrative=('Current entire master text and complete linkset compared with October18 evidence; roster retained only after explicit equality. ' if same else 'No prior roster copied as today\'s roster. ')+(old.get('reconciliation','') if sid!=newid else 'Whole fresh sponsor roster reconciled by exact intervention, cohort, provider groups and all published closure rows; historical2023 primary establishes VGS-002 identity.')
 if portal:
  narrative='Independent fresh public JSON responses retrieved after the new VGS-002 status signal. Full objects and complete pagination compared to October18: no added/removed/changed records. Earlier rejected mixed batch output not consumed. Individual primary gaps remain separate. '+question
  if not missing:complete=True;assessment='external_blocker'
  portal_evidence={k:v for k,v in portal.items() if k not in ['whole_current_roster','current_roster']}
  portal_evidence['whole_current_roster_evidence_file']=str((RUN/(portal_names[sid]+'-comparison.json')).relative_to(ROOT))
 # These are explicit source-specific human role/route decisions, not a blanket
 # conversion of all partial rows into complete processing.
 manual={
 'directory-veterinary-cancer-society':'Full current Web directory/resource links read. They point to institutional sources, not named new trials. Guardian and Gulf Coast targeted source searches inspected; no new named protocol signal. Their general clinical services are outside this task. No exhaustive recruiting roster is demanded from VCS.',
 'usa-iowa-state-vmc-clinical-trials':'Two native503 results plus same-URL Web recovered a four-day-old active-trial list: one oncology cerumen/lymphoma-screening project, diagnostic not treatment. Current freshness is not proved by the cache; no other published oncology trial link was exposed.',
 'usa-michigan-state-oncology-trials':'Empty native body recovered via same-URL Web. Five named oncology protocols and all five corresponding permitted individual pages opened through Web after empty native bodies. Publication/crawl freshness limitations and quasiorganelle medical-inclusion proposal retained; no guessed criteria or new successful clinical date.',
 'europe-esvonc-ongoing-trials':'Full same-URL Web table read today. Named modalities, countries and linked organizer routes compared with known source/canonical identities; owner-quarantined European entries remain hidden. This non-exhaustive secondary table does not resolve exact organizer intake gaps.',
 'australia-uq-school-veterinary-clinical-trials':'Unchanged fresh master plus whole official February6 Enzistat news fallback read. Two described cohorts, oral6weeks, >3month prognosis, Gatton visits and drug/research coverage acknowledged. Current individual protocol confirmation beyond dated news remains unavailable; no news-only activation.',
 'australia-caninecancer-state-research-guide':'Current full archived-style state guide read: auranofin osteosarcoma signal, five-state legacy referral links and historical breed sampling. It has no newly named patient invitation beyond already qualified legacy research; old eligibility remains history, not current recruitment.',
 'usa-veterinary-cancer-care-clinical-trials':'Native503 twice and same-URL Web read. The published Current Trials section says no trials currently enrolling; old Immunocidin/Canalevia are Past Trials. Yesterday crawl cannot independently prove today\'s full roster. No extra public current-trial path is published.',
 'japan-hokkaido-vmth-clinical-research':'Entire changed research list and linkset reviewed. Added2026 feline AML/azacitidine entry is a research/project title, without a new link or owner-enrollment protocol. Other additions are lymphoma biomarkers, OA and nononcology projects. Targeted local-language search did not establish intake; absence is not claimed.',
 'usa-veterinary-oncology-services-trials':'Two native503 attempts and same-URL Web502. No current protocol navigation can be read; historical immunotherapy signals retain distinct unresolved identities. No new successful roster or verification date inferred.',
 'foundation-mibagents-canine-trials':'Entire current directory read, with its March19,2024 update limitation and linked institutional trials. It is a discovery directory; current separate primary/source rosters control access, not old inclusion. No specific new recruiting protocol is asserted.',
 'india-actrec-comparative-oncology-program':'Whole changed programme/profile and link differences read. Changes are staff ordering, JRF2027 and two2026 publication references, not a current named dog/cat owner invitation. Copper-delivery paper abstract remains an unqualified evidence signal, kept outside matching.',
 'australia-anzcvs-oncology-research-news':'Native500 twice and same-URL Web500; public chapter-news parent read unchanged. Only exposed chapter-repository path has an inherited explicit member-login gate, not retried. No publicly readable named recruiting oncology protocol is established.'}
 if sid in manual and not missing:
  narrative=manual[sid];complete=True;assessment='external_blocker'
 if missing:narrative+=' Unperformed/unconfirmed permitted routes remain executor work; the rejected batch output was not used.'
 actual_urls=aa+[{'url':u,'method':'none','result':'NOT_VISITED_PRIOR_PROHIBITION','not_a_current_attempt':True,'restriction_evidence':denied[m.route_key(u)]} for u in routes if not any(m.route_key(a['url'])==m.route_key(u) for a in aa) and m.route_key(u) in denied]
 latest=max(aa,key=lambda a:a['attempted_at']) if aa else None
 r={'source_id':sid,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':bool(aa),'content_sufficient':sufficient,'source_result':result,'master_result':'unchanged' if sufficient and sid!=newid else 'reachable' if sufficient else result,'protocols_seen':count,'current_roster':roster,'route_used':sorted({a['method'] for a in aa}),'actual_attempts':aa,'attempted_urls':actual_urls,'current_comparison_evidence':cc+([portal_evidence] if portal else []),'processing_complete':complete,'processing_assessment':assessment,'category':None if sufficient else category,'question':None if sufficient else question,'reconciliation':narrative,'unperformed_steps':['NOT VERIFIED; do not retry an alias of a denied target without clarified permission: '+u for u in missing],'previous_last_checked':s.get('last_checked'),'previous_last_checked_at':s.get('last_checked_at'),'previous_last_result':s.get('last_result'),'new_last_checked':latest['attempted_at'][:10] if latest else s.get('last_checked'),'new_last_checked_at':latest['attempted_at'] if latest else s.get('last_checked_at'),'new_last_result':'unchanged' if sufficient and sid!=newid else 'reachable' if sufficient else result}
 r['mandatory_routes']=[{'url':u,'actual_attempt_evidence':[{'url':a['url'],'at':a['attempted_at'],'method':a['method'],'evidence':a['evidence_file']} for a in aa if m.route_key(a['url'])==m.route_key(u)],'inherited_or_current_prohibition':denied.get(m.route_key(u))} for u in routes]
 if not sufficient:
  r['completion_decision']={'remaining_fact':question,'routes_exhausted_evidence':r['mandatory_routes'],'available_reconciliation_done_evidence':{'actual_comparisons':cc,'current_source_decision':narrative,'available_protocol_status_correction':'VGS-002 exact Penn/Ethos cohort closed from current sponsor; all other ambiguous statuses retained.'}}
  gaps.append({'source_id':sid,'category':category,'processing_assessment':assessment,'question':question,'reason':narrative,'next_action':'Resume only named permitted missing routes and comparisons; keep exact denials. No full queue restart or repeat prohibited target. Deep old questions retain original due dates.','unperformed_steps':r['unperformed_steps'],'completion_decision':r['completion_decision'],'evidence':{'source_id':sid,'attempted_urls':[a['url'] for a in actual_urls],'current_attempts':aa}})
 if latest:
  s.update(last_checked=r['new_last_checked'],last_checked_at=r['new_last_checked_at'],last_result=r['new_last_result'],last_attempts=[{k:v for k,v in a.items() if k not in ['retrieved_text','raw_file','stderr']} for a in aa],last_route_used=r['route_used'],audit_last_run_id=RUN.name,last_audit_run_id=RUN.name,last_protocols_seen=count,content_sufficient=sufficient,last_check_summary=narrative,last_coverage_receipt=rel+'/receipt-final.json')
  current=[a for a in aa if a.get('http_status')==200 and a.get('text_length',0)>100 and a.get('text_sha256')]
  if current:s['content_fingerprint']='sha256:'+current[0]['text_sha256'];s['fingerprint_method']='Current actual retrieved text only; roster reconciliation is separately recorded.'
 rows.append(r)
receipt={'run_id':RUN.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':read(RUN/'baseline.json')['started_at'],'source_total':len(rows),'attempted_total':sum(r['opened_this_run'] for r in rows),'content_sufficient_total':sum(r['content_sufficient'] for r in rows),'processing_complete_total':sum(r['processing_complete'] for r in rows),'source_result_counts':dict(collections.Counter(r['source_result'] for r in rows)),'executor_incomplete_source_ids':[r['source_id'] for r in rows if not r['processing_complete']],'executor_unfinished_actions':sum(len(r['unperformed_steps']) for r in rows),'unconfirmed_processing_sources':sum(r['processing_assessment']=='not_established' for r in rows),'source_pass_at':now(),'sources':rows,'rejected_mixed_batch_not_used':True,'strict_status':'INCOMPLETE'}
write(RUN/'receipt-final.json',receipt);write(RUN/'gap-review.json',{'original_run_id':RUN.name,'rows':gaps});write(ROOT/'data/source_inventory.json',inv);write(ROOT/'data/audit_source_coverage.json',receipt)
restr=read(ROOT/'data/source_access_restrictions.json');known={m.route_key(r['url']) for r in restr['routes']}
for r in restrictions:
 if m.route_key(r['url']) not in known:restr['routes'].append(r);known.add(m.route_key(r['url']))
restr['updated']='2026-10-19';write(ROOT/'data/source_access_restrictions.json',restr)
write(RUN/'local-date-readback.json',{'at':now(),'source_inventory_sha256':hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),'current_attempt_dates_verified':all(s['last_checked_at']==r['new_last_checked_at'] for s,r in zip(read(ROOT/'data/source_inventory.json')['sources'],rows) if r['opened_this_run']),'unvisited_dates_retained':all(r['new_last_checked_at']==r['previous_last_checked_at'] and r['new_last_checked']==r['previous_last_checked'] for r in rows if not r['opened_this_run']),'rows':[{k:r.get(k) for k in ['source_id','opened_this_run','previous_last_checked','new_last_checked','previous_last_checked_at','new_last_checked_at','previous_last_result','new_last_result']} for r in rows]})
state=read(ROOT/'data/audit_state.json');state['last_source_discovery_attempt']={k:v for k,v in receipt.items() if k!='sources'};state['last_source_discovery_attempt'].update(status='INCOMPLETE',coverage_receipt=rel+'/receipt-final.json',gap_review=rel+'/gap-review.json',global_discovery_regions=12,separate_protocol_review_gaps=33);write(ROOT/'data/audit_state.json',state)
write(RUN/('checkpoint-'+datetime.now().strftime('%H%M%S')+'-source-accounting.json'),{'at':now(),'run_id':RUN.name,'source_results':receipt['source_result_counts'],'source_processed':receipt['processing_complete_total'],'source_total':len(rows),'executor_unfinished_actions':receipt['executor_unfinished_actions'],'processing_not_established':receipt['unconfirmed_processing_sources'],'clinical_pending':33,'new_clinical_trials':0,'closed_enrollment':1,'new_official_sources':1,'note':'Incomplete executor actions and denied action retained, not disguised as external gaps.'})
print(json.dumps({k:v for k,v in receipt.items() if k!='sources'},ensure_ascii=False))
