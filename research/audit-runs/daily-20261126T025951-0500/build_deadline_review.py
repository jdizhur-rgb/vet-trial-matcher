#!/usr/bin/env python3
import hashlib,json,re
from datetime import date,datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parent
catalog_path=ROOT/'data/trials_base.json'; trials=json.loads(catalog_path.read_text())
pev=json.loads((RUN/'current-protocol-evidence.json').read_text())
attempts={}
for a in pev['attempts']: attempts.setdefault(a['trial_id'],[]).append(a)
today=date(2026,11,26); now=datetime.now(timezone.utc).isoformat(); rows=[]
for t in trials:
    raw=t.get('recruitment_end'); parsed=None
    if isinstance(raw,str):
        try: parsed=date.fromisoformat(raw)
        except ValueError: pass
    basis=t.get('recruitment_end_basis') or {}
    crossed=bool(parsed and parsed<today)
    before=bool(t.get('available_for_matching'))
    current=[{'url':a['url'],'result':a['result'],'status':a.get('status'),
              'completed_at':a.get('completed_at'),'artifact':a.get('artifact')} for a in attempts.get(t['id'],[])]
    extension=False
    result='no_stored_deadline_current_routes_reviewed' if current else 'no_stored_deadline_no_current_protocol_route'
    if parsed:
        if crossed:
            result='deadline_passed_record_already_nonmatchable' if not before else 'deadline_passed_extension_not_confirmed'
        else: result='stored_deadline_future_or_today'
    after=before and not (crossed and not extension)
    rows.append({'record_id':t['id'],'stored_recruitment_end':raw,'original_wording':basis.get('published_wording'),
                 'date_type':basis.get('rule') or ('explicit_recruitment_end' if raw else None),
                 'timezone':t.get('recruitment_end_timezone'),'scope':basis.get('scope'),
                 'primary_url':basis.get('primary_url') or t.get('url'),'original_evidence_read_at':basis.get('original_read_at') or t.get('verified'),
                 'checked_at':now,'deadline_crossed':crossed,'extension_confirmed':extension,
                 'matching_before':before,'matching_after':after,'result':result,'current_attempts':current,
                 'evidence_refs':[str((RUN/'current-protocol-evidence.json').relative_to(ROOT))],
                 'unperformed_steps':[] if current or not before else ['No distinct current protocol route was present in the canonical row for deadline extraction.']})
summary={'records':len(rows),'stored_deadlines':sum(r['stored_recruitment_end'] is not None for r in rows),
         'crossed':sum(r['deadline_crossed'] for r in rows),'active_crossed':sum(r['deadline_crossed'] and r['matching_before'] for r in rows),
         'extensions':sum(r['extension_confirmed'] for r in rows),
         'no_current_date_evidence':sum(r['stored_recruitment_end'] is None for r in rows)}
out={'schema_version':1,'run_id':RUN.name,'baseline_catalog_sha256':hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
     'reviewed_at':now,'today':str(today),'rows':rows,'summary':summary}
(RUN/'deadline-review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2))
