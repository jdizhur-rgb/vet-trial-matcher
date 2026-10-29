"""Case-level result for the26 prior candidates; accepted limits stay visible."""
import json
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def read(p):
    return json.loads(Path(p).read_text())


def write(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')


accepted = {
 0: 'animal-cancer-care-specialists', 1: 'integrity-veterinary-center',
 2: 'vca-south-shore-weymouth-animal-hospital', 3: 'ma-vsc-sturbridge',
 7: 'ma-offshore-nantucket', 8: 'ma-berkshire-pittsfield', 9: 'ma-watertown',
 10: 'ma-southborough', 11: 'ma-woburn-animal', 12: 'ma-wellesley-natick',
 13: 'ma-spinnaker-somerset', 14: 'ma-shawsheen', 15: 'ma-chestnut-street',
 16: 'ma-winter-hill', 17: 'ma-topsfield', 19: 'ma-pioneer-valley-greenfield',
 26: 'ma-moves-powers-ne-ma'
}
holds = {
 4: dict(category='branch_allocation',
     result='Owned locations/about/service pages confirm two hospitals, but the procedure link and named surgical service remain Buzzards-Bay-scoped. A Dennis footer, former technician employment or referral catchment is not present local tumor-surgery assignment.',
     sources=['turn50search3','turn50search4','turn50search6','turn50search7'],
     question='Does South Dennis currently perform tumor-removal surgery or administer cancer medication on site? Which surgeon/veterinarian and which appointment days?',
     contact='508-398-7575; dennisinfo@capecodvetspecialists.com'),
 18: dict(category='specific_treatment_unconfirmed',
     result='Extended current owned homepage/about/services bodies establish the WestTisbury practice, Atwood,20AirportRd and contact. They describe general surgery/acupuncture but no explicit tumor-removal or anticancer treatment. Focused professional/clinic-author searches yielded no usable current cancer procedure.',
     sources=['turn52search4','turn52search5','turn52search7'],
     question='Does the practice currently remove dog/cat tumors or provide another cancer treatment locally, and which veterinarian accepts those cases?',
     contact='508-693-6515; animalhealthcareassoc@gmail.com'),
 20: dict(category='specific_treatment_unconfirmed',
     result='MA identity remains18FrenchKingHwy/413phone, corroborated by its own current contact body. Owned homepage contains generic surgery/placeholder wording; explicit mass-removal clinical text found in the wider search belongs to separate GreenfieldOhio and GreenfieldWisconsin practices. Named historical business members do not establish current cancer case acceptance.',
     sources=['turn52search6','turn54search6','turn54search7','turn60search0','turn60search1','turn60search2','turn60search3'],
     question='Does the Massachusetts practice currently offer mass/tumor removal, who performs it, and is it accepting new surgical patients?',
     contact='413-774-9919; website identity must remain greenfieldvetclinic.com, not the Ohio namesake'),
 22: dict(category='professional_tag_vs_current_delivery',
     result='SharonLynch professional MVMA profile explicitly lists chemotherapy/oncology; current owned homepage/team confirm her identity and local practice. They do not confirm which cancer treatments are currently delivered or available to a new case. No chemotherapy tag is promoted from the professional directory alone.',
     sources=['turn51search2','turn51search4','turn51search5'],
     question='Is chemotherapy currently administered in the Washington office, under which veterinarian/protocol arrangements, and can a new cancer patient be referred?',
     contact='413-623-5329'),
 23: dict(category='professional_tag_vs_current_delivery',
     result='LisaTeixeira MVMA profile lists chemotherapy; owned current surgery/team/contact establish PembrokeMA but no specific tumor procedure or present chemotherapy offering. The explicit tumour-removal page found at pemah.com is PembrokeCanada and is excluded.',
     sources=['turn51search3'],
     inherited_primary='ma-finish-20261028: readable owned /surgeries and /about-us/meet-our-team.html',
     question='Is chemotherapy administered at115MattakeesettStreet today, or referred elsewhere? Does the local surgical team remove tumors, and who accepts the case?',
     contact='781-293-5184'),
 24: dict(category='mobile_procedure_allocation',
     result='VSNE owned site and current partner bodies support Clark, mobile referral work and northeasternMA. Cancer surgery remains a published interest. Newly found Bassler current live pages separately prove local mass excision and list Clark as a visiting surgeon, but do not allocate those tumor cases specifically to him or every VSNE visit.',
     sources=['turn56search0','turn56search2','turn56search3','turn57search0'],
     question='Does VSNE currently book tumor-removal operations at Massachusetts host hospitals? Which cancer procedures and host/booking route apply?',
     contact='603-867-5175',
     useful_separate_result='ma-bassler-salisbury is accepted as a physical local mass-surgery hospital; no procedure automatically transferred to the whole mobile service'),
 25: dict(category='mobile_procedure_unconfirmed',
     result='MVMA full professional profile establishes Corti/NorthShore/mobile oncology tag and ACVS/partner sources support surgeon identity. Tumor-biopsy publications establish expertise, not present owner access to cancer operations. No current provider-specific operation/booking page was found in the independent exact-name/procedure search.',
     sources=['turn55search3','turn56search4','turn56search7'],
     question='Is North Shore Veterinary Surgery currently accepting tumor-removal cases through MA primary clinics, and which host hospitals and referral contact should owners use?',
     contact='978-254-0640 (published professional service contact; confirm current route)'),
 27: dict(category='historical_partner_vs_present_delivery',
     result='Current owned site confirms office/mobile care, RodArad and112MainStreetUnit4. The Wix page describes a MOVES partnership in historical language. Neither provides a present provider-specific cancer-procedure assignment or current visit schedule. MichellePowers is independently accepted as one MOVES visiting service, not a duplicate RAAM cancer card.',
     sources=['turn57search2','turn57search3'],
     question='Does RAAM currently arrange tumor operations with a visiting surgeon? Are they performed at the Pepperell office or another host, by whom, and how is a cancer case booked?',
     contact='978-877-9517; info@raamivs.com'),
 29: dict(category='primary_identity_and_freshness',
     result='Independent BBB and local business results converge on10PleasantStRevere and165BroadStLynn and both phones. Copied third-party mass-surgery descriptions trace to old domains; current-owned clinical/provider evidence remains absent. Reassigned gambling/domain-sale destinations were not revisited and do not establish clinic closure.',
     sources=['turn54search0','turn54search1','turn54search3','turn54search5','turn54search8'],
     question='What is the current clinic-owned site and treating veterinarian for each branch, and is mass-removal surgery currently offered there?',
     contact='Revere781-284-2255; Lynn781-598-0044 (secondary published contacts; verify identity before relying on them)')
}
previous = read(ROOT / 'research/audit-runs/ma-finish-20261028/remaining.json')
assert len(previous) == 26 and len(accepted) == 17 and len(holds) == 9
assert set(accepted) | set(holds) == {r['index'] for r in previous}
proof = {r['source_id']:r for r in read(OUT / 'evidence.json')}
reviews = []
for old in previous:
    i = old['index']
    row = dict(original_index=i, candidate=old['candidate'], inherited_outcome=old['outcome'],
               review_date='2026-10-28', prior_reference='research/audit-runs/ma-finish-20261028/decisions.json')
    if i in accepted:
        e = proof[accepted[i]]
        row.update(decision='core_fields_accepted_with_source_limits', source_id=accepted[i],
            reviewed_facts=e['clinical_scope'], primary_source_metadata=e['source_metadata'],
            full_live_primary_review=e['full_live_primary_review'],
            source_limit='Indexed primary copies were actually read and cross-checked across service/team/contact; source freshness and access limitations remain. This is not a claim of a new live complete source review.',
            evidence_reference='research/audit-runs/ma-resolve26-20261028/evidence.json')
    else:
        row.update(decision='not_confirmed_for_new_public_listing', **holds[i])
        row['next_step_requires_direct_clinic_confirmation'] = True
        row['outreach_sent'] = False
        row['absence_of_cancer_care_established'] = False
    reviews.append(row)
write(OUT / 'decisions.json', reviews)
write(OUT / 'remaining.json', [r for r in reviews if r['original_index'] in holds])
write(OUT / 'coverage.json', dict(prior_candidates=26, primary_core_decisions_accepted=17,
    remaining_candidates=9, new_physical_locations=14, new_mobile_services=1,
    existing_records_reconciled=3, new_service_at_existing='Integrity: local tumor/mass surgery',
    bonus_discovery='BasslerSalisbury is separate from the26; actual live primary pages confirm local mass surgery',
    ma_prepared_totals=dict(physical=98, mobile=1, network=2, total=101, physical_chemotherapy=18),
    accepted_record_evidence=dict(live_native_primary=1, indexed_primary_or_partner_with_owned_corroboration=17),
    all_live_access_gaps_resolved=False, all_cancer_scope_questions_resolved=False,
    full_state_primary_census=False, no_outreach=True,
    distinction='Core listing sufficiency, full live-source coverage, treatment certainty and appointment acceptance are separate judgments. Prior access restrictions remain in force.'))

cache = ROOT.parent / 'ma-resolve-source-cache'
pages = [read(f) for f in cache.glob('*.json')]
write(OUT / 'request-receipts.json', [{k:v for k,v in p.items() if k not in ['text','links','scripts']} for p in pages])
index_path = ROOT / 'research/oncology-care-queue/access-restriction-index.json'
index = read(index_path)
index['massachusetts_resolve26_exact_routes_20261028'] = [dict(url=p['url'], observed_at=p['attempted_at'],
    http_status=403, scope='Exact observed native route and www/trailing-slash aliases. No automatic retry/bypass. Independently indexed copies are separately attributed, not new live reads.',
    reference='research/audit-runs/ma-resolve26-20261028/request-receipts.json') for p in pages if p.get('status') == 403]
write(index_path, index)

territories_path = ROOT / 'research/oncology-care-queue/territories.json'
territories = read(territories_path)
def walk(value):
    if isinstance(value, dict):
        if value.get('territory') == 'MA':
            value.update(status='core_reconciliation_with_nine_named_confirmation_questions', completed=False,
                latest_coverage_reference='research/audit-runs/ma-resolve26-20261028/coverage.json',
                remaining='Of26 prior candidates,17 now have sufficient core evidence with explicit indexed-source limitations;9 named cancer-scope/branch/identity questions remain. Prepared98physical+1mobile+2network;not a complete current live clinical census. Publication remains pending authorization.')
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)
walk(territories)
write(territories_path, territories)
print('26 individually reconciled:17 core accepted;9 named direct-confirmation questions;15 new records including bonus Bassler.')
