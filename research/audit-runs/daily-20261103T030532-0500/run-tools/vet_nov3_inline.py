import pathlib,json,re,hashlib
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
from html import unescape
def clinical_islands(islands):
 out={}
 for raw in islands:
  try:v=json.loads(raw)
  except (TypeError,ValueError):continue
  if isinstance(v,dict):
   if 'speciesListDisplay' in v and 'description' in v:out['protocol_content']=v
   elif 'inclusion_criteria' in v and 'intervention_name' in v:out['registry_protocol_details']=v
   elif 'vct_code' in v and 'selection_species' in v:out['registry_protocol_attributes']=v
   elif 'publicId' in v:
    allowed=['publicId','studypageStatus','studyStartDate','studyEndDate','contactName','contactEmail','spPhoneConditional','iacucNumber','avmaId','studyCode','recruitmentTarget','joinButtonTextLong','joinButtonTextShort','schemaVersion']
    out['published_values']={k:v[k] for k in allowed if k in v}
   elif 'isStudypageActive' in v or 'is_studypage_active' in v or 'joinButtonEnabled' in v:
    out['published_access_flags']={k:z for k,z in v.items() if k.lower().replace('_','') in ['isstudypageactive','isactive','isactivenyr','joinbuttonenabled','isfinishedrec','requireslogin']}
  elif isinstance(v,list) and v and isinstance(v[0],dict):
   if 'display_name' in v[0] and 'organization' in v[0]:out['published_investigators']=v
   elif 'location' in v[0] and 'name' in v[0]:out['published_locations']=v
   elif 'file_url' in v[0]:out['published_protocol_documents']=v
 return out
if __name__=='__main__':
 amend=[]
 for f in (R/'evidence').glob('*.json'):
  a=json.loads(f.read_text());islands=a.pop('public_data_islands',None)
  if islands is None:continue
  old=hashlib.sha256(f.read_bytes()).hexdigest();pc=clinical_islands(islands)
  if pc:
   a['public_content']=pc
   chunks=[]
   for label,v in pc.items():chunks.append(label+'\n'+unescape(re.sub('<[^>]+>',' ',json.dumps(v,ensure_ascii=False))))
   a['clinical_text']='\n'.join(chunks)
  f.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');amend.append({'evidence_file':str(f.relative_to(ROOT)),'previous_file_sha256':old,'new_file_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'action':'retain public clinical fields only; discard unrelated script configuration; original source times unchanged'})
 (R/'public-inline-extraction.json').write_text(json.dumps(amend,indent=2))
 print('clinical extraction and unrelated-script removal',len(amend))
