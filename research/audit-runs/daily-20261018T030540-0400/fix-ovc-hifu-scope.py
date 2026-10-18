from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cat=read(ROOT/'data/trials_base.json');r=next(x for x in cat if x['id']=='ca-ovc-osa-hifu');before=copy.deepcopy(r);r['excludes'].pop('prior_surgery');r['excludes']['prior_target_tumor_surgery']=True;r['requires']['distal_radius_osa']=True
rules=read(ROOT/'data/matcher_protocol_rules.json');rules['excludes']['prior_target_tumor_surgery']={'label':'previous surgery for this osteosarcoma','field':'target_tumor_prior_surgery','disallowed':['Yes']};rules['requires']['distal_radius_osa']={'label':'osteosarcoma of the distal radius','field':'osa_site_detail','allowed':['Distal radius']};write(ROOT/'data/matcher_protocol_rules.json',rules);write(ROOT/'data/trials_base.json',cat)
cases=read(ROOT/'data/protocol_selection_cases.json');c=next(x for x in cases['reviews'] if x['trial_id']==r['id']);old=copy.deepcopy(c)
for t in c['cases']:
 if t['name']=='Previous OSA surgery excluded':t['patient']['target_tumor_prior_surgery']='Yes';t['clinical_scope_correction']='Explicit OSA surgery, not an unrelated historical operation.'
c['cases'] += [
 {'name':'General previous surgery of unknown indication needs screening','patient':{'country':'Canada','cancer':'Osteosarcoma','surgery':'Yes'},'expected':'review','unknown_contains':['previous surgery for this osteosarcoma']},
 {'name':'Known unrelated prior surgery does not exclude distal-radius OSA','patient':{'country':'Canada','cancer':'Osteosarcoma','surgery':'Yes','target_tumor_prior_surgery':'No','osa_site_detail':'Distal radius'},'expected':'review'},
 {'name':'Known femur site is not distal radius','patient':{'country':'Canada','cancer':'Osteosarcoma','osa_location':'Appendicular — limb bone','osa_site_detail':'Femur'},'expected':'exclude'}]
fields=read(ROOT/'data/protocol_selection_baseline.json')['signature_fields'];c['selection_sha256']=hashlib.sha256(json.dumps({k:r.get(k) for k in fields},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();c['criteria']+=' Literal-scope correction: previous surgery excludes only surgery for this OSA, not unrelated operations; distal-radius site is a specific team-screening field.';write(ROOT/'data/protocol_selection_cases.json',cases)
write(P/'ovc-hifu-scope-correction.json',{'before':before,'after':r,'original_review':old,'current_review':c,'evidence':c['current_primary_evidence'],'reason':'Full current primary explicitly limits prior surgery/radiation exclusion to the osteosarcoma. General history question cannot establish that indication; missing specific facts remain screening. Distal-radius cohort must not silently become every limb OSA.'})
