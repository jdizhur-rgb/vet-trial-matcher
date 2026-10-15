"""Freeze final research-only delivery evidence; do not mutate canonical data."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path(__file__).resolve().parent
now = datetime.now(ZoneInfo('America/New_York')).isoformat()
def save(name, data):
    (P / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

save('live-catalog-dom.json', {
    'attempted_after': '2026-10-15T04:49:04-04:00',
    'method': 'browser_DOM', 'status': 'NOT VERIFIED',
    'result': 'Browser URL policy rejected read-only evaluation after JSON navigation; no payload returned; no workaround attempted.',
    'does_not_replace': 'Actual live USA/Japan search proof in live-search.json',
})
save('run-closure.json', {
    'run_id': P.name, 'started_at': '2026-10-15T03:02:25-04:00',
    'report_evidence_cutoff_at': '2026-10-15T04:49:42-04:00',
    'closure_prepared_at': now,
    'source_processing_complete': 111, 'source_new_visits': 105,
    'discovery_regions_complete': 12, 'discovery_passes_complete': 2,
    'executor_source_actions_unfinished': 0,
    'source_evidence_status': 'INCOMPLETE', 'source_gaps': 45,
    'live_search': 'PASS', 'latest_live_asset_byte_verification': 'NOT VERIFIED',
    'execution_compliance': 'FAIL: global request peak and checkpoint cadence',
    'data_publication_sha': '2ef665ae0659ae721776f2f2cdba8665e3a99ce0',
    'report_sha256': hashlib.sha256((P / 'report.md').read_bytes()).hexdigest(),
    'no_background_continuation_claimed': True,
})
(P / 'segment-06.md').write_text(
    f'# Final research closure\n\nRecorded: {now}\n\n'
    '111 source decisions; 105 new visits; 66 fully reconciled, 35 partial, '
    '4 unreachable, 6 inherited gates not checked. Two discovery passes, 12/12 regions. '
    'Data main 2ef665ae0659ae721776f2f2cdba8665e3a99ce0 and deploy successful. '
    'Actual live USA/Japan PASS; latest raw asset bytes NOT VERIFIED. '
    'Final exact Russian report saved; research-only publication follows.\n')
files = []
for p in sorted(P.rglob('*')):
    if not p.is_file() or p.name in ['manifest.json', '.native-request-batch.lock'] or '__pycache__' in p.parts:
        continue
    data = p.read_bytes()
    files.append({'path': str(p.relative_to(P)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
save('manifest.json', {'run_id': P.name, 'created_at': now, 'excluded': ['manifest.json (self)', '.native-request-batch.lock', '__pycache__'], 'files': files})
print(json.dumps({'files': len(files), 'report_sha256': hashlib.sha256((P/'report.md').read_bytes()).hexdigest(), 'at': now}))
