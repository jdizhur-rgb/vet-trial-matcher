"""Read-only exact sealed German delta chain; no clinical/country acceptance.

Only explicit checkpoint proposal paths authenticated by the remote ledger are
read. Raw HTTP outputs, restrictions' bodies and quarantine are not traversed.
"""
import argparse
import collections
import copy
import hashlib
import json
import pathlib

RUN = pathlib.Path(__file__).resolve().parent
REPO = RUN.parents[2]
OWN = RUN / 'worker-4'
EXPECTED = (RUN.name, 4, 'Germany', 'b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45', '/root/oct16_de')


def withdraw_unapplied_new(operations, origins, operation, verified):
    """Validate exact frozen old value; never represents a production deletion."""
    assert operation['operation'] == 'WITHDRAW_PROPOSED_NEW'
    target = operation['prior_proposal']
    key = ('NEW', operation['source_id'])
    assert key in operations and key in origins, ('Missing staged NEW', key)
    assert origins[key] == target['path']
    assert verified[target['path']] == target['sha256']
    assert operation['old'] == operations[key]['new'], ('Withdrawal old mismatch', key)
    assert operation['new'] is None and operation['production_modified'] is False
    del operations[key]
    del origins[key]
    return {'source_id': key[1], 'prior_proposal': copy.deepcopy(target),
            'kind': 'withdraw_unapplied_NEW_not_production_delete'}


def audit(last=38):
    assert 19 <= last <= 999
    ledger = json.loads((RUN / 'backups/ledger.json').read_text())['uploaded_files']
    verified = {}

    def read(rel):
        p = pathlib.PurePosixPath(rel)
        assert len(p.parts) == 3 and p.parts[0] == 'checkpoints'
        assert p.parts[1].startswith('block-') and p.parts[1][6:].isdigit()
        assert p.parts[2] == 'proposed_changes.json'
        path = OWN / p
        assert not path.is_symlink() and path.resolve().is_relative_to(OWN.resolve())
        key = path.relative_to(REPO).as_posix()
        assert key in ledger, ('Not remote-verified', key)
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        assert sha == ledger[key], ('Frozen payload changed', key)
        verified[rel] = sha
        data = json.loads(raw)
        assert tuple(data[k] for k in ('run_id', 'slot', 'country', 'baseline_sha', 'agent_id')) == EXPECTED
        return data

    operations = {}
    origins = {}
    previous = None
    amendments = []
    withdrawals = []
    for number in range(19, last + 1):
        rel = f'checkpoints/block-{number:02}/proposed_changes.json'
        data = read(rel)
        if previous:
            assert all(data['base_proposal'][k] == v for k, v in previous.items())
        for operation in data['operations']:
            if operation['operation'] == 'WITHDRAW_PROPOSED_NEW':
                read(operation['prior_proposal']['path'])
                withdrawn = withdraw_unapplied_new(operations, origins, operation, verified)
                assert withdrawn['source_id'] not in [x['source_id'] for x in withdrawals]
                withdrawals.append(dict(withdrawn, block=number))
                continue
            assert operation['operation'] in ('NEW', 'UPDATE')
            key = (operation['operation'], operation['source_id'])
            assert key not in operations, ('Duplicate operation identity', key)
            operation = copy.deepcopy(operation)
            operations[key] = operation
            origins[key] = rel
            if operation['operation'] == 'NEW':
                assert operation['old'] is None
                assert operation['new']['source_id'] == operation['source_id']
                if operation.get('replaces_unapplied_physical_proposal'):
                    target = operation['replaces_unapplied_physical_proposal']
                    assert any(x['source_id'] == operation['replaced_source_id'] and
                               x['prior_proposal'] == target for x in withdrawals)
                    assert operation['new']['location_type'] == 'network'
                    assert operation['new']['service_scope'] == 'network'
                    assert all(not operation['new'].get(f) for f in
                               ('street', 'postal_code', 'city', 'phone', 'latitude', 'longitude'))
                fields = operation['fields']
                assert len({f['field'] for f in fields}) == len(fields)
                for field in fields:
                    assert field['old'] is None
                    assert field['new'] == operation['new'][field['field']]
        for amendment in data.get('staged_NEW_field_amendments', []):
            target = amendment['base_operation']
            read(target['path'])
            assert verified[target['path']] == target['sha256']
            key = ('NEW', amendment['source_id'])
            assert origins[key] == target['path']
            operation = operations[key]
            for field in amendment['fields']:
                assert operation['new'][field['field']] == field['old']
                old = [f for f in operation['fields'] if f['field'] == field['field']]
                assert len(old) == 1 and old[0]['new'] == field['old']
                operation['new'][field['field']] = field['new']
                old[0].update({k: v for k, v in field.items() if k != 'old'})
                old[0]['old'] = None
            amendments.append({'block': number, 'kind': 'staged_NEW_values_only', 'source_id': amendment['source_id'], 'fields': [f['field'] for f in amendment['fields']]})
        for amendment in data.get('proposal_field_evidence_amendments', []):
            target = amendment['target_proposal']
            read(target['path'])
            assert verified[target['path']] == target['sha256']
            key = ('NEW', amendment['source_id'])
            assert origins[key] == target['path']
            operation = operations[key]
            fields = [f for f in operation['fields'] if f['field'] == amendment['field']]
            assert len(fields) == 1 and fields[0] == amendment['old_evidence']
            assert amendment['new_evidence']['new'] == fields[0]['new']
            fields[0].update(amendment['new_evidence'])
            amendments.append({'block': number, 'kind': 'field_evidence_only', 'source_id': amendment['source_id'], 'field': amendment['field']})
        previous = {'path': rel, 'sha256': verified[rel]}
    return {'status': 'PASS', 'run_id': RUN.name, 'slot': 4, 'country': 'Germany', 'first_block': 19, 'last_block': last, 'counts': dict(collections.Counter(k[0] for k in operations)), 'verified_proposal_files': verified, 'amendments': amendments, 'withdrawals': withdrawals, 'exact_chain_identity_old_new_and_amendments_pass': True, 'clinical_evidence_accepted': False, 'country_research_accepted': False, 'site_publication': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--last', type=int, default=38)
    print(json.dumps(audit(parser.parse_args().last), ensure_ascii=False, indent=2))
