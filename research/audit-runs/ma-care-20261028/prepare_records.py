"""Reviewed MA clinic facts, separated from catalog integration."""
import copy,hashlib,json,pathlib,re,sys,urllib.parse
from retrieve import ROOT,OUT,CACHE
DATE='2026-10-28'
RUN='ma-care-20261028'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def digest(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
pages=[json.loads(f.read_text()) for f in CACHE.glob('*.json') if f.name!='integration-baseline.json']
pages=[r for r in pages if 'url' in r]
byurl={r['url']:r for r in pages}
rows=[]
def add(slug,name,street,city,zip,phone,url,doc,team,services=None,note=None):
 assert byurl[url].get('status')==200,url
 assert byurl[team].get('status')==200,team
 rows.append(dict(source_id='ma-'+slug,name=name,street=street,city=city,postal_code=zip,region='MA',country='USA',phone=phone,website=url,verification_url=url,supporting_urls=list(dict.fromkeys([team])),services=services or ['Surgery'],care_clinicians=[{'published_label':doc,'url':team}],location_type='physical',last_verified=DATE,availability_note=note or 'The clinic lists local mass or tumor-removal surgery. Call to confirm suitability for the tumor, the treating veterinarian and appointment availability.',source='Current clinic-owned treatment, veterinary team and contact pages reviewed in the Massachusetts state pass.',audit_run_id=RUN,review_reference='research/audit-runs/'+RUN+'/evidence.json'))
# Each VCA branch below publishes its OWN general-surgery procedure list and
# current named veterinarian roster. The service is local surgery, not a claim
# that the practice has an oncology specialist or a particular cancer protocol.
vca=[]
urls=read('research/audit-runs/'+RUN+'/vca-ma-sitemap.json')
slugs=sorted({u.split('/')[3] for u in urls if u.endswith('/services/primary-care/general-surgery')})
for slug in slugs:
 root='https://vcahospitals.com/'+slug;url=root+'/services/primary-care/general-surgery'
 service=byurl[url];team=byurl[root+'/team'];contact=byurl[root+'/contact-us'];t=contact.get('text','')
 assert 'lump removal' in service.get('text','').lower(),slug
 m=re.search(r'Hours & Info\n(VCA [^\n]+)\n([^\n]+)\n([^\n]*, MA \d{5})',t)
 if m:name,street,local=m.groups()
 else:
  m=re.search(r'Location\n([^\n]+)\n([^\n]*, MA \d{5})',t);assert m,slug
  street,local=m.groups();name=service['text'].split('\n')[0].split(' | ')[1].removesuffix(' VCA Animal Hospitals')
 city,zip=re.fullmatch(r'(.*), MA (\d{5})',local).groups()
 phone=re.search(r'Phone:\s*([^\n]+)',t).group(1).replace('–','-')
 assert len(re.sub(r'\D','',phone))==10,(slug,phone)
 docs=[a for a in team.get('links',[]) if '/team/' in a['url'] and re.search(r'Veterinarian|Medical Director',a['text'])]
 assert docs,slug
 add('vca-'+slug,name,street,city,zip,phone,url,docs[0]['text'],root+'/team',note='The branch-specific general-surgery page lists lump removal and biopsy. Confirm tumor suitability, the assigned veterinarian, surgical scope and appointment by calling this hospital. This is local surgical care; no oncology board credential or chemotherapy service is inferred.'+(' This is a cat practice.' if slug=='city-cats' else ''))
 rows[-1]['supporting_urls'].append(root+'/contact-us')
 if slug=='city-cats':rows[-1]['species']=['Cat']
 vca.append(slug)
# Independently reviewed VetCor clinic pages: contact and current veterinarian
# names come from each clinic, not a network-wide surgical offering.
vetcor=[
('ashland','Ashland Animal Hospital','10 Fountain St','Ashland','01721','508-881-2400','ashlandanimalhospital.com','Amanda Bergeron, DVM','/veterinarians'),
('burlington','Burlington Veterinary Hospital','64 Middlesex Turnpike','Burlington','01803','781-270-0044','burlingtonvet.com','Claudia Kessen-Banks, DVM','/veterinarians'),
('countryside-chelmsford','Countryside Veterinary Hospital','289 Littleton Road','Chelmsford','01824','978-256-9555','countrysideveterinaryhospital.com','F. Alexa Warburton, DVM','/veterinarians'),
('falmouth','Falmouth Animal Hospital','1184 Sandwich Road','East Falmouth','02536','508-563-7147','falmouthanimalhospital.com','Lilan Hauser, DVM','/veterinarian-staff'),
('valley-hadley','Valley Veterinary Hospital','320 Russell Street','Hadley','01035','413-584-1223','valleyvethospital.com','Ya Rote, DVM','/veterinarians'),
('lexington-bedford','Lexington-Bedford Veterinary Hospital','476 Bedford Street','Lexington','02420','781-862-3670','lexingtonbedfordvet.com','Thea Doidge, DVM','/veterinarians'),
('linwood','Linwood Animal Hospital','1500 Gorham Street','Lowell','01852','978-453-1784','linwoodah.com','Victoria Vasilakis, DVM','/veterinarians'),
('new-england-salem','New England Veterinary Clinic & Pet Resort','204 Highland Avenue','Salem','01970','978-744-8325','newenglandveterinaryclinic.com','Ashley Gallagher, DVM','/veterinarians'),
('norwell','Norwell Veterinary Hospital','295R Washington Street','Norwell','02061','781-659-4911','norwellveterinaryhospital.com','Melissa Kenney, DVM','/veterinarians'),
('pittsfield','Pittsfield Veterinary Hospital','1634 West Housatonic St.','Pittsfield','01201','413-499-1580','pittsfieldvet.com','Madeleine Hoog-Crellin, DVM','/veterinarians'),
('sturbridge-general','Sturbridge Veterinary Hospital','6 Cedar Street','Sturbridge','01566','508-347-7374','sturbridgeveterinaryhospital.com','Thomas Hamilton, DVM','/veterinarians/Thomas-Hamilton'),
('taunton-cat','Taunton Cat Hospital','56 Winthrop Street','Taunton','02780','508-824-2287','tauntoncathospital.com','Abby Fitzgerald, DVM','/cat-veterinarians')]
for slug,name,street,city,zip,phone,host,doc,team in vetcor:
 add(slug,name,street,city,zip,phone,'https://'+host+'/services/pet-soft-tissue-surgery',doc,'https://'+host+team)
 if slug=='taunton-cat':rows[-1]['species']=['Cat'];rows[-1]['availability_note']+=' Cat patients only.'
add('agawam','Agawam Animal Hospital','65 Mill St','Agawam','01001','413-786-4440','https://agawamanimalhospital.com/conditions-treated','John E. Guntly, DVM — medical director','https://agawamanimalhospital.com/contact')
add('acoaxet','Acoaxet Veterinary Clinic','965 Sanford Rd','Westport','02790','508-636-8382','https://www.acoaxetvet.com/services/oncology','Maria S. Mutty — managing DVM','https://www.acoaxetvet.com/staff',['Local oncology care','Chemotherapy'],'The clinic oncology page explicitly describes chemotherapy administered at the practice. Confirm the regimen, treating veterinarian and appointment. General discussion of radiation treatment does not establish local radiation delivery or an oncology board-certified clinician.')
add('borash','Borash Veterinary Clinic','79 Prospect St','Peabody','01960','978-531-8713','https://www.borashvet.com/peabody-ma/veterinary-pet-surgery/','Rick Southgate — veterinarian','https://www.borashvet.com/meet-our-doctors/',note='The clinic lists local mass/tumor surgery. The MVMA chemotherapy entry is retained as a lead, not a confirmed local chemotherapy service; call about the specific cancer procedure and assigned veterinarian.')
add('north-shore-lynn','North Shore Animal Hospital','1 Neptune Blvd','Lynn','01902','781-596-0510','https://www.nshoreanimalhospital.com/vet-services/','David A. Dunn, DVM','https://www.nshoreanimalhospital.com/meet-our-team/')
add('sunderland','Sunderland Animal Hospital','52 Amherst Road','Sunderland','01375','413-665-9821','https://sunderlandvet.com/dog-services.pml','Steven M. Ellis, DVM','https://sunderlandvet.com/our-veterinarians.pml',['Local oncology care'],'The clinic explicitly lists cancer treatment for dogs and cats. Specific chemotherapy or cancer-surgery delivery is not established by the reviewed service pages; confirm the treatment plan, veterinarian and appointment.')
rows[-1]['supporting_urls']+=['https://sunderlandvet.com/cat-services.pml','https://sunderlandvet.com/contact-us.pml']
add('countryside-wrentham','Countryside Veterinary Clinic','92 Ellery Street','Wrentham','02093','508-384-8700','https://www.csvetclinicma.com/','Bart Massucco, DVM; Kelly Cygan; John Sykes — clinic veterinarians','https://www.csvetclinicma.com/',['Local oncology care','Chemotherapy','Surgery'],'The clinic explicitly lists in-house chemotherapy and mass-removal surgery and says it is taking new clients. Confirm the regimen, tumor suitability, treating veterinarian and appointment; no oncology board credential is established.')
add('lilvc','Love Is Life Veterinary Clinic','447 E Central St','Franklin','02038','508-876-3211','https://lilvc.org/','April L. Paul, DVM, DACVECC — founder and surgeon','https://lilvc.org/team/team.html',note='Nonprofit surgical clinic listing mass/lump removal, open to all owners with no financial eligibility requirement. Required diagnostics are performed by the referring veterinarian before surgery; the clinic does not perform diagnostic tests or offer overnight hospitalization. Confirm referral, records, case acceptance and appointment. DACVECC is an emergency/critical-care credential, not an oncology or surgery board certification.')
add('back-bay','Back Bay Veterinary Clinic','288 Newbury Street','Boston','02115','617-247-2273','https://www.backbayvet.com/services/surgery-services','Katherine Wheeler — senior veterinarian and medical director','https://www.backbayvet.com/staff')
add('boston-west','Boston West Veterinary Emergency & Specialty','5 Strathmore Rd','Natick','01760','508-319-2117','https://www.bostonwestvet.com/services/surgery','Alane Kosanovich Cahalane, DVM, DACVS-SA — veterinary surgeon','https://www.bostonwestvet.com/services/surgery',note='The hospital explicitly offers tumor-removal and cancer-related surgery. Elective procedures usually begin with a primary-veterinarian referral and surgical consultation; confirm the case and appointment.')
add('boston-veterinary-specialists','Boston Veterinary Specialists','326 Bridge Street','Dedham','02026','781-326-2800','https://bostonvetspecialists.com/pet-soft-tissue-abdominal-surgery-dedham-ma/','Catherine Briere, DVM, MS, DACVS — senior surgeon','https://bostonvetspecialists.com/veterinarian-dedham-ma/')
add('healthy-paws','Healthy Paws Veterinary Center','6 Old Flanders Rd','Westborough','01581','508-475-5051','https://www.healthypawsvetcenter.com/surgery','Elizabeth Russell, DVM','https://www.healthypawsvetcenter.com/our-team')
add('norfolk-county','Norfolk County Veterinary Service','1428 Main Street, Suite 7','Walpole','02081','508-668-5088','https://www.norfolkcountyvet.com/your-pets-surgery.html','Christina M. Poor, BVetMed, MRCVS','https://www.norfolkcountyvet.com/veterinarians.html')
add('compassionate-care-groton','Compassionate Care Veterinary Services','497 Main Street, Suite F','Groton','01450','978-775-1157','https://www.ccvsgroton.com/surgery','Lynne O’Neil — veterinarian and owner','https://www.ccvsgroton.com/meet-the-team')
add('rowley','Rowley Animal Hospital','46 Leslie Rd','Rowley','01969','978-948-2118','https://www.rowleyanimalhospital.com/surgery.pml','Danielle DiBoot, DVM — veterinarian','https://www.rowleyanimalhospital.com/our-doctor.pml')
add('norton','Norton Animal Hospital','147 West Main Street','Norton','02766','508-285-9822','https://nortonanimalhospital.com/services/vet-surgery','Shawna Li, DVM','https://nortonanimalhospital.com/veterinarians')
add('neamc-primary','New England Animal Medical Center Primary Care','20 Pleasant St','West Bridgewater','02379','508-894-7922','https://www.neamcpc.com/services/general-surgery','Caroline Bowlin, DVM; Jamie Fournier, DVM — practice veterinarians','https://www.neamcpc.com/staff',note='The primary-care hospital explicitly lists local tumor-removal surgery. Its current address is 20 Pleasant Street. This is separate from Westbridge Veterinary Referral Hospital at 595 West Center Street; confirm the procedure, veterinarian and appointment.')
add('greylock','Greylock Animal Hospital','1028 State Road','North Adams','01247','413-663-5365','https://greylockanimalhospital.com/services/pet-soft-tissue-surgery','Joanne Ziemba, DVM','https://greylockanimalhospital.com/veterinarians')
add('shepherd','Shepherd Veterinary Clinic','17 Codman Hill Road','Boxborough','01719','978-263-0995','https://www.shepherdvet.com/meet-the-team','Timothy Foster, DVM; Irene Papamitrou — veterinarians','https://www.shepherdvet.com/meet-the-team',note='The current team page describes local growth-removal surgery. Historical MVMA chemotherapy tags are not treated as proof of current chemotherapy delivery; confirm procedure, veterinarian and appointment with the clinic.')
add('cape-cod-buzzards','Cape Cod Veterinary Specialists — Buzzards Bay','11 Bourne Bridge Approach','Buzzards Bay','02532','508-759-5125','https://capecodvetspecialists.com/pet-surgery-buzzards-bay-ma/','Daniel J. Adams, VMD, DACVS-SA; Daniel Beaver, DVM, DACVS; Julie Bennett, DVM, DACVS — practice surgical team','https://capecodvetspecialists.com/veterinarian-buzzards-bay-ma/',note='The Buzzards Bay surgical service explicitly lists oncologic surgery. Confirm the assigned surgeon and case acceptance. The separate South Dennis location is not assigned this service solely from the shared footer.')
add('bulger','Bulger Veterinary Hospital','141 Winthrop Ave','Lawrence','01843','978-682-9905','https://www.bulgervet.com/services/surgery','Brianna Barnet, BVSc, DACVS; Lauren L. Blaeser, DVM, DACVS — surgeons','https://www.bulgervet.com/staff')
add('bluepearl-charlestown','BluePearl Pet Hospital — Charlestown','56 Roland St','Boston','02129','617-284-9777','https://bluepearlvet.com/hospital/charlestown-ma/specialties-services/surgery/','Matthew Cleveland, DVM, DACVS (SA) — surgeon','https://bluepearlvet.com/hospital/charlestown-ma/our-vets/')
add('angell-west','MSPCA-Angell West','293 Second Avenue','Waltham','02451','781-902-8400','https://www.mspca.org/veterinarycare/hospital-locations/waltham/surgery-in-waltham/','Hadley Gleason, VMD, MS, DACVS-SA; Jennifer Peterson-Levitt, DVM, MS, DACVS-SA; Sophia Topulos, DVM, DACVS-SA — branch surgical team','https://www.mspca.org/surgery-team-waltham/',note='Current Waltham surgery page explicitly offers cancer surgery and tumor resection/reconstruction. The oncology and radiation consultations are in-network, not proof of local chemotherapy or radiation equipment. Confirm surgeon assignment, referral, case acceptance and appointment.')
rows[-1]['email']='angellwestsurgery@angell.org'
rows[-1]['supporting_urls'].append('https://www.mspca.org/veterinarycare/hospital-locations/waltham/mspca-angell-west-waltham/')
# South Coastal has two locations, and the shared oncology service does not
# allocate chemotherapy to a branch. Preserve ONE usable network email route.
add('south-coastal-network','South Coastal Animal Health — oncology contact','','','','','https://www.southcoastalah.com/services','Grace Strake, DVM — practice veterinarian offering chemotherapy','https://www.southcoastalah.com/our-team',['Local oncology care','Chemotherapy'],'The practice lists chemotherapy and has locations in Weymouth and Rockland. Email the practice to confirm the treatment branch, assigned veterinarian, regimen and appointment; this listing is one network contact, not two verified chemotherapy locations.')
rows[-1].update(location_type='network',service_scope='network',email='Info@SouthCoastalAH.com',service_area='Massachusetts; Weymouth and Rockland branch allocation to confirm',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Network contact; no fixed treatment location or distance point.')
rows[-1]['supporting_urls'].append('https://www.southcoastalah.com/contact')
rows[-1].update(branch_availability='confirm_before_booking',branch_finder_url='https://www.southcoastalah.com/contact')
# One institutional program route, including its actual branch referral forms;
# individual operating clinicians are assigned during intake, not inferred.
add('mspca-community-program','MSPCA-Angell community clinics — urgent surgical care','','','','','https://www.mspca.org/veterinarycare/low-cost-clinics-all-locations/low-cost-clinics/','MSPCA-Angell community-clinic veterinary team; assigned surgeon to confirm during intake','https://www.mspca.org/programs-resources/mspca-angell-clinic-at-nevins-farm/',note='Subsidized urgent outpatient surgery includes mass removal when quality of life is affected, such as an ulcerated mammary mass. Financial qualification and individual clinical approval are required. The official page provides separate application/referral routes for Cape Cod (Centerville), Nevins Farm (Methuen) and the Boston Larson Kelly clinic (veterinarian referral only). No overnight or specialty cancer care. Use the program page to confirm the branch, surgeon, cost and appointment.')
rows[-1].update(location_type='network',service_scope='network',service_area='Massachusetts; Boston, Centerville and Methuen community-clinic program',latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Institutional program contact with separate branch applications; no single treatment-office distance point.')
rows[-1].update(branch_availability='confirm_before_booking',branch_finder_url=rows[-1]['website'],booking_url=rows[-1]['website'])
zips=read('data/us_zip_centroids.json')['zips']
for r in rows:
 if r['location_type']=='physical':
  z=zips.get(r['postal_code'])
  if z:r.update(latitude=z['latitude'],longitude=z['longitude'],coordinate_source='Public ZIP centroid from us_zip_centroids.json; not building coordinates.')
  else:r.update(latitude=None,longitude=None,coordinates_unknown=True,coordinate_source='Verified clinic address; no verified building coordinates or available ZIP centroid.')
write('research/audit-runs/'+RUN+'/proposed-records.json',rows)
print('Prepared',len(rows),'rows; VCA',len(vca),'VetCor',len(vetcor))
