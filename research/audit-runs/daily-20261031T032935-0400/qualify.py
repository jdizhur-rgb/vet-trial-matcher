from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit
import json,copy,re,collections
R=Path(__file__).resolve().parent;ROOT=R.parents[2];O=R.parent/'daily-20261031T025801-0400'
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
at=datetime.now(ZoneInfo('America/New_York')).isoformat()
av=rd(R/'avma-current-all.json');oldav=rd(O/'avma-current-all.json');prev={x['id']:x for x in oldav};ignore={'is_similar','distance','thumbnail','thumbnail_url'}
clinical=lambda x:{k:v for k,v in x.items()if k not in ignore}
changed=[x['id']for x in av if x['id']in prev and clinical(x)!=clinical(prev[x['id']])]
assert changed==[],changed
base=rd(O/'avma-reconciliation.json')['retained_dispositions'];ids={x['id']for x in av};assert all(x['registry_id']in ids for x in base['rows'])
wr(R/'avma-reconciliation.json',{'reviewed_at':at,'current_records':len(av),'unique_records':len(ids),'previous_records':len(prev),'current_oncology_union':len(base['rows']),'new_non_oncology':[{'id':x['id'],'title':x['name'],'reason':'Chiari-like malformation/syringomyelia neuropathic pain; not anticancer treatment'}for x in av if x['id']not in prev],'changed_clinical_objects':changed,'all_old_oncology_ids_present':True,'retained_dispositions':base,'retention_basis':'Each current registry clinical object compared against the preceding actual same-day payload; all471 oncology identities unchanged. Institutional/protocol questions and original primary dates retained.'})
vt=rd(R/'vettrials-current-all.json');old=rd(O/'vettrials-lead-dispositions.json')['rows'];byid={x['directory_id']:x for x in old};byurl={x.get('current_source_url'):x for x in old if x.get('current_source_url')};replacements={394:327,685:684,512:478,429:557};out=[];unmatched=[]
for x in vt:
 # Preserve previously qualified oncology identities and catch new oncology tags/titles.
 signal=x['id']in byid or x['id']in replacements or 'oncolog'in str(x.get('conditionCategory')).lower() or bool(re.search('cancer|lymphoma|sarcoma|melanoma|carcinoma|leukemia|tumou?r',x['title'],re.I))
 if not signal or x['id']in (685,512,429):continue
 previous=byid.get(x['id'])or byid.get(replacements.get(x['id']))or byurl.get(x.get('sourceUrl'))
 row={'directory_id':x['id'],'title':x['title'],'current_source_url':x.get('sourceUrl'),'current_enrollment_status':x.get('enrollmentStatus'),'previous_directory_id':previous.get('directory_id')if previous else None,'canonical_ids':previous.get('canonical_ids',[])if previous else [],'disposition':previous.get('disposition')if previous else None,'comparison_at':at,'fresh_primary_claimed':False}
 if previous:row['prior_disposition']=previous
 elif x['id']in (10,23) or 'thyroid function'in x['title'].lower()or'genetic landscape'in x['title'].lower()or'cases of canine splenic'in x['title'].lower():row['disposition']='NOT_TREATMENT';row['reason']='Diagnostic/sampling genetic landscape or MRI study; secondary category is not treatment.'
 else:unmatched.append(row)
 if False:row.update(disposition='HOLD_NOT_ACTIVE',fresh_primary_claimed=True,reason='Full official OVC PDT leaf read today, but current official canine index explicitly ON HOLD FOR RECRUITMENT. No activation.',current_primary_evidence=['evidence/7f9a4d0d25144f52e7.json','evidence/1d5a6ab8ea92a83766.json'])
 if x['id']==300:row.update(disposition='HOLD_NOT_ACTIVE',reason='Fresh whole official canine index remains ON HOLD; secondary enrolled label does not reopen study. Prior individual leaf remains historical evidence, not reread in this run.')
 if x['id']==298:row.update(disposition='NOT_TREATMENT_ON_HOLD',reason='Thyroid staining is diagnostic. Current index ON HOLD; direct leaf404 and same-URL Web insufficient.')
 if False:row.update(fresh_primary_claimed=True,reason='Full official Tennessee PDF read today: MRI with contrast and subsequent biopsy to characterize splenic/liver lesions; funded MRI/anesthesia and study histopathology, no experimental anticancer intervention. PDF updated11/16/2016, not a new therapeutic trial.',current_primary_evidence=['evidence/6e3b45299cc679be03.json'])
 out.append(row)
wr(R/'vettrials-lead-dispositions.json',{'reviewed_at':at,'total_all_condition':len(vt),'oncology_review_rows':len(out),'rows':out,'unmatched':unmatched,'substantive_directory_delta_evidence':'vettrials-delta.json','limit':'Extractor revisions are not new primary protocols. Prior dispositions remain historical unless explicitly marked with current primary evidence.'})
# Every actual returned discovery URL gets a review disposition; do not assert fresh
# publication merely because a seven-day query returned it.
inv=rd(R/'before-source_inventory.json')['sources'];hosts=collections.defaultdict(list)
for s in inv:
 for u in [s['master_url']]+s.get('fallback_urls',[]):hosts[(urlsplit(u).hostname or '').removeprefix('www.')].append(s['id'])
leads={};matrix=[]
for i in range(1,8):
 z=rd(R/f'discovery-{i}.json');t='\n'.join(c.get('text','')for c in z['result']['content'])
 for title,u in re.findall(r'^([^\n]*?)\((https?://[^\n]+)\)\n【',t,re.M):
  row=leads.setdefault(u,{'title':title.strip(),'url':u,'search_batches':[]});row['search_batches'].append(i)
 if i<=6:
  for region,q in zip(z['regions'],z['queries']):matrix.append({'region':region,'pass':z['pass'],'query':q,'recency_days':z.get('recency'),'actual_response':str((R/f'discovery-{i}.json').relative_to(ROOT)),'completed_at':z['completed_at'],'freshness_note':'Actual response retained; recency filter is not a publication-date confirmation.'})
for u,row in leads.items():
 h=(urlsplit(u).hostname or '').removeprefix('www.');related=sorted(set(hosts.get(h,[])))
 if 'institucional.ufpel.edu.br/projetos/id/u10335'in u:dis='NEW_OFFICIAL_SOURCE_WATCH';reason='Current native official project, coordinator and linked eyelid-surgery project fully read. Both therapeutic; present owner enrollment, site-specific intake and costs unpublished. Add discovery source, no active trial.'
 elif 'crovet.net'in h:dis='REJECT_GENERIC_CRO_PROGRAMME';reason='Actual programme, clinical-services and news pages read. Investigator network, regulatory services and industry news contain no named owner-enrolling oncology protocol; no blank form submitted.'
 elif 'zonanorte'in h:dis='WATCH_CURRENT_ACCESS_UNVERIFIED';reason='Retained Ensenada silver nanoparticle question; a secondary story does not establish present primary clinical access.'
 elif 'vetmarketportal.com.ar/nota/3224'in u:dis='REJECT_PREVIOUSLY_CLOSED_LEAD';reason='Same UNLP cutaneous SCC/actinic keratosis signal. Actual linked primary public form read Oct29 was explicitly closed; original time retained, not a fresh form visit.'
 elif 'UK-VCSR-2026-00001' in u:dis='REJECT_EXPLICIT_SAMPLE_AI_DEMO';reason='Actual individual official listing read in discovery-primary-1.json: explicitly Sample study AI-generated and not a real recruiting study. No activation.'
 elif 'huaier-v.org' in h:dis='REJECT_HISTORICAL_NON_ONCOLOGY_CAMPAIGN';reason='Both pages of actual Japanese 2024 PDF read. Crowdfunding deadline22June2024, steroid adverse-effect/immune-marker and blood-sampling research, not a current dog/cat anticancer treatment trial.'
 elif 'unlimited.lsu.edu' in h:dis='EXISTING_LSU_SCC_UNRESOLVED';reason='Full official article read; dated12May2026, describes intratumoral chemotherapy SCC trial and eleven visits over four months. No current enrollment confirmation, named individual protocol update or owner coverage. Existing news/index conflict remains unresolved; no reopening.'
 elif 'curelaboncology.com/comparative-medicine' in u:dis='WATCH_UNSPECIFIED_PROTOCOL_ACCESS';reason='Actual company page read with Web cache two weeks: historical Elenagen pilot findings and generic US/Israel/EU interest invitation. No named current protocol, sites, eligibility or owner charges; existing CureLab inventory retained without activation or outreach.'
 elif 'tierspital.uzh.ch' in h and 'formular-'in u:dis='FORM_NAVIGATION_NOT_NAMED_PROTOCOL';reason='Clinical-study referral/contact form navigation, no independently named new protocol from this result; no form submitted. Current official Zurich clinical source separately reconciled.'
 elif 'linkedin.com'in h and '/in/'in u:dis='EXCLUDE_PERSONAL_PROFILE_NOT_PROTOCOL';reason='Researcher/professional profile result, not a named new patient-enrolling anticancer protocol.'
 elif 'linkedin.com'in h and 'bennotx' in u:dis='WATCH_FUTURE_THERAPEUTIC_PROGRAMME';reason='Official company result describes ethical approval for dog UCC/HSA/OSA/melanoma proof-of-concept, first patient expected early2027; cat research starting at Ghent. Existing Benno official source read today; no current enrolling protocol or owner costs published.'
 elif 'linkedin.com'in h and any(k in u for k in ['akston-biosciences','the-cat-health-company','pennvet_tying','animal-cancer-center-at-nc-state']):dis='REJECT_NON_ONCOLOGY_OR_TRAINING';reason='Actual result is feline GLP1 obesity therapy, feline longevity development, equine myopathies, or oncology student rounds. No patient-enrolling anticancer protocol.'
 elif 'linkedin.com'in h and 'kopra-bio' in u:dis='REJECT_HUMAN_PRECLINICAL';reason='Human solid-tumour funding/platform signal, not dog/cat therapeutic enrollment.'
 elif 'linkedin.com'in h and 'fusfoundation' in u:dis='SECONDARY_RESEARCH_PROGRAMME';reason='Veterinary focused-ultrasound programme/fundraising or technology podcast; no named new owner-enrolling oncology protocol.'
 elif 'linkedin.com'in h:
  dis='EXISTING_PROTOCOL_SECONDARY_SIGNAL';reason='Named UCD canine PD-L1, UCSF/UCD feline oral cancer drug, or WSU/Suita/CAStr T-cell engager signal maps to an existing programme. Current institutional master comparison and primary gaps retained; historical/social post does not activate a new cohort or establish free care.'
  if 'pet-cancer-clinical-trials-free-or-discounted'in u or 'lack-unified'in u:dis='SECONDARY_DIRECTORY_OR_RECRUITMENT_MARKETING';reason='Directory launch/recruitment-platform discussion, not a named new treatment protocol; current secondary source separately reconciled.'
 elif related or any(k in h for k in ['uoguelph.ca','ovchsc.ca','ucdavis.edu']):dis='EXISTING_SOURCE_OR_PROTOCOL';reason='Actual returned source/programme mapped to current inventory and named-protocol comparisons. Primary gaps retained; no renewed clinical date from search or historical report.'
 elif h=='vettrialfinder.com':dis='EXCLUDE_OWN_SITE';reason='Own generated catalogue is not independent primary evidence.'
 elif any(k in h for k in ['couriermail','theaustralian','theverge','washingtonpost','sfchronicle','nhregister','reddit','brakkeconsulting']):dis='SECONDARY_KNOWN_OR_HISTORICAL_SIGNAL';reason='Known UQ/Gamgee/Yale/OSCC/ST sarcoma programmes or longevity/industry discussion. No newly verified owner treatment protocol from news or social discussion.'
 elif any(k in h for k in ['canada.ca','clinical-trials-search','recherche-essais','lungcancercanada','sanctr','careacross','ichgcp','healtrials','clinicaltrials.sg','gov.br','oncoguia','abhh','plataformacura','pesquisaoncologia','estudiosclinicos.cl','uofmhealth','binaytara','gilead','siemens']):dis='REJECT_HUMAN_TRIAL_OR_GENERAL_REGISTRY';reason='Actual result concerns human clinical trials, human pet-assisted therapy, regulators or general human research; no dog/cat anticancer intervention.'
 elif any(k in h for k in ['pmc.ncbi','pubmed.ncbi','sciencedirect','doi.org','visualize.jove','ajol.info','tezara','acikerisim','avesis','frontiersin','researchgate','jsvetsci','anicom','vetsci.gt','unam.mx','percdn','mahidol','thailand.go.th','chula.ac','zoetis','uspaberta']):dis='REJECT_PUBLICATION_PRECLINICAL_OR_EDUCATION';reason='Historical paper/thesis/review, preclinical/human platform, educational guideline or faculty/grant profile, not a current named owner-enrolling dog/cat treatment protocol. FAPESP-related abstract is not opened as a workaround.'
 elif 'vet.psu.ac.th'in h:dis='REJECT_NON_ONCOLOGY';reason='Actual named study concerns herbal spray for canine skin disease, not cancer treatment.'
 else:dis='EXCLUDE_CARE_DIRECTORY_TRAINING_OR_NOISE';reason='General care, clinic/association/industry home page, courses, jobs or unrelated result without a named recruiting therapeutic protocol. Outside this daily treatment-trial scope.'
 row.update(related_inventory_sources=related,disposition=dis,reason=reason)
wr(R/'discovery-matrix-final.json',{'reviewed_at':at,'regions':12,'passes':2,'matrix_queries':24,'targeted_queries':4,'languages':['English','French','German','Spanish','Portuguese','Japanese','Korean','Chinese','Hindi','Thai','Turkish','Arabic'],'rows':matrix,'scope_limit':'Regional search completion is not proof of global completeness or resolution of blocked official facts.'})
wr(R/'discovery-lead-dispositions.json',{'reviewed_at':at,'unique_result_urls':len(leads),'counts':dict(collections.Counter(x['disposition']for x in leads.values())),'rows':list(leads.values()),'primary_followups':['discovery-primary-1.json','attempts.jsonl','web-attempts.json','protocol-questions-and-decisions.json']})
print(json.dumps({'avma':len(av),'avma_oncology':len(base['rows']),'vettrials':len(vt),'oncology_signals':len(out),'unmatched':unmatched,'discovery_unique_urls':len(leads)},ensure_ascii=False))
