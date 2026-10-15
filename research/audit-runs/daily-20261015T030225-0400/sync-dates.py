"""Mechanical date readback from actual attempts; never marks work complete."""
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
actual=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()]
actual+=read(P/'web-attempts.json') if (P/'web-attempts.json').exists() else []
actual+=read(P/'browser-attempts.json') if (P/'browser-attempts.json').exists() else []
reviews={r['source_id']:r for r in read(P/'reviews.json')}
inventory=read(ROOT/'data/source_inventory.json');baseline={s['id']:s for s in read(P/'before-source_inventory.json')['sources']}
readback=[]
for s in inventory['sources']:
 sid=s['id'];urls={s['master_url']}|set(s.get('fallback_urls',[]))
 evidence=[a for a in actual if a['source_id']==sid or a['url'] in urls]
 if not evidence:continue
 evidence.sort(key=lambda a:datetime.fromisoformat(a['attempted_at']))
 last=evidence[-1];at=datetime.fromisoformat(last['attempted_at']).astimezone(ZoneInfo('America/New_York'))
 review=reviews.get(sid,{})
 s['last_checked']=at.date().isoformat();s['last_checked_at']=at.isoformat()
 s['last_result']='reachable' if review.get('content_sufficient') else 'unreachable' if review.get('source_result')=='unreachable' else 'partial'
 s['last_http_status']=last.get('http_status');s['audit_last_run_id']=P.name
 s['last_check_summary']=review.get('reconciliation','Actual retrieval recorded; source reconciliation not yet completed. This is not successful content coverage.')
 keep=('source_id','url','effective_url','route','method','attempted_at','completed_at','http_status','retry','result','text_sha256','evidence_file','evidence_reference','crawl_freshness','exit_code')
 s['last_attempts']=[{k:a[k] for k in keep if k in a} for a in evidence]
 master=[a for a in evidence if a['url'].rstrip('/')==s['master_url'].rstrip('/') and a.get('result')=='retrieved_page' and (a.get('text_length') or 0)>200 and (a.get('http_status')==200 or a['method']=='Web' and a.get('crawl_freshness')=='today')]
 if master:
  s['content_fingerprint']='sha256:'+master[-1]['text_sha256'];s['content_fingerprint_method']=master[-1]['method']+'_retrieved_text'
 readback.append({'source_id':sid,'previous_last_checked':baseline[sid].get('last_checked'),'previous_last_checked_at':baseline[sid].get('last_checked_at'),'new_last_checked':s['last_checked'],'new_last_checked_at':s['last_checked_at'],'new_last_result':s['last_result'],'evidence_last_attempted_at':last['attempted_at'],'local_readback':'PASS'})
inventory['updated']=datetime.now(ZoneInfo('America/New_York')).date().isoformat();write(ROOT/'data/source_inventory.json',inventory)
disk=read(ROOT/'data/source_inventory.json');assert [s['id'] for s in disk['sources']]==list(baseline)
unvisited=[s['id'] for s in disk['sources'] if not any(r['source_id']==s['id'] for r in readback)]
for s in disk['sources']:
 if s['id'] in unvisited:
  assert s.get('last_checked')==baseline[s['id']].get('last_checked') and s.get('last_checked_at')==baseline[s['id']].get('last_checked_at')
write(P/'local-date-readback.json',{'run_id':P.name,'verified_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'status':'PASS','attempted_current_dates':len(readback),'unvisited_dates_unchanged':unvisited,'rows':readback})
print('Actual date metadata local PASS:',len(readback),'unvisited unchanged:',len(unvisited))
