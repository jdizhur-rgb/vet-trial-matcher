import subprocess,json,sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2];(P/'validators').mkdir(exist_ok=True)
commands=[
 ['python','scripts/validate_audit_receipt.py',str(P/'receipt-final.json')],
 ['python','scripts/validate_audit_gap_review.py',str(P/'gap-review.json'),'--receipt',str(P/'receipt-final.json')],
 ['python','scripts/validate_catalog_sanitation.py'],
 ['python','scripts/validate_trials_catalog.py'],
 ['python','scripts/validate_source_inventory.py'],
 ['python','scripts/validate_repository_hygiene.py'],
 ['python','scripts/test_matcher_selection.py'],
 ['node','scripts/test_matcher_selection.js'],
 ['node','scripts/test_matcher_protocol_sources.js'],
 ['node','scripts/test_matcher_catalog_loading.js'],
 ['python','scripts/build_static_site.py'],
 ['node','scripts/test_matcher_logic.js'],
 ['python','scripts/validate_production_sync.py'],
 ['python','scripts/test_audit_gap_review.py'],
 ['python','scripts/check_evidence_keys.py','--redact',str(P)],
 ['python','scripts/check_evidence_keys.py']]
results=[]
for i,c in enumerate(commands):
 at=datetime.now(ZoneInfo('America/New_York')).isoformat();p=subprocess.run(c,cwd=ROOT,capture_output=True,text=True);log=P/'validators'/f'{i:02d}-{Path(c[1]).stem}.txt';log.write_text(p.stdout+p.stderr);row={'command':c,'started_at':at,'ended_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'exit_code':p.returncode,'log':str(log.relative_to(ROOT)),'status':'PASS' if p.returncode==0 else 'INCOMPLETE' if i==0 else 'FAIL'};results.append(row);print(json.dumps(row),flush=True)
 (P/'validators.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
