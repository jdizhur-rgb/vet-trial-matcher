import json,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
RUN=Path(__file__).parent
RAW=Path('/tmp/vtf-daily-raw').read_text().strip()
inv=json.loads((RUN/'before-source_inventory.json').read_text())['sources']
native=[json.loads(l) for l in (RUN/'shell-attempts.jsonl').read_text().splitlines()]
byurl={a['url']:a['source_id'] for a in native}
for s in inv:
 for u in [s['master_url'],*s.get('fallback_urls',[])]:byurl[u]=s['id']
fixed={2:['usa-colorado-state-vth-clinical-trials','usa-auburn-vet-clinical-trials'],3:['usa-michigan-state-oncology-trials','usa-lsu-vet-clinical-trials'],4:['usa-johns-hopkins-cigat'],5:['usa-nc-state-clinical-trials','usa-ohio-state-current-trials','usa-oregon-state-oncology-trials','usa-purdue-wcorc-clinical-trials','usa-tennessee-vet-clinical-trials'],6:['usa-purdue-wcorc-clinical-trials','usa-tennessee-vet-clinical-trials','usa-ohio-state-current-trials','usa-ohio-state-current-trials','usa-ohio-state-current-trials',None]}
rows=[]
for p in sorted([*Path(RAW).glob('web*.json'),*Path(RAW).glob('local*.json'),*Path(RAW).glob('primary*.json')]):
 w=json.loads(p.read_text());
 if p.name=='web47.json':continue # mistaken reference resolved Penn generic programmes, excluded from source coverage
 label=int(re.search(r'(\d+)\.json',p.name)[1]);blocks=[]
 for c in w['result'].get('content',[]):
  if c.get('type')=='text':blocks += re.split(r'\n-{10,}\n',c['text'])
 at=w.get('attempted_at') or w.get('attempted_atUTC')
 if not at:continue
 if ' UTC' in at:at=datetime.strptime(at,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
 for i,b in enumerate(blocks):
  if not b.strip():continue
  first=b.splitlines()[0];m=re.search(r'\((https?://[^\s]+)\)',first);url=m[1] if m else None
  if not url:
   m=re.search(r'"ref_id":"(https?://[^"]+)"',b);url=m[1] if m else None
  if not url:continue # a failed click with no resolved URL is not a source visit
  sid=byurl.get(url)
  req=next((x for x in w.get('requests',[]) if x.get('url')==url),None)
  if not sid and req:sid=req['source_id']
  if not sid:
   unique={q.get('source_id') for q in w.get('requests',[]) if q.get('source_id')}
   if len(unique)==1:sid=next(iter(unique))
  if not sid and label in fixed and i<len(fixed[label]):sid=fixed[label][i]
  if not sid:
   candidates=[(len(u),v) for u,v in byurl.items() if url.startswith(u.rstrip('/'))]
   if candidates:sid=max(candidates)[1]
  aliases={'australia-uq-veterinary-clinical-trials':'australia-uq-school-veterinary-clinical-trials','brazil-usp-loct-oncology-research':'brazil-usp-loct-oncolytic-virus-program'}
  sid=aliases.get(sid,sid)
  if not sid:continue
  ref=re.search(r'【([^】]+)】',b);status=re.search(r'\((\d{3})\)',b)
  fail=bool(re.search(r'Failed to fetch|not accessible via this tool|Internal Error|Total lines: 0|Checking your browser',b,re.I))
  fresh=re.search(r'Crawled: ([^;]+);',b)
  rows.append({'source_id':sid,'url':url,'attempted_at':at,'method':'Web','route':'master' if any(s['id']==sid and s['master_url']==url for s in inv) else 'fallback_or_individual_primary','result':'read_error_or_insufficient' if fail else 'retrieved_page','http_status':int(status[1]) if status else None,'evidence_reference':ref[1] if ref else None,'text_sha256':hashlib.sha256(b.encode()).hexdigest(),'crawl_freshness':fresh[1] if fresh else 'unknown','raw_evidence_file':p.name})
(RUN/'web-attempts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('Web attempts with actual URL and timestamp:',len(rows),'sources:',len({x['source_id'] for x in rows}))
