"""Record actual command results, including intentionally incomplete clinical gates."""
from daily19 import ROOT,RUN,write,now
import subprocess,sys
from pathlib import Path
build_root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT
commands=[
 ['python','scripts/audit_preflight.py'],
 ['python','scripts/validate_trials_catalog.py'],
 ['python','scripts/validate_catalog_sanitation.py'],
 ['python','scripts/semantic_dedupe_catalog.py'],
 ['python','scripts/validate_source_inventory.py'],
 ['node','research/test_daily19_closure.js'],
 ['python','scripts/build_static_site.py'],
 ['node','scripts/test_matcher_catalog_loading.js'],
 ['node','scripts/test_matcher_logic.js'],
 ['node','scripts/test_matcher_selection.js'],
 ['python','scripts/test_matcher_selection.py'],
 ['node','scripts/test_matcher_protocol_sources.js'],
 ['python','scripts/validate_production_sync.py'],
 ['python','scripts/validate_audit_receipt.py',str(RUN.relative_to(ROOT)/'receipt-final.json')],
 ['python','scripts/validate_audit_gap_review.py',str(RUN.relative_to(ROOT)/'gap-review.json'),'--receipt',str(RUN.relative_to(ROOT)/'receipt-final.json')],
 ['node','scripts/test_matcher_protocol_sources.js','--reviewed-since=2026-10-16T18:59:47.653454Z','--require-full-review'],
 ['python','scripts/check_evidence_keys.py'],
 ['python','scripts/audit_preflight.py']]
results=[]
if (RUN/'validators.json').exists():
 from daily19 import read
 results=read(RUN/'validators.json')
for i,c in enumerate(commands):
 cwd=build_root if i in [0,6,7,8,9,10,11,12,15,17] else ROOT
 start=now();p=subprocess.run(c,cwd=cwd,text=True,capture_output=True)
 r={'command':c,'cwd':str(cwd),'started_at':start,'finished_at':now(),'exit_code':p.returncode,'output':p.stdout+p.stderr}
 results.append(r);write(RUN/'validators.json',results)
 print(i,'PASS' if not p.returncode else 'NONZERO',c,'\n',r['output'][-1500:],flush=True)
 if p.returncode and i==6:break
