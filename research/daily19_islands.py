"""Extract only public protocol data islands; never export service configuration."""
from daily19 import ROOT,RUN,OLD,read,write,m
import json,re,difflib
def island(raw,key):
 match=re.search(r'<script\s+id="'+re.escape(key)+r'"[^>]*>(.*?)</script>',raw,re.S)
 return json.loads(match.group(1)) if match else None
def extract(a):
 path=Path(a['raw_file'])
 if not path.exists():return None
 raw=path.read_text(errors='replace');content=island(raw,'d_sv_content')
 if not content:return None
 values=island(raw,'d_sv_values') or {};flags=island(raw,'d_sv_flags') or {}
 public_values={k:values.get(k) for k in ['publicId','studypageStatus','studyStartDate','studyEndDate','contactName','contactEmail','spPhoneConditional','iacucNumber','avmaId','studyCode']}
 public_flags={k:flags.get(k) for k in ['is_studypage_active','is_active','is_active_nyr','is_finished_rec','join_button_enabled','requires_login']}
 return json.loads(m.redact_text(json.dumps({'protocol':content,'status_contact':public_values,'availability_flags':public_flags,'published_locations':island(raw,'d_sv_locations_display'),'published_investigators':island(raw,'d_sv_investigators_list'),'published_pdfs':island(raw,'d_sv_study_pdfs')})))
from pathlib import Path
old=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()]
prior={m.route_key(a['url']):a for a in old if a.get('http_status')==200}
rows=[]
for a in [json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]:
 if a.get('http_status')!=200:continue
 x=extract(a)
 if not x:continue
 b=prior.get(m.route_key(a['url']));y=extract(b) if b else None
 same=bool(y and x==y);row={'trial_id':a['source_id'].removeprefix('protocol:'),'url':a['url'],'actual_attempt':a,'extraction_is_not_new_visit':True,'public_protocol':x,'previous_attempt':b,'same_entire_public_protocol_object':same,'changes':None if same or not y else '\n'.join(difflib.unified_diff(json.dumps(y,ensure_ascii=False,indent=2).splitlines(),json.dumps(x,ensure_ascii=False,indent=2).splitlines()))}
 rows.append(row);print(row['trial_id'],'same full public object',same,'changes',str(row['changes'])[:2500])
write(RUN/'public-protocol-islands.json',rows)
