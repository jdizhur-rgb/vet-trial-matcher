import json,re
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent
class T(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None
 def handle_starttag(self,t,a):
  if t=='tr':self.row=[]
  if t in ('td','th'):self.cell=[]
 def handle_data(self,d):
  if self.cell is not None:self.cell.append(d)
 def handle_endtag(self,t):
  if t in ('td','th') and self.cell is not None:
   if self.row is not None:self.row.append(re.sub(r'\s+',' ',' '.join(self.cell)).strip())
   self.cell=None
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
a=[json.loads(x) for x in (P/'attempts.jsonl').read_text().splitlines()]
old=json.loads((P.parent/'daily-20261014T030650-0400/europe-current-reconciliation.json').read_text())
result={}
for sid in ['europe-esvonc-ongoing-trials','europe-oncowaf-clinical-trials']:
 x=[x for x in a if x['source_id']==sid and x['route']=='master' and x['http_status']==200][-1]
 h=T();h.feed(Path(x['raw_file']).read_text());result[sid]={'evidence_file':x['evidence_file'],'attempted_at':x['attempted_at'],'table_rows':h.rows}
 if sid=='europe-esvonc-ongoing-trials':
  dif=[]
  for r in old['esvonc']:
   i=r['source_table_row'];cells=h.rows[i]
   if cells!=r['cells']:dif.append({'row':i,'old':r['cells'],'current':cells})
  result[sid]['current_classification_comparison']={'previous_classified_rows':len(old['esvonc']),'differences':dif,'rule':'Previous classification can be retained only for explicitly equal current table cells; no fresh provider confirmation implied.'}
  assert not dif,dif
result['insulinoma_all_seven_sites_compared']=['RVC London','Liverpool','Edinburgh','North Downs Bletchingley','Southfields Essex','Dick White Cambridgeshire','Nieuwegein Netherlands']
result['italian_melanoma_both_sites_compared']=['I Portoni Rossi Bologna','University of Teramo']
result['clinical_disposition']='Same aggregate signals; retain four owner-quarantined records, six pending current-access questions, and site/phase-specific limitations. No current clinical access inferred from aggregation.'
(P/'europe-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Current ESVONC:',len(old['esvonc']),'exact unchanged classified rows; Oncowaf table rows',len(result['europe-oncowaf-clinical-trials']['table_rows']))
