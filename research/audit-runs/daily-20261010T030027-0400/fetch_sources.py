import json, subprocess, hashlib, re, sys, time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
def fetch(item):
    sid,url,n=item
    ts=datetime.now(ZoneInfo('America/New_York')).isoformat()
    out=ROOT/'http';out.mkdir(exist_ok=True)
    stem=f'{n:03d}'
    raw=out/(stem+'.html');headers=out/(stem+'.headers')
    cmd=['curl','--connect-timeout','5','--max-time','20','--location','--silent','--show-error','-D',str(headers),'-o',str(raw),'-w','%{http_code}\n%{url_effective}',url]
    r=subprocess.run(cmd,capture_output=True,text=True)
    result={'source_id':sid,'url':url,'attempted_at':ts,'method':'shell_curl','exit_code':r.returncode,'transport_result':r.stdout,'error':r.stderr,'raw_file':str(raw.relative_to(ROOT)),'headers_file':str(headers.relative_to(ROOT))}
    html=raw.read_bytes() if raw.exists() else b''
    pdf_text=None
    if raw.exists() and raw.read_bytes().startswith(b'%PDF'):
        converted=out/(stem+'.txt')
        subprocess.run(['pdftotext','-layout',str(raw),str(converted)],capture_output=True)
        pdf_text=converted.read_text(errors='replace') if converted.exists() else ''
        html=''
    soup=BeautifulSoup(html,'html.parser')
    result['links']=[{'text':a.get_text(' ',strip=True),'url':urljoin(url,a['href'])}for a in soup.select('a[href]')]
    result['data_islands']=[{'id':s.get('id'),'type':s.get('type'),'text':s.get_text()} for s in soup.select('script') if s.get('type')=='application/json' or (s.get('id') and not s.get('src'))]
    for s in soup(['script','style','nav','footer']):s.decompose()
    result['text']=pdf_text if pdf_text is not None else soup.get_text('\n',strip=True)
    result['raw_sha256']=hashlib.sha256(html).hexdigest() if html else None
    result['text_sha256']=hashlib.sha256(result['text'].encode()).hexdigest() if html else None
    (out/(stem+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(n,sid,r.returncode,r.stdout.splitlines()[0] if r.stdout else '',len(result['text']),flush=True)
    return result
if __name__=='__main__':
    inv=json.loads((ROOT/'inventory-before.json').read_text())['sources']
    mode=sys.argv[1] if len(sys.argv)>1 else 'master'
    queue=[(s['id'],s['master_url'],i) for i,s in enumerate(inv)] if mode=='master' else json.loads((ROOT/(mode if mode.endswith('.json') else 'http-extra-queue.json')).read_text())
    # Form batches with no more than two requests per domain.
    while queue:
        batch=[];domains={}
        for item in queue[:]:
            domain=urlparse(item[1]).netloc
            if domains.get(domain,0)>=2:continue
            batch.append(item);domains[domain]=domains.get(domain,0)+1;queue.remove(item)
            if len(batch)==6:break
        with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(fetch,batch))
        (ROOT/'http-fetch-checkpoint.json').write_text(json.dumps({'recorded_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'remaining_queue':queue},indent=2))
