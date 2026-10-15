import urllib.request,concurrent.futures,datetime,json,pathlib,re,html,sys,hashlib
ROOT=pathlib.Path(__file__).parent
TMP=pathlib.Path('/tmp/care-nl');TMP.mkdir(exist_ok=True)
def get(u):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30);raw=r.read().decode('utf-8','replace'); name=hashlib.sha256(u.encode()).hexdigest()[:12];(TMP/(name+'.html')).write_text(raw)
  x=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',raw,flags=re.S|re.I); x=re.sub(r'</(p|div|li|h[1-6]|tr)>','\n',x,flags=re.I);x=html.unescape(re.sub('<[^>]+>',' ',x));x='\n'.join(re.sub(r'\s+',' ',l).strip() for l in x.splitlines() if l.strip());(TMP/(name+'.txt')).write_text(x)
  links=[{'text':html.unescape(re.sub('<[^>]+>',' ',a)).strip(),'url':urllib.parse.urljoin(r.url,l)} for l,a in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',raw,re.S|re.I)]
  o={'url':u,'attempted_at':t,'method':'urllib shell escalated','status':r.status,'working_url':r.url,'sha256_visible_text':hashlib.sha256(x.encode()).hexdigest(),'scratch_file':str(TMP/(name+'.txt'))}
  print(json.dumps({'url':u,'file':o['scratch_file'],'text':x[:22000],'links':[z for z in links if any(w in (z['text']+z['url']).lower() for w in ['oncolog','contact','team','overzicht','sharon','ada','specialist','chemoth','afspraak'])]},ensure_ascii=False))
 except Exception as e:o={'url':u,'attempted_at':t,'method':'urllib shell escalated','error':str(e)};print(json.dumps(o))
 return o
urls=sys.argv[1:]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: rows=list(ex.map(get,urls))
p=ROOT/'attempts.json'; old=json.loads(p.read_text()) if p.exists() else [];p.write_text(json.dumps(old+rows,ensure_ascii=False,indent=2)+'\n')
