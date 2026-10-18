// Execute in functions.exec, not native Node. State keys newRunId/newResearchBranch/newRemoteHead/newRemoteTree must be restored from verified branch SHA and tree.
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

