"""Prepare an exact reviewed Git tree for CAS publication; no untested data edits."""
from daily23 import ROOT,RUN,read,write,now
import subprocess,hashlib,sys,json
OUT=ROOT.parent/'publish-daily23';OUT.mkdir(exist_ok=True)
if sys.argv[1]=='prepare':
 known=set(subprocess.check_output(['git','ls-tree','-r','HEAD'],cwd=ROOT,text=True).split());paths=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).split(b'\0');entries=[];big={}
 for b in paths:
  if not b:continue
  path=b.decode();data=(ROOT/path).read_bytes();sha=subprocess.check_output(['git','hash-object','--',path],cwd=ROOT,text=True).strip();e=dict(path=path,mode='100644',type='blob')
  if sha in known:e['sha']=sha
  elif len(data)>150000:e['sha']=sha;big[sha]=dict(path=path,sha=sha,bytes=len(data),chunks=(len(data)+99998)//99999)
  else:e['content']=data.decode()
  entries.append(e)
 batches=[];batch=[];size=0
 for e in entries:
  n=len(json.dumps(e).encode())
  if batch and size+n>200000:batches.append(batch);batch=[];size=0
  batch.append(e);size+=n
 if batch:batches.append(batch)
 for i,b in enumerate(batches):write(OUT/f'batch-{i}.json',b)
 plan=dict(files=len(entries),big=list(big.values()),batches=len(batches),expected_tree_sha=subprocess.check_output(['git','write-tree'],cwd=ROOT,text=True).strip());write(OUT/'plan.json',plan);print(json.dumps({k:v if k!='big' else [dict(path=x['path'],bytes=x['bytes']) for x in v] for k,v in plan.items()}))
elif sys.argv[1]=='chunk':
 import base64
 e=read(OUT/'plan.json')['big'][int(sys.argv[2])];start=int(sys.argv[3])*99999;print(base64.b64encode((ROOT/e['path']).read_bytes()[start:start+99999]).decode())
elif sys.argv[1]=='batch':print((OUT/f'batch-{sys.argv[2]}.json').read_text())
