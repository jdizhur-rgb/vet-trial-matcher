import json, pathlib, subprocess, hashlib, time, threading, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode, urljoin, quote
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103')
R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
sys.path.insert(0,str(ROOT))
from scripts.check_evidence_keys import redact_text
def now(): return datetime.now(ZoneInfo('America/New_York')).isoformat()
def norm(u):
 p=urlsplit(u);return (p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),tuple(sorted(parse_qsl(p.query))))
inv=json.loads((R/'baseline-source_inventory.json').read_text())['sources']
restrictions=json.loads((R/'baseline-source_access_restrictions.json').read_text())['routes']
for s in inv: restrictions.extend(s.get('access_restrictions',[]))
blocked={norm(x['url']):x for x in restrictions if x.get('do_not_retry') and x.get('url')}
locks={}; guard=threading.Lock();outlock=threading.Lock()
E=R/'evidence';E.mkdir(exist_ok=True)
def read(job):
 url=job['url'];key=hashlib.sha256(url.encode()).hexdigest()[:20];file=E/(key+'.json')
 if file.exists():return json.loads(file.read_text())
 a=dict(job,method='shell_curl',attempted_at=now(),new_source_visit=True)
 if norm(url) in blocked:
  a.update(method='restriction_review_no_request',result='saved_exact_access_restriction',new_source_visit=False,restriction=blocked[norm(url)],completed_at=now())
 else:
  with guard: lock=locks.setdefault(urlsplit(url).netloc.lower().removeprefix('www.'),threading.Semaphore(2))
  with lock:
   raw=E/(key+'.raw'); headers=E/(key+'.headers');tries=[]
   for retry in range(2):
    p=subprocess.run(['curl','-sS','-L','--connect-timeout','5','--max-time','20','--max-redirs','5','-D',str(headers),'-o',str(raw),'-w','%{http_code}\n%{url_effective}\n%{content_type}',quote(url,safe=':/?&=%#~+,;@!$()*[]')],capture_output=True,text=True)
    meta=p.stdout.splitlines(); status=int(meta[0]) if meta and meta[0].isdigit() else 0
    tries.append(dict(at=now(),http_status=status,exit_code=p.returncode,stderr=p.stderr[:500],retry=retry))
    if retry or not(p.returncode in (28,) or status==429 or 500<=status<600):break
    h=headers.read_text(errors='replace') if headers.exists() else '';m=re.search(r'(?im)^retry-after:\s*(\d+)',h);delay=int(m.group(1)) if m else 1
    if delay>60:break
    time.sleep(delay)
   b=raw.read_bytes() if raw.exists() else b'';ct=meta[2] if len(meta)>2 else '';effective=meta[1] if len(meta)>1 else url
   text=''; links=[]
   if 'wordprocessingml' in ct or url.endswith('.docx'):
    import zipfile,io,xml.etree.ElementTree as ET
    try:text='\n'.join(ET.fromstring(zipfile.ZipFile(io.BytesIO(b)).read('word/document.xml')).itertext())
    except Exception as e:text='DOCX extraction failed: '+str(e)
   elif 'pdf' in ct or b[:4]==b'%PDF':
    v=subprocess.run(['pdftotext',str(raw),'-'],capture_output=True,text=True);text=v.stdout
   elif 'json' in ct:
    text=b.decode('utf-8',errors='replace')
   else:
    class Parser(HTMLParser):
     def __init__(self):super().__init__();self.parts=[];self.hidden=0;self.link=None;self.lparts=[]
     def handle_starttag(self,tag,attrs):
      at=dict(attrs)
      if tag in ('script','style','noscript','svg'):self.hidden+=1
      if tag=='a' and at.get('href'):self.link=urljoin(effective,at['href']);self.lparts=[]
     def handle_endtag(self,tag):
      if tag in ('script','style','noscript','svg'):self.hidden=max(0,self.hidden-1)
      if tag=='a' and self.link:links.append({'text':' '.join(self.lparts),'url':self.link});self.link=None
     def handle_data(self,data):
      if not self.hidden and data.strip():self.parts.append(data.strip())
      if self.link:self.lparts.append(data.strip())
    parser=Parser();parser.feed(b.decode('utf-8',errors='replace'));text='\n'.join(parser.parts)
    islands=re.findall(r'<script[^>]*type=[\"\']application/(?:ld\+)?json[\"\'][^>]*>(.*?)</script>',b.decode('utf-8',errors='replace'),re.S|re.I)
    if islands:
     from vet_nov3_inline import clinical_islands
     from html import unescape
     pc=clinical_islands(islands)
     if pc:
      a['public_content']=pc
      a['clinical_text']=unescape(re.sub('<[^>]+>',' ',json.dumps(pc,ensure_ascii=False)))
   a.update(completed_at=now(),http_status=status,effective_url=effective,content_type=ct,attempts=tries,result='retrieved_page' if status==200 and not p.returncode else 'request_failed',text=text,links=links,text_length=len(text),text_sha256=hashlib.sha256(text.encode()).hexdigest())
   if status==403 or re.search(r'ATTACK ATTEMPT DETECTED|verify you are human|captcha|access denied',text[:7000],re.I):a['access_gate_observed']=True
   raw.unlink(missing_ok=True);headers.unlink(missing_ok=True)
 a['evidence_file']=str(file.relative_to(ROOT));file.write_text(redact_text(json.dumps(a,ensure_ascii=False,indent=2)))
 with outlock:
  with (R/'attempts.jsonl').open('a') as f:f.write(json.dumps({k:v for k,v in a.items() if k not in ('text','links','public_data_islands')},ensure_ascii=False)+'\n')
 return a
if __name__=='__main__':
 jobs=json.loads(pathlib.Path(sys.argv[1]).read_text())
 with ThreadPoolExecutor(max_workers=4) as ex:
  for i,a in enumerate(ex.map(read,jobs)):
   print(i,a['url'],a['result'],a.get('http_status'),a.get('text_length'),flush=True)
