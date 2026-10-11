"""Assemble this run's actual evidence. HTTP retrieval is not semantic completion."""
import collections
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
NY = ZoneInfo('America/New_York')
def read(p): return json.loads(p.read_text())
def write(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def norm(u): return str(u).rstrip('/')
meta = read(RUN/'run.json')
ended = datetime.now(NY).isoformat()
before = read(RUN/'oncology_care_source_inventory.json.before')
inventory = read(ROOT/'data/oncology_care_source_inventory.json')
pages = [read(p) for p in (RUN/'pages').glob('*.json')]
by_url = collections.defaultdict(list)
for page in pages:
    by_url[norm(page['url'])].append(page)
acvim=read(RUN/'acvim-execution.json')
by_url[norm(acvim['url'])].append({'url':acvim['url'],'attempted_at':acvim['attempted_at'],'method':acvim['method'],'http_status':None,'error':acvim['error'],'evidence_file':'acvim-execution.json','semantic_review':'Complete current US oncology roster extracted: 458 profiles; affiliations are not branch treatment proof.'})
for v in by_url.values(): v.sort(key=lambda x: x['attempted_at'])
fetches = {}
for p in RUN.glob('*fetches.json'):
    val = read(p)
    if isinstance(val, list):
        fetches[p.name] = val

proposed = read(RUN/'verified-additions-proposed.json')
adds = [r for r in proposed if 'Western College' not in r['name'] and 'WCVM' not in r['name']]
medchanges = read(RUN/'medvet-canonical-changes.json')
adds += [r['after'] for r in medchanges if r['classification']=='new_center']
tele = [
 ('Pet Cancer Consulting Inc. / Kim Johnson','https://www.petcancerconsulting.com/','https://www.petcancerconsulting.com/about'),
 ('CVS Collaborative Cancer Care / VetOracle Teleoncology','https://cvs-referrals.com/referrals/vet-oracle/teleoncology/','https://www.cvsukltd.co.uk/news/cvs-launches-new-cancer-care-service-to-support-veterinary-practices/'),
 ('KumAda Veteriner Onkoloji','https://veterineronkoloji.com/online-konsultasyon/','https://veterineronkoloji.com/ekibimiz/'),
]
verified = {norm(r['verification_url']) for r in adds}
verified |= {norm(r['after']['verification_url']) for r in medchanges}
verified |= {norm(r[1]) for r in tele}
verified |= {f'https://mirpet.co.jp/app/owner/clinic/detail/{n}' for n in [136,74,208,129,299]}
verified.add('https://www.akiyoshi-ac.com/online')
# All seven primary location pages were read beyond the global navigation.
verified |= {norm(r['url']) for r in fetches['network-followup-fetches.json'] if 'petcureoncology.com/locations/' in r['url']}
rename=[]; used=set()
for i, source in enumerate(inventory['sources']):
    sid=source['id']
    if sid in used:
        new=sid+'-'+hashlib.sha256(source['master_url'].encode()).hexdigest()[:8]
        if new in used: new += '-'+str(i)
        rename.append({'original_index':i,'legacy_id':sid,'master_url':source['master_url'],'new_id':new})
        source['legacy_id']=sid; source['id']=new
    used.add(source['id'])
for name, url, support in [(r['name'],r['verification_url'],'') for r in adds] + tele:
    if any(s['name']==name and norm(s['master_url'])==norm(url) for s in inventory['sources']): continue
    sid='discovered-'+hashlib.sha256((name+url).encode()).hexdigest()[:14]
    inventory['sources'].append({'id':sid,'name':name,'source_type':'teleconsult_service' if any(name==t[0] for t in tele) else 'center', 'master_url':url,'supporting_urls':[support] if support else [],'required_cadence':'weekly','last_checked':None,'last_checked_at':None,'last_result':'pending'})

# Current official alternatives, actually attempted during this run.
alternatives={
 'network-ethos':['https://www.ethosvet.com/our-hospitals/','https://www.ethosvet.com/locations/','https://www.ethosvet.com/hospital-sitemap.xml'],
 'network-thrive':['https://www.thrivepetcare.com/location','https://www.thrivepetcare.com/veterinary-groups/veterinary-cancer-group'],
}
verified_alternates={}
for s in inventory['sources']:
    extras=[]
    if s['id']=='acvim-board-certified-veterinary-oncologists':
        extras.append(acvim['url']); verified_alternates[s['id']]=acvim['url']
    for change in medchanges:
        if change['before'] and s['master_url']==change['before'].get('verification_url'):
            extras.append(change['after']['verification_url']); verified_alternates[s['id']]=change['after']['verification_url']; s['name']=change['after']['name']
    extras+=alternatives.get(s['id'],[])
    if 'avets.com/service/oncology' in s['master_url']: extras += ['https://www.avets.com/services/oncology']
    for url in extras:
        if norm(url) in by_url or any(norm(r.get('url'))==norm(url) for v in fetches.values() for r in v):
            if url not in s['supporting_urls']: s['supporting_urls'].append(url)

receipt=[]; gaps=[]
original_by_key={(s['id'],s['master_url']):s for s in before['sources']}
for source in inventory['sources']:
    sid=source['id']; old=original_by_key.get((source.get('legacy_id',sid),source['master_url']),{})
    urls=[source['master_url']]+source.get('supporting_urls',[])
    attempts=[]
    for u in urls:
        for page in by_url.get(norm(u),[]):
            attempts.append({'url':u,'attempted_at':page['attempted_at'],'method':page.get('method','shell.urllib'),'http_status':page.get('http_status'),'outcome':'success' if page.get('semantic_review','').startswith('Complete current US oncology roster') else 'partial' if page.get('http_status')==200 else 'unreachable','error':page.get('error'),'fingerprint_sha256':page.get('fingerprint_sha256'),'semantic_review':'not completed' })
        for fn, rows in fetches.items():
            for r in rows:
                if norm(r.get('url'))==norm(u) and not any(a['attempted_at']==r['attempted_at'] for a in attempts):
                    attempts.append({**r,'outcome':'partial' if r.get('http_status')==200 else 'unreachable','method':'shell.urllib','semantic_review':'not completed'})
        for fp in RUN.glob('inventory-web-fallback-*.json'):
            fallback=read(fp)
            if norm(u) in {norm(x) for x in fallback['urls']}:
                attempts.append({'url':u,'attempted_at':fallback['attempted_at'],'method':'web.open','outcome':'partial','evidence_file':fp.name,'semantic_review':'fallback may be cached or empty; not blanket success'})
    sufficient=norm(source['master_url']) in verified or sid in verified_alternates
    status='success' if sufficient else 'partial' if any(a.get('http_status')==200 or a['method']=='web.open' for a in attempts) else 'unreachable'
    if not attempts: raise RuntimeError('Missing actual attempt: '+sid+' '+source['master_url'])
    latest=max(attempts,key=lambda a:datetime.fromisoformat(a['attempted_at'].replace('Z','+00:00')))
    at=datetime.fromisoformat(latest['attempted_at'].replace('Z','+00:00')).astimezone(NY)
    source.update(last_checked=at.date().isoformat(),last_checked_at=at.isoformat(),last_result=status,content_sufficient=sufficient)
    source['last_run_id']=meta['run_id']
    source['last_review_note']='Current branch-specific service evidence reviewed; full audit remains incomplete.' if sufficient else 'Actual source attempt persisted; current care/credentials/location reconciliation unfinished. HTTP 200 is not success.'
    source['http_status']=latest.get('http_status')
    if sufficient:
        for a in attempts: a['outcome']='success' if a.get('http_status')==200 else a['outcome']
    entry={'source_id':sid,'name':source['name'],'master_url':source['master_url'],'before_last_checked':old.get('last_checked'),'before_last_checked_at':old.get('last_checked_at'),'after_last_checked':source['last_checked'],'after_last_checked_at':source['last_checked_at'],'opened_this_run':True,'attempted_urls':attempts,'master_result':status,'content_sufficient':sufficient,'protocols_seen':458 if sid=='acvim-board-certified-veterinary-oncologists' else 1 if sufficient else None,'route_used':verified_alternates.get(sid,source['master_url']),'care_service_count':1 if sufficient else None,'count_semantics':'individual care-service source, not a trial protocol','processing_complete':sufficient}
    receipt.append(entry)
    if not sufficient:
        gaps.append({'source_id':sid,'category':'roster_unestablished','processing_assessment':'executor_unfinished','question':'Is this source currently providing the listed oncology care at this physical branch or via the documented teleconsultation route?','reason':'Retrieval attempts are recorded, but branch identity, service access and/or current credentials have not all been reconciled. No external-blocker or success claim is made.','next_action':'Read the captured current official source and its listed official alternatives; reconcile treatment location, clinician credentials and access with the canonical record.','unperformed_steps':['Current semantic branch/service/credential reconciliation against canonical care catalog'],'evidence':{'source_id':sid,'attempted_urls':list(dict.fromkeys(a['url'] for a in attempts))}})
write(ROOT/'data/oncology_care_source_inventory.json',inventory)
write(RUN/'source-id-rename-map.json',rename)
final={'schema_version':1,**meta,'ended_at':ended,'status':'INCOMPLETE','source_total':len(receipt),'original_source_total':len(before['sources']),'attempted_total':len(receipt),'content_sufficient_total':sum(r['content_sufficient'] for r in receipt),'sources':receipt}
write(RUN/'receipt-final.json',final)
write(RUN/'gap-review.json',{'original_run_id':meta['run_id'],'reviewed_at':ended,'rows':gaps})
write(ROOT/'data/oncology_care_audit_coverage.json',final)

searches=[]
for path in sorted(RUN.glob('search-*.json')):
    row=read(path)
    if not row.get('area') and not row.get('region'):continue
    clean={k:v for k,v in row.items() if k!='result'}
    clean['raw_evidence_file']=path.name
    clean['result_scope']='Captured search batch response; URLs can belong to another query in the same batch. Counts must not be summed as distinct geography-specific primary-page visits.'
    clean['review_method']='automated result URL and snippet screening; selected primary pages fetched separately; not all candidates semantically reconciled'
    searches.append(clean)
areas=sorted({r['area'] for r in searches if 'area' in r})
regions=sorted({r['region'] for r in searches if 'region' in r})
candidates=[]
for i,r in enumerate(adds):
    classification='new_service' if 'Kyoto' in r['name'] else 'new_center'
    candidates.append({'id':'verified-center-'+str(i),'name':r['name'],'official_url':r['verification_url'],'classification':classification,'verified_official_service_page':r['verification_url'],'canonical_reconciled':True,'newly_opened_physical_clinic':False,'note':'New to directory; opening date not asserted. KyotoAR is a new cancer service within an existing hospital.'})
for i,(name,url,_) in enumerate(tele):
    candidates.append({'id':'verified-tele-'+str(i),'name':name,'official_url':url,'classification':'new_teleconsult','verified_official_service_page':url,'canonical_reconciled':True})
for i,r in enumerate(medchanges):
    if r['classification']=='update':candidates.append({'id':'medvet-update-'+str(i),'name':r['after']['name'],'official_url':r['after']['verification_url'],'classification':'update','canonical_reconciled':True})
pending=[
 ('ACCESS Pasadena','https://accessvetspasadena.com/oncology/','Future oncology launch; late 2026 does not prove current treatment.'),
 ('Safe Haven Wexford','https://safehavenpethospital.com/oncologist/','Oncologist vacancy / proposed department is not proof of current oncology.'),
 ('Pet Cancer Center of Providence','https://job-boards.greenhouse.io/pcc-ri/jobs/5235794007?gh_src=8e5ac79n7us','Soon-to-launch recruitment; active care not established.'),
 ('PetCancerInformation Alaska ECT partner','https://www.petcancerinfo.com/locations/alaska','Unidentified host; actual ECT administration address not established.'),
 ('VETINPARIS oncology','https://www.vetinparis.com/cancerologie-veterinaire-paris','Current service at 89 Rue du Faubourg Saint-Antoine; coordinates and complete identity reconciliation unfinished; do not transfer to other branch.'),
 ('OncoHealth Ribeirao Preto','https://oncohealth.vet.br/','Current physical chemotherapy/surgery; coordinates unfinished. Not a verified teleconsultation.'),
 ('Nouvet Sao Paulo','https://nouvet.com.br/oncologia/','Current physical chemotherapy/ECT; coordinates unfinished. Not a verified teleconsultation.'),
 ('Honeydew Animal Clinic','https://www.honeydewanimalclinic.co.za/oncology','Chemotherapy current; exact coordinates and ECT administration site unconfirmed.'),
 ('Fernridge Veterinary Clinic','https://www.fernvet.co.za/services/','Chemotherapy current; coordinates unfinished; radiation is external referral.'),
 ('MOVES Colorado hosts','https://www.vetmoves.com/refer/colorado/','Named hosts found; branch-specific chemotherapy administration addresses still require verification. Radiation oncologist credential is not mobile radiation equipment.'),
 ('VCA Veterinary Care Albuquerque','https://vcahospitals.com/veterinary-care/specialty/departments/oncology','Current address found; relationship to older Montgomery Blvd entry remains unresolved.'),
 ('VCA West Los Angeles','https://vcahospitals.com/west-los-angeles/specialty/departments/oncology','Current services found; relationship to older Sepulveda entry remains unresolved.'),
 ('UC Davis Hobbs San Diego','https://hobbs.vetmed.ucdavis.edu/news/we-have-walls-center-taking-shape','Construction / future opening is not current treatment access.'),
 ('Missouri Animal Cancer Care radiation','https://macc.vet/','Medical oncology verified; onsite radiation not established; no radiation tag added.'),
]
for i,(name,url,note) in enumerate(pending):candidates.append({'id':'unresolved-'+str(i),'name':name,'official_url':url,'classification':'unresolved','canonical_reconciled':False,'note':note})
for i,(name,url,note) in enumerate([
 ('ONCOnseil France','https://onconseil.com/je-suis-veterinaire/','Current service explicitly closed; rejected new teleconsult lead, not a closure of an existing canonical record.'),
 ('Desert View','https://dvah.com/oncology/','Referral list, not demonstrated onsite treatment.'),
 ('Fairhaven Veterinary Hospital','https://fairhavenvet.com/veterinary-oncology/','Referral partners, not demonstrated onsite chemotherapy.'),
 ('WCVM','https://vmc.usask.ca/','Already present; no duplicate added.'),
 ('Nebraska Animal Medical Center','https://namcvet.com/','Already present; no duplicate added.'),
]):candidates.append({'id':'rejected-'+str(i),'name':name,'official_url':url,'classification':'duplicate' if 'Already present' in note else 'rejected','canonical_reconciled':True,'note':note})

def attempts_for(files, extras=()):
    result=[]
    for fn in files:
        for a in fetches.get(fn,[]):
            result.append({**a,'outcome':'partial' if a.get('http_status')==200 else 'unreachable'})
    for url in extras:
        for pg in by_url.get(norm(url),[]):result.append({'url':url,'attempted_at':pg['attempted_at'],'outcome':'partial' if pg.get('http_status')==200 else 'unreachable','http_status':pg.get('http_status')})
    return result
network=[]
specs=[
 ('PetCure',[],7,7,7,7,['https://petcureoncology.com/locations/']),
 ('BluePearl',['bluepearl-branch-fetches.json','bluepearl-services-fetches.json','bluepearl-oncology-primary-fetches.json'],93,40,93,0,['https://bluepearlvet.com/hospital/']),
 ('VCA',['vca-service-fetches.json','vca-gap-followup-fetches.json'],102,102,102,0,[]),
 ('Ethos',['ethos-branch-fetches.json','ethos-known-brand-fetches.json'],144,0,144,0,['https://www.ethosvet.com/our-hospitals/','https://www.ethosvet.com/hospitals/']),
 ('MedVet_WestVet',['medvet-branch-fetches.json','medvet-oncology-master-fetches.json'],40,19,40,19,['https://www.medvet.com/locations/']),
 ('Thrive_VCG',[],0,0,0,0,['https://www.thrivepetcare.com/locations','https://www.thrivepetcare.com/location','https://www.thrivepetcare.com/veterinary-groups/veterinary-cancer-group']),
 ('Universities',['university-primary-fetches.json'],30,30,22,0,[]),
]
for name,files,roster,cand,checked,confirmed,extras in specs:
    attempts=attempts_for(files,extras)
    if name=='PetCure':attempts += [{**r,'outcome':'success'} for r in fetches['network-followup-fetches.json'] if 'petcureoncology.com/locations/' in r['url']]
    if name=='Thrive_VCG':attempts+= [{**r,'outcome':'partial' if r.get('http_status')==200 else 'unreachable'} for r in fetches['network-followup-fetches.json'] if 'thrivepetcare.com/' in r['url']]
    network.append({'network':name,'status':'partial','master_sufficient':False,'attempts':attempts,'roster_locations':roster,'candidate_oncology_locations':cand,'branch_pages_checked':checked,'confirmed_oncology':confirmed,'unresolved_locations':max(roster-confirmed,0),'state_sitemaps_checked':48 if name=='VCA' else 0,'brands_checked':len(fetches['ethos-known-brand-fetches.json']) if name=='Ethos' else 0,'count_notes':'Roster/candidate retrieval counts are not a claim of full branch/catalog reconciliation. Zero confirmed means uncounted semantic confirmation, not zero oncology services. Thrive roster remains unknown; Ethos 144 historic sitemap routes redirect to generic content; 29 brand candidates are not a verified complete ownership roster.'})
discovery={'schema_version':1,'run_id':meta['run_id'],'started_at':meta['started_at'],'ended_at':ended,'status':'INCOMPLETE','review_semantics':'Results reviewed = automated URL/snippet screening; primary-page attempts and incomplete semantic reconciliation reported separately. No unperformed region is counted as zero findings.','us_areas':[{'area':a,'status':'partial','searches':[r for r in searches if r.get('area')==a],'gap':'Searches executed; exhaustive lead-to-canonical semantic reconciliation unfinished.'} for a in areas],'global_regions':[{'region':a,'status':'partial','searches':[r for r in searches if r.get('region')==a],'gap':'Native-language searches executed; exhaustive lead-to-canonical semantic reconciliation unfinished.'} for a in regions],'network_traversals':network,'candidates':candidates}
write(RUN/'care-discovery-receipt.json',discovery)
write(RUN/'pending-discovery-leads.json',{'run_id':meta['run_id'],'status':'INCOMPLETE','candidate_pool':read(RUN/'discovery-screened-leads.json'),'explicit_pending_candidates':pending,'next_action':'Reconcile each screened lead against the full catalog and verify official current treatment/branch/credentials before inclusion.'})
local=read(ROOT/'data/oncology_care_source_inventory.json')
checks=[{'source_id':r['source_id'],'pass':any(s['id']==r['source_id'] and s['last_checked_at']==r['after_last_checked_at'] and s['last_checked']==r['after_last_checked'] and s['last_result']==r['master_result'] for s in local['sources'])} for r in receipt]
write(RUN/'dates-local-readback.json',{'checked_at':datetime.now(NY).isoformat(),'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','sources':checks})
print(json.dumps({'sources':len(receipt),'sufficient':sum(r['content_sufficient'] for r in receipt),'id_collisions_repaired':len(rename),'searches':len(searches),'US':len(areas),'global':len(regions),'new_physical_catalog_entries':len(adds),'new_tele':len(tele)},indent=2))
