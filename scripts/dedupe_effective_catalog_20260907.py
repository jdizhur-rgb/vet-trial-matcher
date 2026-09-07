from pathlib import Path
import json
p=Path('data/trial_updates.json')
d=json.loads(p.read_text())
DROP_UPSERT={'umn-sarcoma-trike-rt','upenn-met-osa-car-inkt','utsw-solid-rt-histotripsy','utsw-advanced-tumor-compassionate','ucd-glioma-prism-radiation','osu-oral-melanoma-r3lcmv','uk-oral-melanoma-tigilanol-tiglate','eu-fr-hepatic-tumor-thermoablation','fr-fregis-hepatic-embolization-chemoembolization','nl-utrecht-osa-viral-therapy','eu-ch-feline-oscc-flash-rt','medvet-egfr-her2-vaccine-osa-hsa-tcc','ch-zurich-oral-vinorelbine-phase1','ch-zurich-feline-sts-adam12-vaccine','ch-zurich-canine-highgrade-glioma-chemoradiation','es-ucm-cancimpet-cpmv-mammary','be-ghent-feline-mammary-gcn2in6','uk-liverpool-dog-fight-glioma-ferumoxytol'}
d['upsert']=[x for x in d.get('upsert',[]) if x.get('id') not in DROP_UPSERT]
DELETE_BASE={'umn-trike-sarcoma','penn-osa-carinkt','vroc-rt-histotripsy','vroc-rt-histotripsy-cat','vroc-compassionate-advanced','vroc-compassionate-advanced-cat','auburn-palbociclib','vt-thyroid','vt-brain-pdt','ucd-glioma-autophagy','osu-oral-melanoma','uk-liverpool-dog-fight-glioma','eu-be-feline-mammary-neoadjuvant','eu-fr-hepatic-thermoablation','eu-fr-hepatic-chemoembolization','eu-nl-utrecht-osa-virus','eu-ch-feline-oscc-feather','medvet-egfr-her2-vax','eu-ch-oral-vinorelbine-phase1','eu-ch-feline-sts-adam12-vaccine','eu-ch-high-grade-glioma-chemoradiation','eu-es-cancimpet-mammary-cpmv','uk-edinburgh-oral-melanoma-tigilanol','tufts-osa-cotc034'}
d['delete']=sorted(set(d.get('delete',[]))|DELETE_BASE)
for x in d['upsert']:
    if x.get('id')=='purdue-aks619d-solid-tumors':
        x['available_for_matching']=False
        x['status_confidence']='needs_reconfirmation'
        x['status']='Ongoing proof-of-concept study in client-owned dogs — owner-facing current enrollment route not independently confirmed'
        if 'Kept out of patient matching' not in x.get('notes',''):
            x['notes']=x.get('notes','')+' Kept out of patient matching until Purdue publishes or confirms a current owner enrollment route.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
