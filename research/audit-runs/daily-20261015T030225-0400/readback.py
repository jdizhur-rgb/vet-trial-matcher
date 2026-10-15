import subprocess,json,hashlib,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
P=Path(__file__).parent;ROOT=P.parents[2];at=lambda:datetime.now(ZoneInfo('America/New_York')).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
head=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();rows=[]
for f in ['data/source_inventory.json','data/trials_base.json','data/audit_state.json','data/audit_source_coverage.json']:
 local=(ROOT/f).read_bytes();remote=subprocess.check_output(['git','show','origin/main:'+f],cwd=ROOT);rows.append({'path':f,'local_sha256':sha(local),'remote_sha256':sha(remote),'equal':local==remote})
localdates=json.loads((P/'local-date-readback.json').read_text());remoteinv=json.loads(subprocess.check_output(['git','show','origin/main:data/source_inventory.json'],cwd=ROOT));disk=json.loads((ROOT/'data/source_inventory.json').read_text());date_ok=all((a['id'],a.get('last_checked'),a.get('last_checked_at'),a.get('last_result'))==(b['id'],b.get('last_checked'),b.get('last_checked_at'),b.get('last_result')) for a,b in zip(disk['sources'],remoteinv['sources']))
write(P/'remote-readback.json',{'verified_at':at(),'remote_main_sha':head,'local_head_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'status':'PASS' if all(x['equal'] for x in rows) and date_ok else 'FAIL','files':rows,'per_source_dates_results_equal':date_ok,'date_readback':localdates})
# Production byte readback. Native transport is not substituted with search cache.
base='https://vettrialfinder.com/matcher/';html=(ROOT/'seo/site/matcher/index.html').read_bytes();s=html.decode();js=re.search(r'<script src="([^"\n]*matcher\.js[^"\n]*)"',s).group(1);cat=re.search(r"MATCHER_DATA_URL='([^']+)'",s).group(1)
checks=[];rawdir=ROOT.parent/'production-readback'/P.name;rawdir.mkdir(parents=True,exist_ok=True)
for name,relative,expected in [('html','',html),('javascript',js,(ROOT/'seo/site/matcher/matcher.js').read_bytes()),('catalog',cat,(ROOT/'seo/site/matcher/trials.json').read_bytes())]:
 url=urljoin(base,relative);out=rawdir/(name+'.body');started=at();p=subprocess.run(['curl','-L','--compressed','-sS','--connect-timeout','5','--max-time','20','-o',str(out),'-w','%{http_code}',url],capture_output=True,text=True);body=out.read_bytes() if out.exists() else b''
 checks.append({'name':name,'url':url,'attempted_at':started,'completed_at':at(),'method':'shell_curl','exit_code':p.returncode,'http_status':p.stdout,'expected_sha256':sha(expected),'live_sha256':sha(body),'bytes':len(body),'equal':body==expected,'stderr':p.stderr[:250]})
write(P/'production-readback.json',{'verified_at':at(),'publication_sha':head,'status':'PASS' if all(x['equal'] and x['http_status']=='200' and x['exit_code']==0 for x in checks) else 'NOT VERIFIED','script_version':js,'catalog_version':cat,'note':'No JS or catalog change in this data-audit publication; content-derived catalog version and existing verified script version must match the build, not receive a fictional daily bump.','checks':checks});print(json.dumps(checks,indent=2))
