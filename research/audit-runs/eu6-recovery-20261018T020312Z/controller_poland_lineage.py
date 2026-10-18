"""Independent controller verification of all222 retained Poland proposal objects against remotely authenticated own inputs."""
import hashlib,json,pathlib
BASE=pathlib.Path(__file__).resolve().parent;OWN=BASE/'worker-3';P=OWN/'checkpoints/block-5'
def read(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
manifest=read(OWN/'input/inheritance-manifest.json');expected={r['local_path']:r['sha256'] for r in manifest['copied']}
loc=read(P/'working/effective-proposal-locators.json');current=read(P/'proposed_changes.json')['changes'];actual={(c['source_id'],c['operation'],c['field']):c for c in current};cache={};differences=[];checked=[]
for row in loc['locators']:
 rel='input/prior/'+row['frozen_path'];assert rel in expected and expected[rel]==row['file_sha256']
 assert row['frozen_path'].startswith(('working/','checkpoints/','sources/')) and '..' not in pathlib.PurePosixPath(rel).parts
 assert not any(t in rel.lower() for t in ['quarantine','cancelled','private-use'])
 if rel not in cache:
  b=(OWN/rel).read_bytes();assert digest(b)==expected[rel];cache[rel]=json.loads(b)
 record=cache[rel]
 for token in row['json_pointer'].split('/')[1:]:
  token=token.replace('~1','/').replace('~0','~');record=record[int(token)] if isinstance(record,list) else record[token]
 assert digest(canonical(record))==row['record_sha256']
 key=(row['source_id'],row['operation'],row['field']);c=actual[key]
 assert record['old_value']==c['old_value']
 old,new=record['new_value'],c['new_value']
 if old!=new:
  fields=set(old)|set(new) if isinstance(old,dict) else [row['field']]
  for field in fields:
   a=old.get(field) if isinstance(old,dict) else old;b=new.get(field) if isinstance(new,dict) else new
   if a!=b:differences.append({'source_id':row['source_id'],'field':field,'old_value':a,'new_value':b})
 checked.append({'effective_index':row['effective_index'],'source_id':row['source_id'],'operation':row['operation'],'field':row['field'],'source_file':rel,'source_file_sha256':row['file_sha256'],'retained_object_sha256':row['record_sha256'],'current_object_sha256':digest(canonical(c))})
assert len(checked)==len(actual)==222 and sorted(r['effective_index'] for r in checked)==list(range(222))
assert all(x['field']=='email' and x['new_value'] is None and 'ilawa' in x['source_id'] for x in differences),differences
print(json.dumps({'run_id':BASE.name,'slot':3,'country':'Poland','records':222,'unique_source_files':len(cache),'source_file_and222_object_hashes':'PASS','old_value_inheritance':'PASS','clinical_new_value_differences':differences,'old_sources_remote_sha':manifest['prior_remote_sha'],'checked':checked,'site_publication':False},ensure_ascii=False))

