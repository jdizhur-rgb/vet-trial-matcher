#!/usr/bin/env python3
import json,re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parent
class E(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.t=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style','noscript','svg'}: self.skip+=1
    def handle_endtag(self,tag):
        if tag in {'script','style','noscript','svg'} and self.skip: self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.t.append(d)

trials={x['id']:x for x in json.loads((ROOT/'data/trials_base.json').read_text())}
ev=json.loads((RUN/'current-protocol-evidence.json').read_text())
by=defaultdict(list); fall=[]
for a in ev['attempts']:
    row=dict(a)
    if a['result']=='http_response':
        raw=(ROOT/a['artifact']).read_bytes(); pdf=raw.startswith(b'%PDF'); text=''
        if not pdf:
            e=E()
            try:e.feed(raw.decode('utf-8','replace')); text=re.sub(r'\s+',' ',' '.join(e.t)).strip()
            except Exception:pass
        canon=trials[a['trial_id']]
        tokens=[]
        for v in [canon.get('title'),canon.get('center'),*(canon.get('cancers') or [])]:
            if isinstance(v,str): tokens += [w.lower() for w in re.findall(r'[A-Za-zÀ-ÿА-Яа-я0-9-]{5,}',v)]
        hits=sorted({w for w in tokens if w in text.lower()})
        row.update({'is_pdf':pdf,'visible_text_chars':len(text),'text_excerpt':text[:2400],
                    'canonical_token_hits':hits[:50]})
        if pdf or len(text)<400:
            fall.append({'trial_id':a['trial_id'],'url':a['url'],
                         'reason':'pdf_requires_text_extraction' if pdf else f'thin_text_{len(text)}'})
    by[a['trial_id']].append(row)

rows=[]
for tid in ev and [t['id'] for t in trials.values() if t.get('available_for_matching') is True]:
    routes=by.get(tid,[]); readable=[x for x in routes if x.get('status')==200 and x.get('visible_text_chars',0)>=400]
    rows.append({'trial_id':tid,'route_count':len(routes),'readable_routes':len(readable),
                 'restricted_routes':sum(x.get('result')=='skipped_exact_restriction' for x in routes),
                 'routes':routes})
out={'run_id':RUN.name,'trial_total':len(rows),'trials':rows,
     'web_fallback_needed':list({(x['trial_id'],x['url']):x for x in fall}.values())}
(RUN/'protocol-body-review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(RUN/'protocol-web-fallback-targets.json').write_text(json.dumps(out['web_fallback_needed'],indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'trials':len(rows),'readable_trials':sum(r['readable_routes']>0 for r in rows),
                  'restricted_only_or_thin':sum(r['readable_routes']==0 for r in rows),
                  'web_fallback_targets':len(out['web_fallback_needed'])},indent=2))
