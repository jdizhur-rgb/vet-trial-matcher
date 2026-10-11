import json,re,collections,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parent
PARENT=ROOT/'research/audit-runs/care-20261011T065613-0400'
def read(p):return json.loads(p.read_text())
def norm(u):
    p=urllib.parse.urlsplit(u or '')
    return urllib.parse.urlunsplit(('https',p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),p.query,''))
pages=collections.defaultdict(list)
for p in list((PARENT/'pages').glob('*.json'))+list((RUN/'pages').glob('*.json')):
    d=read(p);d['evidence_file']=str(p.relative_to(ROOT));pages[norm(d['url'])].append(d)
profiles=read(PARENT/'acvim-current-profiles.json');profiles=profiles.get('profiles',[]) if isinstance(profiles,dict) else profiles
by_profile={urllib.parse.parse_qs(urllib.parse.urlsplit(p['profile_url']).query).get('id',[''])[0]:p for p in profiles}
centers=read(ROOT/'data/oncology_centers.json')['centers']
inv=read(ROOT/'data/oncology_care_source_inventory.json')['sources']
rows=[];queue=set()
for s in inv:
    if s['content_sufficient']:continue
    cs=[c for c in centers if norm(s['master_url']) in {norm(c.get('website')),norm(c.get('verification_url'))}]
    if not cs:cs=[c for c in centers if c['name']==s['name']]
    pid=urllib.parse.parse_qs(urllib.parse.urlsplit(s['master_url']).query).get('id',[''])[0]
    prof=by_profile.get(pid)
    primary=[]
    if prof and prof.get('website'):primary.append(prof['website'])
    for c in cs:primary.extend([c.get('website'),c.get('verification_url')])
    primary.extend([s['master_url']]+s['supporting_urls'])
    urls=[]
    for u in primary:
        if not u or not u.startswith(('http://','https://')):continue
        u=re.sub('^http:','https:',u)
        if norm(u) not in {norm(v) for v in urls}:urls.append(u)
    for u in list(urls):
        for pg in pages.get(norm(u),[]):
            for link in pg.get('links',[]):
                v=link['url']
                if not v.startswith('https://'):continue
                if urllib.parse.urlsplit(v).netloc.removeprefix('www.')!=urllib.parse.urlsplit(u).netloc.removeprefix('www.'):continue
                if re.search(r'oncolog|cancer|chemother|electrochem|radiation',link.get('text','')+' '+urllib.parse.urlsplit(v).path,re.I):
                    if re.search(r'/news|/blog|/article|/research|/trial|/search|/category|/tag/',v,re.I):continue
                    if norm(v) not in {norm(x) for x in urls}:urls.append(v)
    # Retain evidence already fetched. Never repeat a cached 403 or sufficient source.
    new_urls=[u for u in urls if norm(u) not in pages and 'vetspecialists.com' not in u]
    queue.update(new_urls)
    rows.append({'source_id':s['id'],'name':s['name'],'source_type':s['source_type'],'profile':prof,'canonical_candidates':cs,'official_urls':urls,'cached_evidence_files':list(dict.fromkeys(pg['evidence_file'] for u in urls for pg in pages.get(norm(u),[]))),'new_urls':new_urls,'semantic_status':'pending'})
(RUN/'remaining-source-plan.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(RUN/'missing-primary-urls.json').write_text(json.dumps(sorted(queue),indent=2)+'\n')
print(json.dumps({'remaining_sources':len(rows),'cached_primary_pages':sum(bool(r['cached_evidence_files']) for r in rows),'new_official_urls':len(queue),'clinical_sources':sum(r['source_type']=='center' for r in rows)},indent=2))
