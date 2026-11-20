import json
from pathlib import Path
now='2026-11-20T04:31:00-05:00'
trial={
  'id':'penn-flash-metastatic-osa-gilvetmab-2026',
  'title':'Proton FLASH radiation plus gilvetmab for canine metastatic osteosarcoma',
  'center':'Penn Vet Ryan Veterinary Hospital','country':'USA','state':'Pennsylvania','species':'Dog',
  'cancers':['Osteosarcoma'],'status':'Recruiting — posted November 17, 2026',
  'url':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/',
  'source_url':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/',
  'contacts':'Penn Vet VCIC — 215-573-0302; vcic@vet.upenn.edu',
  'funding':'🟡 Partially funded. After enrollment, the study covers protocol examinations, imaging and laboratory tests through the 48-week follow-up, one FLASH-RT treatment, three gilvetmab infusions, up to $500 for complications directly related to the study, and autopsy. Owners pay initial eligibility diagnostics and the amputation of the primary limb tumor.',
  'funding_status':'Partially funded','funding_source':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/','funding_verified':'2026-11-20',
  'requires':{'confirmed':True,'metastatic':True,'lung_metastases':True,'prior_amputation':True,'active_treatment_target':True,'planned_radiation':True,'measurable':True},
  'excludes':{'bone_metastasis':True,'prior_gilvetmab':True,'anesthesia_contraindicated':True,'recent_systemic_chemotherapy_or_immunotherapy':True},
  'notes':'Dogs need confirmed appendicular osteosarcoma after standard-of-care amputation and at least one pulmonary metastasis visible on chest radiographs that is larger than 1 cm; the largest target lung lesion must be smaller than 5 cm. Dogs must be suitable for general anesthesia and clinically stable. Systemic chemotherapy or immunotherapy requires a three-week washout; previous gilvetmab and bone metastasis are excluded. Treatment is one FLASH proton-radiation dose to a lung lesion plus three intravenous gilvetmab infusions, with follow-up through 48 weeks.',
  'intervention':'One FLASH proton-radiation dose to a pulmonary metastasis plus three intravenous gilvetmab infusions',
  'why':'The study evaluates the safety and antitumor activity of FLASH proton radiation combined with anti-PD-1 immunotherapy for pulmonary metastases from appendicular osteosarcoma.',
  'verified':'2026-11-20','protocol_reviewed_at':now,'study_type':'treatment','available_for_matching':True,
  'status_confidence':'confirmed_current','owner_prescreen_required':True,
  'sites':[{'hospital':'Penn Vet Ryan Veterinary Hospital','name':'Penn Vet Ryan Veterinary Hospital','city':'Philadelphia','state':'PA','country':'USA','address':'3900 Spruce Street, Philadelphia, PA 19104','source_url':'https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/'}],
  'location_source':'official Penn Vet protocol page','treatment_approaches':['radiation','immunotherapy'],'address':'3900 Spruce Street, Philadelphia, PA 19104',
  'special_requirement':'Confirmed appendicular osteosarcoma after amputation with a measurable pulmonary metastasis over 1 cm and under 5 cm; no bone metastasis, previous gilvetmab, or systemic chemotherapy/immunotherapy within three weeks; must tolerate anesthesia and attend follow-up at Penn Vet for up to 48 weeks.'
}
p=Path('data/trials_base.json'); trials=json.loads(p.read_text())
if any(t.get('id')==trial['id'] for t in trials): raise SystemExit('trial id already exists')
url=trial['url'].rstrip('/').lower()
if any(str(t.get('url','')).rstrip('/').lower()==url for t in trials): raise SystemExit('trial URL already exists')
trials.append(trial); p.write_text(json.dumps(trials,ensure_ascii=False,indent=2)+'\n')
sp=Path('data/source_inventory.json'); inv=json.loads(sp.read_text()); src=next(s for s in inv['sources'] if s['id']=='usa-penn-vet-clinical-trials')
urls=src.setdefault('fallback_urls',[])
if trial['url'] not in urls: urls.append(trial['url'])
src['notes']='Exact Penn index routes remain held. A separate unheld protocol page posted November 17, 2026 was read through current web discovery on November 20 and confirms recruiting proton FLASH-RT plus gilvetmab for pulmonary metastases from amputated appendicular osteosarcoma; canonical record penn-flash-metastatic-osa-gilvetmab-2026.'
sp.write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'trial_added':trial['id'],'catalog_count':len(trials),'source_route_added':trial['url']},ensure_ascii=False))
