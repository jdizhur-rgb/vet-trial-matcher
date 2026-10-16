#!/usr/bin/env python3
"""Reject cross-country/replayed Europe worker packages before integration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FILES = ('report.md', 'proposed_changes.json', 'result.json', 'evidence.json', 'queries.json', 'remaining.json')
IDENTITY = ('run_id', 'slot', 'country', 'baseline_sha')


def validate(assignments_path: Path, slot: int, package: Path) -> dict:
    plan = json.loads(assignments_path.read_text())
    assignment = next(x for x in plan['assignments'] if x['slot'] == slot)
    own = (assignments_path.parent / f'worker-{slot}').resolve()
    assert package.resolve().is_relative_to(own), 'Package is outside assigned worker directory'
    payloads = {}
    for name in FILES:
        path = package / name
        assert path.is_file() and path.stat().st_size > 0, f'Missing/empty {name}'
        if name.endswith('.json'):
            obj = json.loads(path.read_text())
            assert isinstance(obj, dict), f'{name}: root must carry assignment identity'
            for key in IDENTITY:
                assert obj.get(key) == assignment[key], f'{name}: {key} mismatch: {obj.get(key)!r} != {assignment[key]!r}'
            payloads[name] = obj
    result = payloads['result.json']
    counts = result.get('counts', result)
    numbers = {}
    for name in ('assigned', 'processed', 'fully_verified'):
        value = counts.get(name)
        assert isinstance(value, int) and not isinstance(value, bool) and value >= 0, f'Invalid count {name}'
        numbers[name] = value
    assert numbers['fully_verified'] <= numbers['processed'] <= numbers['assigned']
    changes = payloads['proposed_changes.json'].get('changes', [])
    assert isinstance(changes, list), 'changes must be a list'
    for change in changes:
        assert change.get('operation') in {'NEW', 'UPDATE'}, 'Invalid change operation'
        for key in ('source_id', 'field', 'official_url', 'supporting_quote', 'branch_scope', 'checked_at'):
            assert change.get(key), f'Change missing {key}'
        assert 'old_value' in change and 'new_value' in change
        assert change['official_url'].startswith(('https://', 'http://'))
        if change.get('entity') == 'physical' and change['operation'] == 'NEW':
            record = change['new_value']
            assert record.get('country') == assignment['country'], 'Foreign physical record in assigned country package'
            assert record.get('source_id') == change['source_id']
            assert change['old_value'] is None, 'New record cannot have an old value'
    if result.get('coverage_complete') is True:
        assert result.get('coverage'), 'Country completion requires explicit coverage evidence'
        remaining = payloads['remaining.json']
        assert not remaining.get('executor_unfinished', remaining.get('own_unfinished_work')), 'Unfinished executor work cannot close country'
    return {'status': 'PASS', **{key: assignment[key] for key in IDENTITY}, **numbers, 'changes': len(changes), 'package': str(package)}


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        assignment = {'run_id': 'test-controller', 'slot': 3, 'country': 'Poland', 'baseline_sha': 'abc'}
        plan = root / 'assignments.json'
        plan.write_text(json.dumps({'assignments': [assignment]}))
        worker = root / 'worker-3'
        worker.mkdir()
        for name in FILES:
            (worker / name).write_text('Poland report' if name.endswith('.md') else json.dumps({**assignment, 'counts': {'assigned': 1, 'processed': 1, 'fully_verified': 0}, 'changes': []}))
        assert validate(plan, 3, worker)['status'] == 'PASS'
        wrong = {**assignment, 'country': 'Germany'}
        (worker / 'result.json').write_text(json.dumps(wrong))
        try:
            validate(plan, 3, worker)
        except AssertionError as error:
            assert 'country mismatch' in str(error)
        else:
            raise AssertionError('Cross-country result accepted')
    print('EUROPE_WORKER_IDENTITY_SELF_TEST_OK')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assignments', type=Path)
    parser.add_argument('--slot', type=int)
    parser.add_argument('--package', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print(json.dumps(validate(args.assignments, args.slot, args.package), ensure_ascii=False))


if __name__ == '__main__':
    main()
