import json,hashlib
from pathlib import Path
P=Path(__file__).parent
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
studies={x['id']:x for n in ['77c53826b14ac05c07.json','ef04ee87ab7bb284e0.json'] for x in json.loads(read(P/'evidence'/n)['text'])['studies']}
old=read(P.parent/'daily-20261014T030650-0400/avma-manual-reconciliation.json')['rows']
rows=[]
for prior in old:
    s=studies[prior['registry_id']];h=hashlib.sha256(s['description'].encode()).hexdigest()
    assert s['name']==prior['title'] and s['status']==prior['registry_status'] and h==prior['individual_api_description_sha256']
    rows.append({'registry_id':s['id'],'title':s['name'],'status':s['status'],'url':s['absolute_url'],'current_description_sha256':h,'explicit_comparison':'Current title/status/full description equal saved October14 individual record; this is not fresh provider confirmation.','canonical_id':prior.get('canonical_id'),'classification_retained_from_prior_manual_review':prior.get('classification')})
assert len(studies)==851
tagged={x['id'] for x in studies.values() if x['status']=='Recruiting' and any(t['tag_path']=='primary-field-19_oncology-1' for t in x['visible_sc_items']) and any(t['label'] in ('Canine','Feline') for t in x['visible_sc_items'])}
assert not tagged-{r['registry_id'] for r in rows}
write(P/'registry-comparison.json',{'total':851,'unique':len(studies),'current_tagged_recruiting_oncology':len(tagged),'full_cross_specialty_review_signals':len(rows),'new_tagged_recruiting_identities':[],'rows':rows,'current_page_evidence':['evidence/77c53826b14ac05c07.json','evidence/ef04ee87ab7bb284e0.json'],'clinical_access_limit':'Exact retained source-specific primary gaps remain; recheck by new primary signal or October21.'})
mapping={23693:'csu-ucc-lapatinib-rt',23721:'csu-osa-car-t-met',28702:'csu-agasaca-node-map',23714:'csu-glioma-verdinexor-only-2026',23719:'csu-osa-carboplatin-pain',28250:'csu-feline-oscc-immunotherapy',23725:'csu-sarcoma-engineered-tcells',23722:'csu-cotc033-vaccine-immunity',28144:'csu-tvt-single-radiation-2026',23708:'csu-brain-cart-verdinexor',28251:'csu-aml-trametinib',23713:'csu-brain-barc',28714:'csu-ucc-icg-surgery',23724:'csu-osa-dual-energy-ct',23691:'csu-osa-3d-limb-spare'}
csu=json.loads(read(P/'evidence/a0090b8e25156cf285.json')['text']);assert csu['total']==len(csu['studies'])==39
catalog={r['id']:r for r in read(P/'before-trials_base.json')}
rows=[{'portal_id':s['id'],'title':s['name'],'url':s['absolute_url'],'status':s['status'],'canonical_id':mapping[s['id']],'canonical_available':catalog[mapping[s['id']]].get('available_for_matching'),'description_sha256':hashlib.sha256(s['description'].encode()).hexdigest(),'description':s['description']} for s in csu['studies'] if s['id'] in mapping]
assert len(rows)==15
write(P/'csu-comparison.json',{'gallery_total':39,'oncology_dog_cat_identities':15,'flint_master_labels':11,'rows':rows,'nonmatchable_note':'BARC is one sampling protocol with historical species records; no new trial counted. Diagnostic ICG/node mapping/CT excluded from treatment matching.','unresolved':'Site variation COTC033; current summary is not the full individual eligibility/site list.'})
reviews=read(P/'reviews.json')
for r in reviews:
    if r['source_id']=='registry-avma-veterinary-clinical-trials':r['current_roster']=read(P/'registry-comparison.json')['rows']
    if r['source_id']=='usa-colorado-state-vth-clinical-trials':r['current_roster']=rows
write(P/'reviews.json',reviews)
print('Current registry851 /66 signals unchanged; current CSU39 /15 dog-cat oncology identities compared.')
