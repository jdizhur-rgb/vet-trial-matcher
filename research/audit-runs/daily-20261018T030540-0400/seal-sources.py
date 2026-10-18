"""Source-specific decisions following fresh literal whole-page/whole-API comparisons."""
from reconcile import *
import copy,ast
inv=read(P/'before-source_inventory.json'); prior={r['source_id']:r for r in read(OLD/'reviews.json')}; comps=read(P/'current-full-comparisons.json')
denied=read(P/'restrictions-frozen.json')+[json.loads(x) for x in (P/'new-denials.jsonl').read_text().splitlines()]
deny={key(x['url']):x for x in denied}; actual=native+web;byurl=collections.defaultdict(list)
for a in actual:byurl[key(a['url'])].append(a)
rows=[]
for s in inv['sources']:
 old=prior[s['id']]; aa=[a for a in actual if a['source_id']==s['id']]
 mandatory=[];unperformed=[]
 for u in [s['master_url']]+s.get('fallback_urls',[]):
  hits=byurl[key(u)]; d=deny.get(key(u))
  if not hits and not d:unperformed.append(u)
  mandatory.append({'url':u,'actual_attempt_evidence':[{'method':a['method'],'at':a['attempted_at'],'evidence':a['evidence_file'],'result':a['result'],'http_status':a.get('http_status')} for a in hits],'inherited_or_current_prohibition':d if not hits else None})
  for a in hits:
   if a not in aa:aa.append(a)
 cc=[c for c in comps if c['source_id']==s['id']]
 same=[c for c in cc if c['same_entire_text']]
 sufficient=old['content_sufficient'] and bool(same)
 result='fully_reconciled' if sufficient else 'partial' if aa else 'not_checked'
 category=old.get('category') or 'roster_unestablished'; question=old.get('question')
 narrative=old['reconciliation'];roster=None;seen=None
 if same:
  roster=copy.deepcopy(old.get('current_roster'));seen=old.get('protocols_seen')
  narrative='Fresh full retrieved text and all published links compared against October17 evidence; no substantive roster difference. '+narrative
 else:
  narrative='October17 result retained as history only; current roster NOT copied without a current substantive comparison. '+narrative
  category='freshness_uncertain' if any(x.get('result')=='retrieved_page' for x in aa) else 'source_unavailable'
  question='Can the current official roster be established from a permitted current retrieval? '+(question or 'Prior roster is not today’s proof.')
 if s['id']=='usa-colorado-state-vth-clinical-trials':
  roster=read(P/'csu-comparison.json')['current_roster'];seen=15;narrative='Current39 whole institution API records and complete published linked roster compared. Only visible fallback text change is honeypot Phone→URL, not a protocol. COTC033 exact site question retained.'
 if s['id']=='registry-avma-veterinary-clinical-trials':
  roster=copy.deepcopy(old['current_roster']);seen=len(roster);narrative='Whole current851 registry records compared field by field, ignoring tag-object ordering only; zero added/removed/changed full records. Two exact Missouri Completed identities now hidden under standing owner decision. UTSW3 remain closed. Penn B-cell Suspended versus provider invitation remains unresolved; no silent activation.'
 if s['id']=='usa-uc-davis-vcct':roster=read(P/'ucd-comparison.json')['current_roster'];seen=12
 if s['id']=='usa-mars-veterinary-health-clinical-trials':roster=read(P/'mars-comparison.json')['current_roster'];seen=11
 if s['id']=='global-vettrials-directory':
  full=[]
  for a in aa:
   if '/api/trials?' in a['url'] and a.get('http_status')==200:full+=json.loads(read(ep(a['evidence_file']))['text'])['data']['trials']
  roster=list({x['id']:x for x in full}.values());assert len(roster)==292;seen=292
  write(P/'vettrials-comparison.json',{'total':292,'whole_current_roster':roster,'current_api_evidence':[c for c in same if '/api/' in c['url']],'comparison':'All three complete API response texts byte-equal to October17 (all full fields, not just hashes); secondary aggregation never overrides current primary or owner dispositions.'})
 if s['id']=='australia-pettrials-directory':roster=read(P/'pettrials-parsed.json')['roster'];seen=7
 if s['id']=='japan-jsamc-current-clinical-trials':
  narrative='Fresh original cp932 response decoded and manually read (jsamc-decoded.txt): current dog antiPD1, cat antiPD1 since August2025, ongoing dog high-grade B-cell antiCD20, dog/cat HIFU heading, FN supportive study. Four proposed PD1 combinations are not four confirmed current cohorts; unpublished protocol limits/costs remain exact gaps.'
 if s['id']=='usa-missouri-oncology-clinical-trials':
  sufficient=False;result='partial';category='protocol_uncertainty';question='Does the legacy carboplatin timing osteosarcoma protocol still enroll? It is absent from today’s five-section roster; no specific Completed identity found. Absence alone does not prove closure.'
  narrative='Fresh whole five-section roster unchanged; AVMA whole completed vinorelbine and Laverdia identities matched and hidden. Legacy carboplatin timing protocol remains a precise unpublished status question, not a reason to label all Missouri unavailable.'
 if s['id']=='usa-veterinary-cancer-care-clinical-trials':
  hit=next((a for a in aa if a['method']=='Web' and a['result']=='retrieved_page' and 'Crawled: today' in a['freshness'] and 'No trials' in a['retrieved_text']),None)
  if hit:sufficient=True;result='fully_reconciled';seen=0;roster=[];narrative='Same official URL recovered through Web, crawl today, explicitly No trials currently enrolling. Past Immunocidin/Canalevia are not current cohorts.'
 if not sufficient and result not in ('not_checked',):
  usable=any(a.get('http_status')==200 and a.get('text_length',0)>200 for a in aa) or any(a['method']=='Web' and a['result']=='retrieved_page' and a['text_length']>1000 for a in aa)
  if not usable and s['id'] in ('usa-anivive-trials','usa-oklahoma-state-clinical-trials'):result='unreachable'
 if sufficient:result='fully_reconciled';question=None;category=None
 elif not question:question='Which exact current primary protocol facts remain unpublished or unconfirmed? '+old.get('next_action','Current full protocol and enrollment facts remain unconfirmed.')
 current_evidence=[{'url':a['url'],'method':a['method'],'at':a['attempted_at'],'result':a['result'],'evidence':a['evidence_file']} for a in aa]
 route_proof=[m for m in mandatory if m['actual_attempt_evidence'] or m['inherited_or_current_prohibition']]
 complete=not unperformed
 assessment='external_blocker' if complete else 'executor_unfinished'
 r={'source_id':s['id'],'source_name':s['name'],'master_url':s['master_url'],'opened_this_run':bool(aa),'content_sufficient':bool(sufficient),'source_result':result,'master_result':'reachable' if sufficient else result,'protocols_seen':seen,'current_roster':roster,'category':category,'question':question,'next_action':old.get('next_action') or 'Read a genuinely new primary protocol signal or the next saved recheck after seven days; do not retry prohibited routes. Daily permitted master/fallback visits remain required.','reconciliation':narrative,'current_comparison_evidence':cc,'actual_attempts':aa,'attempted_urls':aa,'mandatory_routes':mandatory,'processing_complete':complete,'processing_assessment':assessment,'reviewed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'previous_last_checked':s.get('last_checked'),'previous_last_checked_at':s.get('last_checked_at'),'previous_last_result':s.get('last_result'),'previous_content_fingerprint':s.get('content_fingerprint')}
 if not sufficient:
  r['completion_decision']={'remaining_fact':question,'routes_exhausted_evidence':route_proof,'available_reconciliation_done_evidence':{'decision':narrative,'fresh_comparisons':cc,'current_attempts':current_evidence,'canonical_dispositions':'Original canonical IDs retained; UTSW3 and six European quarantines preserved. See clinical ledger for individual primary details and unresolved facts.'}}
  if unperformed:r['unperformed_steps']=['Read permitted mandatory URL '+u for u in unperformed]
 rows.append(r)
write(P/'reviews.json',rows)
write(P/'source-pass-checkpoint.json',{'sealed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'original_source_total':113,'decisions':dict(collections.Counter(r['source_result'] for r in rows)),'visited':sum(r['opened_this_run'] for r in rows),'unperformed_mandatory':{r['source_id']:r['unperformed_steps'] for r in rows if not r['processing_complete']},'clinical_gate':'Separate per-trial review required; source processing never implies a complete clinical audit.'})
print((P/'source-pass-checkpoint.json').read_text())
