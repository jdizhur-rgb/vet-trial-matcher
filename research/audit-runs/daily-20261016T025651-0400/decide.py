"""Serialize the explicit source-by-source manual judgments, leaving work visible."""
import json,copy,re,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2];OLD=P.parent/'daily-20261015T030225-0400'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
now=lambda:datetime.now(ZoneInfo('America/New_York')).isoformat()
inv=read(P/'before-source_inventory.json')['sources'];prior={r['source_id']:r for r in read(OLD/'reviews.json')};notes=read(P/'manual-decisions.json');assert set(notes)==set(map(str,range(len(inv))))
native=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()];actual=native+read(P/'web-attempts.json')+read(P/'browser-observations.json')['rows'];comparisons=read(P/'fresh-comparison.json')
resolved={11:5,58:3,109:1}; rows=[]
for i,s in enumerate(inv):
    sid=s['id'];old=prior[sid];urls={s['master_url']}|set(s.get('fallback_urls',[]));attempts=[a for a in actual if a['source_id']==sid or a['url'] in urls]
    r={k:copy.deepcopy(v) for k,v in old.items() if k not in ['completion_decision','reconciliation','current_roster','processing_complete','processing_assessment']}
    r['manual_decision_record']='manual-decisions.json#'+str(i);r['reviewed_at']=now();r['reconciliation']=notes[str(i)]
    r['previous_reconciliation_context']={'run_id':OLD.name,'text':old['reconciliation'],'not_new_visits':True}
    comp=[c for c in comparisons if c['source_id']==sid or c['url'] in urls]
    current_readable=[a for a in attempts if a.get('http_status')==200 and a.get('text_length',0) and a.get('text_length',0)>100 or a.get('method')=='browser_DOM' or a.get('method')=='Web' and a.get('result')=='retrieved_page']
    r['current_comparison_evidence']=comp
    # Completion derives from the individual manual decision plus actual routes,
    # never from a successful HTTP status or inherited outcome alone.
    if i in resolved:
        assert current_readable,(sid,'missing readable current evidence')
        r.update(content_sufficient=True,source_result='fully_reconciled',protocols_seen=resolved[i])
        for k in ['category','question','next_action']:r.pop(k,None)
    if i==104:
        r.update(content_sufficient=False,source_result='partial',protocols_seen=None,category='discovery_source_not_trial_roster',question='Named current oncology protocol/cohort and investigator enrollment, beyond the current general research programme/FAQ.',next_action='Read a new specific current investigator invitation or due October23 signal; retain shared insulinoma issue independently.')
    if i==105:
        r['category']='protocol_uncertainty';r['question']='Current named owner enrollment and qualifying patient benefit/backbone for the early Ambifect solid-tumor cohort; pipeline freshness is now established.'
    if i==33:r['question']='Feline Porphysome full eligibility and owner expense breakdown remain unpublished; the two previously due canine individual protocol rereads are now completed.'
    if i==93:r['question']='Ohio-specific current slot and institutional criteria beyond sponsor invitation; Missouri enrolling and Minnesota hold are now individually reconciled.'
    if i==27:r['question']='Current intake for UTSW Studies1/2/3 after AVMA Completed changes despite current institution/PDF enrolling invitations; separate HSA detailed protocol gap.'
    if i==0:r['question']='Three changed UTSW registry status conflicts and the retained exact NCSU/Impellizeri/WSU provider-intake questions; full registry roster is established.'
    if i==33:r['next_action']='Read a newly published feline Porphysome detailed eligibility/expense protocol, or targeted October21 recheck; canine primary reread gaps resolved today.'
    if i==93:r['next_action']='Read a new Ohio-specific investigator slot/criteria invitation or October21 targeted recheck; do not reopen resolved Missouri/Minnesota questions.'
    if i==27:r['next_action']='Owner disposition on three proposed temporary quarantines pending concordant investigator/registry current intake; read new published intake correction. Separate HSA details recheck October21.'
    if i==0:r['next_action']='Share the three UTSW status conflicts with source27; retain only exact existing provider questions until new primary evidence or October21.'
    if r['content_sufficient']:
        assert attempts and current_readable,(sid,'no current proof')
        r['processing_complete']=True;r['processing_assessment']='completed_reconciliation'
        r['current_roster']=copy.deepcopy(old.get('current_roster'))
        r['current_roster_basis']='Actual current retrieved content explicitly compared in fresh-comparison.json and/or the source-specific manual decision; old roster is not an independent current proof.'
    else:
        r['processing_complete']=True;r['processing_assessment']='external_blocker'
        inherited=old.get('completion_decision',{})
        if r['source_result']=='not_checked':
            assert not attempts,(sid,'gate source unexpectedly attempted')
            r['completion_decision']={'remaining_fact':r.get('question',inherited.get('remaining_fact')),'routes_exhausted_evidence':{'historical_explicit_gate':'inherited-gates.json','source_id':sid,'new_visits':False},'available_reconciliation_done_evidence':notes[str(i)]}
        else:
            assert attempts,(sid,'no actual attempts')
            r['completion_decision']={'remaining_fact':r['question'],'routes_exhausted_evidence':[{'url':a['url'],'method':a['method'],'at':a['attempted_at'],'result':a['result'],'evidence':a.get('evidence_file') or a.get('evidence_reference')} for a in attempts], 'available_reconciliation_done_evidence':{'manual_decision':notes[str(i)],'current_comparisons':comp,'prior_deep_questions_retained_not_redated':inherited.get('remaining_fact'),'deep_recheck_rule':'No repetitive unchanged primary searches before saved due date; current masters/fallbacks actually read.'}}
            if current_readable and old.get('current_roster') is not None:r['current_roster']=copy.deepcopy(old['current_roster']);r['current_roster_basis']='Explicit current-content comparison/manual enumeration, not inherited-date proof.'
    if i==11:r['current_roster']=[{'title':'BI705564 B-cell lymphoma'},{'title':'COTC033'},{'title':'Pulmonary carcinoma gilvetmab'},{'canonical_id':'leah-bcell-cart-2026','status':'enrolling at Missouri; full current primary and today Web agree'},{'title':'Thyroid NIS','classification':'diagnostic'}]
    if i==58:r['current_roster']=[{'canonical_id':'wsu-sts-local-immunotherapy','title':'TCE with mandatory surgery','status':'ongoing; existing shared TCE identity, not new record'},{'title':'Dog Paccal Vet cohort','status':'closed'},{'title':'Cat Paccal Vet cohort','status':'closed'}]
    if i==109:r['current_roster']=[{'title':'FINDIMMUNE canine oral melanoma/OSCC','status':'current individual invitation','funding':'drug and followup funded; screening not asserted free'}]
    if i==0:r['current_roster_change_evidence']='registry-comparison.json: all851unique registry records compared,66retained signals; ids21821/21836/21837 nowCompleted; other retained entries unchanged. Full current API snapshots in evidence.'
    rows.append(r)
write(P/'reviews.json',rows);print('Manual source decisions',len(rows),'sufficient',sum(r['content_sufficient'] for r in rows))
