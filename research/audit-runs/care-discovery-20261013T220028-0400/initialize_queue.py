import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
QUEUE = ROOT / 'research/oncology-care-queue'
now = datetime.now(timezone.utc).isoformat()

def read(p): return json.loads((ROOT / p).read_text())
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

centers = read('data/oncology_centers.json')['centers']
inventory = read('data/oncology_care_source_inventory.json')['sources']
states = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR'.split()
coverage = []
for state in states:
    rows = [c for c in centers if c.get('country') == 'USA' and c.get('region') == state]
    mobile = [c for c in rows if c.get('location_type') == 'mobile']
    physical = [c for c in rows if c not in mobile]
    limited = [c for c in physical if c.get('available_for_care') is False or c.get('availability_status') == 'unconfirmed' or 'closed' in str(c.get('operating_status', '')).lower() or 'closed' in str(c.get('availability_status', '')).lower()]
    usable = [c for c in physical if c not in limited]
    modalities = ['Chemotherapy', 'Radiation therapy', 'Radiation oncology', 'Surgical oncology', 'Surgery', 'ECT', 'Immunotherapy', 'Targeted therapy', 'ONCEPT']
    coverage.append({'territory': state, 'listed_address_records': len(physical), 'not_flagged_closed_or_unconfirmed': len(usable), 'explicit_active_status': sum(c.get('operating_status') == 'active' for c in usable), 'operation_status_not_explicit': sum(c.get('operating_status') != 'active' for c in usable), 'limited_or_operation_unconfirmed': [c['name'] for c in limited], 'city_distribution': dict(Counter(c.get('city', '').casefold() for c in usable)), 'catalog_confirmed_service_tags': {m: sum(m in c.get('services', []) for c in usable) for m in modalities}, 'without_specific_treatment_tag': sum(not set(modalities).intersection(c.get('services', [])) for c in usable), 'mobile_service_records': [{'name': c['name'], 'source_id': c.get('source_id'), 'service_area': c.get('service_area'), 'services': c.get('services')} for c in mobile], 'visiting_or_remote_supported_records': [{'name': c['name'], 'care_delivery': c.get('care_delivery'), 'availability_note': c.get('availability_note')} for c in usable if any(t in str([c.get('care_delivery'),c.get('availability_note'),c.get('access_note')]).lower() for t in ['visiting','remote','monthly','partner'])], 'geographic_coverage_complete': False})
write(RUN/'us-coverage-baseline.json', {'baseline_sha':'718b115', 'computed_at':now, 'method':'Complete generated care catalog; counts reflect saved tags, not fresh source verification. Unknown service/operation remains unknown; Surgery is retained legacy label, not a new certification assertion.', 'states':coverage})

pending=[]
for s in inventory:
    questions=s.get('review_questions')
    if questions or s.get('review_required') or s.get('needs_recheck'):
        pending.append({'source_id':s['id'], 'direction':'existing-care-review', 'name':s['name'], 'status':'pending', 'last_substantive_review':s.get('last_reviewed_at') or s.get('evidence_checked_date') or s.get('last_checked'), 'questions':questions or [s.get('recheck_scope') or s.get('last_review_note') or 'Review flag requires scoped clarification'], 'urls':list(dict.fromkeys([s['master_url']]+s.get('supporting_urls',[]))), 'recheck_after':s.get('recheck_after') or s.get('recheck_on') or '2026-10-20', 'reference':s.get('review_reference') or s.get('last_review_run_id') or s.get('last_run_id'), 'successful_verification_date_refreshed':False})
six='research/audit-runs/six-worker-test-publish-20261012/'
leads=[]
for n in [5,6]:
    q=read(six+f'worker{n}-queries.json')
    for lead in q['unprocessed_remainder']:
        leads.append({**lead,'source_id':None,'status':'unprocessed','reference':six+f'worker{n}-queries.json','last_substantive_review':None,'recheck_after':None})
    result=read(six+f'worker{n}-result.json')
    candidates=result.get('candidates') or result.get('discovery',{}).get('candidates',[])
    for c in candidates:
        if c.get('classification') == 'UNRESOLVED' or c.get('core_fields_sufficient') is False:
            pending.append({'source_id':c.get('source_id'),'direction':'discovery','status':'pending','name':c.get('name'), 'territory':c.get('territory') or c.get('country'), 'recheck_after':'2026-10-20','reference':six+f'worker{n}-result.json','saved_candidate':c,'successful_verification_date_refreshed':False})
integration=read(six+'integration.json')
for d in integration['deferred']:
    pending.append({**d,'direction':'existing-care-review' if d.get('source_id') else 'discovery','status':'pending','recheck_after':'2026-10-20','reference':six+'integration.json','last_substantive_review':None,'successful_verification_date_refreshed':False})
two=RUN/'prior-two-worker'
two.mkdir(exist_ok=True)
for n in [1,2]:
    source=ROOT.parent/'delegation-test'/f'worker{n}'
    for filename in ['result.json','proposed_changes.json','report.md']:
        if (source/filename).exists(): (two/f'worker{n}-{filename}').write_bytes((source/filename).read_bytes())
    result=json.loads((source/'result.json').read_text())
    for row in result['records']:
        if not row.get('fully_verified'):
            pending.append({'source_id':row.get('source_id'),'direction':'existing-care-review','status':'pending','recheck_after':'2026-10-20','reference':str((two/f'worker{n}-result.json').relative_to(ROOT)),'saved_record':row,'successful_verification_date_refreshed':False})
assignments=[{'territory':s,'agent_id':f'/root/discovery_{s.lower()}','direction':'US discovery','baseline_sha':'718b115','candidate_limit':3,'status':'running','result_directory':str((RUN/s).relative_to(ROOT))} for s in ['ND','SD','WV','AR','NE','KY']]
run=json.loads((RUN/'run.json').read_text());run['assignments']=assignments;run['spawn_agent']='PASS: six actual spawn calls returned six canonical agent IDs';write(RUN/'run.json',run)
write(QUEUE/'state.json',{'schema_version':1,'updated_at':now,'active_run':RUN.name,'prior_weekly_run':'disabled by owner; not modified','prior_batched_queue':'research/audit-runs/care-batched-20261011T143110-0400/queue.json','prior_batched_status':'historical IN_PROGRESS; current inventory and published A–E/P00/six receipts supersede proposals; do not resume old snapshots','pending':pending,'unprocessed_leads':leads,'existing_review_cursor':{'after_source_id':None,'next_rule':'oldest substantive successful review, due flags first; never restart completed sources'},'publication_policy':'field-scoped fresh-main serial integration; no external messages; no user text/UI changes'})
write(QUEUE/'assignments.json',{'run_id':RUN.name,'assignments':assignments})
territories=[{'territory':x['territory'],'direction':'US discovery','status':'assigned' if x['territory'] in ['ND','SD','WV','AR','NE','KY'] else 'not_started_in_daily_queue','coverage_reference':str((RUN/'us-coverage-baseline.json').relative_to(ROOT)),'remaining':'Not exhaustive; regional treatment geography and unprocessed leads remain','completed':False} for x in coverage]
for country in ['Canada','United Kingdom','Japan','continental Europe','Australia/New Zealand','Latin America','Middle East','Africa','other Asia']:
    territories.append({'territory':country,'direction':'international discovery','status':'partial_prior_search' if country in ['Canada','United Kingdom','Japan'] else 'not_started_in_daily_queue','completed':False,'remaining_leads':[l for l in leads if l.get('territory') in [country,{'United Kingdom':'UK','Canada':'Ontario'}.get(country)]]})
write(QUEUE/'territories.json',{'schema_version':1,'territories':territories})
print('QUEUE_INITIALIZED',len(pending),'pending',len(leads),'unprocessed leads',len(coverage),'US areas')
