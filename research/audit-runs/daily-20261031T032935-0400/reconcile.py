"""Record today's reviewed whole-content comparisons and individual decisions."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,unquote,parse_qsl
import json,hashlib,collections,re,copy
R=Path(__file__).resolve().parent;ROOT=R.parents[2];OLD=R.parent/'daily-20261031T025801-0400'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def key(u):
 p=urlsplit(u);return ((p.hostname or '').removeprefix('www.'),unquote(p.path).rstrip('/'),tuple(sorted(parse_qsl(p.query,keep_blank_values=True))))
def body(a):return read(ROOT/a['evidence_file'])['text']
attempts=[json.loads(l)for l in(R/'attempts.jsonl').read_text().splitlines()]
oldattempts={key(a['url']):a for a in map(json.loads,(OLD/'attempts.jsonl').read_text().splitlines())}
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
for w in web:
 if '/studies/UK-VCSR-2026-00001' in w['url']:w['source_id']='registry-uk-vcsr'
 elif 'unlimited.lsu.edu/vetmed/blog/2026/cancer_research.php' in w['url']:w['source_id']='usa-lsu-vet-clinical-trials'
 elif 'curelaboncology.com/comparative-medicine' in w['url']:w['source_id']='sponsor-curelab-veterinary-research'
write(R/'web-attempts.json',web)
inv=read(R/'before-source_inventory.json')
newid='brazil-ufpel-electroporation-oncology-project'

manual={
'usa-colorado-state-vth-clinical-trials':'Current complete clinical roster compared against the preceding run; only the anti-spam validation field label changed Email to Phone. Oncology identities and clinical content unchanged.',
'usa-michigan-state-oncology-trials':'Native master and five individual pages returned Incapsula protective stubs. Same-URL master Web timed out. Five full individual pages read through Web, cache3-4days: CHOP/LOPP, HS quasiorganelle, MCT steroids, feline metastatic mammary miR10b, STING CMP002. Eligibility, treatment and funding compared with all five complete canonical records; no material delta found. Cache age and inaccessible live roster prevent a new current clinical signoff; verified dates preserved.',
'registry-uk-vcsr':'Current registry index compared with preceding run; individual UK-VCSR-2026-00001 additionally read. It explicitly says AI-generated sample and not a real recruiting study. No real treatment lead from that result.',
'usa-lsu-vet-clinical-trials':'Current official clinical-trials master compared. Newly surfaced official news article additionally read, explicitly dated12May2026: historical ongoing SCC intratumoral chemotherapy description, eleven visits over four months, without present intake or owner funding confirmation. Existing SCC news/current-index conflict retained, no reopening.',
'sponsor-curelab-veterinary-research':'Current source and comparative-veterinary page reviewed. Historical Elenagen pilot findings plus a generic invitation to inquire, without a named current protocol, confirmed sites, eligibility and owner charges. Prior questions retained; no activation.',
'italy-bologna-oncology-clinical-trials':'Fresh complete native official master explicitly lists three protocols all CONCLUSO: canine appendicular OSA, canine malignant melanoma, canine visceral/cardiac HSA. Entire named roster compared with canonical: no Bologna entries, no activation or closure required. Zero currently open protocols on that retrieved roster. Same-URL Web503 does not invalidate actual native content.',
'brazil-ufpel-electroporation-oncology-project':'Both complete project pages and coordinator profile compared with preceding run; only generated-page timestamps changed. Two therapeutic project leads unchanged, present intake and costs remain unpublished.',
'uk-valirx-animal-health':'Current master/news unchanged; native pipeline failed, same-URL Web recovered pipeline with cache last week. Explicitly no current pet-trial recruitment; future network and biospecimen collaborations are not owner-enrolling treatment. Prior October30 educational article is historical, not reread today.'}

special_questions={
 'registry-avma-veterinary-clinical-trials':'Recovered current856/oncology471 registry roster; exact23 institutional current-intake/site/funding questions remain in avma-reconciliation.json, without activation from registry status.',
 'uk-cambridge-veterinary-clinical-trials':'Current institutional oncology roster and individual OSA research status cannot be established from503 followed by exact-route403; prior blood-sampling study is not a new therapy.',
 'brazil-usp-onvex-precision-oncology':'Compliant action scope and current programme reconciliation for the withheld FAPESP route remain unestablished; no bypass request is allowed.',
 'sweden-slu-oxc101-canine-oncology':'The supporting FAPESP action scope remains unestablished; no open owner oncology protocol or complete processing signoff from a grant alone.',
 newid:'Are either electroporation u10335 or eyelid-surgery u7937 currently accepting owner referrals, at which participating site, with what eligibility confirmation and owner charges? Published project periods and general coordinator profile do not establish present trial access.'}
denials=read(R/'restrictions-frozen.json')+[dict(x,method='automatic_review_scope_withheld_no_request',new_visit=False,origin=str(R/'automatic-review-rejection.json'))for x in read(R/'automatic-review-rejection.json')['withheld']]+[json.loads(l)for l in(R/'new-denials.jsonl').read_text().splitlines()]
# The run's explicit FAPESP action-scope exclusion also withholds the separate
# SLU support-grant URL; it is not an unperformed permitted network request.
denials += [dict(d,method='planning_restriction_review_no_request',new_visit=False)for d in read(R/'withheld.json')if 'fapesp.br'in d['url']and key(d['url'])not in {key(z['url'])for z in denials}]
denykeys={key(d['url'])for d in denials}
reviews=[];rows=[];gaps=[];dates=[]
for s in inv['sources']:
 sid=s['id'];prior=priorrows.get(sid,{});pr=priorreviews.get(sid,{});pg=priorgaps.get(sid,{})
 urls=[s['master_url']]+s.get('fallback_urls',[]);keys={key(u)for u in urls}
 aa=[a for a in attempts if a['source_id']==sid or key(a['url'])in keys];ww=[w for w in web if w.get('source_id')==sid or key(w['url'])in keys|{key(a['url'])for a in aa}];allattempts=aa+ww
 withheld=[d for d in denials if key(d['url'])in keys];comp=[]
 for a in aa:
  o=oldattempts.get(key(a['url']))
  if a.get('http_status')==200 and a.get('text_length',0)>180 and o and o.get('http_status')==200:
   comp.append({'url':a['url'],'current_evidence':a['evidence_file'],'previous_evidence':o['evidence_file'],'whole_retrieved_text_compared':True,'equal':body(a)==body(o)})
 currentmaster=next((c for c in comp if key(c['url'])==key(s['master_url'])),None)
 history=pr.get('historical_named_protocol_findings',[]) or pr.get('observed_facts',[])
 historical_source=str(OLD/'reviews.json')
 observed=manual.get(sid)
 if not observed and any(c['equal']for c in comp):
  observed='Current whole official page compared with the preceding run; no clinical delta. Historical named findings (not new protocol readings): '+' '.join(history)
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
 if sid in ('brazil-usp-onvex-precision-oncology','sweden-slu-oxc101-canine-oncology','brazil-usp-loct-oncolytic-virus-program','br-usp-fmvz-clinical-recruitment-news'):
  complete=False;steps=['Establish permitted source-specific scope and compliant completion after the recorded automatic-review restriction for '+sid+'; no request or bypass of withheld USP/FAPESP routes.']
 suff=bool(prior.get('content_sufficient')and currentmaster and currentmaster['equal']and not steps)
 if sid in ('usa-colorado-state-vth-clinical-trials','italy-bologna-oncology-clinical-trials'):suff=True

 assessment='complete'if suff and complete else 'external_blocker'if complete else 'executor_unfinished'if (absent or missingweb)else 'not_established'
 result='not_checked'if not allattempts else 'fully_reconciled'if suff else prior.get('source_result','partial')
 if result in ('fully_reconciled','not_checked')and not suff and allattempts:result='partial'
 if sid=='uk-cambridge-veterinary-clinical-trials':result='unreachable'if allattempts else'not_checked'
 # Prior roster is current only after the full current master is explicitly compared.
 roster=copy.deepcopy(prior.get('current_roster'))if currentmaster and currentmaster['equal']else None
 count=prior.get('protocols_seen')if roster is not None else None
 if sid=='usa-colorado-state-vth-clinical-trials':roster=prior.get('current_roster');count=prior.get('protocols_seen')
 if sid=='italy-bologna-oncology-clinical-trials':roster=[{'title':t,'status':'CONCLUSO'}for t in ['Osteosarcoma appendicolare del cane','Melanoma maligno del cane','Emangiosarcoma viscerale e cardiaco del cane']];count=3
 if sid=='registry-avma-veterinary-clinical-trials':
  ar=read(R/'avma-reconciliation.json')['retained_dispositions']['rows'];roster=[{'protocol_id':z.get('vct_code'),'id':z['registry_id'],'title':z['title'],'status':z['registry_status']}for z in ar];count=len(roster)

 question=special_questions.get(sid)or pg.get('question')or pr.get('remaining_fact')or('Current named oncology roster not established for '+s['name'])
 previous={k:s.get(k)for k in ('last_checked','last_checked_at','last_result')}
 if allattempts:
  last=max(allattempts,key=lambda a:a.get('completed_at',a.get('attempted_at','')));at=last.get('completed_at',last.get('attempted_at'))
  s.update(last_checked=at[:10],last_checked_at=at,last_result='unchanged'if suff else result,content_sufficient=suff,last_audit_run_id=R.name,last_protocols_seen=count,last_attempts=allattempts,last_route_used=sorted({a['method']for a in allattempts}),last_coverage_receipt=str(R.relative_to(ROOT)/'receipt-final.json'),last_http_status=last.get('http_status'))
  master=next((a for a in reversed(aa)if key(a['url'])==key(s['master_url'])and a.get('http_status')==200 and a.get('text_length',0)>180),None)
  if master:s['content_fingerprint']='sha256:'+master['text_sha256']
  if not suff:s['last_coverage_gap']=question
  else:s.pop('last_coverage_gap',None)
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
state=read(R/'before-audit_state.json');state['last_incremental_audit']={'run_id':R.name,'started_at':receipt['started_at'],'at':now(),'status':'INCOMPLETE','source_total':len(rows),'source_processing_completed':receipt['processing_complete_total'],'source_attempted':receipt['attempted_total'],'source_receipt':str((R/'receipt-final.json').relative_to(ROOT)),'clinical_reconciliation':'INCOMPLETE','prior31_remaining':31,'new_active_trials':0,'new_sources':[],'execution_note':'All current requests filtered against frozen restrictions before dispatch. No FAPESP request or bypass; four permission/completion scopes remain NOT VERIFIED; excluded mixed-action results are not used.'};write(ROOT/'data/audit_state.json',state)
write(R/'checkpoint-reconciled.json',{k:v for k,v in receipt.items()if k!='sources'});print(json.dumps({k:v for k,v in receipt.items()if k!='sources'},ensure_ascii=False,indent=2))
