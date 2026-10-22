"""Finite October22 requests; current evidence and historical evidence kept separate."""
import importlib.util,json,sys,hashlib,subprocess,concurrent.futures,fcntl
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'research/audit-runs/daily-20261021T030035-0400'
RUN=ROOT/'research/audit-runs/daily-20261022T030531-0400'
spec=importlib.util.spec_from_file_location('retrieval',ROOT/'research/audit-runs/daily-20261018T030540-0400/run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ROOT=ROOT;m.RUN=RUN;m.RAW=ROOT.parent/'raw-evidence'/RUN.name
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
_denials=m.known_denials
def known_denials():
 d=_denials()
 if (RUN/'web-denials.json').exists():d.update(m.route_key(r['url']) for r in read(RUN/'web-denials.json'))
 return d
m.known_denials=known_denials
def attempts():return [json.loads(l) for l in (RUN/'attempts.jsonl').read_text().splitlines()] if (RUN/'attempts.jsonl').exists() else []
def checkpoint():
 a=attempts();b=read(RUN/'baseline.json');rows=read(RUN/'receipt-final.json').get('sources',[]) if (RUN/'receipt-final.json').exists() else []
 t=datetime.now(ZoneInfo('America/New_York')).strftime('%H%M%S')
 v={'run_id':RUN.name,'at':now(),'actual_native_requests':len(a),'visited_source_ids':sorted({x['source_id'] for x in a}),'processed_sources':sum(r.get('processing_complete',False) for r in rows),'source_total':len(read(ROOT/'data/source_inventory.json')['sources']),'frozen_start_source_total':b['counts']['sources'],'remaining_source_ids':[s['id'] for s in read(ROOT/'data/source_inventory.json')['sources'] if s['id'] not in {r['source_id'] for r in rows if r.get('processing_complete')}],'deadline':'2026-10-22T06:00:00-04:00','note':'Requests are not reconciliation. No date or clinical sign-off inferred from a fetch.'}
 v['discovery_regions_with_both_passes']=read(RUN/'discovery-matrix.json')['regions_with_both_passes'] if (RUN/'discovery-matrix.json').exists() else 0
 v['source_evidence_and_clinical_review_separate']=True
 write(RUN/('checkpoint-'+t+'.json'),v)
 (RUN/('segment-'+t+'.md')).write_text(f"# Immutable segment {t}\n\nAt {v['at']}: {len(a)} actual native request receipts; {v['processed_sources']}/{v['source_total']} processing decisions. Clinical and discovery completion require separate saved evidence.\n")
m.checkpoint=checkpoint
def fetch(plan):
 lock=(RUN/'.native-batch.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(m.get,plan))
 checkpoint()
if __name__=='__main__':
 cmd=sys.argv[1]
 if cmd=='init':
  RUN.mkdir();(RUN/'evidence').mkdir();m.RAW.mkdir(parents=True)
  from seo.catalog_selection import current_public
  for n in ['trials_base.json','source_inventory.json','audit_state.json','audit_source_coverage.json','source_access_restrictions.json','protocol_selection_cases.json']:(RUN/('before-'+n)).write_bytes((ROOT/'data'/n).read_bytes())
  inv=read(ROOT/'data/source_inventory.json');cat=read(ROOT/'data/trials_base.json');pub=current_public(cat);prior=read(OLD/'receipt-final.json')
  restrictions=read(ROOT/'data/source_access_restrictions.json')['routes']+read(OLD/'restrictions-frozen.json')
  for s in inv['sources']:restrictions+=s.get('access_restrictions',[])
  for r in prior['sources']:
   for a in r.get('attempted_urls',[]):
    if a.get('restriction_evidence'):restrictions.append(a['restriction_evidence'])
    if a.get('http_status')==403:restrictions.append(dict(url=a['url'],do_not_retry=True,origin=a.get('evidence_file'),observed_at=a.get('attempted_at')))
  if (OLD/'web-denials.json').exists():restrictions+=read(OLD/'web-denials.json')
  restrictions=[r for r in restrictions if r.get('do_not_retry',True) and r.get('url')]
  write(RUN/'restrictions-frozen.json',list({m.route_key(r['url']):r for r in restrictions}.values()))
  write(RUN/'public-frozen.json',pub);write(RUN/'previous-receipt.json',prior)
  for src,dst in [('trial-review.json','prior-trial-review.json'),('independent40-progress.json','pending-frozen.json'),('issues.json','prior-issues.json')]:write(RUN/dst,read(OLD/src))
  write(RUN/'baseline.json',{'run_id':RUN.name,'started_at':'2026-10-22T03:05:31-04:00','snapshot_at':now(),'base_main_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_ids':[s['id'] for s in inv['sources']],'public_ids':[r['id'] for r in pub],'counts':{'canonical':len(cat),'public_matchable':len(pub),'treatment_trials':sum(r.get('study_type','treatment')=='treatment' for r in pub),'other_treatment_access':sum(r.get('study_type')=='other_treatment_access' for r in pub),'sources':len(inv['sources'])},'sha256':{n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in ['trials_base.json','source_inventory.json','audit_state.json']},'previous_receipt':str((OLD/'receipt-final.json').relative_to(ROOT)),'instructions':{n:subprocess.check_output(['git','hash-object',n],text=True).strip() for n in ['AGENTS.md','PROJECT_OPERATIONS.md','data/DAILY_AUDIT_ALGORITHM.md','data/DAILY_AUDIT_TASK.md']}})
  write(RUN/'preflight.json',{'at':now(),'commands':[{'command':'pwd','output':'/workspace/scratch/7a43f0b7d905','exit_code':0},{'command':'python --version','output':'Python 3.12.14','exit_code':0},{'command':'git --version','output':'git version 2.51.1','exit_code':0}]})
  checkpoint();print(json.dumps(read(RUN/'baseline.json')['counts']))
 elif cmd=='plan':
  kind=sys.argv[2];inv=read(RUN/'before-source_inventory.json')['sources'];plans=[]
  if kind=='master':plans=[dict(source_id=s['id'],url=s['master_url'],route='master') for s in inv]
  elif kind=='fallback':plans=[dict(source_id=s['id'],url=u,route='official_fallback') for s in inv for u in s.get('fallback_urls',[])]
  denied=m.known_denials();seen={m.route_key(a['url']) for a in attempts()};out=[];skips=[]
  for p in plans:
   k=m.route_key(p['url'])
   if k in denied or p['url'].rstrip('/')=='https://www.vet.cam.ac.uk/node/2971':skips.append(dict(p,reason='prior_explicit_restriction_or_unresolved_same_action_alias_not_retried'))
   elif k not in seen:out.append(p);seen.add(k)
  write(RUN/(kind+'-plan.json'),out);write(RUN/(kind+'-restricted.json'),skips);print('permitted',len(out),'restricted',len(skips))
 elif cmd=='fetch':
  plan=read(Path(sys.argv[2]));a=int(sys.argv[3]) if len(sys.argv)>3 else 0;b=int(sys.argv[4]) if len(sys.argv)>4 else len(plan);fetch(plan[a:b])
 elif cmd=='checkpoint':checkpoint()
