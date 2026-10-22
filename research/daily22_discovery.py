"""Every returned URL kept; prior decisions explicitly remain historical."""
from daily22 import ROOT,RUN,OLD,read,write,now
from urllib.parse import urlsplit,parse_qsl,urlencode
import re,collections
def key(u):
 p=urlsplit(u);return p.netloc.removeprefix('www.')+p.path.rstrip('/')+'?'+urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.startswith(('utm_','srsltid','ref'))])
prior={key(r['url']):r for r in read(OLD/'discovery-ledger.json')['leads']};leads={};matrix=[]
for f in sorted(RUN.glob('discovery-*.json'),key=lambda f:('targeted-sites' in f.name,f.name)):
 d=read(f)
 if 'result' not in d:continue
 matrix.append({'file':str(f.relative_to(ROOT)),'region':d['region'],'pass':d['pass'],'actual_search_at':d['at'],'queries':d['queries']})
 text='\n'.join(c.get('text','') for c in d['result']['content'] if c['type']=='text')
 for b in re.split(r'\n-{20,}\n',text):
  first=b.split('\n')[0];match=re.search(r'\((https?://[^)]+)\)',first)
  if not match:continue
  u=match[1];r=leads.setdefault(key(u),{'url':u,'title':first[:match.start()].strip(),'search_hits':[]});ref=re.search(r'【([^】]+)】',b)
  r['search_hits'].append({'evidence':str(f.relative_to(ROOT)),'region':d['region'],'pass':d['pass'],'at':d['at'],'reference':ref.group(1) if ref else None,'retrieved_snippet':b[len(first):],'snippet_not_protocol_proof':True})
for k,r in leads.items():
 old=prior.get(k)
 if old:r.update(disposition='retained_prior_qualification',prior_disposition=old['disposition'],prior_reason=old.get('reason'),prior_evidence=str((OLD/'discovery-ledger.json').relative_to(ROOT)),not_a_new_primary_visit=True)
 elif re.search(r'pubmed|pmc\.ncbi|doi\.org|onlinelibrary.wiley|arxiv\.org|link.springer|sciencedirect|frontiersin|mdpi.com',r['url']):r.update(disposition='PUBLICATION_ACCESS_SIGNAL',reason='Publication/result is not current owner recruitment. Disease-specific clinical evidence and real veterinary access require separate qualification.')
 elif 'vettrialfinder.com' in r['url']:r.update(disposition='SELF_REFERENCE',reason='Existing own catalog is not independent primary evidence.')
 elif not re.search(r'canin|feline|dog|cat\b|veterinar|vetmed|pet |animal|oncolog|glioma|ensai|recrut|犬|猫|獣|臨床|肿瘤|狗|貓|สุนัข|แมว|köpek|kedi|الكلاب|القطط|고양이|반려|chien|chat\b|cão|cães|cani|cane\b|gatto|hund|tumör|OXC-101',r['title'],re.I):r.update(disposition='NOT_DOG_CAT_ONCOLOGY_SIGNAL',reason='Returned title/context does not identify a client-owned dog/cat anticancer opportunity; no clinical claim made.')
 else:r.update(disposition='NEEDS_ADJUDICATION',reason='New returned veterinary signal, not a verified present treatment invitation.')
regions=collections.defaultdict(set)
for x in matrix:
 if x['pass'] in ['current','fresh']:regions[x['region']].add(x['pass'])
write(RUN/'discovery-matrix.json',{'run_id':RUN.name,'reviewed_at':now(),'actual_queries':sum(len(r['queries']) for r in matrix),'regions_with_both_passes':sum(v=={'current','fresh'} for v in regions.values()),'fresh_window':['2026-10-15','2026-10-22'],'rows':matrix})
write(RUN/'discovery-ledger.json',{'summary':{'run_id':RUN.name,'reviewed_at':now(),'unique_normalized_result_urls':len(leads),'actual_search_hits':sum(len(r['search_hits']) for r in leads.values()),'dispositions':dict(collections.Counter(r['disposition'] for r in leads.values())),'limitation':'Actual regional queries in two passes cover the mandatory12-region matrix, with additional targeted followups; not an exhaustive search of all-world websites. Index noise, old results and restricted primary sources remain explicit.'},'leads':list(leads.values())})
for i,r in enumerate(leads.values()):
 if r['disposition'] in ['NEEDS_ADJUDICATION','PUBLICATION_ACCESS_SIGNAL']:print(i,r['disposition'],r['title'],r['url'])
print('COUNTS',len(leads),collections.Counter(r['disposition'] for r in leads.values()))
