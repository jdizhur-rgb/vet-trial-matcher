import pathlib,json,re,datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rec=rd(R/'receipt-final.json');S=rd(R/'individual-source-decisions.json');index=[]
for n in [1,2,21]:
 p=R/f'web-{n}.json';x=rd(p);text='\n'.join(c.get('text','') for c in x['result']['content']);urls=[]
 if n==21:urls=['https://www.caninecancer.org.au/Osteostudyflyer-2.pdf']
 else:
  for body in re.findall(r'Source: open\((\{[^\n]*?\})\)',text):
   try:urls.append(json.loads(body)['ref_id'])
   except (ValueError,KeyError):pass
 for u in urls:
  started=x['started_at'];ended=x['completed_at']
  if isinstance(started,dict):started=datetime.datetime.strptime(started['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc).isoformat();ended=datetime.datetime.strptime(ended['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc).isoformat()
  part=next((t for t in text.split('--------------------------------------------------------------------------------') if u in t),text)
  row={'url':u,'method':'Web','route':'official_linked_protocol' if n==21 else 'same_url_transport_fallback','attempted_at':started,'completed_at':ended,'evidence_file':str(p.relative_to(ROOT)),'new_source_visit':True,'http_status':None,'result':'web_unavailable' if 'is not accessible via this tool' in part or 'Failed to fetch' in part else 'web_retrieved_content','freshness':'Original crawler/cache metadata retained in the full artifact; no independent server-freshness assertion.'};index.append(row)
  for src in rec['sources']:
   if any(a['url'].rstrip('/')==u.rstrip('/') for a in src['attempted_urls']) or n==21 and src['source_id']=='australia-caninecancer-state-research-guide':
    if not any(a['url']==u and a['evidence_file']==row['evidence_file'] for a in src['attempted_urls']):src['attempted_urls'].append(row)
    d=S[src['source_id']];d['evidence_refs']=list(dict.fromkeys(d['evidence_refs']+[row['evidence_file']]));src['opened_this_run']=True;src['route_used']=list(dict.fromkeys(src['route_used']+['Web']))
for src in rec['sources']:
 actual=[a for a in src['attempted_urls'] if a.get('new_source_visit')]
 if actual:
  latest=max(actual,key=lambda a:datetime.datetime.fromisoformat(a['completed_at'].replace('Z','+00:00')));src['new_last_checked_at']=latest['completed_at'];src['new_last_checked']=datetime.datetime.fromisoformat(latest['completed_at'].replace('Z','+00:00')).astimezone(ZoneInfo('America/New_York')).date().isoformat()
wr(R/'receipt-final.json',rec);wr(R/'individual-source-decisions.json',S);review=rd(R/'execution-review.json');review['source_reviews']=list(S.values());wr(R/'execution-review.json',review)
wr(R/'web-route-index-amendment.json',{'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finding':'Web1/2 URLs were present in original tool Source metadata but absent from our wrapper urls field. Indexing them is provenance repair, not a new visit. Web21 was a click on link19; actual retrieved URL is the PDF, not the wrapper diagnostic fragment. Original response/timestamps are unchanged.','actual_attempts':index})
wr(R/'execution-deviations.json',{'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':[{'kind':'checkpoint_interval','actual_intervals':['03:11:48→03:28:10=16m22s','03:28:10→03:46:54=18m44s'],'finding':'Two early intervals exceeded15min; no retroactive checkpoints fabricated. Thereafter automatic immutable checkpoints every10min.'},{'kind':'extra_diagnostic_request','url':'https://veterinaryclinicaltrials.org/','finding':'Initial native diagnostic request preceded the inventory wrapper and the root was read again by the normal master pass. Original diagnostic instant was not separately saved; it is not reconstructed.'},{'kind':'redundant_Web_retrieval','urls':['https://leahlabs.com/','https://www.anivive.com/trials','https://www.caninecancer.org.au/ausresearch.html'],'finding':'Web20 repeated URLs already in Web2 because the wrapper metadata omitted its URL list. LEAH/Anivive were already readable; guide initial Web retrieval was insufficient. Both original tool responses/times are retained; no exact access denial was retried or bypassed.'},{'kind':'timestamp_ordering','finding':'Three source-date selections were corrected using actual timezone-aware instants instead of lexicographic mixed-zone strings. Original attempts were not redated. See timestamp-order-review.json.'}]})
print('Provenance rows indexed',len(index))
