"""Allowlist-first, immutable six-worker research checkpoint collector."""
import argparse,datetime,hashlib,io,json,pathlib,re,tarfile,zstandard
ROOT=pathlib.Path(__file__).resolve().parents[3]
BASE=pathlib.Path(__file__).resolve().parent
ASSIGN=json.loads((BASE/'assignments.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def chunks(b):
    """Content-defined UTF-8 line chunks; insertion changes do not recopy a whole national payload."""
    start=offset=0
    for line in b.splitlines(keepends=True):
        offset+=len(line);size=offset-start
        if size>=32768 or (size>=2048 and int.from_bytes(hashlib.sha256(line).digest()[:2],'big')&127==0):
            yield start,b[start:offset];start=offset
    if start<len(b):yield start,b[start:]
def identity(j,slot,country):
    return (j.get('run_id'),j.get('slot'),j.get('country'),j.get('baseline_sha'))==(ASSIGN['run_id'],slot,country,ASSIGN['baseline_sha'])
def collect(seq):
    ledger_path=BASE/'backups/ledger.json'
    old=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'uploaded_files':{},'checkpoints':[]}
    found={};ready_proofs=[];errors=[]
    for a in ASSIGN['assignments']:
        slot,country=a['slot'],a['country'];own=BASE/f'worker-{slot}'
        # Never recurse into input/prior, old quarantines or mutable worker root.
        for rp in sorted((own/'checkpoints').rglob('ready.json')) if (own/'checkpoints').exists() else []:
            try:
                assert not rp.is_symlink()
                rb=rp.read_bytes();j=json.loads(rb);assert identity(j,slot,country),'Ready identity mismatch'
                f=j.get('files');assert f,'Empty ready payload'
                rows=[{'path':p,'sha256':h if isinstance(h,str) else h.get('sha256')} for p,h in f.items()] if isinstance(f,dict) else f
                block={}
                for x in rows:
                    rawpath=x.get('relative_path') or x.get('path');p=pathlib.Path(rawpath)
                    if not p.is_absolute():
                        if len(p.parts)==1:p=rp.parent/p
                        else:p=own/p
                    assert '..' not in p.parts and not p.is_symlink() and p.resolve().is_relative_to(own.resolve())
                    assert not p.resolve().is_relative_to((own/'input').resolve()),'Prior input not new payload'
                    assert p.suffix in {'.json','.md','.py','.js','.mjs','.txt','.log'},'Non-text payload'
                    name=p.relative_to(ROOT).as_posix()
                    assert not any(t in name.casefold() for t in ['quarantine','cancelled','private-use']),'Quarantined path'
                    b=p.read_bytes();h=sha(b);assert h==x['sha256'],('Changed frozen file',name)
                    assert not re.search(rb'AIza[A-Za-z0-9_-]{35}|github_pat_[A-Za-z0-9_]{40,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',b),'Credential-shaped payload'
                    assert b.decode('utf-8')
                    block[name]={'path':name,'sha256':h,'bytes':len(b)}
                name=rp.relative_to(ROOT).as_posix();block[name]={'path':name,'sha256':sha(rb),'bytes':len(rb)}
                for name,row in block.items():
                    if name in found:assert found[name]['sha256']==row['sha256'],'Conflicting frozen paths'
                    found[name]=row
                ready_proofs.append({'slot':slot,'country':country,'path':rp.relative_to(ROOT).as_posix(),'sha256':sha(rb),'members':len(block)})
            except Exception as e:errors.append({'slot':slot,'country':country,'ready':rp.relative_to(ROOT).as_posix(),'error':str(e)})
    new=[]
    for p,row in found.items():
        if p in old['uploaded_files']:assert old['uploaded_files'][p]==row['sha256'],('Previously backed frozen path changed',p)
        else:new.append(row)
    content_paths={h:p for p,h in old['uploaded_files'].items()};archive_rows=[];reused=[];chunked=[];archive_data={}
    # Index only exact immutable, already remote-verified worker files. Never
    # inspect prior input or mutable root outputs, even for deduplication.
    chunk_index={};indexed_hashes=set();source_cache={}
    if any(row['bytes']>=32768 and row['sha256'] not in content_paths for row in new):
        for path,h in old['uploaded_files'].items():
            if h in indexed_hashes:continue
            p=ROOT/path
            assert path.startswith(BASE.relative_to(ROOT).as_posix()+'/worker-') and '/checkpoints/' in path
            assert not p.is_symlink() and p.resolve().is_relative_to(BASE.resolve())
            b=p.read_bytes();assert sha(b)==h,('Previously backed source changed',path)
            indexed_hashes.add(h)
            if len(b)<32768:continue
            source_cache[path]=b
            for start,part in chunks(b):
                h=sha(part);chunk_index.setdefault((h,len(part)),{'from_path':path,'start':start,'bytes':len(part),'sha256':h})
    def add_archive(path,b):
        if path in archive_data:assert archive_data[path]==b;return
        archive_data[path]=b;archive_rows.append({'path':path,'sha256':sha(b),'bytes':len(b)})
    for row in new:
        if row['sha256'] in content_paths:reused.append({**row,'from_path':content_paths[row['sha256']]})
        else:
            b=(ROOT/row['path']).read_bytes();assert sha(b)==row['sha256'];parts=list(chunks(b)) if len(b)>=32768 else []
            saved=sum(len(part) for _,part in parts if (sha(part),len(part)) in chunk_index)
            if parts and saved>=len(b)//4:
                pieces=[];rebuilt=[]
                for _,part in parts:
                    h=sha(part);key=(h,len(part))
                    if key in chunk_index:
                        ref=dict(chunk_index[key]);source=source_cache[ref['from_path']][ref['start']:ref['start']+ref['bytes']]
                        assert sha(source)==h;pieces.append(ref);rebuilt.append(source)
                    else:
                        path=BASE.relative_to(ROOT).as_posix()+'/backups/chunks/'+h+'.bin';add_archive(path,part)
                        pieces.append({'archive_path':path,'bytes':len(part),'sha256':h});rebuilt.append(part)
                assert sha(b''.join(rebuilt))==row['sha256'];chunked.append({**row,'chunks':pieces,'bytes_reused':saved})
            else:add_archive(row['path'],b)
            content_paths[row['sha256']]=row['path']
    payload={'run_id':ASSIGN['run_id'],'baseline_sha':ASSIGN['baseline_sha'],'seq':seq,'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_layout_version':3,'files':new,'archive_files':archive_rows,'reused_payloads':reused,'chunked_payloads':chunked,'ready_blocks':ready_proofs,'errors':errors,'site_publication':False}
    archive=BASE/'backups'/f'{seq}.tar.zst';archive.parent.mkdir(exist_ok=True)
    # Only the immutable files selected above enter the incremental archive.
    with archive.open('wb') as sink:
        with zstandard.ZstdCompressor(level=10,threads=2).stream_writer(sink) as compressed:
            with tarfile.open(fileobj=compressed,mode='w|') as tf:
                for row in archive_rows:
                    b=archive_data[row['path']];assert sha(b)==row['sha256']
                    ti=tarfile.TarInfo(row['path']);ti.size=len(b);ti.mode=0o644;tf.addfile(ti,io.BytesIO(b))
    expected={r['path']:r['sha256'] for r in archive_rows};seen={}
    with archive.open('rb') as src:
        with zstandard.ZstdDecompressor().stream_reader(src) as dec:
            with tarfile.open(fileobj=dec,mode='r|') as tf:
                for member in tf:
                    assert member.isfile() and member.name in expected and member.name not in seen
                    seen[member.name]=sha(tf.extractfile(member).read())
    assert seen==expected,'Compressed archive member readback mismatch'
    payload['archive_member_readback']='PASS'
    b=archive.read_bytes();payload['archive']={'local_path':str(archive),'path':archive.relative_to(ROOT).as_posix(),'sha256':sha(b),'bytes':len(b)}
    return payload
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('seq');p.add_argument('--manifest-file',action='store_true');args=p.parse_args();assert re.fullmatch(r'[0-9]{3}',args.seq)
    payload=collect(args.seq)
    if args.manifest_file:
        target=BASE/'backups'/f'{args.seq}-draft-manifest.json'
        encoded=(json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
        target.write_bytes(encoded)
        print(json.dumps({'manifest_path':str(target),'bytes':len(encoded),'sha256':sha(encoded)}))
    else:
        print(json.dumps(payload,ensure_ascii=False))
