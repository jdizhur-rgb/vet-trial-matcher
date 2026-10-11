"""Run-local public evidence retrieval. HTTP success never implies reconciliation."""
import concurrent.futures, gzip, hashlib, json, sys, threading, urllib.parse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import urllib.request, urllib.error
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.check_evidence_keys import redact_text

BASE=Path(__file__).resolve().parent
locks={}
lock=threading.Lock()
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def fetch(url):
    domain=urllib.parse.urlparse(url).netloc.lower().removeprefix('www.')
    with lock: semaphore=locks.setdefault(domain,threading.Semaphore(2))
    with semaphore:
        at=now(); out={'url':url,'attempted_at':at,'method':'shell.urllib','http_status':None,'text':'','links':[],'structured_data':[],'error':None,'review_status':'pending'}
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; VetTrialFinder research audit)'}),timeout=20) as r:
                body=r.read();out.update(http_status=r.status,final_url=r.url)
                if body[:2]==b'\x1f\x8b':body=gzip.decompress(body)
            if out['http_status']==200:
                soup=BeautifulSoup(body,'html.parser')
                for script in soup.find_all('script',type='application/ld+json'):
                    try:out['structured_data'].append(json.loads(script.string or script.get_text()))
                    except Exception:pass
                out['links']=[{'text':a.get_text(' ',strip=True),'url':urllib.parse.urljoin(out['final_url'],a['href'])} for a in soup.find_all('a',href=True) if not a['href'].startswith(('mailto:','tel:','javascript:','#')) and urllib.parse.urlsplit(urllib.parse.urljoin(out['final_url'],a['href'])).scheme in ('http','https')]
                out['map_embeds']=[a.get('src') or a.get('data-src') for a in soup.find_all('iframe') if any(s in str(a) for s in ('maps','google'))]
                for elem in soup(['script','style','noscript','svg']):elem.decompose()
                out['text']='\n'.join(line.strip() for line in soup.get_text('\n',strip=True).splitlines() if line.strip())
                out['fingerprint_sha256']=hashlib.sha256(out['text'].encode()).hexdigest()
            else:out['error']='HTTP '+str(out['http_status'])
        except urllib.error.HTTPError as e:out.update(http_status=e.code,error=repr(e))
        except Exception as e:out['error']=repr(e)
        out['ended_at']=now()
        key=hashlib.sha256(url.encode()).hexdigest()[:18]
        target=BASE/'pages'/f'{key}.json';target.parent.mkdir(exist_ok=True)
        if target.exists():
            key+='-'+datetime.now().strftime('%H%M%S%f');target=BASE/'pages'/f'{key}.json'
        target.write_text(redact_text(json.dumps(out,ensure_ascii=False,indent=2))+'\n')
        return {'url':url,'evidence_file':str(target.relative_to(BASE)),'attempted_at':at,'http_status':out['http_status'],'error':out['error'],'characters':len(out['text'])}

if __name__=='__main__':
    urls=json.loads(Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=[]
        for result in pool.map(fetch,urls):results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
    Path(sys.argv[2]).write_text(redact_text(json.dumps(results,indent=2))+'\n')
