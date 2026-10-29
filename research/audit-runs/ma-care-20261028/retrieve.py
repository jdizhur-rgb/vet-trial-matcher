"""Bounded public-page reader. Payload cache is outside the repository."""
import concurrent.futures as cf
import datetime as dt
import hashlib,json,pathlib,re,sys,urllib.parse
import requests
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from scripts.check_evidence_keys import redact_text
OUT=pathlib.Path(__file__).parent
CACHE=ROOT.parent/'ma-source-cache'
CACHE.mkdir(exist_ok=True)
def norm(u):
 p=urllib.parse.urlsplit(u);return p.netloc.lower().removeprefix('www.')+p.path.rstrip('/')+('?' + p.query if p.query else '')
denied=set()
for file in ['data/source_access_restrictions.json','research/oncology-care-queue/access-restriction-index.json']:
 for u in re.findall(r'https?://[^\s"<>]+',(ROOT/file).read_text()):denied.add(norm(u))
# Earlier ACCS live 403 is retained in narrative rather than serialized restrictions.
denied.update(norm('https://accsvets.com'+p) for p in ['/services/','/about-us/team/','/about-us/location-hours/'])
def get(u):
 key=hashlib.sha256(u.encode()).hexdigest()[:16];dest=CACHE/f'{key}.json'
 if dest.exists():return json.loads(dest.read_text())
 row={'url':u,'attempted_at':dt.datetime.now(dt.timezone.utc).isoformat(),'method':'requests GET','key':key}
 if norm(u) in denied:row['result']='skipped_prior_restriction';return row
 try:
  current=u
  for hop in range(6):
   if norm(current) in denied:row.update(result='skipped_restricted_redirect',final_url=current);break
   r=requests.get(current,timeout=(7,18),allow_redirects=False)
   if r.is_redirect:
    current=urllib.parse.urljoin(current,r.headers['Location']);continue
   row.update(status=r.status_code,final_url=current)
   if r.status_code!=200:row['result']='http_error';break
   s=BeautifulSoup(r.text,'html.parser');links=[]
   for a in s.select('a[href]'):
    href=urllib.parse.urljoin(current,a['href'])
    if href.startswith(('http','tel:','mailto:')):links.append({'text':a.get_text(' ',strip=True),'url':href})
   if 'xml' in r.headers.get('content-type','') or current.endswith('.xml'):
    links += [{'text':'sitemap loc','url':v} for v in re.findall(r'<loc>\s*(.*?)\s*</loc>',r.text)]
   row['scripts']=[urllib.parse.urljoin(current,x['src']) for x in s.select('script[src]')]
   for x in s(['script','style','noscript','svg']):x.decompose()
   txt='\n'.join(z.strip() for z in s.get_text('\n').splitlines() if z.strip())
   row.update(result='readable' if len(txt)>200 else 'thin',text=redact_text(txt),links=json.loads(redact_text(json.dumps(links))))
   break
 except Exception as e:row.update(result='transport_error',error=str(e)[:250])
 dest.write_text(json.dumps(row,ensure_ascii=False,indent=2));return row
def batch(urls):
 with cf.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(get,sorted(set(urls))))
 payloads=[json.loads(f.read_text()) for f in CACHE.glob('*.json') if f.name!='integration-baseline.json']
 receipts=[{k:v for k,v in r.items() if k not in ['text','links','scripts']} for r in payloads if 'url' in r]
 (OUT/'request-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
 return rows
if __name__=='__main__':
 rows=batch(json.loads(pathlib.Path(sys.argv[1]).read_text()))
 for r in rows:print(r['key'],r['result'],r['url'],len(r.get('text','')))
