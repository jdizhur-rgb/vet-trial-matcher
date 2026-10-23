"""Actual finite local validators and clean build, preserving intentionally strict gates."""
from daily23 import ROOT,RUN,read,write,now
import subprocess,sys,tempfile
from pathlib import Path
if len(sys.argv)>1:build=Path(sys.argv[1])
else:
 build=Path(tempfile.mkdtemp(prefix='trial-build-',dir=ROOT.parent))
 subprocess.run(['git','checkout-index','--all','--prefix',str(build)+'/'],cwd=ROOT,check=True)
 subprocess.run(['git','init','--quiet'],cwd=build,check=True)
 subprocess.run(['git','add','--all'],cwd=build,check=True)
write(RUN/'build-root.json',{'path':str(build),'at':now(),'method':'Fresh isolated export of staged reviewed tree; no shared seo/site output'})
commands=[
 ['python','scripts/validate_trials_catalog.py'],['python','scripts/validate_catalog_sanitation.py'],['python','scripts/semantic_dedupe_catalog.py'],['python','scripts/validate_source_inventory.py'],['node','research/test_daily20_status.js'],['python','scripts/build_static_site.py'],['node','scripts/test_matcher_catalog_loading.js'],['node','scripts/test_matcher_logic.js'],['node','scripts/test_matcher_selection.js'],['python','scripts/test_matcher_selection.py'],['node','scripts/test_matcher_protocol_sources.js'],['python','scripts/validate_production_sync.py'],['node','scripts/test_matcher_protocol_sources.js','--reviewed-since=2026-10-16T18:59:47.653454Z','--require-full-review'],['python','scripts/validate_audit_receipt.py',str(RUN.relative_to(ROOT)/'receipt-final.json')],['python','scripts/validate_audit_gap_review.py',str(RUN.relative_to(ROOT)/'gap-review.json'),'--receipt',str(RUN.relative_to(ROOT)/'receipt-final.json')],['python','scripts/check_evidence_keys.py'],['python','scripts/audit_preflight.py'],['git','diff','--check']]
results=read(RUN/'validators.json') if (RUN/'validators.json').exists() else []
for c in commands:
 cwd=ROOT if 'validate_audit_receipt.py' in c[1] or 'validate_audit_gap_review.py' in c[1] or 'check_evidence_keys.py' in c[1] else build
 at=now();p=subprocess.run(c,cwd=cwd,text=True,capture_output=True,timeout=600)
 r=dict(command=c,cwd=str(cwd),started_at=at,finished_at=now(),exit_code=p.returncode,output=p.stdout+p.stderr);results.append(r);write(RUN/'validators.json',results)
 print(c,'EXIT',p.returncode,r['output'][-2400:],flush=True)
 if p.returncode and c[1]=='scripts/build_static_site.py':raise SystemExit(p.returncode)
