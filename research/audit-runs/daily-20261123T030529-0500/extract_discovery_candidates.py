#!/usr/bin/env python3
import glob,json,pathlib,re
from urllib.parse import urlsplit,urlunsplit,unquote

ROOT=pathlib.Path(__file__).resolve().parents[3]
RUN=pathlib.Path(__file__).resolve().parent
def norm(u):
 p=urlsplit(u.strip()); path=re.sub(r'/+','/',unquote(p.path or '/'))
 if path!='/': path=path.rstrip('/')
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,''))

rows=[]
for fn in sorted(glob.glob(str(RUN/'discovery-search-*.json'))):
 d=json.load(open(fn)); payload=d.get('result',d); text='\n'.join(x.get('text','') for x in payload.get('content',[]) if x.get('type')=='text')
 parts=re.split(r'\n-{20,}\n',text)
 for part in parts:
  m=re.search(r'^(.+?) \((https?://[^\s)]+)\)\n【[^】]+】',part,re.M)
  if not m: continue
  rows.append({'title':m.group(1).strip(),'url':m.group(2),'search_artifact':str(pathlib.Path(fn).relative_to(ROOT)),'snippet':part[:4000]})
uniq={}
for r in rows: uniq.setdefault(norm(r['url']),r)
catalog=json.load(open(ROOT/'data/trials_base.json'))
exact={}
for t in catalog:
 for k in ('url','source_url','status_source','funding_source','contact_source'):
  u=t.get(k)
  if isinstance(u,str) and u.startswith('http'): exact.setdefault(norm(u),[]).append(t['id'])
inventory=json.load(open(ROOT/'data/source_inventory.json'))['sources']
inv={}
for s in inventory:
 for u in [s['master_url']]+(s.get('fallback_urls') or []): inv.setdefault(norm(u),[]).append(s['id'])
out=[]
for k,r in uniq.items():
 r['exact_canonical_ids']=sorted(set(exact.get(k,[])))
 r['exact_source_ids']=sorted(set(inv.get(k,[])))
 out.append(r)
(RUN/'discovery-candidates-raw.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'raw':len(rows),'unique':len(out),'exact_catalog':sum(bool(x['exact_canonical_ids']) for x in out),'source_index':sum(bool(x['exact_source_ids']) for x in out)},ensure_ascii=False))
for r in out:
 if not r['exact_canonical_ids'] and not r['exact_source_ids']:
  print(r['title'][:90],r['url'])
