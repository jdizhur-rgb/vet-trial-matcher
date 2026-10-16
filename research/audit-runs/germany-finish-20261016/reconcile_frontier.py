"""Offline source-route review only. No source fetch, no provider verification."""
import json, pathlib, re, collections
from urllib.parse import urlsplit

OLD = pathlib.Path('/workspace/scratch/2d03a6db0cc6/eu6-20261016T142911-0400/research/audit-runs/eu6-20261016T142911-0400/worker-4')
OUT = pathlib.Path(__file__).parent
def read(p): return json.loads(p.read_text())
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows = read(OLD/'discovery-frontier/source-route-triage-block06.json')['records']
general = [r for r in rows if r['source_route_state']=='GENERAL_OR_OUTOFSCOPE_REFERENCE_LEAD_UNRECONCILED']
assert len(general)==333
provider_hosts = {'berlinvets.de','vet-chemnitz.de','tierzahnheilkunde-hamburg.de','tieraerztegmbh-hamburg.de','svea-lucas.de','tinodi24.com','haustierdocs.de','naftie-praxis.de','tierpsychologie-mobil.de','elementavet.com','plasmovet.com','tzn-bergheim.de','tebbe-vet.de','thevethouse.de','filu.vet','my.filu.vet','felmo.de','anicura.de'}
credential_hosts = {'symposien.vet','just4vets.online','dvg-vet-congress.de','d-nb.info','hundkatzepferd.com','images.leipziger-messe.de','fis-workmediagroup.de'}
university_hosts = {'vetmed.uni-muenchen.de','med.vetmed.uni-muenchen.de','tierkardiologie.uni-muenchen.de','vetmed.uni-leipzig.de','tiho-hannover.de','elib.tiho-hannover.de','fu-berlin.de','vetmed.fu-berlin.de','uni-giessen.de','studip.uni-giessen.de','jlupub.ub.uni-giessen.de','lmu.de'}
professional_hosts = {'tk-sh.de','ltk-bw.de','upgrade.ltk-bw.de','web.ltk-bw.de','bltk.de','ltk-brandenburg.de','ltk-hessen.de','ltk-rlp.de','ltkt.de','tk-st.de','vmf-online.de'}
thirdparty_vet = {'jameda.de','vetstage.de','arbeitsagentur.de','ava1.de','ocepaw.de','tieraerztewelt.de','katzenhilfe-bremen.de'}
decisions=[]
for r in general:
 u=r['url']; host=(urlsplit(u).hostname or '').removeprefix('www.'); title=r.get('title',''); path=urlsplit(u).path
 if host in provider_hosts:
  state='CLINICAL_OR_PROVIDER_ROUTE_SCOPE_UNRESOLVED'; reason='Provider/network/remote route; clinical facts require full permitted primary review, and lost held queue membership cannot be inferred from absence in partial list.'
 elif host in university_hosts:
  state='UNIVERSITY_NONCLINICAL_REFERENCE_OR_NEWS'; reason='University research, personnel, publication or construction source lead; not evidence of present owner treatment delivery. Clinical candidate routes remain separately held.'
 elif host in professional_hosts:
  state='PROFESSIONAL_ADMINISTRATIVE_REFERENCE_ONLY'; reason='Professional body, education, law, imprint or register route. Not an oncology provider or a clinical service proof.'
 elif host in credential_hosts:
  state='VETERINARY_PUBLICATION_OR_CONFERENCE_REFERENCE'; reason='Publication/conference discovery reference; cannot establish current clinical branch access without independent primary confirmation.'
 elif host in thirdparty_vet:
  state='THIRD_PARTY_PROVIDER_DISCOVERY_ONLY'; reason='Directory/job/industry lead; no primary verification or active modality inferred. Any linked candidate needs source-specific permission review.'
 elif host=='pferdeklinikwolfesing.de':
  state='EQUINE_ONLY_DISCOVERY_OUTSIDE_DOG_CAT_SCOPE'; reason='Saved route explicitly identifies an equine clinic; no dog/cat treatment evidence retained. Exclusion is source-lead scope, not a finding that clinic treats no other species.'
 elif host in {'reddit.com','facebook.com'}:
  state='SOCIAL_OR_ANECDOTAL_REFERENCE_ONLY'; reason='Social/anecdotal route, not primary clinical evidence; no outreach performed.'
 elif host.endswith('wikipedia.org'):
  state='ENCYCLOPEDIA_REFERENCE_NOT_PROVIDER'; reason='Encyclopedia route, not an official clinical provider source. No clinical outcome inferred from index label.'
 elif any(s in host for s in ['klinikum','kliniken','unimedizin','medizin.uni','med.uni','ukgm','uk-koeln','helios','asklepios','charite','onko-','aerzteblatt','krebshilfe','krebsinformation','mvz','degro','dgho','gpoh','laek-','aeksh','kvsa','kvbawue','kvno','kvhb','kvmv','kzv-lsa','gesundheitnord','diakobremen','wtz-essen','kem-med','caritasklinikum','kksaar','mhh.de','doccheck','selpers','jamanetwork','pubmed']):
  state='HUMAN_MEDICINE_OR_HUMAN_PROFESSIONAL_REFERENCE'; reason='Human medical/professional route visible in saved URL/title. It is not a dog/cat oncology provider source.'
 else:
  state='NONCLINICAL_ADMINISTRATIVE_OR_GENERAL_REFERENCE'; reason='Saved route is general government, legal, education, news, commercial or other nonclinical reference. Not a verified provider and not automatically discarded underlying veterinary signal.'
 decisions.append(dict(url=u,saved_title=title,discovery_shards=r.get('discovery_shards',[]),route_disposition=state,reason=reason,read_this_execution=False,provider_outcome_inferred=False,request_authorized=False))
write('general-333-route-review.json',dict(unit='source URL, not provider',total=len(decisions),counts=dict(collections.Counter(r['route_disposition'] for r in decisions)),records=decisions,network_requests=0))

remaining=read(OLD/'remaining-shards/named-provider-remainder-v7.json')['records']
def urls(v):
 if isinstance(v,str):
  return [v] if v.startswith(('https://','http://')) else []
 if isinstance(v,list): return sum((urls(x) for x in v),[])
 if isinstance(v,dict): return sum((urls(x) for x in v.values()),[])
 return []
named=[]
for r in remaining:
 c=read(OLD/r['current_candidate_record'])
 allurls=sorted(set(urls(c)+urls(r)))
 named.append(dict(candidate_id=r['candidate_id'],name=r['name'],previous_outcome=r['classification'],provider_processed=r['provider_processed'],missing_facts=r['missing'],saved_candidate=r['current_candidate_record'],known_exact_URLs=allurls,preserved_evidence_dates=r.get('actual_preserved_evidence_dates',[]),clinical_permission='HOLD_SCOPE_UNKNOWN; no request permitted',source_inventory_missing=True,request_made=False,required_review='Read only concrete official clinical/contact/team source after scope restoration or explicit permission; preserve clinician/modality separation, dedupe current main, never treat professional roster alone as local oncology evidence.'))
write('named-87-clinical-recovery.json',dict(total=len(named),units='candidate identities, not confirmed new clinics',counts=dict(collections.Counter(r['previous_outcome'] for r in named)),records=named,requests_made=0))
write('restrictions-preserved.json',read(OLD/'source-access-ledger.json'))
write('ready-four-proposals.json',read(OLD/'proposed_changes.json'))
write('retained-service-evidence.json',read(OLD/'input/inherited/retained-sh-evidence-partial.json'))
print(json.dumps({'route333':collections.Counter(r['route_disposition'] for r in decisions),'named87':len(named),'known_urls':len(set(u for r in named for u in r['known_exact_URLs']))},ensure_ascii=False))
