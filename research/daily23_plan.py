"""Single finite protocol/API plan, exact restrictions checked at dispatch."""
from daily23 import ROOT,RUN,OLD,read,write,m,attempts
import json
public=read(RUN/'public-frozen.json');used={m.route_key(a['url']) for a in read(RUN/'master-plan.json')}|{m.route_key(a['url']) for a in attempts()}|{m.route_key(a['url']) for a in read(RUN/'fallback-plan.json')};denied=m.known_denials();plan=[];skips=[]
for r in public:
 u=r.get('source_url') or r['url'];p={'source_id':'protocol:'+r['id'],'url':u,'route':'individual_primary'};k=m.route_key(u)
 if k in denied:skips.append(dict(p,reason='known_denial_not_requested'))
 elif k not in used:plan.append(p);used.add(k)
old=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
for a in old:
 u=a['url'];k=m.route_key(u)
 if ('/studies/search/json/' in u or '/api/trials?' in u or '140763' in u) and k not in used and k not in denied:
  plan.append(dict(source_id=a['source_id'],url=u,route='whole_public_paginated_roster'));used.add(k)
write(RUN/'protocol-plan.json',plan);write(RUN/'protocol-restricted.json',skips);print('protocol/API allowed',len(plan),'blocked',len(skips))
