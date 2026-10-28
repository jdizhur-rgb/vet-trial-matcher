import concurrent.futures,datetime,hashlib,json,pathlib,subprocess
R=pathlib.Path(__file__).parent
ROOT=R.parents[2]
items=[('index.html','https://vettrialfinder.com/matcher/'),('matcher.js','https://vettrialfinder.com/matcher/matcher.js?v=clinical-audit-20261028-r2'),('trials.json','https://vettrialfinder.com/matcher/trials.json')]
def read(item):
 name,url=item
 before=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=R/('live-'+name)
 c=subprocess.run(['curl','--connect-timeout','5','--max-time','20','-L','-sS','-D',str(R/('live-'+name+'.headers')),'-o',str(p),'-w','%{http_code}',url],capture_output=True,text=True)
 b=p.read_bytes() if p.exists() else b''
 expected=(ROOT/'seo/site/matcher'/name).read_bytes()
 return {'url':url,'method':'shell_curl','attempted_at':before,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':c.returncode,'http_status':c.stdout,'error':c.stderr,'sha256':hashlib.sha256(b).hexdigest(),'expected_sha256':hashlib.sha256(expected).hexdigest(),'exact_match':b==expected,'evidence_file':str(p.relative_to(ROOT))}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(read,items))
html=(R/'live-index.html').read_text()
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':'e4ec0906b59b554d12ff01166c3f19757cf97bbc','files':rows,'script_version_present':'matcher.js?v=clinical-audit-20261028-r2' in html,'status':'PASS' if all(x['exact_match'] and x['http_status']=='200' for x in rows) else 'NOT VERIFIED'}
(R/'production-readback.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
