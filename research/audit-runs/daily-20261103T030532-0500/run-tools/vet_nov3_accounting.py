import json,pathlib,hashlib,re,sys
from collections import Counter,defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500';sys.path.insert(0,str(ROOT/'scripts'))
import audit_execution_gate as gate
def rd(p):return json.loads(p.read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ref(p):return str(p.relative_to(ROOT))
def now():return datetime.now(ZoneInfo('America/New_York')).isoformat()
def norm(u):return str(u).rstrip('/')
E=[rd(p) for p in (R/'evidence').glob('*.json')]; byurl=defaultdict(list)
for e in E:byurl[norm(e['url'])].append(e)
I=rd(R/'baseline-source_inventory.json');S=rd(R/'individual-source-decisions.json');B=rd(R/'execution-baseline.json');C=rd(ROOT/'data/trials_base.json');C0={x['id']:x for x in rd(R/'baseline-trials_base.json')};CT={x['id']:x for x in C};at=now()
S['australia-caninecancer-state-research-guide']['reviewed_at']=at
web=[]
def webtime(x):
 if isinstance(x,dict):x=x.get('current_time')
 return datetime.strptime(x,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).isoformat() if ' UTC' in str(x) else x
for p in R.glob('web-*.json'):
 x=rd(p);text='\n'.join(c.get('text','') for c in x['result'].get('content',[]) if c.get('type')=='text')
 for u in x.get('urls',[]):
  if not isinstance(u,str):continue
  parts=text.split('--------------------------------------------------------------------------------');part=next((s for s in parts if u in s),text)
  web.append({'url':u,'method':'Web','attempted_at':webtime(x.get('started_at',x.get('start'))),'completed_at':webtime(x.get('completed_at',x.get('end'))),'evidence_file':ref(p),'new_source_visit':True,'result':'web_unavailable' if 'is not accessible via this tool' in part or 'Failed to fetch' in part else 'web_retrieved_content','http_status':None,'retrieved_text_excerpt':part[:1200],'freshness':'Crawl/cache metadata preserved in original Web artifact; no independent server-freshness claim.'})
def attempts_for(u):return byurl.get(norm(u),[])+[w for w in web if norm(w['url'])==norm(u)]
# Current source decisions were individually written while reading. Associate the actual document comparisons, not yesterday's result.
changes=rd(R/'all-changed-document-reviews.json');receipt=[]
def slim(e):return {k:v for k,v in e.items() if k not in ['text','links','public_content','clinical_text','retrieved_text_excerpt']}
for inv in I['sources']:
 sid=inv['id'];d=S[sid];es=[e for e in E if e.get('source_id')==sid]
 urls={norm(inv['master_url'])}|{norm(u) for u in inv.get('fallback_urls',[])}|{norm(e['url']) for e in es}
 es+= [e for e in E if norm(e['url']) in urls and e not in es]
 ws=[w for w in web if norm(w['url']) in urls];ats=[slim(e) for e in es]+ws
 d['evidence_refs']=list(dict.fromkeys(d['evidence_refs']+[e['evidence_file'] for e in es]+[w['evidence_file'] for w in ws]))
 relevant=[x for x in changes if x['source_id']==sid or norm(x['url']) in urls]
 d['change_reviews']=[{k:x[k] for k in ['current_evidence','finding','catalog_impact']} for x in relevant]
 d['remaining_available_steps']=d.get('remaining_available_steps',[])
 # Do not elevate Web cache recovery or partial protocol evidence to full current roster proof.
 source={'source_id':sid,'source_name':inv['name'],'opened_this_run':any(a.get('new_source_visit') for a in ats),'attempted_urls':ats,'route_used':list(dict.fromkeys(a['method'] for a in ats)), 'protocols_seen':len(d['protocols']) if d['roster_complete'] else None,'protocols':d['protocols'],'current_roster':d['protocols'] if d['roster_complete'] else None,'current_content_comparison':[{k:x[k] for k in ['url','current_evidence','previous_evidence','whole_text_equal']} for x in relevant],'processing_complete':d['processing_complete'],'previous_last_checked':inv.get('last_checked'),'previous_last_checked_at':inv.get('last_checked_at'),'previous_fingerprint':inv.get('content_fingerprint'),'finding':d['finding'],'catalog_comparison':d['catalog_comparison']}
 source['content_sufficient']=gate.current_source_sufficient(source,d,ROOT,gate.timestamp(B['started_at']),gate.timestamp(at))
 source['master_result']='checked' if source['content_sufficient'] else 'partial' if d.get('current_official_content') or any(a.get('result') in ['retrieved_page','web_retrieved_content'] for a in ats) else 'unreachable' if source['opened_this_run'] else 'not checked'
 actual=[a for a in ats if a.get('new_source_visit')];last=max(actual,key=lambda a:a['completed_at']) if actual else None
 source['new_last_checked_at']=last['completed_at'] if last else inv.get('last_checked_at');source['new_last_checked']=datetime.fromisoformat(last['completed_at']).astimezone(ZoneInfo('America/New_York')).date().isoformat() if last else inv.get('last_checked')
 currenthashes=[e.get('text_sha256') for e in es if e.get('text_sha256') and e.get('new_source_visit')]
 source['current_evidence_sha256']=hashlib.sha256(json.dumps(currenthashes).encode()).hexdigest() if currenthashes else None
 receipt.append(source)
wr(R/'individual-source-decisions.json',S)
Q=[]
for p in sorted(R.iterdir()):
 if re.fullmatch(r'discovery-\d+\.json',p.name):
  x=rd(p)
  for q in x['queries']:Q.append({**q,'query':q['q'],'evidence_refs':[ref(p)]})
# Each inherited issue is re-adjudicated against today's exact route result and current corroboration.
special={
'eu-fr-hifu-urothelial':'Current Oncowaf/ESVONC HIFU-UCC listing corroborates the exact Armonia intervention. The institutional individual remains under its exact restriction; the current standard-treatment-failed/inapplicable/refused screening and local fees cannot be completed from the secondary roster.',
'ncsu-mammary-inspire':'Current NCSU roster still names mammary INSPIRE. The individual exact route is held; neither the roster nor registry recruiting establishes all1–3cm, weight/spay/metastasis exclusions or present owner charges.',
'uga-bcell-ivp':'Both UGA indexes and the individual B-cell IVP route retain exact restrictions. Today no current permitted primary identifies the unnamed agent/cohort; Ethos age/weight similarity was explicitly rejected as identity evidence.',
'wsu-sts-local-immunotherapy':'Current CASTR T-cell-engager protocol and exact AVMA28496 were reconciled; the published biological-effect/safety scope and old surgery-credit benefit still require owner inclusion judgment. VRCCO exact restriction cannot establish WSU intake.',
'wisc-ptcl-90y-nm600-rpt':'AVMA current roster corroborates the separate 90Y-NM600 PTCL identity. Wisconsin master/PTCL primary is restricted; today HBRT/FLASH full reviews do not establish PTCL intake, eligibility or cost terms.',
'ethos-gilvetmab-melanoma':'Current permitted registry/network signals identify the gilvetmab melanoma program, while the exact Ethos individual remains restricted. Whole present allocation and mandatory standard-care/owner costs are not published in the permitted source evidence.',
'ethos-bcell-oral':'The exact Ethos unnamed oral B-cell study route remains held. No current allowed primary names the agent/cohort or full medical/cost rules; no merge with UGA IVP is justified.',
'ethos-osa-vaccine':'The sponsor OSA vaccine exact protocol remains restricted. Other current OSA vaccine invitations are distinct protocols and cannot establish this cohort, whole site roster or subsidy.',
'tamu-mct-acid-suppressant':'The exact TAMU GI-lab study page remains held. Other TAMU oncology protocols were read separately; they do not answer whether this acid-suppressant cohort funds definitive tumor surgery or only supportive research.',
'ethos-solid-relapse':'Current Metropolitan primary names SOLID at Akron/Cleveland. This is affirmative local corroboration, not complete corporate allocation/current relapse criteria and cost evidence; exact sponsor individual remains held.',
'ethos-epush-hsa':'Current Metropolitan primary names PUSH Akron, conditional phase1 $1000 surgery credit and phase2 funded oncologic care. No blanket phase/site/current intake is inferred; the complete exact sponsor protocol remains held.',
'ethos-mimic-osa-lung':'The current AVMA MIMIC identity supports mandatory VATS metastasectomy already represented canonically. Exact Ethos primary is held; full current local intake, weight/disease criteria and owner fees are not newly verified.',
'anivive-sine-osa-carboplatin':'Today-crawled same-URL Web sponsor invitation says Recruiting SINE/verdinexor+carboplatin OSA. The exact AniTrial protocol is held and prior cohort was completed; sponsor card does not prove a reopened Cornell cohort or costs. Midwestern unnamed chemotherapy is a different unresolved lead.',
'uk-ndsr-osa-rfil2-watch':'Current permitted regional directories do not publish a new individual rFIL2 intake/cost protocol. The exact NDSR OSA route is held; old study descriptions are not present enrollment proof.',
'eu-uk-ndsr-high-grade-mammary-current':'NDSR individual high-grade mammary route remains under exact restriction. Current directories/news do not establish this specific intervention, screening or owner fees; no other mammary protocol is substituted.',
'ncsu-canine-sts-xcsgel':'Current NCSU roster still names the STS gel program; its individual primary is held. Known Aug31,2027 end-date evidence is preserved with its original date, not reread today; full surgical/lesion/owner-cost criteria remain unknown.',
'ncsu-feline-oral-pivot-c':'Current NCSU roster names PIVOT-C. Its exact individual is held. AVMA enhanced ethanol ablation is a different feline oral-SCC intervention and was not merged; PIVOT-C full concurrent therapy/fees remain unverified.',
'umn-feline-mammary-olaparib-meloxicam':'UMN exact olaparib primary and index are held. Ohio State mammary imaging registry20735 was individually rejected as a substitute therapeutic identity; no current permitted full UMN criteria/cost protocol recovered.',
'penn-flash-rt-extremity-sts':'Penn exact FLASH extremity primary remains held. Current Wisconsin FLASH documents were read but represent a different cohort; their mandatory amputation and subsidy cannot be transferred to Penn.',
'penn-psma-theranostic-prostate':'Penn exact PSMA prostate primary remains held. Current registry identity signals do not independently settle this individual cohort intake or screening-versus-treatment charges.',
'umn-canine-oral-melanoma-aav-vaccine':'UMN exact AAV vaccine primary remains held. Current LCMV/TIL registry21453 is a different cellular/vaccine protocol, not a replacement for this cohort or its owner charges.',
'ch-anicura-aoi-superficial-tumor-immunocytokines':'AOI exact immunocytokine therapy page remains held. Newly read Zurich ADAM12 feline phase0 vaccine is a separate intervention and does not establish AOI intake, medical screening or benefit/cost scope.',
'china-petcura-personalized-mrna-iit-2026':'The exact PetCura personalized mRNA IIT invitation remains held. Current China discovery did not recover a permitted complete owner protocol; promotional/regulatory signals do not establish site allocations or funded care.',
'jhu-cigat-osa-cryo-immunotherapy-2026':'CIGAT exact clinical-trials route remains held. Current registry signals were compared by OSA cryo-immunotherapy identity; actinium metastatic OSA is distinct and cannot supply amputation/chemotherapy/cost facts.',
'jhu-cigat-brain-rt-tmz-2026':'CIGAT brain RT/TMZ individual facts remain behind the exact clinical-trials restriction. Current UCD CARE/PRISM primary reviews are distinct glioma protocols and do not resolve this question.',
'jhu-cigat-mammary-kubanda-cryo-2026':'CIGAT Kubanda mammary cryotherapy remains separately identified with the exact primary restriction. Today no permitted document establishes full current medical eligibility, intake sites or initial diagnostic charges.',
'penn-osa-car-inkt-newly-diagnosed':'The newly diagnosed Penn OSA CAR-iNKT cohort is preserved separately from metastatic CAR-iNKT. Exact comparative-immunotherapy primary remains held; no cross-cohort transfer of prior treatment, mandatory care or costs.',
'penn-osa-carinkt':'The metastatic Penn OSA CAR-iNKT exact primary remains held. Newly diagnosed OSA and B-cell IL18 CAR-T registry status concern distinct cohorts; neither resolves metastatic eligibility, site intake or funding.',
'umn-orbit-lymphoma':'UMN exact ORBIT primary remains held. Current registry/LEAH CAR-T invitation is a separate intervention; >=7.5kg, indolent/herbal restrictions, standard-care backbone and owner costs remain not fully verified.',
'penn-bcell-car-t-registry':'NEW current primary registry signal: exact record22208/public999878/VCT25005914 IL18 B-cell CAR-T changed Suspended→Completed and its individual HTML is inactive. Canonical still public under older Penn recruiting evidence; Penn primary is restricted. Owner decision is required on this conflict; study end June30,2027 is not a recruitment cutoff.',
'penn-atherton-steap1-car-t-hs':'Atherton exact primary remains held. Current HS CAR-T identities were kept separate from B-cell CAR-T; no permitted full STEAP1 cohort protocol resolves measurable disease, concurrent chemotherapy or owner-benefit scope.',
'au-melbourne-hsa-autologous-vaccine-multicenter':'Exact Medipaws ethics35274 HSA vaccine primary remains held. Australian discovery distinguishes the commercial CANCV and other OSA/melanoma vaccines; no fresh complete ethics35274 owner/site/cost protocol was recovered.',
'penn-glioma-flash-gilvetmab-2026':'Penn exact FLASH+gilvetmab glioma primary remains held. Current UCD RT/drug and UTSW radiation studies are different cohorts and cannot resolve Penn diagnostic/brain-treatment/cost limits.',
'jp-jsamc-feline-anti-pd1':'Exact JSAMC feline anti-PD1 primary remains held. Current Yamaguchi broad canine PD1 and three-center canine oral-melanoma program were distinguished by species/cohort; neither is a feline protocol substitute.',
'uk-edinburgh-oral-melanoma-tigilanol-tiglate':'Today the full official Edinburgh eight-dog tigilanol oral-melanoma pilot news invitation was read. It remains historical2024, with no complete current intake, eligibility/cost protocol; current invitation cannot be inferred from page survival.',
'uk-liverpool-dogfight-glioma-ferumoxytol-rt':'Today the complete investigator DOGFIGHT description was read; changed pronouns/footer are nonclinical. It describes glioma ferumoxytol+RT and incentive but no full current screening/intake/owner-fee protocol.',
'tufts-hsa-liquid':'Today the full Tufts HSA liquid-biopsy primary was read again. It does not support the canonical $1500 splenectomy reimbursement clause. Existing owner decision remains necessary; diagnostic study eligibility alone does not justify that treatment benefit claim.',
'mizzou-osa-carboplatin-timing':'Today the full current Missouri oncology roster was read. Other OSA studies and LEAH are explicit, while this exact carboplatin-timing cohort lacks affirmative current intake. Absence alone is not confirmed closure; retain owner status decision.',
'mexico-ensenada-silver-nanoparticle-cancer-2026':'Today actual ZonANorte/UNAM sources were read and country-language discovery expanded. They do not publish a current complete treating-institution silver-nanoparticle owner protocol. Sidebar2027 political dates are unrelated; experimental access remains an owner inclusion/status question.',
'ucd-liver-tae-tace':'Today full current public clinical data for liver TAE/TACE were compared. Other-organ disease is conditional clinical screening, and full TAE diagnostic-cost funding is not affirmatively published; current canonical absolute exclusion/cost wording remains an owner medical/editorial decision.',
'jp-yamaguchi-canine-lymphoid-anti-cd20':'Today complete current Yamaguchi individual trial page explicitly invites anti-CD20 lymphoid-tumor research but omits complete criteria, present cohort allocations and owner costs. This is an unpublished protocol gap, not an inaccessible whole institution.',
'jp-nvlu-survivin-peptide-vaccine-2026':'Today NVLU primary read in full. March31,2027 is the stated research period, not an explicit guaranteed recruitment cutoff. Canonical recruiting-through wording still requires owner revision decision; Oct30,2026 belongs to nononcology MUO/MSC.',
'dk-copenhagen-flash-superficial-tumors':'Both exact Copenhagen official research routes returned native503 and same-URL Web timed out. No current permitted document establishes whole superficial-tumor FLASH intake, eligibility/funding or Swedish travel arrangements.',
'utsw-hsa-temozolomide-propranolol':'Today UTSW eight-title roster, individual registry22252 and primary PDF screenshots were compared. HSA doxo OR carboplatin+temozolomide+propranolol is absent from the current eight-title roster and cost coverage is unpublished. VSNT28067 randomized doxo+temozolomide±propranolol is a different exact registry/cohort/site; no merge.',
'medvet-egfr-her2-vaccine-2026':'Today entire sponsor12-site table, nine enrolling names and three non-enrolling exclusions were compared with all canonical sites. VCCS local diagnostic exceptions, $995 visit terms and medical exclusions remain site-specific owner matcher-scope decisions; no blanket eligibility edit.'}
done={x['trial_id']:x for x in rd(R/'completed-clinical-reviews.json')};updates=[]
for old in B['issues']:
 t=CT[old['trial_id']];tid=t['id'];es=attempts_for((t.get('url') or t.get('source_url') or ''))+[e for e in E if e.get('source_id')==tid];refs=list(dict.fromkeys(e['evidence_file'] for e in es))
 row={**old,'reviewed_at':at}
 if tid in done and old['kind']=='full_protocol':
  d=done[tid];row.update(state='RESOLVED',finding='Completed current full primary review: '+json.dumps(d['facts_checked'],ensure_ascii=False),facts_checked=list(d['facts_checked']),evidence_refs=d['evidence_refs'],primary_evidence_read_at=d['primary_read_at'])
 else:
  row['finding']=special[tid];row['evidence_refs']=refs or [ref(R/'individual-source-decisions.json')];row['next_action']='Review a newly permitted exact individual primary or newly published complete protocol to answer: '+old['question'];row['question']=old['question']
  row['state']='OWNER_DECISION' if old.get('state')=='OWNER_DECISION' or tid=='penn-bcell-car-t-registry' else 'BLOCKED'
  row['restriction_or_unpublished_evidence_refs']=row['evidence_refs'];row['original_primary_evidence_retained']=old.get('evidence_refs',[])
  if tid=='penn-bcell-car-t-registry':row['new_primary_signal']=True;row['evidence_refs']+=[ref(R/'avma-delta.json')];row['next_action']='Юля: decide public matching status for the exact IL18 CAR-T cohort given current AVMA Completed and inaccessible Penn confirmation; retain separate cohorts.'
  if old['kind']=='independent_selection':row['finding']+=' Independent positive/negative/unknown cases cannot be completed from the missing or medically ambiguous source criteria; existing matcher agreement is not independent verification.'
  if row['state']=='OWNER_DECISION' and tid!='penn-bcell-car-t-registry':row['next_action']='Юля: '+old['question']
 updates.append(row)
wr(R/'issue-review-current.json',updates)
# Daily clock comparison preserves original evidence dates. A URL visit alone is never a full clinical reread.
oldledger={x['record_id']:x for x in rd(ROOT/'research/audit-runs/daily-20261102T030506-0500/deadline-review.json')['rows']};dead=[]
for t in C:
 tid=t['id'];prev=oldledger.get(tid,{});es=attempts_for((t.get('url') or t.get('source_url') or ''))+[e for e in E if e.get('source_id')==tid];es=list({e['evidence_file']+e['url']:e for e in es}.values());reads=[e for e in es if e.get('result') in ['retrieved_page','web_retrieved_content']]
 dates=[{**d,'provenance_note':'Original evidence retained; daily clock comparison is not a new visit.'} for d in prev.get('dates',[]) if 'politic' not in str(d).lower() and 'sidebar' not in str(d).lower()]
 result='CURRENT_PRIMARY_READ_NO_NEW_EXPLICIT_CUTOFF_ESTABLISHED' if reads else 'NOT_VERIFIED_exact_restriction' if any(e.get('method')=='restriction_review_no_request' for e in es) else 'NOT_VERIFIED_no_current_primary_read'
 if tid=='ncsu-bladder-il12':result='EXPIRED_2026_09_30_NO_PRIMARY_EXTENSION_CONFIRMED'
 if 'lapatinib' in tid and t.get('available_for_matching') is False:result='INACTIVE_CANONICAL_PRESERVED_CHECK_PRIMARY_END_AND_ENROLLMENT'
 if tid=='jp-nvlu-survivin-peptide-vaccine-2026':result='RESEARCH_PERIOD_2027_03_31_NOT_RECRUITMENT_CUTOFF_OWNER_DECISION'
 dead.append({'record_id':tid,'compared_at':at,'previous_verified':C0[tid].get('verified'),'current_verified':t.get('verified'),'primary_urls':[(t.get('url') or t.get('source_url') or '')],'current_primary_evidence':[{'url':e['url'],'evidence_ref':e['evidence_file'],'original_read_at':e.get('completed_at'),'method':e['method']} for e in reads],'actual_new_attempts':[slim(e) for e in es],'dates':dates,'comparison_result':result,'extension_confirmed':False,'matching_before':C0[tid].get('available_for_matching'),'matching_after':t.get('available_for_matching'),'question':prev.get('question'),'unperformed_steps':[],'scope':'Daily deadline semantics/current read or exact restriction; does not reset verified date.'})
wr(R/'deadline-review.json',{'run_id':R.name,'baseline_sha':'2ad2ecfd77474c0185596ef2b11907966d342842','compared_at':at,'baseline_ids':B['catalog_ids'],'rows':dead,'additional_semantic_findings':['NCSU explicit2026-09-30 bladder IL12 cutoff remains expired without primary extension; no registry Recruiting override.','Tokyo feline TCC/lapatinib ended2026-10-31 and is fully enrolled; preserve inactive trial separately from paid access.','NVLU2026-10-30 MUO/MSC is non-oncology; survivin2027-03-31 is a research period.','UCD CARE2028,PRISM2031,CSU2028 and AVMA2027/2028 dates are study periods, not automatic enrollment cutoffs.','Unrelated Mexican political/sidebar2027dates excluded.']})
review=rd(R/'execution-review.json');review.update(ended_at=at,source_reviews=list(S.values()),issue_updates=updates,discovery_queries=Q,deadline_review_ref=ref(R/'deadline-review.json'))
wr(R/'execution-review.json',review)
receipt_payload={'run_id':R.name,'mode':'DAILY GLOBAL WORK AUDIT','started_at':B['started_at'],'at':at,'baseline_main_sha':'2ad2ecfd77474c0185596ef2b11907966d342842','source_total':len(receipt),'baseline_source_total':len(B['source_ids']),'attempted_total':sum(s['opened_this_run'] for s in receipt),'content_sufficient_total':sum(s['content_sufficient'] for s in receipt),'processing_complete_total':sum(s['processing_complete'] for s in receipt),'source_result_counts':dict(Counter(s['master_result'] for s in receipt)),'executor_incomplete_source_ids':[s['source_id'] for s in receipt if not s['processing_complete']],'discovery_regions_processed':len({q['region'] for q in Q}),'discovery_passes':sorted({q['pass'] for q in Q}),'sources':receipt}
wr(R/'receipt-final.json',receipt_payload)
gaps=[]
for s in receipt:
 if s['content_sufficient']:continue
 d=S[s['source_id']];hold=not s['processing_complete'];q=d.get('gap') or 'Which current complete cohort/status/owner-access facts remain unpublished or unavailable after this source-specific reconciliation? '+d['catalog_comparison']
 cat='discovery_source_not_trial_roster' if any(x in s['source_id'] for x in ['directory','pipeline','news','guide','foundation','research-grants']) else 'source_unavailable' if not d['current_official_content'] else 'protocol_uncertainty' if d['protocols'] else 'roster_unestablished'
 gaps.append({'source_id':s['source_id'],'category':cat,'processing_assessment':'not_established' if hold else 'external_blocker','question':q,'reason':d['finding'],'next_action':'Clarify the exact saved automatic-review scope without requesting the held route.' if hold else 'Recheck daily permitted master/fallback routes; revisit this exact remaining fact on new primary evidence or seven-day deep recheck, preserving original evidence dates.','evidence':{'source_id':s['source_id'],'attempted_urls':list(dict.fromkeys(a['url'] for a in s['attempted_urls'])),'evidence_refs':d['evidence_refs']},'completion_decision':{'remaining_fact':q,'routes_exhausted_evidence':[{k:a.get(k) for k in ['url','method','result','evidence_file','completed_at']} for a in s['attempted_urls']],'available_reconciliation_done_evidence':s['source_id']+': '+d['finding']+' Comparison: '+d['catalog_comparison']},'unperformed_steps':d['remaining_available_steps']})
wr(R/'gap-review.json',{'original_run_id':R.name,'reviewed_at':at,'rows':gaps})
print(json.dumps({'sources':len(receipt),'results':receipt_payload['source_result_counts'],'sufficient':receipt_payload['content_sufficient_total'],'processing':receipt_payload['processing_complete_total'],'issues':dict(Counter(u['state'] for u in updates)),'queries':len(Q),'countries':len({q['country'] for q in Q}),'languages':len({q['language'] for q in Q}),'deadline_rows':len(dead)},indent=2))
