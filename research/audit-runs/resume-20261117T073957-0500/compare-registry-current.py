from pathlib import Path
from collections import Counter
import json,sys,re
r=Path(sys.argv[1]);o=Path('research/audit-runs/daily-20261117T030023-0500')
def read(p): return json.loads(p.read_text())
ks=['34f4affa7b11a9cba24c','6964147c732220816f6b']
payload=[read(r/'evidence'/f'{k}.txt') for k in ks]
raw=[z for p in payload for z in p['studies']]
assert len(raw)==len({x['id'] for x in raw})==payload[0]['total']==payload[1]['total']
old={x['id']:x for x in read(o/'avma-overview.json')['cards']}
d={x['id']:x for x in raw}
old_req={x.get('registry_vct'): x for x in read(r/'morning-accounting'/'execution-review.json')['leads'] if x.get('registry_vct')}
changed=[]
for bid in sorted(set(d)|set(old)):
 now=d.get(bid,{})
 prev=old.get(bid,{})
 diff={k:{'prior':prev.get(k),'current':now.get(k)} for k in ['vct_code','name','status','absolute_url'] if prev.get(k)!=now.get(k)}
 if diff: changed.append({'registry_id':bid,'changes':diff})
focus=[]
for x in raw:
 if x['status']!='Recruiting':continue
 tags=[i['label'] for i in x.get('visible_sc_items',[])]
 if not (any(t in tags for t in ('Oncology','Cancer')) or re.search(r'oncol|tumou?r|sarcom|lympho|carcin|leukem|melan|gliom|cancer|mast cell',x['name'],re.I)):continue
 v=x.get('vct_code')
 a=old_req.get(v,{})
 focus.append({k:x[k] for k in ['id','name','vct_code','status','absolute_url']}|{'tags':tags,'title_or_registry_identity_prior_visible':bool(a),'morning_decision':a.get('disposition'),'morning_decision_reason':a.get('reason'),'exact_canonical_ids_if_previously_reconciled':a.get('canonical_ids',[])})
out={'fresh_gallery_ref':str(r/'source-route-evidence.json'),'fresh_gallery_evidence_keys':ks,'gallery_counts':{'declared':payload[0]['total'],'distinct':len(d),'page_sizes':[len(x['studies']) for x in payload],'record_statuses':dict(Counter(z['status'] for z in raw))},'changed_comparable_card_fields':changed,'attention':{'recruiting_candidates':len(focus),'exact_vct_in_saved_morning_leads':sum(x['title_or_registry_identity_prior_visible'] for x in focus)},'individual_recruiting_candidates':focus}
(r/'avma-comparison-continuation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(out['gallery_counts'],out['attention'],'changed',len(changed))
for x in focus:
 if not x['title_or_registry_identity_prior_visible']:print(x['vct_code'],x['name'],x['absolute_url'])
