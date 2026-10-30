"""Record today's reviewed whole-content comparisons and individual decisions."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,unquote,parse_qsl
import json,hashlib,collections,re,copy
R=Path(__file__).resolve().parent;ROOT=R.parents[2];OLD=R.parent/'daily-20261029T030505-0400'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def key(u):
 p=urlsplit(u);return ((p.hostname or '').removeprefix('www.'),unquote(p.path).rstrip('/'),tuple(sorted(parse_qsl(p.query,keep_blank_values=True))))
def body(a):return read(ROOT/a['evidence_file'])['text']
attempts=[json.loads(l)for l in(R/'attempts.jsonl').read_text().splitlines()]
oldattempts={key(a['url']):a for a in map(json.loads,(OLD/'permitted/attempts.jsonl').read_text().splitlines())}
priorrows={s['source_id']:s for s in read(OLD/'receipt-final.json')['sources']}
priorreviews={s['source_id']:s for s in read(OLD/'reviews.json')}
priorgaps={s['source_id']:s for s in read(OLD/'gap-review.json')['rows']}
web=[]
for f in sorted(R.glob('web-[0-9]*.json'))+sorted(R.glob('discovery-primary-*.json')):
 z=read(f);txt='\n'.join(c.get('text','')for c in z['result']['content']if c['type']=='text')
 stamp=z['completed_at'];stamp=stamp['current_time']if isinstance(stamp,dict)else stamp
 at=datetime.strptime(stamp,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat() if stamp.endswith(' UTC')else stamp
 for b in re.split(r'\n-{3,}\n',txt):
  m=re.search(r'Source: open\(\{"ref_id":"(https?://[^"]+)"',b)or re.search(r'^.*?\((https?://[^\n]+)\)\n',b)
  if not m:continue
  u=m[1].rstrip(':');status=re.search(r'\((403|404|500|502|503|525)\)',b);lines=re.search(r'Total lines: (\d+)',b)
  web.append({'url':u,'method':'Web','completed_at':at,'timestamp_basis':'actual tool completion; not page cache date','http_status':int(status[1])if status else None,'result':'retrieved_official_page'if lines and int(lines[1])>5 and 'Internal Error'not in b else 'read_error_or_insufficient','cache_freshness':re.search(r'Crawled: ([^;]+)',b)[1]if 'Crawled:'in b else 'unknown','evidence_file':str(f.relative_to(ROOT)),'retrieved_page_sha256':hashlib.sha256(b.encode()).hexdigest()})
write(R/'web-attempts.json',web)
inv=read(R/'before-source_inventory.json')
newid='brazil-ufpel-electroporation-oncology-project'
inv['sources'].append({'id':newid,'name':'UFPel veterinary oncology treatment projects — electroporation and eyelid surgery','country':'Brazil','source_type':'investigator_lab','master_url':'https://institucional.ufpel.edu.br/projetos/id/u10335','fallback_urls':['https://institucional.ufpel.edu.br/servidores/id/21596','https://institucional.ufpel.edu.br/projetos/id/u7937'],'required_cadence':'daily','last_checked':None,'last_checked_at':None,'last_result':'pending','content_fingerprint':None,'source_role':'Official university project discovery; published project periods do not prove present owner enrollment.'})
manual={
 'registry-avma-veterinary-clinical-trials':'Read both current gallery pages:856 unique records. All855 previous identities retained with no substantive clinical-field change. Added VCT26005991/id29135 is UF AZ194 nasal pain treatment for Cavalier Chiari-like malformation/syringomyelia, not oncology. The471 oncology identities and exact23 institutional questions are retained after object-level comparison; no new primary verification claimed.',
 'global-vettrials-directory':'Read all292 current records in three API pages. Six removed IDs have six same-study replacements (including nononcology rows). Dog oral PDT new id300 is the old held OVC protocol481; current full primary leaf and current canine index were read, the latter explicitly ON HOLD FOR RECRUITMENT. Thyroid staining id298 replaces522 and is diagnostic/on hold; its primary404 also received same-URL Web fallback. Tufts SABR671 replaces667, not another trial; Missouri BTK57 replaces329. Extractor wording changes do not supersede unchanged current institutional primary rosters.',
 'japan-kamogawa-oncology-news':'Full current oncology category, Sept30 oral-melanoma PD1 invitation and its linked official PDF read. The added navigation link points to the already catalogued corporate registration protocol. Three published sites exactly match Tokorozawa, Yamaguchi and Kyoto; dogs with confirmed oral malignant melanoma, six fortnightly visits, health/stage and concomitant-drug screening by site. Costs individually explained, no free-care claim. Full published protocol reread completed today; only verified date and case provenance refreshed, not funding date or clinical selection.',
 'japan-nihon-anmec-clinical-research':'Current index and four individual protocol pages differ only by added Japanese Skip to content navigation text. Lymphoid-neoplasm, canine lung-cancer, alternating-magnetic-field and remaining published study descriptions are unchanged; prior full individual review was Oct28, within28days. No clinical eligibility or funding update.',
 'india-actrec-comparative-oncology-program':'Current programme/staff page changes publication order and adds Re-analogue neuroblastoma xenograft and hepatic-copper papers. These are preclinical/publication signals, not newly recruiting owner treatment protocols. No new anticancer-access record or grant-as-recruitment claim.',
 'global-pettrialfinder-secondary':'Current whole public homepage compared: tumour-category percentages/counts changed (tags184 to172) while claimed unique studies100 and four illustrative identities remain. Cornell trametinib OSCC, UGA B-cell IVP, Ohio NK/STS and UCD TACE already mapped. A changed marketing counter does not expose a new named study. Full dataset remains behind profile/payment unlock; no login, payment, form entry or submission performed. Existing Oct28 OSA article is unchanged.',
 'uk-cambridge-veterinary-clinical-trials':'Permitted node2971 native attempts returned503, same-URL Web returned403. This exact route is now withheld without retry. Earlier OSA CTC sampling findings remain historical; no current primary roster or renewed study date claimed. Other configured clinical-index gates remain in force.',
 'denmark-copenhagen-veterinary-research':'Both official research-project and patient-recruitment URLs returned503 with one transient native retry each; both same-URL Web reads timed out. No current oncology roster was recovered. Old cached general-research pages cannot prove present owner intake.',
 'japan-icat-translational-cancer-research':'Fresh full home and research pages retain JSAMC-affiliated canine PD1, feline PD1 and canine high-grade B-cell CD20 programmes. CAR-T is preparation for future clinical trials; TIL/NK/macrophage descriptions do not establish a named open owner cohort. Shared clinical07 gate is respected; HIFU individual eligibility/cost question remains shared with JSAMC, not duplicated as another source task.',
 'usa-utsw-vroc-clinical-trials':'Native current master returned503; same-URL Web recovered the current eight-title research index and VROC contact. Existing study4/5 and previously catalogued protocols are not new studies. Owner-directed Completed dispositions for CPMV, RT-histotripsy and melanoma CRTNP remain; unchanged institutional invitation cannot reverse them. Full individual brochure contents remain unverified on restricted/insufficient routes.',
 'brazil-usp-onvex-precision-oncology':'No network request to FAPESP or this action-restricted source was dispatched today. Prior rejected mixed-action material is excluded from evidence. Exact permitted action scope and compliant source reconciliation remain NOT VERIFIED; no source date changed.',
 'uk-edinburgh-small-animal-clinical-trials':'Fresh full clinical-trials programme and due individual tigilanol-tiglate article read. Article is explicitly7Oct2024, describes eight-dog pilot for oral melanoma, QBiotics research funding and referral through Professor Blacklock; no current cohort dates, full eligibility or owner cost allocation. An old invitation and a generic current programme do not establish present enrollment; verified date remainsSept18.',
 'usa-missouri-oncology-clinical-trials':'Fresh whole current institutional roster read and compared: BTK BI705564, COTC033 VPL, LEAH and remaining published protocols retained. No carboplatin/amputation-timing study is present in current text. Due targeted official-domain search found only general chemotherapy/FAQ, not a current individual protocol. Disappearance alone does not close the retained timing trial; its eligibility/funding/current-intake question and prior dates remain. Newly worded secondary BTK record is the same existing protocol.',
 'usa-tennessee-vet-clinical-trials':'Fresh complete current master compared with named prior protocols; AML genetic-landscape and thyroid function remain diagnostic/sampling. New secondary oncology tag for splenic/liver MRI prompted full official PDF read: MRI contrast, biopsy, MRI/anesthesia and study histology funded; updated11/16/2016 and no experimental anticancer treatment. No new therapeutic identity.',
 'sweden-slu-oxc101-canine-oncology':'Fresh permitted SLU faculty and Silver Bullet2.0 sponsor programme pages read and compared. They describe OXC101 translational research, not a verified owner-enrolling cohort. Separate FAPESP supporting-grant route remains withheld; action-permission scope and processing completion are not established. No inferred activation.',
 newid:'Two full current official project pages and coordinator profile read natively. u10335:31Oct2025–28Feb2027,40dogs,cutaneous solid tumours<=3cm,bleomycin ECT versus calcium electroporation. u7937:12Mar2024–12Mar2028,eyelid neoplasms<=1cm,conventional excision versus excision/cryotherapy at HCV-UFPel and Dr Ricardo Oliveira clinic. Its group-size text is internally inconsistent (30 versus n35). These are therapeutic projects, but current recruitment, study-specific owner intake and owner costs are unpublished. Both WATCH/nonmatchable; project dates are not recruitment evidence.'}
special_questions={
 'registry-avma-veterinary-clinical-trials':'Recovered current856/oncology471 registry roster; exact23 institutional current-intake/site/funding questions remain in avma-reconciliation.json, without activation from registry status.',
 'uk-cambridge-veterinary-clinical-trials':'Current institutional oncology roster and individual OSA research status cannot be established from503 followed by exact-route403; prior blood-sampling study is not a new therapy.',
 'brazil-usp-onvex-precision-oncology':'Compliant action scope and current programme reconciliation for the withheld FAPESP route remain unestablished; no bypass request is allowed.',
 'sweden-slu-oxc101-canine-oncology':'The supporting FAPESP action scope remains unestablished; no open owner oncology protocol or complete processing signoff from a grant alone.',
 newid:'Are either electroporation u10335 or eyelid-surgery u7937 currently accepting owner referrals, at which participating site, with what eligibility confirmation and owner charges? Published project periods and general coordinator profile do not establish present trial access.'}
denials=read(R/'restrictions-frozen.json')+[json.loads(l)for l in(R/'new-denials.jsonl').read_text().splitlines()]
# The run's explicit FAPESP action-scope exclusion also withholds the separate
# SLU support-grant URL; it is not an unperformed permitted network request.
denials += [dict(d,method='planning_restriction_review_no_request',new_visit=False)for d in read(R/'withheld.json')if 'fapesp.br'in d['url']and key(d['url'])not in {key(z['url'])for z in denials}]
denykeys={key(d['url'])for d in denials}
reviews=[];rows=[];gaps=[];dates=[]
for s in inv['sources']:
 sid=s['id'];prior=priorrows.get(sid,{});pr=priorreviews.get(sid,{});pg=priorgaps.get(sid,{})
 urls=[s['master_url']]+s.get('fallback_urls',[]);keys={key(u)for u in urls}
 aa=[a for a in attempts if a['source_id']==sid or key(a['url'])in keys];ww=[w for w in web if key(w['url'])in keys|{key(a['url'])for a in aa}];allattempts=aa+ww
 withheld=[d for d in denials if key(d['url'])in keys];comp=[]
 for a in aa:
  o=oldattempts.get(key(a['url']))
  if a.get('http_status')==200 and a.get('text_length',0)>180 and o and o.get('http_status')==200:
   comp.append({'url':a['url'],'current_evidence':a['evidence_file'],'previous_evidence':o['evidence_file'],'whole_retrieved_text_compared':True,'equal':body(a)==body(o)})
 currentmaster=next((c for c in comp if key(c['url'])==key(s['master_url'])),None)
 history=pr.get('observed_facts',[]) if pr.get('observed_facts') and not pr['observed_facts'][0].startswith('Current whole published content') else pr.get('prior_semantic_findings',[])
 historical_source=str(OLD/'reviews.json')
 observed=manual.get(sid)
 if not observed and any(c['equal']for c in comp):
  observed='Fresh whole official page content was explicitly compared with the prior named-protocol review. No published clinical delta in the compared content. Reconciled source-specific findings: '+' '.join(history)
 elif not observed and not allattempts:
  observed='No new source visit. Reviewed exact existing access/action gates and retained source-specific historical questions: '+' '.join(history)
 elif not observed:
  observed='Fresh allowed native/Web route results reviewed; insufficient current text is not a zero-trial roster. Source-specific retained question: '+str(pg.get('question')or pr.get('remaining_fact'))
 absent=[u for u in urls if key(u)not in {key(a['url'])for a in allattempts} and key(u)not in denykeys]
 latest={key(a['url']):a for a in aa}
 missingweb=[a['url']for a in latest.values()if (a.get('http_status')!=200 or a.get('text_length',0)<100)and a.get('http_status')!=403 and key(a['url'])not in {key(w['url'])for w in web}]
 steps=['Read permitted configured official URL '+u for u in absent]+['Use same-URL Web fallback '+u for u in missingweb]
 semanticbasis=bool(manual.get(sid)or(history and (comp or withheld or allattempts)))
 complete=semanticbasis and not steps
 if sid in ('brazil-usp-onvex-precision-oncology','sweden-slu-oxc101-canine-oncology'):
  complete=False;steps=['Establish exact permissible action scope and compliant source-specific completion; do not request or bypass the withheld FAPESP route.']
 suff=bool(prior.get('content_sufficient')and currentmaster and currentmaster['equal']and not steps)
 if sid=='japan-kamogawa-oncology-news':suff=True
 if sid==newid:suff=False
 assessment='complete'if suff and complete else 'external_blocker'if complete else 'executor_unfinished'if (absent or missingweb)else 'not_established'
 result='not_checked'if not allattempts else 'fully_reconciled'if suff else prior.get('source_result','partial')
 if result in ('fully_reconciled','not_checked')and not suff and allattempts:result='partial'
 if sid=='uk-cambridge-veterinary-clinical-trials':result='unreachable'
 # Prior roster is current only after the full current master is explicitly compared.
 roster=copy.deepcopy(prior.get('current_roster'))if currentmaster and currentmaster['equal']else None
 count=prior.get('protocols_seen')if roster is not None else None
 if sid=='japan-kamogawa-oncology-news':roster=['jp-multicenter-oral-melanoma-anti-pd1-2026'];count=1
 if sid=='registry-avma-veterinary-clinical-trials':
  ar=read(R/'avma-reconciliation.json')['retained_dispositions']['rows'];roster=[{'protocol_id':z.get('vct_code'),'id':z['registry_id'],'title':z['title'],'status':z['registry_status']}for z in ar];count=len(roster)
 if sid==newid:roster=[{'project':'u10335','disposition':'WATCH_NOT_CURRENT_INTAKE_VERIFIED'},{'project':'u7937','disposition':'WATCH_NOT_CURRENT_INTAKE_VERIFIED'}];count=2
 question=special_questions.get(sid)or pg.get('question')or pr.get('remaining_fact')or('Current named oncology roster not established for '+s['name'])
 previous={k:s.get(k)for k in ('last_checked','last_checked_at','last_result')}
 if allattempts:
  last=max(allattempts,key=lambda a:a.get('completed_at',a.get('attempted_at','')));at=last.get('completed_at',last.get('attempted_at'))
  s.update(last_checked=at[:10],last_checked_at=at,last_result='unchanged'if suff else result,content_sufficient=suff,last_audit_run_id=R.name,last_protocols_seen=count,last_attempts=allattempts,last_route_used=sorted({a['method']for a in allattempts}),last_coverage_receipt=str(R.relative_to(ROOT)/'receipt-final.json'),last_http_status=last.get('http_status'))
  master=next((a for a in reversed(aa)if key(a['url'])==key(s['master_url'])and a.get('http_status')==200 and a.get('text_length',0)>180),None)
  if master:s['content_fingerprint']='sha256:'+master['text_sha256']
  if not suff:s['last_coverage_gap']=question
 row={'source_id':sid,'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':bool(allattempts),'content_sufficient':suff,'source_result':result,'master_result':'unchanged'if suff else result,'protocols_seen':count,'current_roster':roster,'attempted_urls':allattempts,'route_used':sorted({a['method']for a in allattempts}),'protocol_pages_checked':[a for a in aa if 'protocol'in a.get('route','')or'individual'in a.get('route','')],'processing_complete':complete,'processing_assessment':assessment,'unperformed_steps':steps,'previous_last_checked':previous['last_checked'],'previous_last_checked_at':previous['last_checked_at'],'new_last_checked':s.get('last_checked'),'new_last_checked_at':s.get('last_checked_at'),'new_last_result':s.get('last_result'),'withheld_routes':withheld,'web_evidence':ww}
 reviews.append({'source_id':sid,'reviewed_at':now(),'observed_facts':[observed],'historical_named_protocol_findings':history,'historical_comparison_source':historical_source,'fresh_literal_comparison':comp,'current_roster_basis':'whole fresh master comparison'if currentmaster and currentmaster['equal']else'manual current primary reconciliation'if roster is not None else'NOT_ESTABLISHED','current_roster':roster,'processing_complete':complete,'processing_assessment':assessment,'remaining_fact':None if suff else question,'unperformed_steps':steps,'actual_evidence_files':sorted({a['evidence_file']for a in allattempts})})
 if not suff:
  cat=pg.get('category','roster_unestablished')
  if sid==newid:cat='discovery_source_not_trial_roster'
  if sid in ('uk-cambridge-veterinary-clinical-trials','denmark-copenhagen-veterinary-research'):cat='source_unavailable'
  if not allattempts and withheld:
   row['attempted_urls']=[{'url':s['master_url'],'method':'restriction_review_no_request','result':'withheld_known_action_or_access_gate','new_visit':False,'evidence_file':str(R.relative_to(ROOT)/'restrictions-frozen.json')}]
  gap={'source_id':sid,'category':cat,'processing_assessment':assessment,'question':question,'reason':observed,'next_action':'Continue daily permitted master/fallback visits. Read new individual primary evidence when published or when the retained seven-day question is due. Respect exact access/action gates; no outreach performed.','evidence':{'source_id':sid,'attempted_urls':[a['url']for a in row['attempted_urls']]},'unperformed_steps':steps}
  if assessment=='external_blocker':gap['completion_decision']={'remaining_fact':question,'routes_exhausted_evidence':{'actual_current_attempts':allattempts,'exact_withheld_routes':withheld,'unattempted_permitted_configured_urls':absent},'available_reconciliation_done_evidence':{'source_id':sid,'actual_source_specific_review':observed,'fresh_whole_page_comparisons':comp,'historical_questions_not_automatically_closed':history,'catalog_compared':'data/trials_base.json;315 canonical/155 public; clinical selection unchanged'}}
  gaps.append(gap)
 rows.append(row);dates.append({'source_id':sid,'previous':previous,'new':{k:s.get(k)for k in previous},'attempted':bool(allattempts),'unvisited_dates_preserved':bool(allattempts)or previous=={k:s.get(k)for k in previous}})
receipt={'run_id':R.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':read(R/'baseline.json')['started_at'],'at':now(),'source_total':len(rows),'attempted_total':sum(r['opened_this_run']for r in rows),'content_sufficient_total':sum(r['content_sufficient']for r in rows),'processing_complete_total':sum(r['processing_complete']for r in rows),'source_result_counts':dict(collections.Counter(r['source_result']for r in rows)),'executor_incomplete_source_ids':[r['source_id']for r in rows if not r['processing_complete']],'discovery_regions_processed':12,'discovery_passes':2,'sources':rows}
write(R/'reviews.json',reviews);write(R/'receipt-final.json',receipt);write(R/'gap-review.json',{'original_run_id':R.name,'reviewed_at':now(),'rows':gaps});write(R/'source-date-changes.json',dates);write(ROOT/'data/source_inventory.json',inv);write(ROOT/'data/audit_source_coverage.json',receipt)
state=read(R/'before-audit_state.json');state['last_incremental_audit']={'run_id':R.name,'started_at':receipt['started_at'],'at':now(),'status':'INCOMPLETE','source_total':len(rows),'source_processing_completed':receipt['processing_complete_total'],'source_attempted':receipt['attempted_total'],'source_receipt':str((R/'receipt-final.json').relative_to(ROOT)),'clinical_reconciliation':'INCOMPLETE','prior31_remaining':31,'new_active_trials':0,'new_sources':[newid],'execution_note':'All current requests filtered against frozen restrictions before dispatch. No FAPESP request or bypass; two permission/completion scopes remain NOT VERIFIED.'};write(ROOT/'data/audit_state.json',state)
write(R/'checkpoint-reconciled.json',{k:v for k,v in receipt.items()if k!='sources'});print(json.dumps({k:v for k,v in receipt.items()if k!='sources'},ensure_ascii=False,indent=2))
