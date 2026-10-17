"""Read-only parent structural/identity audit; frozen safe members only.

This deliberately does not accept clinical statements or country completion.
No network requests, generated source files, private or held raw outputs.
"""
import argparse
import ast
import collections
import hashlib
import json
import pathlib
import re
import unicodedata

RUN = pathlib.Path(__file__).resolve().parent
REPO = RUN.parents[2]
OWN = RUN / 'worker-5'
EXPECTED = (RUN.name, 5, 'France', 'b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45', '/root/oct16_fr')


def norm(value):
    value = unicodedata.normalize('NFKD', str(value)).casefold()
    return ''.join(c for c in value if c.isalnum() and not unicodedata.combining(c))


def phone(value):
    value = ''.join(c for c in str(value) if c.isdigit())
    if value.startswith('0033'):
        value = value[2:]
    if value.startswith('0'):
        value = '33' + value[1:]
    return value


def identity(value):
    return tuple(value.get(k) for k in ('run_id', 'slot', 'country', 'baseline_sha', 'agent_id'))


def audit(block='64'):
    assert re.fullmatch(r'\d{2,3}', block)
    ledger = json.loads((RUN / 'backups/ledger.json').read_text())['uploaded_files']
    verified = {}

    def read(rel, json_file=True):
        p = pathlib.PurePosixPath(rel)
        assert not p.is_absolute() and '..' not in p.parts
        assert p.parts[0] in ('checkpoints', 'working', 'sources', 'input')
        assert not any(s in rel.lower() for s in ('quarantine', 'denied-output', 'raw-web', 'block08-network-faluns-details'))
        assert rel != 'checkpoints/block-17/new-reviews-block-17.json'
        path = OWN / p
        assert not path.is_symlink() and path.resolve().is_relative_to(OWN.resolve())
        key = path.relative_to(REPO).as_posix()
        expected = ledger.get(key)
        assert expected, ('Not an authenticated remote safe member', key)
        raw = path.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        assert actual == expected, ('Remote/local member mismatch', key)
        verified[rel] = actual
        return json.loads(raw) if json_file else raw.decode('utf-8')

    prefix = f'checkpoints/block-{block}/'
    ready = read(prefix + 'ready.json')
    assert identity(ready) == EXPECTED
    for path, sha in ready['files'].items():
        read(path, path.endswith('.json'))
        assert verified[path] == sha
    packet = {n: read(prefix + n) for n in ('result.json', 'proposed_changes.json', 'evidence.json', 'queries.json', 'remaining.json', 'candidate-register.json')}
    assert all(identity(o) == EXPECTED for o in packet.values())
    result = packet['result.json']
    register = packet['candidate-register.json']
    rows = register['results']
    pending = register['pending_candidates']
    counts = collections.Counter(r['classification'] for r in rows)
    assert len(rows) == result['processed']
    assert len(rows) + len(pending) == result['assigned']
    assert len(pending) == result['unprocessed_registered']
    assert len({r['source_id'] for r in rows + pending}) == result['assigned']
    assert sum(r.get('fully_verified') is True for r in rows) == result['fully_verified']
    names = {'NEW': 'NEW', 'UPDATE': 'UPDATE', 'DUP': 'DUPLICATE', 'DUPLICATE': 'DUPLICATE', 'EXCL': 'EXCLUDED', 'EXCLUDED': 'EXCLUDED', 'UNRES': 'UNRESOLVED', 'UNRESOLVED': 'UNRESOLVED'}
    for k, count in counts.items():
        assert count == result[names[k]], (k, count)
    dependencies = read(result['operational_dependency_proof'])
    assert identity(dependencies) == EXPECTED
    for dep in dependencies['files']:
        read(dep['path'])
        assert verified[dep['path']] == dep['sha256']
    queries = packet['queries.json']
    assert len(queries['actual_query_metadata_payloads']) == queries['actual_query_payload_count']
    for dep in queries['actual_query_metadata_payloads']:
        read(dep['path'])
        assert verified[dep['path']] == dep['sha256']
    proposed = packet['proposed_changes.json']['changes']
    assert len(proposed) == result['NEW']
    for c in proposed:
        assert c['operation'] == 'NEW' and c['old_value'] is None
        assert c['fully_verified'] is True and c['field_evidence']
        for e in c['field_evidence']:
            assert e.get('official_url') or e.get('url'), c['source_id']
            assert e.get('checked_at') and e.get('branch_scope') and e.get('method'), (c['source_id'], e.get('field'))
        assert any(e.get('supporting_quote') or e.get('quote') for e in c['field_evidence'])
    baseline = []
    sizes = {}
    for filename, key in [('oncology_centers.json', 'centers'), ('oncology_centers_supplemental.json', 'centers'), ('oncology_care_source_inventory.json', 'sources'), ('acvim_oncology_profiles.json', 'profiles')]:
        obj = json.loads((OWN / 'input' / filename).read_text())
        values = obj if isinstance(obj, list) else obj[key]
        assert isinstance(values, list)
        baseline.extend(values)
        sizes[filename] = len(values)
    tele_tree = ast.parse((OWN / 'input' / 'oncology_teleconsultations.py').read_text())
    tele = next(ast.literal_eval(n.value) for n in tele_tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROWS' for t in n.targets))
    hits = []
    def match(a, b):
        same_phone = len(phone(a.get('phone', ''))) >= 8 and phone(a['phone']) == phone(b.get('phone', ''))
        same_address = bool(a.get('street')) and norm(a['street']) == norm(b.get('street', '')) and bool(a.get('city')) and norm(a['city']) == norm(b.get('city', ''))
        same_id = a.get('source_id', a.get('id')) == b.get('source_id', b.get('id'))
        return [k for k, value in [('phone', same_phone), ('address', same_address), ('id', same_id)] if value]
    own_hits = []
    for c in proposed:
        v = c['new_value']
        if not isinstance(v, dict):
            continue
        for other in baseline:
            m = match(v, other)
            if m:
                hits.append({'source_id': c['source_id'], 'baseline': other.get('source_id', other.get('id')), 'name': other.get('name'), 'match': m})
        for other in rows + pending:
            if other['source_id'] == c['source_id']:
                continue
            b = other.get('record') or other
            if not isinstance(b, dict):
                continue
            b = dict(b, source_id=other['source_id'])
            m = match(v, b)
            if m:
                own_hits.append({'new': c['source_id'], 'other': other['source_id'], 'classification': other.get('classification'), 'match': m})
    return {'run_id': RUN.name, 'slot': 5, 'country': 'France', 'block': block, 'ready_sha256': verified[prefix + 'ready.json'], 'assigned': result['assigned'], 'processed': len(rows), 'fully_verified': result['fully_verified'], 'classification_counts': dict(counts), 'unprocessed_external': len(pending), 'verified_frozen_files': len(verified), 'operational_dependency_count': len(dependencies['files']), 'actual_query_payloads': len(queries['actual_query_metadata_payloads']), 'baseline_catalog_rows': sizes, 'baseline_tele_rows': len(tele), 'strong_baseline_identity_hits': hits, 'strong_own_identity_hits_requiring_adjudication': own_hits, 'research_complete_worker_claim': result['research_complete'], 'country_parent_acceptance': False, 'clinical_evidence_acceptance': False, 'publication': False, 'qualification': 'Read-only structural/remote-member and strong-identity audit only. Manual field/source, report, fuzzy aliases, full tele semantics, coverage and external-gap adjudication remain required.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--block', default='64')
    args = parser.parse_args()
    print(json.dumps(audit(args.block), ensure_ascii=False, indent=2))
