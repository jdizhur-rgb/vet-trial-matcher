(async function bootstrapEu6Backup(){
const root="/workspace/scratch/2d03a6db0cc6/recovered-vet-trial-matcher",run="eu6-recovery-20261016T220849-0400",branch="research/europe-recovery-"+run,base="research/audit-runs/"+run;
if(load("eu6PendingCheckpoint"))throw Error("A checkpoint is pending; inspect and reconcile before bootstrap");
const command=async(cmd,max=50000)=>{let r=await tools.exec_command({cmd,workdir:root,yield_time_ms:1000,max_output_tokens:max}),out=r.output;while(r.session_id){r=await tools.write_stdin({session_id:r.session_id,chars:"",yield_time_ms:1000,max_output_tokens:max});out+=r.output;}if(r.exit_code!==0)throw Error("Read/fetch failed: "+out.slice(-1800));return out;};
const readText=async(path)=>{const py="import pathlib,json\ns=pathlib.Path("+JSON.stringify(path)+").read_text()\n";const n=JSON.parse(await command("python - <<'PY'\n"+py+"print(json.dumps(len(s)))\nPY"));let s="";for(let i=0;i<n;i+=24000)s+=JSON.parse(await command("python - <<'PY'\n"+py+"print(json.dumps(s["+i+":"+Math.min(i+24000,n)+"],ensure_ascii=False))\nPY"));return s;};
const output=await command("set -euo pipefail\ntimeout 45 git -c credential.interactive=never fetch origin refs/heads/"+branch+"\ngit rev-parse FETCH_HEAD\ngit rev-parse FETCH_HEAD^{tree}\ngit show FETCH_HEAD:"+base+"/backups/ledger.json | sha256sum\nsha256sum "+base+"/backups/ledger.json",3000);
const lines=output.split("\n"),objects=lines.filter(s=>/^[0-9a-f]{40}$/.test(s)),hashes=lines.filter(s=>/^[0-9a-f]{64} /.test(s)).map(s=>s.slice(0,64));
if(objects.length!==2||hashes.length!==2||hashes[0]!==hashes[1])throw Error("Remote/local ledger mismatch or incomplete native proof; reconcile actual pending commit/receipt before writes");
const ledger=JSON.parse(await readText(base+"/backups/ledger.json"));if(!ledger.uploaded_files||!Array.isArray(ledger.checkpoints))throw Error("Invalid backup ledger");
const routine=await readText(base+"/github_backup_orchestrator.js");if(typeof eval(routine)!=="function")throw Error("Backup source not function");
store("eu6Root",root);store("eu6Run",run);store("eu6Branch",branch);store("eu6RemoteHead",objects[0]);store("eu6RemoteTree",objects[1]);store("eu6BackupLedger",ledger);store("eu6BackupRoutine",routine);store("eu6LastBackupVerifiedAt",ledger.last_verified_at);store("eu6PendingCheckpoint",null);
return {run_id:run,remote_head:objects[0],remote_tree:objects[1],ledger_remote_local_sha256_match:true,verified_checkpoints:ledger.checkpoints.length,last_verified_at:ledger.last_verified_at,no_remote_write:true};
})
