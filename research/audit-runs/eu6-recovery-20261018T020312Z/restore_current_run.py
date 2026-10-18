"""Restore only this run's verified research archives; never reads prior cancelled/private payloads."""
import argparse,hashlib,io,json,pathlib,re,subprocess,tarfile,zstandard
BASE='research/audit-runs/eu6-recovery-20261018T020312Z'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(ref,path):return subprocess.run(['git','show',ref+':'+path],check=True,capture_output=True,timeout=45).stdout
def safe(path):
 p=pathlib.PurePosixPath(path);assert not p.is_absolute() and '..' not in p.parts and path.startswith(BASE+'/')
 assert not any(x in path.casefold() for x in ['quarantine','cancelled','private-use','/.git/']);return p

def restore(ref,dest,sequences):
 for seq in sequences:
  manifest=git(ref,f'{BASE}/backups/{seq}-manifest.json');m=json.loads(manifest);assert m['run_id']==BASE.rsplit('/',1)[-1]
  blob=git(ref,m['archive']['path']);assert sha(blob)==m['archive']['sha256']
  expected={r['path']:r['sha256'] for r in m.get('archive_files',m['files'])};seen={}
  with zstandard.ZstdDecompressor().stream_reader(io.BytesIO(blob)) as reader:
   with tarfile.open(fileobj=reader,mode='r|') as tf:
    for item in tf:
     p=safe(item.name);assert item.isfile() and item.name in expected and item.name not in seen and item.size<30_000_000
     data=tf.extractfile(item).read();assert sha(data)==expected[item.name];seen[item.name]=sha(data)
     out=dest/pathlib.Path(p);out.parent.mkdir(parents=True,exist_ok=True)
     if out.exists():assert sha(out.read_bytes())==sha(data)
     else:out.write_bytes(data)
  assert seen==expected
  for r in m.get('chunked_payloads',[]):
   parts=[]
   for piece in r['chunks']:
    if 'archive_path' in piece:data=(dest/pathlib.Path(safe(piece['archive_path']))).read_bytes()
    else:
     source=dest/pathlib.Path(safe(piece['from_path']));assert isinstance(piece['start'],int) and piece['start']>=0
     with source.open('rb') as f:f.seek(piece['start']);data=f.read(piece['bytes'])
    assert len(data)==piece['bytes'] and sha(data)==piece['sha256'];parts.append(data)
   data=b''.join(parts);assert len(data)==r['bytes'] and sha(data)==r['sha256']
   out=dest/pathlib.Path(safe(r['path']));out.parent.mkdir(parents=True,exist_ok=True)
   if out.exists():assert sha(out.read_bytes())==r['sha256']
   else:out.write_bytes(data)
  for r in m.get('reused_payloads',[]):
   out=dest/pathlib.Path(safe(r['path']));src=dest/pathlib.Path(safe(r['from_path']));data=src.read_bytes();assert sha(data)==r['sha256']
   out.parent.mkdir(parents=True,exist_ok=True)
   if out.exists():assert sha(out.read_bytes())==r['sha256']
   else:out.write_bytes(data)
  for r in m['files']:assert sha((dest/pathlib.Path(safe(r['path']))).read_bytes())==r['sha256']
  print(json.dumps({'seq':seq,'archive_sha256':sha(blob),'files_verified':len(m['files']),'stored_unique_members':len(expected),'reused_by_hash':len(m.get('reused_payloads',[])),'chunked_files':len(m.get('chunked_payloads',[])),'bytes_reused_from_verified_files':sum(x['bytes_reused'] for x in m.get('chunked_payloads',[]))}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ref');p.add_argument('destination',type=pathlib.Path);p.add_argument('sequences',nargs='+');a=p.parse_args();assert all(re.fullmatch('[0-9]{3}',s) for s in a.sequences)
 a.destination.mkdir(parents=True,exist_ok=True);restore(a.ref,a.destination,a.sequences)

