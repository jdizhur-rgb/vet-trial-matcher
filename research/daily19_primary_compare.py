"""Compare only separately authorized protocol output, never rejected fallback output."""
from daily19 import ROOT,RUN,OLD,read,write,m
import json,difflib,collections
old=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
prior={m.route_key(a['url']):a for a in old if a.get('http_status')==200 and a.get('text_length',0)>100}
rows=[]
for a in [json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]:
 b=prior.get(m.route_key(a['url']));x=read(ROOT/a['evidence_file']);y=read(ROOT/b['evidence_file']) if b else None
 same=bool(y and x['text']==y['text']);links=bool(y and sorted(z['url'] for z in x['links'])==sorted(z['url'] for z in y['links']))
 row={'trial_id':a['source_id'].removeprefix('protocol:'),'url':a['url'],'attempt':a,'previous_attempt':b,'same_full_text':same,'same_full_links':links,'diff':None if same or not y else '\n'.join(difflib.unified_diff(y['text'].splitlines(),x['text'].splitlines()))}
 rows.append(row)
 if a.get('http_status')==200 and a.get('text_length',0)>500:
  print(row['trial_id'],'SAME' if same else 'CHANGED','LINKS',links,'DIFF',str(row['diff'])[:3000])
write(RUN/'individual-full-comparisons.json',rows)
