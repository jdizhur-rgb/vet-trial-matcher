"""Finite daily retrieval and honest checkpoints; reconciliation is manual."""
import concurrent.futures, hashlib, json, subprocess, sys, threading, time, re, fcntl
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urlparse, urljoin, quote
from html.parser import HTMLParser
from html import unescape
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.check_evidence_keys import redact_text
from seo.catalog_selection import current_public
TZ=ZoneInfo('America/New_York')
RAW=ROOT.parent/'raw-evidence'/RUN.name
LOCK=threading.Lock(); DOMAINS={}
def now(): return datetime.now(TZ).isoformat()
def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def read(path): return json.loads(path.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def checkpoint():
    rows=read(RUN/'reviews.json') if (RUN/'reviews.json').exists() else []
    inv=read(RUN/'before-source_inventory.json')['sources']
    done={r['source_id'] for r in rows}
    write(RUN/('checkpoint-'+datetime.now(TZ).strftime('%H%M%S')+'.json'),{'at':now(),'run_id':RUN.name,'reviewed':len(rows),'processing_complete':sum(r.get('processing_complete') is True for r in rows),'remaining_source_ids':[s['id'] for s in inv if s['id'] not in done],'discovery_regions_completed':[],'deadline':'2026-10-31T06:00:00-04:00','note':'Fetched pages are not completed source reconciliations.'})
class H(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[];self.links=[];self.skip=0;self.a=None
    def handle_starttag(self,t,a):
        if t in ('script','style','noscript','svg'): self.skip+=1
        if t=='a' and not self.skip: self.a=[dict(a).get('href',''),'']
    def handle_endtag(self,t):
        if t in ('script','style','noscript','svg'): self.skip=max(0,self.skip-1)
        if t=='a' and self.a: self.links.append(self.a);self.a=None
    def handle_data(self,d):
        if not self.skip:
            self.parts.append(d)
            if self.a: self.a[1]+=d
def get(item):
    with LOCK: sem=DOMAINS.setdefault(urlparse(item['url']).netloc,threading.Semaphore(2))
    with sem:
        for retry in range(2):
            at=now(); token=hashlib.sha256((item['url']+at).encode()).hexdigest()[:18]
            body=RAW/(token+'.body');header=RAW/(token+'.headers')
            p=subprocess.run(['curl','-L','--compressed','-sS','--connect-timeout','5','--max-time','20','-D',str(header),'-o',str(body),'-w','%{http_code}\n%{url_effective}\n%{content_type}',quote(item['url'],safe=':/?&=%#')],capture_output=True)
            meta=p.stdout.decode(errors='replace').splitlines(); status=int(meta[0]) if meta and meta[0].isdigit() and int(meta[0]) else None
            effective=meta[1] if len(meta)>1 else item['url'];ctype=meta[2] if len(meta)>2 else '';raw=body.read_bytes() if body.exists() else b''
            links=[]; title=''
            if raw.startswith(b'%PDF'):
                out=RAW/(token+'.pdf.txt');subprocess.run(['pdftotext',str(body),str(out)],capture_output=True);text=out.read_text(errors='replace') if out.exists() else ''
            else:
                decoded=redact_text(raw.decode(errors='replace'))
                if '<html' in decoded[:5000].lower() or 'html' in ctype:
                    h=H();h.feed(decoded);text='\n'.join(z.strip() for z in h.parts if z.strip());m=re.search(r'<title[^>]*>(.*?)</title>',decoded,re.I|re.S);title=unescape(m.group(1)) if m else ''
                    links=[{'url':redact_text(urljoin(effective,u)),'label':l.strip()} for u,l in h.links if urljoin(effective,u).startswith(('http://','https://'))]
                else: text=decoded
            text=redact_text(text)
            evidence={'title':title,'text':text,'links':links}
            ep=RUN/'evidence'/(token+'.json');write(ep,evidence)
            row={**item,'attempted_at':at,'completed_at':now(),'method':'shell_curl','retry':retry,'http_status':status,'effective_url':effective,'content_type':ctype,'exit_code':p.returncode,'stderr':redact_text(p.stderr.decode(errors='replace'))[-400:],'text_length':len(text),'text_sha256':hashlib.sha256(text.encode()).hexdigest() if text else None,'evidence_file':str(ep.relative_to(ROOT)),'raw_file':str(body),'result':'retrieved_page' if p.returncode==0 else 'transport_error'}
            with LOCK:
                with (RUN/'attempts.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
            print(json.dumps({k:row[k] for k in ('source_id','route','http_status','exit_code','text_length','evidence_file')}),flush=True)
            if retry or not (p.returncode in (6,28,52,56) or status==429 or status and status>=500):break
            headers=header.read_text(errors='replace') if header.exists() else '';r=re.findall(r'(?im)^retry-after:\s*(\d+)',headers); delay=int(r[-1]) if r else 1
            if delay>60:break
            time.sleep(delay)
def main():
    # Serialize native batches across invocations of this runner, not just threads.
    # Each batch itself retains six global workers and two per domain.
    batch_lock=None
    if sys.argv[1] in ('fetch','master'):
        batch_lock=(RUN/'.native-request-batch.lock').open('w')
        fcntl.flock(batch_lock,fcntl.LOCK_EX)
    RAW.mkdir(parents=True,exist_ok=True);(RUN/'evidence').mkdir(exist_ok=True)
    if sys.argv[1]=='init':
        for name in ('source_inventory.json','trials_base.json','audit_state.json','audit_source_coverage.json'):
            p=ROOT/'data'/name;(RUN/('before-'+name)).write_bytes(p.read_bytes())
        catalog=read(ROOT/'data/trials_base.json');public=current_public(catalog)
        write(RUN/'baseline.json',{'run_id':RUN.name,'started_at':'2026-10-31T02:58:01.171612-04:00','snapshot_at':now(),'base_main_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_ids':[s['id'] for s in read(ROOT/'data/source_inventory.json')['sources']],'counts':{'canonical':len(catalog),'public':len(public),'treatment':sum(r.get('study_type','treatment')=='treatment' for r in public),'other_access':sum(r.get('study_type')=='other_treatment_access' for r in public),'sources':len(read(ROOT/'data/source_inventory.json')['sources'])},'sha256':{n:digest(ROOT/'data'/n) for n in ('trials_base.json','source_inventory.json','audit_state.json','audit_source_coverage.json')}})
        write(RUN/'reviews.json',[]);checkpoint()
    elif sys.argv[1]=='fetch':
        plan=read(Path(sys.argv[2]))
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,plan))
        checkpoint()
    elif sys.argv[1]=='review':
        rows=read(RUN/'reviews.json'); incoming=read(Path(sys.argv[2]));ids={r['source_id'] for r in incoming}
        write(RUN/'reviews.json',[r for r in rows if r['source_id'] not in ids]+incoming);checkpoint()
    elif sys.argv[1]=='master':
        a,b=map(int,sys.argv[2:]);inv=read(RUN/'before-source_inventory.json')['sources']
        attempted=[json.loads(l) for l in (RUN/'attempts.jsonl').read_text().splitlines()] if (RUN/'attempts.jsonl').exists() else []
        attempted+=read(RUN/'web-attempts.json') if (RUN/'web-attempts.json').exists() else []
        visited={x['url'] for x in attempted}
        denials=read(RUN/'restrictions-frozen.json')
        denied={x['url'] for x in denials}
        plan=[{'source_id':s['id'],'url':s['master_url'],'route':'master'} for s in inv[a:b] if s['master_url'] not in visited and s['master_url'] not in denied]
        write(RUN/f'shared-or-denied-{a}-{b}.json',[{'source_id':s['id'],'url':s['master_url'],'reason':'prior_explicit_denial_not_retried' if s['master_url'] in denied else 'actual_current_run_evidence_reused','actual_current_attempts':[x for x in attempted if x['url']==s['master_url']],'prior_denial_evidence':[x for x in denials if x['url']==s['master_url']]} for s in inv[a:b] if s['master_url'] in visited or s['master_url'] in denied])
        write(RUN/f'plan-{a}-{b}.json',plan)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,plan))
        checkpoint()
    elif sys.argv[1]=='show':
        ids=sys.argv[2:];attempts=[json.loads(x) for x in (RUN/'attempts.jsonl').read_text().splitlines()];latest={}
        for a in attempts:
            if a['source_id'] in ids:latest[(a['source_id'],a['url'])]=a
        for a in latest.values():
            ev=read(ROOT/a['evidence_file']);print('\nSOURCE',a['source_id'],a['url'],a['http_status'],'FILE',a['evidence_file']);print(ev['text'][:18000]);print('LINKS',json.dumps([x for x in ev['links'] if re.search('trial|stud|recruit|enrol|oncolog|cancer|tumou?r|lymph|sarcoma|melanoma|carcinoma|glioma',x['label']+' '+x['url'],re.I)],ensure_ascii=False)[:14000])
    elif sys.argv[1]=='body':
        a,b=map(int,sys.argv[2:]);ids={s['id'] for s in read(RUN/'before-source_inventory.json')['sources'][a:b]};latest={}
        for line in (RUN/'attempts.jsonl').read_text().splitlines():
            x=json.loads(line)
            if x['source_id'] in ids:latest[(x['source_id'],x['url'])]=x
        for x in latest.values():
            e=read(ROOT/x['evidence_file']);print('\nSOURCE',x['source_id'],x['route'],x['url'],x['http_status'],x['text_length'],x['evidence_file'])
            raw=Path(x['raw_file']).read_text(errors='replace') if Path(x['raw_file']).exists() else ''
            m=re.search(r'<main\b[^>]*>(.*?)</main>',raw,re.I|re.S)
            if m:
                h=H();h.feed(m.group(1));text='\n'.join(z.strip() for z in h.parts if z.strip())
            else:text=e['text']
            if len(text)>18000:print('LARGE CONTENT; inspect separately')
            else:print(text)
            unique={l['url']:{'url':l['url'],'label':l['label'][:150]} for l in e['links'] if re.search('trial|stud|recruit|enrol|oncolog|cancer|tumou?r|lymph|sarcoma|melanoma|carcinoma|glioma',l['label'],re.I) and '#' not in l['url'] and not re.search('student|recruitment strateg|undergraduate|course',l['label'],re.I)}
            print('CLINICAL_LINKS',json.dumps(list(unique.values()),ensure_ascii=False)[:6500])
# Restriction check is performed again at actual dispatch, before curl.
from urllib.parse import urlsplit,unquote,parse_qsl

def route_key(u):
    v=urlsplit(u)
    return ((v.hostname or '').removeprefix('www.'),unquote(v.path).rstrip('/'),tuple(sorted(parse_qsl(v.query,keep_blank_values=True))))
_original_get=get

def known_denials():
    rows=read(RUN/'restrictions-frozen.json')
    extra=RUN/'new-denials.jsonl'
    if extra.exists():rows += [json.loads(l) for l in extra.read_text().splitlines()]
    return {route_key(r['url']) for r in rows}

def get(item):
    if 'fapesp.br' in urlparse(item['url']).netloc.lower() or item['source_id']=='brazil-usp-onvex-precision-oncology': raise RuntimeError('Excluded restricted source')
    # Reuse actual current-run evidence across source aliases and protocol rows.
    # A local reread is not another network visit and must not renew dates.
    attempts_path=RUN/'attempts.jsonl'
    if attempts_path.exists():
        with LOCK:
            prior=[json.loads(l) for l in attempts_path.read_text().splitlines()]
            shared=next((a for a in reversed(prior) if route_key(a['url'])==route_key(item['url'])),None)
            if shared:
                with (RUN/'evidence-reuse.jsonl').open('a') as f:
                    f.write(json.dumps(dict(request=item,actual_attempt=shared,result='current_run_evidence_reused',at=now()))+'\n')
                return
    if route_key(item['url']) in known_denials():
        with LOCK:
            with (RUN/'skipped-restricted-routes.jsonl').open('a') as f:f.write(json.dumps(dict(item,result='known_denial_not_requested',at=now()))+'\n')
        return
    _original_get(item)
    # Persist first explicit current403; no retry or Web visit to that route.
    with LOCK:
        rows=[json.loads(l) for l in (RUN/'attempts.jsonl').read_text().splitlines()]
        last=next((r for r in reversed(rows) if r['url']==item['url']),None)
        if last and last.get('http_status')==403:
            with (RUN/'new-denials.jsonl').open('a') as f:f.write(json.dumps(dict(url=item['url'],do_not_retry=True,observed_at=last['attempted_at'],http_status=403,origin=last['evidence_file']))+'\n')

if __name__=='__main__':main()
