import json
from pathlib import Path

p=Path('data/trial_updates.json')
doc=json.loads(p.read_text(encoding='utf-8'))
upserts=doc.setdefault('upsert',[])
by_id={x['id']:x for x in upserts}
new=[
{
'id':'upenn-osa-car-inkt-met','title':'CAR-iNKT cell therapy for canine metastatic osteosarcoma','center':'University of Pennsylvania School of Veterinary Medicine — Comparative Immunotherapy Program','country':'USA','state':'Pennsylvania','species':'Dog','cancers':['Osteosarcoma'],'status':'Recruiting — listed as a current trial by Penn Vet Comparative Immunotherapy Program','url':'https://www.vet.upenn.edu/research/research-programs/comparative-immunotherapy-program/clinical-trials/','contacts':'Nicola Mason, BVetMed, PhD, DACVIM, FRCVS — nmason@vet.upenn.edu; (215) 898-3996','funding':'Confirm study-covered and owner-paid costs with the Penn Vet study team.','requires':{'confirmed':True,'active_treatment_target':True,'lung_metastases':True},'excludes':{},'notes':'Phase I cell-therapy study using donor-derived invariant natural killer T (iNKT) cells engineered with a chimeric antigen receptor (CAR). The study evaluates safety, maximum tolerated dose, persistence, and antitumor activity against canine osteosarcoma metastatic to the lungs. Full protocol eligibility requires Penn prescreening.','verified':'2026-09-05','study_type':'treatment','available_for_matching':True,'status_confidence':'confirmed_current','owner_prescreen_required':True
},
{
'id':'purdue-ucc-aks701d','title':'AKS-701d anti-PD-L1 immunotherapy for canine invasive urothelial carcinoma','center':'Purdue University Veterinary Hospital — Werling Comparative Oncology Research Center / Canine Bladder Cancer Clinic','country':'USA','state':'Indiana','species':'Dog','cancers':['Urothelial / transitional cell carcinoma','Urothelial carcinoma'],'status':'Enrollment ongoing — current 2026 sponsor regulatory filing reports active Purdue enrollment','url':'https://www.sec.gov/Archives/edgar/data/1776612/000110465926041980/tm2516611-24_s1a.htm','contacts':'Purdue Veterinary Hospital / Werling Comparative Oncology Research Center — contact the Canine Bladder Cancer Clinic for current prescreening','funding':'Confirm current study-covered and owner-paid costs with Purdue.','requires':{'confirmed':True,'active_treatment_target':True,'measurable':True,'cystoscopy_accessible':True},'excludes':{'high_urethral_obstruction_risk':True},'notes':'Therapeutic study of AKS-701d, a canine PD-L1 monoclonal antibody, for invasive urothelial carcinoma. A March 2026 regulatory filing states enrollment at Purdue is ongoing and reports treated dogs at 2 mg/kg and 4 mg/kg dose levels. Histopathologic confirmation and measurable cystoscopy-accessible disease are required; full current eligibility and treatment schedule must be confirmed with Purdue.','verified':'2026-09-05','study_type':'treatment','available_for_matching':True,'status_confidence':'confirmed_current','owner_prescreen_required':True
}
]
for x in new:
    by_id[x['id']]=x
# preserve original order, append/replace safely
seen=set(); merged=[]
for x in upserts:
    i=x['id']
    if i in {n['id'] for n in new}:
        if i not in seen: merged.append(by_id[i]); seen.add(i)
    else: merged.append(x); seen.add(i)
for x in new:
    if x['id'] not in seen: merged.append(x)
doc['upsert']=merged
p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Applied',len(new),'AVMA/registry gap records')
