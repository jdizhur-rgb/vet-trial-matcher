#!/usr/bin/env python3
import concurrent.futures, hashlib, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
OUT = RUN / "raw-protocols"
OUT.mkdir(exist_ok=True)

def norm(url):
    p=urlsplit(url.strip()); path=re.sub(r"/+","/",p.path or "/")
    if path!="/": path=path.rstrip("/")
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,""))

restr={}
rd=json.loads((ROOT/'data/source_access_restrictions.json').read_text())
for x in rd.get('routes',[]):
    if x.get('do_not_retry') and x.get('url'): restr[norm(x['url'])]=x
inv=json.loads((ROOT/'data/source_inventory.json').read_text())['sources']
for s in inv:
    for x in s.get('access_restrictions') or []:
        if x.get('do_not_retry') and x.get('url'): restr[norm(x['url'])]=x

trials=json.loads((ROOT/'data/trials_base.json').read_text())
public=[t for t in trials if t.get('available_for_matching') is True and t.get('study_type') in {'treatment','other_treatment_access'}]
jobs=[]
for t in public:
    seen=set()
    for field in ['url','source_url','registry_url']:
        u=t.get(field)
        if not u or not isinstance(u,str) or not u.startswith(('http://','https://')): continue
        k=norm(u)
        if k in seen: continue
        seen.add(k); jobs.append({'trial_id':t['id'],'field':field,'url':u,'normalized_url':k})

def one(j):
    st=datetime.now(timezone.utc).isoformat(); k=j['normalized_url']
    if k in restr:
        x=restr[k]
        return {**j,'started_at':st,'completed_at':datetime.now(timezone.utc).isoformat(),
                'result':'skipped_exact_restriction','status':None,
                'restriction_evidence':x.get('origin') or x.get('evidence_file') or x.get('observed_at')}
    fn=hashlib.sha256((j['trial_id']+'\n'+j['url']).encode()).hexdigest()[:20]+'.bin'; target=OUT/fn
    cmd=['curl','-L','--connect-timeout','5','--max-time','20','--retry','1','--retry-delay','1',
         '--retry-max-time','20','--retry-connrefused','-A','VetTrialFinderAudit/1.0','-sS','-o',str(target),
         '-w','%{http_code}',j['url']]
    p=subprocess.run(cmd,capture_output=True,text=True); stxt=p.stdout.strip()[-3:]
    status=int(stxt) if stxt.isdigit() and stxt!='000' else None
    body=target.read_bytes() if target.exists() else b''
    if status is not None:
        return {**j,'started_at':st,'completed_at':datetime.now(timezone.utc).isoformat(),
                'result':'http_response','status':status,'bytes':len(body),'curl_exit':p.returncode,
                'content_sha256':hashlib.sha256(body).hexdigest(),'artifact':str(target.relative_to(ROOT)),
                'stderr':p.stderr[-2000:]}
    target.unlink(missing_ok=True)
    return {**j,'started_at':st,'completed_at':datetime.now(timezone.utc).isoformat(),
            'result':'transport_error','status':None,'curl_exit':p.returncode,
            'error':p.stderr[-2000:] or 'curl returned no HTTP status'}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(one,jobs))
result={'run_id':RUN.name,'recorded_at':datetime.now(timezone.utc).isoformat(),
        'method':'curl; connect timeout 5s, total timeout 20s, one transient retry; exact restriction guard',
        'restriction_count_loaded':len(restr),'public_trial_total':len(public),'jobs':len(jobs),'attempts':rows}
(RUN/'current-protocol-evidence.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'public_trials':len(public),'jobs':len(jobs),
                  'results':{k:sum(r['result']==k for r in rows) for k in sorted({r['result'] for r in rows})}},indent=2))
