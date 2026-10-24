"""Apply four reviewed local surgery sites and one existing-site service correction."""
import copy
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
RUN=BASE.name
DAY='2026-10-24'
REF=f'research/audit-runs/{RUN}/evidence.json'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
before={p:read(p) for p in ['data/oncology_centers.json','data/oncology_centers_supplemental.json','data/oncology_care_source_inventory.json']}
specs=[
 ('nd-enderlin-veterinary-clinic','Enderlin Veterinary Clinic','13484 Highway 46','Enderlin','58027','701-437-3201','https://www.enderlinvetclinic.com/surgery-services',['https://www.enderlinvetclinic.com/doctors-staff','https://www.enderlinvetclinic.com/contact'],['Sara Fridrych, MPH, DVM'],'Mass/tumor removals','The clinic lists mass/tumor removal and limb amputation for cancer. Call to confirm surgical suitability, the treating veterinarian and appointment availability.'),
 ('nd-valley-veterinary-hospital-fargo','Valley Veterinary Hospital','3210 Main Avenue','Fargo','58103','701-232-3391','https://valleyveterinary.net/services/surgery/',['https://valleyveterinary.net/about/','https://valleyveterinary.net/contact/'],['Derine Winning, DVM','Vanessa Aschnewitz, DVM'],'Mass removals','The hospital offers mass removal for treatment and diagnosis. Confirm the surgical scope, case suitability and appointment availability; chemotherapy is not confirmed.'),
 ('nd-two-rivers-veterinary-hospital','Two Rivers Veterinary Hospital','2630 Sheyenne Street','West Fargo','58078','701-356-5588','https://www.tworiversveterinaryhospital.com/services/',['https://www.tworiversveterinaryhospital.com/veterinarians','https://www.tworiversveterinaryhospital.com/contact'],['Tracie Hoggarth, DVM','Teri-Lee James, DVM, MPH','Abby Sullivan, DVM, CCRT','Melissa Caid, DVM','Jason Erickson, DVM','Kristine Haroldson, DVM'],'From routine mass removals and organ biopsies','The hospital lists local mass removal among its soft tissue procedures. Confirm the treating veterinarian, case suitability and appointment availability. Stem-cell storage and rehabilitation are separate services, not cancer-treatment claims.'),
 ('nd-new-salem-veterinary-clinic','New Salem Veterinary Clinic','1109 N 8th St','New Salem','58563','701-843-8020','https://www.newsalemveterinaryclinic.com/copy-of-services',['https://www.newsalemveterinaryclinic.com/about-us','https://www.newsalemveterinaryclinic.com/contact-us'],['Chad Wild, DVM','HP O’Doherty, DVM'],'lump removal','The clinic routinely performs lump removal for dogs and cats. Call to discuss whether its surgical scope fits the case and to confirm the treating veterinarian and availability.'),
]
supp=read('data/oncology_centers_supplemental.json');inv=read('data/oncology_care_source_inventory.json');new=[];ev=[]
for sid,name,street,city,postal,phone,url,urls,doctors,quote,note in specs:
 assert not any(r.get('source_id')==sid for r in before['data/oncology_centers.json']['centers']),sid
 row=dict(source_id=sid,name=name,street=street,city=city,postal_code=postal,region='ND',country='USA',phone=phone,website=url,verification_url=url,supporting_urls=urls,services=['Local oncology care','Surgery'],location_type='physical',service_scope='physical',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Official street address confirmed; exact building coordinates not obtained in this pass.',last_verified=DAY,availability_note=note,source='Current official local surgical-service, veterinary-team and contact review; North Dakota followup.',audit_run_id=RUN,review_reference=REF,care_clinicians=[dict(published_label=n,url=urls[0]) for n in doctors])
 supp['centers'].append(row);new.append(row)
 inv['sources'].append(dict(id=sid,name=name,source_type='center',master_url=url,supporting_urls=urls,required_cadence='weekly',last_checked=DAY,last_result='verified_core_care',content_sufficient=True,working_url=url,last_run_id=RUN,review_reference=REF,service_scope='physical',needs_recheck=False))
 ev.append(dict(source_id=sid,date=DAY,time_precision='date_only',primary_urls=[url]+urls,quote=quote,confirmed_services=['Surgery'],limitations=note))
red=next(r for r in supp['centers'] if r.get('source_id')=='red-river-animal-emergency-hospital-referral-center')
url='https://rraeh.com/services/rraeh-surgery-service/'
red['services'].append('Surgery')
red.update(availability_note='Not accepting new oncology patients. The separate Surgery Service advertises oncologic procedures by veterinary referral; call to confirm whether it can accept the surgical case before travelling.',review_reference=REF)
red['supporting_urls']=list(dict.fromkeys(red.get('supporting_urls',[])+[red['verification_url'],url]))
# Do not relax the existing false intake flag or infer a board credential.
assert red['accepting_new_patients'] is False
r=next(r for r in inv['sources'] if r.get('id')==red['source_id'])
r.update(supporting_urls=list(dict.fromkeys(r['supporting_urls']+[url])),last_run_id=RUN,review_reference=REF,last_review_note='Separate current Surgery Service explicitly lists oncologic surgery and referrals Monday–Thursday with David Silliman, described as residency-trained. Oncology new-patient restriction retained. Surgical case acceptance must be confirmed.',last_checked=DAY)
ev.append(dict(source_id=red['source_id'],date=DAY,time_precision='date_only',primary_urls=[url,red['verification_url']],quote='Tumor and mass removals',new_confirmed_service='Surgery',published_clinician='David Silliman — residency trained in surgery',limitation='No board-certified credential or reopened oncology intake inferred; surgical case acceptance to confirm.'))
write('data/oncology_centers_supplemental.json',supp);write('data/oncology_care_source_inventory.json',inv)
write(f'research/audit-runs/{RUN}/published-records.json',new);write(f'research/audit-runs/{RUN}/evidence.json',ev)
(ROOT.parent/'nd-finish-before.json').write_text(json.dumps(before,ensure_ascii=False))
print('Prepared four new surgery locations and separate Red River surgery scope; restricted oncology intake retained.')
