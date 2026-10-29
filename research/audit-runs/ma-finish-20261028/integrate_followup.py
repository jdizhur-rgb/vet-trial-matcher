"""Integrate four individually reviewed follow-up identities, once only."""
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
CACHE = ROOT.parent / 'ma-follow-source-cache'
RUN = OUT.name
DATE = '2026-10-28'
PATHS = ['data/oncology_centers.json', 'data/oncology_centers_supplemental.json',
         'data/oncology_care_source_inventory.json']


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def sha(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


baseline = read(ROOT.parent / 'ma-follow-integration-baseline.json')
for path in PATHS:
    assert read(ROOT / path) == baseline[path], 'Refuse to overwrite changed baseline: ' + path
supp = copy.deepcopy(baseline[PATHS[1]])
inv = copy.deepcopy(baseline[PATHS[2]])
pages = [read(f) for f in CACHE.glob('*.json')]
byurl = {p['url']: p for p in pages if 'url' in p}
rows, evidence = [], []


def add(slug, name, street, city, zip_code, phone, email, url, support, clinicians,
        note, timestamp, lat=None, lon=None):
    assert not any(x.get('source_id') == slug for x in supp['centers'])
    row = dict(source_id=slug, name=name, street=street, city=city, postal_code=zip_code,
               region='MA', country='USA', phone=phone, email=email, website=url,
               verification_url=url, supporting_urls=support, services=['Surgery'],
               care_clinicians=clinicians, location_type='physical', last_verified=DATE,
               availability_note=note, audit_run_id=RUN,
               review_reference=f'research/audit-runs/{RUN}/evidence.json',
               source='Reviewed current clinic-owned services, veterinary team and contact; '
                      'see follow-up evidence for retrieval method and intake limits.')
    if lat is not None:
        row.update(latitude=lat, longitude=lon,
                   coordinate_source='Coordinates published in the official clinic page location data; not independently geocoded.')
    else:
        z = read(ROOT / 'data/us_zip_centroids.json')['zips'].get(zip_code)
        if z:
            row.update(latitude=z['latitude'], longitude=z['longitude'],
                       coordinate_source='Existing public ZIP centroid; not building coordinates.')
        else:
            row.update(latitude=None, longitude=None, coordinates_unknown=True,
                       coordinate_source='Verified street address; no verified building coordinates or available ZIP centroid.')
    rows.append(row)
    evidence.append(dict(source_id=slug, name=name, source_urls=[url] + support,
                         actual_primary_request=timestamp, review_date=DATE,
                         facts=note, clinicians=clinicians, services=['Surgery']))


for slug, source_id in [('wignall-animal-hospital', 'ma-thrive-wignall'),
                        ('newton-animal-hospital', 'ma-thrive-newton')]:
    page = read(CACHE / 'decoded' / (slug + '-public-fields.json'))
    assert page['status'] == 200
    blocks = page['blocks']
    assert any(b.get('heading') == 'Mass Removal' for b in blocks)
    location = next(b for b in blocks if 'addressLine1' in b)
    doctors = [dict(published_label=b['bioName'] + ' — ' + b.get('bioPosition', ''),
                    url=page['url']) for b in blocks if b.get('bioName')]
    assert doctors
    add(source_id, location['name'], location['addressLine1'], location['city'],
        location['postcode'], location['mainPhone'], location['emailAddress'],
        page['url'], [], doctors,
        'The branch page explicitly lists mass-removal surgery. Current branch clinicians '
        'and contact are published in the same public page content. Confirm the procedure, '
        'assigned veterinarian and appointment; no medical-oncology specialist or chemotherapy is asserted.',
        page['attempted_at'], location['latitude'], location['longitude'])
    evidence[-1]['retrieval_method'] = 'Decode inline public Next.js Flight page content; visible-text reader alone was incomplete.'

brook = 'https://brooksideveterinary.com/services/'
assert 'Mass Removals' in byurl[brook]['text']
contact = 'https://brooksideveterinary.com/contact-us/'
assert 'not accepting new clients' in byurl[contact]['text']
team = 'https://brooksideveterinary.com/?page_id=41'
assert 'Dr. Funk' in byurl[team]['text']
add('ma-brookside-greenfield', 'Brookside Animal Hospital', '279 Plain Road', 'Greenfield',
    '01301', '413-774-5151', '', brook, [team, contact],
    [dict(published_label='Edward Funk, DVM — veterinarian and owner', url=team)],
    'The clinic lists local mass-removal surgery. Its current contact page says it is not '
    'accepting new clients. Existing clients should confirm tumor suitability, treating '
    'veterinarian and scheduling; new owners should not assume an appointment is available.',
    byurl[brook]['attempted_at'])
rows[-1]['accepting_new_patients'] = False
evidence[-1]['accepting_new_patients'] = False

job = 'https://www.secondchanceanimals.org/jobs/veterinary-technician-surgery/'
intake = 'https://www.secondchanceanimals.org/scasconnect-north-brookfield/'
group = 'https://www.secondchanceanimals.org/vetcare/'
director = 'https://www.secondchanceanimals.org/dr-ashley-raymond/'
assert 'mass removals' in byurl[job]['text']
assert 'Surgery – North Brookfield' in byurl[job]['text']
assert 'New Patient Exams' in byurl[intake]['text']
add('ma-secondchance-north-brookfield', 'Second Chance Community Veterinary Hospital — North Brookfield',
    '372 N. Main Street', 'North Brookfield', '01535', '508-637-1333',
    'northbrookfield@secondchanceanimals.org', intake, [job, group, director],
    [dict(published_label='Second Chance veterinary team; Ashley Raymond, DVM — group medical director. Assigned operating veterinarian to confirm.', url=director)],
    'The current clinic-authored North Brookfield surgical-role description explicitly '
    'includes mass removals; the hospital has a current new-patient exam booking route. '
    'Surgical-case acceptance and the operating veterinarian require confirmation. Open '
    'to all owners; subsidized rates require documented household income below 150% of '
    'the federal poverty level. Other owners pay regular fees. This is local general '
    'surgery, without an oncology-specialist or chemotherapy claim. Services are not '
    'automatically assigned to the other Second Chance branches.', byurl[job]['attempted_at'])
evidence[-1]['retrieval_method'] = 'Current employer-authored branch surgical description plus current patient entry, clinician and contact pages; not a vacancy-only opening inference.'

for row, proof in zip(rows, evidence):
    supp['centers'].append(row)
    inv['sources'].append(dict(id=row['source_id'], name=row['name'], source_type='center',
        master_url=row['verification_url'], supporting_urls=row['supporting_urls'],
        required_cadence='weekly', last_checked=DATE,
        last_checked_at=proof['actual_primary_request'], last_result='success', http_status=200,
        content_sufficient=True, last_run_id=RUN, last_review_run_id=RUN,
        last_reviewed_at=DATE, last_review_note=row['availability_note'],
        review_reference=row['review_reference'], needs_recheck=False,
        fingerprint_sha256=sha(proof), fingerprint_method='sha256-concise-reviewed-primary-facts'))

# New permitted route failures update attempt metadata, not clinical dates.
for sid, host in [('animal-cancer-care-specialists', 'accsvets.com'),
                  ('integrity-veterinary-center', 'integrityvetcenter.com')]:
    attempts = [p for p in pages if host in p.get('url', '') and p.get('status') == 403]
    last = max(attempts, key=lambda p: p['attempted_at'])
    source = next(s for s in inv['sources'] if s['id'] == sid)
    source.update(last_checked=DATE, last_checked_at=last['attempted_at'], last_result='unreachable',
        http_status=403, content_sufficient=False, last_run_id=RUN, last_review_run_id=RUN,
        needs_recheck=True, review_reference=f'research/audit-runs/{RUN}/decisions.json',
        last_review_note='Additional independently identified primary routes returned 403; earlier exact restricted routes were not retried. Prior clinical verification date and services remain unchanged.')

write(ROOT / PATHS[1], supp)
write(ROOT / PATHS[2], inv)
write(OUT / 'proposed-records.json', rows)
write(OUT / 'evidence.json', evidence)
print('Integrated four physical locations; Brookside new-client intake remains false.')
