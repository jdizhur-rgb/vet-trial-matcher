import json,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def norm(u):return u.rstrip('/')
known={norm(u):s['id'] for s in read(P/'before-source_inventory.json')['sources'] for u in [s['master_url']]+s.get('fallback_urls',[])}
for line in (P/'attempts.jsonl').read_text().splitlines():
    a=json.loads(line);known.setdefault(norm(a['url']),a['source_id'])
known["https://vethospital.okstate.edu/clinical-trials.html"]='usa-oklahoma-state-clinical-trials'
rows=[]
for p in sorted(P.glob('web-*.json')):
    if not re.fullmatch(r'web-\d+\.json',p.name):continue
    d=read(p);when=datetime.strptime(d['at']['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
    text='\n'.join(c.get('text','') for c in d['result'].get('content',[]) if c.get('type')=='text');parts=re.split(r'\n\s*-{20,}\s*\n',text)
    assert len(parts)==len(d['urls']),(p,len(parts),len(d['urls']))
    for u,s in zip(d['urls'],parts):
        assert norm(u) in known,(p,u)
        ref=re.search(r'【(turn\d+(?:view|search)\d+)】',s);crawl=re.search(r'Crawled: ([^;\n]+)',s);error=bool(re.search(r'Internal Error|not accessible via this tool|Failed to fetch',s))
        rows.append({'source_id':known[norm(u)],'url':u,'method':'Web','route':'same_url_reader_or_official_fallback','attempted_at':when,'result':'read_error' if error else 'retrieved_page','evidence_reference':ref.group(1) if ref else None,'evidence_file':str(p.relative_to(ROOT)),'crawl_freshness':crawl.group(1) if crawl else 'unknown','http_status':None,'text_sha256':hashlib.sha256(s.encode()).hexdigest(),'text_length':len(s),'new_visit_this_run':True})
(P/'web-attempts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('Actual Web reads',len(rows))
