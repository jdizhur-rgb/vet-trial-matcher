"""Actual finite reads; retrieval is separate from source reconciliation."""
import concurrent.futures, hashlib, json, os, re, subprocess, sys, threading, time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse, urljoin, quote
from html.parser import HTMLParser
from html import unescape

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from scripts.check_evidence_keys import redact_text
RUN=Path(__file__).resolve().parent
RAW=Path('/workspace/scratch/2226bbb8952f/raw-evidence/finalize-68-20261014T185109-0400')
TZ=ZoneInfo('America/New_York')
LOCK=threading.Lock(); DOMAINS={}
def stamp(): return datetime.now(TZ).isoformat()
def get(item):
    host=urlparse(item['url']).netloc
    with LOCK: sem=DOMAINS.setdefault(host,threading.Semaphore(2))
    with sem:
        attempts=[]
        for retry in range(2):
            at=stamp(); token=hashlib.sha256((item['url']+at).encode()).hexdigest()[:18]
            body=RAW/(token+'.body'); headers=RAW/(token+'.headers')
            p=subprocess.run(['curl','-L','--compressed','--silent','--show-error','--connect-timeout','5','--max-time','20','-D',str(headers),'-o',str(body),'-w','%{http_code}\n%{url_effective}\n%{content_type}',quote(item['url'],safe=':/?&=%#')],capture_output=True)
            meta=p.stdout.decode(errors='replace').splitlines(); status=int(meta[0]) if meta and meta[0].isdigit() and int(meta[0]) else None
            ctype=meta[2] if len(meta)>2 else ''; effective=meta[1] if len(meta)>1 else item['url']
            raw=body.read_bytes() if body.exists() else b''; title=''; links=[]
            if 'pdf' in ctype.lower() or raw.startswith(b'%PDF'):
                pdftext=RAW/(token+'.pdf.txt'); z=subprocess.run(['pdftotext',str(body),str(pdftext)],capture_output=True); text=pdftext.read_text(errors='replace') if pdftext.exists() else ''
            else:
                decoded=redact_text(raw.decode(errors='replace'))
                if '<html' in decoded[:5000].lower() or 'html' in ctype:
                    class PublicHTML(HTMLParser):
                        def __init__(self): super().__init__(); self.parts=[];self.links=[];self.skip=0;self.anchor=None
                        def handle_starttag(self,tag,attrs):
                            if tag in ('script','style','noscript','svg'): self.skip+=1
                            if tag=='a' and not self.skip:
                                self.anchor=[dict(attrs).get('href',''),'']
                        def handle_endtag(self,tag):
                            if tag in ('script','style','noscript','svg'): self.skip=max(0,self.skip-1)
                            if tag=='a' and self.anchor:
                                self.links.append(self.anchor);self.anchor=None
                        def handle_data(self,data):
                            if not self.skip:
                                self.parts.append(data)
                                if self.anchor: self.anchor[1]+=data
                    h=PublicHTML();h.feed(decoded);text='\n'.join(z.strip() for z in h.parts if z.strip())
                    title_match=re.search(r'<title[^>]*>(.*?)</title>',decoded,re.I|re.S);title=unescape(title_match.group(1)) if title_match else ''
                    links=[{'url':redact_text(urljoin(effective,u)),'label':label.strip()[:300]} for u,label in h.links if urljoin(effective,u).startswith(('http://','https://'))]
                else: text=decoded
            text=redact_text(text); (RAW/(token+'.txt')).write_text(text)
            # Raw bytes stay transient and are never staged for public publication.
            row={**item,'attempted_at':at,'completed_at':stamp(),'method':'shell_curl','retry':retry,'http_status':status,'effective_url':effective,'content_type':ctype,'exit_code':p.returncode,'stderr':redact_text(p.stderr.decode(errors='replace'))[-500:],'title':title,'text_length':len(text),'text_sha256':hashlib.sha256(text.encode()).hexdigest() if text else None,'text_path':str(RAW/(token+'.txt')),'relevant_links':[x for x in links if re.search(r'trial|stud|recruit|enrol|oncolog|cancer|tumou?r|lymph|sarcoma|melanoma|carcinoma|glioma',x['label']+' '+x['url'],re.I)][:200],'result':'retrieved_page' if p.returncode==0 else 'transport_error'}
            attempts.append(row)
            with LOCK:
                with (RUN/'shell-attempts.jsonl').open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
            transient=p.returncode in (6,28,52,56) or status==429 or (status is not None and status>=500)
            if retry or not transient: break
            h=headers.read_text(errors='replace') if headers.exists() else ''; r=re.findall(r'(?im)^retry-after:\s*(\d+)',h); delay=int(r[-1]) if r else 1
            if delay>60: break
            time.sleep(delay)
        print(json.dumps({'source_id':item['source_id'],'route':item['route'],'status':status,'exit':p.returncode,'text_length':len(text),'attempts':len(attempts)}),flush=True)
        return attempts
if __name__=='__main__':
    queue=json.loads(Path(sys.argv[1]).read_text()); assert queue
    queue=list({(x['source_id'],x['url']):x for x in queue}.values())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: list(pool.map(get,queue))
