import json,pathlib,datetime,concurrent.futures,urllib.request,urllib.error,hashlib
from urllib.parse import urlsplit,urljoin
from lxml import html
HERE=pathlib.Path(__file__).parent
RAW=pathlib.Path('/workspace/scratch/c43bd3696660/germany-source-raw');RAW.mkdir(exist_ok=True)
DENIED={'schlager.vet','tierarzt-konstanz.de','tierarzt-weinstadt.de','tierarzt.top','tierklinik-ismaning.de','tierklinik-reif.de','tknds.de','anicura.de'}
RESTRICTIONS=json.loads(pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-20261016T142911-0400/research/audit-runs/eu6-20261016T142911-0400/worker-4/input/shared-restrictions/slot-4.json').read_text())
def norm(u):
 from urllib.parse import unquote
 p=urlsplit(u);return((p.hostname or '').removeprefix('www.'),unquote(p.path).casefold().rstrip('/') or '/')
EXACT={norm(x['url']) for x in RESTRICTIONS['restrictions']}|{norm(u) for u in RESTRICTIONS['equivalent_national_roster_aliases']}
class NoAutoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl): return None
def fetch(url):
 timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(); key=hashlib.sha256(url.encode()).hexdigest()[:16]
 r=dict(url=url,attempted_at=timestamp,authorization='Owner explicit scoped reauthorization after review of87candidates/18routes: Разрешаю.',method='ordinary public GET',redirects=[])
 current=url
 for n in range(4):
  if (urlsplit(current).hostname or '').removeprefix('www.') in DENIED or norm(current) in EXACT:
   r.update(result='SKIPPED_REAL_SITE_DENIAL',blocked_url=current);return r
  try:
   if n==0 and (RAW/(key+'.html')).exists():
    data=(RAW/(key+'.html')).read_bytes();status=200;r['attempted_at']=None;r['recovered_from_successful_raw']=True;r['raw_file_completed_at']=datetime.datetime.fromtimestamp((RAW/(key+'.html')).stat().st_mtime,datetime.timezone.utc).isoformat()
   else:
    req=urllib.request.Request(current,headers={'User-Agent':'Mozilla/5.0 (compatible; public veterinary source review)'})
    response=urllib.request.build_opener(NoAutoRedirect).open(req,timeout=22);data=response.read(3000000);status=response.status
   (RAW/(key+'.request.json')).write_text(json.dumps(dict(r,status=status,final_url=current,bytes=len(data)),ensure_ascii=False))
  except urllib.error.HTTPError as e:
   status=e.code
   if status in (301,302,303,307,308):
    target=urljoin(current,e.headers['Location']);r['redirects'].append(dict(from_url=current,to_url=target,status=status));current=target;continue
   r.update(status=status,result='SITE_ACCESS_DENIAL' if status in (401,403,429) else 'HTTP_ERROR',final_url=current);(RAW/(key+'.request.json')).write_text(json.dumps(r));return r
  except Exception as e:r.update(result='TRANSPORT_FAILURE',error=str(e),final_url=current);return r
  
  if not data.strip():r.update(status=status,result='EMPTY_BODY',final_url=current);return r
  soup=html.fromstring(data);title=' '.join(soup.xpath('//title/text()'))
  links=[dict(text=' '.join(a.itertext()).strip(),url=urljoin(current,a.get('href',''))) for a in soup.xpath('//a[@href]')]
  for e in soup.xpath('//script|//style|//noscript'):e.drop_tree()
  text=' '.join(' '.join(soup.itertext()).split())
  (RAW/(key+'.txt')).write_text(text);(RAW/(key+'.html')).write_bytes(data)
  relevant=[]
  import re
  for m in re.finditer(r'(?i)tumor|onkol|chemo|telefon|kontakt|impressum|tierärzt|tierarzt|öffnungs|termin|strahlen|elektro',text):
   a=max(0,m.start()-80);b=min(len(text),m.end()+180)
   if not relevant or a>relevant[-1][1]:relevant.append((a,b))
  r.update(status=status,result='READABLE_PRIMARY',final_url=current,title=title,text_chars=len(text),raw_key=key,review_passages=[text[a:b] for a,b in relevant][:45],links=[x for x in links if any(t in x['url'].lower() for t in ['kontakt','team','impressum','onkolog','chemo','chirurg','strahl','leistung','standort'])][:60]);return r
 r.update(result='REDIRECT_LIMIT',final_url=current);return r
if __name__=='__main__':
 import sys
 urls=json.loads((HERE/sys.argv[1]).read_text())['URLs'];results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for r in pool.map(fetch,urls):
   results.append(r);print(r['url'],r['result'],r.get('status'),flush=True);(HERE/sys.argv[2]).write_text(json.dumps(dict(records=results),ensure_ascii=False,indent=2)+'\n')
 (HERE/sys.argv[2]).write_text(json.dumps(dict(authorization='User explicit Разрешаю following concrete scopedreview',source_attempts=len(results),records=results),ensure_ascii=False,indent=2)+'\n')
