"""Persist individual decisions; no blanket clinical-completeness flags."""
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
CACHE = ROOT.parent / 'ma-follow-source-cache'


def read(path):
    return json.loads(Path(path).read_text())


def write(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


# Index follows the immutable original 32-item ledger. These are specific
# decisions, not 32 successful clinical audits or assertions of no treatment.
decisions = [
('access_gap', ['accsvets.com'],
 'Newly identified homepage and about routes both returned 403. Original services/team/location restrictions were respected. Search still exposes the current Littleton address and indexed treatment descriptions; it does not replace a complete current clinical read.',
 'Preserve existing services and October11 clinical date; record the two actual failed attempts.',
 'A readable current clinical/team source remains needed; do not infer closure.'),
('access_gap', ['integrityvetcenter.com'],
 'Additional clinician biography and surgery-service routes returned 403. Indexed clinician/pricing material suggests surgery as well as oncology, but surgery cannot be promoted from that lead alone.',
 'Retain previous oncology/chemotherapy and successful clinical date; do not add surgery from search text.',
 'Readable primary surgery, clinician and present-access evidence remains needed for a new modality.'),
('partial_modality_evidence', ['vcahospitals.com/south-shore-weymouth'],
 'The current first-pass medical-oncology parent page and current indexed parent list chemotherapy, ONCEPT and electrochemotherapy, with Cicchirillo/Gumash. The earlier conclusion should distinguish this parent evidence from the three inaccessible child pages.',
 'No service deletion or new clinic. Preserve parent-page support and earlier child evidence with their actual dates.',
 'Full current ECT/immunotherapy/surgical-oncology child-page rereads remain restricted; no repeated requests.'),
('access_gap', ['vscsturbridge.com', 'online.acvs.org'],
 'Current live homepage confirms advanced surgery, address, phone and referral routes. A separate full ACVS page confirms Paul McCarthy at175CharltonRd. Newly identified internal-medicine, referring-vet and pet-parent routes returned403. The cancer procedure remains in indexed surgery text only.',
 'The clinician gap is narrowed, but no snippet-only public cancer card is added.',
 'Need readable present cancer-procedure evidence. Referral wording also conflicts between indexed parent introduction and FAQ, so confirm referral requirements.'),
('branch_gap', ['capecodvetspecialists.com'],
 'Read the current group services and Dennis contact pages. The cancer/surgery links still point to Buzzards-Bay-named routes. Zuckerman biography mentions former Dennis technician work, not present surgical assignment.',
 'Retain verified Buzzards Bay only; no South Dennis clone.',
 'Current tumor-surgery or cancer-treatment allocation to South Dennis remains unconfirmed.'),
('added', ['thrivepetcare.com/locations/massachusetts/dracut'],
 'Decoded complete inline public clinic content: branch Mass Removal service, eight published clinicians,1837BridgeSt,9784548272 and location coordinates.',
 'Add Wignall Animal Hospital, local surgery only.',
 'Assigned veterinarian, tumor suitability and appointment to confirm; no chemotherapy or oncology-board claim.'),
('added', ['thrivepetcare.com/locations/massachusetts/newton'],
 'Decoded complete inline public clinic content: branch Mass Removal service, four published clinicians,602WashingtonSt,6175272222 and location coordinates.',
 'Add Newton Animal Hospital, local surgery only.',
 'Assigned veterinarian, tumor suitability and appointment to confirm.'),
('service_gap', ['thrivepetcare.com/locations/massachusetts/nantucket'],
 'The inline public page was recovered, including seven clinicians and11CrookedLn/5082281491. It lists preventive, urgent/emergency and end-of-life care but not chemotherapy, mass removal or another explicit cancer treatment. Surgical interests in biographies are not a local procedure list.',
 'The previous empty-shell explanation is resolved. Do not add a modality from the MVMA/Pets-for-Patriots lead.',
 'Current clinic-authored cancer-treatment offering remains needed; not a claim that care is unavailable.'),
('access_gap', ['berkshirevet.com'],
 'The newly reviewed homepage also returned403. Search returns a full-looking indexed mass-removal section, but both original surgery/team bodies remain inaccessible.',
 'Preserve the Pittsfield clinical lead without creating a card from indexed excerpts.',
 'Readable current service and team evidence remains needed.'),
('access_gap', ['watertownanimalhospitalma.com'],
 'A distinct surgical-services category was found with indexed mass-removal text; its native read returned403. Previous chemotherapy wording concerns referrals, not local administration.',
 'Keep a surgery candidate; do not label this local chemotherapy.',
 'Readable surgery/team/contact core evidence remains needed.'),
('access_gap', ['southboroughvet.com'],
 'Found the older official surgery route independently; it too returned403. Indexed cancer-management wording includes mass surgery and supportive care, and refers advanced chemotherapy/radiation.',
 'Retain surgery/local-care lead; no local chemotherapy or radiation claim.',
 'Readable current clinical and clinician evidence remains needed.'),
('access_gap', ['woburnanimalhospital.com'],
 'Distinct older official surgery route returned403 as well. Indexed current practice/contact evidence is consistent with Woburn, not MassVet.',
 'No merging with Massachusetts Veterinary Referral Hospital and no snippet-based addition.',
 'Readable branch procedure and clinician evidence remains needed.'),
('access_gap', ['wellesleynatickveterinaryhospital.com', 'wellesley-natickvet.com'],
 'Located the older owned domain with explicit indexed mass-removal text,359WorcesterSt and5086533420. Both older homepage and surgery reads returned403, while the newer exact surgical route was already restricted.',
 'Record identity convergence of the two domains without inventing a second clinic.',
 'Readable current procedure/team core evidence remains needed.'),
('access_gap', ['spinnakervetclinic.com'],
 'New homepage route returned403. Indexed address167CountySt/Somerset and5086733690 distinguish it from the Maryland namesake; indexed service text alone is not a complete current review.',
 'Keep one Somerset lead; no Maryland service transfer.',
 'Readable current clinical and clinician evidence remains needed.'),
('access_gap', ['shawsheenanimalhospital.com'],
 'Found a separate owned surgical consent form explicitly describing lumpectomy marking. Its native read returned403, as did the original surgical route.',
 'Preserve mass-removal lead; do not submit the form or add a snippet-only card.',
 'Readable current procedure/team/contact evidence remains needed.'),
('access_gap', ['chestnutstreetah.com'],
 'Current homepage is readable and confirms operation/contact. Indexed surgical body describes mass removal and complex cases with on-call Dr.Fish; indexed team includes Billy Dundon, Tamara Kremer Mecabell and Kate Heaton. The actual procedure page remains restricted.',
 'Keep specific routine/complex-surgery lead without inferring Dr.Fish credentials or creating a public row from excerpts.',
 'Readable primary procedure evidence remains needed.'),
('service_gap', ['winterhillvet.wb.vetstreet.com'],
 'Read the alternate clinic-authored Vetstreet service roster. It confirms general surgery, hospice and pain care, but no explicit mass/tumor operation. Third-party mass-removal descriptions remain uncorroborated.',
 'Alternate primary route was actually checked; no generic-surgery-to-cancer conversion.',
 'An explicit current cancer treatment or mass-removal service remains needed.'),
('access_gap', ['topsfieldvet.com'],
 'New homepage attempt returned403. Search retains specific tumor surgery attributed to Dr.Wilson, but the original procedure route remains restricted.',
 'Keep Topsfield lead and exact route restrictions; do not infer a specialist credential.',
 'Readable primary clinical core evidence remains needed.'),
('service_gap', ['animalhealthcaremv.com'],
 'Original owned homepage is available, but service/contact/team child restrictions remain. The focused independent cancer-procedure search did not provide a usable current owned cancer-service route.',
 'Do not promote generic surgical capability or old professional records into a cancer modality.',
 'Explicit current tumor procedure and current assigned clinician/contact evidence remains needed.'),
('access_gap', ['pioneervalleyvh.net'],
 'Found a previously missed owned surgical page with indexed tumor removal, but its native read plus about/contact returned403. This narrows the question from generic scope to primary access.',
 'Preserve explicit tumor-surgery candidate, not a statewide absence assertion.',
 'Readable current procedure/team/contact bodies remain needed.'),
('access_gap', ['greenfieldvetclinic.com'],
 'Additional owned services route returned403. The seemingly explicit mass-removal result belongs to greenfieldveterinaryclinic.com,211NMcArthurWay/937phone,GreenfieldOhio.',
 'Exclude the Ohio evidence from MA; keep the actual MA clinic unresolved.',
 'Current MA cancer-treatment service remains unconfirmed.'),
('added_with_intake_restriction', ['brooksideveterinary.com'],
 'A previously missed owned /services/ page explicitly lists mass removals. Current team identifies EdwardFunkDVM, contact279PlainRd/4137745151, and explicitly no new clients.',
 'Add Brookside local surgery, accepting_new_patients=false, with the restriction visible in availability text.',
 'Existing clients confirm case/schedule. No promise of new-owner access.'),
('service_gap', ['hilltownsvetclinic.com'],
 'Reconciled current owned services/team/contact from the first pass with the independently indexed MVMA chemotherapy tag. No owned clinical treatment page confirms the chemotherapy tag.',
 'Preserve discrepancy; no invented local chemotherapy or claim it is absent.',
 'Current clinic-authored local treatment offering remains needed.'),
('service_gap', ['pembrokeanimalhosp.com'],
 'Recovered readable owned surgery and actual team route. They establish local soft-tissue/specialty surgery and LisaTeixeira/team, but do not publish chemotherapy or a specific tumor procedure. The tempting explicit tumour-removal page on pemah.com has a613phone and is Canadian.',
 'Resolve access/identity gap; keep cancer-modality question. Do not transfer Canadian procedures.',
 'Current MA cancer-treatment or mass-removal offering remains needed.'),
('service_gap', ['veterinarysurgeryne.com'],
 'Compared the current mobile-service description, hospital/owner entry route and Clark biography. NortheasternMA coverage and surgeon identity are supported; oncologic surgery is expressed as a personal interest rather than a current procedure offering.',
 'Retain one mobile candidate, not a DoverMA office or a cancer-service card.',
 'Specific current owner-accessible tumor operations need confirmation.'),
('service_gap', ['massvet.org/find-a-veterinarian-directory/lisa-corti', 'hampsteadanimalhospital.com'],
 'ACVS/MVMA and current partner biography support Corti and North-Shore mobile general/orthopedic surgery. Her peer-reviewed tumor-biopsy article is education, not present booking evidence for cancer operations.',
 'No mailing-address physical pin and no conversion of generic oncology directory tags to a concrete service.',
 'Specific present tumor procedure and service entry remain needed.'),
('access_gap', ['vetmoves.com', 'online.acvs.org'],
 'ACVS full page establishes MichellePowersDACVS-SA, mobile setting and surgical-oncology interest. Newly found current specialist referral route and biography returned403; partner/current indexed descriptions confirm NH/northeasternMA reach but not an independently read cancer procedure.',
 'Clinician/region gap narrowed; do not create a fixed Boston office or a duplicate mobile service.',
 'Readable specific cancer-operation offering and current route remain needed.'),
('service_gap', ['raamivs.com'],
 'Current owned office/home care services do not publish a specific cancer procedure. The independently found Wix MOVES partnership is an older separate site; it cannot prove a present schedule or branch treatment allocation.',
 'No current cancer-service card and no transfer of an old mobile partner offering.',
 'Current clinic-authored tumor procedure/partner arrangement remains needed.'),
('added_one_branch', ['secondchanceanimals.org'],
 'Current owned NorthBrookfield surgical-role description explicitly includes mass removals. Read that whole page plus actual new-patient booking, group income rules, roster and medical-director biography. The job also mentions Springfield openings; it does not independently allocate each procedure to every branch.',
 'Add NorthBrookfield only, general mass surgery with income-qualified subsidy and regular-fee access for others. Group director is not labelled the assigned surgeon.',
 'Operating veterinarian, surgical case acceptance and date to confirm. Springfield/Worcester/Southbridge cancer-surgery allocation remains unverified.'),
('source_identity_gap', ['reverepet', 'bostonpetclinics', 'bostonanimalclinic'],
 'Reviewed additional directory identities: current-looking business listings point to inconsistent addresses and old/reassigned domains. No new owned clinical source was established. Previously observed unrelated gambling/domain-sale redirects are not clinic closure evidence.',
 'Keep Revere/Lynn out of new public cancer cards; do not visit unrelated destination content again.',
 'Current clinic-owned identity, contact/provider and cancer procedure remain needed.'),
('excluded_independent_provider', ['massvet.org/find-a-veterinarian-directory/elizabeth-tullett'],
 'Professional description offers relief work at general/urgent practices and mentions mass removal among skills; it supplies no independently owner-bookable cancer service or practice.',
 'Exclude a separate clinic/service identity, without asserting she does not operate on masses.',
 None),
('excluded_geography_or_non_treatment', [],
 'Rechecked the original named OH/MO/MD/Ontario/VA/FL/UK false leads. This follow-up adds explicit GreenfieldOH and PembrokeCanada procedure traps. Spay-only programs do not establish cancer treatment.',
 'Exclude these source-to-MA service transfers; keep their actual geography in the decision ledger.',
 None),
]

original = read(ROOT / 'research/audit-runs/ma-care-20261028/remaining.json')
assert len(original) == len(decisions) == 32
pages = [read(f) for f in CACHE.glob('*.json') if 'url' in read(f)]
reviews = []
for index, (old, item) in enumerate(zip(original, decisions)):
    outcome, patterns, facts, action, remaining = item
    attempts = [p for p in pages if any(s in p['url'] for s in patterns)]
    reviews.append(dict(index=index, candidate=old['candidate'], outcome=outcome,
        inherited_review=old['reviewed_disposition'], observed_followup=facts,
        decision=action, remaining_fact=remaining,
        new_attempt_urls=[p['url'] for p in attempts],
        request_keys=[p.get('key') for p in attempts],
        references=['research/audit-runs/ma-care-20261028/remaining.json',
                    f'research/audit-runs/{OUT.name}/queries.json',
                    f'research/audit-runs/{OUT.name}/request-receipts.json'],
        review_date='2026-10-28', full_current_clinical_verification=outcome.startswith('added')))
write(OUT / 'decisions.json', reviews)
write(OUT / 'remaining.json', [r for r in reviews
    if not r['outcome'].startswith(('added', 'excluded'))])
receipts = [{k:v for k,v in p.items() if k not in ['text','links','scripts']} for p in pages]
for f in (CACHE / 'decoded').glob('*-public-fields.json'):
    p = read(f)
    receipts.append({k:v for k,v in p.items() if k != 'blocks'})
for ref, url, result in [
    ('turn30view0', 'https://www.thrivepetcare.com/locations/massachusetts/dracut/wignall-animal-hospital', 'empty_visible_text'),
    ('turn30view1', 'https://www.thrivepetcare.com/locations/massachusetts/newton/newton-animal-hospital', 'empty_visible_text'),
    ('turn30view2', 'https://www.thrivepetcare.com/locations/massachusetts/nantucket/offshore-animal-hospital', 'empty_visible_text'),
    ('turn30view3', 'https://online.acvs.org/acvsssa/rflcustomdisplay.detail_page?p_vendor_serno=103200', 'readable_provider_identity')]:
    receipts.append(dict(url=url, method='Web open', observed_date='2026-10-28',
                         timestamp_precision='date-only', result=result, reference=ref))
write(OUT / 'request-receipts.json', receipts)

index_file = ROOT / 'research/oncology-care-queue/access-restriction-index.json'
restriction_index = read(index_file)
restriction_index['massachusetts_followup_exact_routes_20261028'] = [dict(
    url=p['url'], observed_at=p['attempted_at'], http_status=403,
    scope='Exact observed route including www/trailing-slash aliases; no automatic retry/bypass. Not closure or absence of treatment.',
    reference=f'research/audit-runs/{OUT.name}/request-receipts.json')
    for p in pages if p.get('status') == 403]
write(index_file, restriction_index)
write(OUT / 'coverage.json', dict(original_items=32,
    individual_decisions=len(reviews), outcomes=dict(Counter(r['outcome'] for r in reviews)),
    new_physical_locations=4, new_network_contacts=0, new_chemotherapy_locations=0,
    final_ma_physical_locations=84, final_ma_network_contacts=2,
    final_ma_physical_chemotherapy=18, unresolved_candidate_rows=26,
    full_state_primary_census=False,
    all_source_gaps_resolved=False,
    source_note='A candidate decision is not a successful clinical verification. Remaining facts include routine appointment questions at accepted sites and unresolved clinical evidence elsewhere. No outreach performed.'))
print(Counter(r['outcome'] for r in reviews))
