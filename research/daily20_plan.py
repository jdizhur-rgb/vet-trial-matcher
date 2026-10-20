"""Single finite protocol/API plan, exact restrictions checked at dispatch."""
from daily20 import ROOT,RUN,OLD,read,write,m,attempts
import json
public=read(RUN/'public-frozen.json');used={m.route_key(a['url']) for a in attempts()}|{m.route_key(a['url']) for a in read(RUN/'fallback-plan.json')};denied=m.known_denials();plan=[];skips=[]
for r in public:
 u=r.get('source_url') or r['url'];p={'source_id':'protocol:'+r['id'],'url':u,'route':'individual_primary'};k=m.route_key(u)
 if k in denied:skips.append(dict(p,reason='known_denial_not_requested'))
 elif k not in used:plan.append(p);used.add(k)
old=[json.loads(l) for l in (OLD/'protocol-attempts.jsonl').read_text().splitlines()]
for a in old:
 u=a['url'];k=m.route_key(u)
 if ('/studies/search/json/' in u or '/api/trials?' in u) and k not in used and k not in denied:
  plan.append(dict(source_id=a['source_id'],url=u,route='whole_public_paginated_roster'));used.add(k)
for sid,u in [('sponsor-elias-clinical-studies','https://eliasanimalhealth.com/clinical-studies/eci-combined-with-chemotherapy/'),('sponsor-vmd-sciences-clinical-studies','https://www.vmdsciences.com/accessstrategies'),('discovery:uf-pain','https://research.vetmed.ufl.edu/post-operative-pain-phenotypes-in-dogs-undergoing-abdominal-surgery-versus-a-ct-mri-scan/'),('discovery:lmu-rehab','https://cms-cdn.lmu.de/media/08-vetmed/fakultaetswebsite-website/downloads/flyer-zur-studie-2026.pdf')]:
 if m.route_key(u) not in used and m.route_key(u) not in denied:plan.append(dict(source_id=sid,url=u,route='new_primary_signal'));used.add(m.route_key(u))
write(RUN/'protocol-plan.json',plan);write(RUN/'protocol-restricted.json',skips);print('protocol/API allowed',len(plan),'blocked',len(skips))
