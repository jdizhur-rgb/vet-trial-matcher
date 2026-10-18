from reconcile import *
catalog=read(ROOT/'data/trials_base.json');inventory=read(P/'before-source_inventory.json')['sources'];known={}
for r in catalog:
 for f in ['url','source_url','registry_url','status_source','funding_source']:
  if r.get(f):known.setdefault(key(r[f]),[]).append(r['id'])
source_urls={key(u):s['id'] for s in inventory for u in [s['master_url']]+s.get('fallback_urls',[])}
records=[];matrix={};queries=0
for f in sorted(P.glob('discovery-*.json')):
 d=read(f)
 if not isinstance(d,dict) or d.get('pass') not in ['current_undated','fresh_7_days']:continue
 for region,language,q in d['queries']:
  queries+=1;matrix.setdefault(region,{}).setdefault(d['pass'],[]).append({'language':language,'query':q,'at':d['at'],'evidence':str(f.relative_to(ROOT))})
 t='\n'.join(b.get('text','') for b in d['result'].get('content',[]) if b.get('type')=='text')
 for block in re.split(r'\n-{20,}\n',t):
  m=re.search(r'^(.+?) \((https?://[^\n]+)\)\n.*?【([^】]+)】',block,re.S)
  if not m:continue
  title,url,ref=m.groups();snippet=block[m.end():];title=title.split('\n')[-1]
  records.append({'region':d['region'],'pass':d['pass'],'title':title,'url':url,'reference':ref,'search_evidence':str(f.relative_to(ROOT)),'retrieved_snippet':snippet,'current_invitation_not_proved_by_snippet':True})
group={}
for r in records:
 k=key(r['url']);group.setdefault(k,{'url':r['url'],'title':r['title'],'search_hits':[]})['search_hits'].append(r)
rows=[]
for k,r in group.items():
 url=r['url'];text=r['title']+' '+r['search_hits'][0]['retrieved_snippet'];low=text.lower();host=k[0];ids=known.get(k,[])
 if host=='vettrialfinder.com':disp='rejected_self_reference';why='Own site/search result is not independent primary evidence.'
 elif ids:disp='duplicate_existing_protocol';why='Exact primary/registry URL already belongs to the canonical identity; preserved current status rather than adding another card.'
 elif k in source_urls:disp='known_source_reconciled';why='Current source pass already reviewed this exact official master/fallback. Its individual leads retain their protocol-specific dispositions.'
 elif 'kodevet9.com' in host:disp='confirmed_new_trial';ids=['nz-kvs-kv9-solid-tumor-pilot'];why='Individual current pilot, owner FAQ, all8named sites and public supporting documents retrieved and reviewed; one protocol, dog/cat invitation, conservative unknown criteria and owner costs. See new-kv9-trial.json.'
 elif 'news.uq.edu.au/2026-02-dogs-cancer' in url or 'uq-gatton-launches-trial' in url:disp='unresolved_current_protocol';why='Known official February2026 Enzistat research/recruitment news signal; current full named protocol, drug specification, detailed enrollment and owner access are not established by news alone. Current UQ source/fallback read, no activation.'
 elif 'pharmaust.com' in host:disp='unresolved_current_status';why='Official historical monepantel results page: native526 twice and same-URL Web526. Search snippets describe results, not verified current intake. Not activated or declared completed from snippet.'
 elif 'research.upm.edu.my' in host or ('vet.upm.edu.my' in host and 'memorandum' in url):disp='unresolved_current_protocol';why='Actual official2023 UPM/NUS engineered mesenchymal stem-cell announcement says future dog/cat recruitment; comparative-oncology research programme last updated2015. No published current owner-enrolling drug/cohort, criteria or costs. New official discovery source, no trial activation.'
 elif 'clinical-trials-dogs-glioma-brain-tumors' in url or 'uc-davis-clinical-trials-are-recruiting-dogs-with-glioma' in url:disp='duplicate_existing_protocol';ids=['ucd-care-canine-glioma','ucd-prism-canine-glioma'];why='Fresh full UC Davis September3primary news read: CARE drug+radiation and PRISM observational/radiation pathways match existing identities. Today recrawl/secondary publication is not a new protocol.'
 elif 'feline-small-cell-gi-lymphoma-a-cancer' in url:disp='duplicate_existing_protocol';ids=['tamu-feline-small-cell-gi-lymphoma-wart'];why='TAMU current programme is the existing WART trial, confirmed by today’s permitted institutional listing. Secondary new article is not a distinct intervention.'
 elif 'mro.massey.ac.nz/bitstreams/628e2c39' in url or 'PMC11209120' in url or 'defying-the-odds-one-dog' in url:disp='rejected_historical_results';why='Original full paper retrieved: five-dog RAS-blockade safety pilot, published June17,2024, completed observation/results; no currently recruiting efficacy trial established.'
 elif 'research.ku.ac.th/forest/ProjectByPerson' in url:disp='rejected_no_current_therapeutic_intake';why='Full current university project ledger read: 2026 canine transmissible venereal tumour/antimicrobial projects are under Internal Closed Project. Research-project metadata supplies no current patient treatment protocol.'
 elif 'cmu.ac.th/th/article/87e945e2' in url:disp='rejected_no_current_therapeutic_intake';why='Full official March9,2026 news read: patent27360 for canine mammary-cancer vaccine issued February9,2026. A patent announcement does not establish an enrolling clinical trial.'
 elif 'up.ac.za' in host:disp='rejected_no_current_therapeutic_intake';why='Actual university primary pages read: October13,2021 oncology-centre collaboration and current general service description; no named current therapeutic protocol or owner-enrollment criteria. No clinic/care directory imported.'
 elif 'vet.chula.ac.th/cuvet_sat_event/31' in url:disp='unresolved_signal_retrieval';why='Specific official candidate page attempted natively503twice and same-URL Web502; no current trial identity/criteria established. Generic educational/care pages are not substituted.'
 elif 'novel-immunotherapy-for-canine-lymphoma' in url or 'UK-VCSR-2026-00001' in url:disp='rejected_sample_entry';why='Current actual UK-VCSR registry explicitly labels three sample studies AI-generated. Sample lymphoma entry is not clinical access.'
 elif any(s in host for s in ['pubmed.ncbi.nlm.nih.gov','pmc.ncbi.nlm.nih.gov','onlinelibrary.wiley.com','nature.com','researchgate.net','arxiv.org','sciencedirect.com','academic.oup.com','frontiersin.org','mro.massey.ac.nz','repositorio.unesp.br','colibri.udelar.edu.uy','silo.uy','openalex.org','educapes.capes.gov.br','pure.ed.ac.uk','link.springer.com','scielo.cl']):disp='rejected_publication_not_current_invitation';why='Published paper, abstract, repository or research review; no independent current owner-enrollment claim is established. Publication/result is not promoted into an open treatment trial.'
 elif any(s in low for s in ['trial','clinical','recruit','enroll','essai','studie','study','research','вакцин','臨床','治験','วิจัย']) and any(s in low for s in ['canine','feline','dog','cat','veterinary','chien','hund','perro','cães','สุนัข','猫','犬']):disp='screened_signal_no_new_primary_protocol';why='Research/news/generic source signal screened; no distinct primary current therapeutic protocol established beyond the source-pass catalogue and qualified leads. Remains a signal, not proof of zero trials in the region.'
 else:disp='rejected_outside_treatment_trial_scope';why='No dog/cat current anticancer treatment invitation: human trials, training, funding calls, care/service directories, diagnostics, observational research, general news or unrelated lexical matches.'
 r.update(disposition=disp,reason=why,canonical_ids=ids,primary_evidence=[{'url':a['url'],'at':a['attempted_at'],'method':a['method'],'evidence':a['evidence_file'],'result':a['result'],'http_status':a.get('http_status')} for a in native+web if key(a['url'])==k]);rows.append(r)
required=['USA','Canada','UK','Europe','LatinAmerica','AustraliaNZ','EastAsia','SouthAsia','SoutheastAsia','MiddleEast','NorthAfrica','SubSaharanAfrica'];assert all(all(p in matrix[r] for p in ['current_undated','fresh_7_days']) for r in required)
summary={'run_id':P.name,'reviewed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'actual_queries':queries,'regions_with_both_passes':12,'actual_search_hits':len(records),'unique_result_urls':len(rows),'dispositions':dict(collections.Counter(r['disposition'] for r in rows)),'confirmed_new_protocols':1,'not_a_claim_of_worldwide_absence':'Both passes executed; weak/noisy indexing remains a coverage limitation, particularly SouthAsia, MiddleEast, NorthAfrica, SubSaharanAfrica, and some local-language queries. Recrawled dates do not make old studies fresh.'}
write(P/'discovery-ledger.json',{'summary':summary,'leads':rows});write(P/'discovery-matrix.json',{'run_id':P.name,'completed_at':summary['reviewed_at'],'regions_completed':12,'passes':2,'query_count':queries,'fresh_window_start':'2026-10-11','fresh_window_end':'2026-10-18','matrix':matrix,'limits':summary['not_a_claim_of_worldwide_absence']});print(json.dumps(summary,ensure_ascii=False));print('REQUIRES MANUAL SIGNAL SCREEN:')
for r in rows:
 if r['disposition']=='screened_signal_no_new_primary_protocol':print(r['title'][:140],r['url'])
