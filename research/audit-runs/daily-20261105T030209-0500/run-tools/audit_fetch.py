#!/usr/bin/env python3
from __future__ import annotations
import hashlib,html,json,re,subprocess,sys,threading,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl,urljoin,urlsplit
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[4]
RUN=Path(sys.argv[1]).resolve(); PLAN=Path(sys.argv[2]); OUT=Path(sys.argv[3])
EVIDENCE=RUN/'evidence';EVIDENCE.mkdir(parents=True,exist_ok=True);NY=ZoneInfo('America/New_York')
def now():return datetime.now(NY).isoformat()
def norm(u):
 p=urlsplit(u);return(p.scheme.lower(),p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),tuple(sorted(parse_qsl(p.query))))
inv=json.loads((RUN/'baseline-source_inventory.json').read_text())['sources']
restr=json.loads((RUN/'baseline-source_access_restrictions.json').read_text()).get('routes',[])
for s in inv:restr+=s.get('access_restrictions',[])
blocked={norm(x['url']):x for x in restr if x.get('do_not_retry') and x.get('url')}
locks={};guard=threading.Lock();write=threading.Lock()
class V(HTMLParser):
 def __init__(self,b):super().__init__();self.b=b;self.skip=0;self.parts=[];self.links=[];self.cur=None;self.lab=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t in {'script','style','noscript','svg'}:self.skip+=1
  if t=='a' and d.get('href'):self.cur=urljoin(self.b,d['href']);self.lab=[]
 def handle_endtag(self,t):
  if t in {'script','style','noscript','svg'}:self.skip=max(0,self.skip-1)
  if t=='a' and self.cur:self.links.append({'text':' '.join(self.lab),'url':self.cur});self.cur=None;self.lab=[]
 def handle_data(self,d):
  x=' '.join(d.split())
  if x and not self.skip:self.parts.append(x)
  if x and self.cur:self.lab.append(x)
def extract(body,ctype,url,key):
 if body.startswith(b'%PDF') or 'pdf' in ctype.lower():
  p=EVIDENCE/(key+'.pdf');p.write_bytes(body);q=subprocess.run(['pdftotext',str(p),'-'],capture_output=True,text=True);return q.stdout,[],{'format':'pdf','pdf_file':str(p.relative_to(ROOT))}
 raw=body.decode('utf-8',errors='replace')
 if 'json' in ctype.lower() or raw.lstrip().startswith(('{','[')):return raw,[],{'format':'json'}
 v=V(url)
 try:v.feed(raw)
 except:pass
 return '\n'.join(v.parts),v.links,{'format':'html'}
def one(j):
 url=j['url'];key=hashlib.sha256((j.get('source_id','')+'\0'+j.get('trial_id','')+'\0'+j['route']+'\0'+url).encode()).hexdigest()[:24];out=EVIDENCE/(key+'.json')
 row={**j,'method':'shell_curl','attempted_at':now(),'new_source_visit':True}
 held=blocked.get(norm(url))
 if held:
  row.update(method='restriction_review_no_request',new_source_visit=False,result='saved_exact_access_restriction',restriction=held,completed_at=now(),evidence_file=str(out.relative_to(ROOT)));out.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n');return row
 host=urlsplit(url).netloc.lower().removeprefix('www.')
 with guard:lock=locks.setdefault(host,threading.Semaphore(2))
 ats=[];body=b'';heads=b'';status=0;eff=url;ctype=''
 with lock:
  for retry in range(2):
   raw=EVIDENCE/(key+'.raw');hdr=EVIDENCE/(key+'.headers')
   p=subprocess.run(['curl','-sS','-L','--connect-timeout','5','--max-time','20','--max-redirs','5','-D',str(hdr),'-o',str(raw),'-w','%{http_code}\n%{url_effective}\n%{content_type}',url],capture_output=True,text=True)
   meta=p.stdout.splitlines();status=int(meta[0]) if meta and meta[0].isdigit() else 0;eff=meta[1] if len(meta)>1 else url;ctype=meta[2] if len(meta)>2 else '';body=raw.read_bytes() if raw.exists() else b'';heads=hdr.read_bytes() if hdr.exists() else b''
   ats.append({'at':now(),'retry':retry,'exit_code':p.returncode,'http_status':status,'stderr':p.stderr[:1000]});raw.unlink(missing_ok=True);hdr.unlink(missing_ok=True)
   trans=p.returncode==28 or status==429 or 500<=status<600
   if retry or not trans:break
   m=re.search(br'(?im)^retry-after:\s*(\d+)',heads);time.sleep(min(int(m.group(1)),60) if m else 1)
 text,links,meta=extract(body,ctype,eff,key);gate=bool(status==403 or re.search(r'verify you are human|captcha|access denied|cloudflare',text[:12000],re.I))
 row.update(completed_at=now(),http_status=status,effective_url=eff,content_type=ctype,attempts=ats,result='retrieved_page' if status==200 and ats[-1]['exit_code']==0 else 'request_failed',access_gate_observed=gate,body_bytes=len(body),body_sha256=hashlib.sha256(body).hexdigest(),text=text,text_length=len(text),text_sha256=hashlib.sha256(text.encode()).hexdigest(),links=links,extraction=meta,evidence_file=str(out.relative_to(ROOT)));out.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
 with write:
  with (RUN/'attempts.jsonl').open('a') as f:f.write(json.dumps({k:v for k,v in row.items() if k not in {'text','links','extraction'}},ensure_ascii=False)+'\n')
 return row
jobs=json.loads(PLAN.read_text());res=[];last=time.monotonic()
with ThreadPoolExecutor(max_workers=6) as ex:
 fut={ex.submit(one,j):j for j in jobs}
 for i,f in enumerate(as_completed(fut),1):
  x=f.result();res.append(x);print(i,len(jobs),x.get('source_id'),x['route'],x['result'],x.get('http_status'),x.get('text_length'),flush=True)
  if time.monotonic()-last>=900:
   (RUN/f"segment-auto-{datetime.now(NY).strftime('%H%M%S')}.json").write_text(json.dumps({'at':now(),'completed':i,'total':len(jobs)},indent=2)+'\n');last=time.monotonic()
OUT.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
