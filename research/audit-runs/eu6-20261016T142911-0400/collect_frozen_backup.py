"""Collect only frozen research checkpoints, never mutable worker snapshots."""
import json,pathlib,hashlib,datetime
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
        ready_paths = [q for q in w.rglob("*ready.json") if q.relative_to(w).parts[0] != "input"]
        for ready in sorted(ready_paths):
            if item['slot']==4 and ready.relative_to(w).as_posix()=='checkpoints/block-02/ready.json':
                quarantined.append({'ready':str(ready.relative_to(ROOT)),'reason':'Worker declared erroneous draft; immutable history superseded by block-02delta/ready.json. Not an accepted report or checkpoint.'})
                continue
            try:
                raw=ready.read_bytes();v=json.loads(raw)
                for k in ["run_id","slot","country","baseline_sha","agent_id"]:assert v[k]==item[k],(k,v.get(k),item[k])
                mf=v.get("files",v.get("file_checksums",v.get("sha256",{})))
                entries=list(mf.items()) if isinstance(mf,dict) else [(x["path"],x.get("sha256")) for x in mf]
                assert entries,"Empty frozen file list"
                resolved=[]
                for name,z in entries:
                    sha=z.get("sha256") if isinstance(z,dict) else z
                    candidates=[ready.parent/name,w/name]
                    hits=[q for q in candidates if q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(w.resolve()) and digest(q)==sha]
                    assert hits,("Missing/changed frozen file",name)
                    q=hits[0];rel=str(q.relative_to(ROOT))
                    if rel in uploaded:assert uploaded[rel]==sha,("Previously backed immutable file changed",rel)
                    else:files[rel]={"path":rel,"sha256":sha,"bytes":q.stat().st_size}
                    resolved.append(rel)
                    if q.name=="report.md":reports[str(item["slot"])]={"source_path":rel,"target_path":item["worker_directory"]+"/report.md","sha256":sha}
                assert ready.read_bytes()==raw,"Ready changed during read"
                rr=str(ready.relative_to(ROOT));rs=hashlib.sha256(raw).hexdigest()
                if rr not in uploaded:files[rr]={"path":rr,"sha256":rs,"bytes":len(raw)}
                else:assert uploaded[rr]==rs
                blocks.append({"slot":item["slot"],"country":item["country"],"ready":rr,"ready_sha256":rs,"file_count":len(resolved)})
            except Exception as e:errors.append({"ready":str(ready.relative_to(ROOT)),"error":str(e)})
    return {"run_id":RUN.name,"collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"files":list(files.values()),"ready_blocks":blocks,"latest_frozen_reports":reports,"errors":errors,"quarantined":quarantined,"new_file_count":len(files),"publication":False}
if __name__=="__main__":print(json.dumps(collect(),ensure_ascii=False))

