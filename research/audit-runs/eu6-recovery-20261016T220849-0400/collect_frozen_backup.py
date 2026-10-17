"""Collect only frozen research checkpoints, never mutable worker snapshots."""
import json,pathlib,hashlib,datetime,re
ROOT=pathlib.Path(__file__).resolve().parents[3]
RUN=pathlib.Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def collect():
    a=json.loads((RUN/"assignments.json").read_text())
    lp=RUN/"backups/ledger.json"
    uploaded=json.loads(lp.read_text()).get("uploaded_files",{}) if lp.exists() else {}
    files={};blocks=[];reports={};errors=[];quarantined=[]
    for item in a["assignments"]:
        w=ROOT/item["worker_directory"]
        ready_paths = [q for q in w.rglob("*.json") if q.relative_to(w).parts[0] != "input" and re.search(r'(?:^|-)ready(?:-[^.]+)?\.json$',q.name)]
        for ready in sorted(ready_paths):
            superseded={(4,'checkpoints/block-02/ready.json'):'Worker declared erroneous draft; superseded by block-02delta/ready.json.',(4,'checkpoints/block-02delta/ready.json'):'Mutable root references corrected by block-02delta-seal; original bytes restored from verified archive003.',(4,'checkpoints/block-03/ready.json'):'Mutable root references corrected by block-03-seal; payload unchanged.',(3,'checkpoints/block-3/ready.json'):'Header omitted baseline_sha; superseded by block-3-corrected-ready.json. Payload preserved as history.'}
            historical_run = RUN.name == 'eu6-20261016T142911-0400'
            reason=superseded.get((item['slot'],ready.relative_to(w).as_posix())) if historical_run else None
            if historical_run and item['slot']==5 and ready.relative_to(w).as_posix()=='checkpoints/restriction-08-01/ready.json':
                reason='Metadata-only cancellation notice missing baseline_sha header; superseded by ready-v002.json, same two safe members'
            if historical_run and item['slot']==2 and ready.relative_to(w).as_posix().startswith('checkpoints/block-08') and not ready.relative_to(w).as_posix().startswith('checkpoints/block-08-public-safe-v3/'):
                reason='Original or intermediate UNSAFE KVL-derived block08: LOCAL QUARANTINE; only public-safe-v3 is permitted'
            if historical_run and item['slot']==2 and ready.relative_to(w).as_posix() in {'checkpoints/block-08/ready.json','checkpoints/restriction-07/ready.json'}:
                reason='PRIVATE-USE KVL database extraction/withdrawn row in payload: LOCAL QUARANTINE, not permitted in public backup; await worker public-safe derivative with independent evidence'
            if historical_run and item['slot']==6 and ready.relative_to(w).as_posix() in {'source-events/restriction-007-ready.json','source-events/restriction-008-ready.json'}:
                reason='Missing baseline_sha header; superseded by corresponding ready-v002.json with unchanged evidence'
            if RUN.name=='eu6-recovery-20261016T220849-0400' and item['slot']==5 and ready.relative_to(w).as_posix()=='checkpoints/block-17/ready.json':
                reason='Full third-party raw CGF PDF and unnecessary source-body asset are local-only. Use immutable block-17-safe derivative with same research facts, dates, URL/hash/page/short quote evidence. Not a rejection of clinical findings.'
            if reason:
                quarantined.append({'ready':str(ready.relative_to(ROOT)),'reason':reason+' Not an independently accepted result.'})
                continue
            try:
                raw=ready.read_bytes();v=json.loads(raw)
                for k in ["run_id","slot","country","baseline_sha","agent_id"]:assert v[k]==item[k],(k,v.get(k),item[k])
                mf=v.get("files",v.get("file_checksums",v.get("sha256",{})))
                entries=list(mf.items()) if isinstance(mf,dict) else [(x["path"],x.get("sha256")) for x in mf]
                assert entries,"Empty frozen file list"
                resolved=[];block_files={};block_reports={};ready_mtime=ready.stat().st_mtime_ns
                for name,z in entries:
                    sha=z.get("sha256") if isinstance(z,dict) else z
                    candidates=[ready.parent/name,w/name]
                    permitted=[]
                    for candidate in candidates:
                        if not candidate.resolve().is_relative_to(w.resolve()):continue
                        ownrel=candidate.resolve().relative_to(w.resolve()).as_posix()
                        if item['slot']==5 and ownrel=='receipts/block08-network-faluns-details.json':continue
                        if item['slot']==3 and candidate.name=='evidence-quarantine-001.json':continue # Incidental held passport/earlier-text output is local-only, never hash or archive.
                        if item['slot']==3 and ownrel in {'sources/web079.json','sources/web080.json','sources/web79.json','sources/web80.json'}:continue # Worker identified these mixed held-passport returns before backup; no body/hash/archive.
                        never_read_cz={'block-09-source-b.json','block-09-source-m.json','block-09-vakpo-public-native.json','block-04-prochazka-service.json'}
                        if item['slot']==2 and candidate.name in never_read_cz:continue
                        protected_cz={'block-08-source-h.json','block-08-source-i.json','block-08-outcome-delta.json','block08_outcomes.py','restriction-07-withdrawal.json'}
                        if item['slot']==2 and (candidate.name in protected_cz or ownrel.startswith('checkpoints/block-08/')):
                            if not ownrel.startswith('checkpoints/block-08-public-safe-v3/'):continue
                        permitted.append(candidate)
                    hits=[q for q in permitted if q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(w.resolve()) and digest(q)==sha]
                    assert hits,("Missing/changed frozen file",name)
                    q=hits[0].resolve();rel=str(q.relative_to(ROOT))
                    assert not(item['slot']==5 and q.relative_to(w).as_posix()=='receipts/block08-network-faluns-details.json'),('Cancelled approval batch content is quarantined, not backup material',rel)
                    assert not(q.parent==w and q.name in {'report.md','result.json','proposed_changes.json','evidence.json','queries.json','remaining.json'}),('Mutable root file cannot be frozen checkpoint target',rel)
                    if rel in uploaded:assert uploaded[rel]==sha,("Previously backed immutable file changed",rel)
                    else:block_files[rel]={"path":rel,"sha256":sha,"bytes":q.stat().st_size}
                    resolved.append(rel)
                    if q.name=="report.md":
                        match=re.search(r'/block-(\d+)',rel)
                        logical=int(match.group(1)) if match else 0
                        if q.parent.name.startswith('final'):
                            logical=1000000+logical # Report delivery alias only; never independent research acceptance.
                        block_reports[str(item["slot"])]={"source_path":rel,"target_path":item["worker_directory"]+"/report.md","sha256":sha,"ready_file_mtime_ns":ready_mtime,"logical_block":logical,"order_note":"Logical block first, actual ready mtime only tie-break; historical repairs do not advance country. NOT source checked_at or acceptance"}
                assert ready.read_bytes()==raw,"Ready changed during read"
                rr=str(ready.relative_to(ROOT));rs=hashlib.sha256(raw).hexdigest()
                if rr not in uploaded:block_files[rr]={"path":rr,"sha256":rs,"bytes":len(raw)}
                else:assert uploaded[rr]==rs
                files.update(block_files)
                for slot,report in block_reports.items():
                    if slot not in reports or (report['logical_block'],report['ready_file_mtime_ns'])>(reports[slot]['logical_block'],reports[slot]['ready_file_mtime_ns']):reports[slot]=report
                blocks.append({"slot":item["slot"],"country":item["country"],"ready":rr,"ready_sha256":rs,"file_count":len(resolved),"ready_file_mtime_ns":ready_mtime})
            except Exception as e:errors.append({"slot":item['slot'],"country":item['country'],"ready":str(ready.relative_to(ROOT)),"error":str(e)})
    return {"run_id":RUN.name,"collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"files":list(files.values()),"ready_blocks":blocks,"latest_frozen_reports":reports,"errors":errors,"quarantined":quarantined,"new_file_count":len(files),"publication":False}
if __name__=="__main__":print(json.dumps(collect(),ensure_ascii=False))

