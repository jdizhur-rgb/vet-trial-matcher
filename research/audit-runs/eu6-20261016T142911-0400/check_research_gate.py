"""Fail closed before site integration; research-only backups are independent."""
import hashlib,json,pathlib,sys
RUN=pathlib.Path(__file__).resolve().parent
def check():
    assignments=json.loads((RUN/'assignments.json').read_text())['assignments']
    assert len(assignments)==6,'Six fixed country assignments required'
    issues=[]
    for item in assignments:
        path=RUN/f"worker-acceptance-{item['slot']}.json"
        if not path.exists():
            issues.append({'slot':item['slot'],'country':item['country'],'reason':'No independent parent acceptance receipt'})
            continue
        v=json.loads(path.read_text())
        try:
            for key in ['run_id','slot','country','baseline_sha','agent_id']:
                assert v[key]==item[key],f'{key} mismatch'
            assert v.get('parent_accepted') is True,'Parent acceptance missing'
            assert v.get('research_complete') is True,'Research unfinished'
            assert v.get('accessible_remaining_count')==0,'Available research frontier remains'
            assert v.get('full_report_content_reviewed') is True,'Substantive Russian report not reviewed'
            assert v.get('evidence_identity_counter_reviewed') is True,'Evidence/identity/count review missing'
            report=(RUN/v['frozen_report_relative_path']).resolve()
            assert report.is_relative_to((RUN/f"worker-{item['slot']}").resolve()),'Wrong worker report scope'
            assert hashlib.sha256(report.read_bytes()).hexdigest()==v['frozen_report_sha256'],'Accepted report changed'
            assert v.get('remote_backup_verified_sha'),'No verified remote research checkpoint'
        except (AssertionError,KeyError,OSError) as e:
            issues.append({'slot':item['slot'],'country':item['country'],'reason':str(e)})
    print(json.dumps({'run_id':RUN.name,'site_integration_allowed':not issues,'research_only_backup_allowed':True,'issues':issues},ensure_ascii=False))
    return 1 if issues else 0
if __name__=='__main__':sys.exit(check())
