"""Serialize the explicitly staged, verified tree for configured GitHub publication."""
import json,subprocess,hashlib,base64,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];P=Path(__file__).parent;OUT=ROOT.parent/('publish-'+P.name)
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False)+'\n')
if sys.argv[1]=='prepare':
 OUT.mkdir(exist_ok=True)
 files=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).split(b'\0');entries=[];big=[];known=set(subprocess.check_output(['git','ls-tree','-r','HEAD'],cwd=ROOT,text=True).split())
 for f in files:
  if not f:continue
  rel=f.decode();data=(ROOT/rel).read_bytes();sha=subprocess.check_output(['git','hash-object','--',rel],cwd=ROOT,text=True).strip();e={'path':rel,'mode':'100644','type':'blob'}
  if sha in known:e['sha']=sha
  elif len(data)>180000:
   e['sha']=sha;big.append({'path':rel,'sha':sha,'bytes':len(data),'chunks':(len(data)+179999)//180000})
  else:e['content']=data.decode('utf-8')
  entries.append(e)
 # Duplicate content shares one blob, and no unknown SHA is reused without upload.
 uniq={x['sha']:x for x in big};big=list(uniq.values());batch=[];batches=[];size=0
 for e in entries:
  n=len(json.dumps(e,ensure_ascii=False).encode())
  if batch and size+n>230000:batches.append(batch);batch=[];size=0
  batch.append(e);size+=n
 if batch:batches.append(batch)
 for i,b in enumerate(batches):write(OUT/f'batch-{i}.json',b)
 write(OUT/'plan.json',{'files':len(entries),'big':big,'batches':len(batches),'expected_tree_sha':subprocess.check_output(['git','write-tree'],cwd=ROOT,text=True).strip()});print((OUT/'plan.json').read_text())
elif sys.argv[1]=='chunk':
 plan=json.loads((OUT/'plan.json').read_text());e=plan['big'][int(sys.argv[2])];data=(ROOT/e['path']).read_bytes();start=int(sys.argv[3])*180000;print(base64.b64encode(data[start:start+180000]).decode())
elif sys.argv[1]=='batch':print((OUT/f'batch-{int(sys.argv[2])}.json').read_text())
