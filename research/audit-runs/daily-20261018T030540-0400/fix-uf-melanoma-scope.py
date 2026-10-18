from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cat=read(ROOT/'data/trials_base.json');r=next(x for x in cat if x['id']=='uf-oral-melanoma-vaccine-pd1');before=copy.deepcopy(r);r['requires'].pop('prior_surgery');r['requires']['oral_tumor_not_excised']=True;r['verified']='2026-10-18'
rules=read(ROOT/'data/matcher_protocol_rules.json');rules['requires']['oral_tumor_not_excised']={'label':'oral melanoma has not been surgically excised (diagnostic biopsy is a separate procedure)','field':'oral_tumor_excised','allowed':['No']};write(ROOT/'data/matcher_protocol_rules.json',rules);write(ROOT/'data/trials_base.json',cat)
cases=read(ROOT/'data/protocol_selection_cases.json');c=next(x for x in cases['reviews'] if x['trial_id']==r['id']);old=copy.deepcopy(c)
for t in c['cases']:
 if t['expected']=='exclude' and t['patient'].get('surgery')=='Yes':t['patient']['oral_tumor_excised']='Yes';t['clinical_scope_correction']='Confirmed oral tumor excision is excluded; general unrelated surgery alone does not establish that.'
c['cases'] += [
 {'name':'Unknown indication of past surgery requires screening','patient':{'species':'Dog','country':'USA','cancer':'Oral melanoma','surgery':'Yes'},'expected':'review','unknown_contains':['oral melanoma has not']},
 {'name':'Unrelated surgery does not establish oral tumor excision','patient':{'species':'Dog','country':'USA','cancer':'Oral melanoma','surgery':'Yes','oral_tumor_excised':'No'},'expected':'review'},
 {'name':'Known excised oral melanoma remains excluded','patient':{'species':'Dog','country':'USA','cancer':'Oral melanoma','oral_tumor_excised':'Yes'},'expected':'exclude'}]
packet=next(x for x in read(P/'clinical-packets.json') if x['trial_id']==r['id']);c['source_read_at']=packet['origin'][0]['read_at'];c['current_primary_evidence']=packet['origin'][0]['evidence'];c['criteria']+=' Current full protocol explicitly says the oral tumor must not have been excised; general history of surgery does not prove this. Required diagnostic tumor biopsies are distinct from tumor excision.'
from datetime import datetime
from zoneinfo import ZoneInfo
c['reviewed_at']=datetime.now(ZoneInfo('America/New_York')).isoformat();fields=read(ROOT/'data/protocol_selection_baseline.json')['signature_fields'];c['selection_sha256']=hashlib.sha256(json.dumps({k:r.get(k) for k in fields},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();write(ROOT/'data/protocol_selection_cases.json',cases)
write(P/'uf-melanoma-scope-correction.json',{'before':before,'after':r,'original_review':old,'current_review':c,'primary_evidence':packet['origin'],'literal_reason':'The source prohibits prior excision of the oral melanoma, not every past operation; biopsy itself is mandatory in the study. Specific unknown excision status remains screening, never a Likely match.'})
