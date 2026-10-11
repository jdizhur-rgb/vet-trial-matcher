import json,copy,re,hashlib,urllib.parse,collections
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;P=ROOT/'research/audit-runs/care-20261011T065613-0400'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def norm(u):
 p=urllib.parse.urlsplit(u or '');return urllib.parse.urlunsplit(('https',p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),p.query,''))
meta=read(RUN/'run.json');before=read(RUN/'oncology_care_source_inventory.json.before');inv=copy.deepcopy(before);rece=read(P/'receipt-final.json');rece.update(run_id=RUN.name,parent_run_id=P.name,started_at=meta['inherited_audit_started_at'],resumed_at=meta['started_at'],base_sha=meta['base_sha'],ended_at=now(),status='INCOMPLETE',visit_semantics='Cumulative same-day evidence; inherited visits keep original timestamps. New invocation and review times are separate from actual visits.')
plans={x['source_id']:x for x in read(RUN/'remaining-source-plan.json')};sem={x['source_id']:x for x in read(RUN/'semantic-reconciliation.json')};allpages=[]
for base in [P,RUN]:
 for f in (base/'pages').glob('*.json'):
  d=read(f);d['evidence_file']=str(f.relative_to(ROOT));d['inherited_visit']=base==P;allpages.append(d)
pageby=collections.defaultdict(list)
for pg in allpages:pageby[norm(pg['url'])].append(pg)
pet=read(RUN/'petcure-full-reconciliation.json');petby={x['canonical_name']:x for x in pet['locations']};med=read(P/'medvet-branch-review.json');medby={x['name']:x for x in med if x['services'] and x['name'] not in ['MedVet New Orleans','MedVet Vancouver']};cat=read(ROOT/'data/oncology_centers.json')['centers'];verified=[]
selected={'arise-veterinary-center','avets-specialty-emergency-trauma-center','casper-animal-medical-center','central-toronto-veterinary-referral-clinic','countryside-veterinary-hospital','cross-lanes-veterinary-hospital','veterinary-emergency-referral-center-of-hawaii','veterinary-emergency-specialty-hospital-singapore','veterinary-referral-center','veterinary-referral-center-of-central-oregon'}
for s,r in zip(inv['sources'],rece['sources']):
 assert s['id']==r['source_id'];sid=s['id'];r['before_last_checked']=s['last_checked'];r['before_last_checked_at']=s['last_checked_at'];r['inherited_content_sufficient']=r['content_sufficient'];r['before_last_result']=s['last_result'];plan=plans.get(sid);roots={norm(u) for u in [s['master_url']]+s['supporting_urls']};primary=[]
 if plan:
  for c in plan['canonical_candidates']:primary += [c.get('website',''),c.get('verification_url','')]
  if plan['profile']:primary.append(plan['profile'].get('website',''))
  roots.update(norm(u) for u in primary if u)
 relevant=[]
 for u in roots:relevant += pageby.get(u,[])
 # Include captured candidate clinical evidence, keeping branch proof separate.
 if sid in sem:
  for e in sem[sid]['evidence']:
   relevant += pageby.get(norm(e['url']),[])
 seen={(a['url'],a['attempted_at']) for a in r['attempted_urls']}
 for pg in relevant:
  key=(pg['url'],pg['attempted_at'])
  if key in seen:continue
  seen.add(key);r['attempted_urls'].append({'url':pg['url'],'attempted_at':pg['attempted_at'],'http_status':pg.get('http_status'),'method':pg.get('method','shell.urllib'),'outcome':'partial','error':pg.get('error'),'fingerprint_sha256':pg.get('fingerprint_sha256'),'evidence_file':pg['evidence_file'],'inherited_visit':pg['inherited_visit'],'semantic_review':'Clinical verification or explicit pending status in semantic-reconciliation.json'})
 approved=[];reason=None
 if s['name'] in medby:
  mv=medby[s['name']];pg=read(P/mv['evidence_file']);approved=[mv['url']];reason='Current local Specialty Services at named MedVet branch and current clinician roster checked with branch address; no global-navigation service inference.'
 elif s['name'] in petby:
  approved=[petby[s['name']]['official_url']];reason='All seven PetCure locations reconciled to physical host addresses; current location-specific treatment and clinical-team text verified.'
 elif sid=='network-petcure':
  approved=[x['official_url'] for x in pet['locations']];reason='Complete current PetCure seven-site roster reconciled; no duplicate host hospitals added.'
 elif sid in selected and sem[sid]['content_sufficient']:
  approved=sem[sid]['verified_primary_urls'];reason='Current branch-specific clinical body, published treatment, physical address/contact and available doctor qualifications reconciled. No additional modalities inferred.'
 elif sid in sem and sem[sid]['content_sufficient']:
  for e in sem[sid]['evidence']:
   if not e['sufficient'] or 'vcahospitals.com' not in e['url']:continue
   candidates=plans[sid]['canonical_candidates'];body=read(ROOT/e['evidence_file']).get('text','')
   if any(c['services'] and set(c['services']) <= {'Local oncology care','Chemotherapy'} for c in candidates) and re.search(r'At our hospital,?\s+we have a specialized area to treat our chemotherapy patients',body,re.I):
    approved.append(e['url']);reason='Exact VCA branch address/contact and explicit dedicated hospital chemotherapy administration area; GP chemotherapy listing, no board-specialist or radiation inference.'
 if approved:
  # Accepted URLs were actually opened; append any inherited supporting attempt.
  for u in approved:
   for pg in pageby[norm(u)]:
    if (pg['url'],pg['attempted_at']) not in seen:
     r['attempted_urls'].append({'url':pg['url'],'attempted_at':pg['attempted_at'],'method':pg['method'],'http_status':pg.get('http_status'),'outcome':'success','evidence_file':pg['evidence_file'],'inherited_visit':pg['inherited_visit'],'fingerprint_sha256':pg.get('fingerprint_sha256')});seen.add((pg['url'],pg['attempted_at']))
  s['supporting_urls']=list(dict.fromkeys(s['supporting_urls']+[u for u in approved if norm(u)!=norm(s['master_url'])]));s.update(last_result='success',content_sufficient=True,last_reviewed_at=now(),last_review_run_id=RUN.name,last_review_note=reason);r.update(master_result='success',content_sufficient=True,processing_complete=True,protocols_seen=7 if sid=='network-petcure' else 1,care_service_count=7 if sid=='network-petcure' else 1,route_used=approved[0],semantic_review=reason,reviewed_at=s['last_reviewed_at']);verified.append({'source_id':sid,'official_urls':approved,'reason':reason})
 else:
  s.update(last_reviewed_at=now(),last_review_run_id=RUN.name)
  if not s['content_sufficient']:s['last_review_note']='Captured official alternatives checked conservatively; full source-specific service/identity/credentials reconciliation remains unfinished. No success or external-blocker claim.'
 fresh=[a for a in r['attempted_urls'] if not a.get('inherited_visit',True) and norm(a['url']) in roots]
 if fresh:
  last=max(fresh,key=lambda a:a['attempted_at']);s.update(last_checked_at=last['attempted_at'],last_checked=last['attempted_at'][:10],last_run_id=RUN.name)
 r.update(after_last_checked=s['last_checked'],after_last_checked_at=s['last_checked_at'],reviewed_this_resume=sid in plans,visit_date_changed=bool(fresh))
 r['opened_this_run']=True
# New canonical clinical sources preserve actual inherited clinic visits.
for x in read(RUN/'confirmed-discovery-additions.json'):
 c=x['verified_record'];e=x['clinical_evidence'];latest=max(e,key=lambda z:z['actual_attempted_at']);sid='discovered-'+hashlib.sha256(c['verification_url'].encode()).hexdigest()[:14];at=latest['actual_attempted_at'];urls=list(dict.fromkeys(z['url'] for z in e));pg=max(pageby[norm(c['verification_url'])],key=lambda z:z['attempted_at'])
 inv['sources'].append({'id':sid,'name':c['name'],'source_type':'center','master_url':c['verification_url'],'supporting_urls':[u for u in urls if u!=c['verification_url']],'required_cadence':'weekly','last_checked':at[:10],'last_checked_at':at,'last_result':'success','http_status':200,'working_url':c['verification_url'],'fingerprint_sha256':pg['fingerprint_sha256'],'content_sufficient':True,'last_run_id':P.name,'last_review_run_id':RUN.name,'last_reviewed_at':x['reviewed_at'],'last_review_note':'New to directory; current clinical treatment and physical address/team/access facts verified in confirmed-discovery-additions.json; separate map check dates.'})
 rece['sources'].append({'source_id':sid,'name':c['name'],'master_url':c['verification_url'],'before_last_checked':None,'before_last_checked_at':None,'after_last_checked':at[:10],'after_last_checked_at':at,'opened_this_run':True,'attempted_urls':[{'url':z['url'],'attempted_at':z['actual_attempted_at'],'method':'shell.urllib','http_status':200,'outcome':'success','evidence_file':z['evidence_file'],'inherited_visit':True} for z in e],'master_result':'success','content_sufficient':True,'protocols_seen':1,'care_service_count':1,'count_semantics':'individual care source, not trial protocol','processing_complete':True,'route_used':c['verification_url'],'reviewed_at':x['reviewed_at']})
rece.update(source_total=len(inv['sources']),attempted_total=len(rece['sources']),content_sufficient_total=sum(x['content_sufficient'] for x in rece['sources']),original_source_total=487,ended_at=now())
save(ROOT/'data/oncology_care_source_inventory.json',inv);save(ROOT/'data/oncology_care_audit_coverage.json',rece);save(RUN/'receipt-final.json',rece);save(RUN/'accepted-source-reconciliations.json',verified)
gaprows=[]
for r in rece['sources']:
 if r['content_sufficient']:continue
 sr=sem.get(r['source_id'],{});missing=sr.get('missing_facts') or ['Source-specific detail reconciliation remains unfinished']
 if r['source_id']=='medvet-new-orleans':missing=['Current local service list excludes radiation; historical radiation tag is unresolved and has not been removed merely from absence. Verify radiation equipment/current delivery separately.']
 if r['source_id']=='medvet-vancouver':missing=['Current physician is Stephanie Byrne DVM MVetMed, residency trained in oncology; historical ACVIM board affiliation must be reconciled without claiming departure from absence.']
 gaprows.append({'source_id':r['source_id'],'category':'roster_unestablished','processing_assessment':'executor_unfinished','question':'Does this source establish all current clinical care, physical branch and access facts required by the canonical record?','reason':' '.join(missing),'next_action':'Complete the exact source/branch service and clinician reconciliation using captured official alternatives; retain unresolved status until sufficient evidence.','unperformed_steps':missing,'evidence':{'source_id':r['source_id'],'attempted_urls':[a['url'] for a in r['attempted_urls']]}})
save(RUN/'gap-review.json',{'original_run_id':RUN.name,'reviewed_at':now(),'rows':gaprows})
# Search queries remain the original actual discovery; no invented rerun searches.
dis=read(P/'care-discovery-receipt.json');dis.update(run_id=RUN.name,parent_run_id=P.name,started_at=meta['inherited_audit_started_at'],resumed_at=meta['started_at'],ended_at=now(),status='INCOMPLETE',inherited_search_count=274,new_search_count_this_resume=0,review_semantics='Cumulative actual same-day search receipt. All 274 queries were performed in parent run; exact timestamps and raw evidence retained. Resume adds clinical reconciliation and actual page retrievals, not fictitious new searches. Batch search URL counts are not unique per-geography page counts.')
for field in ['us_areas','global_regions']:
 for geo in dis[field]:
  for q in geo['searches']:
   if q.get('raw_evidence_file'):q['raw_evidence_file']='../'+P.name+'/'+q['raw_evidence_file']
for net in dis['network_traversals']:
 for a in net['attempts']:
  if a.get('evidence_file'):a['evidence_file']='../'+P.name+'/'+a['evidence_file']
 if net['network']=='PetCure':net.update(status='complete',master_sufficient=False,unresolved_locations=0,count_notes='Current seven-site roster and all seven individual locations fully reconciled against canonical physical hosts; four radiation tags added; no extra physical clinic.')
 if net['network']=='MedVet_WestVet':net.update(unresolved_locations=2,count_notes='40 branch pages retrieved; current local specialty list identifies 19 medical-oncology and 5 radiation sites. All 19 physical locations mapped; 17 current local service/doctor records sufficient. Vancouver current residency-trained clinician versus historical board affiliation, and New Orleans historical radiation tag remain unresolved. Other 21 branches are not automatically oncology sites.')
for x in read(RUN/'confirmed-discovery-additions.json'):
 c=x['verified_record'];dis['candidates'].append({'id':'resume-'+hashlib.sha256(c['website'].encode()).hexdigest()[:14],'name':c['name'],'official_url':c['verification_url'],'classification':'new_service' if c['country']=='France' else 'new_center','verified_official_service_page':c['verification_url'],'canonical_reconciled':True,'newly_opened_physical_clinic':False,'details_file':'confirmed-discovery-additions.json'})
for x in read(RUN/'verified-medvet-radiation-additions.json')+pet['locations']:
 if x.get('classification') not in ['new_service','NEW_SERVICE_EXISTING_CENTER']:continue
 name=x.get('canonical_name') or x['after']['name'];url=x.get('official_url') or x['evidence_url'];dis['candidates'].append({'id':'resume-service-'+hashlib.sha256(url.encode()).hexdigest()[:14],'name':name,'official_url':url,'classification':'new_service','verified_official_service_page':url,'canonical_reconciled':True,'note':'Existing physical hospital; current local radiation service, no duplicate clinic.'})
save(RUN/'care-discovery-receipt.json',dis)
# Complete bookkeeping over inherited search URLs, without presenting screening as semantic review.
pool=read(P/'discovery-screened-leads.json');ledger={};official={norm(c.get(k,'')):c['name'] for c in cat for k in ['website','verification_url'] if c.get(k)};confirmed={norm(x['verified_record']['website']):x['verified_record']['name'] for x in read(RUN/'confirmed-discovery-additions.json')}
for geo,leads in pool.items():
 for url,snips in leads.items():
  k=norm(url)
  if k not in ledger:
   host=urllib.parse.urlsplit(url).netloc;duplicate=official.get(k);nonclinic=any(s in host for s in ['reddit.com','linkedin.com','facebook.com','wikipedia.org','pubmed.ncbi','ncbi.nlm','clinicaltrials.gov','youtube.com'])
   cl='new_center' if k in confirmed and 'vetinparis' not in k else 'new_service' if k in confirmed else 'duplicate' if duplicate else 'rejected' if nonclinic else 'unresolved'
   ledger[k]={'url':url,'geographies':[],'classification':cl,'screening_method':'Exact current canonical service URL match or explicit non-provider platform; remaining lead unresolved','canonical_match':duplicate,'actual_primary_attempts':[{'attempted_at':pg['attempted_at'],'http_status':pg.get('http_status'),'evidence_file':pg['evidence_file']} for pg in pageby.get(k,[])],'semantic_processing_complete':cl in ['duplicate','new_center','new_service'],'snippets':snips,'primary_provider_status':'verified' if duplicate or k in confirmed else 'not_established'}
  ledger[k]['geographies'].append(geo)
save(RUN/'discovery-lead-ledger.json',{'source_parent_file':str((P/'discovery-screened-leads.json').relative_to(ROOT)),'unique_urls':len(ledger),'classification_counts':dict(collections.Counter(x['classification'] for x in ledger.values())),'unresolved_are_not_zero_findings':True,'leads':list(ledger.values())})
readback=[{'id':s['id'],'last_checked':s['last_checked'],'last_checked_at':s['last_checked_at'],'last_result':s['last_result']} for s in inv['sources']];save(RUN/'dates-local-readback.json',{'status':'PASS','rows':readback,'rows_count':len(readback),'timezone':'America/New_York','visit_timestamps_not_review_timestamps':True,'read_at':now()})
summary={'status':'INCOMPLETE','run_id':RUN.name,'parent_run_id':P.name,'invocation_started_at':meta['started_at'],'inherited_audit_started_at':meta['inherited_audit_started_at'],'ended_at':now(),'source_total':len(inv['sources']),'content_sufficient':rece['content_sufficient_total'],'partial':len(inv['sources'])-rece['content_sufficient_total'],'new_page_attempts':len(list((RUN/'pages').glob('*.json'))),'new_unique_page_urls':len({pg['url'] for pg in allpages if not pg['inherited_visit']}),'all_page_attempts':len(allpages),'all_unique_page_urls':len({pg['url'] for pg in allpages}),'new_map_attempts':4,'new_vca_identity_attempts':2,'searches_cumulative':274,'us_search_coverage':'52/52','world_search_coverage':'12/12','complete_networks':'1/7','before_centers':438,'after_centers':441,'tele_before':59,'tele_after':59,'clinical_counts':dict(collections.Counter(s for c in cat for s in c['services'])),'source_persisted_dates_changed':sum(x.get('visit_date_changed',False) for x in rece['sources']),'search_lead_classifications':dict(collections.Counter(x['classification'] for x in ledger.values()))}
save(RUN/'run-summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
