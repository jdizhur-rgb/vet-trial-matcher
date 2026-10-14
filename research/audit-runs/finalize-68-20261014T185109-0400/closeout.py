"""Document the stopped source review without converting inherited reads into visits.

All medical/source decisions below are manual. Mechanical steps only join actual
attempts, validate identity/counts, and serialize those decisions for review.
"""
import copy, hashlib, json, re, subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit, parse_qsl, urlencode, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
STOPPED = ROOT.parent / 'vtf-68/research/audit-runs/reconcile-68-20261014T070053-0400'
DAILY = ROOT / 'research/audit-runs/daily-20261014T030650-0400'
TZ = ZoneInfo('America/New_York')
now = datetime.now(TZ).isoformat()
def read(p): return json.loads(p.read_text())
def write(name, value): (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def norm(u):
    x=urlsplit(unquote(u)); q=[(k,v) for k,v in parse_qsl(x.query) if k!='ref' and not k.startswith('utm_')]
    return urlunsplit((x.scheme,x.netloc,x.path.rstrip('/'),urlencode(sorted(q)),''))

baseline = read(RUN/'baseline.json')
inventory = read(ROOT/'data/source_inventory.json')
previous = copy.deepcopy(inventory)
by_source = {s['id']:s for s in inventory['sources']}
catalog = read(ROOT/'data/trials_base.json')
by_id = {r['id']:r for r in catalog}
draft = read(STOPPED/'source-decisions-draft.json')['rows']
daily_rows = {r['source_id']:r for r in read(DAILY/'receipt-final.json')['sources']}
denials = read(STOPPED/'inherited-forbidden-routes.json')

# Full manually enumerated published oncology sets for the sufficient sources.
# Includes diagnostic/history entries where needed to account for the entire set.
ROSTERS = {
3: [('ICG UCC surgery','csu-ucc-icg-surgery'),('Feline OSCC immunotherapy','csu-feline-oscc-immunotherapy'),('AML trametinib','csu-aml-trametinib'),('3D OSA limb implant','csu-osa-3d-limb-spare'),('AGASACA node mapping','csu-agasaca-node-map'),('UCC lapatinib RT','csu-ucc-lapatinib-rt'),('Engineered T cells STS','csu-sarcoma-engineered-tcells'),('OSA dual energy CT','csu-osa-dual-energy-ct'),('COTC033','csu-cotc033-vaccine-immunity'),('Metastatic OSA CAR-T','csu-osa-car-t-met'),('Carboplatin OSA pain','csu-osa-carboplatin-pain')],
6: [('Feline cancer tissue legacy donation','ncsu-feline-cancer-legacy-tissue'),('Canine cancer tissue legacy donation',None),('STS RT/XCSgel','ncsu-canine-sts-xcsgel'),('PIVOT-C oral tumour vaccine','ncsu-feline-oral-pivot-c'),('UCC IL12','ncsu-canine-ucc-il12'),('Liver INSPIRE','ncsu-liver-inspire'),('Mammary INSPIRE','ncsu-mammary-inspire')],
8: [('Prostate fluid/treatment','ucd-prostate-liquid-treatment'),('Urethral stent supportive procedure','ucd-urinary-stent'),('VCCT22-005 liver TAE/TACE: two portal cards, one protocol','ucd-liver-tae-tace'),('CAALM','ucd-pdl1-metastatic'),('CARE glioma','ucd-care-canine-glioma'),('FAP CAR-T','tufts-sts-fap-car-t'),('Nasal TAE','ucd-nasal-tae'),('Cutaneous lymphoma gene expression',None),('PRISM glioma','ucd-prism-canine-glioma'),('Nasal RT +/- arterial chemo','ucd-nasal-chemo-radiation'),('OSA characterization/amputation only','ucd-osa-palliative-amputation'),('Oral PDL1 fluorescence','ucd-oral-margin')],
10: [('Dog HSA Paccal — completed cohort, stale hospital invite','bluepearl-hsa-paccal')],
12: [('Study 1 CPMV','utsw-solid-cpmv'),('Study 2 RT/histotripsy','vroc-rt-histotripsy'),('Study 3 CRT-NP/HIFU','utsw-vroc-melanoma-crtnp-hifu-pdl1'),('Study 4 carboplatin +/- HIFU','utsw-vroc-melanoma-carboplatin-hifu'),('Study 5 advanced nonprotocol solid tumours','utsw-vroc-compassionate-advanced-unresectable'),('Study 6 CAR-neutrophils/RT','utsw-vroc-glioma-car-neutrophils-rt'),('Study 7 ferumoxytol/RT','utsw-vroc-glioma-ferumoxytol-rt'),('Separate HSA chemotherapy combination','utsw-hsa-temozolomide-propranolol')],
23: [('PetCure osteosarcoma — not currently recruiting',None),('PetCure lung tumour — not currently recruiting',None),('ImpriMed MCT sampling/on hold',None),('Feline lymphoma diagnostic redirect',None)],
24: [],
26: [('Newly diagnosed OSA CAR-iNKT','penn-osa-car-inkt-newly-diagnosed'),('Metastatic OSA CAR-iNKT','penn-osa-carinkt'),('B-cell CAR-T lymphoma/leukemia','penn-bcell-car-t-registry'),('Bladder anti-PD1','penn-anti-pd1-urothelial-carcinoma'),('STEAP1 HS CAR-T','penn-atherton-steap1-car-t-hs')],
28: [('Australian MCT mRNA vaccine','au-gamgee-personalized-mrna-vaccine')],
31: [('Auranofin OSA — historical guide, five centres are not five trials',None)],
32: [('Splenic HSA vaccine plus doxorubicin','au-melbourne-hsa-autologous-vaccine-multicenter')],
33: [('PET-CT OSA/auranofin historical and completed',None),('HBI lymphoma — current clinical consolidation service, not a new recruiting trial',None),('Skin SCC bacterial research',None),('Prostate preclinical target',None),('STS tigilanol — completed six-dog study',None)],
37: [('Feline small-cell GI lymphoma WART','tamu-feline-small-cell-gi-lymphoma-wart')],
39: [('ReachGlio NGR-TNF/TMZ','spain-puchol-reachglio-2026')],
41: [('Three-centre anti-PD1 oral melanoma','jp-multicenter-oral-melanoma-anti-pd1-2026')],
43: [('Tokyo organoid-guided therapy','jp-tokyo-organoid-guided-targeted-therapy-2026'),('Tokyo bladder IDO1','jp-tokyo-canine-bladder-ido1-inhibitor')],
48: [('Paccal dog HSA completed','bluepearl-hsa-paccal'),('Paccal cat solid tumours completed',None)],
50: [('Ardent/Unleash K9-ACV + CD200AR-L — recruitment complete',None)],
58: [('Boxer glioma autogenic vaccine','uf-boxer-glioma-autogenic-vaccine')],
62: [('Mars HIFU followed by doxorubicin, one managed Dallas site','mvh-hifu-doxorubicin-lymphoma')],
63: [('B-cell proteasome inhibitor','jp-nihon-proteasome-inhibitor-b-cell-tumors'),('Mutation-positive lung therapy','jp-nihon-mutation-positive-lung-cancer'),('IL12 glioma early research',None),('Alternating magnetic field early research',None)],
65: [('High-grade glioma chemoradiation','ch-zurich-canine-high-grade-glioma-chemoradiation'),('Feline oral SCC RT','ch-zurich-feline-oscc-flash-proton-rt'),('Plexus fluorescence surgery','eu-ch-pnst-plexus-fluorescence-surgery'),('STS fluorescence surgery','ch-zurich-sts-fluorescence-guided-surgery'),('FISS ADAM12 Phase0',None),('MCT sentinel-node camera',None),('Sarcoma PET staging',None),('HS blood tests',None)],
67: [('SOLID-Relapse','ethos-solid-relapse'),('PUSH','ethos-epush-hsa'),('Volition feline diagnostic DNA',None),('IDEXX biobanking',None)],
68: [],
}

# Individual completion judgments, separate from sufficiency and visit success.
# Specific source actions below were reviewed against the stored pages/attempts.
DONE = {
1:'Compared all configured registry routes and inherited seven-lead primary resolution; current API rereads failed. VRCCO is verified independently; WSU and the other exact candidate intakes are not inferred.',
2:'Compared the resource links with all 111 inventory identities; shared Guardian 404 and Hope-to-Malvern redirect now have actual retrieval evidence. No nonexistent exhaustive VCS roster is demanded.',
3:'Compared all eleven current FACC labels with canonical identities and the recent individual ledger; decoded the new COTC033 primary and its two-site identity. Nine-record corrections are already published.',
4:'Compared the current five CIGAT/VCTN signals and linked PDF with the inactive actinium record; PET imaging and IF7-SN38 are not actinium-225. No new actinium invitation exists in the retrieved material.',
5:'Compared Missouri current twelve labels, sponsor ECIP-OSA-01 closure, and individual LEAH holds. Ohio sponsor access remains distinct from Missouri/Minnesota holds. Direct ECIP closure was additionally read in the finalizer.',
6:'Enumerated seven dog/cat oncology identities; excluded FCGS and equine entries explicitly. Old IL12/liver deadlines are not silently extended. Unchanged records retain their individual primary dispositions.',
7:'Compared the nine current Tufts oncology families, inherited BG34 suspension, owner-approved Z007 HCC prescreening and shared Davis FAP primary. Did not retry denied BG34 or re-ask an existing owner decision.',
8:'Read all 38 API identities and reviewed the 14 neoplastic-candidate cards; excluded benign pituitary, merged TAE/TACE, and compared twelve oncology protocols. Corrected CAALM/oral/FAP data and retained non-treatment exclusions.',
9:'Read the generic UGA information and documented denied trial-search route. Preserved separately verified IVP and the owner-excluded benign endocrine cohort; no whole roster invented from FAQ.',
10:'Compared the sole oncology signal with the exact completed Paccal HSA cohort. All remaining posted clinical studies are non-oncology. Sponsor completion controls over the hospital stale invite.',
11:'Read the actual inherited Wisconsin 403 receipt; no retry or bypass. Reviewed source-only impact and retained individual protocol evidence without claiming a fresh master.',
12:'Compared seven current VROC brochures plus distinct HSA protocol; master tissue consent is not an eighth treatment. Image PDF/JSON criteria support published corrections. Historical aliases were not counted twice.',
13:'Both published central Ethos study routes are 404; hospital-posting FAQ and independently read Discovery/Mars studies do not establish an all-Ethos roster. Classified the central-source-only gap.',
14:'Compared both Discovery pages and current ePUSH, original SOLID, Relapse and two MIMIC aliases; retained current narrower MIMIC costs/scope and all verified published sites, without duplicate trials.',
15:'Checked master and both recorded official LifeSciences alternatives via actual shell/Web failures; independent Cornell study evidence is preserved rather than substituted for a missing sponsor roster.',
16:'OVC home is readable; dog/cat lists, actual ICCI current index and individual Palladia/OSA-HIFU routes failed via shell/Web. Cached old searches were not treated as current recruitment.',
17:'Compared all 29 populated ESVONC study rows as 27 protocol identities with Oncowaf, current Zurich and Fregis organizer readings. Six core questions are distinct and held for block 3; Dissectron is a separate watch lead.',
18:'Read the recovered full Oncowaf table and complete seven-site insulinoma list; compared 24 identities. Reused the same six organizer questions instead of repeating research under another source name.',
19:'Read inherited Utrecht attestation evidence without passing the gate. Distinguished January long-term treatment access from a current recruiting trial and from an unobserved whole OnGo roster.',
20:'Read both current Zurich primary lists and nine programme identities; current ADAM12 is Phase0, and absent old sinonasal cohort is not declared closed. Its exact access question is shared with European aliases.',
21:'Reviewed actual shell and same-URL Web failure for Milan, preserving dated October12 primary evidence. Old news cannot establish the whole current roster or close an existing record.',
22:'Read actual RVC master/fallback 403 receipts; no retry. Partner-specific public searches added no positive current insulinoma intake; those results remain supporting evidence only.',
23:'Compared all four SAGE oncology signals individually: two PetCure cohorts, MCT sampling/on hold and feline diagnostic redirect. Fresh PetCure zero-current-trials resolves the historical RT invitations.',
24:'Read the complete native PetCure page and its explicit zero-current-recruiting statement. Distinguished active radiation care from trial enrollment.',
25:'Read AMC current index and actual neobladder description; compared existing inactive identity and its enrollment uncertainty. Surgical-service availability does not reactivate the study.',
26:'Read full current CIP and Atherton pages and the B-cell flyer; established five actual identities instead of copying four incorrect parent labels. Existing direct-PI HS consent/capacity caveats are retained.',
27:'Compared UQ current list and February6 Enzistat announcement; existing OSA vaccine is not Enzistat. The old news does not supply a fresh protocol-level invitation and no closure is inferred from absence.',
28:'Read current Gamgee study-specific Australian MCT recruiting and application path; retained MCT-only scope, individualized administering clinic and unpublished owner costs without inventing an OSA cohort.',
29:'Reviewed native failure and same-URL PetTrials Web shell; no complete embedded trial array is available in those receipts. No trials match is not interpreted as zero national oncology trials.',
30:'Read SASH programme examples and real research context. Dual-drug MCT example lacks a named current cohort/protocol; no service or generic appointment is promoted as a trial.',
31:'Read the full undated auranofin state guide, distinguished its five sites from one protocol, and compared fresh BVSC completed research. Generic UK breed/genetics link is not treatment enrollment.',
32:'Read both MediPaws research index and HSA owner invitation; Sydney treating intake is confirmed, Melbourne coordination is not a second automatically inferred treating site.',
33:'Read all five BVSC research descriptions and the actual linked HBI client sheet. Historical clinical research, completed PET/STS work and current HBI care are qualified separately.',
34:'Read public ANZCVS oncology news/navigation and respected member repository boundary. A society/news page does not publish or promise an exhaustive national trial roster.',
35:'Corrected the false existing-Immunocidin claim by exact canonical search. Read the linked CCA article, current NovaVive home/research/product and 2019 retrospective PDF; no current named enrolling protocol is established. NCSU current named bladder PDF is IL12, not MCWF; two Immunocidin trial leads remain separate watch items.',
36:'Read prior WSU master 403 and the new fallback 403; no retry or bypass after denial. Shared vaccine/TCE current protocols do not establish an unseen institutional master roster.',
37:'Read the investigator roster and decoded entire current WART protocol; compared cat cohort, radiation, washout, travel and funding criteria with the existing canonical record. Missing RT constraint is published.',
38:'Read the full Chinese organizer three-cohort invitation and owner/vet screening route; compared pathology/age/tumour state and free-drug/monitoring clauses. Drug identity, named administering clinic and other costs remain explicitly unpublished.',
39:'Read full native Spanish ReachGlio invitation and current Puchol owner route; NGR-TNF/TMZ and funded procedure scope agree with the canonical primary review.',
40:'Read the actual NCI 403 and institutional COTC supporting provenance; did not retry the prohibited master or interpret individual COTC evidence as a full NCI roster.',
41:'Read Japanese index and Sep30 direct owner invitation with all three participating centres. Unpublished stage/medication/cost rules are explicitly site prescreening, not missing current invitation.',
42:'Read Yamaguchi homepage and entire actual info page. Classified five oncology families: CD20, broad PD1, diagnostic blood and two ended programmes. A generic PD1 phrase does not create another defined cohort.',
43:'Read both posted JVCS Tokyo announcements and compared existing primary-controlled organoid/IDO1 identities. Submitted announcement scope is not represented as an exhaustive Japanese roster.',
44:'Reviewed failed JSAMC direct route and full current iCAT home/research. Checkpoint/CD20 work, CAR-T preparation and undefined combinations are not conflated into new recruiting cohorts.',
45:'Read 200 unique public directory records across pages1/2, manually mapped all 67 reachable oncology signals, and documented failed third-page native/Web attempts. Remaining99 are not described as checked.',
46:'Read actual inherited JVCOG professional-attestation content/receipt; no impersonation, gate bypass or new source-date claim. Existing protocols remain independently assessed.',
47:'Read Portuguese LOCT investigator and ONVEP pages. NDV canine PhaseI safety/dose and feline platform projects lack current qualifying owner protocol; no unsupported treatment activation.',
48:'Matched the two Paccal owner cohorts to direct Vivesto completion and BARC/CASTR closure evidence, retaining the existing inactive state. No future pivotal cohort is inferred.',
49:'Read complete Estima COE research/partnership content. Generic low-cost care and partnership do not specify drug, cohort, protocol or trial entry; no metadata-only trial is fabricated.',
50:'Compared fresh Ardent ongoing label, individual study content and Unleash explicit recruitment complete statement for the identical K9-ACV/CD200AR-L protocol. No unresolved 19-site intake remains to reconcile for a closed recruitment cohort.',
51:'Read three Alfort project descriptions, separating TG6002 undated invitation from carboplatin PK and colorectal sampling. Verified that no TG6002 canonical row exists; current access remains a watch question.',
52:'Read Perseus resource links and map to existing inventory plus shared Guardian/Hope outcomes. Its institutional link list is not a new clinical protocol or an exhaustive recruiting roster.',
53:'Read four historical EVVIVAX vaccine families and linked VOS evidence; retain all five inactive historical canonical entries. Generic ECT services and platform papers do not reactivate named vaccine trials.',
54:'Read CureLab veterinary pilot narrative and human-trial statements separately. An inquiry invitation and preclinical/pilot outcomes do not establish a new named veterinary enrollment cohort/site.',
55:'Read Cancer Vet actual generic participation page; it has no named drug, disease-specific study or protocol link. Oncology appointments do not constitute a treatment trial.',
56:'Read Dog Cancer Foundation resource page; compare its institutional/provider leads with current inventory and shared VCS outcomes. Avoid a third duplicate Guardian/Hope investigation.',
57:'Read Benno current research and its prior UCC/HSA outcomes versus ongoing OSA/amputation signal. Publication and Leuven company address do not specify a current treating hospital or owner protocol.',
58:'Read complete native Boxer-only glioma primary and current neurology index; prior-treatment, imaging/biopsy, vaccine, costs and eligibility agree with the existing record.',
59:'Read LEAH sponsor and three institutional routes. Minnesota/Missouri hold and sponsor-listed Ohio enrollment are distinct; use the one shared Ohio corroboration issue, no duplicate investigation.',
60:'All three configured Oklahoma URLs are404. Followed the actual current Research-page Clinical Trials link to the hospital host; its advertised route is also404. Old FUS lab projects are not an enrollment roster.',
61:'Read actual non-www VOS official navigation/GET alternatives after old route failure; native transport errors and Web empty shells remain insufficient for a named trial roster. No generic ECT service is counted as a trial.',
62:'Read entire eleven-record Mars gallery, full lymphoma primary and advertised managed-location endpoint. One oncology protocol, exactly one current managed Dallas site; no omitted location inferred from empty HTML islands.',
63:'Read all four Nihon individual public pages with identity-bearing page_id preserved. Two qualifying treatment records already exist; IL12 and magnetic-field programmes remain early research without new treatment promotion.',
64:'Read current LMU index and both official individual fallbacks. Documented thyroid/Palladia title versus analgesia body publisher mismatch; neither a new anticancer trial nor an active canonical conflict is established.',
65:'Read all eight DVG oncology labels and current Zurich official fallback. Classified four therapeutic programmes, ADAM12 Phase0 and three diagnostic studies rather than requiring an unpublished national total.',
66:'Read Edinburgh programme and actual linked FAQ. Neither publishes named cohorts; linked European insulinoma question remains protocol-specific instead of casting doubt on all Edinburgh treatments.',
67:'Read all four Metropolitan postings; distinguish two cancer-treatment cohorts from Volition and IDEXX diagnostics/banking. Hospital-specific PUSH invitation verifies Akron despite sponsor-list omission.',
68:'Read full native Red Bank page and all five non-oncology entries; verified zero dog/cat cancer trials. Five all-condition entries replace the inaccurate inherited count of four.',
}

# Corrections to draft facts; source outcome remains independent of processing.
draft[5]['protocols_seen']=7
draft[5]['reconciliation']='Seven dog/cat oncology identities: two tissue donations, STS XCSgel, PIVOT-C, bladder IL12, liver and mammary INSPIRE. FCGS and equine studies are excluded. Previously reported eight wrongly included non-cancer FCGS. Existing liver/bladder deadline-based inactive dispositions are retained.'
draft[34]['impact']='P2'
draft[34]['decision']='watch_nonmatchable'
draft[34]['reconciliation']=DONE[35]
draft[34]['remaining_fact']='A current NovaVive/investigator protocol and enrolling site for the separately described Immunocidin OSA/solid-tumour pilot and alleged NCSU bladder cohort; the known NCSU IL12 protocol is not proof of MCWF recruitment.'

def normal_attempt(r, origin):
    keep=['source_id','url','effective_url','route','method','attempted_at','completed_at','http_status','retry','result','text_sha256','evidence_reference','crawl_freshness','title','text_length','exit_code']
    x={k:r[k] for k in keep if k in r};x['visit_origin_run_id']=origin;x['new_visit_in_finalizer']=origin==RUN.name
    file=r.get('text_path') or r.get('raw_text_path')
    if file and Path(file).exists():
        content=Path(file).read_bytes();x['stored_text_sha256']=hashlib.sha256(content).hexdigest()
    return x

old_attempts=[]
for fn in ['shell-attempts.jsonl','web-attempts.jsonl']:
    old_attempts += [normal_attempt(json.loads(l), STOPPED.name) for l in (STOPPED/fn).read_text().splitlines()]
new_attempts=[normal_attempt(json.loads(l),RUN.name) for l in (RUN/'shell-attempts.jsonl').read_text().splitlines()]
web_new=read(RUN/'new-web-attempts.json')
last_web=next(r for r in web_new if r['name']=='cca_primary_final')
new_attempts.append({'source_id':'usa-missouri-oncology-clinical-trials','url':'https://eliasanimalhealth.com/clinical-studies/canine-osteosarcoma-combined-immunotherapy/','route':'shared_direct_protocol_status','method':'Web','attempted_at':last_web['attempted_at'],'completed_at':last_web['completed_at'],'evidence_reference':'turn731view2','crawl_freshness':'today','result':'retrieved_page','visit_origin_run_id':RUN.name,'new_visit_in_finalizer':True,'response_sha256':last_web['response_sha256']})
write('inherited-attempts.json',old_attempts)
write('new-native-attempts.json',new_attempts)
write('stopped-draft-preserved.json',read(STOPPED/'source-decisions-draft.json'))
write('inherited-denials.json',denials)
write('target-inventory.json',{'sources':[copy.deepcopy(by_source[r['source_id']]) for r in draft]})

rows=[];gaps=[];date_rows=[];roster_rows=[]
for d in draft:
    n=d['index'];sid=d['source_id'];src=by_source[sid];old=copy.deepcopy(src)
    visits=[r for r in old_attempts if r['source_id']==sid]
    prior_denials=[r for r in denials if r['source_id']==sid]
    assert n in DONE and len(DONE[n])>70
    denied={norm(x['url']) for x in prior_denials}
    observed={norm(x['url']) for x in visits}
    required=[src['master_url'],*src.get('fallback_urls',[])]
    missing=[u for u in required if norm(u) not in observed and norm(u) not in denied]
    assert not missing,(sid,missing)
    # For the five deliberately unvisited sources, real prior denied requests are
    # attached as inherited evidence, never marked as new visits to this run.
    evidence_attempts=visits if visits else [normal_attempt({'source_id':sid,**a},'daily-20261014T030650-0400') for a in daily_rows[sid]['attempted_urls']]
    sufficient=d['result']=='fully_reconciled'
    roster=None
    if sufficient:
        assert n in ROSTERS and len(ROSTERS[n])==d['protocols_seen'],(n,d['protocols_seen'])
        roster=[{'title':title,'canonical_id':cid,'disposition':('existing_public' if by_id[cid].get('available_for_matching') and by_id[cid].get('status_confidence') in ['current','confirmed_current'] else 'existing_nonmatchable') if cid else 'classified_no_new_canonical_record'} for title,cid in ROSTERS[n]]
        assert visits and any(x.get('stored_text_sha256') for x in visits)
        roster_rows.append({'source_id':sid,'published_oncology_protocols':roster,'protocols_seen':d['protocols_seen'],'comparison':DONE[n],'actual_source_evidence':[x for x in visits if x.get('stored_text_sha256')],'individual_details_policy':'changed/due protocols read; unchanged recent individual evidence inherited with actual prior dates, not refreshed'})
    completion={'remaining_fact':d['remaining_fact'] or 'No unresolved source-scope fact after this reconciliation.',
        'routes_exhausted_evidence':{'required_routes':[{'url':u,'outcome':'actual_request_recorded' if norm(u) in observed else 'prior_explicit_gate_do_not_repeat'} for u in required],'actual_attempts':evidence_attempts,'explicit_prohibitions':prior_denials,'additional_official_routes':[x['url'] for x in visits if norm(x['url']) not in {norm(u) for u in required}]},
        'available_reconciliation_done_evidence':{'manual_decision':DONE[n],'record_ids_compared':d['record_ids'],'primary_corrections_published_in':'eca20a12c3b67348db3de18935ac874a81a98e98' if n in [3,8,12,37] else None,'specific_new_followup':'new-native-attempts.json and new-web-attempts.json' if n==35 else None}}
    # This snapshot describes the STOPPED run's real source visits. The finalizer
    # only signs off the evidence/comparisons and appends separately dated reads.
    manual_proof_complete = (n in DONE and not missing and bool(evidence_attempts)
                             and bool(completion['available_reconciliation_done_evidence']['manual_decision'])
                             and (not sufficient or (roster is not None and len(roster)==d['protocols_seen']))
                             and (sufficient or bool(d['remaining_fact'])))
    assert manual_proof_complete, (sid, 'completion is not established')
    row={'source_id':sid,'source_name':src['name'],'master_url':src['master_url'],'opened_this_run':bool(visits),'attempted_urls':evidence_attempts,'route_used':sorted({r['method'] for r in evidence_attempts}),
        'master_result':'reachable' if sufficient else ('partial' if d['result']=='not_checked' else d['result']),
        'source_result':d['result'],'content_sufficient':sufficient,'protocols_seen':d['protocols_seen'],'current_roster':roster,
        'processing_complete':manual_proof_complete,'processing_completed_in_run':RUN.name,'manual_completion_review_id':f'source-review-{n:02d}','processing_assessment':'completed_review' if sufficient else 'external_blocker','completion_decision':completion,'reconciliation':d['reconciliation'],'impact':d['impact'],'record_ids':d['record_ids'],
        'actual_source_visit_run_id':STOPPED.name if visits else 'daily-20261014T030650-0400','new_visit_in_finalizer':False,
        'previous_last_checked':old['last_checked'],'previous_last_checked_at':old.get('last_checked_at'),'previous_last_result':old['last_result'],'previous_content_fingerprint':old.get('content_fingerprint'),
        'fingerprint_preserved_from_prior_same_day_visit':False,'historical_fingerprint_preserved_not_roster_proof':True}
    # Persist actual stopped-run visits. New CCA primary reads have their own real
    # finalizer timestamps; other dates are not renewed by writing documentation.
    metadata_visits=visits+[x for x in new_attempts if x['source_id']==sid]
    if metadata_visits:
        last=max(metadata_visits,key=lambda x:datetime.fromisoformat(x['attempted_at'].replace('Z','+00:00')))
        latest=datetime.fromisoformat(last['attempted_at'].replace('Z','+00:00')).astimezone(TZ)
        src.update(last_checked=latest.date().isoformat(),last_checked_at=latest.isoformat(),last_result='reachable' if sufficient else ('unreachable' if d['result']=='unreachable' else 'partial'),
            notes=d['reconciliation'],last_attempts=metadata_visits,last_route_used=sorted({x['method'] for x in metadata_visits}),last_audit_run_id=last['visit_origin_run_id'],last_protocols_seen=d['protocols_seen'],last_coverage_gap=d['remaining_fact'] or None,
            last_coverage_receipt=str((RUN/'receipt-final.json').relative_to(ROOT)),content_sufficient=sufficient,recheck_after='2026-10-21' if not sufficient or d['remaining_fact'] else None,
            reconciliation_run_id=RUN.name,last_http_status=last.get('http_status'))
        # No old content hash is turned into today's roster proof.
    row.update(new_last_checked=src['last_checked'],new_last_checked_at=src.get('last_checked_at'),new_last_result=src['last_result'],new_content_fingerprint=src.get('content_fingerprint'),new_finalizer_attempts=[a for a in new_attempts if a['source_id']==sid])
    date_rows.append({'source_id':sid,'actual_attempts_present':bool(metadata_visits),'new_visit_in_finalizer':any(x['new_visit_in_finalizer'] for x in metadata_visits),'previous':{'last_checked':old['last_checked'],'last_checked_at':old.get('last_checked_at'),'last_result':old['last_result']},'new':{'last_checked':src['last_checked'],'last_checked_at':src.get('last_checked_at'),'last_result':src['last_result']},'unchanged_no_new_visit':not bool(metadata_visits)})
    rows.append(row)
    if not sufficient:
        if n in [11,15,19,21,22,36,40,46,60,61]: category='source_unavailable'
        elif n in [2,30,34,35,49,52,54,55,56,57,66]: category='discovery_source_not_trial_roster'
        elif n in [9,13,16,29,45]: category='roster_unestablished'
        else: category='protocol_uncertainty'
        next_action=('Compare newly posted named protocols and actual outgoing links during daily visits; do not demand an exhaustive trial roster from a resource/news/programme page. Deep review only for a concrete new lead.' if category=='discovery_source_not_trial_roster' and n!=35 else 'Recheck exact missing fact after new primary evidence, changed master or 2026-10-21; daily master/fallback duty remains. No repeated deep search without a signal.')
        gaps.append({'source_id':sid,'category':category,'processing_assessment':'external_blocker','question':d['remaining_fact'],'reason':d['reconciliation'],'next_action':next_action,'evidence':{'source_id':sid,'attempted_urls':list(dict.fromkeys(a['url'] for a in evidence_attempts)),'additional_current_followup':'new-native-attempts.json' if n==35 else None},'completion_decision':completion,'impact':d['impact'],'record_ids':d['record_ids']})

receipt={'run_id':STOPPED.name,'finalized_by_run_id':RUN.name,'mode':'TARGETED CUMULATIVE EVIDENCE CLOSEOUT, not a new daily/global sweep','receipt_semantics':'opened_this_run counts actual visits in the stopped source-review run named by run_id. The finalizer never converts inherited evidence into new visits. Its targeted extra reads are separate addendum evidence.',
    'started_at':read(STOPPED/'baseline.json')['started_at'],'finalized_at':now,'base_main_sha':baseline['base_main_sha'],'source_total':68,'attempted_total':sum(r['opened_this_run'] for r in rows),'content_sufficient_total':sum(r['content_sufficient'] for r in rows),'processing_complete_total':sum(r['processing_complete'] for r in rows),'source_result_counts':dict(Counter(r['source_result'] for r in rows)),'executor_unfinished_actions':0,'executor_incomplete_source_ids':[],'new_full_traversal':False,'new_global_discovery_regions':0,'sources':rows,'status':'INCOMPLETE','processing_status':'EVIDENCE_REVIEW_FINISHED_EXTERNAL_GAPS','technical_publication_of_nine_corrections':'research/audit-runs/publish-nine-20261014T183019-0400/report.md'}
review={'original_run_id':STOPPED.name,'review_run_id':RUN.name,'reviewed_at':now,'rows':gaps}
write('receipt-final.json',receipt);write('gap-review.json',review);write('roster-reconciliation.json',roster_rows);write('source-date-readback.json',{'reviewed_at':now,'rows':date_rows})
write('inventory-before.json',previous)
(ROOT/'data/source_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_outcomes':receipt['source_result_counts'],'sufficient':receipt['content_sufficient_total'],'actual_stopped_source_visits':receipt['attempted_total'],'manual_processing_decisions':len(DONE),'gaps':len(gaps),'metadata_changed_sources':sum(a!=b for a,b in zip(previous['sources'],inventory['sources']))},indent=2))
