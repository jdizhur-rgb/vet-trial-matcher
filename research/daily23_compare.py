"""Full current text/link comparisons to accepted historical evidence only."""
from daily23 import ROOT,RUN,OLD,read,write,m,attempts
import json,difflib,sys
prior=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
by={m.route_key(a['url']):a for a in prior if a.get('http_status')==200 and a.get('text_length',0)>100}
rows=[]
def linkset(x):return sorted(z['url'].split('#')[0] if '/cdn-cgi/l/email-protection#' in z['url'] else z['url'] for z in x['links'])
for a in attempts():
 if a.get('http_status')!=200 or a.get('text_length',0)<100:continue
 b=by.get(m.route_key(a['url']));x=read(ROOT/a['evidence_file']);y=read(ROOT/b['evidence_file']) if b else None
 same=bool(y and x['text']==y['text']);links=bool(y and linkset(x)==linkset(y))
 r={'source_id':a['source_id'],'url':a['url'],'actual_attempt':a,'prior_evidence':b,'same_entire_text':same,'same_entire_semantic_linkset':links,'diff':None if same or not y else '\n'.join(difflib.unified_diff(y['text'].splitlines(),x['text'].splitlines())),'new_links':[z for z in x['links'] if not y or z['url'] not in {l['url'] for l in y['links']}]}
 rows.append(r)
 if not same or not links:print(a['source_id'],'NEW' if not y else 'CHANGED','text_equal',same,'links_equal',links,'DIFF',str(r['diff'])[:5500],'NEWLINKS',json.dumps(r['new_links'],ensure_ascii=False)[:3000])
write(RUN/'full-comparisons.json',rows)
print('comparisons',len(rows),'whole_text_and_links_equal',sum(r['same_entire_text'] and r['same_entire_semantic_linkset'] for r in rows))
