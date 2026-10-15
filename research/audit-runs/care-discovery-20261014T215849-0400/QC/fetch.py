import urllib.request,json,sys,datetime,hashlib,re
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='a':self.links += [v for k,v in a if k=='href']
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(d.strip())
rows=[];out=Path('/tmp/care-qc');root=Path('research/audit-runs/care-discovery-20261014T215849-0400/QC');old=root/'attempts.json'
if old.exists():rows=json.loads(old.read_text())
for u in sys.argv[1:]:
 ts=datetime.datetime.now(datetime.timezone.utc).isoformat();r={'url':u,'attempted_at':ts,'method':'shell urllib public GET'}
 key=re.sub('[^a-zA-Z0-9]+','_',u)[:190]
 try:
  res=urllib.request.urlopen(u,timeout=30);html=res.read().decode('utf-8','replace');p=P();p.feed(html);s='\n'.join(p.text)
  r.update(status=res.status,working_url=res.url,text_sha256=hashlib.sha256(s.encode()).hexdigest(),scratch_key=key)
  (out/(key+'.txt')).write_text(s);(out/(key+'.links.json')).write_text(json.dumps(p.links,ensure_ascii=False))
  print(u,res.status,len(s),key)
 except Exception as e:r['error']=str(e);print(u,str(e))
 rows.append(r)
old.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
