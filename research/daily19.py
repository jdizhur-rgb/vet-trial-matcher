"""Finite audit retrieval. Evidence retrieval never implies clinical completion."""
import importlib.util,json,sys,hashlib,subprocess,concurrent.futures,fcntl
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'research/audit-runs/daily-20261018T030540-0400'
RUN=ROOT/'research/audit-runs/daily-20261019T032107-0400'
spec=importlib.util.spec_from_file_location('retrieval',OLD/'run.py'); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ROOT=ROOT;m.RUN=RUN;m.RAW=ROOT.parent/'raw-evidence'/RUN.name
_denials=m.known_denials
def known_denials():
 result=_denials()
 if (RUN/'web-denials.json').exists():result.update(m.route_key(r['url']) for r in read(RUN/'web-denials.json'))
 return result
m.known_denials=known_denials
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def checkpoint():
 a=[json.loads(l) for l in (RUN/'attempts.jsonl').read_text().splitlines()] if (RUN/'attempts.jsonl').exists() else []
 write(RUN/('checkpoint-'+datetime.now().strftime('%H%M%S')+'.json'),{'run_id':RUN.name,'at':now(),'actual_native_requests':len(a),'visited_source_ids':sorted({x['source_id'] for x in a}),'source_reconciliation_complete':0,'discovery_regions_complete':0,'note':'Requests are not reconciliation; remaining work retained.'})
m.checkpoint=checkpoint
if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='init':
  RUN.mkdir();(RUN/'evidence').mkdir();m.RAW.mkdir(parents=True)
  from seo.catalog_selection import current_public
  for n in ['trials_base.json','source_inventory.json','audit_state.json','audit_source_coverage.json','source_access_restrictions.json']:(RUN/('before-'+n)).write_bytes((ROOT/'data'/n).read_bytes())
  inv=read(ROOT/'data/source_inventory.json');cat=read(ROOT/'data/trials_base.json');pub=current_public(cat)
  restrictions=read(ROOT/'data/source_access_restrictions.json')['routes']+read(OLD/'restrictions-frozen.json')
  if (OLD/'new-denials.jsonl').exists():restrictions += [json.loads(l) for l in (OLD/'new-denials.jsonl').read_text().splitlines()]
  for s in inv['sources']:restrictions+=s.get('access_restrictions',[])
  restrictions=[r for r in restrictions if r.get('do_not_retry',True) and r.get('url')]
  write(RUN/'restrictions-frozen.json',list({m.route_key(r['url']):r for r in restrictions}.values()))
  write(RUN/'public-frozen.json',pub)
  prior=read(OLD/'trial-review.json');pending=read(OLD/'independent40-progress.json')
  write(RUN/'prior-trial-review.json',prior);write(RUN/'pending-frozen.json',pending)
  write(RUN/'baseline.json',{'run_id':RUN.name,'started_at':'2026-10-19T03:21:07-04:00','snapshot_at':now(),'base_main_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_ids':[s['id'] for s in inv['sources']],'public_ids':[r['id'] for r in pub],'counts':{'canonical':len(cat),'public_matchable':len(pub),'treatment_trials':sum(r.get('study_type','treatment')=='treatment' for r in pub),'other_treatment_access':sum(r.get('study_type')=='other_treatment_access' for r in pub),'sources':len(inv['sources'])},'sha256':{n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in ['trials_base.json','source_inventory.json','audit_state.json']},'previous_receipt':str((OLD/'receipt-final.json').relative_to(ROOT))})
  write(RUN/'previous-receipt.json',read(OLD/'receipt-final.json'))
  for n in ['AGENTS.md','PROJECT_OPERATIONS.md','data/DAILY_AUDIT_ALGORITHM.md']:
   local=subprocess.check_output(['git','hash-object',n],text=True).strip();print(n,local)
  checkpoint();print(json.dumps(read(RUN/'baseline.json')['counts']))
 elif cmd=='plan':
  inv=read(RUN/'before-source_inventory.json')['sources'];plan=[]
  if sys.argv[2]=='master':plan=[{'source_id':s['id'],'url':s['master_url'],'route':'master'} for s in inv]
  elif sys.argv[2]=='fallback':plan=[{'source_id':s['id'],'url':u,'route':'official_fallback'} for s in inv for u in s.get('fallback_urls',[])]
  elif sys.argv[2]=='protocol':
   plan=[{'source_id':'protocol:'+r['id'],'url':r.get('source_url') or r['url'],'route':'individual_primary'} for r in read(RUN/'public-frozen.json')]
  denied=m.known_denials();seen={m.route_key(json.loads(l)['url']) for l in (RUN/'attempts.jsonl').read_text().splitlines()} if (RUN/'attempts.jsonl').exists() else set();out=[];skips=[]
  for p in plan:
   k=m.route_key(p['url'])
   if k in denied:skips.append(dict(p,reason='inherited_explicit_restriction_not_retried'))
   elif k not in seen:out.append(p);seen.add(k)
  write(RUN/(sys.argv[2]+'-plan.json'),out);write(RUN/(sys.argv[2]+'-restricted.json'),skips);print('permitted',len(out),'restricted',len(skips))
 elif cmd=='fetch':
  batch_lock=(RUN/'.native-batch.lock').open('w');fcntl.flock(batch_lock,fcntl.LOCK_EX)
  plan=read(Path(sys.argv[2]));a=int(sys.argv[3]) if len(sys.argv)>3 else 0;b=int(sys.argv[4]) if len(sys.argv)>4 else len(plan)
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(m.get,plan[a:b]))
  checkpoint()
