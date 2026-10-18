from pathlib import Path
import re,subprocess,hashlib,json
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).resolve().parent;ROOT=P.parents[2];raw=ROOT.parent/'raw-evidence'/P.name;raw.mkdir(exist_ok=True)
html=(ROOT/'seo/site/matcher/index.html').read_text();js=re.search(r'<script src="(\./matcher.js[^\"]*)"',html).group(1);cat=re.search(r"window.MATCHER_DATA_URL='([^']+)'",html).group(1)
checks=[]
for name,route,file in [('html','',ROOT/'seo/site/matcher/index.html'),('javascript',js.removeprefix('./'),ROOT/'seo/site/matcher/matcher.js'),('catalog',cat.removeprefix('./'),ROOT/'seo/site/matcher/trials.json')]:
 at=datetime.now(ZoneInfo('America/New_York')).isoformat();url='https://vettrialfinder.com/matcher/'+route;out=raw/f'production-{name}.body';p=subprocess.run(['curl','--connect-timeout','5','--max-time','20','-L','-sS','-w','%{http_code}','-o',str(out),url],text=True,capture_output=True);b=out.read_bytes() if out.exists() else b'';expected=file.read_bytes();checks.append({'name':name,'url':url,'attempted_at':at,'completed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'method':'shell_curl','exit_code':p.returncode,'http_status':p.stdout,'expected_sha256':hashlib.sha256(expected).hexdigest(),'live_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'equal':b==expected,'stderr':p.stderr})
result={'verified_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'publication_sha':'7cf7e5538c26d6e7501ab6e2a4da4d4f8eb26554','status':'PASS' if all(x['equal'] and x['http_status']=='200' for x in checks) else 'NOT_VERIFIED','script_version':js,'catalog_version':cat,'checks':checks};(P/'production-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(result['status']!='PASS')
