"""Serialize current audit evidence and preserve the predecessor in accounting."""
from pathlib import Path
import sys, json, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter

run = Path(sys.argv[1])
old = Path('research/audit-runs/daily-20261117T030023-0500')
old_disk = Path('../vtf-audit') / old
now = datetime.now(ZoneInfo('America/New_York')).isoformat()
def load(path):
    return json.loads(path.read_text())
def write(name, body):
    (run/name).write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
def kfor(url):
    return hashlib.sha256(url.encode()).hexdigest()[:20]
def routeev(k):
    for area in ('evidence','structured','pdf-ocr'):
        p=run/area/(k+'.json')
        if p.exists(): return load(p)
    return None
bundle={}
def bundle_evidence(obj):
    k=obj['evidence_key']
    if k in bundle:return
    bundle[k]={x:obj.get(x) for x in ('evidence_key','url','effective_url','method','attempts','result','http_status','body_sha256','text_sha256','text_length','restriction')}
manual={}
for path in [run/'source-reconciliation-slice.tsv',run/'source-reconciliation-next.tsv',run/'source-reconciliation-rosters.tsv',run/'source-reconciliation-latest.tsv']:
    if not path.exists():continue
    for line in path.read_text().splitlines():
        sid,state,keys,ids,finding=line.split('\t')
        assert sid not in manual or path.name == "source-reconciliation-latest.tsv", sid
        manual[sid]=state,keys.split(';'),[x for x in ids.split(';') if x],finding

ref=str(run/'source-route-evidence.json')
plans={t['source_id']:t for t in load(run/'unfinished-source-plan.json')}
historical={s['source_id']:s for s in load(old/'receipt-final.json')['sources']}
inventory=load(Path('data/source_inventory.json'))
catalog={x['id']:x for x in load(Path('data/trials_base.json'))}
rows,decisions,gaps,progress=[],[],[],[]
for t in inventory['sources']:
    sid=t['id']; h=historical[sid]; s=plans.get(sid); m=manual.get(sid)
    status, keys, ids, finding = m or ('working', [], [], None)
    keys=list(dict.fromkeys(keys+[kfor(u) for u in [s['master']]+s['fallbacks']])) if s else []
    data=[d for x in keys if (d:=routeev(x))]
    for d in data: bundle_evidence(d)
    same=[]
    for d in data:
        prior=old_disk/'evidence'/(d['evidence_key']+'.json')
        if prior.exists() and d.get('body_sha256'):
            z=load(prior)
            if z.get('body_sha256'):
                same.append({'old_body_sha256':z['body_sha256'],'current_body_sha256':d['body_sha256'],'whole_response_equal':z['body_sha256']==d['body_sha256'],'url':d['url'],'old_attempt_not_a_new_visit':True})
    actual=[]
    master=kfor(s['master']) if s else ''
    for d in data:
        for a in d.get('attempts',[]):
            actual.append(dict(a,route='master' if d['evidence_key']==master else 'official_fallback_or_leaf',method=d['method'],evidence_file=ref,evidence_key=d['evidence_key'],result=('retrieved' if a.get('http_status')==200 and not a.get('exit_code') else 'error_or_redirect')))
        if not d.get('attempts') and d.get('restriction'):
            actual.append({'url':d['url'],'route':'master' if d['evidence_key']==master else 'official_fallback_or_leaf','method':'restriction_review_no_request','result':'exact_route_not_retried','evidence_file':ref,'evidence_key':d['evidence_key'],'original_restriction':d['restriction']})
    if s:
        opened=any(a['method']!='restriction_review_no_request' for a in actual)
        complete=status in {'roster','external','discovery'}
        sufficient=status=='roster' and opened and bool(actual)
        attempt_ts=max((a.get('completed_at','') for a in actual),default='') or None
        steps=[] if complete else s['remaining']
        if not finding:
            found=[f"{d['url']}: {d['result']}, HTTP {d.get('http_status','n/a')}" for d in data]
            finding='Transport evidence only. '+' | '.join(found)
        if sufficient:
            assert all(i in catalog for i in ids),sid
        visible='reachable' if sufficient else ('partial' if opened and any(a.get('http_status')==200 for a in actual) else 'unreachable' if opened else 'not_checked')
    else:
        opened=False
        complete=False
        sufficient=False
        attempt_ts=None
        steps=[]
        finding='Completed portion of predecessor checkpoint; no repeated current visit. Original handling and dates retained separately.'
        actual=[{**a,'inherited_attempt_not_current':True} for a in h.get('attempted_urls',[])]
        visible='not_checked'
    result={'source_id':sid,'opened_this_run':opened,'processing_complete':complete,'content_sufficient':sufficient,'protocols_seen':len(ids) if sufficient else None,
        'master_result':visible,'attempted_urls':actual,'route_used':next((a['route'] for a in actual if a.get('http_status')==200),None) if opened else None,
        'current_response_comparison_evidence':same,'previous_last_checked':t.get('last_checked'),'previous_last_checked_at':t.get('last_checked_at'),'continuation_latest_attempt_at':attempt_ts,
        'finding':finding,'cumulative_previous_processing_complete':h.get('processing_complete') is True,'cumulative_previous_content_sufficient':h.get('content_sufficient') is True,
        'previous_receipt_ref':str(old/'receipt-final.json')}
    rows.append(result)
    dec={'source_id':sid,'reviewed_at':now,'finding':finding,
        'evidence_refs':[ref] if s else [str(old/'receipt-final.json')],
        'remaining_available_steps':steps,'completion_basis':finding if complete else None,
        'current_official_content':sufficient,'roster_complete':sufficient,'protocols':ids if sufficient else [],
        'catalog_comparison':({'identities':ids,'finding':finding} if sufficient else None),
        'roster_evidence_refs':[ref] if sufficient else [], 'change_reviews':[]}
    decisions.append(dec)
    if not sufficient:
        if s and complete:
            assess='external_blocker'
            cat='discovery_source_not_trial_roster' if status=='discovery' else ('source_unavailable' if visible=='unreachable' else 'protocol_uncertainty')
        elif s:
            assess='executor_unfinished'
            cat='roster_unestablished'
        else:
            assess='not_established'
            cat='freshness_uncertain'
        row=dict(source_id=sid,category=cat,processing_assessment=assess,question=(finding if complete else 'Current full roster and catalog disposition for '+sid),
            reason=finding,next_action=('Recheck only on new permitted official record or scheduled due date' if complete else steps[0] if steps else 'Use predecessor exact evidence; no repeat needed for cumulative sweep'),
            evidence={'source_id':sid,'attempted_urls':list(dict.fromkeys(a['url'] for a in actual if a.get('url')))})
        if assess=='external_blocker':
            row['completion_decision']={'remaining_fact':row['question'],'routes_exhausted_evidence':row['evidence']['attempted_urls'],'available_reconciliation_done_evidence':finding}
        elif assess=='executor_unfinished':row['unperformed_steps']=steps
        gaps.append(row)
    progress.append({'source_id':sid,'segment_disposition':status if s else 'covered_in_predecessor','completed_this_segment':complete,
        'processed_cumulative':complete or h.get('processing_complete') is True, 'sufficient_cumulative':sufficient or h.get('content_sufficient') is True})
write('source-route-evidence.json',bundle)
write('source-decisions-progress.json',decisions)
write('source-progress-summary.json',{'run_id':run.name,'as_of':now,'segment_states':dict(Counter(x['segment_disposition'] for x in progress)),
        'transport_fresh_sources':sum(x['opened_this_run'] for x in rows),'processed_cumulative':sum(x['processed_cumulative'] for x in progress),
        'sufficient_cumulative':sum(x['sufficient_cumulative'] for x in progress),'rows':progress})
write('receipt-progress.json',{'run_id':run.name,'time_context':'America/New_York','recorded_at':now,'status':'IN_PROGRESS','source_total':len(rows),
       'attempted_total':sum(x['opened_this_run'] for x in rows),'content_sufficient_total':sum(x['content_sufficient'] for x in rows),'sources':rows})
write('gap-progress.json',{'original_run_id':run.name,'recorded_at':now,'rows':gaps})
