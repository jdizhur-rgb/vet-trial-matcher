"""Keep real Web retrieval times/references, never claim shell HTTP status."""
import json,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent
inv=json.loads((P/'before-source_inventory.json').read_text())['sources']
def norm(u):return str(u).rstrip('/')
known={norm(u):s['id'] for s in inv for u in [s['master_url']]+s.get('fallback_urls',[])}
for line in (P/'attempts.jsonl').read_text().splitlines():
    a=json.loads(line);known.setdefault(norm(a['url']),a['source_id'])
rows=[]
for p in sorted(P.glob('web-*.json')):
    if not re.fullmatch(r'web-\d+\.json',p.name):continue
    obj=json.loads(p.read_text());when=datetime.strptime(obj['at']['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
    text='\n'.join(x.get('text','') for x in obj['result'].get('content',[]) if x.get('type')=='text')
    sections=re.split(r'\n\s*-{20,}\s*\n',text)
    requests=obj.get('urls') or obj.get('clicks') or obj.get('operations') or []
    assert len(sections)==len(requests),(p.name,len(sections),len(requests))
    for n,(s,req) in enumerate(zip(sections,requests)):
        header=re.search(r'^.*?\((https?://[^\n]+)\)\s*\n',s.strip())
        url=req if isinstance(req,str) else req.get('url') or (header.group(1) if header else None)
        assert url,(p.name,n)
        sid=(req.get('source_id') if isinstance(req,dict) else None) or known.get(norm(url))
        if not sid:
            # Explicit source group for navigation-only routes absent from inventory.
            sid={'web-03.json':'usa-colorado-state-vth-clinical-trials','web-09.json':'usa-johns-hopkins-cigat','web-11.json':'usa-purdue-wcorc-clinical-trials','web-12.json':'usa-purdue-wcorc-clinical-trials'}.get(p.name)
        assert sid,(p.name,url)
        ref=re.search(r'【(turn\d+(?:view|search)\d+)】',s)
        crawl=re.search(r'Crawled: ([^;\n]+)',s)
        err=bool(re.search(r'Internal Error|not accessible via this tool|Failed to fetch',s))
        denied=bool(re.search(r'\(403\)|CAPTCHA|attestation',s,re.I))
        rows.append({'source_id':sid,'url':url,'method':'Web','route':'master' if norm(url)==norm(next(x['master_url'] for x in inv if x['id']==sid)) else 'official_fallback_or_protocol','attempted_at':when,'result':'explicit_denial' if denied else 'read_error' if err else 'retrieved_page','evidence_reference':ref.group(1) if ref else None,'evidence_file':str(p.relative_to(P.parents[2])),'section_index':n,'crawl_freshness':crawl.group(1) if crawl else 'unknown','http_status':403 if denied else None,'text_sha256':hashlib.sha256(s.encode()).hexdigest(),'text_length':len(s),'new_visit_this_run':True})
(P/'web-attempts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Web actual retrievals:',len(rows))
