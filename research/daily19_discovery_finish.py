"""Explicit adjudication of the 93 newly returned URL variants/signals."""
from daily19 import ROOT,RUN,OLD,read,write,now
import collections,json
d=read(RUN/'discovery-ledger.json');a=[r for r in d['leads'] if r['disposition']=='signal_needs_adjudication'];assert len(a)==93
groups=[
([0,8,16,19,22,23,34,36,38,43,74],'excluded_training_or_jobs','Education, conference/CE, employment or clinical-research administration; not an owner anticancer treatment invitation.'),
([1,5,6,9,10,11,12,18,40,42,68,69,70,71,72,73,75,76,77,78],'excluded_human_research','Human oncology registry, medical centre or human-patient clinical study; not dog/cat treatment.'),
([3,21,29,91],'publication_not_current_invitation','Survey, descriptive cohort, review or historical paper, not a current owner treatment protocol.'),
([14,17,32,33,41,44,45,47,48,49,51,52,53,55,56,88,89,90,92],'excluded_care_or_unrelated','Care/services, general animal content, taxation, product brand or non-oncology case. Outside daily treatment-trial discovery.'),
([2,26,27,35,37,46,54],'research_or_diagnostic_signal_not_trial','Prospectus, historical centre/programme news, funding announcement, general research or diagnostic invitation. No named new therapeutic intake established; not rejected as proof that a centre has no trials.'),
([4,59],'duplicate_existing_sponsor_signal','Gamgee/Rosie financing or company story is not a new separate owner protocol; existing official Gamgee source retains its exact access question.'),
([13,15,20,24,25,31,39,50,57,58,62,64,65,83],'known_source_or_protocol_signal','Named programme already represented in full canonical/source inventory. Fresh source traversal and independent public portal comparisons govern status, not this search snippet. See source receipt and trial review; inaccessible primary routes remain inaccessible.'),
([28],'excluded_observational_biobank','RVC Oncobiome bank is sample/biobank research, not an anticancer treatment trial.'),
([60],'excluded_trial_finder_service','A trial-finder service is not a treatment protocol or an independent official trial source.'),
([61],'duplicate_wsu_local_immunotherapy','WSU/CASTR solid-tumour local-immunotherapy signal matches existing wsu-sts-local-immunotherapy family. Institution primary is restricted; preserve unresolved scope rather than activate a new LinkedIn-derived row.'),
([63],'general_clinical_research_explainer','Toronto AHP post explains oncology trials in general, without a named new intervention/cohort.'),
([66,80,81,82,84,86,87],'vgs002_identity_and_closure','Vetigenics VGS-002 historical promotion/identity versus current entire sponsor closure roster and exact AVMA Completed object. One existing record hidden, no new trial. See vgs002-completed-amendment.json.'),
([67],'preclinical_future_pipeline','Benno explicitly expects first patient early2027. Ethical approval/financing is not current owner enrollment.'),
([79],'vgs002_current_site_conflict','Full fresh VSH primary still says OPEN and lists CASE Boulder, Metropolitan Cleveland East and VSH North County. Current sponsor marks the entire Ethos and BARC programme Closed, exact AVMA record Completed. Conflict retained, conservative nonmatchable completion; no site activation.'),
([85],'secondary_tcc_signal_reconciled','Full secondary directory read: enitociclib is completed on Purdue primary, anti-PD1 is VGS-002 closed, NIH972/B7H3 and NCSU/OSU/UMN/Wisconsin/AMC entries are existing protocol families. Registry/current institutional evidence controls; not a new institutional source, no activation from this stale directory.')]
for indices,status,reason in groups:
 for i in indices:
  assert a[i]['disposition']=='signal_needs_adjudication',i
  a[i].update(disposition=status,reason=reason,manual_adjudicated_at=now())
for i,status,reason,ev in [
 (7,'excluded_diagnostic_planning_studies','Full current official page has two canine research projects: nasal CBCT radiation planning (study covers CT/planning) and oral-melanoma PET-CT staging (covers PET/MRI/immobilization plus$500). Neither tests an anticancer intervention; ordinary RT eligibility does not turn staging/planning research into a treatment trial.','759ef4ae44a4fc83bd'),
 (30,'rejected_completed_legacy_cohort','Full current owner page still solicits feline solid-tumour Paccal Vet, three hospitals and4dosesq3weeks. Sponsor September17 results/recruitment completion and CAStr/Bridge closure evidence remain controlling after today full unchanged sponsor-master comparison. No newly named cohort; preserve conflict, do not reactivate.','bf524800f439b5864c')]:
 a[i].update(disposition=status,reason=reason,primary_evidence=str((RUN/'evidence'/(ev+'.json')).relative_to(ROOT)),manual_adjudicated_at=now())
assert not any(r['disposition']=='signal_needs_adjudication' for r in a)
# Specific current primary reads of signals that matched yesterday's URL.
for r in d['leads']:
 if 'marsvets.com.au/services/oncology-services/immunotherapy' in r['url']:
  r.update(disposition='treatment_access_watch_not_verified',reason='Whole current official MARS APAVAC page read today (web-05-leads.json). Commercial autologous vaccine requires biopsy/excision;4weekly+4monthly schedule. Price and adequate protocol-level medical evidence not established. Not a trial; no catalog addition or promise.',current_primary_evidence=str((RUN/'web-05-leads.json').relative_to(ROOT)))
 if 'vetmed.illinois.edu/wp-content/uploads/2026/01/RT-Gilvetmab' in r['url']:
  r.update(disposition='unresolved_current_protocol',reason='January2026 oligometastatic RT/gilvetmab PDF remains a named lead, not confirmed current intake by today unchanged eight-protocol master; prior qualification and current source receipts retained. No activation or false global absence claim.')
d['summary'].update(reviewed_at=now(),dispositions=dict(collections.Counter(r['disposition'] for r in d['leads'])),new_signal_rows_manually_adjudicated=93,unadjudicated_signal_rows=0,executor_unfinished_discovery_qualification_actions=0,confirmed_new_protocols=0,new_official_sources=1,regions_with_both_passes=12,actual_queries=85)
write(RUN/'discovery-ledger.json',d);print(json.dumps(d['summary'],ensure_ascii=False))
