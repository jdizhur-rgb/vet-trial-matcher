"""Run publication gates and preserve actual command outputs for one intake."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess,json
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
commands=[
 ['python','scripts/validate_trials_catalog.py'],
 ['python','scripts/validate_catalog_sanitation.py'],
 ['python','scripts/semantic_dedupe_catalog.py'],
 ['python','scripts/build_static_site.py'],
 ['node','scripts/test_matcher_catalog_loading.js'],
 ['node','scripts/test_matcher_logic.js'],
 ['node','scripts/test_matcher_selection.js'],
 ['python','scripts/test_matcher_selection.py'],
 ['python','scripts/validate_production_sync.py'],
 ['python','scripts/validate_source_inventory.py'],
 ['python','scripts/check_evidence_keys.py'],
 ['git','diff','--check'],
]
logs=[]
for command in commands:
 start=now();p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
 logs.append(dict(command=command,started_at=start,finished_at=now(),exit_code=p.returncode,output=p.stdout+p.stderr))
 (RUN/'validators.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
 print(' '.join(command), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print((p.stdout+p.stderr)[-5000:]);raise SystemExit(p.returncode)
print('ALL_PUBLICATION_GATES_PASS',flush=True)
