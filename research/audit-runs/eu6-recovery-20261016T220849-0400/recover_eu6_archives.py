"""Restore only remotely backed research bytes; verify every available member hash."""
import pathlib,json,hashlib,subprocess,tarfile,shutil,datetime
src=pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-durable-recovery')
run=pathlib.Path('research/audit-runs/eu6-20261016T142911-0400')
dst=pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-restored-evidence')
dst.mkdir(exist_ok=True)
proof=[]
for seq in ['initial']+[f'{n:03}' for n in range(1,22)]:
    stem='initial' if seq=='initial' else 'checkpoint-'+seq
    control=json.loads((src/run/'backups'/f'{stem}-control.json').read_text())
    archive=src/control['archive_path']
    ah=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert ah==control['archive_sha256'],(seq,'archive hash')
    manifest=json.loads((src/run/('initial-backup-manifest.json' if seq=='initial' else f'backups/{stem}-manifest.json')).read_text())
    expected={x['path']:x['sha256'] for x in manifest['files']}
    expected.update(control.get('controller_sha256',{}))
    p=subprocess.Popen(['zstd','-dc',str(archive)],stdout=subprocess.PIPE)
    count=0;checked=0;archive_authenticated_controller=[]
    with tarfile.open(fileobj=p.stdout,mode='r|') as tf:
        for m in tf:
            rel=pathlib.PurePosixPath(m.name)
            assert not rel.is_absolute() and '..' not in rel.parts and rel.parts[:2] in {('research','audit-runs'),('research','oncology-care-queue')},m.name
            if m.isdir():continue
            assert m.isfile(),('nonregular member',m.name)
            data=tf.extractfile(m).read();h=hashlib.sha256(data).hexdigest()
            if m.name in expected:assert h==expected[m.name],(seq,m.name);checked+=1
            elif seq=='initial' and m.name==(run/'initial-backup-manifest.json').as_posix():archive_authenticated_controller.append(m.name)
            elif rel.is_relative_to(run) and str(rel.relative_to(run)) in {'assignments.json','backups/ledger.json','collect_frozen_backup.py','controller-plan.json','criteria.json','github_backup_orchestrator.js','report.md','restore-guide.md',f'backups/{stem}-manifest.json'}:archive_authenticated_controller.append(m.name)
            else:raise AssertionError(('unmanifested',seq,m.name))
            target=dst/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);count+=1
    assert p.wait()==0
    assert checked==len(expected),(seq,checked,len(expected))
    proof.append({'checkpoint':seq,'archive_sha256':ah,'members_restored':count,'members_individually_verified':checked,'controller_members_authenticated_by_archive_only':archive_authenticated_controller})
receipt={'restored_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_branch_sha':'67697594526d4a0e60e23f584ed212301d845115','destination':str(dst),'archives':proof,'production_changes':False}
(dst/'restoration-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
