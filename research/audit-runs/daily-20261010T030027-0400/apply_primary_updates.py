import json
from pathlib import Path
P=Path(__file__).parent
catalog=Path('data/trials_base.json'); rows=json.loads(catalog.read_text()); by={r['id']:r for r in rows}
changes=json.loads((P/'confirmed-changes.json').read_text())
updates=[]
def edit(id, evidence, explanation):
 r=by[id];r['verified']='2026-10-10';r['owner_prescreen_required']=True
 updates.append({'trial_id':id,'evidence':evidence,'change':explanation});return r
r=edit('csu-osa-car-t-met','http/450.json','Replace old estimated cost under $500 with literal current owner-paid diagnostic and examination fees; current direct StudyPages protocol and washouts.')
r['funding']='🟡 Partially funded. Owners pay initial cancer diagnostics and examination fees at every study visit. Study treatment, CAR T-cell manufacture/infusion, study diagnostics and bloodwork are covered; screening assistance is available, with up to $2,000 for study-related side effects.'
r['url']='https://clinicaltrials.csuveterinaryhealth.org/s/car-t-cell-immunotherapy-for-metastatic-osteosarcoma-in-dogs-888207/'
r['notes']='Appendicular OSA primary removed; measurable metastasis limited to lungs; dog ≥20 kg. No chemotherapy in preceding 2–3 weeks; no current steroids or immune-modifying medication. Blood collection about two weeks before treatment, preparatory chemotherapy, CAR T-cell infusion and daily oral medications; visits days 1, 3, 7, 14, 28, 60.'
r['special_requirement']='Study team must confirm lung-only measurable metastases, previous treatment washout of 2–3 weeks, organ function and ability to attend CSU visits.'
r['excludes']['current_steroids']=True;r['excludes']['immunosuppressive']=True
r=edit('csu-feline-oscc-immunotherapy','http/451.json','Clarify covered screening, four intratumoral treatments every three weeks, side-effect cap, diagnostic owner costs and distant-metastasis exclusion.')
r['url']='https://clinicaltrials.csuveterinaryhealth.org/s/novel-immunotherapy-for-cats-with-oral-squamous-cell-carcinoma-126320/'
r['funding']='🟡 Partially funded. Screening support is available for CBC, chemistry, urine testing, lymph-node aspirates and chest radiographs. After acceptance, study examinations, blood tests, anesthesia, four immunotherapy injections, CT and biopsies are covered; up to $1,000 is available for study-related side effects. Owners pay cancer-diagnosis tests and any additional oncologist-recommended tests outside study coverage.'
r['funding_status']='Partially funded';r['excludes']['immunosuppressive']=True
r['special_requirement']='Oral SCC in gums, tongue, lips or jaw; tumor safely accessible for injections; no spread beyond regional lymph nodes; repeated anesthesia and adequate organ function required.'
r['notes']='Four intratumoral immunotherapy injections under anesthesia every three weeks, with CT and biopsies to assess response. Study ends at day 84; all visits at CSU.'
r=edit('csu-osa-3d-limb-spare','http/452.json','Specify distal-radius nonmetastatic disease and funded implant, limb-sparing surgery and six chemotherapy treatments; owner-paid diagnostics and complication cap.')
r['url']='https://studypages.com/s/a-limb-sparing-option-for-bone-cancer-in-dogs-558225/'
r['funding']='🟡 Partially funded. PET-CT/anesthesia, custom 3D-printed implant, surgery/hospitalization, six chemotherapy treatments and study follow-up imaging up to 20 months are covered, with up to $5,825 for surgical complications. Owners pay initial diagnosis/additional recommended tests, care outside CSU and complications beyond coverage.'
r['funding_status']='Partially funded';r['requires']['no_metastasis']=True;r['excludes']['immunosuppressive']=True
r['special_requirement']='Distal-radius OSA suitable for limb-sparing surgery; giant breed OR weight ≥40 kg. Study team must assess this alternative breed/weight criterion and surgical suitability.'
r['notes']='Custom 3D-printed implant replaces affected distal-radius bone, followed by six chemotherapy treatments every three weeks and follow-up every two months up to 20 months. Frequent postoperative bandage changes are required; owner must agree to donate the limb after death.'
r=edit('csu-ucc-lapatinib-rt','http/453.json','Replace unspecified costs with $3,000 radiation support and covered lapatinib/monitoring; explicitly retain owner-paid staging, NSAID and remaining radiation cost.')
r['url']='https://clinicaltrials.csuveterinaryhealth.org/s/combination-of-lapatinib-and-fractionated-radiation-therapy-for-dogs-with-transitional-cell-carcinoma-598674/'
r['funding']='🟡 Partially funded. Lapatinib, recheck examinations, study bloodwork, urinary ultrasounds/sedation and $3,000 toward discounted radiation are covered; some side-effect funding is available. Owners pay initial examination/diagnosis including cystoscopy/biopsy, NSAID medication and radiation costs beyond study support.'
r['funding_status']='Partially funded';r['requires']['planned_radiation']=True
r['special_requirement']='Biopsy-confirmed bladder TCC; safe NSAID use and repeated anesthesia. No radiation in previous six weeks or chemotherapy in previous two weeks; study team confirms washout and the published radiation timetable.'
r['notes']='Daily oral lapatinib plus NSAID and 15 radiation fractions, with monthly follow-up for three months. Source timetable says 15 daily treatments within seven days of starting pills; this inconsistency requires study-team clarification rather than a guessed schedule.'
r=edit('csu-osa-carboplatin-pain','http/454.json','Clarify owner-paid baseline pain medication and side-effect expenses; preserve funded single carboplatin treatment and diagnostics.')
r['url']='https://clinicaltrials.csuveterinaryhealth.org/s/effect-of-intravenous-carboplatin-on-pain-control-in-dogs-with-appendicular-osteosarcoma-571539/'
r['funding']+=' Owners pay standard pain medication for the seven days before enrollment and additional chemotherapy side-effect care beyond the initial study-provided medication.'
r['funding_status']='Partially funded';r['special_requirement']='Weight-bearing appendicular OSA; oral pain medication stable for ≥7 days; no bone medication within 30 days; no previous chemotherapy/radiation or spread to other bones.'
r=edit('csu-aml-trametinib','http/455.json','Replace unspecified costs with covered trametinib/prednisone, study diagnostic monitoring and sample shipping; add circulating-leukemia-cell and washout prescreen.')
r['url']='https://clinicaltrials.csuveterinaryhealth.org/s/pilot-clinical-trial-of-anti-cancer-therapy-with-trametinib-in-naturally-occurring-acute-myeloid-leukemia-860722/'
r['funding']='🟡 Partially funded. Study trametinib and prednisone, study-related diagnostic monitoring and sample shipping are covered. The source does not state that initial leukemia diagnosis or unrelated care is covered; confirm the individual owner estimate with CSU.'
r['funding_status']='Partially funded';r['excludes']['current_chemo']=True
r['special_requirement']='Confirmed AML with circulating leukemia cells, adequate activity/organ function and completion of previous chemotherapy washout; concurrent other anticancer treatment is excluded.'
r=edit('ethos-mimic-osa-lung','http/408.json','Add both hospitals in the entire current sponsor roster; retain subsidized rather than free treatment and primary tumor control requirement.')
r['sites']=[{'hospital':'Veterinary Specialty Hospital – North County','name':'Veterinary Specialty Hospital – North County','city':'San Marcos','state':'CA'},{'hospital':'Gulf Coast Veterinary Specialists','name':'Gulf Coast Veterinary Specialists','city':'Houston','state':'TX'}]
r['special_requirement']='Suspected or confirmed lung metastases from osteosarcoma; primary tumor controlled or controllable by surgery/radiation. The team confirms pulmonary disease and the current owner contribution.'
r=edit('ethos-epush-hsa',['http/407.json','http/106.json'],'Add Akron from its current direct trial listing, preserve all 12 sponsor-listed hospitals, and distinguish $1,000 surgery support from fully funded qualifying HSA treatment.')
r['sites'].append({'hospital':'Metropolitan Veterinary Hospital','name':'Metropolitan Veterinary Hospital','city':'Akron','state':'OH','protocol_source':'https://www.metropolitanvet.com/current-clinical-trials','funding':'Phase 1: $1,000 toward surgery. Qualifying Phase 2: fully funded oncology care.','notes':'Direct current hospital trial listing names PUSH at Akron; coordinating sponsor roster currently omits Akron.'})
r['funding']='🟡 Partially funded overall. Phase 1 provides $1,000 toward splenectomy; owners remain responsible for other initial surgical/screening costs. Dogs subsequently confirmed with splenic HSA and no metastases can enter fully funded Phase 2 (> $10,000 value). Sponsor states up to $3,000 for study-related side effects.'
r['funding_status']='Partially funded';r['special_requirement']='Entry before splenectomy for a ruptured splenic tumor; only qualifying nonmetastatic HSA proceeds to funded treatment. Hospital must confirm its current participation and phase-specific eligibility.'
r['notes']+=' Current sponsor lists 12 participating hospitals; Akron is additionally listed on its own official current clinical-trials page. This roster discrepancy is preserved for confirmation, not silently dropped.'
(P/'primary-update-decisions.json').write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n');catalog.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Confirmed additional updates',len(updates))
