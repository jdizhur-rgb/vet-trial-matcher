"""Reuse tested finite transport, with new-run state and no inherited completion."""
import importlib.util, json, sys, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
PRIOR=P.parent/'daily-20261015T030225-0400'
spec=importlib.util.spec_from_file_location('finite_transport',PRIOR/'run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.RUN=P;m.ROOT=ROOT;m.RAW=ROOT.parent/'raw-evidence'/P.name
def checkpoint():
    rows=m.read(P/'reviews.json') if (P/'reviews.json').exists() else []
    done={r['source_id'] for r in rows if r.get('processing_complete') is True}
    inv=m.read(P/'before-source_inventory.json')['sources']
    m.write(P/('checkpoint-'+m.datetime.now(m.TZ).strftime('%H%M%S')+'.json'),{
        'at':m.now(),'run_id':P.name,'reviewed':len(rows),'processing_complete':len(done),
        'remaining_source_ids':[s['id'] for s in inv if s['id'] not in done],
        'discovery_matrix': 'discovery-matrix.json' if (P/'discovery-matrix.json').exists() else None,
        'deadline':'2026-10-16T06:00:00-04:00',
        'note':'Fetch and old decisions are not current completed reconciliation.'})
m.checkpoint=checkpoint
if sys.argv[1]=='init':
    P.mkdir(exist_ok=True)
    for name in ('source_inventory.json','trials_base.json','audit_state.json','audit_source_coverage.json'):
        (P/('before-'+name)).write_bytes((ROOT/'data'/name).read_bytes())
    inv=m.read(P/'before-source_inventory.json')['sources'];cat=m.read(P/'before-trials_base.json');pub=m.current_public(cat)
    m.write(P/'baseline.json',{'run_id':P.name,'started_at':'2026-10-16T02:56:51-04:00','snapshot_at':m.now(),
        'base_main_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_ids':[s['id'] for s in inv],
        'counts':{'canonical':len(cat),'public':len(pub),'treatment':sum(r.get('study_type','treatment')=='treatment' for r in pub),'other_access':sum(r.get('study_type')=='other_treatment_access' for r in pub),'sources':len(inv)},
        'sha256':{n:m.digest(ROOT/'data'/n) for n in ('trials_base.json','source_inventory.json','audit_state.json','audit_source_coverage.json')}})
    m.write(P/'reviews.json',[])
    prior=m.read(PRIOR/'reviews.json');gates=[r for r in prior if r['source_result']=='not_checked']
    m.write(P/'inherited-gates.json',{'origin':str(PRIOR.relative_to(ROOT)),'rows':gates,'new_visit':False})
    denied={s['master_url'] for s in inv if s['id'] in {r['source_id'] for r in gates}}
    m.write(P/'plan-masters.json',[{'source_id':s['id'],'url':s['master_url'],'route':'master'} for s in inv if s['master_url'] not in denied])
    checkpoint();print(json.dumps(m.read(P/'baseline.json')['counts']))
elif sys.argv[1]=='checkpoint':checkpoint()
else:m.main()
