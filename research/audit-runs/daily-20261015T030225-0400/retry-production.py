import json,subprocess,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2];f=P/'production-readback.json';d=json.loads(f.read_text());(P/'production-readback-initial.json').write_bytes(f.read_bytes());raw=ROOT.parent/'production-readback'/P.name
at=lambda:datetime.now(ZoneInfo('America/New_York')).isoformat()
for c in d['checks']:
 if c['exit_code']!=28:continue
 first=dict(c);out=raw/(c['name']+'-retry.body');start=at();p=subprocess.run(['curl','-L','--compressed','-sS','--connect-timeout','5','--max-time','20','-o',str(out),'-w','%{http_code}',c['url']],capture_output=True,text=True);body=out.read_bytes() if out.exists() else b'';sh=hashlib.sha256(body).hexdigest()
 c.update({'initial_attempt':first,'retry':1,'attempted_at':start,'completed_at':at(),'exit_code':p.returncode,'http_status':p.stdout,'live_sha256':sh,'bytes':len(body),'equal':sh==c['expected_sha256'],'stderr':p.stderr[:250]})
d['verified_at']=at();d['status']='PASS' if all(c['equal'] and c['exit_code']==0 and c['http_status']=='200' for c in d['checks']) else 'NOT VERIFIED';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2))
