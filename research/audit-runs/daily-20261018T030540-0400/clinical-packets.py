"""Prepare actual retrieved protocol passages for manual field-level review."""
from reconcile import *
from run import H
import zipfile,xml.etree.ElementTree as ET
cases={r['trial_id']:r for r in read(ROOT/'data/protocol_selection_cases.json')['reviews']};current={r['id']:r for r in read(ROOT/'data/trials_base.json')};packets=[]
feeds=[]
for name in ['csu','ucd','mars','avma']:
 d=read(P/(name+'-comparison.json'))
 for study in d['current_roster']:feeds.append((name,study,d['evidence'],d['read_at']))
for i in read(P/'trial-evidence-index.json'):
 tid=i['trial_id'];r=current[tid];a=i['native'];body='';origin=[]
 if a and a.get('text_length',0)>500 and a.get('http_status')==200:
  body=read(ep(a['evidence_file']))['text'];origin=[{'url':a['url'],'read_at':a['attempted_at'],'evidence':a['evidence_file'],'method':a['method']}]
  raw=Path(a['raw_file'])
  if raw.exists() and 'html' in a.get('content_type',''):
   rawtext=raw.read_text(errors='replace');m=re.search(r'<main\b[^>]*>(.*?)</main>',rawtext,re.S|re.I)
   if m:
    h=H();h.feed(m.group(1));maintext='\n'.join(x.strip() for x in h.parts if x.strip())
    if len(maintext)>300:body=maintext
  if raw.exists() and raw.read_bytes()[:2]==b'PK':
   try:
    with zipfile.ZipFile(raw) as z:node=ET.fromstring(z.read('word/document.xml'));body='\n'.join(''.join(n.itertext()) for n in node.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))
    (P/'wisconsin-flash-docx-decoded.txt').write_text(body);origin[0]['derived_document_text']=str((P/'wisconsin-flash-docx-decoded.txt').relative_to(ROOT))
   except Exception as ex:body='DOCUMENT DECODE NOT ESTABLISHED '+str(ex)
 if not body or len(body)<800:
  for name,study,evidence,at in feeds:
   if key(study.get('absolute_url',''))==key(i['url']):
    h=H();h.feed(study['description']);desc='\n'.join(x.strip() for x in h.parts if x.strip())
    if len(desc)>len(body):body=study['name']+'\nSTATUS: '+str(study.get('status'))+'\n'+desc+'\nINVESTIGATOR: '+str(study.get('top_investigator'));origin=[{'url':study['absolute_url'],'read_at':at,'evidence':evidence,'method':'current_permitted_public_'+name+'_full_protocol_record','record_id':study['id']}]
 if tid=='jp-jsamc-feline-anti-pd1':body=(P/'jsamc-decoded.txt').read_text()
 if body:
  packets.append({'trial_id':tid,'title':r['title'],'origin':origin,'current_primary_text':body,'prior_independent_criteria':cases.get(tid,{}).get('criteria'),'canonical_review_fields':{k:r.get(k) for k in ['species','cancers','status','intervention','requires','excludes','funding','contacts','contact','sites']}})
write(P/'clinical-packets.json',packets)
print('Manual review packets:',len(packets))
