from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
import re,subprocess,json,hashlib
root=Path('/workspace/scratch/55af69f9810e/owner-rules-20261103');r=root/'research/audit-runs/owner-rules-20261103T065741-0500';out=r/'production';out.mkdir(exist_ok=True)
base='https://vettrialfinder.com/matcher/';html=(root/'seo/site/matcher/index.html').read_text();js=re.findall(r'<script[^>]*src="([^"]+)"',html)[-1];cat=re.search(r"MATCHER_DATA_URL='([^']+)'",html).group(1);rows=[]
for name,url,local in [('html',base,root/'seo/site/matcher/index.html'),('js',urljoin(base,js),root/'seo/site/matcher/matcher.js'),('catalog',urljoin(base,cat),root/'seo/site/matcher/trials.json')]:
 start=datetime.now(ZoneInfo('America/New_York')).isoformat();p=subprocess.run(['curl','--connect-timeout','5','--max-time','20','-L','-sS','-D',str(out/(name+'.headers')),'-o',str(out/(name+'.body')),'-w','%{http_code}',url],capture_output=True,text=True);end=datetime.now(ZoneInfo('America/New_York')).isoformat();b=(out/(name+'.body')).read_bytes() if (out/(name+'.body')).exists() else b'';expected=local.read_bytes();rows.append({'name':name,'url':url,'method':'shell_curl','started_at':start,'completed_at':end,'http_status':p.stdout,'exit_code':p.returncode,'stderr':p.stderr,'local_sha256':hashlib.sha256(expected).hexdigest(),'live_sha256':hashlib.sha256(b).hexdigest(),'equal':b==expected,'evidence':str((out/(name+'.body')).relative_to(root))})
d={'commit':'5fc2f1db27ec9314b7544cf409b0d3055372592d','deploy_run':41634278066,'script_version':'clinical-audit-20261103-owner-rules-r1','catalog_version':'5d031c3b8485f52b','result':'PASS' if all(x['equal'] and x['http_status']=='200' and x['exit_code']==0 for x in rows) else 'NOT VERIFIED','rows':rows};(r/'production-byte-readback.json').write_text(json.dumps(d,indent=2)+'\n');print(d['result']);print([(x['name'],x['http_status'],x['equal']) for x in rows])
raise SystemExit(d['result']!='PASS')
