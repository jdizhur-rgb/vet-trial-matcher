#!/usr/bin/env python3
"""Offline regression proof for the independently accepted six-country recovery.

The old logical-content hashes are committed so shallow CI checkouts do not
need an older git object or live source/network access to prove preservation.
"""
import ast
import copy
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path

from build_oncology_center_catalog import center_match
from integrate_europe_recovery import all_country_gate, OWN_KEYS, TELE_FIELDS
from validate_europe_worker_result import FILES

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = 'eu6-recovery-20261018T020312Z'
BASE = ROOT / 'research/audit-runs' / RUN_ID
COUNTRIES = ('Austria', 'Czechia', 'Poland', 'Germany', 'France', 'Netherlands')


def read(path):
    return json.loads(path.read_text())


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def sha(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def before_ri_finish(rows, path):
    """Validate and remove the two accepted October23 RI additions only."""
    manifest = read(ROOT / 'research/audit-runs/ri-finish-20261023/baseline-projection.json')
    spec = manifest['collections'][path]
    changes = {c['id']: c for c in spec['changes']}
    assert set(changes) == {'ri-hope-veterinary-care', 'ri-cumberland-animal-hospital'}
    assert len(rows) == spec['after_count']
    result, seen = [], set()
    for row in rows:
        identity = row.get(spec['key'])
        if identity not in changes:
            result.append(row)
            continue
        assert identity not in seen
        seen.add(identity)
        assert changes[identity]['before'] is None
        assert sha(row) == changes[identity]['after_sha256'], identity
    assert seen == set(changes)
    assert len(result) == spec['before_count']
    return result


def before_later_ri_pass(rows, path):
    """Project the exact accepted RI delta out of the historical EU proof.

    Every changed current row is checked first. The original European counts,
    hashes, dates and branch-identity assertions below remain unchanged.
    """
    # Remove only the eight individually reviewed Nebraska additions after
    # verifying their exact current hashes. Historical European/RI proof stays frozen.
    ne = read(ROOT / 'research/audit-runs/ne-care-20261023/baseline-projection.json')['collections'][path]
    assert len(rows) == ne['after_count']
    changes = {c['id']: c for c in ne['changes']}
    assert len(changes) == 8
    added = [r for r in rows if r.get(ne['key']) in changes]
    assert len(added) == 8
    assert all(sha(r) == changes[r[ne['key']]]['after_sha256'] for r in added)
    rows = [r for r in rows if r.get(ne['key']) not in changes]
    assert len(rows) == ne['before_count']
    # Exact independently accepted Foster addition; historical baselines stay frozen.
    spec = read(ROOT / 'research/audit-runs/ri-six-final-20261023/baseline-projection.json')['collections'][path]
    assert spec['id'] == 'ri-foster-veterinary-clinic'
    assert len(rows) == spec['after_count']
    added = [r for r in rows if r.get(spec['key']) == spec['id']]
    assert len(added) == 1 and sha(added[0]) == spec['after_sha256']
    rows = [r for r in rows if r.get(spec['key']) != spec['id']]
    assert len(rows) == spec['before_count']
    rows = before_ri_finish(rows, path)
    manifest = read(ROOT / 'research/audit-runs/ri-care-20261022/baseline-projection.json')
    spec = manifest['collections'][path]
    key = spec['key']
    assert len(rows) == spec['after_count']
    changes = {c['id']: c for c in spec['changes']}
    assert len(changes) == 11
    assert sum(c['before'] is None for c in changes.values()) == 10
    assert set(changes) == {'ocean-state-veterinary-specialists'} | {
        r['source_id'] for r in read(ROOT / 'research/audit-runs/ri-care-20261022/published-records.json')
    }
    result, seen = [], set()
    for row in rows:
        change = changes.get(row.get(key))
        if change is None:
            result.append(row)
            continue
        assert row[key] not in seen, row[key]
        seen.add(row[key])
        assert sha(row) == change['after_sha256'], (row[key], 'unreviewed later RI drift')
        if change['before'] is not None:
            result.append(copy.deepcopy(change['before']))
    assert seen == set(changes)
    assert len(result) == spec['before_count']
    return result


def tele_rows():
    module = ast.parse((ROOT / 'seo/oncology_teleconsultations.py').read_text())
    return ast.literal_eval(next(node.value for node in module.body
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROWS'
                                               for t in node.targets)))


def expect_rejected(root, approval):
    try:
        all_country_gate(root, approval)
    except AssertionError:
        return
    raise AssertionError('Incomplete/replayed fixture passed the publication gate')


def test_gate():
    with tempfile.TemporaryDirectory(prefix='eu6-gate-test-') as temp:
        root = Path(temp)
        run = root / 'research/audit-runs' / 'test-run'
        run.mkdir(parents=True)
        approval = {'run_id': 'test-run', 'independent_parent_review': True,
                    'all_assigned_countries_research_complete': True, 'packages': []}
        assignments = []
        for slot, country in enumerate(COUNTRIES, 1):
            ident = dict(run_id='test-run', slot=slot, country=country, baseline_sha='fixture-baseline')
            assignments.append(ident)
            worker = run / f'worker-{slot}'
            worker.mkdir()
            obj = {**ident, 'counts': dict(assigned=1, processed=1, fully_verified=1),
                   'research_complete': True, 'coverage_complete': True,
                   'coverage': {'fixture': 'complete'}, 'changes': []}
            for name in FILES:
                (worker / name).write_text('Fixture report; not real research.'
                    if name.endswith('.md') else json.dumps(obj))
            hashes = {n: hashlib.sha256((worker / n).read_bytes()).hexdigest() for n in FILES}
            agent = f'/fixture/worker-{slot}'
            receipt = {**ident, 'agent_id': agent, 'parent_accepted': True,
                       'research_complete': True, 'available_remaining': 0,
                       'report_sha256': hashes['report.md']}
            (run / f'worker-acceptance-{slot}.json').write_text(json.dumps(receipt))
            approval['packages'].append(dict(slot=slot, country=country, agent_id=agent,
                package=str(worker.relative_to(root)), file_sha256=hashes))
        (run / 'assignments.json').write_text(json.dumps({'assignments': assignments}))
        all_country_gate(root, approval)
        for key in OWN_KEYS:
            path = run / 'worker-4/remaining.json'
            obj = read(path)
            obj[key] = ['documented accessible unfinished source']
            path.write_text(json.dumps(obj))
            approval['packages'][3]['file_sha256']['remaining.json'] = hashlib.sha256(path.read_bytes()).hexdigest()
            expect_rejected(root, approval)
            del obj[key]
            path.write_text(json.dumps(obj))
            approval['packages'][3]['file_sha256']['remaining.json'] = hashlib.sha256(path.read_bytes()).hexdigest()
        partial = copy.deepcopy(approval)
        partial['packages'].pop()
        expect_rejected(root, partial)
        partial = copy.deepcopy(approval)
        partial['all_assigned_countries_research_complete'] = False
        expect_rejected(root, partial)
        partial = copy.deepcopy(approval)
        del partial['packages'][0]['file_sha256']['queries.json']
        expect_rejected(root, partial)
        receipt_path = run / 'worker-acceptance-2.json'
        obj = read(receipt_path)
        obj['country'] = 'Germany'
        receipt_path.write_text(json.dumps(obj))
        expect_rejected(root, approval)


def test_data():
    approval, integration, proof = [read(BASE / name) for name in
        ('publication-approval.json', 'integration.json', 'baseline-preservation.json')]
    assert approval['all_assigned_countries_research_complete'] is True
    assert integration['all_six_gate'] is True
    assert len(approval['packages']) == 6
    for slot, country in enumerate(COUNTRIES, 1):
        package = next(x for x in approval['packages'] if x['slot'] == slot)
        accepted = read(BASE / f'worker-acceptance-{slot}.json')
        assert package['country'] == accepted['country'] == country
        assert accepted['parent_accepted'] and accepted['research_complete']
        assert accepted['available_remaining'] == 0
        assert accepted['agent_id'] == package['agent_id']
        assert accepted['report_sha256'] == package['file_sha256']['report.md']
        assert set(FILES).issubset(package['file_sha256'])
    applied = integration['applied']
    news = [x for x in applied if x['operation'] == 'NEW']
    updates = [x for x in applied if x['operation'] == 'UPDATE']
    assert len(news) == 680 and len(updates) == 79
    assert len({x['source_id'] for x in updates}) == 53
    assert not integration['already_applied'] and len(integration['deferred']) == 4
    catalog = read(ROOT / 'data/oncology_centers.json')
    public = before_later_ri_pass(catalog['centers'], 'data/oncology_centers.json')
    supp = before_later_ri_pass(read(ROOT / 'data/oncology_centers_supplemental.json')['centers'],
                               'data/oncology_centers_supplemental.json')
    inventory = before_later_ri_pass(read(ROOT / 'data/oncology_care_source_inventory.json')['sources'],
                                    'data/oncology_care_source_inventory.json')
    care_new = {x['source_id']: x for x in news if 'record_sha256' in x}
    assert len(care_new) == 678 and len(public) == 1579
    assert catalog['last_verified'] == proof['baseline_catalog_date']
    for rows in (public, supp):
        for sid, change in care_new.items():
            hits = [r for r in rows if r.get('source_id') == sid]
            assert len(hits) == 1, sid
            row = hits[0]
            actual = hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            assert actual == change['record_sha256'], (sid, 'clinical/schema drift or unintended merge')
    new_rows = [r for r in public if r.get('source_id') in care_new]
    assert Counter(r['location_type'] for r in new_rows) == proof['new_care_types']
    for row in new_rows:
        if row['location_type'] == 'network':
            assert not any(row.get(k) for k in ('street', 'city', 'postal_code', 'latitude', 'longitude'))
            assert row['branch_availability'] == 'confirm_before_booking' and row['branch_finder_url']
        if row['location_type'] == 'mobile':
            assert row['service_area'] and row['latitude'] is None and row['longitude'] is None
        if row.get('coordinates_unknown'):
            assert row['latitude'] is None and row['longitude'] is None and row['coordinate_source']
        expected_date = ('2026-10-17' if row['source_id'] in proof['new_source_date_exceptions_actual_retained17Oct']
                         else care_new[row['source_id']]['checked_at'][:10])
        assert row['last_verified'] == expected_date, (row['source_id'], 'source date drift')
    for deferred in integration['deferred']:
        assert not any(r.get('source_id') == deferred['source_id'] for r in public)
    def reversed_rows(rows):
        old_rows = copy.deepcopy([r for r in rows if r.get('source_id') not in care_new])
        for change in updates:
            if change['field'].startswith('teleconsultation.'):
                continue
            hits = [r for r in old_rows if r.get('source_id') == change['source_id']]
            assert len(hits) == 1
            assert hits[0].get(change['field']) == change['new_value']
            hits[0][change['field']] = change['old_value']
        return old_rows
    old_public, old_supp = reversed_rows(public), reversed_rows(supp)
    assert len(old_public) == proof['baseline_public_rows']
    assert sha(sorted(old_public, key=canonical)) == proof['baseline_public_reversed_delta_sha256']
    assert len(old_supp) == proof['baseline_supplemental_rows']
    assert sha(old_supp) == proof['baseline_supplemental_reversed_delta_sha256']
    prefix = proof['baseline_inventory_rows']
    assert sha(inventory[:prefix]) == proof['baseline_inventory_unchanged_prefix_sha256']
    assert len(inventory) == prefix + 680
    assert {r['id'] for r in inventory[prefix:]} == {x['source_id'] for x in news}
    tele = tele_rows()
    assert len(tele) == 66 and sum(r[5] == 'Vet only' for r in tele) == 15
    assert sum(not r[5].startswith('Vet only') for r in tele) == 50
    assert all(r[1] == 'France' and r[5] == 'Vet only' for r in tele[64:])
    old_tele = [list(r) for r in tele[:64]]
    ix = next(i for i, r in enumerate(tele[:64]) if r[1] == 'Germany' and r[2].startswith('HaustierDocs'))
    for change in updates:
        if change['field'].startswith('teleconsultation.'):
            index = TELE_FIELDS[change['field'].split('.', 1)[1]]
            assert old_tele[ix][index] == change['new_value']
            old_tele[ix][index] = change['old_value']
    assert sha(old_tele) == proof['baseline_tele_reversed_delta_sha256']
    pairs = read(ROOT / 'data/oncology_care_distinct_sites.json')['pairs']
    assert len(pairs) == 78
    for pair in pairs:
        a, b = [next(r for r in public + supp if r.get('source_id') == sid) for sid in pair['source_ids']]
        assert not center_match(a, b) and not center_match(b, a)
    # Different arbitrary IDs still deduplicate a genuinely identical branch.
    a = dict(source_id='unreviewed-a', name='Example Veterinary Clinic', street='1 Example Street',
             city='Example City', country='Austria', region='Vienna', phone='+431234567', postal_code='1234')
    b = {**a, 'source_id': 'unreviewed-b'}
    assert center_match(a, b) and center_match(b, a)


if __name__ == '__main__':
    test_gate()
    test_data()
    print('EUROPE_RECOVERY_OK six-country fail-closed gate; 680 NEW; 53 UPDATE identities/79 fields; baseline hashes and 78 exact identity pairs preserved')
