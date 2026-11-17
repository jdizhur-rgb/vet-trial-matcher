"""Record only actual, processed source visits, with before/after history."""
from datetime import datetime
from zoneinfo import ZoneInfo
import json,sys
from pathlib import Path
r=Path(sys.argv[1])
p=Path('data/source_inventory.json')
def load(q):return json.loads(q.read_text())
def put(q,d):q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
inv=load(p)
rows={x['source_id']:x for x in load(r/'receipt-progress.json')['sources']}
events=load(r/'source-route-evidence.json')
fields=['last_checked','last_checked_at','last_result','last_audit_run_id','last_protocols_seen','content_sufficient','processing_complete']
changes=[]
for s in inv['sources']:
    row=rows[s['id']]
    if not row['processing_complete'] or not row['opened_this_run']:continue
    done=[a for a in row['attempted_urls'] if a.get('completed_at')]
    if not done:continue
    newest=max(done,key=lambda a:datetime.fromisoformat(a['completed_at']))
    t=datetime.fromisoformat(newest['completed_at'])
    old=s.get('last_checked_at')
    if old and t<=datetime.fromisoformat(old):continue
    before={n:s.get(n) for n in fields}
    successful=[a for a in done if a.get('http_status')==200 and events.get(a.get('evidence_key'),{}).get('text_sha256')]
    s.update(last_checked=t.astimezone(ZoneInfo('America/New_York')).date().isoformat(),last_checked_at=t.isoformat(),
        last_result=row['master_result'],last_audit_run_id=r.name,last_protocols_seen=row['protocols_seen'],
        content_sufficient=row['content_sufficient'],processing_complete=True,last_visit_timestamp_precision='instant',
        last_processing_review_at=datetime.now(ZoneInfo('America/New_York')).isoformat(),
        last_current_review_finding=row['finding'],last_coverage_receipt=str(r/'receipt-progress.json'),
        last_attempted_urls=[{k:a.get(k) for k in ('url','route','method','result','completed_at','http_status','evidence_file','evidence_key')} for a in done],
        last_coverage_gap=None if row['content_sufficient'] else row['finding'])
    if successful:
        selected=next((a for a in successful if a['url']==s['master_url']),successful[0])
        s.update(last_route_used=selected['route'],content_fingerprint="sha256:"+events[selected['evidence_key']]['text_sha256'],
                 fingerprint_method='sha256 of actual current retrieved text; transport fingerprint alone is not roster proof',
                 last_http_status_at=selected['completed_at'])
    else:
        s.update(last_route_used=None,content_fingerprint=None,fingerprint_method=None)
    changes.append({'source_id':s['id'],'previous':before,'new':{n:s.get(n) for n in fields},
                    'evidence_ref':str(r/'source-route-evidence.json'),'most_recent_actual_attempt':newest})
if changes:
    put(p,inv)
    put(r/'source-date-delta-0840.json',{'run_id':r.name,'recorded_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'updated':changes,'unchanged_count':len(inv['sources'])-len(changes)})
print('updated',len(changes))
