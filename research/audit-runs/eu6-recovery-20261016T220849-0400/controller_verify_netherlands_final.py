"""Parent structural QA of the frozen Dutch final; never reads held raw outputs."""
import collections, hashlib, json, pathlib, re, subprocess

RUN = pathlib.Path(__file__).resolve().parent
OWN = RUN / 'worker-6'
EXPECTED = (RUN.name, 6, 'Netherlands', 'b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45', '/root/oct16_nl')
HISTORICAL = {}

def authenticate_historical_manifests():
    old_run = 'research/audit-runs/eu6-20261016T142911-0400'
    old_root = pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-durable-recovery')
    for seq in ['003','006','012']:
        rel = f'{old_run}/backups/checkpoint-{seq}-manifest.json'
        local = (old_root/rel).read_bytes()
        remote = subprocess.run(['git','show','67697594526d4a0e60e23f584ed212301d845115:'+rel], cwd=RUN.parents[2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True).stdout
        assert local == remote, ('Historical remote manifest differs',rel)
        manifest_sha = hashlib.sha256(remote).hexdigest()
        for row in json.loads(remote)['files']:
            marker = old_run+'/worker-6/records/'
            if row['path'].startswith(marker):
                suffix = row['path'].removeprefix(old_run+'/worker-6/')
                if suffix in ['records/zod-proposals-002.json','records/wellensiek-proposals-001.json','records/inherited-proposals-revalidated-001.json']:
                    HISTORICAL['input/history/'+suffix] = {'sha256':row['sha256'],'manifest':rel,'manifest_sha256':manifest_sha,'remote_sha':'67697594526d4a0e60e23f584ed212301d845115','original_path':row['path']}

def read_verified(rel, ledger):
    path = OWN / rel
    assert not path.is_symlink() and path.resolve().is_relative_to(OWN.resolve())
    assert not any(x in str(rel).lower() for x in ['quarantine', 'denied-output', 'raw-web'])
    key = path.relative_to(RUN.parents[2]).as_posix()
    expected = ledger.get(key) or HISTORICAL.get(str(rel),{}).get('sha256')
    assert expected, ('No authenticated remote member',key)
    blob = path.read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    assert expected == digest, ('Not exact remotely verified dependency', key)
    return json.loads(blob), digest

def identity(v):
    return tuple(v.get(k) for k in ['run_id','slot','country','baseline_sha','agent_id'])

def norm(s):
    return re.sub(r'[^a-z0-9]', '', str(s).casefold())

def phone(s):
    n = re.sub(r'\D', '', str(s))
    if n.startswith('0031'): n = n[2:]
    if n.startswith('0'): n = '31' + n[1:]
    return n

def walk(v):
    if isinstance(v, dict):
        if any(k in v for k in ['name','source_id','id']): yield v
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)

def verify():
    ledger = json.loads((RUN/'backups/ledger.json').read_text())['uploaded_files']
    authenticate_historical_manifests()
    ready, ready_sha = read_verified('checkpoints/block-67/ready.json', ledger)
    assert identity(ready) == EXPECTED
    final = {}
    for name in ['result.json','proposed_changes.json','evidence.json','queries.json','remaining.json']:
        obj, digest = read_verified('checkpoints/block-67/'+name, ledger)
        assert identity(obj) == EXPECTED, name
        final[name] = obj
    result = final['result.json']; rows = result['candidate_results']
    ids = [r['source_id'] for r in rows]
    assert len(ids) == len(set(ids)) == 554
    counts = collections.Counter(r['classification'] for r in rows)
    assert dict(counts) == {k: result['counts'][k] for k in counts}
    assert sum(bool(r.get('processed')) for r in rows) == 551
    assert sum(bool(r.get('fully_verified')) for r in rows) == 95
    core, core_sha = read_verified('records/final-core-index-001.json', ledger)
    assert identity(core) == EXPECTED and len(core['records']) == 95
    assert len({r['source_id'] for r in core['records']}) == 95
    dependencies = {}
    for row in core['records']:
        assert row['source_id'] in ids
        for field in ['clinical_record_files','retained_proposal_files']:
            for dep in row[field]:
                _, digest = read_verified(dep['path'], ledger)
                assert digest == dep['sha256']
                dependencies[dep['path']] = digest
    changes = final['proposed_changes.json']['changes']
    eligible = [r for r in changes if r.get('publication_eligible', True) and r.get('apply_permitted', True)]
    new = [r for r in changes if r['operation'] in ['ADD','NEW']]
    updates = [r for r in eligible if r['operation'] == 'UPDATE']
    assert len(new) == 83 and len(updates) == 9
    assert len([r for r in new if r in eligible]) == 79
    baseline = []
    for name in ['oncology_centers.json','oncology_centers_supplemental.json','oncology_care_source_inventory.json','acvim_oncology_profiles.json']:
        baseline += list(walk(json.loads((OWN/'input'/name).read_text())))
    old_values = []
    for change in updates:
        matches = [r for r in baseline if r.get('source_id',r.get('id')) == change['source_id'] and change['field'] in r]
        assert matches, ('Missing baseline identity/field', change['source_id'], change['field'])
        assert all(r[change['field']] == change['old_value'] for r in matches), ('Old-value mismatch',change['source_id'])
        old_values.append({'source_id':change['source_id'],'field':change['field'],'matches':len(matches)})
    hits = []
    for change in new:
        v = change['new_value']; sid = change['source_id']
        for other in baseline:
            exact_id = other.get('source_id',other.get('id')) == sid
            exact_phone = len(phone(v.get('phone',''))) >= 8 and phone(v['phone']) == phone(other.get('phone',''))
            exact_address = bool(v.get('street')) and norm(v['street']) == norm(other.get('street','')) and norm(v.get('city','')) == norm(other.get('city',''))
            if exact_id or exact_phone or exact_address:
                hits.append({'source_id':sid,'baseline_id':other.get('source_id',other.get('id')),'name':other.get('name'),'exact_id':exact_id,'phone':exact_phone,'address':exact_address})
    assert not hits, ('Semantic strong baseline matches require manual review',hits)
    networks = []
    for change in new:
        v=change['new_value']
        if v.get('location_type',v.get('entity')) == 'network':
            assert not v.get('street') and not v.get('postal_code') and not v.get('latitude') and not v.get('longitude')
            networks.append(change['source_id'])
    return {'run_id':RUN.name,'slot':6,'country':'Netherlands','kind':'PARENT_STRUCTURAL_FINAL_QA','frozen_ready_sha256':ready_sha,'classification_counts':dict(counts),'assigned':554,'clinical_processed':551,'fully_supported':95,'core_dependency_files':len(dependencies),'historical_remote_member_provenance':HISTORICAL,'core_dependency_sha_pass':True,'proposed_new':len(new),'eligible_new':len([r for r in new if r in eligible]),'eligible_update_fields':len(updates),'baseline_old_values':old_values,'strong_semantic_baseline_hits':hits,'network_ids':networks,'clinical_source_acceptance':False,'country_research_acceptance':False,'site_publication':False,'qualification':'Exact remote payload/core dependency, counters and old values only; full primary quote/branch and whole-tele/manual semantic review remain independent.'}

if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
