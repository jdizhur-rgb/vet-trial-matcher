// Research-only backup controller for functions.exec. Restore run/branch/head/tree from verified remote before execution.
async function commitNewResearch(files,message,extraEntries=[]){
 const repo="jdizhur-rgb/vet-trial-matcher", entries=[...extraEntries];
 const keys=Object.keys(files);
 for(let n=0;n<keys.length;n+=6)await Promise.all(keys.slice(n,n+6).map(async p=>{
  if(!p.startsWith("research/audit-runs/"+load("newRunId")+"/"))throw Error("Outside current research run");
  const r=await tools.mcp__codex_apps__github_create_blob({repository_full_name:repo,content:files[p],encoding:"utf-8"});
  const sha=r.structuredContent?.sha;if(!sha)throw Error("Git blob creation failed "+p);
  entries.push({path:p,mode:"100644",type:"blob",sha});
 }));
 const tree=await tools.mcp__codex_apps__github_create_tree({repository_full_name:repo,base_tree_sha:load("newRemoteTree"),tree_elements:entries});
 if(!tree.structuredContent?.sha)throw Error("tree failure");
 const parent=load("newRemoteHead");
 const c=await tools.mcp__codex_apps__github_create_commit({repository_full_name:repo,parent_sha:parent,tree_sha:tree.structuredContent.sha,message});
 if(!c.structuredContent?.sha)throw Error("commit failure");
 const u=await tools.mcp__codex_apps__github_update_ref({repository_full_name:repo,branch_name:load("newResearchBranch"),expected_sha:parent,sha:c.structuredContent.sha,force:false});
 if(u.isError||!u.structuredContent?.success)throw Error("Ref lease failure "+JSON.stringify(u));
 store("newRemoteHead",c.structuredContent.sha);store("newRemoteTree",tree.structuredContent.sha);
 const control=keys.find(p=>p.endsWith("control.json"))||keys[0];
 const back=await tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:c.structuredContent.sha,path:control});
 if(back.structuredContent?.content!==files[control])throw Error("Control content readback mismatch");
 return {sha:c.structuredContent.sha,tree_sha:tree.structuredContent.sha,parent_sha:parent,files:keys.length,reference_entries:extraEntries.length,readback_path:control,exact_readback:true};
}
async function readBinary(path,size){const chunks=[];for(let i=0;i<Math.ceil(size/24576);i+=12){const part=await Promise.all(Array.from({length:Math.min(12,Math.ceil(size/24576)-i)},(_,k)=>tools.exec_command({cmd:"dd if='"+path+"' bs=24576 skip="+(i+k)+" count=1 status=none | base64 -w0",max_output_tokens:14000})));for(const p of part){if(p.exit_code!==0||!/^[A-Za-z0-9+/=]*$/.test(p.output))throw Error("binary read failed");chunks.push(p.output);}}const s=chunks.join("");if(s.length!==4*Math.ceil(size/3))throw Error("base64 length mismatch");return s;}
async function command(cmd,budget=10000){let r=await tools.exec_command({cmd,workdir:load("eu6Root"),max_output_tokens:budget,yield_time_ms:1000});let out=r.output;while(r.session_id){r=await tools.write_stdin({session_id:r.session_id,chars:"",max_output_tokens:budget,yield_time_ms:1000});out+=r.output;}if(r.exit_code!==0)throw Error("Command failed: "+out);return out;}
async function writeResearch(path,content,exists=false){let patch="*** Begin Patch\n";if(exists){const old=await command("sed -n '1,30000p' '"+path+"'",60000);patch+="*** Update File: "+path+"\n@@\n"+old.trimEnd().split("\n").map(x=>"-"+x).join("\n")+"\n"+content.trimEnd().split("\n").map(x=>"+"+x).join("\n")+"\n";}else patch+="*** Add File: "+path+"\n"+content.split("\n").map(x=>"+"+x).join("\n")+"\n";await tools.apply_patch(patch+"*** End Patch");}
async function backupOne(seq,extras=[]){
 const repo="jdizhur-rgb/vet-trial-matcher",root=load("eu6Root"),base="research/audit-runs/"+load("newRunId");
 const m=JSON.parse(await command("python "+base+"/collect_ready.py "+seq,50000));
 if(m.errors.length)throw Error("Collector errors "+JSON.stringify(m.errors));
 if(m.archive_member_readback!=="PASS")throw Error("Archive member verification failed");
 const entries=[];const upload=async(path,local,size)=>{const data=await readBinary(local,size);const r=await tools.mcp__codex_apps__github_create_blob({repository_full_name:repo,content:data,encoding:"base64"});if(!r.structuredContent?.sha)throw Error("blob failed "+path);entries.push({path,mode:"100644",type:"blob",sha:r.structuredContent.sha});};
 await upload(m.archive.path,m.archive.local_path,m.archive.bytes);
 for(const r of m.files.filter(x=>x.path.endsWith("/report.md")))await upload(r.path,root+"/"+r.path,r.bytes);
 for(const r of extras)await upload(r.path,r.local_path,r.bytes);
 const files={};files[base+"/backups/"+seq+"-manifest.json"]=JSON.stringify(m,null,2)+"\n";
 files[base+"/backups/"+seq+"-control.json"]=JSON.stringify({run_id:load("newRunId"),seq,baseline_sha:load("newBaseline"),archive_path:m.archive.path,archive_sha256:m.archive.sha256,file_count:m.files.length,site_publication:false},null,2)+"\n";
 for(const name of ["research_backup.js","collect_ready.py","deliver_nl_dependencies.py"])files[base+"/"+name]=await command("sed -n '1,500p' "+base+"/"+name,15000);
 for(const[p,s]of Object.entries(files)){const exists=(await command("test -f '"+root+"/"+p+"' && echo yes || echo no",100)).trim()==="yes";if(!p.endsWith("research_backup.js"))await writeResearch(root+"/"+p,s,exists);}
 const data=await commitNewResearch(files,"Research-only checkpoint "+seq+": immutable country evidence",entries);
 await command("timeout 60 git -c http.connectTimeout=10 -c http.lowSpeedLimit=1 -c http.lowSpeedTime=30 fetch --no-tags origin '"+load("newResearchBranch")+"'",2000);
 const proof=await command("set -euo pipefail\ngit show "+data.sha+":"+m.archive.path+" | sha256sum\ntimeout 45 git -c http.connectTimeout=10 -c http.lowSpeedLimit=1 -c http.lowSpeedTime=25 ls-remote --heads origin '"+load("newResearchBranch")+"'",2000);
 if(!proof.includes(m.archive.sha256+"  -")||!proof.includes(data.sha+"\trefs/heads/"+load("newResearchBranch")))throw Error("Remote SHA verification failed "+proof);
 const receipt={run_id:load("newRunId"),seq,checked_at:(await tools.clock__curr_time({})).current_time,branch:load("newResearchBranch"),data_sha:data.sha,tree_sha:data.tree_sha,archive_path:m.archive.path,archive_sha256:m.archive.sha256,remote_archive_sha256:m.archive.sha256,remote_branch_sha:data.sha,archive_member_readback:"PASS",control_exact_readback:true,files:m.files.length,ready_blocks:m.ready_blocks,extra_direct_files:extras,site_publication:false};
 let ledger=JSON.parse(await command("sed -n '1,30000p' "+base+"/backups/ledger.json",50000));
 for(const r of m.files)ledger.uploaded_files[r.path]=r.sha256;ledger.checkpoints.push(receipt);
 const final={[base+"/backups/"+seq+"-receipt.json"]:JSON.stringify(receipt,null,2)+"\n",[base+"/backups/ledger.json"]:JSON.stringify(ledger,null,2)+"\n"};
 for(const[p,s]of Object.entries(final))await writeResearch(root+"/"+p,s,p.endsWith("/ledger.json"));
 const saved=await commitNewResearch(final,"Verify remote research checkpoint "+seq+", no site deployment");store("newLastVerifiedBackup",{receipt_sha:saved.sha,...receipt});return {receipt_sha:saved.sha,...receipt};
}

