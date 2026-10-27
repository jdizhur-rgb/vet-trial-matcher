import json,re
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,urljoin
from datetime import datetime
from zoneinfo import ZoneInfo
R=Path(Path('/tmp/current-vet-run').read_text());now=datetime.now(ZoneInfo('America/New_York')).isoformat();c=json.load(open('data/trials_base.json'));by={x['id']:x for x in c};write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def norm(u):
 try:p=urlsplit(u);return (p.hostname or '').replace('www.','')+p.path.rstrip('/')
 except:return u
vt=json.load(open(R/'vettrials-oncology.json'));non={593,161,157,159,158,268,269,522,336,10,192,153,130,555,118,93,584,266,186,182,181,425,678,67,303,302,301,274,187,547,648,646,144}
manual={45:'vt-canine-glioma-ced',424:'tufts-sts-fap-car-t',164:'osu-osa-ai-sbrt',163:'osu-sts-mic-nk',322:'tufts-met-osa-vaccine-tme',661:'tufts-osa-actionable-targets-2026',672:'tufts-primary-pulmonary-carcinoma-sbrt',160:'osu-oral-melanoma',120:'ncsu-feline-oral-pivot-c',115:'ncsu-mammary-inspire',107:'ncsu-liver-inspire',95:'ncsu-canine-sts-xcsgel',418:'vt-thyroid-histotripsy',147:'uf-hsa-vaccine',146:'uf-osa-mrna',145:'uf-osa-vaccine',489:'jhu-cigat-mammary-kubanda-cryo-2026',655:'jhu-cigat-brain-rt-tmz-2026',487:'jhu-cigat-osa-cryo-immunotherapy-2026',654:'cornell-smart-start-bcell-lymphoma',75:'cornell-oscc-trametinib',148:'uf-melanoma',152:'uf-hs-trametinib',600:'tufts-z007-broad-solid-2026',671:'tufts-sabr-pulmonary-metastases-2026',70:'wsu-sts-local-immunotherapy',315:'amc-neobladder',575:'illinois-ucc-gilvetmab-epacadostat',574:'illinois-sts-treatment',573:'illinois-sts-surgery',683:'ill-osa-z007-current',682:'illinois-osa-sbrt-dc-homing-hydrogel',572:'ill-osa-il12-rt-current',571:'illinois-oral-melanoma-il12-il15',681:'illinois-daunomustine-multicentric-lymphoma',65:'leah-bcell-cart-2026',64:'mizzou-pulmonary-carcinoma-gilvetmab',675:'mizzou-feline-highgrade-lymphoma-wart',329:'mizzou-bcell-btk-bi705564',304:'ca-ovc-osa-hifu',299:'ca-ovc-oral-melanoma-palladia',204:'uga-bcell-ivp',190:'umn-orbit-lymphoma',402:'umn-feline-mammary-olaparib-meloxicam',188:'umn-canine-oral-melanoma-aav-vaccine',676:'leah-bcell-cart-2026',632:'umn-canine-brain-tumor-program',608:'csu-osa-carboplatin-pain',436:'csu-osa-car-t-met',355:'csu-sarcoma-engineered-tcells',432:'csu-ucc-lapatinib-rt',647:'csu-osa-3d-limb-spare',565:'csu-aml-trametinib',641:'csu-feline-oscc-immunotherapy',438:'penn-feline-oscc',32:'penn-psma-theranostic-prostate',31:'penn-osa-carinkt',30:'penn-flash-rt-extremity-sts',677:'penn-glioma-flash-gilvetmab-2026',312:'ca-ovc-feline-oscc-porphysome-pdt',276:'auburn-palbociclib-solid-cancers'}
# AMC ID resolved by literal primary URL, never by guessed identifier.
manual.pop(315)
rows=[]
for x in vt:
 id=x['id'];u=x['sourceUrl'];matches=[t['id'] for t in c if norm(t.get('url',''))==norm(u) and u.startswith('http')];mid=manual.get(id)
 if mid:assert mid in by,mid;matches=[mid]
 disposition='EXISTING_PROTOCOL_IDENTITY' if matches else 'PENDING_IDENTITY'
 reason='Recognized existing protocol; no new record or blanket fresh-primary claim from directory metadata.'
 if id in non:disposition='NOT_TREATMENT';reason='Diagnostic, sampling, surveillance, supportive research, non-oncology or equine; not a new dog/cat antitumor protocol.'
 elif id==138:disposition='INVENTORY_ALIAS';reason='UF oncology index, not an individual protocol.'
 elif id==481:disposition='ON_HOLD';reason='Actual source title says recruitment on hold; no reopening.'
 elif id==319:disposition='PENDING_CURRENT_PHASE';reason='BG34 registrySuspended versus undated institutional invitation; no forced closure/reopening.'
 elif id in {411,60,40,39}:disposition='OWNER_SCOPE_EXCLUDED_OR_CONTROL';reason='Preserve scoped owner exclusions and current VT control/amputation intake; no new therapeutic-arm activation.'
 elif id==106:disposition='PAST_PUBLISHED_END';reason='NCSU primary finishSeptember30,2026 remains unchanged; do not reactivate from stale secondarycard.'
 elif id==656:disposition='PENDING_PRIMARY';reason='JHU unnamed HSA investigational-agent protocol remains restricted; current agent/cohort/funding not established.'
 elif id==492:disposition='WATCH_NOT_CONFIRMED_TREATMENT';reason='Lumps-and-bumps cryotherapy/sampling programme does not establish a new matching oncology protocol.'
 elif id==355:reason='Current primary limits engineeredTcells toSTS; oldsecondarytitle does not broaden toOSA.'
 rows.append(dict(directory_id=id,title=x['title'],primary_destination=u,canonical_ids=matches,disposition=disposition,reason=reason))
write(R/'vettrials-lead-dispositions.json',dict(at=now,total=len(rows),rows=rows,remaining_questions=['JHU656 current unnamed agent/cohort','BG34 current phase','Unmatched literal primary destinations require manual identity review; not automatically a new trial.']))
# All 157 search responses were read; classifications do not assert fresh verification of snippets.
ds=json.load(open(R/'discovery-result-index.json'))
not_scope={22,32,33,35,38,46,51,52,54,57,63,64,67,68,72,74,77,78,79,80,82,84,86,87,88,90,92,94,95,96,98,100,102,104,106,107,109,114,115,117,119,120,121,122,126,127,131,134,137,139,140,141,142,143,145,146,148,150,154}
results={62,65,66,69,70,71,73,75,76,81,85,91,93,97,99,103,110,112,113,116,118,144}
reasons={8:'New secondaryTCCdirectory added; fullbody read, existing/closed/supportive protocols separated.',18:'UKVCSR artificialAI sample, not a real enrolling lymphoma trial.',37:'Tokyoorganoidresearch maps existing current primary, not a newprogramme.',56:'UPM/NUS partnership, no published named enrolling ownerprotocol.',61:'OfficialUCDcurrent CARE/PRISM pages read: twoexistingcohorts, not two newrecords.',65:'Publishedpriorlimbsparinghistotripsyresults; currentVTprimary admits control/amputationarm.',71:'OfficialUCDdatedAugust28,2025completedfelineSTAT3trialresults, no freshintake.',76:'ArticleOctober2,2024CalviriSOCH announcement; not a new2026opening.',83:'GenericCancerResearchUKgene-therapyannouncement does not identify a dog/cat patientcohort; no veterinaryrecruitmentclaim.',89:'ActualCalusaUConnASOpostread, onepatientfree not generalfunding; retainedsource140gap.',90:'ActualOctober2026Oncovetnewsread:cliniccases/staff/conference, no recruitment.',99:'Recoveredsame24810article:February18,2026Oregon51dogvaccine/microbiome results; originalnative503/Webinaccessible, alternateindexedarticleisnotcurrentintake.',101:'OfficialUCDbraincenter full current CARE/PRISM identitycheck.',108:'September30antiPD1threecenters alreadycanonical; allthreepreserved.',111:'ExistingJSAMCimmunoprograms; not a newtrialfrom old announcement.',113:'ActualJuly2,2025FiDoAR/testosterone+AImammaryresearchresults/futurelargertrials; Adelaideprimary retainedwatch.',116:'SorafenibresultsSeptember2026 for oldcohortended2021; no reopening.',123:'UQEnzistat programme/news, presentfullcohort termsunpublished, already sourcegap45.',135:'SameSeptember30three-siteantiPD1officialrelease; no duplicate.',153:'Ownsite news index, not independentdiscoveryevidence.'}
for i,x in enumerate(ds):
 x.update(result_index=i,disposition='EXISTING_SOURCE_OR_PROTOCOL',reason='Existing inventory/canonical signal; reconcile against same-run source evidence, not snippet alone.')
 if i in not_scope:x.update(disposition='OUT_OF_SCOPE_OR_NOT_TREATMENT',reason='Human/nononcology/diagnostic/results-methodology/care/jobs/market/conference signal, without a new qualifying owner therapeutic protocol.')
 if i in results:x.update(disposition='RESULTS_OR_HISTORICAL_NEWS',reason='Publication or historical/development news is not proof of present trial enrollment.')
 if i in reasons:x['reason']=reasons[i]
 if i in {18,83}:x['disposition']='NOT_QUALIFIED_VETERINARY_RECRUITMENT'
 if i in {56,89,123}:x['disposition']='RETAINED_PUBLISHED_INFORMATION_GAP'
 if i==8:x['disposition']='NEW_SOURCE_SECONDARY'
write(R/'global-discovery-dispositions.json',dict(at=now,returned_results=len(ds),new_trials_added=0,rows=ds))
regions=['USA','Canada','UnitedKingdom','ContinentalEurope','LatinAmericaCaribbean','AustraliaNewZealand','EastAsia','SouthAsia','SoutheastAsia','MiddleEast','NorthAfrica','SubSaharanAfrica'];matrix=[]
for passname,prefix in [('current_undated','dc'),('recent_overlap7days','df')]:
 for batch in range(1,4):
  d=json.load(open(R/f'{prefix}{batch}.json'))
  for j,q in enumerate(d['payload']['queries']):matrix.append(dict(region=regions[(batch-1)*4+j],discovery_pass=passname,query=q,method='Web',requested_or_saved_at=d.get('saved_at'),response_file=str(R/f'{prefix}{batch}.json'),processing_complete=True,dispositions=str(R/'global-discovery-dispositions.json'),note='Actualquery/results reviewed; scope-limited discovery, not a claim of exhaustive globalabsence.'))
write(R/'discovery-matrix-final.json',dict(regions=12,passes=2,queries=len(matrix),rows=matrix))
print('VetTrials unmatched',[(x['directory_id'],x['title']) for x in rows if x['disposition']=='PENDING_IDENTITY']);print('discovery',len(ds),'matrix',len(matrix))
