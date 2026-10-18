#!/usr/bin/env python3
"""Serialize independently accepted all-country field deltas; never load a canonical snapshot.

Research packages remain in their separately verified checkout/remote archive.
Every old-value and country-completion check finishes before any production write.
"""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from validate_europe_worker_result import validate
from build_oncology_center_catalog import center_match

ROOT = Path(__file__).resolve().parents[1]
OWN_KEYS = ('executor_unfinished', 'own_unfinished', 'own_unfinished_work',
            'national_own_unfinished', 'coverage_unfinished', 'available_frontier',
            'own_accessible_remaining', 'own_accessible_unfinished', 'own_remaining',
            'available_unprocessed_provider_ids', 'available_own_frontier',
            'known_available_source_directions_unfinished', 'available_work_remains',
            'accessible_remaining_count', 'current_known_remaining_count',
            'available_remaining_count', 'own_available_remaining', 'available_unprocessed')
ROW_KEYS = set(('source_id name street city region postal_code country phone email '
                'website verification_url supporting_urls species services location_type '
                'latitude longitude coordinates_unknown coordinate_source service_area '
                'service_scope branch_availability branch_finder_url booking_url '
                'services_confirmation_status clinician_review availability_note access_note '
                'last_verified verified_at review_status source audit_run_id').split())
TELE_FIELDS = {'service': 2, 'clinician_label': 3, 'consultation_details': 7,
               'primary_service_url': 8, 'assignment': 10}
FINDER_FROM_REVIEWED_CONTACT = {
    'dier-en-dokter-network-netherlands': 'https://www.dier-en-dokter.nl/nl-nl/contact',
    'dierenkliniek-ijsselstein-network': 'https://www.dierenkliniekijsselstein.nl/contact',
}


def read(p):
    return json.loads(p.read_text())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def all_country_gate(research, approval):
    assert approval.get('independent_parent_review') is True, 'Independent parent review required'
    assert approval.get('all_assigned_countries_research_complete') is True, 'All assigned countries must finish research first'
    run = research / 'research/audit-runs' / approval['run_id']
    plan = read(run / 'assignments.json')
    assigned = {x['slot']: x for x in plan['assignments']}
    assert len(assigned) == len(approval['packages']) == 6
    assert {x['slot'] for x in approval['packages']} == set(assigned)
    for package in approval['packages']:
        slot = package['slot']
        path = research / package['package']
        validate(run / 'assignments.json', slot, path)
        assert package['country'] == assigned[slot]['country']
        for name, expected in package['file_sha256'].items():
            assert digest(path / name) == expected, (slot, name, 'changed sealed file')
        accepted = read(run / f'worker-acceptance-{slot}.json')
        assert accepted['parent_accepted'] and accepted['research_complete']
        assert accepted['report_sha256'] == digest(path / 'report.md')
        assert accepted['agent_id'] == package['agent_id']
        assert accepted['available_remaining'] == 0
        for name in ('result.json', 'remaining.json'):
            obj = read(path / name)
            assert obj['research_complete'] is True
            assert obj.get('coverage_complete', True) is True
            for key in OWN_KEYS:
                assert not obj.get(key), (slot, name, 'unfinished own work', key)
    return run


def normalize(change, package, approval, normalized):
    original = change['new_value']
    row = {k: copy.deepcopy(v) for k, v in original.items() if k in ROW_KEYS}
    row['source_id'] = change['source_id']
    for key in ('street', 'city', 'region', 'postal_code', 'phone'):
        row[key] = row.get(key) or ''
    row['country'] = package['country']
    raw_location_type = original.get('location_type') or 'physical'
    row['location_type'] = 'physical' if raw_location_type == 'fixed' else raw_location_type
    assert row['location_type'] in {'physical', 'mobile', 'network'}
    row['last_verified'] = original.get('last_verified') or original.get('verified_at') or original['checked_at'][:10]
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['last_verified'])
    for key in ('latitude', 'longitude'):
        row.setdefault(key, None)
    if row['latitude'] is None or row['longitude'] is None:
        row.update(latitude=None, longitude=None, coordinates_unknown=True)
        row.setdefault('coordinate_source', 'Exact official address retained; building coordinates unknown, not estimated.')
    row.setdefault('verification_url', original.get('service_url') or change['official_url'])
    row.setdefault('supporting_urls', list(dict.fromkeys(x for x in
        (original.get('service_url'), original.get('team_url'), original.get('contact_url'), change['official_url']) if x)))
    row.setdefault('source', 'Official clinic service, team and contact sources; independent country-package review.')
    row.setdefault('clinician_review', original.get('current_clinician') or original.get('clinician') or '')
    row.setdefault('availability_note', original.get('access_note') or original.get('access_assessment') or original.get('access_quote') or '')
    if package['slot'] == 2:
        caveats = [original.get(k) for k in ('scope', 'scope_note', 'clinician_scope_note', 'caveat') if original.get(k)]
        row['availability_note'] = ' '.join(dict.fromkeys([row['availability_note']] + caveats))
    if row['location_type'] == 'network':
        assert not any(row[k] for k in ('street', 'city', 'postal_code', 'latitude', 'longitude'))
        row.update(service_scope='network', branch_availability='confirm_before_booking')
        if not row.get('branch_finder_url'):
            row['branch_finder_url'] = FINDER_FROM_REVIEWED_CONTACT[row['source_id']]
            assert row['branch_finder_url'] in row['supporting_urls']
        assert row.get('phone') or row.get('email') or row.get('booking_url')
    if row['location_type'] == 'mobile':
        assert row.get('service_area'), (row['source_id'], 'mobile area missing')
        assert row['latitude'] is None and row['longitude'] is None
    # Existing filter accepts Surgery; explicit tumour-surgery evidence was reviewed.
    row['services'] = ['Surgery' if s == 'Cancer surgery' else s for s in row['services']]
    row['review_reference'] = package['report_url']
    row['publication_run_id'] = approval['run_id']
    if not row.get('audit_run_id'):
        source_run = change.get('inherited_proposal_identity', {}).get('run_id') or change.get('source_visit_run_id')
        if source_run:
            row['audit_run_id'] = source_run
        # A publication wrapper is not a source visit. Missing original run
        # attribution stays unknown; its retained source date/report remain.
    assert row['name'] and row['website'] and row['services']
    assert row['clinician_review'] and row['availability_note'], (row['source_id'], 'core alias normalization missing')
    for key in row:
        if row[key] != original.get(key):
            normalized.append({'source_id': row['source_id'], 'field': key,
                               'old_value': original.get(key), 'new_value': row[key],
                               'reason': 'Technical schema/provenance alias or explicit unknown/branch-confirmation state; no new clinical inference.'})
    return row


def inventory_for(change, row, package, approval):
    src = copy.deepcopy(change.get('inventory_record') or {})
    original_url = src.get('working_url') or src.get('master_url')
    if original_url != row['verification_url'] or src.get('last_checked') != row['last_verified']:
        for key in ('fingerprint_sha256', 'fingerprint_method', 'http_status', 'last_reviewed_at'):
            src.pop(key, None)
    src.update(id=row['source_id'], name=row['name'], source_type=src.get('source_type', 'center'),
               master_url=row['verification_url'], supporting_urls=row['supporting_urls'],
               required_cadence='weekly', last_checked=row['last_verified'],
               last_result='Verified official cancer-service/core facts; documented modality and access limits retained.',
               working_url=row['verification_url'], content_sufficient=True,
               last_run_id=row.get('audit_run_id'), review_reference=package['report_url'],
               publication_run_id=approval['run_id'], needs_recheck=src.get('needs_recheck', False) or row['location_type'] == 'network',
               service_scope=row.get('service_scope', row['location_type']))
    if row['location_type'] == 'network':
        src['review_questions'] = list(dict.fromkeys(src.get('review_questions', []) + ['Branch-specific cancer-treatment allocation remains unconfirmed; confirm before booking.']))
    if not row.get('audit_run_id'):
        src['source_visit_run_id_unknown'] = True
    # Do not copy an unrelated/stale full-visit timestamp into a newly normalized source.
    src.pop('last_checked_at', None)
    if change['official_url'] == row['verification_url'] and 'T' in change['checked_at'] and change['checked_at'][:10] == row['last_verified']:
        src['last_checked_at'] = change['checked_at']
    return src


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--research-root', type=Path, required=True)
    parser.add_argument('--approval', type=Path, required=True)
    args = parser.parse_args()
    approval = read(args.approval)
    research = args.research_root.resolve()
    run = all_country_gate(research, approval)
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert head == remote == approval['fresh_main_sha'], 'Fresh-main lease changed'
    supp_path = ROOT / 'data/oncology_centers_supplemental.json'
    inv_path = ROOT / 'data/oncology_care_source_inventory.json'
    supp, inv = read(supp_path), read(inv_path)
    original_supp, original_inv = copy.deepcopy(supp), copy.deepcopy(inv)
    public = read(ROOT / 'data/oncology_centers.json')['centers']
    seen = public + supp['centers']
    tele_path = ROOT / 'seo/oncology_teleconsultations.py'
    tele_text = tele_path.read_text()
    module = ast.parse(tele_text)
    assignment = next(x for x in module.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROWS' for t in x.targets))
    tele_rows = ast.literal_eval(assignment.value)
    tele_old = copy.deepcopy(tele_rows)
    tele_updates, tele_new = {}, []
    applied, already, deferred, normalized = [], [], [], []
    allowed_changed = set()
    for package in approval['packages']:
        # Check the remote lease before each country packet, while all deltas
        # are still in memory. A competing main aborts without canonical writes.
        subprocess.run(['timeout', '60', 'git', '-c', 'http.connectTimeout=15',
                        '-c', 'http.lowSpeedLimit=1', '-c', 'http.lowSpeedTime=30',
                        'fetch', '--no-tags', 'origin', 'main'], cwd=ROOT,
                       check=True, capture_output=True, timeout=65)
        current_remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
        assert current_remote == head, 'Competing main: reconcile verified fields against its new baseline'
        changes = read(research / package['package'] / 'proposed_changes.json')['changes']
        for change in changes:
            sid, field = change['source_id'], change['field']
            unit = {k: change[k] for k in ('source_id', 'field', 'operation', 'official_url', 'checked_at')}
            unit.update(slot=package['slot'], country=package['country'])
            if sid not in package['approved_source_ids']:
                deferred.append(unit)
                continue
            value = change['new_value']
            if change['operation'] == 'NEW' and isinstance(value, list):
                row = tuple(value)
                assert len(row) == 11 and row[1] == package['country']
                if row in tele_rows:
                    already.append(unit)
                    continue
                assert not any((r[1], r[2]) == (row[1], row[2]) for r in tele_rows)
                assert not any(x.get('id') == sid for x in inv['sources'])
                tele_rows.append(row); tele_new.append(row)
                inv['sources'].append({'id': sid, 'name': row[2], 'source_type': 'oncology_teleconsultation', 'master_url': change['official_url'], 'supporting_urls': list(dict.fromkeys([row[8], row[9]])), 'required_cadence': 'weekly', 'last_checked': change['checked_at'][:10], 'last_result': 'Verified independently described veterinarian-only remote oncology service; geography limits retained.', 'working_url': row[8], 'content_sufficient': True, 'last_run_id': change.get('inherited_proposal_identity', {}).get('run_id'), 'source_visit_run_id_unknown': not bool(change.get('inherited_proposal_identity', {}).get('run_id')), 'review_reference': package['report_url'], 'publication_run_id': approval['run_id'], 'needs_recheck': False})
            elif field.startswith('teleconsultation.'):
                index = TELE_FIELDS[field.split('.', 1)[1]]
                hits = [i for i, r in enumerate(tele_old) if r[1] == 'Germany' and r[2] == 'HaustierDocs – Dr. Cristina Popa']
                assert len(hits) == 1
                i = hits[0]
                row = list(tele_updates.get(i, tele_rows[i]))
                if row[index] == value:
                    already.append(unit); continue
                assert row[index] == change['old_value'], (sid, field, 'tele old-value conflict')
                row[index] = value; tele_rows[i] = tuple(row); tele_updates[i] = tuple(row)
                unit.update(old_value=change['old_value'], new_value=value)
            elif change['operation'] == 'NEW':
                row = normalize(change, package, approval, normalized)
                assert not any(x.get('source_id') == sid for x in seen), (sid, 'existing identity requires field reconciliation')
                assert not any(x.get('id') == sid for x in inv['sources'])
                assert not any(center_match(row, x) or center_match(x, row) for x in seen), (sid, 'unadjudicated semantic identity collision')
                supp['centers'].append(row); seen.append(row)
                inv['sources'].append(inventory_for(change, row, package, approval))
                unit['record_sha256'] = hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            else:
                hits = [x for x in supp['centers'] if x.get('source_id') == sid]
                assert len(hits) == 1, (sid, 'missing/duplicate UPDATE identity')
                row = hits[0]
                if row.get(field) == value:
                    already.append(unit); continue
                assert row.get(field) == change['old_value'], (sid, field, 'baseline old-value conflict')
                row[field] = copy.deepcopy(value)
                allowed_changed.add((sid, field))
                unit.update(old_value=change['old_value'], new_value=value)
            applied.append(unit)
    for old, current in zip(original_supp['centers'], supp['centers']):
        for field in set(old) | set(current):
            assert old.get(field) == current.get(field) or (old.get('source_id'), field) in allowed_changed
    assert inv['sources'][:len(original_inv['sources'])] == original_inv['sources'], 'Unrelated/source dates changed'
    assert len(tele_rows) == len(tele_old) + len(tele_new)
    lines = tele_text.splitlines(keepends=True)
    for i, row in tele_updates.items():
        node = assignment.value.elts[i]
        assert node.lineno == node.end_lineno
        lines[node.lineno - 1] = repr(row) + ',\n'
    lines.insert(assignment.value.end_lineno - 1, ''.join(repr(row) + ',\n' for row in tele_new))
    new_tele_text = ''.join(lines)
    old_count, count = len(tele_old), len(tele_rows)
    old_vet_only = sum(r[5] == 'Vet only' for r in tele_old)
    vet_only = sum(r[5] == 'Vet only' for r in tele_rows)
    for old, new in [(f'len(ROWS) == {old_count}', f'len(ROWS) == {count}'), (f'>{old_count} services shown</p>', f'>{count} services shown</p>'), (f'These are {old_count} distinct services', f'These are {count} distinct services'), (f', {old_vet_only} veterinarian-only,', f', {vet_only} veterinarian-only,')]:
        assert old in new_tele_text, old
        new_tele_text = new_tele_text.replace(old, new)
    assert ast.literal_eval(next(x.value for x in ast.parse(new_tele_text).body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROWS' for t in x.targets))) == tele_rows
    # All checks above are read-only/in-memory. These are the only production writes.
    write(supp_path, supp); write(inv_path, inv); tele_path.write_text(new_tele_text)
    receipt = {'run_id': approval['run_id'], 'fresh_main_sha': head, 'integrated_at': datetime.now(timezone.utc).isoformat(), 'all_six_gate': True, 'status': 'LOCAL_VALIDATION_PENDING', 'applied': applied, 'already_applied': already, 'deferred': deferred, 'technical_normalizations': normalized, 'old_source_inventory_rows_unchanged': len(original_inv['sources']), 'old_supplemental_unrelated_fields_unchanged': True}
    write(ROOT / 'research/audit-runs' / approval['run_id'] / 'integration.json', receipt)
    print(json.dumps({'applied_NEW': sum(r['operation'] == 'NEW' for r in applied), 'applied_UPDATE_fields': sum(r['operation'] == 'UPDATE' for r in applied), 'already_applied': len(already), 'withheld': len(deferred), 'tele_rows': len(tele_rows)}))


if __name__ == '__main__':
    main()
