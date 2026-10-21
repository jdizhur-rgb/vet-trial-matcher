"""Actual Web evidence is never attributed to shell; cache age remains explicit."""
from daily21 import ROOT,RUN,read,write,m,attempts
from datetime import datetime
from zoneinfo import ZoneInfo
import re,json
rows=[]
for f in sorted(RUN.glob('web-*.json')):
 d=read(f)
 if not isinstance(d,dict) or 'result' not in d or 'urls' not in d:continue
 text='\n'.join(c.get('text','') for c in d['result'].get('content',[]) if c.get('type')=='text');blocks=re.split(r'\n-{20,}\n',text)
 at=datetime.strptime(d['at']['current_time'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('America/New_York')).isoformat()
 for u,b in zip(d['urls'],blocks):
  denial=bool(re.search(r'\(403\)|Forbidden|Access Denied|CAPTCHA',b,re.I));error='Internal Error' in b[:100] or 'not accessible via this tool' in b;ref=re.search(r'【([^】]+)】',b);fresh=re.search(r'Crawled:[^;\n]+',b)
  rows.append({'url':u,'method':'Web','attempted_at':at,'result':'access_denied' if denial else 'retrieval_error' if error else 'retrieved_page','http_status':403 if denial else None,'evidence_file':str(f.relative_to(ROOT)),'reference':ref.group(1) if ref else None,'freshness':fresh.group(0) if fresh else 'not established','text_length':len(b),'retrieved_text':m.redact_text(b)})
write(RUN/'accepted-Web-attempts.json',rows)
write(RUN/'web-denials.json',[{'url':a['url'],'method':'Web','do_not_retry':True,'http_status':403,'observed_at':a['attempted_at'],'origin':a['evidence_file']} for a in rows if a['result']=='access_denied'])
seen={m.route_key(a['url']) for a in rows};denied=m.known_denials();last={m.route_key(a['url']):a for a in attempts()};todo=[]
islands=read(RUN/'public-protocol-islands.json') if (RUN/'public-protocol-islands.json').exists() else [];sufficient_islands={m.route_key(a['url']) for a in islands if len(json.dumps(a['public_protocol']['protocol']))>500}
for k,a in last.items():
 if k in seen or k in denied:continue
 if a.get('http_status')!=200 or a.get('text_length',0)<500:
  # Fully decoded study-level public JSON is not an empty shell. Gallery shells
  # still get their same-URL Web fallback and independent full public pagination.
  if k in sufficient_islands:continue
  todo.append({'source_id':a['source_id'],'url':a['url'],'reason':'native_error_or_insufficient_body','native_evidence':a['evidence_file']})
write(RUN/'Web-recovery-pending.json',todo)
print('Web actual',len(rows),'pending',len(todo))
for a in todo:print(a['source_id'],a['url'])
