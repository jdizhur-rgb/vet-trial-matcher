"""Persist reviewed scope, source attempts and concrete exceptions."""
import datetime as dt,json,pathlib,re,sys,urllib.parse
from retrieve import ROOT,OUT,CACHE,batch
def write(name,d):(OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
batch([])
attempts=json.loads((OUT/'request-receipts.json').read_text())
pages=[json.loads(f.read_text()) for f in CACHE.glob('*.json') if f.name!='integration-baseline.json']
pages=[p for p in pages if 'url' in p]
index=next(p for p in pages if p['url']=='https://vetscorecard.com/vets/ma/')
cities=[p for p in pages if re.fullmatch(r'https://vetscorecard.com/vets/ma/[^/]+/',p['url'])]
coverage=[]
for p in cities:
 entries=re.findall(r'(?m)^#(\d+)\n([^\n]+)\n([^\n]+)',p['text'])
 coverage.append({'url':p['url'],'request_key':p['key'],'numbered_rows':len(entries),'raw_entries':[{'number':n,'name':name,'next_line':address} for n,name,address in entries],'scope':'Secondary discovery inventory only; not individual primary clinical verification.'})
single=index['text'].split('93 smaller towns with one clinic')[1].split('Typical vet prices')[0]
write('directory-coverage.json',{'vetscorecard':{'advertised_raw_entries':802,'advertised_town_labels':281,'city_pages':len(cities),'numbered_rows':sum(x['numbered_rows'] for x in coverage),'single_town_rows':93,'single_town_inventory_text':single,'pages':coverage},'animalshelter':{'pages':[{'url':p['url'],'request_key':p['key'],'MA_ZIP_rows':len(re.findall(r'MA\s+\d{5}',p['text'])),'raw_roster_text':p['text'].split('Massachusetts Veterinarians')[-1].split('Featured Pet')[0]} for p in pages if 'animalshelter.org/veterinarian/Massachusetts' in p['url']],'scope':'Independent historical directory layer; duplicate doctors, old addresses and nonclinical entries are not current clinics.'},'vca':{'national_sitemap':'https://vcahospitals.com/-/sitemap/sitemap-hospitals.xml','state_sitemap':'https://vcahospitals.com/-/sitemap/sitemap-hospitals-massachusetts.xml','state_urls':len(json.loads((OUT/'vca-ma-sitemap.json').read_text())),'surgery_routes':52,'surgical_branch_identities':31,'oncology_chemotherapy_routes':12}})
remaining=[
('Animal Cancer Care Specialists, Littleton','Prior exact live-route 403 restriction retained. Existing services/address preserved; no new successful source date fabricated.'),
('Integrity Veterinary Center, Northampton','Current oncology, team, chemotherapy and pricing routes returned 403. Prior successful clinic date and clinical services preserved. New source-attempt date records failure, not closure.'),
('VCA South Shore, Weymouth','Current medical-oncology page confirms the two named clinicians, branch contact and specialty phone. Direct ECT, immunotherapy and surgical-oncology child routes returned 403. Those previously evidenced services are retained; these failed child reads are not new full modality verification.'),
('Veterinary Specialty Center of Sturbridge','Current official indexed surgery offering and contact at 173 & 175 Charlton Road found. Surgery/team/about native routes returned 403; current clinician/core review insufficient for a new public row. Do not confuse with the separately verified Sturbridge Veterinary Hospital, 6 Cedar Street.'),
('Cape Cod Veterinary Specialists, South Dennis','Two current branches confirmed. Explicit oncologic surgical page is Buzzards Bay. South Dennis local cancer procedure/assigned surgical schedule remains unallocated; no cloned branch card.'),
('Thrive: Wignall Animal Hospital, Dracut','Native and Web pages are content shells. Search evidence about mass removal and clinicians is a lead, not a full current branch verification.'),
('Thrive: Newton Animal Hospital','Native and Web pages are content shells. Search evidence about mass removal and clinicians is a lead, not a full current branch verification.'),
('Thrive: Offshore Animal Hospital, Nantucket','MVMA and Pets for Patriots supply cancer-care/chemotherapy leads, but the current owned page is a native/Web shell. Public document inspection did not establish chemotherapy. No present modality or clinician assignment invented.'),
('Berkshire Veterinary Hospital, Pittsfield','Owned surgery and team routes returned 403. Indexed official mass-removal/contact lead preserved; no new card from snippets alone.'),
('Watertown Animal Hospital','Owned oncology/additional-service routes returned 403; indexed wording explicitly concerns chemotherapy referrals. No local chemotherapy inferred.'),
('Southborough Veterinary Hospital','Current official indexed local surgery/cancer assessment found; native clinical routes returned 403. Preserve service/clinician verification gap, not an assertion that treatment is absent.'),
('Woburn Animal Hospital','Indexed local mass-removal lead; owned surgical page returned 403. Current complete clinical verification remains unavailable.'),
('Wellesley-Natick Veterinary Hospital','New official indexed surgery route found; native route returned 403. Old/new domains and current staff require a complete primary review before addition.'),
('Spinnaker Veterinary Clinic, Somerset','Indexed local surgery lead; owned route returned 403. Do not confuse with Somerset Regional Animal Hospital in Maryland.'),
('Shawsheen Animal Hospital, Tewksbury','Indexed mass-removal surgery lead; owned surgery route returned 403. No snippet-only addition.'),
('Chestnut Street Animal Hospital, Needham','Indexed routine and complex mass-removal offering; owned service route returned 403. Current full team/contact/service review remains unestablished.'),
('Winter Hill Veterinary Clinic, Somerville','Indexed mass-removal lead; owned service returned 403. Current full primary verification gap.'),
('Topsfield Veterinary Hospital','Indexed tumor-surgery lead; owned surgical route returned 403. No new card from an excerpt.'),
('Animal Health Care Associates, Martha’s Vineyard','Current owned homepage found; services/contact/team child routes returned 403. No branch oncology modality inferred from general surgery.'),
('Pioneer Valley Veterinary Hospital, Greenfield','Current owned homepage returned 403. General-surgery and clinician references do not establish a reviewed cancer service.'),
('Greenfield Veterinary Clinic','Owned homepage returned 403; general surgical references alone insufficient for a cancer service.'),
('Brookside Animal Hospital, Greenfield','Current owned homepage/about/contact read. Generic surgery lacks a published cancer/mass procedure in reviewed material. This is unconfirmed scope, not absence of care.'),
('Hilltowns Veterinary Clinic, Washington','Current owned service/team pages read. MVMA chemotherapy tag not corroborated by a current owned treatment offering. No local chemotherapy inferred.'),
('Pembroke Animal Hospital','MVMA chemotherapy lead; attempted owned root returned 403. Current primary services/provider/contact remain unverified.'),
('Veterinary Surgery of New England','Current mobile surgery and northeastern Massachusetts service area confirmed, with Geoffrey Clark DACVS. Oncologic surgery appears as a personal interest; reviewed current service pages emphasize cruciate work, not explicit present owner-accessible tumor operations. Retain cancer-service scope question; Dover base is not a MA office.'),
('North Shore Veterinary Surgery / Lisa Corti','Current professional and partner sources establish mobile surgery and coverage, but not a specific present cancer procedure. No mailing-address point or generic surgeon-to-oncologist conversion.'),
('MOVES Boston','Current regional source returned 403. Partner pages are evidence of visiting surgery, not an independent confirmed MA cancer service or fixed office.'),
('RAAM','Current owned service page establishes office/home veterinary care, not an explicit current tumor procedure. Historical MOVES partnership is not a current cancer-service allocation.'),
('Second Chance Animal Services','Current owned hospital/clinician roster and 2025 impact page reviewed. The official 2024 report describes mass removals, but the current group service and impact text do not allocate current cancer surgery by branch. Retain present service/allocation question rather than clone four clinics.'),
('Revere Pet Clinic and Lynn Pet Clinic','Follow-up establishes the directory-linked bostonpetclinics.com redirects to unrelated gambling content; bostonanimalclinic.com redirects to a domain-sale page. Do not use either as clinical evidence or infer clinic closure. Secondary mass-removal descriptions are not a current owned clinical verification.'),
('Elizabeth Tullett','Professional source describes relief work, not an independently owner-bookable cancer-care practice. No physical or mobile clinic card created.'),
('Out-of-state and non-cancer noise','Northside Springfield OH; All Creatures Springfield MO; Somerset Regional Animal Hospital MD; Hyde Park Veterinary Hospital Ontario; Veterinary Outpatient Surgical Center VA; Vet Mobile Surgery Southwest FL; UK Berkshire practices were excluded by their actual locations. ARL Spay Waggin and MAF spay/neuter programs do not establish tumor treatment.')]
write('remaining.json',[{'candidate':name,'reviewed_disposition':reason,'requires_owner_outreach':False} for name,reason in remaining])
accepted=json.loads((OUT/'evidence.json').read_text())
write('candidate-dispositions.json',accepted+[{'candidate':n,'decision':'specific_unconfirmed_or_excluded_scope','reason':r} for n,r in remaining])
restrictions=json.loads((ROOT/'research/oncology-care-queue/access-restriction-index.json').read_text())
restrictions['massachusetts_exact_routes_20261028']=[{'url':r['url'],'observed_at':r['attempted_at'],'http_status':403,'scope':'Exact observed native route including www/trailing-slash aliases; no automatic retry/bypass. Not closure or absence of treatment.','reference':'research/audit-runs/'+OUT.name+'/request-receipts.json'} for r in attempts if r.get('status')==403]
(ROOT/'research/oncology-care-queue/access-restriction-index.json').write_text(json.dumps(restrictions,ensure_ascii=False,indent=2)+'\n')
write('coverage-summary.json',{'run_id':OUT.name,'date':'2026-10-28','status':'systematic_discovery_pass_closed_with_named_source_and_scope_exceptions','not_a_statewide_individual_primary_clinical_census':True,'saved_exact_search_queries':sum(len(json.loads(f.read_text())['queries']) for f in OUT.glob('search-*.json')),'native_request_receipts':len(attempts),'new_physical':61,'new_network_contacts':2,'existing_successful_core_reviews':17,'existing_retained_prior_successful_dates':2,'unprocessed_inventory_rows_not_claimed_as_primary_reviews':True,'no_outreach':True,'no_new_state_guide':True})
print('Research saved:',len(attempts),'request receipts;',len(accepted),'accepted individual reviews;',len(remaining),'specific remaining/excluded dispositions')
