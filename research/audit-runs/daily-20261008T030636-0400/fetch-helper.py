import json,sys,hashlib,re,urllib.request,urllib.error,concurrent.futures,threading
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from lxml import html

ROOT=Path('/workspace/scratch/0856bb16a45a/daily-audit-20261008')
RUN=Path('/workspace/scratch/0856bb16a45a/audit-20261008/run-path.txt').read_text();RUN=Path(RUN)
CACHE=Path('/workspace/scratch/0856bb16a45a/audit-pages-20261008');CACHE.mkdir(exist_ok=True)
TZ=ZoneInfo('America/New_York')
LOCK=threading.Lock()
KEY=re.compile(r'trial|stud(?:y|ies)|oncolog|cancer|lymphoma|sarcoma|tumou?r|glioma|carcinoma|vaccine|melanoma|vinorelbine|clinical|臨床|治験|腫瘍|研究|がん|tumor|ensaio|estud',re.I)

def fetch(url):
    attempt={'url':url,'attempted_at':datetime.now(TZ).isoformat(),'method':'urllib_current_run'}
    key=hashlib.sha256(url.encode()).hexdigest()[:20]
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; public-source-review)','Accept-Language':'en-US,en;q=0.8'})
        with urllib.request.urlopen(req,timeout=18) as response:
            raw=response.read(4*1024*1024);attempt.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''))
        (CACHE/(key+'.raw')).write_bytes(raw)
        if 'pdf' in attempt['content_type']:
            attempt.update(result='pdf_requires_review',raw_path=str(CACHE/(key+'.raw')),normalized_chars=0);return attempt
        doc=html.fromstring(raw)
        links=[]
        for node in doc.xpath('//a[@href]'):
            label=' '.join(node.text_content().split());href=urllib.parse.urljoin(attempt['final_url'],node.get('href'))
            if KEY.search(label+' '+href) and href.startswith('https://'): links.append({'title':label,'url':href})
        for n in doc.xpath('//script|//style|//noscript'):
            parent=n.getparent()
            if parent is not None: parent.remove(n)
        mains=doc.xpath('//main|//*[@role="main"]'); body=[max(mains,key=lambda n:len(n.text_content()))] if mains and max(len(n.text_content()) for n in mains)>500 else [doc]
        text='\n'.join(' '.join(x.split()) for x in body[0].text_content().splitlines() if x.strip())
        heads=[' '.join(n.text_content().split()) for n in body[0].xpath('.//h1|.//h2|.//h3|.//h4')]
        normalized=' '.join(text.split());fp='sha256:'+hashlib.sha256(normalized.encode()).hexdigest()
        attempt.update(result='fetched_requires_roster_review',fingerprint=fp,normalized_chars=len(normalized),text_path=str(CACHE/(key+'.txt')),links_path=str(CACHE/(key+'.links.json')),headings=heads,links=links)
        (CACHE/(key+'.txt')).write_text(text);(CACHE/(key+'.links.json')).write_text(json.dumps(links,ensure_ascii=False,indent=2))
    except urllib.error.HTTPError as e: attempt.update(http_status=e.code,result='unreachable',error=str(e))
    except Exception as e: attempt.update(result='unreachable',error=type(e).__name__+': '+str(e))
    return attempt

def source(s):
    routes=[s['master_url']]+s.get('fallback_urls',[])
    return {'source_id':s['id'],'source_name':s['name'],'attempts':[fetch(url) for url in routes]}

if __name__=='__main__':
    inventory=json.loads((RUN/'inventory-before.json').read_text())
    out=json.loads((RUN/'source-fetch-evidence.json').read_text()) if (RUN/'source-fetch-evidence.json').exists() else []
    completed={r['source_id'] for r in out}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        prior=json.loads((RUN/'previous-receipt.json').read_text()); backlog={r['source_id'] for r in prior['sources'] if not r.get('content_sufficient')}; ordered=sorted(inventory['sources'],key=lambda s:s['id'] not in backlog); pending={ex.submit(source,s):s for s in ordered if s['id'] not in completed}
        for f in concurrent.futures.as_completed(pending):
            row=f.result();out.append(row)
            (RUN/'source-fetch-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
            print(row['source_id'],[(a.get('http_status'),a.get('normalized_chars',0),len(a.get('links',[]))) for a in row['attempts']],flush=True)
    print('TOTAL',len(out))
