import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).parent
catalog_path = ROOT / 'data/trials_base.json'
rows = json.loads(catalog_path.read_text())
by_id = {row['id']: row for row in rows}
assert len(rows) == 305 and len(by_id) == 305
date = '2026-10-10'

new = [
    {
        'id': 'illinois-daunomustine-multicentric-lymphoma',
        'title': 'Daunomustine chemotherapy for treatment-naive canine multicentric lymphoma',
        'center': 'University of Illinois Veterinary Teaching Hospital',
        'country': 'USA', 'state': 'Illinois', 'species': 'Dog',
        'cancers': ['B-cell lymphoma', 'T-cell lymphoma', 'Lymphoma — other'],
        'study_type': 'treatment', 'available_for_matching': True,
        'status': 'Currently listed as a funded canine lymphoma study by the University of Illinois',
        'status_confidence': 'confirmed_current', 'verified': date,
        'url': 'https://vetmed.illinois.edu/wp-content/uploads/2026/10/Daunomustine-LSA-3.0-RDVM-Trial-Announcement-for-Website-June-2026.pdf',
        'contacts': 'Rebecca Kamerer — rmoss81@illinois.edu; 217-300-6453. Oncology appointments: 217-333-5300.',
        'funding': 'Study treatment and study visits are fully funded after eligibility is established. Owners pay the initial examination and eligibility diagnostics, unrelated care and uncovered adverse-event costs. The consultation is approximately $250, excluding diagnostics, medication and treatment. Partial adverse-event funding is available for care at Illinois. A $1,000 Illinois hospital credit is provided after completion or removal for stable/progressive disease.',
        'funding_status': 'Partially funded', 'funding_source': 'https://vetmed.illinois.edu/wp-content/uploads/2026/10/Daunomustine-LSA-3.0-RDVM-Trial-Announcement-for-Website-June-2026.pdf',
        'funding_verified': date,
        'requires': {'confirmed': True, 'active_treatment_target': True, 'min_age_years': 1, 'min_weight_kg': 4, 'prior_chemo': False, 'lymphoma_response': ['Newly diagnosed / untreated']},
        'excludes': {'prior_chemo': True, 'prior_steroids': True},
        'treatment_approaches': ['chemotherapy'], 'owner_prescreen_required': True,
        'special_requirement': 'Peripheral-node multicentric lymphoma only; indolent and small-cell lymphoma are excluded. No previous chemotherapy or systemic steroid therapy; steroid-containing topical products are allowed. Organ function, blood counts and cardiac eligibility require study-team review.',
        'notes': 'Up to five intravenous daunomustine doses every 14 days, with response-guided within-patient dose escalation and examinations/bloodwork seven days after treatment. A single L-asparaginase dose may be added for dogs not in complete remission. Dogs with progressive disease leave the trial and are offered standard care. Long-term visits follow the treatment course. Initial eligibility testing and unrelated care remain owner-paid; participation does not guarantee response.',
        'sites': [{'hospital': 'University of Illinois Veterinary Teaching Hospital', 'name': 'University of Illinois Veterinary Teaching Hospital', 'city': 'Urbana', 'state': 'IL', 'source_url': 'https://vetmed.illinois.edu/research/clinical-trials/'}],
    },
    {
        'id': 'uga-sorafenib-radiation-pituitary-macroadenoma',
        'title': 'Sorafenib with radiation for canine pituitary tumors causing Cushing’s disease',
        'center': 'University of Georgia Veterinary Teaching Hospital',
        'country': 'USA', 'state': 'Georgia', 'species': 'Dog', 'cancers': ['Brain tumor'],
        'study_type': 'treatment', 'available_for_matching': True,
        'status': 'OPEN on the current University of Georgia protocol page',
        'status_confidence': 'confirmed_current', 'verified': date,
        'url': 'https://vet.uga.edu/clinical-trial/dogs-with-pituitary-tumors-and-cushings-disease/',
        'contacts': 'Lisa Reno, UGA Clinical Trials Coordinator — 706-296-7818; see the official protocol contact link.',
        'funding': 'The study covers screening examination and laboratory tests, radiation-planning imaging, ten radiation fractions with anesthesia/hospitalization, and scheduled study rechecks, laboratory tests and follow-up MRI. Trilostane is covered if indicated. Owners pay diagnostics or treatment unrelated to the study and travel.',
        'funding_status': 'Fully funded', 'funding_source': 'https://vet.uga.edu/clinical-trial/dogs-with-pituitary-tumors-and-cushings-disease/', 'funding_verified': date,
        'requires': {'min_age_years': 1, 'active_treatment_target': True, 'planned_radiation': True},
        'excludes': {}, 'owner_prescreen_required': True,
        'special_requirement': 'This protocol is specifically for a pituitary macroadenoma with suspected ACTH-dependent Cushing’s disease, not glioma or brain tumors generally. MRI evidence, mild neurologic impairment, stable seizure frequency, suitable liver function and eligibility for general anesthesia require study-team review.',
        'treatment_approaches': ['radiation', 'targeted therapy'],
        'notes': 'Dogs with MRI evidence of a pituitary mass and clinical signs strongly suggestive of hyperadrenocorticism are randomized to sorafenib or placebo; both groups receive standard radiation treatment. The oral study product starts four days before radiation and continues during ten consecutive weekday radiation sessions. Rechecks occur at 1, 2, 3, 6 and 12 months; repeat MRI at months 3, 6 and 12. The purpose is to improve tumor and endocrine response; benefit is not guaranteed. The pituitary tumor may be an adenoma, so this is not evidence that all eligible tumors are malignant.',
        'sites': [{'hospital': 'University of Georgia Veterinary Teaching Hospital', 'name': 'University of Georgia Veterinary Teaching Hospital', 'city': 'Athens', 'state': 'GA', 'source_url': 'https://vet.uga.edu/clinical-trial/dogs-with-pituitary-tumors-and-cushings-disease/'}],
    },
]
for row in new:
    assert row['id'] not in by_id
    rows.append(row)

keep = by_id['wsu-sts-local-immunotherapy']
keep['url'] = 'https://vrcvet.com/clinical-trials/'
keep['status'] = 'VRCCO is currently enrolling; confirm WSU intake separately'
keep['verified'] = date
keep['status_confidence'] = 'confirmed_current'
keep['contacts'] = 'VRCCO / Dr. Kristen Couto — official clinical-trial page. WSU: Jennifer Heusser — jpmarcus3@wsu.edu; 509-592-3668; current WSU intake needs reconfirmation.'
keep['notes'] = 'One local T-cell-engager protocol, AVMA study 534230, previously represented by two active catalog records. Current VRCCO primary evidence describes CD3/CD28 T-cell engagement targeting B7-H3/PD-L1, injected into the tumor, followed by standard surgical removal approximately one week later. There is no placebo. VRCCO eligibility includes cutaneous soft tissue sarcoma over 1.7 cm and body weight at least 5 kg. Previously published WSU criteria required easily accessible STS at least 2 cm; the WSU page could not be read in this audit, so its present intake and site-specific criteria require confirmation. Do not apply VRCCO-specific thresholds to the unverified WSU cohort.'
keep['special_requirement'] = 'Site-specific prescreening is required. VRCCO: cutaneous STS >1.7 cm, weight ≥5 kg, suitable for surgery. WSU current recruitment was not independently confirmed on 2026-10-10.'
keep['funding_verified'] = date
keep['funding_source'] = 'https://vrcvet.com/clinical-trials/'
keep['funding'] = 'VRCCO provides a $1,500 surgery credit and covers study-related ICU stays, bloodwork and medications. The previously published WSU offer was a $1,000 medical credit plus study-related ICU, medications and bloodwork; that WSU offer was not independently reverified today. Owners pay uncovered standard surgical/diagnostic care.'
for site in keep['sites']:
    if site.get('city') == 'Bend':
        site.update({'status': 'currently enrolling', 'verified': date, 'source_url': 'https://vrcvet.com/clinical-trials/', 'eligibility': 'Cutaneous STS >1.7 cm; body weight ≥5 kg; suitable surgical candidate.', 'funding': '$1,500 surgery credit plus study-related ICU, bloodwork and medications.'})
    else:
        site['current_reconfirmation_required'] = True
        site['notes'] = 'Retained historical WSU site. Current intake was not verified because its official pages were unavailable; this is not proof of closure.'
duplicate = by_id['castr-vrcco-sts-tcell-engager']
duplicate.update({'available_for_matching': False, 'duplicate_of': keep['id'], 'status': 'Duplicate record merged into the multicenter AVMA 534230 protocol', 'status_confidence': 'confirmed_duplicate', 'verified': date, 'registry_url': keep['registry_url']})
duplicate['notes'] += ' Current VRCCO and CASTR pages link AVMA study 534230, already represented by wsu-sts-local-immunotherapy. Retained for provenance; hidden from matching to avoid counting the same protocol twice.'

vt = by_id['vt-canine-glioma-ced']
vt['url'] = 'https://research.vetmed.vt.edu/clinical-trials/current-studies/molecular-combinatorial-therapy.html'
vt['verified'] = date
vt['excludes']['prior_local_radiation'] = True
vt['notes'] = 'Current official primary protocol describes molecularly targeted cytotoxins delivered by MRI-monitored convection-enhanced delivery to a single glioma-like brain mass at least 1 cm in diameter. Dogs must weigh 3–45 kg and have mild-to-moderate neurologic signs. Prior radiation is excluded; chemotherapy/surgery require six weeks and immunotherapy six months since prior treatment. Brainstem/ventricular involvement, multiple or spreading brain tumors, uncontrolled seizures and significant concurrent illness exclude. Initial diagnostic MRI, travel, seizure-control medication and non-study/emergency care are owner-paid; enrolled study treatment and scheduled follow-up examinations are funded.'
vt['special_requirement'] = 'MRI review and neurologic prescreening are required; single glioma-like mass ≥1 cm, no previous radiation, six-week chemotherapy/surgery interval and six-month immunotherapy interval.'

catalog_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
changes = {'new': [r['id'] for r in new], 'update': [keep['id'], vt['id']], 'hide_duplicates': [duplicate['id']], 'close': [], 'new_sources': [], 'primary_evidence_files': ['http/257.json', 'http/329.json', 'http/307.json', 'http/058.json', 'web-tce-identity.json'], 'unverified_site_details_not_refreshed': ['WSU recruitment and funding']}
(RUN / 'confirmed-changes.json').write_text(json.dumps(changes, indent=2) + '\n')
print(json.dumps(changes, indent=2))
