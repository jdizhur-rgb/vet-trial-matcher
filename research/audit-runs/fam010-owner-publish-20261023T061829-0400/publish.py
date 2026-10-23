"""Prepare exact Git objects for a leased main publication of reviewed files."""
from pathlib import Path
import json,subprocess,sys,base64
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
OUT=ROOT.parent/'publish-fam010'
OUT.mkdir(exist_ok=True)
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
if sys.argv[1]=='prepare':
 known=set(subprocess.check_output(['git','ls-tree','-r','HEAD'],cwd=ROOT,text=True).split())
 entries=[];big={}
 for raw in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).split(b'\0'):
  if not raw:continue
  path=raw.decode();b=(ROOT/path).read_bytes();sha=subprocess.check_output(['git','hash-object','--',path],cwd=ROOT,text=True).strip();e=dict(path=path,mode='100644',type='blob')
  if sha in known:e['sha']=sha
  elif len(b)>150000:e['sha']=sha;big[sha]=dict(path=path,sha=sha,bytes=len(b),chunks=(len(b)+99998)//99999)
  else:e['content']=b.decode()
  entries.append(e)
 batches=[];batch=[];size=0
 for e in entries:
  n=len(json.dumps(e).encode())
  if batch and n+size>180000:batches.append(batch);batch=[];size=0
  batch.append(e);size+=n
 if batch:batches.append(batch)
 for i,b in enumerate(batches):write(OUT/f'batch-{i}.json',b)
 plan=dict(files=len(entries),big=list(big.values()),batches=len(batches),base_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),base_tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip(),expected_tree_sha=subprocess.check_output(['git','write-tree'],cwd=ROOT,text=True).strip());write(OUT/'plan.json',plan);print(json.dumps(plan))
elif sys.argv[1]=='chunk':
 p=json.loads((OUT/'plan.json').read_text())['big'][int(sys.argv[2])];offset=int(sys.argv[3])*99999;print(base64.b64encode((ROOT/p['path']).read_bytes()[offset:offset+99999]).decode())
elif sys.argv[1]=='batch':print((OUT/f'batch-{sys.argv[2]}.json').read_text())
