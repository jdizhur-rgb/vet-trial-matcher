import pathlib,json,subprocess,hashlib,time
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/owner-rules-20261103');R=ROOT/pathlib.Path('/tmp/vet-owner-rules-path').read_text();OUT=R/'evidence';OUT.mkdir(exist_ok=True)
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def norm(u):
 p=urlsplit(u);return (p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),p.query)
restr=json.loads((ROOT/'data/source_access_restrictions.json').read_text())['routes'];held={norm(a.get('url') or a.get('target_url') or '') for a in restr}
urls=['https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip=0&take=500','https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip=500&take=500']
for i,u in enumerate(urls):
 if norm(u) in held:raise RuntimeError('Exact saved restriction; no request: '+u)
 f=OUT/f'avma-page-{i+1}.json';head=OUT/f'avma-page-{i+1}.headers';attempts=[]
 for repeat in range(2):
  st=now();p=subprocess.run(['curl','--silent','--show-error','--location','--connect-timeout','5','--max-time','20','--dump-header',str(head),'--output',str(f),'--write-out','%{http_code}',u],capture_output=True,text=True);status=int(p.stdout[-3:]) if p.stdout[-3:].isdigit() else 0;attempts.append({'started_at':st,'completed_at':now(),'status':status,'exit_code':p.returncode,'stderr':p.stderr,'retry':repeat})
  if not(repeat==0 and (p.returncode in [28,7] or status==429 or status>=500)):break
  delay=0
  for line in head.read_text().splitlines():
   if line.lower().startswith('retry-after:') and line.split(':',1)[1].strip().isdigit():delay=int(line.split(':',1)[1].strip())
  if delay>30:break
  if delay:time.sleep(delay)
 result={'url':u,'method':'shell_curl','attempts':attempts,'evidence_file':str(f.relative_to(ROOT)),'retrieved_at':now(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None,'success':p.returncode==0 and status==200}
 (OUT/f'avma-page-{i+1}-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
