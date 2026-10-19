"""Independent permitted individual pages; does not consume rejected batch output."""
import types,concurrent.futures,json,sys
from daily19 import ROOT,RUN,OLD,read,write,m
source=(OLD/'run.py').read_text().replace("'attempts.jsonl'","'protocol-attempts.jsonl'").replace("'new-denials.jsonl'","'protocol-denials.jsonl'")
p=types.ModuleType('independent_protocol_retrieval');p.__file__=str(OLD/'run.py');exec(compile(source,p.__file__,'exec'),p.__dict__)
p.ROOT=ROOT;p.RUN=RUN;p.RAW=ROOT.parent/'raw-evidence'/RUN.name
def checkpoint():pass
p.checkpoint=checkpoint
if __name__=='__main__':
 inv=read(RUN/'before-source_inventory.json')['sources'];public=read(RUN/'public-frozen.json');denied=p.known_denials()|{p.route_key(r['url']) for r in read(RUN/'web-denials.json')}
 used={p.route_key(u) for s in inv for u in [s['master_url']]+s.get('fallback_urls',[])}
 plan=[];blocked=[]
 for r in public:
  u=r.get('source_url') or r['url'];k=p.route_key(u);item={'source_id':'protocol:'+r['id'],'url':u,'route':'individual_primary'}
  if k in denied:blocked.append(item)
  elif k not in used:plan.append(item);used.add(k)
 write(RUN/'independent-protocol-plan.json',plan);write(RUN/'independent-protocol-blocked.json',blocked)
 print('independent allowed pages',len(plan),'blocked protocols',len(blocked),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(p.get,plan))
