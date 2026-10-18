"""Current-run evidence indexing and literal before/current comparisons; no signoff inference."""
import json,re,hashlib,collections,difflib
from pathlib import Path
from urllib.parse import urlsplit,unquote,parse_qsl
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).resolve().parent; ROOT=P.parents[2]; OLD=P.parent/'daily-20261017T025640-0400'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def key(u):
 v=urlsplit(u);return ((v.hostname or '').removeprefix('www.'),unquote(v.path).rstrip('/'),tuple(sorted((k,v) for k,v in parse_qsl(v.query) if k!='ref')))
def resolve(p):return ROOT/str(p).split('/research/')[-1] if '/research/' not in str(p) else ROOT/'research'/str(p).split('/research/')[-1]
def ep(p):
 p=Path(p)
 if p.exists():return p
 return ROOT/'research'/str(p).split('research/')[-1]
native=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()]
prior=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
old_by={key(x['url']):x for x in prior if x.get('http_status')==200 and x.get('text_length',0)>100}
comparisons=[]
for a in native:
 b=old_by.get(key(a['url']))
 if not b or a.get('http_status')!=200 or a.get('text_length',0)<100:continue
 c=read(ep(a['evidence_file']));o=read(ep(b['evidence_file']))
 same=c['text']==o['text'];links=sorted(x['url'] for x in c['links'])==sorted(x['url'] for x in o['links'])
 comparisons.append({'source_id':a['source_id'],'url':a['url'],'read_at':a['attempted_at'],'evidence':a['evidence_file'],'prior_evidence':b['evidence_file'],'same_entire_text':same,'same_entire_linkset':links,'changed_text':None if same else '\n'.join(difflib.unified_diff(o['text'].splitlines(),c['text'].splitlines()))[:10000]})
write(P/'current-full-comparisons.json',comparisons)
web=[]
for f in sorted(list(P.glob('web-*.json'))+list(P.glob('kv9-web-*.json'))+list(P.glob('discovery-primary-recovery-*.json'))):
 d=read(f)
 if 'result' not in d or 'urls' not in d:continue
 content='\n'.join(x.get('text','') for x in d['result'].get('content',[]) if x.get('type')=='text')
 blocks=re.split(r'\n[-]{20,}\n',content)
 # Web batch has one separator per page; uncertain matching is explicit, never guessed from count.
 for i,u in enumerate(d['urls']):
  matches=[b for b in blocks if u in b[:1200]]
  block=matches[0] if len(matches)==1 else blocks[i] if len(blocks)==len(d['urls']) else ''
  m=re.search(r'【([^】]+)】',block);crawl=re.search(r'(?:Crawled|Published|Content type|Fetched):[^\n]*',block)
  denied=bool(re.search(r'(?:HTTP|error|status|response|fetch)[^\n]{0,30}\b403\b|Forbidden|Access Denied|blocked by robots|CAPTCHA',block,re.I))
  error=not block or bool(re.search(r'Failed to fetch|Internal Error|Timeout|502 Bad Gateway|500 Internal|HTTP 525|404 Not Found|not accessible via this tool|non-retryable error',block,re.I))
  plan=next((x for x in d.get('plan',[]) if x['url']==u),{})
  ids=[s['id'] for s in read(P/'before-source_inventory.json')['sources'] if key(u) in [key(s['master_url'])]+[key(v) for v in s.get('fallback_urls',[])]]
  web.append({'source_id':plan.get('source_id') or (ids[0] if ids else 'protocol-primary'),'url':u,'method':'Web','route':'same_url_Web_recovery','attempted_at':datetime.strptime(d['at'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat(),'result':'access_denied' if denied else 'retrieval_error' if error else 'retrieved_page','evidence_file':str(f.relative_to(ROOT)),'evidence_reference':m.group(1) if m else None,'freshness':crawl.group(0) if crawl else 'Freshness NOT ESTABLISHED','text_length':len(block),'text_sha256':hashlib.sha256(block.encode()).hexdigest(),'retrieved_text':block,'mapping_verified':bool(block)})
write(P/'web-attempts.json',web)
write(P/'nonretryable-Web-method-failures.json',[x for x in web if x['result']=='retrieval_error' and 'not accessible via this tool' in x['retrieved_text']])
denials=[{'url':x['url'],'observed_at':x['attempted_at'],'origin':x['evidence_file'],'method':'Web','do_not_retry':True,'reason':x['result']} for x in web if x['result']=='access_denied']
extra=P/'new-denials.jsonl';existing=[json.loads(x) for x in extra.read_text().splitlines()] if extra.exists() else []
unique={key(x['url']):x for x in [v for v in existing if v.get('method')!='Web']+denials};extra.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in unique.values()))
public=read(P/'public-frozen.json');latest={key(x['url']):x for x in native if x.get('http_status')==200 and x.get('text_length',0)>100};comp={key(x['url']):x for x in comparisons}
index=[]
for r in public:
 u=r.get('source_url') or r['url'];a=latest.get(key(u));w=[x for x in web if key(x['url'])==key(u)]
 index.append({'trial_id':r['id'],'url':u,'native':a,'comparison':comp.get(key(u)),'web':w,'frozen_requires':r.get('requires',{}),'frozen_excludes':r.get('excludes',{})})
write(P/'trial-evidence-index.json',index)
print(json.dumps({'native':len(native),'web_urls':len(web),'full_comparisons':len(comparisons),'changed_text':[(x['source_id'],x['url']) for x in comparisons if not x['same_entire_text']],'public_native_substantive':sum(bool(x['native']) for x in index)},ensure_ascii=False))
