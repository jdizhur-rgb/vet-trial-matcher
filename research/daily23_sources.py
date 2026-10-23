"""October23 single-pass source reconciliation, explicit current content comparisons."""
from daily23 import ROOT,RUN,OLD,read,write,now,m,attempts,checkpoint
import json,copy,collections,hashlib
rel=str(RUN.relative_to(ROOT));native=attempts();web=read(RUN/'accepted-Web-attempts.json');comps=read(RUN/'full-comparisons.json')
inv=read(RUN/'before-source_inventory.json');old={r['source_id']:r for r in read(RUN/'previous-receipt.json')['sources']}
new=read(RUN/'discovered-source-definitions.json') if (RUN/'discovered-source-definitions.json').exists() else []
inv['sources'].extend(new)
manual=read(RUN/'manual-source-decisions.json')
same_roster=set(read(RUN/'same-roster-decisions.json'))
explicit=read(RUN/'explicit-roster-decisions.json')
portals={'registry-avma-veterinary-clinical-trials':'avma','usa-colorado-state-vth-clinical-trials':'csu','usa-uc-davis-vcct':'ucd','usa-mars-veterinary-health-clinical-trials':'mars','global-vettrials-directory':'vettrials'}
restrictions=read(RUN/'restrictions-frozen.json')+read(RUN/'web-denials.json')
if (RUN/'new-denials.jsonl').exists():restrictions += [json.loads(l) for l in (RUN/'new-denials.jsonl').read_text().splitlines()]
denied={m.route_key(r['url']):r for r in restrictions};rows=[];gaps=[]
for s in inv['sources']:
 sid=s['id'];p=old.get(sid,{});urls=[s['master_url']]+s.get('fallback_urls',[]);keys={m.route_key(u) for u in urls}
 aa=[a for a in native+web if m.route_key(a['url']) in keys or a.get('source_id')==sid]
 cc=[c for c in comps if m.route_key(c['url']) in keys or c['source_id']==sid]
 master_equal=any(m.route_key(c['url'])==m.route_key(s['master_url']) and c['same_entire_text'] and c['same_entire_semantic_linkset'] for c in cc)
 roster=copy.deepcopy(p.get('current_roster')) if master_equal else None;count=p.get('protocols_seen') if master_equal else None
 sufficient=bool(master_equal and p.get('content_sufficient'));known=master_equal
 narrative='Fresh entire master text and complete semantic linkset equal the accepted October22 content; prior mapped roster explicitly compared, not copied from a fingerprint. Original detailed clinical dates remain unchanged.' if master_equal else 'No historical roster reused without a fresh explicit comparison.'
 category=p.get('category') or 'protocol_uncertainty';question=p.get('question') or 'Current complete protocol, eligible cohort, owner access and expenses are not established by the published primary content.'
 if sid in manual:narrative=manual[sid];known=True
 if sid in same_roster:
  roster=copy.deepcopy(p.get('current_roster'));count=p.get('protocols_seen');sufficient=bool(p.get('content_sufficient'))
 if sid in portals:
  name=portals[sid];v=read(RUN/(name+'-comparison.json'));known=True
  if name=='avma':roster=[x for x in v['current_roster'] if any(t.get('tag_path')=='primary-field-19_oncology-1' for t in x.get('visible_sc_items',[]))] if v['pagination_complete'] else None;count=len(roster) if roster is not None else None;sufficient=False
  elif name=='vettrials':roster=[x for x in v['current_roster'] if x.get('conditionCategory')=='oncology'] if v['pagination_complete'] else None;count=len(roster) if roster is not None else None;sufficient=False
  else:
   unchanged=v['pagination_complete'] and not v['changed'] and not v['added'] and not v['missing']
   if unchanged:roster=copy.deepcopy(p.get('current_roster'));count=p.get('protocols_seen');sufficient=bool(p.get('content_sufficient'))
   else:roster=None;count=None;sufficient=False
  narrative='All current public objects and pagination actually compared in '+name+'-comparison.json. '+str(v['total'])+' unique versus reported '+str(v['reported_totals'])+'. Changes '+str(v['changed'])+', additions '+str(v['added'])+', missing '+str(v['missing'])+'. Whole object comparison preserves the explicitly mapped prior roster only if all relevant objects are identical; it does not renew clinical dates. Current primary conflicts are retained separately.'
 if sid in explicit:
  z=explicit[sid];roster=z['roster'];count=len(roster) if roster is not None else None;sufficient=z['sufficient'];category=z.get('category','protocol_uncertainty');question=z.get('question',question);known=True
 missing=[u for u in urls if not any(m.route_key(a['url'])==m.route_key(u) for a in aa) and m.route_key(u) not in denied]
 banned_all=all(m.route_key(u) in denied for u in urls)
 complete=bool((known and not missing) or banned_all)
 if sufficient:complete=True;missing=[]
 assessment='external_blocker' if complete and not sufficient else 'not_applicable' if sufficient else 'executor_unfinished' if missing else 'not_established'
 if sid=='uk-cambridge-veterinary-clinical-trials':complete=False;assessment='not_established';narrative='No current visit. Explicit master403 preserved; permission scope of unresolved node/2971 alias not established, so it was not used as a workaround.';missing=[]
 actual=list(aa)
 for a in aa:
  if a.get('effective_url') in urls and a['effective_url']!=a['url'] and not any(b['url']==a['effective_url'] for b in actual):
   actual.append(dict(a,url=a['effective_url'],original_requested_url=a['url'],route='actual_redirect_target',not_a_separate_visit=True))
 actual += [dict(url=u,method='none',result='NOT_VISITED_PRIOR_PROHIBITION',not_a_current_attempt=True,restriction_evidence=denied.get(m.route_key(u)) or dict(url=u,do_not_retry=True,origin='Cambridge inherited unresolved action-scope question')) for u in urls if not any(m.route_key(a['url'])==m.route_key(u) for a in aa) and (m.route_key(u) in denied or sid=='uk-cambridge-veterinary-clinical-trials')]
 latest=max(aa,key=lambda a:a['attempted_at']) if aa else None
 result='fully_reconciled' if sufficient else 'partial' if aa else 'not_checked'
 if sid in ['usa-anivive-trials','usa-oklahoma-state-clinical-trials','usa-veterinary-oncology-services-trials'] and aa:result='unreachable';category='source_unavailable'
 summary_attempts=[{k:v for k,v in a.items() if k not in ['retrieved_text','raw_file','stderr']} for a in aa]
 refs=[dict(comparison_file=rel+'/full-comparisons.json',comparison_index=comps.index(c),url=c['url'],same_entire_text=c['same_entire_text'],same_entire_semantic_linkset=c['same_entire_semantic_linkset'],actual_attempt={k:c['actual_attempt'].get(k) for k in ['attempted_at','method','evidence_file']}) for c in cc]
 steps=['Open and reconcile permitted route '+u for u in missing]
 if sid=='uk-cambridge-veterinary-clinical-trials':steps=['Establish inherited alias action-permission scope without replaying the denied master or using the alias as a workaround.']
 if not complete and not steps:steps=['Finish source-specific semantic reconciliation of currently retrieved pages and protocol navigation.']
 saved_result=('unchanged' if sufficient and master_equal else 'reachable' if sufficient else result) if latest else s.get('last_result')
 rr=dict(source_id=sid,source_name=s['name'],master_url=s['master_url'],opened_this_run=bool(aa),content_sufficient=sufficient,source_result=result,master_result=saved_result,protocols_seen=count,current_roster=roster,route_used=sorted({a['method'] for a in aa}),actual_attempts=summary_attempts,attempted_urls=actual,current_comparison_evidence=refs,processing_complete=complete,processing_assessment=assessment,category=None if sufficient else category,question=None if sufficient else question,reconciliation=narrative,unperformed_steps=steps,previous_last_checked=s.get('last_checked'),previous_last_checked_at=s.get('last_checked_at'),previous_last_result=s.get('last_result'),new_last_checked=latest['attempted_at'][:10] if latest else s.get('last_checked'),new_last_checked_at=latest['attempted_at'] if latest else s.get('last_checked_at'),new_last_result=saved_result)
 rr['mandatory_routes']=[dict(url=u,actual_attempt_evidence=[dict(at=a['attempted_at'],method=a['method'],evidence=a['evidence_file']) for a in aa if m.route_key(a['url'])==m.route_key(u)],inherited_or_current_prohibition=denied.get(m.route_key(u))) for u in urls]
 if not sufficient:
  rr['completion_decision']=dict(remaining_fact=question,routes_exhausted_evidence=rr['mandatory_routes'],available_reconciliation_done_evidence=dict(current_full_comparisons=refs,source_specific_current_review=narrative,prior_protocol_questions_preserved=rel+'/prior-issues.json'))
  gaps.append(dict(source_id=sid,category=category,processing_assessment=assessment,question=question,reason=narrative,next_action='Follow exact missing study fact when a new primary signal appears or its original recheck date is due; no whole-source automatic requeue.',unperformed_steps=steps,completion_decision=rr['completion_decision'],evidence=dict(source_id=sid,attempted_urls=[a['url'] for a in actual],current_attempts=summary_attempts)))
 if latest:
  s.update(last_checked=rr['new_last_checked'],last_checked_at=rr['new_last_checked_at'],last_result=saved_result,last_attempts=summary_attempts,last_route_used=rr['route_used'],audit_last_run_id=RUN.name,last_audit_run_id=RUN.name,last_protocols_seen=count,content_sufficient=sufficient,last_check_summary=narrative,last_coverage_receipt=rel+'/receipt-final.json')
  s.update(last_http_status=latest.get('http_status'),last_http_status_at=latest['attempted_at'])
  usable=[a for a in aa if a.get('http_status')==200 and a.get('text_sha256') and a.get('text_length',0)>100]
  if usable:s.update(content_fingerprint='sha256:'+usable[0]['text_sha256'],fingerprint_method='Actual retrieved current text, not a claim of clinical/roster verification.')
 rows.append(rr)
inv['updated']='2026-10-23';write(ROOT/'data/source_inventory.json',inv)
write(RUN/'new-sources.json',new)
receipt=dict(run_id=RUN.name,mode='DAILY GLOBAL WORK AUDIT',started_at=read(RUN/'baseline.json')['started_at'],source_total=len(rows),attempted_total=sum(r['opened_this_run'] for r in rows),content_sufficient_total=sum(r['content_sufficient'] for r in rows),processing_complete_total=sum(r['processing_complete'] for r in rows),source_result_counts=dict(collections.Counter(r['source_result'] for r in rows)),executor_incomplete_source_ids=[r['source_id'] for r in rows if not r['processing_complete']],executor_unfinished_actions=sum(len(r['unperformed_steps']) for r in rows),unconfirmed_processing_sources=sum(r['processing_assessment']=='not_established' for r in rows),source_pass_at=now(),strict_status='INCOMPLETE',sources=rows)
write(RUN/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt);write(RUN/'gap-review.json',dict(original_run_id=RUN.name,rows=gaps))
persisted={s['id']:s for s in read(ROOT/'data/source_inventory.json')['sources']}
write(RUN/'local-date-readback.json',dict(at=now(),source_inventory_sha256=hashlib.sha256((ROOT/'data/source_inventory.json').read_bytes()).hexdigest(),current_attempt_dates_verified=all(persisted[r['source_id']]['last_checked_at']==r['new_last_checked_at'] and persisted[r['source_id']]['last_result']==r['new_last_result'] for r in rows if r['opened_this_run']),unvisited_dates_and_results_retained=all(r['new_last_checked']==r['previous_last_checked'] and r['new_last_checked_at']==r['previous_last_checked_at'] and r['new_last_result']==r['previous_last_result'] for r in rows if not r['opened_this_run']),rows=[{k:r.get(k) for k in ['source_id','opened_this_run','previous_last_checked','new_last_checked','previous_last_checked_at','new_last_checked_at','previous_last_result','new_last_result']} for r in rows]))
write(RUN/'source-manual-review.json',dict(at=now(),reviews=manual,comparison_receipt=rel+'/full-comparisons.json'))
checkpoint();print(json.dumps({k:v for k,v in receipt.items() if k!='sources'}));print('UNPROVEN',[r['source_id'] for r in rows if not r['processing_complete']])
