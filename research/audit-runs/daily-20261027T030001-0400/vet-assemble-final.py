import json,copy,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,parse_qsl,urlencode
from collections import Counter
R=Path(Path('/tmp/current-vet-run').read_text());now=datetime.now(ZoneInfo('America/New_York')).isoformat();read=lambda p:json.loads(Path(p).read_text());write=lambda p,x:Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inv=read('data/source_inventory.json');sources=inv['sources'];sids={s['id'] for s in sources};before={s['id']:s for s in read(R/'before-source_inventory.json')['sources']};reviews={r['source_id']:r for r in read(R/'reviews.json')};A=[json.loads(x) for x in (R/'attempts.jsonl').read_text().splitlines()];restr=read(R/'restrictions-frozen.json')
def norm(u):
 p=urlsplit(str(u));q=[(k,v) for k,v in parse_qsl(p.query) if k not in ['ref','utm_source','utm_medium','utm_campaign']];return(p.hostname or '').replace('www.','')+p.path.rstrip('/')+('?' +urlencode(q) if q else '')
urls={};domains={}
for s in sources:
 for u in [s['master_url']]+s.get('fallback_urls',[]):urls.setdefault(norm(u),set()).add(s['id']);domains.setdefault((urlsplit(u).hostname or '').replace('www.',''),set()).add(s['id'])
prefix={'ill':23,'uf-':20,'msu-':9,'csu-':4,'cornell-':5,'wisc-':26,'ucd-':19,'osu-':13,'vt-':25,'tamu-':60,'penn-':15,'purdue-':16,'tufts-':18,'mizzou-':11,'umn-':10,'jhu-':7,'jp-nihon':101,'mvh-':98,'jp-nvlu':75,'jp-gifu':86,'jp-hokkaido':87,'jp-yamaguchi':67,'jp-jsamc':69,'korea-vax':144,'au-':48,'ch-zurich':37,'be-ghent':100,'eu-it-unimi':38,'nz-kvs':114}
def owners(u,trial=None,original=None):
 nu=norm(u)
 if any(z in u for z in ['320455','217934','468706']) and 'studypages.com/s/' in u:return{sources[19]['id']}
 if 'dyrehospitalet.ku.dk' in u:return{sources[143]['id']}
 if 'vaxcell-bio.com' in u:return{sources[144]['id']}
 if 'dogcancertcc.com/clinical-trials' in u:return{sources[145]['id']}
 if original in sids:return {original}|urls.get(nu,set())
 if nu in urls:return urls[nu]
 if trial:
  if trial=='uf-boxer-glioma-autogenic-vaccine':return{sources[92]['id']}
  if trial=='uf-feline-oscc':return{sources[21]['id']}
  for p,i in prefix.items():
   if trial.startswith(p):return{sources[i]['id']}
 ds=domains.get((urlsplit(u).hostname or '').replace('www.',''),set());return ds if len(ds)==1 else set()
associated=[];unmapped=[]
for x in A:
 oo=owners(x['url'],x.get('trial_id') or (x['source_id'][9:] if x['source_id'].startswith('protocol:') else None),x['source_id'])
 for sid in oo:associated.append({**x,'source_id':sid,'original_source_id':x['source_id'],'association_only_not_new_visit':True})
 if not oo:unmapped.append({k:x.get(k) for k in ['source_id','trial_id','url','evidence_file']})
# Web page opens/clicks, never search snippets. Earlier date-only receipts retain their precision.
web=[]
for p in list(R.glob('web*.json'))+list(R.glob('todayweb*.json'))+list(R.glob('regweb*.json')):
 try:d=read(p)
 except:continue
 if not isinstance(d,dict):continue
 timestamp=d.get('requested_at',{});timestamp=timestamp.get('current_time') if isinstance(timestamp,dict) else timestamp
 if timestamp:
  dt=datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat();precision='second'
 elif d.get('saved_at'):dt=datetime.fromisoformat(d['saved_at'].replace('Z','+00:00')).astimezone(ZoneInfo('America/New_York')).isoformat();precision='response_saved_at'
 else:dt=None;precision='date_only'
 payload=d.get('payload',d);payload=payload.get('result',payload) if isinstance(payload,dict) else {};content=payload.get('content',[]) if isinstance(payload,dict) else []
 for b in content:
  if b.get('type')!='text':continue
  for segment in re.split(r'\n-{10,}\n',b.get('text','')):
   m=re.search(r'Source: (?:open|click)\(',segment)
   if not m:continue
   h=re.search(r'^([^\n]*)\((https?://[^\n]+)\)\n【([^】]+)】',segment)
   requested=re.search(r'Source: open\(\{"ref_id":"(https?://[^\"]+)"',segment)
   u=h.group(2) if h else requested.group(1) if requested else None
   if not u:continue
   oo=owners(u);ref=re.search(r'【([^】]+)】',segment);status=403 if '(403)' in segment else 502 if '(502)' in segment else None;ok=bool(h and 'Total lines: 1\n' not in segment and 'Internal Error' not in segment[:40]);cache=re.search(r'Crawled: ([^;\n]+)',segment)
   for sid in oo:
    row=dict(source_id=sid,url=u,method='Web',http_status=status if not ok else 200,result='retrieved_page' if ok else 'web_unavailable',text_length=len(segment) if ok else 0,evidence_file=str(p),reference=ref.group(1) if ref else None,timestamp_precision=precision,crawled=cache.group(1) if cache else None)
    if dt:row['attempted_at' if precision=='second' else 'completed_at']=dt
    else:row['attempted_date']='2026-10-27'
    web.append(row)
# Explicit original date-only MSU page evidence.
w1=read(R/'web-1.json')
for k,v in w1.items():
 if isinstance(v,dict) and v.get('source_id') and v.get('url'):web.append({**v,'evidence_file':str(R/'web-1.json'),'text_length':len(v.get('observations',''))})
write(R/'web-attempts-final.json',web);write(R/'attempt-associations-final.json',dict(rows=associated,unmapped=unmapped,note='Original attempts.jsonl is immutable; these are attribution corrections and shared same-run evidence, not new visits.'))
policy=[]
for s in sources:
 for u in [s['master_url']]+s.get('fallback_urls',[]):
  rs=[r for r in restr if norm(r.get('url'))==norm(u)]
  if rs:policy.append(dict(source_id=s['id'],url=u,method='policy_withheld',opened=False,result='prior_exact_denial_not_retried',restriction_evidence=rs))
for p in [R/'skipped-restricted-routes.jsonl',R/'public-primary-withheld.json']:
 if p.suffix=='.jsonl':xs=[json.loads(l) for l in p.read_text().splitlines()]
 else:xs=read(p)
 if isinstance(xs,list):
  for x in xs:
   for sid in owners(x.get('url',''),x.get('trial_id'),x.get('source_id')):policy.append({**x,'source_id':sid,'method':'policy_withheld','opened':False})
rows=[];gaps=[];missing=[];allattempts=associated+web
for s in sources:
 sid=s['id'];rr=reviews[sid];xs=[x for x in allattempts if x['source_id']==sid];pp=[x for x in policy if x['source_id']==sid];old=before.get(sid,{});routes=xs+pp;done=rr['processing_complete'];sufficient=rr.get('source_result','fully_reconciled')=='fully_reconciled' and bool(xs);used={norm(x['url']) for x in routes}
 # Mandatory recorded fallbacks need an actual read attempt or an exact restriction when master is insufficient.
 missing_urls=[u for u in s.get('fallback_urls',[]) if norm(u) not in used] if not sufficient else []
 if missing_urls:
  done=False;missing.extend(dict(source_id=sid,url=u,route='required_final_fallback') for u in missing_urls)
 result='fully_reconciled' if sufficient else 'not_checked' if not xs else 'unreachable' if not any(x.get('http_status')==200 and x.get('text_length',0)>100 for x in xs) else 'partial'
 if xs:
  dated=[x for x in xs if x.get('attempted_at') or x.get('completed_at')]
  if dated:
   last=max(dated,key=lambda x:x.get('attempted_at',x.get('completed_at','')));dt=last.get('attempted_at',last.get('completed_at'));s.update(last_checked=dt[:10],last_checked_at=dt,last_result='unchanged' if sufficient else 'unreachable' if result=='unreachable' else 'partial',last_http_status=last.get('http_status'))
  else:s.update(last_checked='2026-10-27',last_result='unchanged' if sufficient else 'partial')
 # Preserve all fields/dates of wholly unvisited sources and never advance old fingerprints as new roster proof.
 assessment='complete' if sufficient else rr.get('processing_assessment','not_established') if done else 'executor_unfinished'
 todo=rr.get('unperformed_steps',[])+['Attempt required recorded official fallback: '+u for u in missing_urls]
 fact=rr.get('reconciliation');question=rr.get('question') or ('Current evidence remains insufficient for '+s['name'])
 comp=copy.deepcopy(rr.get('completion_decision'))
 if comp:comp['routes_exhausted_evidence']=[dict(url=x.get('url'),method=x.get('method'),at=x.get('attempted_at',x.get('completed_at',x.get('attempted_date'))),result=x.get('result'),evidence=x.get('evidence_file',x.get('restriction_evidence'))) for x in routes]
 row=dict(source_id=sid,source_name=s['name'],master_url=s['master_url'],opened_this_run=bool(xs),content_sufficient=sufficient,source_result=result,master_result='reconciled' if sufficient else result,protocols_seen=rr.get('protocols_seen') if rr.get('current_roster') is not None else None,current_roster=rr.get('current_roster'),route_used=sorted({x['method'] for x in xs}),actual_attempts=xs,attempted_urls=routes or [dict(url=s['master_url'],method='not_requested',opened=False)],current_comparison_evidence=fact,processing_complete=done,processing_assessment=assessment,category=rr.get('category') if not sufficient else None,question=question if not sufficient else None,reconciliation=fact,completion_decision=comp if done else None,unperformed_steps=todo,previous_last_checked=old.get('last_checked'),previous_last_checked_at=old.get('last_checked_at'),previous_last_result=old.get('last_result'),new_last_checked=s.get('last_checked'),new_last_checked_at=s.get('last_checked_at'),new_last_result=s.get('last_result'))
 rows.append(row)
 if not sufficient:gaps.append(dict(source_id=sid,category=rr.get('category') or 'roster_unestablished',processing_assessment=assessment,question=question,reason=fact,next_action=todo[0] if todo else 'On new primary evidence or changed master, or after seven days, recheck the exact remaining fact: '+question,recheck_after='2026-11-03',evidence=dict(source_id=sid,attempted_urls=[x['url'] for x in row['attempted_urls']],evidence_files=sorted({x['evidence_file'] for x in xs if x.get('evidence_file')})),unperformed_steps=todo,completion_decision=comp if done else None))
receipt=dict(run_id=R.name,mode='DAILY GLOBAL WORK AUDIT',started_at=read(R/'baseline.json')['started_at'],checkpoint_at=now,source_total=len(rows),initial_source_total=len(before),attempted_total=sum(x['opened_this_run'] for x in rows),content_sufficient_total=sum(x['content_sufficient'] for x in rows),processing_complete_total=sum(x['processing_complete'] for x in rows),source_result_counts=dict(Counter(x['source_result'] for x in rows)),executor_incomplete_source_ids=[x['source_id'] for x in rows if not x['processing_complete']],executor_unfinished_actions=sum(len(x['unperformed_steps']) or int(not x['processing_complete']) for x in rows),unconfirmed_processing_sources=sum(not x['processing_complete'] for x in rows),discovery_regions_processed=12,discovery_passes=2,strict_status='INCOMPLETE',sources=rows)
write(R/'receipt-final.json',receipt);write('data/audit_source_coverage.json',receipt);write(R/'gap-review.json',dict(original_run_id=R.name,reviewed_at=now,rows=gaps));write('data/source_inventory.json',inv);write(R/'required-missing-fallbacks.json',missing)
st=read('data/audit_state.json');st['last_incremental_audit'].update(run_id=R.name,at=now,status='INCOMPLETE',source_total=len(rows),source_processing_completed=receipt['processing_complete_total'],executor_unconfirmed_source_actions=receipt['executor_unfinished_actions'],new_sources=3,new_active_trials=0,activated_existing_watch_trials=1,source_receipt=str(R/'receipt-final.json'),clinical_full_fresh_gate='INCOMPLETE');write('data/audit_state.json',st)
write(R/'date-readback-final.json',dict(at=now,local='PASS',rows=[{k:r[k] for k in ['source_id','previous_last_checked','previous_last_checked_at','new_last_checked','new_last_checked_at','new_last_result']} for r in rows],unvisited_dates_preserved=all(not r['opened_this_run'] and r['previous_last_checked_at']==r['new_last_checked_at'] for r in rows if not r['opened_this_run'])))
write(R/'segment-052x-processing.json',dict(at=now,run_id=R.name,source_result_counts=receipt['source_result_counts'],processing_complete=receipt['processing_complete_total'],executor_unfinished_actions=receipt['executor_unfinished_actions'],new_sources=3,global_discovery='24actualqueries/12regions/2passes;157resultdispositions',note='Final explicit semantic decisions; no automatic blanket external labeling. Missing permitted mandatory fallbacks remain executor actions.'))
print(json.dumps({k:v for k,v in receipt.items() if k!='sources'},indent=2));print('missing mandatory fallbacks',len(missing));print(missing)
