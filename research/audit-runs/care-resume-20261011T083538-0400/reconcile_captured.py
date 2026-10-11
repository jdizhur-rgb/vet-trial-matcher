"""Conservative evidence checks; missing proof stays partial, never HTTP=success."""
import json,re,collections,urllib.parse
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parent
PARENT=ROOT/'research/audit-runs/care-20261011T065613-0400'
def read(p):return json.loads(p.read_text())
def norm(u):
 p=urllib.parse.urlsplit(u or '');return urllib.parse.urlunsplit(('https',p.netloc.lower().removeprefix('www.'),p.path.rstrip('/'),p.query,''))
def plain(s):return re.sub(r'[^a-z0-9]','',s.lower())
pages=collections.defaultdict(list)
for p in list((PARENT/'pages').glob('*.json'))+list((RUN/'pages').glob('*.json')):
 d=read(p);d['evidence_file']=str(p.relative_to(ROOT));pages[norm(d['url'])].append(d)
plan=read(RUN/'remaining-source-plan.json');output=[]
medvet={norm(r['url']):r for r in read(PARENT/'medvet-branch-review.json')}
for r in plan:
 evidence=[];approved=[];candidate_clinics=r['canonical_candidates'];profile=r['profile']
 for url in r['official_urls']:
  if 'vetspecialists.com' in url:continue
  for pg in pages.get(norm(url),[]):
   if pg.get('http_status')!=200:continue
   text=pg.get('text','');lower=text.lower();path=urllib.parse.urlsplit(url).path.lower()
   if len(text)<200 or re.search(r'page (?:not found|does not exist)|404 not found',lower[:500]):continue
   carewords=[m for m in re.finditer(r'oncolog|chemotherap|radiation therap|electrochem|teleconsult|telemed|second.opinion|online consult',text,re.I)]
   windows=[text[max(0,m.start()-160):min(len(text),m.end()+250)] for m in carewords]
   clinics=[]
   for c in candidate_clinics:
    digits=re.sub(r'\D','',text);phone=re.sub(r'\D','',c.get('phone',''))[-10:]
    phone_match=len(phone)==10 and phone in digits
    zip_match=bool(c.get('postal_code')) and c['postal_code'] in text
    name_match=plain(c['name'].removeprefix('VCA ')) in plain(text[:1800])
    street_number=re.match(r'\d+',c.get('street',''))
    address_match=bool(street_number and street_number.group() in text and zip_match and c['city'].lower() in lower)
    same_host=urllib.parse.urlsplit(url).netloc.removeprefix('www.')==urllib.parse.urlsplit(c.get('website','')).netloc.removeprefix('www.')
    identity=address_match and (phone_match or name_match) and same_host
    clinics.append({'name':c['name'],'phone_match':phone_match,'postcode_match':zip_match,'title_name_match':name_match,'address_match':address_match,'same_host':same_host,'identity_sufficient':identity})
   future=any(re.search(r'coming soon|will (?:open|offer|provide)|expected to open|soon.to.launch',w,re.I) for w in windows)
   service_path=bool(re.search(r'oncolog|chemotherap|cancer-care|cancer-treatment|electrochem|radiation',path)) and not bool(re.search(r'/blog|/news|/article|/team|/staff|/doctor|/provider',path))
   treatment=bool(re.search(r'chemotherap|radiation therap|electrochem|cancer treatment|treatment (?:options|plan)|manage.{0,15}cancer',lower))
   active_offer=any(re.search(r'(?:we|our|team|hospital|clinic).{0,80}(?:offer|provid|administer|treat)|(?:offer|provid|administer).{0,100}(?:chemotherap|oncolog|radiation)',w,re.I|re.S) for w in windows)
   credential=bool(profile and 'DACVIM (Oncology)' in profile['name']) or bool(re.search(r'DACVIM.{0,30}Oncology|DipECVIM|JVCS|FANZCVS.{0,25}Oncology',text,re.I))
   specialist_source=bool(profile)
   entry={'url':url,'evidence_file':pg['evidence_file'],'actual_attempted_at':pg['attempted_at'],'inherited_visit':PARENT.name in pg['evidence_file'],'branch_identity_checks':clinics,'service_path':service_path,'treatment_text':treatment,'explicit_active_offer':active_offer,'future_signal':future,'credential_evidence':credential,'clinical_excerpts':windows[:8]}
   sufficient=False
   if r['source_type']=='center':
    sufficient=any(c['identity_sufficient'] for c in clinics) and service_path and treatment and active_offer and not future and (credential or not specialist_source)
    # MedVet local service block precedes global footer and was explicitly read.
    mv=medvet.get(norm(url))
    if mv and 'Medical Oncology' in mv['services'] and any(c['address_match'] and c['same_host'] for c in clinics) and credential:
     sufficient=True;entry['verified_rule']='Current local Specialty Services at <branch> block, branch address, current oncology clinician roster'
   entry['sufficient']=sufficient
   if sufficient:approved.append(entry)
   evidence.append(entry)
 missing=[]
 if not approved:
  if not evidence:missing.append('No usable current clinical body after captured primary-route attempts')
  elif r['source_type']=='teleconsult_service':missing.append('Audience, remote service/booking and doctor/fee/records details require individual semantic reconciliation')
  elif r['source_type']=='network_master':missing.append('Full current roster, branch-level reconciliation and aliases require individual traversal proof')
  else:missing.append('Current local treatment/branch identity/credentials are not all established by conservative checks; read exact evidence and applicable next official routes')
 output.append({'source_id':r['source_id'],'name':r['name'],'reviewed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'review_method':'Conservative explicit-text and physical identity reconciliation; no success from HTTP alone','content_sufficient':bool(approved),'verified_primary_urls':list(dict.fromkeys(e['url'] for e in approved)),'missing_facts':missing,'evidence':evidence})
(RUN/'semantic-reconciliation.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'remaining_processed':len(output),'sufficient_candidates':sum(r['content_sufficient'] for r in output),'still_partial':sum(not r['content_sufficient'] for r in output),'captured_pages':sum(len(v) for v in pages.values())},indent=2))
for r in output:
 if r['content_sufficient']:print(r['source_id'],r['verified_primary_urls'][:2])
