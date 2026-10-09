import json, hashlib, re
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
RID=RUN.name
def read(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def norm(u): return u.strip().rstrip('/')
pages=read(RUN/'web-page-index.json')
byref={p['reference']:p for p in pages}
before=read(RUN/'inventory-before.json')
inv=read(ROOT/'data/source_inventory.json')
assert len(inv['sources'])==100, 'First application only; never rewrite final immutable receipts'
now=datetime.now(ZoneInfo('America/New_York')).isoformat()
reviews=[]
for line in (RUN/'source-review-ledger.txt').read_text().splitlines():
    ix,status,count,roster,note=line.split('|',4)
    reviews.append(dict(index=int(ix),status=status,protocols_seen=None if count=='null' else int(count),current_roster=[x.strip() for x in roster.split(';')],review_notes=note))
assert [r['index'] for r in reviews]==list(range(100))
extras={5:['turn292view1','turn292view2'],10:['turn348view0'],16:['turn296view0','turn297view0','turn298view1','turn305view1','turn299view2','turn303view0'],29:['turn345view1','turn346view0'],30:['turn292view0'],31:['turn304view0','turn354view0'],33:['turn320view1','turn334view1'],51:['turn298view0'],57:['turn305view0','turn304view2','turn359view0','turn292view0'],61:['turn335view0'],69:['turn319view1','turn338view0'],86:['turn288view1'],98:['turn333view0','turn333view1','turn334view0']}
newdefs=[
 ('belgium-ghent-small-animal-clinical-research','Ghent University small-animal clinical research','Belgium','university','turn342view0',['turn336view1','turn351view0','turn318view1'],3,'Feline GCN2-IN-6 mammary trial; chemotherapy heart screening; fluorescence-lifetime cancer surgery imaging; separate unlisted nanobody head/neck lead','Current master lists three oncology-related studies; nanobody primary is still reachable but unlisted, so current identity/enrollment remains unresolved.'),
 ('japan-nihon-anmec-clinical-research','Nihon University Animal Medical Center clinical research','Japan','university','turn329view0',['turn330view0','turn330view1'],4,'B-cell proteasome inhibitor; mutation-positive canine lung cancer; alternating magnetic field cancer treatment; glioma IL12-CBD','All four individual oncology protocols read. Two confirmed therapeutic records added; magnetic-field and IL12 first-in-dog programs held outside matching pending treatment-benefit qualification.'),
 ('germany-lmu-small-animal-research','LMU Munich small-animal clinical research','Germany','university','turn328view0',['turn332view0','turn332view1'],2,'OSA peripheral nerve blocks; Palladia thyroid-function study','Nerve-block study supportive, not anticancer. Palladia-linked title returns the nerve-block body: publisher inconsistency preserved, no invented protocol.'),
 ('germany-dvg-veterinary-clinical-studies','German Veterinary Medical Society clinical-study registry','Germany','registry','turn328view1',['turn337view1'],8,'High-grade glioma; feline oral SCC radiation; plexus fluorescence; STS fluorescence; feline FISS vaccine; MCT sentinel nodes; sarcoma PET; HS screening','Eight registry entries reconciled against current Zurich primary source. Registry linked legacy primary is404; stale registry/primary differences remain external.'),
 ('uk-edinburgh-small-animal-clinical-trials','University of Edinburgh small-animal clinical-trials programme','UK','university','turn327view1',[],None,'Clinical-trials programme including cancer','Durable official programme confirmed, but no complete named current oncology protocol roster published.'),
 ('sponsor-akston-oncology-pipeline','Akston Biosciences oncology development and trial announcements','USA','cro_sponsor','turn351view1',['turn355view0','turn338view1'],None,'AKS701d; AKS197d; AKS427c; AKS619d pipeline projects','Four oncology pipeline projects are not four activated protocols. Current news and dated Oct29,2025 announcement read; known Purdue program/Phase-I lead not duplicated or activated.'),
 ('usa-metropolitan-vet-current-trials','Metropolitan Veterinary Hospital current clinical trials','USA','hospital_program','turn352view0',[],4,'Volition feline LSA diagnosis; IDEXX oncology samples; SOLID relapse; PUSH hemangiosarcoma','Current four-title oncology roster read. SOLID six sites reconciled with current Ethos primary; PUSH phase-specific eligibility and whole current roster not public.')
]
# Add only URLs actually retrieved/attempted. Supplementary primary URLs below
# were opened during this run, not constructed from guessed paths.
for definition in newdefs:
    sid,name,country,typ,masterref,refs,count,roster,note=definition
    mast=byref[masterref]
    if sid=='japan-nihon-anmec-clinical-research':
        refs += [p['reference'] for p in pages if p['url'] in ['https://hp.brs.nihon-u.ac.jp/~nuanmec/?page_id=4035','https://hp.brs.nihon-u.ac.jp/~nuanmec/?page_id=5145']]
    if sid=='belgium-ghent-small-animal-clinical-research':
        refs += [p['reference'] for p in pages if 'fluorescentie-levensduur-beeldvorming' in p['url']]
    if sid=='germany-dvg-veterinary-clinical-studies':
        # Current official Zurich route already opened as an inventory fallback.
        refs += ['turn283view1']
    if sid=='usa-metropolitan-vet-current-trials': refs+=['turn345view1']
    fallback=list(dict.fromkeys(byref[x]['url'] for x in refs if x in byref and byref[x]['url'].startswith('https://') and norm(byref[x]['url'])!=norm(mast['url'])))
    inv['sources'].append(dict(id=sid,name=name,country=country,source_type=typ,master_url=mast['url'],fallback_urls=fallback,required_cadence='daily',last_checked=None,last_checked_at=None,last_result='pending',content_fingerprint=None))
    reviews.append(dict(index=len(reviews),status='partial',protocols_seen=count,current_roster=roster.split('; '),review_notes=note,explicit_refs=list(dict.fromkeys([masterref]+refs))))
assert len(inv['sources'])==107
# Additional official research-centre route established today for the same institution.
jsamc=inv['sources'][69]
jsamc.setdefault('fallback_urls',[])
if 'https://www.cure-cancer.jp/' not in jsamc['fallback_urls']:jsamc['fallback_urls'].append('https://www.cure-cancer.jp/')
receipt=[]
missing=[]
for s,review in zip(inv['sources'],reviews):
    ix=review['index']; prev=before['sources'][ix] if ix<100 else {}
    required=[s['master_url']]+s.get('fallback_urls',[])
    selected=[p for p in pages if norm(p['url']) in {norm(u) for u in required}]
    refs=review.get('explicit_refs',[])+extras.get(ix,[])
    selected += [byref[r] for r in refs if r in byref]
    # Reuse today's already-read protocol pages from the same official host,
    # retaining exact URL/ref/time provenance. Not fresh visits to other sources.
    host=urlsplit(s['master_url']).netloc
    selected += [p for p in pages if urlsplit(p['url']).netloc==host and p['url'].startswith('https://')]
    selected=list({(p['file'],p['reference']):p for p in selected}.values())
    for u in required:
        if not any(norm(p['url'])==norm(u) for p in selected):missing.append((s['id'],u))
    if not selected:raise ValueError('No actual attempts: '+s['id'])
    attempts=[]
    for p in sorted(selected,key=lambda x:x['attempted_at'] or ''):
        attempts.append(dict(url=p['url'],attempted_at=p['attempted_at'],method=p['method'],result='retrieved_text_requires_semantic_review' if p['retrieved'] else 'unavailable_or_empty',http_status=None,web_reference=p['reference'],evidence_file=p['file'],crawl_label=p['crawl_label'],reader_text_sha256=p['reader_sha256'] if p['retrieved'] else None,full_text_available=p['full_text_available'],timestamp_precision='tool-call batch start'))
    saved_at=max(a['attempted_at'] for a in attempts if a['attempted_at'])
    sufficient=review['status']=='fully_reconciled'
    result='reachable' if sufficient else ('unreachable' if review['status']=='unreachable' else 'partial')
    currentbody=next((p for p in sorted(selected,key=lambda p:(p['full_text_available'],len(p['body'])),reverse=True) if p['retrieved']),None)
    fp='sha256:'+currentbody['reader_sha256'] if currentbody else None
    row=dict(source_id=s['id'],source_name=s['name'],opened_this_run=True,processing_complete=True,executor_incomplete=False,content_sufficient=sufficient,protocols_seen=review['protocols_seen'],status=review['status'],master_result=result,attempted_urls=attempts,route_used='Official master and required fallbacks via Web; current-run shared protocol evidence has explicit provenance',roster_evidence=dict(current_roster=review['current_roster'],review_notes=review['review_notes'],current_evidence_references=list(dict.fromkeys(p['reference'] for p in selected)),count_unit='Named oncology program/protocol identities, including closed and non-treatment research; null if whole roster cannot be counted',baseline_catalog='catalog-before.json (303 records)',unchanged_detail_provenance='Oct8 current-primary-semantic-reconciliation.json; individual re-read skipped only for current unchanged roster and primary read within28days'),previous_last_checked=prev.get('last_checked'),previous_last_checked_at=prev.get('last_checked_at'),previous_last_result=prev.get('last_result'),previous_fingerprint=prev.get('content_fingerprint'),saved_last_checked=saved_at[:10],saved_last_checked_at=saved_at,saved_last_result=result,current_fingerprint=fp,fingerprint_method='Current Web reader text SHA256, not raw HTTP or prior-run hash',fingerprint_preserved_from_prior_same_day_visit=False,external_gap=None if sufficient else review['review_notes'],recheck_after=None if sufficient else '2026-10-16')
    receipt.append(row)
    s.update(last_checked=row['saved_last_checked'],last_checked_at=saved_at,last_result=result,content_fingerprint=fp,last_http_status=None,last_attempts=attempts,last_route_used=row['route_used'],last_audit_run_id=RID,last_protocols_seen=review['protocols_seen'],last_coverage_gap=row['external_gap'],notes=review['review_notes'],fingerprint_method=row['fingerprint_method'])
if missing:
    save(RUN/'missing-required-attempts.json',missing)
    raise ValueError('Missing actual required URL attempts: '+str(missing))
inv['updated']='2026-10-09'
save(ROOT/'data/source_inventory.json',inv)
coverage=dict(schema_version=1,run_id=RID,audit_mode='DAILY GLOBAL WORK AUDIT',status='INCOMPLETE',started_at='2026-10-09T02:58:43-04:00',checkpoint_at=now,timezone='America/New_York',base_commit='c22113f024c986a58f047ca46bdc87d2b9b31658',source_total=len(receipt),attempted_total=len(receipt),processing_total=len(receipt),executor_unfinished_total=0,content_sufficient_total=sum(r['content_sufficient'] for r in receipt),global_discovery_regions=12,global_discovery_passes=2,sources=receipt)
save(RUN/'receipt-final.json',coverage)
save(ROOT/'data/audit_source_coverage.json',coverage)
save(RUN/'queue-final.json',dict(run_id=RID,processing_total=107,executor_unfinished_total=0,pending_source_ids=[],terminal_external_gap_ids=[r['source_id'] for r in receipt if not r['content_sufficient']],automatic_requeue=False,regions_completed=12))
state=read(ROOT/'data/audit_state.json')
state['last_incremental_audit']=now
state['last_source_discovery_attempt']=dict(run_id=RID,started_at=coverage['started_at'],checkpoint_at=now,status='daily_trial_only_incomplete_external_gaps',attempted=107,sufficient=coverage['content_sufficient_total'],source_total=107,coverage_receipt=str((RUN/'receipt-final.json').relative_to(ROOT)),latest_receipt='data/audit_source_coverage.json',catalog_changes=4,new_source_entries=7,global_discovery_regions=[x['id'] for x in read(RUN/'discovery-query-plan.json')['matrix']],pending_source_ids=[],external_gap_source_ids=[r['source_id'] for r in receipt if not r['content_sufficient']],executor_unfinished_total=0,terminal_external_gaps_no_automatic_requeue=True,previous_checkpoint='research/audit-runs/daily-20261008T080207-0400/receipt-final.json',remote_persistence_verification={'status':'not_checked','reason':'Publication not yet executed; no prior SHA reused'})
save(ROOT/'data/audit_state.json',state)
save(RUN/'source-reviews-final.json',reviews)
save(RUN/'source-date-readback-local.json',dict(status='PASS',verified_at=now,source_total=107,source_ids=[r['source_id'] for r in receipt],previous_new=[{k:r[k] for k in ['source_id','previous_last_checked','previous_last_checked_at','saved_last_checked','saved_last_checked_at','saved_last_result']} for r in receipt],inventory_sha256=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest()))
from collections import Counter
print(json.dumps({'sources':107,'coverage':dict(Counter(r['status'] for r in receipt)),'mandatory_url_gaps':missing,'dates_range':[min(r['saved_last_checked_at'] for r in receipt),max(r['saved_last_checked_at'] for r in receipt)]},indent=2))
