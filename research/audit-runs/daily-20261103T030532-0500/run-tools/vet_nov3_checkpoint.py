import json,pathlib,time
from datetime import datetime
from zoneinfo import ZoneInfo
R=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103/research/audit-runs/daily-20261103T030532-0500')
baseline=json.loads((R/'execution-baseline.json').read_text())
limit=datetime.fromisoformat(baseline['execution_deadline']);last=0
while not (R/'CHECKPOINTS_STOP').exists():
 now=datetime.now(ZoneInfo('America/New_York'))
 if now>=limit:break
 if time.monotonic()-last>=600:
  try:
   sources=json.loads((R/'individual-source-decisions.json').read_text())
   clinical=json.loads((R/'completed-clinical-reviews.json').read_text())
   review=json.loads((R/'execution-review.json').read_text())
   value={'at':now.isoformat(),'run_id':R.name,'execution_deadline':limit.isoformat(),'seconds_elapsed':(now-datetime.fromisoformat(baseline['started_at'])).total_seconds(),'seconds_remaining':(limit-now).total_seconds(),'source_decision_ids':list(sources),'source_processing_complete_ids':[sid for sid,s in sources.items() if s.get('processing_complete') is True],'source_ids_without_decision':[sid for sid in baseline['source_ids'] if sid not in sources],'full_current_clinical_review_ids':[t['trial_id'] for t in clinical],'issue_updates_saved':review.get('issue_updates',[]),'discovery_queries_saved':review.get('discovery_queries',[]),'remaining_work_note':'Actual saved state only; unreviewed sources/issues are not converted into external blockers. Continuous audit still executing.','stop':False}
   target=R/('segment-auto-'+now.strftime('%H%M%S')+'.json');target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');last=time.monotonic()
  except (OSError,ValueError):pass
 time.sleep(30)
