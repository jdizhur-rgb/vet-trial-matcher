import ast,copy,datetime,importlib.util,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;Q=ROOT/'research/oncology-care-queue'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert sha==read(RUN/'run.json')['baseline_sha'],'main changed: reconcile before applying'
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build_oncology_center_catalog.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
supp=read(ROOT/'data/oncology_centers_supplemental.json');inv=read(ROOT/'data/oncology_care_source_inventory.json');public=read(ROOT/'data/oncology_centers.json')['centers'];prior_supp=copy.deepcopy(supp['centers']);prior_inv=copy.deepcopy(inv['sources'])
state=read(Q/'state.json');territories=read(Q/'territories.json');assign=read(RUN/'assignments.json');applied=[];amendments=[];summaries=[]
for area,territory in [('ON','Ontario'),('UK','United Kingdom'),('QC','Quebec'),('DE','Germany'),('FR','France'),('NL','Netherlands')]:
 package=read(RUN/area/'result.json');rows=package.get('candidates',package.get('results',package.get('records',package.get('candidate_results',[]))));counts=package.get('counts',package);assert counts['assigned']==counts['processed']==len(rows)==10
 summary={'territory':territory,'assigned':10,'processed':10,'fully_verified':counts['fully_verified'],'new_physical':0};summaries.append(summary)
 for proposal in read(RUN/area/'normalized.json'):
  c=copy.deepcopy(proposal['center']);s=copy.deepcopy(proposal['inventory']);sid=c['source_id'];assert sid==s['id'];assert not any(x['id']==sid for x in inv['sources'])
  assert all(c.get(k) for k in ['name','street','city','region','postal_code','country','phone','website','services','verification_url'])
  assert not any(b.center_match(x,c) for x in public+supp['centers']),('duplicate',sid)
  assert c['latitude'] is None and c['longitude'] is None and c.get('coordinates_unknown')
  # Access facts are displayed; source-scoped pending questions remain internal.
  if area=='FR' and c.get('access_note'):
   if c.get('availability_note')!=c['access_note']:
    c['review_questions']=[c['availability_note']];amendments.append({'source_id':sid,'field':'availability_note','reason':'Use verified appointment/access facts; retain pending question under review_questions.'})
   c['availability_note']=c['access_note']
  elif area=='UK' and c.get('access_note'):
   c['availability_note']=c['access_note'].replace(' Separate physical treatment listing; existing remote service tele-24 unchanged.','')
  if sid=='cancer-vet-montreal-monkland':
   c['availability_note']='In-person oncology consultation at Clinique Vétérinaire Monkland by phone or consultation request form. Local chemotherapy and radiation delivery are not established by this review.'
  c.setdefault('audit_run_id',RUN.name);c.setdefault('review_reference',str((RUN/area/'result.json').relative_to(ROOT)))
  questions=c.get('review_questions') or s.get('review_questions') or []
  if questions:
   c['review_questions']=questions;s['review_questions']=questions;s['review_required']=True;s['recheck_after']='2026-10-21'
  s.setdefault('review_reference',c['review_reference']);s.setdefault('visit_method','Saved actual official source receipts; parent reviewed branch scope and field evidence');s.setdefault('verified_fields',next((x.get('checked_fields',x.get('verified_fields',[])) for x in rows if x.get('source_id')==sid),[]))
  # Do not substitute integration time for successful source visits.
  if s.get('last_checked_at'):datetime.datetime.fromisoformat(s['last_checked_at'].replace('Z','+00:00'))
  supp['centers'].append(c);inv['sources'].append(s);summary['new_physical']+=1
  applied.append({'territory':territory,'source_id':sid,'operation':'NEW','old_value':None,'new_value':c,'source_metadata':s,'parent_evidence_review':'Saved field evidence reviewed; parent direct service-page retrieval separately recorded; no network modality or unsupported credential transferred.'})
 # Every processed item leaves the unprocessed-lead list, including unresolved.
 names={x.get('name','').casefold() for x in rows};urls=set()
 for row in rows:
  for e in row.get('evidence',[]) if isinstance(row.get('evidence'),list) else []:
   if e.get('url') or e.get('official_url'):urls.add(e.get('url') or e.get('official_url'))
 state['unprocessed_leads']=[l for l in state['unprocessed_leads'] if not (l.get('name','').casefold() in names or l.get('url') in urls)]
 for row in rows:
  if not row.get('fully_verified'):
   questions=row.get('pending_questions',row.get('remaining_questions',row.get('unresolved_questions',row.get('questions',row.get('external_gaps',[])))))
   if not questions:
    c=next((x['new_value'] for x in applied if x['source_id']==row.get('source_id')),{});questions=c.get('review_questions') or [row.get('gap') or row.get('uncertainty') or 'See exact source-scoped unresolved question in the saved candidate record.']
   state['pending'].append({'source_id':row.get('source_id'),'name':row.get('name'),'territory':territory,'direction':'Canada/Europe discovery','status':'pending','recheck_after':'2026-10-21','last_substantive_review':row.get('last_substantive_review',row.get('checked_at',row.get('checked_date'))),'questions':questions,'urls':list(dict.fromkeys([e.get('url') or e.get('official_url') for e in row.get('evidence',[]) if isinstance(e,dict) and (e.get('url') or e.get('official_url'))])),'reference':str((RUN/area/'result.json').relative_to(ROOT)),'saved_candidate':row,'successful_verification_date_refreshed':False})
 leads=package.get('unprocessed_leads',package.get('remaining_leads',[]))
 if area=='QC':
  ld=read(RUN/area/'leads.json');leads=ld if isinstance(ld,list) else ld.get('unprocessed_leads',ld.get('leads',[]))
 for lead in leads:
  if isinstance(lead,dict):state['unprocessed_leads'].append({**lead,'territory':lead.get('territory',territory),'status':'unprocessed','last_substantive_review':None,'reference':str((RUN/area/'result.json').relative_to(ROOT))})
 existing=next((t for t in territories['territories'] if t['territory']==territory),None)
 update={'territory':territory,'direction':'Canada/Europe discovery','status':'partial_bounded_search_complete','completed':False,'last_run':RUN.name,'remaining_leads':leads,'result_reference':str((RUN/area/'result.json').relative_to(ROOT)),'remaining':package.get('remaining_territory',package.get('territory_remaining',package.get('next_cursor')))}
 if existing:existing.update(update)
 else:territories['territories'].append(update)
 for a in assign['assignments']:
  if a['territory']==area:a.update(status='research_complete_awaiting_publication',counts=summary)
# Country umbrella cannot retain Ontario's processed leads as unprocessed.
for t in territories['territories']:
 if t['territory']=='Canada':
  t['remaining_leads']=[l for l in state['unprocessed_leads'] if l.get('territory') in ['Ontario','Quebec','Canada']];t['last_run']=RUN.name;t['completed']=False;t['status']='partial_bounded_search_complete'
 if t['territory']=='continental Europe':t.update(status='partial_bounded_search_complete',last_run=RUN.name,completed=False,visited_territories=['Germany','France','Netherlands'])
assert supp['centers'][:len(prior_supp)]==prior_supp and inv['sources'][:len(prior_inv)]==prior_inv
tele=read(RUN/'UK/proposals.json')['teleconsultation_changes'][0];assert tele['old_value'] is None
p=ROOT/'seo/oncology_teleconsultations.py';text=p.read_text();tree=ast.parse(text);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ROWS' for t in n.targets));old_rows=ast.literal_eval(node.value);row=tuple(tele['new_value']);assert not any(x[2]==row[2] or x[8]==row[8] for x in old_rows)
lines=text.splitlines(keepends=True);insert=node.end_lineno-1;assert lines[insert].strip()==']';lines.insert(insert,repr(row)+',\n');text=''.join(lines);text=text.replace('assert len(ROWS) == 60','assert len(ROWS) == 61').replace("for row in ROWS) == 46","for row in ROWS) == 47").replace('46 involving owners in an initial review, 14 veterinarian-only','47 involving owners in an initial review, 13 veterinarian-only');p.write_text(text)
s=next(x for x in read(RUN/'UK/proposals.json')['add_sources'] if x['id']==tele['source_id']);assert not any(x['id']==s['id'] for x in inv['sources']);inv['sources'].append(s)
p=ROOT/'scripts/test_a02_care_reconciliation.py';text=p.read_text().replace('assert len(rows) == 60','assert len(rows) == 61');p.write_text(text)
write(ROOT/'data/oncology_centers_supplemental.json',supp);write(ROOT/'data/oncology_care_source_inventory.json',inv)
state['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();state['active_run']['status']='validated_research_integrated_awaiting_publication'
write(Q/'state.json',state);write(Q/'territories.json',territories);write(Q/'assignments.json',assign);write(RUN/'assignments.json',assign)
write(RUN/'integration.json',{'run_id':RUN.name,'baseline_sha':sha,'packages':summaries,'processed':60,'fully_verified':sum(x['fully_verified'] for x in summaries),'new_physical':len(applied),'new_tele':1,'applied':applied,'tele_change':tele,'parent_amendments':amendments,'old_source_rows_preserved':len(prior_inv),'old_supplemental_rows_preserved':len(prior_supp),'territories_complete':False,'publication_status':'awaiting_checks'})
print('INTEGRATED',len(applied),'physical +1 tele;',sum(x['fully_verified'] for x in summaries),'fully verified; 60 processed')
