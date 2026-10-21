"""Whole multicentre/source provenance, without invented clinical sign-off."""
from daily21 import ROOT,RUN,read,write,now,m,attempts
from collections import Counter
aa=attempts()+read(RUN/'accepted-Web-attempts.json')
def ev(fragment):return [{k:a.get(k) for k in ['url','attempted_at','completed_at','method','http_status','result','evidence_file','freshness']} for a in aa if fragment in a['url']]
cat=read(ROOT/'data/trials_base.json');r=next(x for x in cat if x['id']=='medvet-egfr-her2-vaccine-2026')
rows=[]
for s in r['sites']+r['inactive_sites']:
 h=s['hospital'];paused=s in r['inactive_sites'];sponsor=h!='University of Missouri Veterinary Health Center'
 rows.append(dict(canonical_site=s,sponsor_approved=sponsor,cca_current_status='CURRENTLY NOT ENROLLING' if paused else 'Listed without non-enrolling warning',provider_status='Not independently freshly established on a local protocol today',decision='Retain exact prior site state; do not reactivate a paused site from sponsor approval.'))
 for_match={'MedVet Salt Lake City':'Enrolling','MedVet Cleveland':'Established patients only','MedVet Cincinnati':'Established patients only','MedVet Pittsburgh':'Pennsylvania residents only','MedVet Chicago':'Pause'}
 if h in for_match:rows[-1]['provider_status']='Fresh MedVet clinical-studies master: '+for_match[h]
 if h=='Veterinary Cancer Concierge Services':rows[-1].update(sponsor_address='46 Maltbie Ave., Stamford CT06902',current_canonical_address=s['address'],remaining_question='Provider current1086LongRidge address vs sponsor approved46Maltbie; do not overwrite from sponsor list alone.')
rows.append(dict(hospital='MedVet Northern Virginia',city='Manassas',state='VA',sponsor_approved=True,sponsor_address='8614 Centreville Rd., Manassas VA20110',cca_current_status='Not in current whole12-site status table',provider_status='Not in current MedVet vaccine cohort list; old2023 Hope news404 in native and Web',canonical_added=False,decision='PENDING_SITE_INTAKE; approved is not enrolling; preserve one shared question instead of duplicate trial.'))
write(RUN/'therajan-multicenter-reconciliation.json',dict(run_id=RUN.name,at=now(),canonical_id=r['id'],sponsor_approved_total=12,cca_current_table_total=12,canonical_active_sites=9,canonical_paused_sites=3,union_sites=len(rows),whole_roster_rows=rows,evidence=ev('find-a-clinic.html')+ev('/yale-status')+ev('/clinical-studies/')+ev('hopevetspecialty.services'),canonical_changes=False,clinical_dates_refreshed=False))
managed=[a for a in aa if '140763' in a['url']]
write(RUN/'managed-multicenter-reconciliation.json',dict(run_id=RUN.name,at=now(),protocol='HIFU for canine nodal lymphoma',canonical_candidates=[r['id'] for r in cat if '140763' in r.get('url','')],actual_attempts=[{k:a.get(k) for k in ['url','attempted_at','method','http_status','evidence_file']} for a in managed],current_whole_published_roster=[dict(hospital='VCA Dallas Animal Specialty',address='17727 Dallas Parkway Suite150, Dallas TX75287',investigators=['Zachary Wright','Rachel Kovac'])],decision='Entire public study-content and locations API responses actually retrieved. Same nodal B/T lymphoma study/site, HIFU plus doxorubicin day8 then five doses. No new separate cohort or fresh full medical review inferred from a site read.'))
write(RUN/'transport-summary.json',dict(at=now(),native_requests=len(attempts()),native_status_counts=dict(Counter(str(x.get('http_status')) for x in attempts())),native_transient_retries=sum(a.get('retry',0)>0 for a in attempts()),native_unique_urls=len({m.route_key(a['url']) for a in attempts()}),web_requests=sum(a.get('method')=='Web' for a in aa),new_native_denials=read(RUN/'new-denials.jsonl') if False else [__import__('json').loads(x) for x in (RUN/'new-denials.jsonl').read_text().splitlines()],same_url_recovery_pending=read(RUN/'Web-recovery-pending.json'),source_requests_not_source_completion=True))
# A compact API comparison refers to the entire preserved current/previous objects,
# rather than embedding a multi-megabyte one-line JSON diff a second time.
c=read(RUN/'full-comparisons.json')
for x in c:
 if '/api/' in x['url'] or '/json/' in x['url']:
  if len(x.get('diff') or '')>50000:x['diff']='Whole structured objects compared in the corresponding avma/csu/ucd/mars/vettrials-comparison.json; raw current/previous evidence references and equality flags retained here.'
write(RUN/'full-comparisons.json',c)
print('WHOLE13 sites, managed location API and actual transport summary saved')
