#!/usr/bin/env python3
import concurrent.futures, datetime as dt, hashlib, html, json, pathlib, re, threading, time
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from urllib.request import Request, build_opener
from urllib.error import HTTPError, URLError
from zoneinfo import ZoneInfo

ROOT=pathlib.Path(__file__).resolve().parents[3]
RUN=pathlib.Path(__file__).resolve().parent
ET=ZoneInfo('America/New_York')
UA='VetTrialFinderAudit/2026-11-11 (+https://vettrialfinder.com/how-we-verify/)'

def now(): return dt.datetime.now(ET).isoformat()
def norm(u):
    p=urlsplit(u.strip())
    host=p.netloc.lower().removeprefix('www.')
    path=re.sub('/+','/',p.path or '/').rstrip('/') or '/'
    q=urlencode(sorted((k,v) for k,v in parse_qsl(p.query,keep_blank_values=True)
                       if k.lower() not in {'utm_source','utm_medium','utm_campaign','utm_term','utm_content','ref'}))
    return urlunsplit((p.scheme.lower() or 'https',host,path,q,''))

def strip_text(data,ctype):
    s=data.decode('utf-8','replace')
    if 'html' not in (ctype or '').lower() and not s.lstrip().startswith('<'):
        return s
    s=re.sub(r'(?is)<(script|style|noscript|svg).*?</\1>',' ',s)
    s=re.sub(r'(?s)<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',html.unescape(s)).strip()

restriction_doc=json.loads((ROOT/'data/source_access_restrictions.json').read_text())
restricted={norm(x['url']):x for x in restriction_doc.get('routes',[]) if x.get('do_not_retry')}
inv=json.loads((ROOT/'data/source_inventory.json').read_text())
sources=inv if isinstance(inv,list) else inv['sources']
for s in sources:
    for x in s.get('access_restrictions') or []:
        if x.get('do_not_retry') and x.get('url'): restricted.setdefault(norm(x['url']),x)

sems={}; lock=threading.Lock()
def sem_for(url):
    host=urlsplit(url).netloc.lower()
    with lock: return sems.setdefault(host,threading.Semaphore(2))

def one(url):
    attempted=now(); n=norm(url)
    if n in restricted:
        return {'url':url,'attempted':False,'restricted':True,'attempted_at':None,'completed_at':now(),
                'method':'restriction_guard','result':'not_requested_exact_restriction',
                'restriction':restricted[n]}
    out={'url':url,'attempted':True,'restricted':False,'attempted_at':attempted,'method':'python_urllib','retry_count':0}
    with sem_for(url):
      for attempt in range(2):
        try:
            req=Request(url,headers={'User-Agent':UA,'Accept':'text/html,application/json,application/pdf;q=0.9,*/*;q=0.5','Accept-Encoding':'identity'})
            with build_opener().open(req,timeout=20) as r:
                data=r.read(5_000_001); status=getattr(r,'status',200); headers=dict(r.headers.items())
                out.update(http_status=status,effective_url=r.geturl(),content_type=headers.get('Content-Type',''),headers={k:v for k,v in headers.items() if k.lower() in {'content-type','last-modified','etag','retry-after'}},result='retrieved')
                break
        except HTTPError as e:
            data=e.read(5_000_001) if hasattr(e,'read') else b''; status=e.code; headers=dict(e.headers.items()) if e.headers else {}
            out.update(http_status=status,effective_url=e.geturl(),content_type=headers.get('Content-Type',''),headers={k:v for k,v in headers.items() if k.lower() in {'content-type','last-modified','etag','retry-after'}},result=f'http_{status}')
            if attempt==0 and (status==429 or 500<=status<600):
                out['retry_count']=1
                try: wait=min(10,max(0,int(headers.get('Retry-After','0'))))
                except: wait=0
                if wait: time.sleep(wait)
                continue
            break
        except (URLError,TimeoutError,OSError) as e:
            data=b''; out.update(http_status=None,effective_url=url,content_type='',headers={},result=f'transport_{type(e).__name__}',error=str(e)[:500])
            if attempt==0:
                out['retry_count']=1; continue
            break
    text=strip_text(data,out.get('content_type'))
    # redact copied third-party Google API keys without logging values
    text=re.sub(r'AIza[0-9A-Za-z_-]{35}', '[REDACTED_GOOGLE_API_KEY]', text)
    out.update(body_sha256=hashlib.sha256(data).hexdigest(),body_bytes=len(data),text_sha256=hashlib.sha256(text.encode()).hexdigest(),text_length=len(text),text_excerpt=text[:1200],completed_at=now())
    return out,text[:100000]

def fetch_job(job):
    src,route,url=job
    got=one(url)
    if isinstance(got,tuple): meta,txt=got
    else: meta,txt=got,''
    meta.update(source_id=src['id'],route=route)
    key=hashlib.sha256((src['id']+'\0'+route+'\0'+url).encode()).hexdigest()[:20]
    d=RUN/'evidence'/route; d.mkdir(parents=True,exist_ok=True)
    jp=d/f'{key}.json'; tp=d/f'{key}.txt'
    if txt: tp.write_text(txt); meta['text_file']=str(tp.relative_to(ROOT))
    else: meta['text_file']=None
    jp.write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    meta['evidence_file']=str(jp.relative_to(ROOT))
    return meta

masters=[(s,'master',s['master_url']) for s in sources]
fallbacks=[]
for s in sources:
    for u in s.get('fallback_urls') or []: fallbacks.append((s,'fallback',u))

def run_batch(jobs):
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        fs=[ex.submit(fetch_job,j) for j in jobs]
        for f in fs: rows.append(f.result())
    return rows

master_rows=run_batch(masters)
(RUN/'master-index.json').write_text(json.dumps(master_rows,ensure_ascii=False,indent=2))
fallback_rows=run_batch(fallbacks)
(RUN/'fallback-index.json').write_text(json.dumps(fallback_rows,ensure_ascii=False,indent=2))
summary={
 'run_id':RUN.name,'completed_at':now(),'source_count':len(sources),'master_jobs':len(masters),'fallback_jobs':len(fallbacks),
 'master_attempted':sum(x['attempted'] for x in master_rows),'master_restricted':sum(x['restricted'] for x in master_rows),
 'fallback_attempted':sum(x['attempted'] for x in fallback_rows),'fallback_restricted':sum(x['restricted'] for x in fallback_rows),
 'master_statuses':{},'fallback_statuses':{}
}
from collections import Counter
summary['master_statuses']=dict(Counter(str(x.get('http_status')) for x in master_rows if x['attempted']))
summary['fallback_statuses']=dict(Counter(str(x.get('http_status')) for x in fallback_rows if x['attempted']))
(RUN/'source-traversal-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
