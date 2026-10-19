"""Finite actual production byte readback against the independently clean build."""
from daily19 import ROOT,RUN,read,write,now
from pathlib import Path
import subprocess,hashlib,json,re
from urllib.parse import urljoin
build=Path('/workspace/scratch/7a43f0b7d905/trial-build-HF56L8/seo/site/matcher');out=RUN/'production-readback';out.mkdir(exist_ok=True)
html=(build/'index.html').read_text();catalog=re.search(r"MATCHER_DATA_URL='([^']+)'",html)[1];script=re.search(r'<script src="([^\"]*matcher.js[^\"]*)"',html)[1]
rows=[]
for name,path in [('index.html','https://vettrialfinder.com/matcher/'),('matcher.js',urljoin('https://vettrialfinder.com/matcher/',script)),('trials.json',urljoin('https://vettrialfinder.com/matcher/',catalog))]:
 at=now();cmd=['curl','--silent','--show-error','--location','--connect-timeout','5','--max-time','20','--dump-header',str(out/(name+'.headers')),'--output',str(out/name),'--write-out','%{http_code}',path]
 p=subprocess.run(cmd,capture_output=True,text=True);body=(out/name).read_bytes() if (out/name).exists() else b''
 row={'url':path,'file':str((out/name).relative_to(ROOT)),'attempted_at':at,'finished_at':now(),'method':'shell_curl','http_status':p.stdout,'exit_code':p.returncode,'stderr':p.stderr,'sha256':hashlib.sha256(body).hexdigest(),'expected_sha256':hashlib.sha256((build/name).read_bytes()).hexdigest(),'identical_bytes':body==(build/name).read_bytes() and p.returncode==0 and p.stdout=='200'}
 rows.append(row)
result={'at':now(),'expected_data_url':catalog,'expected_script_url':script,'js_source_changed':False,'catalog_cache_version_changed':True,'rows':rows,'byte_readback':'PASS' if all(r['identical_bytes'] for r in rows) else 'NOT_VERIFIED'}
write(RUN/'production-byte-readback.json',result);print(json.dumps(result,ensure_ascii=False))
