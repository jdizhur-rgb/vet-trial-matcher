import pathlib,json,hashlib,shutil
root=pathlib.Path('/workspace/scratch/2d03a6db0cc6/recovered-vet-trial-matcher'); old='research/audit-runs/eu6-recovery-20261016T220849-0400'; new='research/audit-runs/eu6-recovery-20261018T020312Z'
proof=json.loads((root/new/'worker-6/input/prior/checkpoints/block-67/proposed_changes.json').read_text())
expected={x['path']:x['sha256'] for x in proof['source_files']};rows=[]
for name in ['zod-proposals-002.json','wellensiek-proposals-001.json','inherited-proposals-revalidated-001.json']:
 p=old+'/worker-6/input/history/records/'+name
 rel='input/history/records/'+name;assert rel in expected
 raw=(root/p).read_bytes();h=hashlib.sha256(raw).hexdigest();assert h==expected[rel]
 dest=root/new/'worker-6/input/prior/input/history/records'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 assert not dest.exists()
 shutil.copyfile(root/p,dest); rows.append({'local_path':str(dest),'remote_archive_ledger_path':p,'sha256':h,'bytes':len(raw),'prior_remote_sha':'a1278262482f56f7571d35b8d2a3e2d5e2edede3'})
print(json.dumps(rows))

