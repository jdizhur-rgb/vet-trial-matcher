import hashlib,json,pathlib
P=pathlib.Path(__file__).parent
ROOT=P.parents[2]
def sha(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
before=json.loads((ROOT.parent/'ma-source-cache/integration-baseline.json').read_text())
expected={r['source_id'] for f in ['published-records.json','existing-updates.json'] for r in json.loads((P/f).read_text())}
manifest={'run_id':'ma-care-20261028','baseline_sha':(P/'baseline-sha.txt').read_text().strip(),'collections':{}}
for path,b in before.items():
 a=json.loads((ROOT/path).read_text());key='id' if 'inventory' in path else 'source_id';field='sources' if key=='id' else 'centers';br=b[field];ar=a[field];changes=[];nonafter=[]
 wanted=expected | ({'integrity-veterinary-center'} if key=='id' else set())
 byid={r.get(key):r for r in br if r.get(key)}
 byname={tuple(r.get(k) for k in ['name','city','country','postal_code']):r for r in br} if key=='source_id' else {}
 for r in ar:
  if r.get(key) in wanted:
   old=byid.get(r[key]) or byname.get(tuple(r.get(k) for k in ['name','city','country','postal_code']))
   changes.append({'id':r[key],'before':old,'after_sha256':sha(r)})
  else:nonafter.append(r)
 changed={sha(c['before']) for c in changes if c['before'] is not None};nonbefore=[r for r in br if sha(r) not in changed]
 sortkey=lambda r:r.get(key) or '|'.join(str(r.get(k,'')) for k in ['name','city','country','postal_code'])
 assert sha(sorted(nonbefore,key=sortkey))==sha(sorted(nonafter,key=sortkey)),path
 assert {c['id'] for c in changes}==wanted,(path,len(changes))
 manifest['collections'][path]={'key':key,'before_count':len(br),'after_count':len(ar),'changes':changes,'unchanged_rows_sha256':sha(sorted(nonbefore,key=sortkey))}
(P/'baseline-projection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print({k:(v['before_count'],v['after_count'],len(v['changes'])) for k,v in manifest['collections'].items()})
