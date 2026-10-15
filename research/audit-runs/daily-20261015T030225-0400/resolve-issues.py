import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;p=P/'issues.json';d=json.loads(p.read_text());at=datetime.now(ZoneInfo('America/New_York')).isoformat()
resolved={
 'shared-resource-directory-scope':'All actual VCS/Perseus/DCF published destinations reconciled today including six residual VCS clicks and full current DCF rendered list. These are discovery directories, not purported trial rosters; source-scope duty fulfilled by real linked-lead classification, not by a methodological waiver.',
 'source-question-italy-milan-veterinary-studies':'Fresh native full current study page and actual individual OncoFAP-MMAE primary retrieved/read. One published protocol and current details match existing canonical; prior transport/roster question genuinely resolved.',
 'source-question-australia-pettrials-directory':'Actual current rendered seven-card result set fully read in browser. Two oncology signals individually qualified: existing UQ and Murdoch coming soon/service destination. Empty JS shell no longer an open roster question.',
 'source-question-australia-anzcvs-science-week-oncology':'Current official public news page explicitly empty, full Web-today content read. No actual public trial lead left unqualified. No requirement for private repository or all-Australia recruiting roster.',
 'source-question-global-vettrials-directory':'All three native API pages retrieved200 and total292/current unique IDs exhaust boundary (not yesterday299). All108 candidate signals reconciled to current provider decisions, primary Tufts false oncology lead rejected. Previous missing third page is concretely resolved, distinct shared provider-specific primary questions remain in their own issues.'}
narrow={
 'source-question-registry-avma-veterinary-clinical-trials':'Current full registry roster851 and66 oncology signals established today; exact provider intake/site questions for NCSU historical ethanol, Impellizeri PD1/IL12 and WSU remain. Registry unreadability is no longer a remaining fact.',
 'source-question-usa-georgia-clinical-trials':'Current two oncology research signals read; exact investigational B-cell primary remains denied and detailed drug/criteria unavailable. Do not call complete UGA roster unreadable.',
 'source-question-canada-ovc-active-oncology-trials':'Current dog/cat roster nine identities read today. Due individual HIFU/Palladia protocol rereads failed native/Web; these specific detail-freshness questions remain, not complete OVC-roster absence.',
 'source-question-japan-jsamc-current-clinical-trials':'Current direct master decoded cp932 and five research signals read. Separate combination cohort criteria and feline PD1 details remain unpublished; new HIFU bare-heading question tracked separately.',
 'leah-ohio-current-site':'Ohio is still the sole canonical active site under sponsor invitation; Ohio-specific institutional criteria/corroboration remain a P1 question. Missouri now advertises changed enrolling cohort (new P0 issue), Minnesota current primary remains on hold.'}
for x in d['issues']:
 iid=x['issue_id']
 if iid in resolved:
  x['previous_decision']=x['decision'];x['decision']='resolved_verified';x['resolved_at']=at;x['resolution_evidence']=resolved[iid];x['remaining_fact']=None;x['processing_assessment']='completed_reconciliation';x['next_action']='Daily source visit only; reopen on new conflicting primary signal.';x['recheck_after']=None
 if iid in narrow:
  x['previous_question']=x.get('question');x['question']=narrow[iid];x['remaining_fact']=narrow[iid];x['current_review_evidence']='reviews.json and current receipt-final.json';x['last_reviewed']=at
d['concretely_resolved_this_run']=list(resolved);d['narrowed_this_run']=list(narrow);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('issues',len(d['issues']),'resolved_total',sum(x['decision']=='resolved_verified' for x in d['issues']),'resolved_this_run',len(resolved))
