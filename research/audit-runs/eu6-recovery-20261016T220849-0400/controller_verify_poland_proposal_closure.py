"""Parent-only verification of frozen Poland proposal locators, not clinical acceptance."""
import argparse,collections,hashlib,json,pathlib
def canonical(v):
    return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def verify(root,base,patches):
    own=root/base/'worker-3'
    ledger=json.loads((root/base/'backups/ledger.json').read_text())['uploaded_files']
    rows=[]
    for rel in ['working/effective-proposal-closure-001.json',*patches]:
        path=own/rel
        full=path.relative_to(root).as_posix()
        assert full in ledger,('Closure not remote verified',full)
        blob=path.read_bytes()
        assert hashlib.sha256(blob).hexdigest()==ledger[full],('Closure changed',full)
        obj=json.loads(blob)
        assert (obj['run_id'],obj['slot'],obj['country'],obj['baseline_sha'])==(base.name,3,'Poland','b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45')
        rows+=obj.get('records',obj.get('added_records',[]))
    indices=[];identities=[];counts=collections.Counter()
    files={}
    for row in rows:
        rel=pathlib.PurePosixPath(row['frozen_path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        assert rel.parts[0] in ('working','sources','checkpoints')
        path=own/rel
        assert path.resolve().is_relative_to(own.resolve()) and not path.is_symlink()
        full=path.relative_to(root).as_posix()
        assert full in ledger and ledger[full]==row['file_sha256'],('Not remotely verified exact file',full)
        if full not in files:
            blob=path.read_bytes()
            assert hashlib.sha256(blob).hexdigest()==row['file_sha256'],('File changed',full)
            files[full]=json.loads(blob)
        record=files[full]
        for part in row['json_pointer'].split('/')[1:]:
            part=part.replace('~1','/').replace('~0','~')
            record=record[int(part)] if isinstance(record,list) else record[part]
        assert hashlib.sha256(canonical(record)).hexdigest()==row['record_sha256'],('Record mismatch',row['source_id'])
        assert record['source_id']==row['source_id']
        assert record['operation']==row['operation']
        assert record.get('field','record')==row['field']
        if row['operation']=='NEW':
            assert record['old_value'] is None
        assert 'old_value' in record and 'new_value' in record
        indices.append(row['effective_index']);identities.append((row['source_id'],row['operation'],row['field']));counts[row['operation']]+=1
    assert len(set(indices))==len(indices) and sorted(indices)==list(range(len(rows)))
    assert len(set(identities))==len(identities)
    return {'run_id':base.name,'slot':3,'country':'Poland','kind':'PARENT_INDEPENDENT_FROZEN_PROPOSAL_LOCATOR_QA','records':len(rows),'counts':dict(counts),'unique_files':len(files),'exact_path_file_record_sha_identity_operation_field_pass':True,'new_old_null_pass':True,'sequential_unique_indices_pass':True,'clinical_source_evidence_accepted':False,'country_research_complete_accepted':False,'site_publication':False,'qualification':'Locator integrity only. Supporting quote, branch scope, full semantic identity and baseline old/new publication checks remain independent gates.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--base',required=True);p.add_argument('--patch',action='append',default=[])
    a=p.parse_args();print(json.dumps(verify(pathlib.Path(a.root),pathlib.Path(a.base),a.patch),ensure_ascii=False,indent=2))
