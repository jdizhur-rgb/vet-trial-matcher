"""Apply eight primary-reviewed Nebraska locations; preserve all existing rows."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = 'ne-care-20261023'
DAY = '2026-10-23'
BASE = ROOT / 'research/audit-runs' / RUN
REF = f'research/audit-runs/{RUN}/result.json'

# Exact branch facts reviewed through Web; dates have day precision only.
specs = [
 ('ne-animal-clinic-suburban','Animal Clinic Suburban','14203 Pacific Street','Omaha','68154','402-334-1660','https://www.animalclinicsuburban.com/services/pets/chemotherapy','Chemotherapy', ['https://www.animalclinicsuburban.com/about-us/staff/veterinarians/dr-melody-kaliff'], ['Melody Kaliff, DVM'], 'At Animal Clinic Suburban we can safely administer a number of different chemotherapy agents.', 'Consultation required to select a chemotherapy protocol; contact the clinic for case assessment and treatment scheduling.'),
 ('ne-ehlers-animal-care','Ehlers Animal Care','6855 S 70th St','Lincoln','68516','402-420-7020','https://ehlersanimalcare.com/pet-chemotherapy-lincoln-ne/','Chemotherapy', ['https://ehlersanimalcare.com/veterinarian-lincoln-ne/'], ['Megan Ehlers, DVM','Emily Kerl, DVM','Chandler Labenz, DVM','Brooke Porter, DVM','Claire Martin (Sintek), DVM','Tessa Klein, DVM'], 'Chemotherapy treatments are typically administered during scheduled sessions and carefully monitored.', 'Chemotherapy is offered after evaluation and diagnostic testing. Call or request an appointment to confirm suitability and the treating veterinarian.'),
 ('ne-heartland-animal-center','Heartland Animal Center','220 West Fremont Drive','North Platte','69101','308-532-4880','https://www.heartlandanimal.com/veterinarycare','Surgery', ['https://www.heartlandanimal.com/contact'], ['Erin Rowland, veterinarian','Ron Green, veterinarian'], 'Tumor Removal', 'Tumor removal is listed among local procedures. Contact the clinic for assessment and surgical scheduling.'),
 ('beebout-veterinary-medical-center-holdrege','Beebout Veterinary Medical Center - Holdrege','1625 Burlington St.','Holdrege','68949','308-995-2419','https://beeboutvetmedcenter.com/holdrege/','Chemotherapy', ['https://beeboutvetmedcenter.com/services/internal-medicine/','https://beeboutvetmedcenter.com/our-team/?tab=holdrege','https://beeboutvetmedcenter.com/schedule-an-appointment/'], ['Melissa Drain, veterinarian (Holdrege)','Lacey Warning, DVM (Kearney and Holdrege)'], 'We offer chemotherapy as part of our commitment to providing advanced treatment options close to home', 'The Holdrege branch lists Internal Medicine, whose service page offers chemotherapy. Confirm local scheduling and the assigned veterinarian with Holdrege; Saturday has no doctor on-site.'),
 ('ne-twin-creek-animal-hospital','Twin Creek Animal Hospital','4006 Twin Creek Drive','Bellevue','68123','402-505-9033','https://twincreekah.com/services/pet-soft-tissue-surgery','Surgery', ['https://twincreekah.com/veterinarians'], ['Katie Olson, DVM','Monty Roberts, DVM','Nicole Tank, DVM','Amanda Thaler, DVM'], 'Mass/Tumor Removal', 'Mass/tumor removal is listed among local soft-tissue procedures. Call or request an appointment for assessment.'),
 ('ne-westside-family-pet-clinic','Westside Family Pet Clinic','104 N 37th Street','Norfolk','68701','402-844-4738','https://westsidefamilypetclinic.com/services/cancer-surgery-norfolk-ne','Surgery', ['https://westsidefamilypetclinic.com/','https://westsidefamilypetclinic.com/general-information-request','https://westsidefamilypetclinic.com/appointment-request'], ['Shane Pedersen, DVM','Stevie Morris, DVM','Miranda Bader, DVM'], 'All three of our veterinarians, Dr. Shane Pedersen, Dr. Stevie Morris, and Dr. Miranda Bader, perform cancer surgery', 'Local cancer surgery is offered after individual assessment. Call for a consultation; online appointment requests require confirmation.'),
 ('ne-westfield-small-animal-clinic','Westfield Small Animal Clinic','1821 West A Street','North Platte','69101','308-534-4480','https://westfieldvetnp.com/pet-surgery-north-platte-ne/','Surgery', ['https://westfieldvetnp.com/veterinarian-north-platte-ne/'], ['Kira L. Kautz, veterinarian','Katie Bunde, veterinarian'], 'Soft Tissue Surgery: Our team addresses tumors, wound repairs, and internal organ concerns.', 'The clinic lists tumor surgery among its soft-tissue procedures. Call for case assessment and appointment availability.'),
 ('ne-morgan-pet-clinic','Morgan Pet Clinic','16937 Audrey St','Omaha','68136','402-895-1001','https://www.morganpetclinic.com/tumor-removal','Surgery', ['https://www.morganpetclinic.com/staff','https://www.morganpetclinic.com/contact'], ['Charles Morgan, veterinarian','Kayla Clark, DVM','Jaclyn Sommer, DVM','Mackenzie Walkenhorst, DVM'], 'Mast cell tumors (cancerous tumors found on the skin and in internal organs)', 'Tumor removal, including mast cell tumors, is listed. Call for a surgical consultation and confirmation of case suitability.'),
]

def read(p): return json.loads((ROOT/p).read_text())
def write(p,x): (ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

files = {'data/oncology_centers.json':'centers','data/oncology_centers_supplemental.json':'centers','data/oncology_care_source_inventory.json':'sources'}
before = {p:copy.deepcopy(read(p)) for p in files}
supp = read('data/oncology_centers_supplemental.json')
inv = read('data/oncology_care_source_inventory.json')
existing = {r.get('source_id') for r in before['data/oncology_centers.json']['centers']}
evidence=[]
new=[]
for sid,name,street,city,postal,phone,url,modality,urls,clinicians,quote,note in specs:
 assert sid not in existing, sid
 row=dict(source_id=sid,name=name,street=street,city=city,region='NE',postal_code=postal,country='USA',phone=phone,website=url,verification_url=url,services=['Local oncology care',modality],supporting_urls=urls,last_verified=DAY,source='Current official branch service, team and contact review; Nebraska single-executor discovery.',availability_note=note,location_type='physical',service_scope='physical',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Official street address confirmed; exact building coordinates not obtained in this pass.',review_reference=REF,audit_run_id=RUN,care_clinicians=[dict(published_label=n,url=next((u for u in urls if any(t in u for t in ['staff','team','veterinarian','contact'])),urls[0])) for n in clinicians])
 supp['centers'].append(row); new.append(row)
 assert not any(r.get('id')==sid for r in inv['sources'])
 inv['sources'].append(dict(id=sid,name=name,source_type='center',master_url=url,supporting_urls=urls,required_cadence='weekly',last_checked=DAY,last_result='verified_core_care',working_url=url,content_sufficient=True,last_run_id=RUN,review_reference=REF,needs_recheck=False,service_scope='physical'))
 evidence.append(dict(source_id=sid,checked_on=DAY,time_precision='date_only',method='Web open/click',urls=[url]+urls,quote=quote,reviewed_facts=['branch contact and address','current veterinary roster','locally offered '+modality,'owner appointment route'],not_inferred=['board-certified oncologist','radiation','other branches']))
write('data/oncology_centers_supplemental.json',supp)
write('data/oncology_care_source_inventory.json',inv)
write(f'research/audit-runs/{RUN}/published-records.json',new)
write(f'research/audit-runs/{RUN}/evidence.json',evidence)
(ROOT.parent/'ne-baseline-before.json').write_text(json.dumps(before,ensure_ascii=False))
print('Prepared eight new physical locations; existing data unchanged.')
