import json,sys,pathlib,subprocess,hashlib,re,tempfile,time,zipfile
from urllib.parse import urljoin,urlsplit,urlunsplit
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor
from lxml.html import fromstring
R=pathlib.Path(sys.argv[1]); D=R/(sys.argv[3] if len(sys.argv)>3 else 'evidence'); D.mkdir(exist_ok=True)
def key(x):
 p=urlsplit(x); return urlunsplit(('',p.netloc.lower(),p.path.rstrip('/'),p.query,''))
holds={key(v['url']):v for v in json.load(open('data/source_access_restrictions.json'))['routes'] if v.get('do_not_retry')}
def stamp():return datetime.now().astimezone().isoformat()
def save(u):
 h=hashlib.sha256(u.encode()).hexdigest()[:20]; p=D/(h+'.json')
 if p.exists():return json.loads(p.read_text())
 out=dict(url=u,evidence_key=h,attempts=[],method='curl')
 with tempfile.TemporaryDirectory() as a:
  b=pathlib.Path(a)/'body'; hdr=pathlib.Path(a)/'hdr'
  prev=set(); current=u
  for hop in range(6):
   k=key(current)
   if k in holds:
    out.update(result='exact_route_restricted',restriction=holds[k]);break
   if k in prev:out.update(result='redirect_loop');break
   prev.add(k)
   for retry in range(2):
    b.unlink(missing_ok=True);hdr.unlink(missing_ok=True)
    run=['curl','-sS','--connect-timeout','5','--max-time','20','--max-filesize','15000000','-D',str(hdr),'-o',str(b),'-w','%{http_code}\t%{content_type}',current]
    at=stamp(); z=subprocess.run(run,capture_output=True,text=True); et=stamp(); raw=z.stdout.split('\t',1)
    status=int(raw[0]) if raw and raw[0].isdigit() else 0
    heads=dict((k.lower(),v.strip()) for k,v in re.findall(r'(?m)^([A-Za-z0-9_-]+):([^\r\n]*)',hdr.read_text(errors='replace') if hdr.exists() else ''))
    out['attempts'].append(dict(attempted_at=at,completed_at=et,url=current,http_status=status,exit_code=z.returncode,error=z.stderr[:240]))
    transient=z.returncode==28 or status==429 or status>=500
    if not transient or retry:break
    ra=heads.get('retry-after')
    if ra:
     try:w=max(0,int(ra))
     except ValueError:
      try:w=max(0,(parsedate_to_datetime(ra)-datetime.now(timezone.utc)).total_seconds())
      except (ValueError,TypeError):break
     if w>30:break
     if w:time.sleep(w)
   if status in (301,302,303,307,308) and heads.get('location'):
    target=urljoin(current,heads['location'])
    if urlsplit(target).scheme not in ('http','https'):out.update(result='redirect_unsupported');break
    current=target;continue
   out.update(effective_url=current,http_status=status,result='error' if z.returncode or status!=200 else 'retrieved')
   if out['result']=='retrieved' and b.exists():
    content=b.read_bytes(); out['body_sha256']=hashlib.sha256(content).hexdigest(); text=''; links=[]
    if content.startswith(b'%PDF'):
     text=subprocess.run(['pdftotext','-layout',str(b),'-'],capture_output=True,text=True).stdout
     if D.name=='pdf-ocr' and len(text.strip())<100:
      image_prefix=pathlib.Path(a)/'scan'
      subprocess.run(['pdftoppm','-r','180','-f','1','-l','5','-png',str(b),str(image_prefix)],check=True,timeout=35,capture_output=True)
      text='\n'.join(subprocess.run(['tesseract',str(img),'stdout'],check=True,capture_output=True,text=True,timeout=25).stdout for img in sorted(pathlib.Path(a).glob('scan-*.png')))
      out['extraction']='pdftoppm 180dpi and local Tesseract OCR; check against native text and layout'
    elif content.startswith(b'PK\x03\x04') and current.lower().endswith('.docx'):
     from xml.etree import ElementTree as ET
     with zipfile.ZipFile(b) as zf:
      root=ET.fromstring(zf.read('word/document.xml'))
      text='\n'.join(''.join(p.itertext()) for p in root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))
    elif 'json' in (raw[1] if len(raw)>1 else ''):
     try:text=json.dumps(json.loads(content),ensure_ascii=False,indent=2)
     except Exception: pass
    else:
     try:
      doc=fromstring(content)
      if urlsplit(current).path.startswith('/s/'):
       islands={}
       for code in ('d_study_links','d_avma_study_data','d_avma_studycontent_data','d_sv_content','d_sv_locations_display'):
        raw_data=doc.xpath('//script[@id=$code]/text()',code=code)
        if raw_data:
         try:islands[code]=json.loads(raw_data[0])
         except (ValueError,TypeError):pass
       for code, allowed in [('d_sv_values',('publicId','studypageStatus','studyStartDate','studyEndDate','contactName','contactEmail','spPhoneConditional','iacucNumber','avmaId','studyCode')), ('d_sv_flags',('is_studypage_active','is_active','is_active_nyr','is_finished_rec','join_button_enabled','requires_login'))]:
        raw_data=doc.xpath('//script[@id=$code]/text()',code=code)
        if raw_data:
         try:
          ob=json.loads(raw_data[0]); islands[code]={k:ob[k] for k in allowed if k in ob}
         except (ValueError,TypeError):pass
       if islands and not islands.get('d_sv_flags',{}).get('requires_login'):
        ref=D/(h+'-protocol.json')
        ref.write_text(json.dumps(islands,ensure_ascii=False,indent=2)+'\n')
        out['public_protocol_ref']=str(ref)
      for t in doc.xpath('//script|//style|//noscript|//svg'):t.drop_tree()
      text='\n'.join(s for line in doc.text_content().splitlines() if (s:=' '.join(line.split())))
      links=[[urljoin(current,t.get('href')), ' '.join(t.text_content().split())] for t in doc.xpath('//a[@href]') if t.get('href') and not t.get('href').startswith(('javascript:','#','mailto:','tel:'))]
     except (ValueError,TypeError):pass
    if re.search('verify (?:that )?you are human|captcha|checking your browser',text,re.I) and len(text)<1700:out['result']='access_gate'
    out.update(text_length=len(text),text_sha256=hashlib.sha256(text.encode()).hexdigest(),links=list(dict((u,v) for u,v in links).items()),text_ref=str(D/(h+'.txt')))
    (D/(h+'.txt')).write_text(text)
   break
 p.write_text(json.dumps(out,ensure_ascii=False)+'\n')
 return out
urls=list(dict.fromkeys(u.strip() for u in pathlib.Path(sys.argv[2]).read_text().splitlines() if u.strip()))
with ThreadPoolExecutor(max_workers=6) as pool:
 while urls:
  new=[];wait=[];domains={}
  for u in urls:
   host=(urlsplit(u).hostname or '').removeprefix('www.')
   if len(new)<6 and domains.get(host,0)<2:new.append(u);domains[host]=domains.get(host,0)+1
   else:wait.append(u)
  for u,v in zip(new,pool.map(save,new)):
   print(v.get('evidence_key'),v.get('result'),v.get('http_status'),v.get('text_length'),u,flush=True)
  urls=wait
