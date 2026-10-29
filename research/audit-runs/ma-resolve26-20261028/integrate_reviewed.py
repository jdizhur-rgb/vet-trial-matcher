"""Accepted care facts, with indexed-primary and live-read provenance separate."""
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
RUN = OUT.name
DATE = '2026-10-28'
CACHE = ROOT.parent / 'ma-resolve-source-cache'


def read(p):
    return json.loads(Path(p).read_text())


def write(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')


def sha(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


base = read(ROOT.parent / 'ma-resolve-baseline.json')
for p, d in base.items():
    assert read(ROOT / p) == d, 'Refuse to overwrite an altered baseline: ' + p
supp = copy.deepcopy(base['data/oncology_centers_supplemental.json'])
inventory = copy.deepcopy(base['data/oncology_care_source_inventory.json'])
queries = read(OUT / 'queries.json')
sources = {s['reference']: s for s in queries['sources']}
# Previously returned complete clinical section, retained as inherited evidence
# rather than a new native visit or a fresh timestamp.
sources['turn40search0'] = dict(reference='turn40search0',
    url='https://watertownanimalhospitalma.com/service-category/surgicalservices/',
    title='Surgical Services – Watertown Animal Hospital',
    reported_source_metadata='Crawled: last week',
    inherited_from='ma-finish-20261028; primary indexed surgical body reviewed in the preceding continuation')
zips = read(ROOT / 'data/us_zip_centroids.json')['zips']
new, updates, evidence = [], [], []
INDEX_NOTE = 'Clinical information was reviewed from extended indexed copies of separate primary pages; direct retrieval remains restricted. Confirm current case acceptance, treating veterinarian and scheduling with the practice.'


def add(slug, name, street, city, postal, phone, email, service_ref, team_ref,
        doctors, contact_ref=None, note='', services=None):
    sid = 'ma-' + slug
    assert not any(r.get('source_id') == sid for r in supp['centers'])
    refs = list(dict.fromkeys([service_ref, team_ref] + ([contact_ref] if contact_ref else [])))
    facts = [sources[x] for x in refs]
    row = dict(source_id=sid, name=name, street=street, city=city, postal_code=postal,
        region='MA', country='USA', phone=phone, email=email,
        website=sources[service_ref]['url'], verification_url=sources[service_ref]['url'],
        supporting_urls=list(dict.fromkeys(s['url'] for s in facts[1:])),
        services=services or ['Surgery'], location_type='physical',
        care_clinicians=[dict(published_label=x, url=sources[team_ref]['url']) for x in doctors],
        last_verified=DATE, verification_method='indexed primary page bodies; date-only review; live access restricted',
        availability_note=(note + ' ' + INDEX_NOTE).strip(), source='Multiple clinic-owned primary page bodies reviewed through the search index; clinician/service/contact identity reconciled, with crawl-age limitations retained.',
        audit_run_id=RUN, review_reference=f'research/audit-runs/{RUN}/evidence.json')
    z = zips.get(postal)
    if z:
        row.update(latitude=z['latitude'], longitude=z['longitude'], coordinate_source='Existing public ZIP centroid; not building coordinates.')
    else:
        row.update(latitude=None, longitude=None, coordinates_unknown=True, coordinate_source='Verified published address; no verified building point or available ZIP centroid.')
    new.append(row)
    evidence.append(dict(source_id=sid, name=name, decision='new_core_sufficient_care_listing',
        review_date=DATE, review_time_precision='date-only', source_metadata=facts,
        services=row['services'], clinical_scope=note, clinicians=row['care_clinicians'],
        retrieval_method='web.search: extended primary page bodies, multiple separate service/team/contact sources',
        full_live_primary_review=False, live_access_limitation=True))
    return row


add('vsc-sturbridge', 'Veterinary Specialty Center of Sturbridge', '173 & 175 Charlton Road', 'Sturbridge', '01566', '774-241-3111', 'info@vscsturbridge.com',
    'turn43search3', 'turn43search2', ['Paul McCarthy, DVM, DACVS', 'Megan Griffin, VMD, DACVS (SA)', 'Janet Welch, DVM, DACVS'], 'turn43search5',
    'The branch explicitly lists oncological surgery. Surgical consultations take place at 175 Charlton Road. Published referral wording is inconsistent; call to confirm whether a primary-veterinarian referral is required. This is distinct from Sturbridge Veterinary Hospital at 6 Cedar Street.')
add('berkshire-pittsfield', 'Berkshire Veterinary Hospital', '730 1/2 Crane Avenue', 'Pittsfield', '01201', '413-499-2820', 'contact@berkshirevet.com',
    'turn43search0', 'turn43search1', ['John Makuc, DVM — medical director', 'Barbara Wohlfahrt, DVM', 'Amelia Krump, DVM', 'Elizabeth Tullett, DVM'], 'turn43search4',
    'The practice explicitly lists local mass-removal surgery and surgical referrals for cases needing specialty care; no chemotherapy or medical-oncology specialist is asserted.')
add('watertown', 'Watertown Animal Hospital', '404 Main Street', 'Watertown', '02472', '617-926-8888', 'info@watertownanimalhospitalma.com',
    'turn40search0', 'turn44search1', ['Thomas J. Cusick, DVM — veterinarian and practice owner'], 'turn44search6',
    'The owned surgical-services page explicitly describes mass/lump removal at the clinic. Chemotherapy is a referral lead, not a confirmed local modality. Appointment requests require confirmation.')
add('southborough', 'Southborough Veterinary Hospital', '78 Deerfoot Road', 'Southborough', '01772', '508-485-4259', 'info@southboroughvet.com',
    'turn48search2', 'turn44search2', ['Joan Ogden, DVM', 'Joanna Gromadzki, DVM', 'Laura Cummings, DVM', 'Sharon Westphal, DVM'], 'turn44search7',
    'Local cancer management includes published mass surgery, symptom support and specialist coordination. Advanced chemotherapy/radiation may require referral; neither is assigned as local delivery.')
add('woburn-animal', 'Woburn Animal Hospital', '373 Old Russell Street', 'Woburn', '01801', '781-933-0170', '',
    'turn45search0', 'turn45search4', ['Kaleena Bysko, DVM'], 'turn59search3',
    'The branch explicitly lists mass-removal surgery. This general practice is separate from Massachusetts Veterinary Referral Hospital at 20 Cabot Road.')
add('wellesley-natick', 'Wellesley-Natick Veterinary Hospital', '359 Worcester Street', 'Natick', '01760', '508-653-3420', '',
    'turn45search2', 'turn45search3', ['Matthew Turner, BVMS, MRCVS — medical director', 'Ori Stollar, DVM, DACVB — veterinary behavior credential, not oncology'], 'turn59search4',
    'The current owned branch pages explicitly list mass-removal surgery. Old and new owned domains identify one hospital, not two sites.')
add('spinnaker-somerset', 'Spinnaker Veterinary Clinic', '167 County Street', 'Somerset', '02726', '508-673-3690', 'email@spinnakervet.com',
    'turn46search0', 'turn46search1', ['Angela Jasper, DVM', 'Christopher Jeremy Murdock, DVM'], 'turn46search2',
    'The branch lists local mass-removal surgery. The newer team roster differs from an older /site/ roster; confirm the assigned veterinarian without assuming that a clinician has departed.')
add('shawsheen', 'Shawsheen Animal Hospital', '1415 Main Street', 'Tewksbury', '01876', '978-851-5558', 'staff@shawsheenanimalhospital.com',
    'turn46search4', 'turn46search5', ['Michele Caruso, DVM', 'Tomlinson, DVM', 'Mayer, DVM', 'Kali Scott, DVM'], 'turn48search4',
    'The practice explicitly lists mass-removal surgery. A veterinarian\'s interest in oncology is not represented as board certification or local chemotherapy.')
add('chestnut-street', 'Chestnut Street Animal Hospital', '334 Chestnut Street', 'Needham', '02492', '781-444-8838', 'info@chestnutstreetah.com',
    'turn47search0', 'turn48search1', ['Billy Dundon — medical director', 'Tamara Kremer Mecabell, DVM', 'Kate Heaton, DVM'], None,
    'Routine mass-removal surgery is offered. The clinic also describes complex mass procedures with an on-call veterinarian, Dr. Fish; exact clinician credentials and visiting availability require confirmation.')
add('winter-hill', 'Winter Hill Veterinary Clinic', '257 Broadway', 'Somerville', '02145', '617-623-5075', 'contact@winterhillvet.com',
    'turn52search0', 'turn52search3', ['Kathryn Peabody, DVM — medical director', 'Oliver Hummer, DVM'], 'turn52search1',
    'The owned surgical page explicitly lists mass removals; the older generic Vetstreet service list was insufficient on its own.')
add('topsfield', 'Topsfield Veterinary Hospital', '443 Boston Road', 'Topsfield', '01983', '978-887-6553', '',
    'turn47search2', 'turn47search1', ['Matthew J. Wilson, DVM — owner', 'Evelyn Bailey, DVM'], 'turn47search4',
    'The practice explicitly offers tumor-removal surgery, with Matthew Wilson described as performing local soft-tissue operations. No surgery-board or oncology-board credential is inferred.')
add('pioneer-valley-greenfield', 'Pioneer Valley Veterinary Hospital', '571 Bernardston Road', 'Greenfield', '01301', '413-773-7511', 'pvvhreceptionist@gmail.com',
    'turn47search3', 'turn48search0', ['Lisa Underwood, DVM — veterinarian and proprietor'], None,
    'The practice explicitly lists local tumor-removal surgery. Visiting surgical support is described, but no individual visiting oncologist is assigned. It does not provide continuous 24-hour observation; critical patients may need referral.')

# Three independent sources support a conservative cancer-care contact; the
# MVMA chemotherapy tag is NOT promoted into the Chemotherapy filter.
off = add('offshore-nantucket', 'Offshore Animal Hospital', '11 Crooked Lane', 'Nantucket', '02554', '508-228-1491', 'offshore@offshoreanimalhospital.com',
    'turn51search1', 'turn51search0', ['Maia Howard, DVM — current owned profile describes part-time Nantucket work; assigned veterinarian to confirm'], None,
    'The hospital\'s direct care-program partner lists cancer treatment, corroborated by the named veterinary professional profile and current owned clinician/contact page. The professional directory lists chemotherapy, but current on-site chemotherapy delivery is not confirmed; ask the hospital before arranging cancer treatment.', ['Local oncology care'])
off['website'] = 'https://www.thrivepetcare.com/locations/massachusetts/nantucket/offshore-animal-hospital'
off['source'] = 'Direct care-program partner and professional veterinary listing, corroborated by owned inline clinic/clinician/contact content; chemotherapy remains unconfirmed.'
off['verification_method'] = 'Indexed partner/professional clinical bodies plus owned inline clinic content; date-only review'
off['care_clinicians'][0]['url'] = off['website']
off['supporting_urls'] += [off['website']]
off['review_questions'] = ['Confirm current on-site chemotherapy, treating clinician and regimen; no chemotherapy filter until confirmed.']
off.update(latitude=41.286516, longitude=-70.121038, coordinate_source='Coordinates published in the owned clinic inline location content; not independently geocoded.')
off.pop('coordinates_unknown', None)
evidence[-1]['owned_inline_reference'] = 'research/audit-runs/ma-finish-20261028/request-receipts.json'
evidence[-1]['source_role_note'] = 'Direct care-program partner plus veterinary professional listing, corroborated by owned public inline clinic data; not a hospital-owned cancer-procedure page.'

mobile = add('moves-powers-ne-ma', 'MOVES — Michelle Powers, visiting surgery', '', '', '', '', 'newhampshire@vetmoves.com',
    'turn55search4', 'turn59search1', ['Michelle Powers, DVM, DACVS (SA), CCRT, DACVSMR — surgeon, not a medical oncologist'], 'turn59search0',
    'The current provider-specific referral roster lists mass removals for Michelle Powers. Her profile explicitly covers northeastern Massachusetts through a New Hampshire-based visiting practice. Your primary veterinarian must coordinate the host clinic, surgical case and appointment through MOVES; the clinic portal is not an owner booking service. There is no fixed Massachusetts treatment office.')
mobile.update(location_type='mobile', service_scope='mobile', service_area='Northeastern Massachusetts; visiting partner veterinary hospitals, with New Hampshire coverage separately stated by the provider.', latitude=None, longitude=None, coordinates_unknown=True, coordinate_source='Visiting service; no fixed Massachusetts office or distance point.', booking_url='https://www.vetmoves.com/refer/powers/')
evidence[-1]['location_type'] = 'mobile'
evidence[-1]['clinical_scope'] += ' The mass-removal list is under Dr. Powers herself, not a nationwide service transferred to every market.'

# Independently found actual host hospital: a separate physical listing, without
# transferring its GP mass-removal procedures to every Clark/VSNE mobile visit.
bassler = add('bassler-salisbury', 'Bassler Veterinary Hospital', '1 Merrill Street', 'Salisbury', '01952', '978-463-3309', 'heidibassler@basslervet.com',
    'turn57search0', 'turn56search3', ['Heidi Bassler, DVM — primary veterinarian and owner; Geoffrey N. Clark, DVM, DACVS — separately listed visiting surgeon'], None,
    'The hospital explicitly offers local mass excision and biopsy. Geoffrey Clark is separately listed for visiting surgery; confirm whether he or the primary veterinarian will perform a particular tumor operation. This listing does not establish every VSNE mobile cancer procedure or local chemotherapy.')
bassler['verification_url'] = 'https://www.basslervet.com/surgical/'
bassler['website'] = bassler['verification_url']
bassler['supporting_urls'] = ['https://www.basslervet.com/team/', 'https://www.basslervet.com/contact/']
bassler['availability_note'] = 'The hospital explicitly offers local mass excision and biopsy. Geoffrey Clark is separately listed for visiting surgery; confirm whether he or the primary veterinarian will perform a particular tumor operation. This listing does not establish every VSNE mobile cancer procedure or local chemotherapy.'
bassler['verification_method'] = 'Live native primary surgical, team and contact bodies'
live = read(CACHE / 'f9904ea2d8594630.json')
assert live['status'] == 200 and 'mass excision and biopsy' in live['text']
evidence[-1].update(retrieval_method='requests GET of three owned primary pages', full_live_primary_review=True, live_access_limitation=False, actual_primary_request=live['attempted_at'])

existing_notes = {
 'animal-cancer-care-specialists': ('turn49search3', 'turn49search4',
     'Indexed primary service/team bodies corroborate Erin Michael Romansik, local chemotherapy, immunotherapy and small-molecule therapy. Radiation, surgery and CT are referral services; the explicit Littleton moved notice controls over old Acton titles. The live source remains restricted; confirm the appointment.'),
 'integrity-veterinary-center': ('turn49search0', 'turn49search1',
     'The owned surgical service explicitly lists mass removal and other tumor-related procedures with Anna Dunlap, DVM, DACVS-SA. The published offered/not-offered procedure list limits case scope; do not infer every abdominal or thoracic cancer operation is available. Current oncology and chemotherapy remain. Primary service bodies were reviewed as indexed copies; live retrieval remains restricted.'),
 'vca-south-shore-weymouth-animal-hospital': ('turn50search0', 'turn50search1',
     'The branch medical-oncology parent explicitly lists chemotherapy, ONCEPT and ECT. The branch surgical-oncology body lists specific tumor operations and William Snell, DVM, DACVS-SA, ACVS Fellow (Surgical Oncology). This supersedes old fellow-candidate wording, without treating an old referral PDF as the current team. Native medical-page evidence and indexed child-page evidence retain their separate methods; confirm appointment and case acceptance.')
}
for sid, (service_ref, team_ref, note) in existing_notes.items():
    row = next(r for r in supp['centers'] if r.get('source_id') == sid)
    previous_date = row.get('last_verified')
    row.update(last_verified=DATE, audit_run_id=RUN,
        review_reference=f'research/audit-runs/{RUN}/evidence.json', availability_note=note,
        verification_method='Indexed primary clinical/team bodies, with prior native evidence separately retained',
        previous_verification_date=previous_date)
    if sid == 'integrity-veterinary-center':
        row['services'] = list(dict.fromkeys(row['services'] + ['Surgery']))
        row['care_clinicians'] = [dict(published_label='Anna Dunlap, DVM, DACVS-SA — surgeon', url=sources[team_ref]['url'])]
    refs = [service_ref, team_ref]
    if sid == 'integrity-veterinary-center':
        refs.append('turn49search2')
    row['supporting_urls'] = list(dict.fromkeys(row.get('supporting_urls', []) + [sources[x]['url'] for x in refs]))
    updates.append(copy.deepcopy(row))
    evidence.append(dict(source_id=sid, name=row['name'], decision='existing_primary_body_reconciliation',
        review_date=DATE, review_time_precision='date-only', source_metadata=[sources[x] for x in refs],
        services=row['services'], clinical_scope=note, previous_verification_date=previous_date,
        retrieval_method='Extended indexed primary page bodies; blocked native routes not retried',
        full_live_primary_review=False, live_access_limitation=True))

supp['centers'].extend(copy.deepcopy(new))
for row, proof in zip(new + updates, evidence):
    sid = row['source_id']
    source = next((r for r in inventory['sources'] if r['id'] == sid), None)
    if source is None:
        source = dict(id=sid, name=row['name'], source_type='center', required_cadence='weekly')
        inventory['sources'].append(source)
    source.update(master_url=row['verification_url'] if sid != 'ma-moves-powers-ne-ma' else 'https://www.vetmoves.com/refer/',
        supporting_urls=row['supporting_urls'], last_checked=DATE,
        last_result='partial' if proof['live_access_limitation'] else 'success',
        content_sufficient=True, core_fields_sufficient=True,
        last_run_id=RUN, last_review_run_id=RUN, last_reviewed_at=DATE,
        visit_method=proof['retrieval_method'], successful_review_date_precision='date-only' if proof['live_access_limitation'] else 'exact-request',
        last_review_note=row['availability_note'], review_reference=row['review_reference'],
        fingerprint_sha256=sha(proof), fingerprint_method='sha256-reviewed-facts-and-provenance',
        needs_recheck=proof['live_access_limitation'],
        live_access_limitation=proof['live_access_limitation'])
    if proof.get('actual_primary_request'):
        source.update(last_checked_at=proof['actual_primary_request'], http_status=200)
    elif source.get('last_checked_at'):
        # Preserve the actual failed native attempt separately, rather than
        # pretending its timestamp is the successful indexed review time.
        source['last_native_attempt_at'] = source.pop('last_checked_at')
        source['last_native_attempt_http_status'] = source.pop('http_status', None)
    source['review_questions'] = row.get('review_questions', []) + (
        ['Confirm current direct-source clinical text and appointment; indexed copy crawl age is preserved in evidence.']
        if proof['live_access_limitation'] else [])

assert len(new) == 15 and len(updates) == 3
write(ROOT / 'data/oncology_centers_supplemental.json', supp)
write(ROOT / 'data/oncology_care_source_inventory.json', inventory)
write(OUT / 'proposed-records.json', new)
write(OUT / 'existing-updates.json', updates)
write(OUT / 'evidence.json', evidence)
print('Integrated14physical+1mobile; reconciled3existing; live/indexed provenance separate.')
