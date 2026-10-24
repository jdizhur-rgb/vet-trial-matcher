"""Apply the dated primary-reviewed ND care package, without specialist inference."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = 'nd-care-20261024'
DAY = '2026-10-24'
BASE = ROOT / 'research/audit-runs' / RUN
REF = f'research/audit-runs/{RUN}/result.json'
FILES = {'data/oncology_centers.json':'centers', 'data/oncology_centers_supplemental.json':'centers', 'data/oncology_care_source_inventory.json':'sources'}
def read(p): return json.loads((ROOT/p).read_text())
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

# Explicit locally advertised treatment. No oncology board credentials inferred.
# source_id, name, address, city, ZIP, phone, service URL, confirmed modality,
# supporting URLs, published veterinary roster, short evidence quotation.
specs = [
 ('nd-petcetera-animal-clinic','Petcetera Animal Clinic','1150 40th Ave S','Grand Forks','58201','701-775-0549','https://www.petcgfk.com/services/','Surgery',['https://www.petcgfk.com/contact/','https://www.petcgfk.com/who-we-are/ourteam/','https://www.petcgfk.com/contact/request-an-appointment/'],['Stacy Lord, DVM','Ashley Pearson, DVM','Kerry Haage, DVM'],'Tumor removal'),
 ('nd-turtle-mountain-veterinary-service','Turtle Mountain Veterinary Service','1040 Highway 5 NE','Bottineau','58318','701-228-3075','https://www.turtlemountainvet.com/small-animal-services.pml',None,['https://www.turtlemountainvet.com/our-doctors.pml','https://www.turtlemountainvet.com/contact-us.pml'],['Jill Franks, veterinarian'],'We offer treatment for conditions ranging from allergies to cancer care.'),
 ('nd-casselton-veterinary-service-casselton','Casselton Veterinary Service - Casselton','910 Governor’s Dr','Casselton','58012','701-347-5496','https://cassvetservice.com/services/internal-medicine/',None,['https://cassvetservice.com/our-locations-hours/'],['Dr. Bartholomay, veterinarian (published service-page caption; assigned cancer clinician to confirm)'],'We cover all areas of internal medicine including'),
 ('nd-casselton-veterinary-service-fargo','Casselton Veterinary Service - Fargo','5012 47th St S','Fargo','58104','701-895-2135','https://cassvetservice.com/service-category/small-animal-services-fargo/',None,['https://cassvetservice.com/services/internal-medicine/','https://cassvetservice.com/our-locations-hours/'],[],'Oncology'),
 ('nd-country-acres-veterinary-clinic','Country Acres Veterinary Clinic','8279 37th St SE','Jamestown','58401','701-252-7133','https://www.countryacresveterinaryclinic.com/surgery','Surgery',['https://www.countryacresveterinaryclinic.com/contact-us','https://www.countryacresveterinaryclinic.com/dr-looysen-staff'],['Barbara Looysen, DVM'],'growth and mass removal'),
 ('nd-southwood-veterinary-clinic-jamestown','Southwood Veterinary Clinic - Jamestown','833 18th St SW','Jamestown','58401','701-252-3430','https://www.southwoodvetclinic.com/surgery','Surgery',['https://www.southwoodvetclinic.com/about-us','https://www.southwoodvetclinic.com/contact-us'],['Greg Carlson, veterinarian','Debra Trnovec, veterinarian','Melissa Schlecht, veterinarian'],'Eye, ear, and mass removal surgeries'),
 ('nd-grand-valley-animal-hospital','Grand Valley Animal Hospital','2825 36th Ave S, Suite B','Grand Forks','58201','701-757-3500','https://grandvalleyvet.com/surgery/','Surgery',['https://grandvalleyvet.com/our-team/'],['Darin Meulebroeck, DVM','Jessica Olson, DVM','Emily Dorsey, DVM'],'lump and foreign body removal'),
 ('nd-steele-veterinary-clinic','Steele Veterinary Clinic','2515 HWY 10','Steele','58482','701-475-2300','https://steelevetclinic.com/services/canine/','Surgery',['https://steelevetclinic.com/our-team/'],['Troy Dutton, DVM','Joseph Hochhalter, DVM','Nickolas Hart, veterinarian','Marissa Soderberg, veterinarian','Breanna Nelson, veterinarian'],'Mass/Tumor Removal'),
 ('nd-dakota-paws-veterinary-hospital','Dakota Paws Veterinary Hospital','166 38th St SE','Watford City','58854','701-779-0200','https://www.dakotapawsvet.com/surgery/','Surgery',['https://www.dakotapawsvet.com/team/','https://www.dakotapawsvet.com/contact/'],['Samantha Zuck-Roscoe, veterinarian','Mark Foster, veterinarian'],'Surgeries in our facility range in complexity from minor mass removals to emergency abdominal procedures.'),
 ('nd-knife-river-veterinary-clinic','Knife River Veterinary Clinic','802 16th St NE','Beulah','58523','701-873-5525','https://kniferiverveterinaryclinic.com/services','Surgery',['https://kniferiverveterinaryclinic.com/','https://kniferiverveterinaryclinic.com/staff'],['Matthew O’Neil, DVM','Carolyn R. Woodruff, DVM','Angela Bell, DVM'],'tumor removal'),
 ('nd-lisbon-veterinary-service-lisbon','Lisbon Veterinary Service - Lisbon','702 5th Ave W','Lisbon','58054','701-683-4686','https://www.lisbonvet.com/services',None,['https://www.lisbonvet.com/team','https://www.lisbonvet.com/locations'],['Andrea Sand, DVM','Kevin Smykowski, DVM','Ellen Dauphinais, DVM','Allison Wieler, DVM'],'Oncology'),
 ('nd-dakota-veterinary-hospital-wahpeton','Dakota Veterinary Hospital','18045 79 1/2 St SE','Wahpeton','58075','701-642-9277','https://www.dakotaveterinaryhospital.com/services.html','Surgery',['https://www.dakotaveterinaryhospital.com/about-us.html','https://www.dakotaveterinaryhospital.com/contact-us.html'],['Sara Bakken, veterinarian','Carmen Odegaard, veterinarian','Alyssa Breuer, veterinarian','Madeline DeLeon, veterinarian'],'skin tumor removals'),
]

before = {p:copy.deepcopy(read(p)) for p in FILES}
assert not (ROOT.parent/'nd-baseline-before.json').exists(), 'Do not replay against applied data'
(ROOT.parent/'nd-baseline-before.json').write_text(json.dumps(before,ensure_ascii=False))
supp = read('data/oncology_centers_supplemental.json')
inv = read('data/oncology_care_source_inventory.json')
new=[]; evidence=[]
for sid,name,street,city,postal,phone,url,modality,urls,doctors,quote in specs:
 assert not any(r.get('source_id')==sid for r in before['data/oncology_centers.json']['centers'])
 services=['Local oncology care'] + ([modality] if modality else [])
 note = ('The clinic lists tumor or mass removal among its local surgical procedures. Confirm case suitability, surgical scope, the treating veterinarian and appointment availability.' if modality else 'The clinic advertises local cancer care. Specific treatment modalities and the assigned veterinarian are not confirmed; call to discuss the case and appointment availability.')
 if city=='Bottineau': note += ' Confirm whether new clients are currently being accepted.'
 if 'casselton' in sid: note='Oncology is included in this branch’s internal medicine offering. Chemotherapy and tumor surgery are not confirmed. Ask about the treating veterinarian, local treatment scope, referral needs and appointment availability.'
 if 'lisbon' in sid: note+=' The Lisbon office offers full medical and surgical care; cancer services have not been allocated to the Oakes or LaMoure satellite offices.'
 row=dict(source_id=sid,name=name,street=street,city=city,region='ND',postal_code=postal,country='USA',phone=phone,website=url,verification_url=url,services=services,supporting_urls=urls,last_verified=DAY,source='Current official local service and contact review; North Dakota single-executor discovery.',availability_note=note,location_type='physical',service_scope='physical',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Official street address confirmed; exact building coordinates not obtained in this pass.',review_reference=REF,audit_run_id=RUN)
 if doctors: row['care_clinicians']=[dict(published_label=n,url=next((u for u in urls if any(x in u for x in ['team','staff','doctor','about'])),url)) for n in doctors]
 if 'casselton' in sid: row['clinician_review']='Current branch oncology service is published; current full roster pages were inaccessible. No named oncologist or branch-specific chemotherapy clinician is claimed.'
 supp['centers'].append(row);new.append(row)
 inv['sources'].append(dict(id=sid,name=name,source_type='center',master_url=url,supporting_urls=urls,required_cadence='weekly',last_checked=DAY,last_result='verified_core_care',working_url=url,content_sufficient=True,last_run_id=RUN,review_reference=REF,needs_recheck=False,service_scope='physical'))
 evidence.append(dict(source_id=sid,date=DAY,time_precision='date_only',primary_urls=[url]+urls,quote=quote,confirmed_services=services,scope='physical',limitations=note))

sid='nd-oakes-edgeley-ellendale-veterinary-service-network'
url='https://www.oakesvet.com/surgery'
urls=['https://www.oakesvet.com/about-us','https://www.oakesvet.com/contact']
row=dict(source_id=sid,name='Oakes, Edgeley & Ellendale Veterinary Service — network contact',street='',city='',postal_code='',region='ND',country='USA',phone='',email='oeevs@outlook.com',website=url,verification_url=url,booking_url='https://www.oakesvet.com/contact',branch_finder_url='https://www.oakesvet.com/contact',network_search_terms=['Oakes','Edgeley','Ellendale'],services=['Surgery'],location_type='network',service_scope='network',branch_availability='confirm_before_booking',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Network contact only; no treatment address or distance point.',last_verified=DAY,supporting_urls=urls,availability_note='The network lists mass removal for dogs and cats. Email the shared network contact to confirm the treatment branch, veterinarian and appointment availability before travelling.',clinician_review='Carrie Swier-Galbreath and Ben Galbreath are published network veterinarians; the treating clinician and branch must be confirmed.',source='Official network surgery offering and common email; no branch allocation inferred.',audit_run_id=RUN,review_reference=REF)
supp['centers'].append(row);new.append(row)
inv['sources'].append(dict(id=sid,name=row['name'],source_type='center',master_url=url,supporting_urls=urls,required_cadence='weekly',last_checked=DAY,last_result='verified_network_care',working_url=url,content_sufficient=True,last_run_id=RUN,review_reference=REF,needs_recheck=False,service_scope='network'))
evidence.append(dict(source_id=sid,date=DAY,time_precision='date_only',primary_urls=[url]+urls,quote='Mass Removal',confirmed_services=['Surgery'],scope='network',limitations=row['availability_note']))

# Clinic-authored 2026 job advertisement hosted by NDVTA explicitly names chemotherapy;
# current owned referral page independently continues to advertise oncology treatment.
state=next(r for r in supp['centers'] if r.get('source_id')=='state-ave-veterinary-clinic')
state.update(services=['Local oncology care','Chemotherapy'],last_verified=DAY,review_reference=REF,audit_run_id=RUN,availability_note='The clinic offers oncology consultations and treatment; its February 12, 2026 recruitment advertisement also lists chemotherapy. Confirm the available protocol, treating veterinarian and appointment before travelling. A veterinary referral route is published.',source='Current official referral and team pages plus the clinic-authored February 12, 2026 advertisement hosted by NDVTA.')
ad='https://www.ndvta.org/Job-Opportunities/'
state['supporting_urls']=list(dict.fromkeys(state['supporting_urls']+[ad]))
evidence.append(dict(source_id=state['source_id'],date=DAY,time_precision='date_only',primary_urls=[state['verification_url'],'https://www.stateavevet.com/meet-the-team/',ad],quotes={'referral':'Oncology consultations and treatments','clinic_authored_ad':'Endoscopy, laparoscopy, chemotherapy, and rehab'},ad_publication_date='2026-02-12',confirmed_new_service='Chemotherapy',limitation='No board-certified oncologist or specific chemotherapy protocol claimed.'))
red=next(r for r in supp['centers'] if r.get('source_id')=='red-river-animal-emergency-hospital-referral-center')
red.update(last_verified=DAY,review_reference=REF)
evidence.append(dict(source_id=red['source_id'],date=DAY,time_precision='date_only',primary_urls=[red['verification_url']],quote='not accepting new oncology patients',decision='Preserve false intake status and existing service scope; notice controls over generic offering text.'))
for r in inv['sources']:
 if r.get('id') in [state['source_id'],red['source_id'],'rugby-veterinary-service']:
  r.update(last_checked=DAY,last_result='verified_core_care' if r['id']!=red['source_id'] else 'verified_intake_restriction',last_run_id=RUN,review_reference=REF,content_sufficient=True)
  # Date-only Web review is not the older exact request timestamp.
  r.pop('last_checked_at',None)
  if r['id']==state['source_id']: r['supporting_urls']=state['supporting_urls']
  if r['id']=='rugby-veterinary-service': r['last_review_note']='Current service page reread; local cancer treatment retained. Chemotherapy remains unconfirmed. No fresh full-team/public verification date claimed.'
write('data/oncology_centers_supplemental.json',supp)
write('data/oncology_care_source_inventory.json',inv)
write(f'research/audit-runs/{RUN}/published-records.json',new)
write(f'research/audit-runs/{RUN}/evidence.json',evidence)
print('Prepared 12 new physical locations, one network contact, and one new local chemotherapy tag.')
