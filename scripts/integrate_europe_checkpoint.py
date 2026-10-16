#!/usr/bin/env python3
"""Apply controller-approved European deltas, never worker snapshots.

The approval manifest is an independent parent review, not a worker assertion.
All comparisons finish before any canonical file is written.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from validate_europe_worker_result import validate
from build_oncology_center_catalog import center_match

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(value)).casefold() if c.isalnum())


def identity_hits(row, rows):
    hits = []
    for existing in rows:
        if existing.get('country') != row['country']:
            continue
        same_address = norm(existing.get('street')) == norm(row.get('street')) and norm(existing.get('city')) == norm(row.get('city'))
        same_phone = norm(existing.get('phone')) == norm(row.get('phone')) and bool(row.get('phone'))
        if existing.get('source_id') == row['source_id'] or same_address or same_phone or center_match(row, existing) or center_match(existing, row):
            hits.append({k: existing.get(k) for k in ('source_id', 'name', 'street', 'city', 'phone', 'website')})
    return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--approval', type=Path, required=True)
    args = parser.parse_args()
    approval = read(args.approval)
    run = ROOT / 'research/audit-runs' / approval['run_id']
    assert approval['independent_parent_review'] is True
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert head == remote == approval['fresh_main_sha'], 'Fresh main lease changed'
    supp_path = ROOT / 'data/oncology_centers_supplemental.json'
    inv_path = ROOT / 'data/oncology_care_source_inventory.json'
    supp, inv = read(supp_path), read(inv_path)
    before_supp, before_inv = copy.deepcopy(supp), copy.deepcopy(inv)
    public = read(ROOT / 'data/oncology_centers.json')['centers']
    seen = public + supp['centers']
    receipts = []
    for item in approval['packages']:
        package = ROOT / item['package']
        gate = validate(run / 'assignments.json', item['slot'], package)
        proposed_path = package / 'proposed_changes.json'
        assert hashlib.sha256(proposed_path.read_bytes()).hexdigest() == item['proposed_sha256'], 'Unsealed proposal changed'
        changes = read(proposed_path)['changes']
        assert set(item['approved_source_ids']) <= {x['source_id'] for x in changes}
        receipt = {**gate, 'review': item, 'applied': [], 'already_applied': [], 'deferred': []}
        for change in changes:
            sid = change['source_id']
            if sid not in item['approved_source_ids']:
                receipt['deferred'].append({'source_id': sid, 'reason': 'Not independently approved in this package'})
                continue
            assert change['entity'] in {'physical', 'inventory'}, 'Tele requires separate tuple/count reconciliation'
            field = change['field']
            target = inv['sources'] if change['entity'] == 'inventory' else supp['centers']
            key = 'id' if change['entity'] == 'inventory' else 'source_id'
            found = [x for x in target if x.get(key) == sid]
            if change['operation'] == 'NEW':
                row = copy.deepcopy(change['new_value'])
                row['review_reference'] = str((package / 'evidence.json').relative_to(ROOT))
                if found:
                    # A cumulative checkpoint is not permission to overwrite
                    # an earlier published card or replace its immutable cite.
                    assert len(found) == 1 and {k:v for k,v in found[0].items() if k != 'review_reference'} == {k:v for k,v in row.items() if k != 'review_reference'}, f'Existing new source differs: {sid}'
                    receipt['already_applied'].append({'source_id': sid, 'field': field})
                    continue
                assert not identity_hits(row, seen), (sid, identity_hits(row, seen))
                source = copy.deepcopy(change['inventory_record'])
                source['review_reference'] = row['review_reference']
                assert source['id'] == sid and not any(x.get('id') == sid for x in inv['sources'])
                assert source['last_checked'] == change['checked_at'][:10]
                assert row.get('last_verified', row.get('verified_at')) == change['checked_at'][:10]
                supp['centers'].append(row)
                inv['sources'].append(source)
                seen.append(row)
            else:
                assert len(found) == 1, f'UPDATE missing or duplicate source: {sid}'
                row = found[0]
                if row.get(field) == change['new_value']:
                    receipt['already_applied'].append({'source_id': sid, 'field': field})
                    continue
                assert row.get(field) == change['old_value'], (sid, field, row.get(field), change['old_value'])
                row[field] = copy.deepcopy(change['new_value'])
            receipt['applied'].append({'source_id': sid, 'field': field, 'operation': change['operation'], 'official_url': change['official_url'], 'checked_at': change['checked_at']})
        receipts.append(receipt)
    # Preserve every unrelated record and every historical date byte-for-value.
    changed = {(x['source_id'], x['field']) for r in receipts for x in r['applied'] if x['operation'] == 'UPDATE'}
    # Some historical supplemental overrides intentionally repeat a source ID;
    # compare original positions instead of collapsing them into a dictionary.
    for old, current in zip(before_supp['centers'], supp['centers']):
        sid = old.get('source_id')
        for field in old:
            assert old[field] == current.get(field) or (sid, field) in changed, (sid, field)
    new_inv = {x['id']: x for x in inv['sources']}
    for old in before_inv['sources']:
        for field in old:
            assert old[field] == new_inv[old['id']].get(field) or (old['id'], field) in changed
    write(supp_path, supp)
    write(inv_path, inv)
    output = {'run_id': approval['run_id'], 'fresh_main_sha': head, 'integrated_at': datetime.now().astimezone().isoformat(), 'packages': receipts, 'status': 'LOCAL_VALIDATION_PENDING'}
    write(run / approval['receipt_name'], output)
    print(json.dumps({'status': output['status'], 'applied': sum(len(r['applied']) for r in receipts), 'receipt': approval['receipt_name']}))


if __name__ == '__main__':
    main()
