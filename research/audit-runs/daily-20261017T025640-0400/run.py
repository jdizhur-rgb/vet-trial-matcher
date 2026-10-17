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
        'deadline':'2026-10-17T06:00:00-04:00',
        'note':'Fetch and old decisions are not current completed reconciliation.'})
m.checkpoint=checkpoint
# Guard every future retrieval, including metadata from later independent protocol reviews.
from urllib.parse import urlsplit, unquote, parse_qsl, urlencode
def route_key(url):
    v=urlsplit(url)
    host=(v.hostname or '').lower().removeprefix('www.')
    return (host,unquote(v.path).rstrip('/'),tuple(sorted(parse_qsl(v.query,keep_blank_values=True))))
def known_denials():
    inv=m.read(ROOT/'data/source_inventory.json')['sources']
    denied={route_key(r['url']) for s in inv for r in s.get('access_restrictions',[]) if r.get('do_not_retry')}
    extra=ROOT/'data/source_access_restrictions.json'
    if extra.exists():denied.update(route_key(r['url']) for r in m.read(extra)['routes'] if r.get('do_not_retry'))
    inherited=P/'inherited-gates.json'
    if inherited.exists():
        g=m.read(inherited);denied.update(route_key(u) for u in g['denied_urls'])
        # Whole-source prior narrative explicitly identifies these masters as denied;
        # a missing serialized original master request must never be interpreted as permission.
        denied.update(route_key(r['master_url']) for r in g['rows'] if r.get('master_url'))
    return denied
original_get=m.get
def guarded_get(item):
    if route_key(item['url']) in known_denials():
        with m.LOCK:
            with (P/'skipped-restricted-routes.jsonl').open('a') as f:f.write(json.dumps({**item,'at':m.now(),'result':'known_denial_not_requested'})+'\n')
        return
    return original_get(item)
m.get=guarded_get
if sys.argv[1]=='init':
    P.mkdir(exist_ok=True)
    for name in ('source_inventory.json','trials_base.json','audit_state.json','audit_source_coverage.json'):
        (P/('before-'+name)).write_bytes((ROOT/'data'/name).read_bytes())
    inv=m.read(P/'before-source_inventory.json')['sources'];cat=m.read(P/'before-trials_base.json');pub=m.current_public(cat)
    m.write(P/'baseline.json',{'run_id':P.name,'started_at':'2026-10-17T02:56:40.839128-04:00','snapshot_at':m.now(),
        'base_main_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_ids':[s['id'] for s in inv],
        'counts':{'canonical':len(cat),'public':len(pub),'treatment':sum(r.get('study_type','treatment')=='treatment' for r in pub),'other_access':sum(r.get('study_type')=='other_treatment_access' for r in pub),'sources':len(inv)},
        'sha256':{n:m.digest(ROOT/'data'/n) for n in ('trials_base.json','source_inventory.json','audit_state.json','audit_source_coverage.json')}})
    m.write(P/'reviews.json',[])
    prior=m.read(PRIOR/'reviews.json');gates=[r for r in prior if r['source_result']=='not_checked']
    m.write(P/'inherited-gates.json',{'origin':str(PRIOR.relative_to(ROOT)),'rows':gates,'new_visit':False})
    denied={s['master_url'] for s in inv if s['id'] in {r['source_id'] for r in gates}}
    denied.update(a['url'] for s in inv for a in s.get('access_restrictions',[]) if a.get('do_not_retry'))
    denied.update(a['url'] for s in inv for a in s.get('last_attempts',[]) if a.get('http_status')==403 or a.get('result')=='explicit_denial')
    m.write(P/'plan-masters.json',[{'source_id':s['id'],'url':s['master_url'],'route':'master'} for s in inv if s['master_url'] not in denied])
    checkpoint();print(json.dumps(m.read(P/'baseline.json')['counts']))
elif sys.argv[1]=='checkpoint':checkpoint()
else:m.main()
