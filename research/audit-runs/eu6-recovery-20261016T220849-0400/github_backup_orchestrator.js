(async function(seq){
const repo="jdizhur-rgb/vet-trial-matcher",root=load("eu6Root"),run=load("eu6Run"),branch=load("eu6Branch"),base="research/audit-runs/"+run,opts={workdir:root,yield_time_ms:1000};
if(typeof root!=="string"||!root.startsWith("/workspace/scratch/")||typeof run!=="string"||!run.startsWith("eu6-recovery-")||branch!=="research/europe-recovery-"+run||!load("eu6BackupLedger")?.uploaded_files||!/^([a-f0-9]{40})$/.test(load("eu6RemoteHead")||"")||!/^([a-f0-9]{40})$/.test(load("eu6RemoteTree")||""))throw Error("Research backup state incomplete; rehydrate verified remote state before any file write");
const read=async cmd=>{let r=await tools.exec_command({...opts,cmd,max_output_tokens:50000}),output=r.output;while(r.session_id){r=await tools.write_stdin({session_id:r.session_id,chars:"",yield_time_ms:1000,max_output_tokens:50000});output+=r.output;}if(r.exit_code!==0)throw Error("Command failed: "+JSON.stringify({...r,output:output.slice(-2000)}));return output;};
const readText=async(p,expected)=>{const py="import pathlib,json,hashlib\nb=pathlib.Path("+JSON.stringify(p)+").read_bytes()\n"+(expected?"assert hashlib.sha256(b).hexdigest()=="+JSON.stringify(expected)+", 'Frozen/controller file changed'\n":"")+"s=b.decode('utf-8')\n";const meta=JSON.parse(await read("python - <<'PY'\n"+py+"print(json.dumps({'characters':len(s),'content':s if len(s)<=32000 else None},ensure_ascii=False))\nPY"));if(meta.content!==null)return meta.content;const chunks=[];for(let i=0;i<meta.characters;i+=32000)chunks.push(JSON.parse(await read("python - <<'PY'\n"+py+"print(json.dumps(s["+i+":"+Math.min(i+32000,meta.characters)+"],ensure_ascii=False))\nPY")));const result=chunks.join("");if(result.length<meta.characters)throw Error("Truncated text chunks");return result;};
const put=async content=>{for(let k=0;k<2;k++){const r=await tools.mcp__codex_apps__github_create_blob({repository_full_name:repo,content,encoding:"utf-8"});if(r.structuredContent?.sha)return r.structuredContent.sha;if(k)throw Error("blob failed "+JSON.stringify(r));}};
const m=JSON.parse(await read("python "+base+"/collect_frozen_backup.py"));store("eu6LatestCollection",m);
if(m.errors.length)notify({checkpoint_collection_errors:m.errors});
if(!m.files.length)text({status:"CONTROLLER_ONLY_CHECKPOINT",errors:m.errors});
const manifestPath=base+"/backups/checkpoint-"+seq+"-manifest.json";
text(await tools.apply_patch("*** Begin Patch\n*** Add File: "+root+"/"+manifestPath+"\n+"+JSON.stringify(m)+"\n*** End Patch"));
const archive="/workspace/scratch/2d03a6db0cc6/"+run+"-checkpoint-"+seq+".tar.zst";
const extras=[base+"/assignments.json",base+"/criteria.json",base+"/controller-plan.json",base+"/collect_frozen_backup.py",base+"/github_backup_orchestrator.js",base+"/backups/ledger.json",base+"/report.md",base+"/restore-guide.md",base+"/check_research_gate.py",base+"/publication-ledger.json",base+"/controller-report-readback-008.json",base+"/collector-history-scope-fix.json"];
extras.push(base+"/controller-runtime-rehydration-010.json");
extras.push(base+"/collector-path-normalization-fix.json");
extras.push(base+"/report-alias-final-selection.json");
extras.push(base+"/worker-acceptance-1.json",base+"/worker-acceptance-2.json",base+"/worker-acceptance-4.json");
extras.push(base+"/bootstrap_backup_state.js");
extras.push(base+"/controller-bootstrap-validation.json");
extras.push(base+"/bootstrap-remote-closure-validation.json",base+"/controller-permission-incident-review.json");
extras.push(base+"/source-minimal-backup-policy-receipt.json");
extras.push(base+"/parent-baseline-input-integrity.json");
extras.push(base+"/parent-germany-reference-scope-review.json");
extras.push(base+"/worker-4/input/parent-university-evidence-recovered-001.json");
extras.push(base+"/report-alias-scope-addendum-correction.json");
const packCode="import pathlib,json,subprocess,hashlib,tarfile,zstandard,re\n"+
"m=json.loads(pathlib.Path("+JSON.stringify(manifestPath)+").read_text()); expected={x['path']:x['sha256'] for x in m['files']}\n"+
"controller_paths=["+[manifestPath,...extras].map(x=>JSON.stringify(x)).join(",")+"];controller_hashes={p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest() for p in controller_paths};expected.update(controller_hashes);paths=list(expected)\n"+
"rx=re.compile(rb'AIza[A-Za-z0-9_-]{35}|github_pat_[A-Za-z0-9_]{40,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')\n"+
"for p,h in expected.items():\n b=pathlib.Path(p).read_bytes();assert p.startswith('research/'),('Outside research',p);assert hashlib.sha256(b).hexdigest()==h,('Changed',p);assert not rx.search(b),('Credential-shaped text',p)\n"+
"t=subprocess.Popen(['tar','-c','--null','-T','-'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);z=subprocess.Popen(['zstd','-q','-10','--long=27','-T2','-o',"+JSON.stringify(archive)+"],stdin=t.stdout);t.stdout.close();t.stdin.write(bytes([0]).join(p.encode() for p in paths)+bytes([0]));t.stdin.close();assert t.wait()==0;assert z.wait()==0\n"+
"seen={}\nwith open("+JSON.stringify(archive)+",'rb') as f:\n with zstandard.ZstdDecompressor().stream_reader(f) as stream:\n  with tarfile.open(fileobj=stream,mode='r|') as tf:\n   for x in tf:\n    if x.isfile() and x.name in expected:seen[x.name]=hashlib.sha256(tf.extractfile(x).read()).hexdigest()\nassert seen==expected\np=pathlib.Path("+JSON.stringify(archive)+");print(json.dumps({'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'member_hashes_pass':len(seen),'controller_sha256':controller_hashes}))";
const info=JSON.parse(await read("python - <<'PY'\n"+packCode+"\nPY"));store("eu6PendingCheckpoint",{seq,m,info,archive,stage:"PACKED"});
const pieces=[],chunk=24576,count=Math.ceil(info.bytes/chunk);
for(let first=0;first<count;first+=12)await Promise.all(Array.from({length:Math.min(12,count-first)},(_,j)=>first+j).map(async i=>{const s=(await read("dd if="+archive+" bs="+chunk+" skip="+i+" count=1 status=none | base64 -w0")).trim();if(s.length!==4*Math.ceil(Math.min(chunk,info.bytes-i*chunk)/3))throw Error("Truncated archive chunk");pieces[i]=s;}));
const ab=await tools.mcp__codex_apps__github_create_blob({repository_full_name:repo,content:pieces.join(""),encoding:"base64"});if(!ab.structuredContent?.sha)throw Error("Archive upload failed");const archiveBlob=ab.structuredContent.sha;
const aliases=Object.entries(m.latest_frozen_reports).filter(([slot,v])=>!m.errors.some(e=>e.slot===Number(slot))).map(([slot,v])=>v),sourceFiles=[manifestPath,...extras,...aliases.map(x=>x.source_path)];
const texts={};for(const p of sourceFiles){const expectedHash=info.controller_sha256[p]||aliases.find(x=>x.source_path===p)?.sha256;if(!expectedHash)throw Error("Missing frozen/controller checksum "+p);texts[p]=await readText(p,expectedHash);}
const elems=[];
for(let first=0;first<sourceFiles.length;first+=6)await Promise.all(sourceFiles.slice(first,first+6).map(async p=>{const sha=await put(texts[p]);const alias=aliases.find(x=>x.source_path===p)?.target_path;elems.push({path:alias||p,mode:"100644",type:"blob",sha});}));
const parent=load("eu6RemoteHead"),control={run_id:run,checkpoint:seq,archive_path:base+"/backups/checkpoint-"+seq+".tar.zst",archive_bytes:info.bytes,archive_sha256:info.sha256,archive_git_blob:archiveBlob,controller_sha256:info.controller_sha256,parent_sha:parent,new_immutable_file_count:m.files.length,member_hashes_pass:info.member_hashes_pass,ready_blocks:m.ready_blocks,site_publication:false,remote_readback_pending:true};
const controlPath=base+"/backups/checkpoint-"+seq+"-control.json";
elems.push({path:control.archive_path,mode:"100644",type:"blob",sha:archiveBlob},{path:controlPath,mode:"100644",type:"blob",sha:await put(JSON.stringify(control,null,2))});
const commit=async(es,message)=>{let tr;for(let n=0;n<2;n++){tr=await tools.mcp__codex_apps__github_create_tree({repository_full_name:repo,base_tree_sha:load("eu6RemoteTree"),tree_elements:es});if(tr.structuredContent?.sha)break;}if(!tr.structuredContent?.sha)throw Error("tree failure "+JSON.stringify(tr));const c=await tools.mcp__codex_apps__github_create_commit({repository_full_name:repo,parent_sha:load("eu6RemoteHead"),tree_sha:tr.structuredContent.sha,message});if(!c.structuredContent?.sha)throw Error("commit failure");const up=await tools.mcp__codex_apps__github_update_ref({repository_full_name:repo,branch_name:branch,expected_sha:load("eu6RemoteHead"),sha:c.structuredContent.sha,force:false});if(up.isError||!up.structuredContent?.success)throw Error("ref lease/update failure "+JSON.stringify(up));store("eu6RemoteHead",c.structuredContent.sha);store("eu6RemoteTree",tr.structuredContent.sha);return c.structuredContent.sha;};
const dataSha=await commit(elems,"research-only checkpoint"+seq+": immutable candidate/source/query delta and restriction shards");
store("eu6PendingCheckpoint",{seq,m,info,archive,stage:"REMOTE_DATA_COMMITTED",dataSha});
const rb=await tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:dataSha,path:controlPath});const actual=JSON.parse(rb.structuredContent?.content);if(actual.archive_sha256!==info.sha256||actual.run_id!==run)throw Error("Control readback failed");
const fetch=await tools.exec_command({...opts,cmd:"timeout 45 git -c credential.interactive=never fetch origin refs/heads/"+branch+"\ngit rev-parse FETCH_HEAD\ngit show FETCH_HEAD:"+control.archive_path+" | sha256sum",max_output_tokens:1500});
let fr=fetch,fetchOutput=fetch.output;
while(fr.session_id){fr=await tools.write_stdin({session_id:fr.session_id,chars:"",yield_time_ms:1000,max_output_tokens:1500});fetchOutput+=fr.output;}
if(fr.exit_code!==0||!fetchOutput.includes(info.sha256)||!fetchOutput.includes(dataSha))throw Error("Remote archive SHA readback failed "+JSON.stringify(fr));
const now=(await tools.clock__curr_time({})).current_time;
const receipt={run_id:run,checkpoint:seq,kind:"RESEARCH_ONLY_REMOTE_VERIFIED",branch,data_sha:dataSha,verified_at:now,archive_sha256:info.sha256,archive_bytes:info.bytes,remote_control_readback:true,remote_archive_sha256_match:true,archive_member_hashes_verified:info.member_hashes_pass,new_files:m.files.length,ready_blocks:m.ready_blocks,site_publication:false,collection_errors:m.errors};
const ledger=load("eu6BackupLedger");for(const x of m.files)ledger.uploaded_files[x.path]=x.sha256;ledger.last_verified_data_sha=dataSha;ledger.last_verified_at=now;ledger.checkpoints.push({checkpoint:seq,data_sha:dataSha,manifest:"backups/checkpoint-"+seq+"-manifest.json",receipt:"backups/checkpoint-"+seq+"-remote-receipt.json"});
const receiptPath=base+"/backups/checkpoint-"+seq+"-remote-receipt.json",ledgerPath=base+"/backups/ledger.json";
const oldLedger=JSON.parse(await readText(ledgerPath));
let patch="*** Begin Patch\n*** Add File: "+root+"/"+receiptPath+"\n"+JSON.stringify(receipt,null,2).split("\n").map(x=>"+"+x).join("\n")+"\n*** Update File: "+root+"/"+ledgerPath+"\n@@\n"+JSON.stringify(oldLedger,null,2).split("\n").map(x=>"-"+x).join("\n")+"\n"+JSON.stringify(ledger,null,2).split("\n").map(x=>"+"+x).join("\n")+"\n*** End Patch";text(await tools.apply_patch(patch));
const es=[{path:receiptPath,mode:"100644",type:"blob",sha:await put(JSON.stringify(receipt,null,2)+"\n")},{path:ledgerPath,mode:"100644",type:"blob",sha:await put(JSON.stringify(ledger,null,2)+"\n")}];
const receiptSha=await commit(es,"research-only: verified checkpoint"+seq+" receipt and content-addressed ledger");
const proof=await tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:receiptSha,path:receiptPath});const pv=JSON.parse(proof.structuredContent?.content);if(pv.data_sha!==dataSha||pv.archive_sha256!==info.sha256)throw Error("Receipt readback failed");
store("eu6BackupLedger",ledger);store("eu6LastBackupVerifiedAt",now);store("eu6LastBackupResult",{seq,dataSha,receiptSha,slots:[...new Set(m.ready_blocks.map(x=>x.slot))],files:m.files.length,errors:m.errors});store("eu6PendingCheckpoint",null);
text({status:"REMOTE_BACKUP_VERIFIED",checkpoint:seq,dataSha,receiptSha,files:m.files.length,bytes:info.bytes,blocks:m.ready_blocks.length,errors:m.errors});
})
