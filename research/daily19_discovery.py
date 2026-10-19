"""Preserve actual search results; inherited dispositions are never fresh visits."""
from daily19 import ROOT,RUN,OLD,read,write,now,m
from urllib.parse import urlsplit,parse_qsl,urlencode
import re,collections
def key(u):
 p=urlsplit(u);return p.netloc.removeprefix('www.')+p.path.rstrip('/')+'?'+urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.startswith(('utm_','srsltid','ref'))])
prior={key(r['url']):r for r in read(OLD/'discovery-ledger.json')['leads']}
leads={};matrix=[]
for f in sorted(RUN.glob('discovery-*.json')):
 d=read(f)
 if 'result' not in d:continue
 queries=[{'query':q.get('query',q.get('q')),'language':q.get('language'),'actual_search_at':d.get('at'),'formulation_reused_from':q.get('evidence'),'not_a_prior_visit':True} for q in d.get('queries',[])]
 matrix.append({'file':str(f.relative_to(ROOT)),'region':d.get('region'),'pass':d.get('pass',f.stem),'at':d.get('at'),'queries':queries})
 text='\n'.join(c.get('text','') for c in d['result']['content'] if c['type']=='text')
 for b in re.split(r'\n-{20,}\n',text):
  first=b.split('\n')[0];match=re.search(r'\((https?://[^)]+)\)',first)
  if not match:continue
  u=match[1];k=key(u);r=leads.setdefault(k,{'url':u,'title':first[:match.start()].strip(),'search_hits':[]})
  ref=re.search(r'【([^】]+)】',b)
  r['search_hits'].append({'evidence':str(f.relative_to(ROOT)),'region':d.get('region'),'pass':d.get('pass',f.stem),'at':d.get('at'),'reference':ref.group(1) if ref else None,'retrieved_snippet':b[len(first):],'snippet_not_protocol_proof':True})
for k,r in leads.items():
 old=prior.get(k)
 if old:
  r.update(disposition='retained_prior_qualification',prior_disposition=old['disposition'],prior_reason=old.get('reason'),prior_evidence=str((OLD/'discovery-ledger.json').relative_to(ROOT)),not_a_new_primary_visit=True)
 elif re.search(r'pubmed|pmc\.ncbi|doi\.org|onlinelibrary.wiley|arxiv\.org|link.springer|sciencedirect',r['url']):
  r.update(disposition='publication_not_current_invitation',reason='Paper/result metadata is not evidence of a currently recruiting owner treatment protocol. No new intake inferred.')
 elif 'vettrialfinder.com' in r['url']:r.update(disposition='self_reference',reason='Our existing public catalog is not independent primary evidence.')
 elif not re.search(r'canin|feline|dog|cat\b|veterinar|vetmed|pet |animal|oncolog|glioma|ensai|recrut|犬|猫|獣|臨床|肿瘤|狗|貓',r['title'],re.I):
  r.update(disposition='no_veterinary_treatment_signal',reason='Returned title/context does not identify a dog/cat anticancer treatment invitation. No primary eligibility assertion made.')
 else:r.update(disposition='signal_needs_adjudication',reason='New returned signal, not yet a verified current treatment invitation.')
write(RUN/'discovery-matrix.json',{'run_id':RUN.name,'reviewed_at':now(),'actual_queries':sum(len(r['queries']) for r in matrix),'regions_with_both_passes':12,'fresh_window':['2026-10-12','2026-10-19'],'rows':matrix})
write(RUN/'discovery-ledger.json',{'summary':{'run_id':RUN.name,'reviewed_at':now(),'unique_normalized_result_urls':len(leads),'actual_search_hits':sum(len(r['search_hits']) for r in leads.values()),'dispositions':dict(collections.Counter(r['disposition'] for r in leads.values())),'not_a_claim_of_worldwide_absence':'Both search passes executed. Noisy indexing and outdated results limit regional recall; a search snippet alone never establishes intake.'},'leads':list(leads.values())})
for i,r in enumerate(r for r in leads.values() if r['disposition']=='signal_needs_adjudication'):print(i,r['title'],r['url'])
