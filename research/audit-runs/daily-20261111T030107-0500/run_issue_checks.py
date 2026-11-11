import json,hashlib,time,re,html
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from concurrent.futures import ThreadPoolExecutor,as_completed
from threading import Semaphore,Lock
from datetime import datetime
from zoneinfo import ZoneInfo
RUN='daily-20261111T030107-0500'; root=Path('research/audit-runs')/RUN; outdir=root/'evidence'/'issues'; outdir.mkdir(parents=True,exist_ok=True)
def norm(u):
 p=urlsplit(u); return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/') or '/',p.query,''))
def now(): return datetime.now(ZoneInfo('America/New_York')).isoformat()
b=json.load(open(root/'execution-baseline.json')); issues=b['issues']
restr=json.load(open('data/source_access_restrictions.json'))
# recursively collect exact route URLs
restricted=set()
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('url','route','exact_url') and isinstance(v,str) and v.startswith('http'): restricted.add(norm(v))
   else: walk(v)
 elif isinstance(x,list):
  for y in x: walk(y)
walk(restr)
existing={}
for f in ['master-index.json','fallback-index.json']:
 for x in json.load(open(root/f)): existing[norm(x['url'])]=x
# additional previously read exact new pages
extra={
 norm('https://veterinaryclinicaltrials.org/s/flash-based-radioimmunotherapy-in-canine-glioma-417438/'):str(root/'evidence/avma-penn-vct26005993-json.json'),
 norm('https://veterinaryclinicaltrials.org/s/radiation-treatment-for-cats-with-small-cell-gi-lymphoma-674332/'):str(root/'evidence/avma-feline-vct26005992-json.json'),
 norm('https://studypages.com/s/radiation-therapy-for-small-cell-gi-lymphoma-in-cats-710678/'):str(root/'evidence/csu-feline-scgl-primary-json.json'),
}
unique={norm(i['primary_url']):i['primary_url'] for i in issues if i.get('primary_url')}
host_sem={}; lock=Lock()
def sem(host):
 with lock:
  if host not in host_sem: host_sem[host]=Semaphore(2)
  return host_sem[host]
class Parser(__import__('html.parser').parser.HTMLParser):
 def __init__(self): super().__init__(); self.d=[]
 def handle_data(self,d):
  d=re.sub(r'\s+',' ',d).strip()
  if d:self.d.append(d)
def fetch(item):
 n,u=item; host=urlsplit(u).netloc.lower(); rec={'url':u,'normalized_url':n,'attempted_at':now(),'method':'python_urllib','retry_count':0}
 if n in extra:
  rec.update({'result':'reused_current_run_evidence','evidence_file':extra[n],'completed_at':now()}); return rec
 if n in existing:
  x=existing[n]; rec.update({'result':'reused_current_run_route','http_status':x.get('http_status'),'evidence_file':x.get('evidence_file'),'text_file':x.get('text_file'),'text_excerpt':x.get('text_excerpt'),'completed_at':now()}); return rec
 if n in restricted:
  rec.update({'result':'not_requested_exact_restriction','restricted':True,'completed_at':now()}); return rec
 with sem(host):
  for attempt in range(2):
   try:
    with urlopen(Request(u,headers={'User-Agent':'VetTrialFinderAudit/1.0'}),timeout=20) as r:
     body=r.read(); status=r.status; eff=r.url; ct=r.headers.get('content-type','')
    rec.update({'http_status':status,'effective_url':eff,'content_type':ct,'body_sha256':hashlib.sha256(body).hexdigest(),'body_bytes':len(body)})
    if 'html' in ct or body[:50].lower().find(b'<html')>=0:
     p=Parser(); p.feed(body.decode('utf-8','replace')); text=' '.join(p.d)
    elif 'json' in ct or body[:1] in (b'{',b'['): text=body.decode('utf-8','replace')
    else: text=''
    if text:
     h=hashlib.sha256(text.encode()).hexdigest(); tf=outdir/(h[:20]+'.txt'); tf.write_text(text[:100000]); rec.update({'text_sha256':h,'text_length':len(text),'text_excerpt':text[:800],'text_file':str(tf)})
    rec['result']='retrieved'; break
   except HTTPError as e:
    rec.update({'http_status':e.code,'result':f'http_{e.code}','error':str(e)})
    if attempt==0 and (e.code==429 or e.code>=500): rec['retry_count']=1; time.sleep(min(int(e.headers.get('Retry-After','1') or 1),5)); continue
    break
   except Exception as e:
    rec.update({'result':'transport_error','error':type(e).__name__+': '+str(e)})
    if attempt==0: rec['retry_count']=1; continue
    break
 rec['completed_at']=now(); h=hashlib.sha256(n.encode()).hexdigest()[:20]; jf=outdir/(h+'.json'); jf.write_text(json.dumps(rec,indent=2,ensure_ascii=False)); rec['evidence_file']=str(jf); return rec
results=[]
with ThreadPoolExecutor(max_workers=6) as ex:
 futs=[ex.submit(fetch,it) for it in unique.items()]
 for f in as_completed(futs): results.append(f.result())
by={x['normalized_url']:x for x in results}
rows=[]
for i in issues:
 r=by.get(norm(i['primary_url'])) if i.get('primary_url') else None
 rows.append({'issue_id':i['issue_id'],'trial_id':i.get('trial_id'),'kind':i.get('kind'),'primary_url':i.get('primary_url'),'question':i.get('question'),'prior_state':i.get('state'),'route_result':r})
(root/'issue-checks.json').write_text(json.dumps({'run_id':RUN,'checked_at':now(),'unique_urls':len(unique),'rows':rows},indent=2,ensure_ascii=False))
from collections import Counter
print('issues',len(rows),'unique',len(unique)); print(Counter((x.get('result'),x.get('http_status')) for x in results))
for x in results:
 if x.get('result') not in ('retrieved','reused_current_run_route','reused_current_run_evidence','not_requested_exact_restriction'): print(x['url'],x.get('result'),x.get('http_status'))
