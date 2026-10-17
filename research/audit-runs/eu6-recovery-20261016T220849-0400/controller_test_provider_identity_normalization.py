"""Parent-only pure fixture tests; never rerun the worker's sealing test writer."""
import argparse,copy,hashlib,importlib.util,json,pathlib
from unittest.mock import patch

def run(root,module_relative):
    base=root/'research/audit-runs/eu6-recovery-20261016T220849-0400'
    ledger=json.loads((base/'backups/ledger.json').read_text())['uploaded_files']
    path=root/module_relative
    assert path.resolve().is_relative_to((base/'worker-5/checkpoints').resolve())
    assert not path.is_symlink() and path.name in ('provider_identity_normalization.py','provider_identity_normalization_v2.py')
    expected=ledger[module_relative]
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
    spec=importlib.util.spec_from_file_location('parent_alias_pure',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    identity=dict(run_id=base.name,slot=5,country='France',agent_id='/root/oct16_fr',baseline_sha='b76a77b99d41caa62d5f91dc0c1f1bdef4f64e45')
    canonical=dict(source_id='canonical',fully_verified=True,record=dict(country='France',street='32 Avenue de Fumel',city='Montayral',postal_code='47500',phone='+33 553409355'))
    proof={**identity,'alias_source_id':'alias','canonical_source_id':'canonical','permission_scope_adjudicated':True,'source_body_recovery':False,'source_request_for_normalization':False,'canonical_address_verified_from_saved_current_primary':True,'current_canonical_street':'32 Avenue de Fumel','current_canonical_city':'Montayral','current_canonical_postal':'47500','alias_phone':'0553409355','previous_saved_canonical_explicit_alias_recognition':True,'own_alias_named_veterinarians':['A','B','C'],'saved_current_canonical_named_veterinarians':['A','B','C'],'same_actual_city_and_practice_context':True}
    alias=dict(source_id='alias',identity_alias_of='canonical',identity_normalization_proof=proof,fully_verified=False,clinical_source_date=None,reason='parent synthetic fixture, not evidence')
    proof['actual_recognition_text']='Saved canonical alias recognition: parent synthetic fixture, not evidence'
    negatives=[]
    for key,value in [('country','Germany'),('run_id','wrong'),('agent_id','wrong'),('baseline_sha','wrong'),('slot',4),('alias_source_id','wrong'),('canonical_source_id','wrong'),('current_canonical_street','99 Otherstreet'),('current_canonical_city','Othercity'),('current_canonical_postal','00000'),('alias_phone','000'),('permission_scope_adjudicated',False),('source_body_recovery',True),('source_request_for_normalization',True),('own_alias_named_veterinarians',['A']),('previous_saved_canonical_explicit_alias_recognition',False),('previous_saved_canonical_explicit_alias_recognition','false')]:
        x=copy.deepcopy(alias);x['identity_normalization_proof'][key]=value
        negatives.append((key+':'+str(value),[canonical,x]))
    wrong_country=copy.deepcopy(canonical);wrong_country['record']['country']='Germany'
    for key,value in [('slot',5.0),('previous_saved_canonical_explicit_alias_recognition','true'),('actual_recognition_text','')]:
        x=copy.deepcopy(alias);x['identity_normalization_proof'][key]=value
        negatives.append((key+':'+str(value),[canonical,x]))
    negatives.extend([('canonical_country_wrong',[wrong_country,alias]),('duplicate_identity',[canonical,canonical,alias]),('self_reference',[canonical,{**alias,'identity_alias_of':'alias'}]),('missing_target',[alias])])
    rejected=[];accepted=[]
    with patch('builtins.open',side_effect=AssertionError('Unexpected body read')) as read_mock,patch('socket.socket',side_effect=AssertionError('Unexpected network')) as network_mock,patch('urllib.request.urlopen',side_effect=AssertionError('Unexpected URL read')) as url_mock:
        assert len(module.separate_provider_aliases([canonical,alias],identity)[0])==1
        for name,rows in negatives:
            try:module.separate_provider_aliases(rows,identity)
            except (AssertionError,KeyError,ValueError):rejected.append(name)
            else:accepted.append(name)
        calls=dict(body_open=read_mock.call_count,socket=network_mock.call_count,urlopen=url_mock.call_count)
    return dict(kind='PARENT_PURE_ALIAS_NORMALIZATION_NEGATIVE_TESTS',module_path=module_relative,module_sha256=expected,positive_tests=1,negative_tests=len(negatives),rejected=rejected,unexpectedly_accepted=accepted,guarded_IO_calls=calls,result='PASS' if not accepted and not any(calls.values()) else 'FAIL_CLOSED_GAPS',production_modified=False,clinical_source_requests=0)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);parser.add_argument('--module',required=True)
    args=parser.parse_args();print(json.dumps(run(pathlib.Path(args.root),args.module),ensure_ascii=False,indent=2))
