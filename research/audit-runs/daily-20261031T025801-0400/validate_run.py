from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,subprocess
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
rel=str(R.relative_to(ROOT))
jobs=[['python','scripts/validate_catalog_sanitation.py'],['python','scripts/validate_trials_catalog.py'],['python','scripts/validate_source_inventory.py'],['python','scripts/check_evidence_keys.py'],['python','scripts/test_matcher_selection.py'],['node','scripts/test_matcher_protocol_sources.js'],['node','scripts/test_matcher_protocol_sources.js','--require-full-review'],['python','scripts/build_static_site.py'],['node','scripts/test_matcher_catalog_loading.js'],['node','scripts/test_matcher_logic.js'],['python','scripts/validate_production_sync.py'],['python','scripts/validate_audit_receipt.py',rel+'/receipt-final.json'],['python','scripts/validate_audit_gap_review.py',rel+'/gap-review.json','--receipt',rel+'/receipt-final.json'],['python','scripts/validate_repository_hygiene.py']]
results=[];care=ROOT/'data/oncology_center_audit.json';saved=care.read_bytes()if care.exists()else None
for i,cmd in enumerate(jobs):
 at=now();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);ended=now();f=R/f'validation-{i:02}.txt';f.write_text(p.stdout+p.stderr)
 if cmd==['python','scripts/build_static_site.py']and saved is not None:care.write_bytes(saved)
 results.append({'command':cmd,'started_at':at,'ended_at':ended,'exit_code':p.returncode,'output':str(f.relative_to(ROOT))})
 print(json.dumps({'command':' '.join(cmd),'exit_code':p.returncode,'last_output':(p.stdout+p.stderr)[-700:]}),flush=True)
(R/'validation-results.json').write_text(json.dumps(results,indent=2)+'\n')
