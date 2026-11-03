import json,pathlib
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=pathlib.Path('/workspace/scratch/55af69f9810e/audit-20261103');R=ROOT/'research/audit-runs/daily-20261103T030532-0500'
c=json.loads((R/'baseline-trials_base.json').read_text());a=json.loads((R/'vettrials-current-oncology.json').read_text())
m={164:'osu-osa-ai-sbrt',157:'osu-mct-ai-node',671:'tufts-sabr-pulmonary-metastases-2026',593:'osu-feline-margin-oct',600:'tufts-z007-broad-solid-2026',424:'tufts-sts-fap-car-t',163:'osu-sts-mic-nk',159:'osu-sts-microscopic-extension',158:'osu-sts-immune-infiltrate',322:'tufts-met-osa-vaccine-tme',661:'tufts-osa-actionable-targets-2026',672:'tufts-primary-pulmonary-carcinoma-sbrt',160:'osu-oral-melanoma',319:'tufts-bg34-melanoma',16:'ut-fluorocoxib-bladder',654:'cornell-smart-start-bcell-lymphoma',75:'cornell-oscc-trametinib',148:'uf-melanoma',266:'isu-lymphoma-cerumen',147:'uf-hsa-vaccine',146:'uf-osa-mrna',145:'uf-osa-vaccine',489:'jhu-cigat-mammary-kubanda-cryo-2026',655:'jhu-cigat-brain-rt-tmz-2026',487:'jhu-cigat-osa-cryo-immunotherapy-2026',182:'umn-coed-osa-part2',181:'umn-coed-osa-part1',431:'tufts-hsa-liquid',161:'osu-hepatic-adrenal-thromboembolism',70:'wsu-sts-local-immunotherapy',67:'mizzou-thyroid-nis',65:'leah-bcell-cart-2026',64:'mizzou-pulmonary-carcinoma-gilvetmab',675:'mizzou-feline-highgrade-lymphoma-wart',60:'csu-cotc033-vaccine-immunity',329:'mizzou-bcell-btk-bi705564',312:'ca-ovc-feline-oscc-porphysome-pdt',608:'csu-osa-carboplatin-pain',436:'csu-osa-car-t-met',434:'csu-osa-dual-energy-ct',355:'csu-sarcoma-engineered-tcells',432:'csu-ucc-lapatinib-rt',648:'csu-agasaca-node-map',647:'csu-osa-3d-limb-spare',565:'csu-aml-trametinib',641:'csu-feline-oscc-immunotherapy',276:'auburn-palbociclib-solid-cancers',274:'oregon-lymphoma-microbiome',190:'umn-orbit-lymphoma',402:'umn-feline-mammary-olaparib-meloxicam',188:'umn-canine-oral-melanoma-aav-vaccine',187:'umn-lyra3',676:'leah-bcell-cart-2026',632:'umn-canine-brain-tumor-program',584:'ut-thyroid-function-carcinoma'}
nontherapy={130,555,157,593,159,158,269,10,192,16,153,492,118,93,266,186,182,181,411,268,161,67,302,301,434,648,646,274,187,303,584,522}
closed={481,153,492,656,192,10,16,186,182,181,522}
rows=[]
for x in a:
 u=x.get('sourceUrl');ids=[t['id'] for t in c if u and str(t.get('url','')).split('?')[0].rstrip('/')==u.split('?')[0].rstrip('/')]
 if x['id'] in m:ids=[m[x['id']]]
 assert all(t in {k['id'] for k in c} for t in ids)
 if x['id']==138:disp='SOURCE_INDEX_REVIEWED';reason='UF oncology index route; current official oncology master and6 therapeutic protocol links examined separately. Not a duplicate trial.'
 elif x['id'] in nontherapy:disp='NOT_TREATMENT';reason='Equine species, diagnostic/sample/supportive or observational study; no qualifying dog/cat anticancer-treatment access established by this listing.'
 elif ids:disp='EXACT_EXISTING_IDENTITY';reason='Individual directory title, intervention/disease/cohort and source-specific URL compared with exact canonical identity. Secondary status does not reset current clinical evidence or override primary conflicts.'
 elif x['id'] in closed:disp='HISTORICAL_SECONDARY_ONLY';reason='Directory labels completed/suspended. No current treatment enrollment claim and no primary-confirmed canonical closure from directory alone.'
 else:disp='PENDING_EVIDENCE';reason='No exact canonical identity established; directory-only signal needs current individual primary before adding or merging.'
 rows.append({'directory_record_id':x['id'],'title':x['title'],'source_url':u,'directory_status':x['enrollmentStatus'],'canonical_ids':ids,'disposition':disp,'finding':reason})
(R/'vettrials-oncology-reconciliation.json').write_text(json.dumps({'reviewed_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'all_pages_total':292,'oncology_rows_total':104,'rows':rows},ensure_ascii=False,indent=2)+'\n')
print('Directory104 decisions',len(rows),'unmatched potential',[(x['directory_record_id'],x['title']) for x in rows if x['disposition']=='PENDING_EVIDENCE'])
