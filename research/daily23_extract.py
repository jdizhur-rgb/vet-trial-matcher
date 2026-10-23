"""Current complete public objects and whole paginated rosters, not HTTP proof."""
from daily23 import ROOT,RUN,OLD,read,write,m,attempts
from pathlib import Path
import json,re,difflib,collections
def island(raw,key):
 v=re.search(r'<script\s+id="'+re.escape(key)+r'"[^>]*>(.*?)</script>',raw,re.S)
 return json.loads(v.group(1)) if v else None
def extract(a):
 p=Path(a['raw_file'])
 if not p.exists():return None
 raw=p.read_text(errors='replace');c=island(raw,'d_sv_content')
 if not c:return None
 v=island(raw,'d_sv_values') or {};f=island(raw,'d_sv_flags') or {}
 return json.loads(m.redact_text(json.dumps({'protocol':c,'status_contact':{k:v.get(k) for k in ['publicId','studypageStatus','studyStartDate','studyEndDate','contactName','contactEmail','spPhoneConditional','iacucNumber','avmaId','studyCode']},'availability_flags':{k:f.get(k) for k in ['is_studypage_active','is_active','is_active_nyr','is_finished_rec','join_button_enabled','requires_login']},'published_locations':island(raw,'d_sv_locations_display'),'published_investigators':island(raw,'d_sv_investigators_list'),'published_pdfs':island(raw,'d_sv_study_pdfs')})))
old=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines()];prior={m.route_key(a['url']):a for a in old if a.get('http_status')==200};aa=attempts();rows=[]
for a in aa:
 if a.get('http_status')!=200:continue
 x=extract(a)
 if not x:continue
 b=prior.get(m.route_key(a['url']));old_islands={m.route_key(z['url']):z for z in read(OLD/'public-protocol-islands.json')};y=old_islands.get(m.route_key(a['url']),{}).get('public_protocol');same=bool(y and x==y)
 rows.append({'trial_id':a['source_id'].removeprefix('protocol:'),'url':a['url'],'actual_attempt':a,'extraction_is_not_new_visit':True,'public_protocol':x,'previous_attempt':b,'same_entire_public_protocol_object':same,'changes':None if same or not y else '\n'.join(difflib.unified_diff(json.dumps(y,ensure_ascii=False,indent=2).splitlines(),json.dumps(x,ensure_ascii=False,indent=2).splitlines()))})
 print('ISLAND',a['source_id'],'same',same,'diff',str(rows[-1]['changes'])[:1800])
write(RUN/'public-protocol-islands.json',rows)
def normal(v):
 if isinstance(v,dict):return {k:sorted([normal(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True)) if k=='visible_sc_items' else normal(x) for k,x in v.items()}
 if isinstance(v,list):return [normal(x) for x in v]
 return v
for sid,name in [('registry-avma-veterinary-clinical-trials','avma'),('usa-colorado-state-vth-clinical-trials','csu'),('usa-uc-davis-vcct','ucd'),('usa-mars-veterinary-health-clinical-trials','mars'),('global-vettrials-directory','vettrials')]:
 ax=[a for a in aa if a['source_id']==sid and a.get('http_status')==200 and ('/studies/search/json/' in a['url'] or '/api/trials?' in a['url'])];allrows=[];totals=[]
 for a in ax:
  d=json.loads(read(ROOT/a['evidence_file'])['text']);allrows+=d['studies'] if name!='vettrials' else d['data']['trials'];totals.append(d.get('total') if name!='vettrials' else d['data']['pagination']['total'])
 cur=list({x['id']:x for x in allrows}.values());prev=read(OLD/(name+'-comparison.json'));prev=prev.get('current_roster',prev.get('whole_current_roster'));oldby={x['id']:x for x in prev};new={x['id']:x for x in cur}
 complete=bool(cur and len(cur)==max(totals));obj={'source_id':sid,'total':len(cur),'pagination_complete':complete,'reported_totals':totals,'current_roster':cur,'changed':[k for k in oldby.keys()&new.keys() if normal(oldby[k])!=normal(new[k])],'added':list(new.keys()-oldby.keys()),'missing':list(oldby.keys()-new.keys()),'evidence':[a['evidence_file'] for a in ax],'actual_attempts':ax,'comparison':'Complete public object equality, only tag order normalized; all pages and reported totals checked. No clinical verification inferred from equality.'}
 write(RUN/(name+'-comparison.json'),obj);print('PORTAL',name,len(cur),'complete',complete,'changed',obj['changed'],'added',obj['added'],'missing',obj['missing'])
