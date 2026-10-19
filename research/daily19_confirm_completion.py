from daily19 import ROOT,RUN,read,write,now
import copy
cat=read(ROOT/'data/trials_base.json');r=next(r for r in cat if r['id']=='penn-anti-pd1-urothelial-carcinoma');old=copy.deepcopy(r)
a=read(RUN/'avma-comparison.json');v=next(v for v in a['current_roster'] if v['id']==15973)
assert v['status']=='Completed' and v['top_investigator']=='Samuel Stewart' and v['vct_code']=='VCT23005729'
r.update(status_confidence='confirmed_completed',status='Completed — exact AVMA VCT23005729; sponsor VGS-002 Ethos/BARC enrollment closed',status_source=v['absolute_url'],status_verified_at=max(a['read_at']),status_decision_at=now())
r['status_decision_note']+=' Exact current full AVMA record15973/VCT23005729 independently matches Samuel Stewart, fully canine anti-PD1, urothelial carcinoma, funding and full study description, and is Completed. Standing owner instruction to accept exact AVMA Completed also applies. This resolves the earlier intake-only qualification without treating a different PD-L1/combination protocol as the same study.'
write(ROOT/'data/trials_base.json',cat)
write(RUN/'vgs002-completed-amendment.json',{'record_id':r['id'],'at':now(),'earlier_decision':'vgs002-closure.json','before':old,'after':r,'exact_registry_record':v,'current_registry_evidence':a['evidence'],'actual_read_at':a['read_at'],'original_clinical_verified_date_retained':r['verified'],'standing_owner_rule':'Exact AVMA Completed is completed; sponsor status independently agrees.'})
print('Exact AVMA15973/VCT23005729 Completed corroborated; canonical now confirmed_completed.')
