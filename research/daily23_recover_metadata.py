"""Recover a proven native response, never create a new visit from a file timestamp."""
from daily23 import *
from email.utils import parsedate_to_datetime
import re,hashlib
plan=read(RUN/'master-plan.json');x=next(x for x in plan if x['source_id']=='canada-saskatchewan-wcvm-research-requests');f=RUN/'evidence/0dfa73bebb524498c1.json';h=m.RAW/'0dfa73bebb524498c1.headers';body=m.RAW/'0dfa73bebb524498c1.body';headers=h.read_text();d=read(f)
assert 'WCVM scientists seeking dogs with spreading cancer' in d['text']
t=parsedate_to_datetime(re.findall(r'(?im)^date:\s*(.+)',headers)[-1]).astimezone(ZoneInfo('America/New_York')).isoformat()
r=dict(**x,attempted_at=t,completed_at=t,method='shell_curl',retry=0,http_status=200,effective_url=x['url'],content_type='text/html; charset=UTF-8',exit_code=0,text_length=len(d['text']),text_sha256=hashlib.sha256(d['text'].encode()).hexdigest(),evidence_file=str(f.relative_to(ROOT)),raw_file=str(body),result='retrieved_page',timestamp_basis='Retained HTTP Date of actual response; original client timestamp missing from consolidated ledger. No file mtime used. Not a new request.',metadata_recovery=True)
if not any(m.route_key(a['url'])==m.route_key(x['url']) for a in attempts()):
 with (RUN/'attempts.jsonl').open('a') as out:out.write(json.dumps(r)+'\n')
write(RUN/'metadata-recovery.json',dict(at=now(),original_stdout='/workspace/scratch/7a43f0b7d905/master23.log line60',current_retained_native_page=str(f.relative_to(ROOT)),retained_response_headers_sha256=hashlib.sha256(h.read_bytes()).hexdigest(),actual_response_timestamp=t,limitation='Original client start/end lost; HTTP response Date used explicitly, not represented as recovered client timing. The source was actually fetched; no second traversal.',recovered_row=r))
print('Recovered actual HTTP response Date',t)
p=[];seen={m.route_key(a['url']) for a in attempts()}
for l in d['links']:
 if l['label'] in ['WCVM scientists seeking dogs with spreading cancer for clinical trial','Radiation oncology trials'] and m.route_key(l['url']) not in seen and m.route_key(l['url']) not in m.known_denials():p.append(dict(source_id=x['source_id'],url=l['url'],route='obvious_current_primary_navigation'))
write(RUN/'saskatchewan-primary-plan.json',p);print(p)
