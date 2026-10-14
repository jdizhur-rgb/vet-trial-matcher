import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
supp=read(ROOT/'data/oncology_centers_supplemental.json')
inv=read(ROOT/'data/oncology_care_source_inventory.json')
public=read(ROOT/'data/oncology_centers.json')['centers']
applied=[]
summary=[]
state=read(ROOT/'research/oncology-care-queue/state.json')
assign=read(ROOT/'research/oncology-care-queue/assignments.json')
territories=read(ROOT/'research/oncology-care-queue/territories.json')
for area in ['ND','SD','AR','NE','WV','KY']:
    package=read(RUN/area/'result.json')
    proposals=read(RUN/area/'proposed_changes.json')
    changes=proposals if isinstance(proposals,list) else proposals.get('changes',proposals.get('new_centers',[]))
    counts=package.get('counts',package)
    assert counts['assigned_candidates']==counts['processed']==3,(area,counts)
    summary.append({'territory':area,'assigned_candidates':3,'processed':3,'fully_verified':counts['fully_verified'],'core_sufficient_publication_candidates':len(changes)})
    ev=read(RUN/area/'evidence.json')
    rows=ev if isinstance(ev,list) else ev.get('sources',ev.get('official_evidence',ev.get('evidence',ev.get('attempts',[]))))
    for change in changes:
        c=change['new_value'];sid=c['source_id']
        assert change['old_value'] is None
        assert change.get('core_fields_sufficient',True)
        required=['name','street','city','region','postal_code','country','phone','website','services','source','verification_url']
        assert all(c.get(k) for k in required),(sid,'missing required field')
        assert not any(x.get('source_id')==sid for x in supp['centers'])
        domain=urlsplit(c['website']).netloc.removeprefix('www.')
        matches=[x for x in public+supp['centers'] if (x.get('phone')==c['phone'] or (x.get('street','').casefold()==c['street'].casefold() and x.get('city','').casefold()==c['city'].casefold()) or (urlsplit(x.get('website','')).netloc.removeprefix('www.')==domain and x.get('city','').casefold()==c['city'].casefold()))]
        assert not matches,(sid,'semantic duplicate',matches)
        c['audit_run_id']=RUN.name
        c.setdefault('last_verified','2026-10-13')
        c.setdefault('review_reference',str((RUN/area/'result.json').relative_to(ROOT)))
        supp['centers'].append(c)
        urls=set(c.get('supporting_urls',[])+[c['verification_url']])
        evidence=[x for x in rows if (x.get('url') or x.get('official_url')) in urls]
        assert evidence,(sid,'no official evidence')
        exact_times=[x.get('checked_at') or x.get('attempted_at') for x in evidence if 'T' in str(x.get('checked_at') or x.get('attempted_at','')) and x.get('status',200) not in ['ERROR',403,404] and x.get('result')!='unavailable']
        source={'id':sid,'name':c['name'],'source_type':'center','master_url':c['verification_url'],'supporting_urls':c.get('supporting_urls',[]),'required_cadence':'weekly','last_checked':'2026-10-13','last_result':'partial' if c.get('review_status')=='partial' else 'success','content_sufficient':True,'last_run_id':RUN.name,'last_review_note':c['source'],'review_reference':c['review_reference'],'visit_method':'Saved actual official Web/shell source receipts; parent independently reviewed local treatment scope','verified_fields':next((p.get('verified_fields',[]) for p in package.get('candidates',package.get('results',[])) if p.get('source_id')==sid),[])}
        if exact_times:source['last_checked_at']=max(exact_times,key=lambda t:datetime.fromisoformat(t.replace('Z','+00:00')))
        if c.get('review_questions'):
            source.update({'review_questions':c['review_questions'],'review_required':True,'recheck_after':'2026-10-20'})
        assert not any(x['id']==sid for x in inv['sources'])
        inv['sources'].append(source)
        applied.append({'territory':area,'source_id':sid,'services':c['services'],'old_value':None,'new_value':c,'official_evidence_urls':sorted(urls),'parent_scope_review':'PASS; no unsupported chemotherapy/radiation/oncology credential added','source_metadata':source})
    for candidate in package.get('candidates',package.get('results',[])):
        if not candidate.get('fully_verified',candidate.get('strict_fully_verified',False)) or candidate.get('pending_questions') or candidate.get('remaining_questions'):
            state['pending'].append({'source_id':candidate.get('source_id'),'name':candidate.get('name'),'territory':area,'direction':'US discovery','status':'pending','recheck_after':'2026-10-20','reference':str((RUN/area/'result.json').relative_to(ROOT)),'questions':candidate.get('pending_questions') or candidate.get('remaining_questions') or candidate.get('unconfirmed_fields') or candidate.get('questions') or ['See exact source-scoped candidate gap in referenced result'], 'saved_candidate':candidate,'last_substantive_review':candidate.get('checked_at'),'successful_verification_date_refreshed':False})
    leads=package.get('extra_leads',package.get('additional_leads',package.get('unprocessed_leads',package.get('leads',[]))))
    for lead in leads:state['unprocessed_leads'].append({**lead,'territory':area,'status':lead.get('status','unprocessed'),'reference':str((RUN/area/'result.json').relative_to(ROOT)),'last_substantive_review':None})
    for a in assign['assignments']:
        if a['territory']==area:a.update({'status':'research_complete','finished_at':package.get('completed_at') or package.get('finished_at') or package.get('ended_at'),'counts':summary[-1]})
    for t in territories['territories']:
        if t['territory']==area:t.update({'status':'partial_bounded_search_complete','last_run':RUN.name,'completed':False,'remaining':package.get('remaining_territory') or package.get('next_territory_work') or package.get('coverage',{}).get('remaining'),'result_reference':str((RUN/area/'result.json').relative_to(ROOT)),'remaining_leads':leads})
supp['last_verified']='2026-10-13'
write(ROOT/'data/oncology_centers_supplemental.json',supp)
write(ROOT/'data/oncology_care_source_inventory.json',inv)
state['active_run']=None
state['last_completed_research_run']=RUN.name
state['updated_at']=datetime.now(timezone.utc).isoformat()
write(ROOT/'research/oncology-care-queue/state.json',state)
write(ROOT/'research/oncology-care-queue/assignments.json',assign)
write(ROOT/'research/oncology-care-queue/territories.json',territories)
write(RUN/'integration.json',{'run_id':RUN.name,'integration_baseline_sha':'718b11552418ce4c6630e59863907f6072f3b619','packages':summary,'applied':applied,'added_centers':len(applied),'processed':sum(x['processed'] for x in summary),'fully_verified':sum(x['fully_verified'] for x in summary),'territories_exhaustive':False,'parent_review_urls':[a['new_value']['verification_url'] for a in applied],'publication_status':'awaiting_validation'})
print('INTEGRATED',len(applied),'new centers;',sum(x['processed'] for x in summary),'processed;',sum(x['fully_verified'] for x in summary),'strict fully verified')
