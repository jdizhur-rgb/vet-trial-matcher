"""Parent-only verification of frozen Poland proposal locators, not clinical acceptance."""
import argparse,collections,hashlib,json,pathlib
def canonical(v):
    return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def verify(root,base,patches=(),revisions=(),steps=()):
    own=root/base/'worker-3'
    ledger=json.loads((root/base/'backups/ledger.json').read_text())['uploaded_files']
    def remote_json(rel):
        rel=pathlib.PurePosixPath(rel)
        assert not rel.is_absolute() and '..' not in rel.parts
        assert rel.parts[0] in ('working','sources','checkpoints')
        path=own/rel
        assert path.resolve().is_relative_to(own.resolve()) and not path.is_symlink()
        full=path.relative_to(root).as_posix()
        assert full in ledger,('Closure not remote verified',full)
        blob=path.read_bytes()
        assert hashlib.sha256(blob).hexdigest()==ledger[full],('Closure changed',full)
        obj=json.loads(blob)
        assert (obj['run_id'],obj['slot'],obj['country'],obj['baseline_sha'])==(base.name,3,'Poland','b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45')
        return obj
    rows=[]
    assert not steps or not (patches or revisions), 'Use explicit chronological steps OR legacy patch/revision arguments'
    closure_paths=['working/effective-proposal-closure-001.json',*(steps or [*patches,*revisions])]
    files={}
    def verify_record(row):
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
        return record
    # Authenticate chronological append/revision steps. Revisions replace exactly
    # one existing locator and must never be counted as another NEW.
    revision_count=0
    previous_path=None;seen_paths=[]
    for rel in closure_paths:
        obj=remote_json(rel)
        if previous_path is not None:
            if 'base' in obj:
                assert obj['base']['path']==previous_path
                assert obj['base']['sha256']==ledger[(own/previous_path).relative_to(root).as_posix()]
            else:
                # Early immutable patches 003/004 used an exact cumulative path
                # list instead of one previous-path/hash pair. Every listed
                # file has already passed the remote-ledger SHA check above.
                assert obj['bases']==seen_paths
        added=obj.get('records',obj.get('added_records',[]))
        for row in added:
            verify_record(row)
        rows+=added
        for revision in obj.get('revised_records',[]):
            index=revision['effective_index']
            matches=[i for i,row in enumerate(rows) if row['effective_index']==index]
            assert len(matches)==1,('Revision target must exist exactly once',index)
            i=matches[0];old=rows[i];old_locator=revision['old_locator']
            for key in ('source_id','operation','field','effective_index'):
                assert old[key]==revision[key],('Revision identity changed',index,key)
            for old_key,locator_key in [('frozen_path','path'),('file_sha256','file_sha256'),('json_pointer','json_pointer'),('record_sha256','record_sha256')]:
                assert old[old_key]==old_locator[locator_key],('Revision old locator changed',index,old_key)
            new=dict(old,**revision['new_locator'])
            verify_record(new)
            rows[i]=new;revision_count+=1
        if 'effective_count' in obj:
            assert len(rows)==obj['effective_count']
        elif 'validation' in obj and 'effective_count' in obj['validation']:
            assert len(rows)==obj['validation']['effective_count']
        elif 'effective_counts' in obj:
            assert len(rows)==obj['effective_counts']['total']
        previous_path=rel
        seen_paths.append(rel)
    indices=[];identities=[];counts=collections.Counter();new_flags={k:collections.Counter() for k in ('publication_eligible','apply_permitted','strict_fully_verified','core_fields_sufficient')}
    for row in rows:
        record=verify_record(row)
        if row['operation']=='NEW':
            for key,counter in new_flags.items():
                value=record.get(key)
                counter['true' if value is True else 'false' if value is False else 'unspecified']+=1
        indices.append(row['effective_index']);identities.append((row['source_id'],row['operation'],row['field']));counts[row['operation']]+=1
    assert len(set(indices))==len(indices) and sorted(indices)==list(range(len(rows)))
    assert len(set(identities))==len(identities)
    return {'run_id':base.name,'slot':3,'country':'Poland','kind':'PARENT_INDEPENDENT_FROZEN_PROPOSAL_LOCATOR_QA','records':len(rows),'counts':dict(counts),'unique_files':len(files),'immutable_revisions':revision_count,'new_explicit_flags':{k:dict(v) for k,v in new_flags.items()},'exact_path_file_record_sha_identity_operation_field_pass':True,'new_old_null_pass':True,'sequential_unique_indices_pass':True,'clinical_source_evidence_accepted':False,'country_research_complete_accepted':False,'site_publication':False,'qualification':'Locator integrity only. Explicit flags are reported independently; absent publication flags are not silently promoted. Supporting quote, branch scope, full semantic identity and baseline old/new publication checks remain independent gates.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--base',required=True);p.add_argument('--patch',action='append',default=[])
    p.add_argument('--revision',action='append',default=[])
    p.add_argument('--step',action='append',default=[])
    a=p.parse_args();print(json.dumps(verify(pathlib.Path(a.root),pathlib.Path(a.base),a.patch,a.revision,a.step),ensure_ascii=False,indent=2))
