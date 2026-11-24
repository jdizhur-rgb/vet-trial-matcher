#!/usr/bin/env python3
import hashlib, json, re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent

def norm(url):
    p=urlsplit((url or '').strip())
    path=re.sub(r'/+','/',unquote(p.path or '/'))
    if path != '/': path=path.rstrip('/')
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,''))

class Parser(HTMLParser):
    def __init__(self, base):
        super().__init__(); self.base=base; self.skip=0; self.text=[]; self.links=[]; self.href=None; self.anchor=[]; self.title=[]; self.in_title=False
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style','noscript','svg'}: self.skip += 1
        if tag=='title': self.in_title=True
        if tag=='a' and not self.skip:
            self.href=dict(attrs).get('href'); self.anchor=[]
    def handle_endtag(self, tag):
        if tag in {'script','style','noscript','svg'} and self.skip: self.skip -= 1
        if tag=='title': self.in_title=False
        if tag=='a' and self.href and not self.skip:
            self.links.append({'url':urljoin(self.base,self.href),'text':' '.join(' '.join(self.anchor).split())[:400]}); self.href=None; self.anchor=[]
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
            if self.href: self.anchor.append(data)
            if self.in_title: self.title.append(data)

def read_attempt_text(attempt):
    rel=attempt.get('raw_artifact')
    if not rel: return {'text':'','title':'','links':[]}
    p=ROOT/rel
    if not p.exists(): return {'text':'','title':'','links':[]}
    if p.suffix.lower()=='.pdf':
        try:
            reader=PdfReader(str(p)); text=' '.join(' '.join((page.extract_text() or '') for page in reader.pages).split())
            return {'text':text,'title':'PDF protocol','links':[]}
        except Exception:
            return {'text':'','title':'PDF protocol unreadable','links':[]}
    body=p.read_bytes().decode('utf-8','replace')
    parser=Parser(attempt.get('final_url') or attempt.get('requested_url') or '')
    try: parser.feed(body)
    except Exception: pass
    text=' '.join(' '.join(parser.text).split())
    seen=set(); links=[]
    for x in parser.links:
        if not x['url'].startswith(('http://','https://')): continue
        k=norm(x['url'])
        if k in seen: continue
        seen.add(k); links.append(x)
    return {'text':text,'title':' '.join(' '.join(parser.title).split()),'links':links}

catalog=json.loads((ROOT/'data/trials_base.json').read_text())
by_url=defaultdict(list)
for row in catalog:
    for key in ('url','source_url','status_source','funding_source','contact_source'):
        v=row.get(key)
        if isinstance(v,str) and v.startswith(('http://','https://')): by_url[norm(v)].append(row['id'])

inventory=json.loads((ROOT/'data/source_inventory.json').read_text())['sources']
source_ev=json.loads((RUN/'current-source-proxy-evidence.json').read_text())
source_rows=defaultdict(list)
for a in source_ev['attempts']: source_rows[a.get('source_id')].append(a)

source_reviews=[]
keywords=re.compile(r'(?i)clinical\s*(trial|study)|cancer|oncolog|tumou?r|carcin|sarcoma|lymphoma|melanoma|leukemia|glioma|osteosarcoma|mast cell|hemangiosarcoma')
for source in inventory:
    attempts=source_rows.get(source['id'],[]); route_reviews=[]; exact=set(); candidate_links=[]
    for a in attempts:
        parsed=read_attempt_text(a) if a.get('result')=='success' else {'text':'','title':'','links':[]}
        for link in parsed['links']:
            ids=by_url.get(norm(link['url']),[])
            exact.update(ids)
            if keywords.search((link.get('text') or '')+' '+link['url']):
                candidate_links.append({'url':link['url'],'text':link.get('text',''),'exact_canonical_ids':ids})
        route_reviews.append({
            'role':a.get('role'),'url':a.get('requested_url'),'result':a.get('result'),'status':a.get('status'),
            'completed_at':a.get('completed_at'),'raw_artifact':a.get('raw_artifact'),'title':parsed['title'],
            'text_sha256':hashlib.sha256(parsed['text'].encode()).hexdigest() if parsed['text'] else None,
            'text_chars':len(parsed['text']),'candidate_link_count':len([x for x in parsed['links'] if keywords.search((x.get('text') or '')+' '+x['url'])])
        })
    uniq=[]; seen=set()
    for x in candidate_links:
        k=norm(x['url'])
        if k not in seen: seen.add(k); uniq.append(x)
    readable=[r for r in route_reviews if r['result']=='success' and r['text_chars']>=120]
    source_reviews.append({
        'source_id':source['id'],'name':source.get('name'),'routes':route_reviews,
        'readable_routes':len(readable),'candidate_links':uniq,'exact_canonical_ids':sorted(exact),
        'roster_complete':False,
        'current_finding':f"{source.get('name')} ({source['id']}): {len(attempts)} configured routes received current decisions; readable current routes={len(readable)}; oncology/trial links examined={len(uniq)}; exact canonical URL matches={len(exact)}. The returned material does not independently prove an exhaustive current roster unless separately established in protocol review.",
        'evidence_refs':['research/audit-runs/'+RUN.name+'/current-source-proxy-evidence.json','research/audit-runs/'+RUN.name+'/source-content-review.json']
    })

proto_ev=json.loads((RUN/'current-protocol-proxy-evidence.json').read_text())
proto_rows=defaultdict(list)
for a in proto_ev['attempts']: proto_rows[a.get('source_id')].append(a)
protocol_reviews=[]
for trial_id in json.loads((RUN/'execution-baseline.json').read_text())['public_ids']:
    attempts=proto_rows.get(trial_id,[]); texts=[]; routes=[]
    for a in attempts:
        parsed=read_attempt_text(a) if a.get('result')=='success' else {'text':'','title':'','links':[]}
        if parsed['text']: texts.append(parsed['text'])
        routes.append({'role':a.get('role'),'url':a.get('requested_url'),'result':a.get('result'),'status':a.get('status'),'completed_at':a.get('completed_at'),'raw_artifact':a.get('raw_artifact'),'title':parsed['title'],'text_chars':len(parsed['text']),'text_sha256':hashlib.sha256(parsed['text'].encode()).hexdigest() if parsed['text'] else None})
    text='\n'.join(texts); lo=text.lower()
    facts={
        'identity':bool(text),
        'recruitment_sites':any(k in lo for k in ('location','site','hospital','university','clinic')),
        'eligibility':any(k in lo for k in ('eligibility','eligible','inclusion','exclusion','qualify')),
        'funding':any(k in lo for k in ('funded','funding','cost','compensation','covered','reimburse','financial')),
        'contacts':any(k in lo for k in ('contact','email','phone','@')),
    }
    protocol_reviews.append({'trial_id':trial_id,'routes':routes,'readable_routes':sum(r['text_chars']>=120 for r in routes),'facts_present':facts,'all_five_fact_sections_present':all(facts.values()),'current_text_sha256':hashlib.sha256(text.encode()).hexdigest() if text else None,'current_excerpt':text[:3000],'evidence_refs':['research/audit-runs/'+RUN.name+'/current-protocol-proxy-evidence.json','research/audit-runs/'+RUN.name+'/protocol-content-review.json']})

(RUN/'source-content-review.json').write_text(json.dumps({'run_id':RUN.name,'sources':source_reviews},indent=2,ensure_ascii=False)+'\n')
(RUN/'protocol-content-review.json').write_text(json.dumps({'run_id':RUN.name,'protocols':protocol_reviews},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'sources':len(source_reviews),'source_readable':sum(bool(x['readable_routes']) for x in source_reviews),'source_candidate_links':sum(len(x['candidate_links']) for x in source_reviews),'protocols':len(protocol_reviews),'protocol_readable':sum(bool(x['readable_routes']) for x in protocol_reviews),'protocol_all_five_sections':sum(x['all_five_fact_sections_present'] for x in protocol_reviews)},ensure_ascii=False))
