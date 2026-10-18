"""Read-only identity-risk diagnostic, NOT catalog assembly/integration/publication."""
import collections,importlib.util,json,pathlib
BASE=pathlib.Path(__file__).resolve().parent; ROOT=BASE.parents[2]
spec=importlib.util.spec_from_file_location('care_builder',ROOT/'scripts/build_oncology_center_catalog.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
folders={1:'block-03-final',2:'normalized-final',3:'block-6',4:'clinical-12',5:'normalized-final',6:'block-03'}
frozen=BASE/'worker-1/input/current/data'
public=json.loads((frozen/'oncology_centers.json').read_text())['centers']
supp=json.loads((frozen/'oncology_centers_supplemental.json').read_text())['centers']
def matching_record(r):
 out=dict(r)
 for key in ['street','city','postal_code','region']:out[key]=r.get(key) or ''
 return out
rows={r.get('source_id') or 'public-'+str(i):matching_record(r) for i,r in enumerate(public)}
for i,r in enumerate(supp):rows.setdefault(r.get('source_id') or 'supp-'+str(i),matching_record(r))
news=[]
for slot,folder in folders.items():
 for c in json.loads((BASE/f'worker-{slot}/checkpoints'/folder/'proposed_changes.json').read_text())['changes']:
  if c['operation']=='NEW' and isinstance(c['new_value'],dict):
   r=matching_record(c['new_value']);r['source_id']=c['source_id'];news.append((slot,r))
def summary(r):return {k:r.get(k) for k in ['source_id','name','country','region','city','postal_code','street','phone','website','location_type']}
hits=[]
for slot,r in news:
 for b in rows.values():
  if builder.center_match(r,b) or builder.center_match(b,r):hits.append({'kind':'baseline','slot':slot,'new':summary(r),'other':summary(b)})
for i,(slot,r) in enumerate(news):
 for slot2,b in news[i+1:]:
  if slot==slot2 and (builder.center_match(r,b) or builder.center_match(b,r)):hits.append({'kind':'intra_country_proposals','slot':slot,'new':summary(r),'other':summary(b)})
print(json.dumps({'run_id':BASE.name,'baseline_sha':json.loads((BASE/'assignments.json').read_text())['baseline_sha'],'scope':'Read-only overly-permissive builder identity risk flags, NOT accepted duplicates or integration. Final Germany package still pending.','dict_NEW_examined':len(news),'potential_hits':hits},ensure_ascii=False))

