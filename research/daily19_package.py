"""Explicit publication allowlist. The rejected mixed batch stays local only."""
from daily19 import ROOT,RUN,read,write,now
import json,hashlib,subprocess
files=set()
for a in read(RUN/'accepted-master-attempts.json')+[json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]:files.add(a['evidence_file'])
exclude={'attempts.jsonl','full-comparisons.json','checkpoint-022411.json'}
for f in RUN.iterdir():
 if f.is_file() and f.suffix in ['.json','.jsonl','.md'] and f.name not in exclude and f.name!='publication-allowlist.json' and not f.name.startswith('checkpoint-02'):
  files.add(str(f.relative_to(ROOT)))
for f in RUN.glob('checkpoint-*-source-accounting.json'):files.add(str(f.relative_to(ROOT)))
for f in ROOT.glob('research/daily19*.py'):
 if f.name!='daily19_compare.py':files.add(str(f.relative_to(ROOT)))
files.add('research/test_daily19_closure.js');files.add('research/daily19_expected.js');files.add('PROJECT_OPERATIONS.md')
for suffix in ['','-final']:
 if (RUN/('production-byte-readback'+suffix+'.json')).exists():
  for r in read(RUN/('production-byte-readback'+suffix+'.json'))['rows']:
   files.add(r['file']);files.add(r['file']+'.headers')
files.update(['data/trials_base.json','data/source_inventory.json','data/audit_source_coverage.json','data/audit_state.json','data/source_access_restrictions.json','seo/static/matcher/trials.json'])
assert not any('/attempts.jsonl' in f or '/full-comparisons.json' in f for f in files)
entries=[{'path':f,'bytes':(ROOT/f).stat().st_size,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),'git_blob_sha':subprocess.check_output(['git','hash-object',f],cwd=ROOT,text=True).strip()} for f in sorted(files)]
write(RUN/'publication-allowlist.json',{'at':now(),'run_id':RUN.name,'evidence_policy':'Only accepted master-stage output, separate independent protocol requests and accepted Web requests. Rejected fallback batch output and mixed comparisons excluded.','explicit_exclusions':sorted(exclude),'entries':entries})
print('allowed files',len(entries),'bytes',sum(r['bytes'] for r in entries),'current evidence',sum('/evidence/' in r['path'] for r in entries))
