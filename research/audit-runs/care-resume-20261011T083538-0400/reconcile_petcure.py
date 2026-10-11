import json,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;P=ROOT/'research/audit-runs/care-20261011T065613-0400'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cat=read(ROOT/'data/oncology_centers.json')['centers'];supp=read(ROOT/'data/oncology_centers_supplemental.json');rows=[]
aliases={'chicago-illinois':'PetCure Oncology Chicago','clifton-newjersey':'PetCure Oncology, Clifton, NJ','dallas-fort-worth':'Thrive Pet Healthcare Specialists (formerly Animal Emergency Hospital of Mansfield)','phoenix-arizona':'Arizona Veterinary Oncology','pittsburgh-pennsylvania':'BluePearl Pet Hospital – Pittsburgh North Hills','san-antonio':'PetCure Oncology San Antonio','san-jose-california':'PetCure Oncology San Jose'}
for x in read(P/'network-followup-fetches.json'):
 slug=x['url'].rstrip('/').split('/')[-1]
 if slug not in aliases:continue
 d=read(P/x['evidence_file']);c=next(c for c in cat if c['name']==aliases[slug]);t=d['text'];number=re.search(r'\d+',c['street']).group();assert number in t and c['city'].lower() in t.lower() and c['postal_code'] in t
 before=json.loads(json.dumps(c));added='Radiation oncology' not in c['services']
 if added:
  c['services'].append('Radiation oncology');c.update(verification_url=x['url'],last_verified='2026-10-11',source='Current official PetCure location-specific page confirms radiation oncology at this physical host hospital; the host is reconciled by street, city and postcode. Remote radiation planning by published board-qualified clinicians is distinguished from local treatment delivery.');c.pop('oncologist_count',None)
  if not c.get('phone'):c['phone']={'phoenix-arizona':'480-327-6690','pittsburgh-pennsylvania':'412-348-6524'}[slug]
  if slug=='clifton-newjersey':c['street']='1071 Paulison Avenue'
  existing=next((z for z in supp['centers'] if z['name']==c['name']),None)
  if existing:existing.update(c)
  else:supp['centers'].append(c)
 a=t.find('PetCure Oncology '+{'phoenix-arizona':'Phoenix','clifton-newjersey':'Clifton','pittsburgh-pennsylvania':'Pittsburgh','dallas-fort-worth':'Dallas','san-jose-california':'San Jose','san-antonio':'San Antonio','chicago-illinois':'Chicago'}[slug],1800)
 rows.append({'official_url':x['url'],'canonical_name':c['name'],'exact_branch_identity':{'street':c['street'],'city':c['city'],'postcode':c['postal_code']},'classification':'new_service' if added else 'duplicate','actual_attempted_at':d['attempted_at'],'evidence_file':str((P/x['evidence_file']).relative_to(ROOT)),'inherited_visit':True,'reviewed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'clinical_excerpt':t[a:a+1800],'before':before,'after':c,'radiation_current':True,'stereotactic_addition_claim':False,'care_team_note':'Published remote radiation planner is not represented as an on-site doctor; physical radiation service established in branch-specific text.'})
assert len(rows)==7
save(ROOT/'data/oncology_centers_supplemental.json',supp);save(RUN/'petcure-full-reconciliation.json',{'status':'complete','roster':7,'branches_reconciled':7,'new_physical_centers':0,'new_radiation_services':sum(x['classification']=='new_service' for x in rows),'locations':rows})
