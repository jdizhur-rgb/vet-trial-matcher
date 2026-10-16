"""Read all canonical data; expose fresh page comparisons for manual decisions."""
import json, re, sys, difflib, importlib.util
from pathlib import Path
P=Path(__file__).parent;ROOT=P.parents[2];OLD=P.parent/'daily-20261015T030225-0400'
spec=importlib.util.spec_from_file_location('runner',P/'run.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner);m=runner.m
def read(p):return json.loads(p.read_text())
def attempts(p):return [json.loads(l) for l in (p/'attempts.jsonl').read_text().splitlines()]
prev={x['url']:x for x in attempts(OLD) if x.get('http_status')==200 and x['text_length']>100}
latest={x['url']:x for x in attempts(P)};inv=read(P/'before-source_inventory.json')['sources'];cat=read(P/'before-trials_base.json');catalog={r['id']:r for r in cat};prior={r['source_id']:r for r in read(OLD/'reviews.json')}
def body(a):
    raw=Path(a['raw_file']);html=raw.read_text(errors='replace') if raw.exists() else ''
    t=re.search(r'<main\b[^>]*>(.*?)</main>',html,re.I|re.S)
    if t:
        h=m.H();h.feed(t.group(1));return '\n'.join(z.strip() for z in h.parts if z.strip())
    return read(ROOT/a['evidence_file'])['text']
if sys.argv[1]=='compare':
    rows=[]
    for u,a in latest.items():
        b=prev.get(u);e=read(ROOT/a['evidence_file']);old=read(ROOT/b['evidence_file']) if b else None
        same=bool(old and e['text'] and e['text']==old['text']);links=bool(old and e['links']==old['links'])
        rows.append({'source_id':a['source_id'],'url':u,'at':a['attempted_at'],'current_evidence':a['evidence_file'],'previous_evidence':b['evidence_file'] if b else None,'full_current_text_equals_previous':same,'full_linkset_equals_previous':links,'previous_protocol_count':prior[a['source_id']]['protocols_seen'],'automatic_completion':False})
    m.write(P/'fresh-comparison.json',rows)
    for s in inv:
        a=latest.get(s['master_url']);r=next((r for r in rows if r['url']==s['master_url']),{})
        print(s['id'],a['http_status'] if a else 'GATE',a['text_length'] if a else 0,'EQUAL_TEXT+LINKS' if r.get('full_current_text_equals_previous') and r.get('full_linkset_equals_previous') else 'INSPECT',prior[s['id']]['source_result'])
elif sys.argv[1]=='show':
    for arg in sys.argv[2:]:
        s=inv[int(arg)] if arg.isdigit() else next(s for s in inv if s['id']==arg)
        print('\nSOURCE',inv.index(s),s['id'])
        for a in latest.values():
            if a['source_id']!=s['id']:continue
            e=read(ROOT/a['evidence_file']);print(a['route'],a['url'],a['http_status'],a['evidence_file'])
            text=body(a);print(text if len(text)<18000 else 'LARGE: '+str(len(text))+' read separately')
            links={l['url']:l for l in e['links'] if re.search(r'trial|stud|recruit|enrol|oncolog|cancer|tumou?r|lymph|sarcoma|melanoma|carcinoma|glioma',l['label'],re.I) and not re.search(r'student|undergraduate|course',l['label'],re.I)}
            print('CLINICAL LINKS',json.dumps([{'url':l['url'],'label':re.sub(r'\s+',' ',l['label'])[:140]} for l in links.values()],ensure_ascii=False))
elif sys.argv[1]=='prior':
    for arg in sys.argv[2:]:
        s=inv[int(arg)] if arg.isdigit() else next(s for s in inv if s['id']==arg);r=prior[s['id']]
        print('\n',s['id'],json.dumps(r,ensure_ascii=False))
