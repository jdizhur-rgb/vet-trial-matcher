"""Independent controller integrity, baseline-old-value and retained-delta checks; no source requests or production writes."""
import ast,collections,hashlib,json,pathlib,re,sys,unicodedata,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[3];BASE=pathlib.Path(__file__).resolve().parent
A=json.loads((BASE/'assignments.json').read_text());SLOTS={1:'block-03-final',2:'final',5:'recovery-01',6:'block-02'}
OLD={1:'final-delivery',2:'final-publicsafe',5:'block-66',6:'block-67'}
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(x):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',str(x).casefold().replace('ß','ss')).encode('ascii','ignore').decode())
def url(x):
 try:
  z=urllib.parse.urlsplit(str(x));return z.hostname.removeprefix('www.')+z.path.rstrip('/') if z.hostname else ''
 except:return ''
def phone(x):
 s=re.sub('[^0-9]','',str(x));return s[2:] if s.startswith('00') else s
rows=[];row_counts={}
for f,key in [('oncology_centers.json','centers'),('oncology_centers_supplemental.json','centers'),('oncology_care_source_inventory.json','sources'),('acvim_oncology_profiles.json','profiles')]:
 data=read(BASE/'worker-1/input/current/data'/f)[key];row_counts[f]=len(data);rows.extend((f,r) for r in data)
mod=ast.parse((BASE/'worker-1/input/current/seo/oncology_teleconsultations.py').read_text())
tele=next(ast.literal_eval(x.value) for x in mod.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ROWS' for t in x.targets))
row_counts['tele']=len(tele)
for t in tele:rows.append(('tele',dict(zip(['region','country','name','clinician','credentials','access','specialty','details','website','clinician_url','assignment'],t))))
byid=collections.defaultdict(list)
for f,r in rows:
 if r.get('source_id') or r.get('id'):byid[r.get('source_id') or r['id']].append((f,r))
def signature(c):return (c.get('operation'),c.get('source_id'),c.get('field'))
output={'run_id':A['run_id'],'baseline_sha':A['baseline_sha'],'controller':'/root','five_input_row_counts':row_counts,'total_representation_rows':sum(row_counts.values()),'slots':[]}
allnew=[]
for slot,folder in SLOTS.items():
 own=BASE/f'worker-{slot}';p=own/'checkpoints'/folder;assignment=next(x for x in A['assignments'] if x['slot']==slot);country=assignment['country']
 expected=(A['run_id'],slot,country,A['baseline_sha']);proof={'slot':slot,'country':country,'checkpoint':str(p.relative_to(ROOT)),'files':{},'identity_errors':[],'old_value_comparisons':[],'new_semantic_hits':[],'network_pin_errors':[]}
 for name in ['proposed_changes.json','result.json','evidence.json','queries.json','remaining.json']:
  j=read(p/name);actual=tuple(j.get(k) for k in ['run_id','slot','country','baseline_sha']);assert actual==expected,(name,actual,expected)
  proof['files'][name]={'sha256':digest(p/name),'bytes':(p/name).stat().st_size}
 report=(p/'report.md').read_text();assert len(report)>10000 and country in report and A['run_id'] in report
 proof['files']['report.md']={'sha256':digest(p/'report.md'),'bytes':(p/'report.md').stat().st_size,'lines':len(report.splitlines())}
 current=read(p/'proposed_changes.json');previous=read(own/'input/prior/checkpoints'/OLD[slot]/'proposed_changes.json')
 oldmap={signature(c):c for c in previous['changes']};changes=current['changes'];proof['operations']=dict(collections.Counter(c.get('operation') for c in changes));deltas=[]
 for c in changes:
  sid=c.get('source_id');key=signature(c);op=c.get('operation');value=c.get('new_value')
  if key in oldmap and value!=oldmap[key].get('new_value'):
   before=oldmap[key].get('new_value');fields=sorted(set(before)|set(value)) if isinstance(before,dict) and isinstance(value,dict) else [c.get('field')]
   for field in fields:
    bv=before.get(field) if isinstance(before,dict) else before;av=value.get(field) if isinstance(value,dict) else value
    if bv!=av:deltas.append({'source_id':sid,'field':field,'old_value':bv,'new_value':av})
  elif key not in oldmap:deltas.append({'source_id':sid,'new_signature':key})
  if op=='UPDATE' and c.get('publication_eligible',True) and c.get('effective_publication_eligible',True):
   field=c.get('field');targets=[(f,r) for f,r in byid[sid] if field in r]
   assert targets,('No baseline field',sid,field)
   for f,r in targets:proof['old_value_comparisons'].append({'source_id':sid,'field':field,'store':f,'match':r[field]==c.get('old_value'),'already_applied':r[field]==value})
  if op not in ['NEW','ADD'] or not isinstance(value,dict):continue
  assert value.get('country')==country,(sid,'wrong candidate country',value.get('country'))
  allnew.append((slot,sid,value));h=[]
  for f,r in rows:
   signals=[]
   if sid and sid in [r.get('source_id'),r.get('id')]:signals.append('source_id')
   if value.get('phone') and phone(value['phone']) and phone(value['phone'])==phone(r.get('phone','')):signals.append('phone')
   if value.get('street') and value.get('city') and norm(value['street'])==norm(r.get('street','')) and norm(value['city'])==norm(r.get('city','')):signals.append('street_city')
   if value.get('name') and norm(value['name'])==norm(r.get('name','')):signals.append('exact_name')
   if signals:h.append({'store':f,'baseline_id':r.get('source_id') or r.get('id'),'baseline_name':r.get('name'),'signals':signals})
  if h:proof['new_semantic_hits'].append({'source_id':sid,'hits':h})
  if value.get('location_type')=='network':
   bad={k:value.get(k) for k in ['street','city','postal_code','latitude','longitude'] if value.get(k) not in [None,'']}
   if bad:proof['network_pin_errors'].append({'source_id':sid,'fields':bad})
 proof['new_value_deltas_against_accepted_prior']=deltas;proof['research_complete_claim']=read(p/'result.json').get('research_complete');proof['prior_acceptance']=read(own/f'input/worker-acceptance-{slot}.json')
 output['slots'].append(proof)
output['cross_country_strong_hits']=[]
for i,(s1,id1,r1) in enumerate(allnew):
 for s2,id2,r2 in allnew[i+1:]:
  if s1==s2:continue
  if id1==id2 or (r1.get('phone') and phone(r1['phone'])==phone(r2.get('phone',''))):output['cross_country_strong_hits'].append([s1,id1,s2,id2])
print(json.dumps(output,ensure_ascii=False))

