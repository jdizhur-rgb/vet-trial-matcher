'use strict';
const fs=require('fs'),vm=require('vm'),cp=require('child_process'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'../../..');process.chdir(root);
const baseline='f9b924c4baf8acd101c7df890e1c663e54f8f201';
const doc={querySelector:()=>null,querySelectorAll:()=>[]};global.window={};global.document=doc;
require(path.join(root,'seo/static/matcher/matcher.js'));const after=window.__MATCHER_TEST__;
const sandbox={window:{},document:doc};vm.runInNewContext(cp.execFileSync('git',['show',baseline+':seo/static/matcher/matcher.js'],{encoding:'utf8'}),sandbox);const before=sandbox.window.__MATCHER_TEST__;
const rows=JSON.parse(fs.readFileSync('seo/static/matcher/trials.json'));
const old=new Map(JSON.parse(cp.execFileSync('git',['show',baseline+':seo/static/matcher/trials.json'],{encoding:'utf8'})).map(t=>[t.id,t]));
const changed=new Set(Object.keys(JSON.parse(fs.readFileSync(path.join(__dirname,'correction-sources.json')))));
const families=Object.keys(JSON.parse(fs.readFileSync('data/diagnosis_taxonomy.json')).families);
const reviews=new Map(JSON.parse(fs.readFileSync('data/protocol_selection_cases.json')).reviews.map(r=>[r.trial_id,r]));
const unknown="I don't know";
const fields={tumor_status:['Tumor still present / measurable','Local recurrence','Completely removed — clean margins','Removed — incomplete/dirty margins','No evidence of disease (NED)'],metastasis:['No known metastases','Confirmed metastases','Suspected / staging incomplete'],surgery:['No','Yes'],prior_procedure:['Splenectomy','Amputation','Limb-sparing surgery','Other'],chemo:['Never','Currently receiving','Previously received'],radiation:['Never','Currently receiving','Previously received'],immunotherapy_history:['Never','Previously received','Currently receiving'],steroids:['Never / no','Currently taking','Previously took'],immunosuppressive:['Yes','No'],hsa_site:['Spleen','Heart / right atrium','Other'],lymphoma_type:['B-cell','T-cell','Other'],lymphoma_response:['Newly diagnosed / untreated','Complete remission','Partial response','Progression during treatment','First relapse after remission','More than one relapse']};
const allPrefs=['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'];
let checks=0,removed=0,added=0;const ledger=[];
for(const t of rows){const b=old.get(t.id);assert(b,'unexpected public addition');let n=0,loss=0,gain=0;
 const defaults={species:'Dog',country:'All countries',diagnosis_status:unknown,tumor_status:unknown,metastasis:unknown,localized:unknown,age_known:false,weight_known:false,surgery:unknown,prior_procedure:unknown,chemo:unknown,radiation:unknown,immunotherapy_history:unknown,steroids:unknown,immunosuppressive:unknown,hsa_site:unknown,lymphoma_type:unknown,lymphoma_response:unknown,osa_location:unknown,node_status:unknown,standard_therapy_unavailable:unknown,large_inoperable_or_rt_preferred:unknown,surgery_or_rt_not_possible:unknown,ct_and_current_biopsy:unknown,radiation_affordability:unknown,prefs:new Set(allPrefs)};
 function check(p){const was=!!before.matchTrial(b,p),now=!!after.matchTrial(t,p);if(was!==now){assert(changed.has(t.id),'unreviewed selection delta '+t.id);if(now){assert(t.id==='ethos-epush-hsa' && p.prefs.size===1 && p.prefs.has('Surgery'),'unexpected newly added selection '+t.id);gain++;}else loss++;}n++;}
 for(const species of ['Dog','Cat'])for(const cancer of families){const p={...defaults,species,cancer};check(p);if(!before.diagnosisMatch(b,cancer,species)[0])continue;
 for(const [field,values] of Object.entries(fields))for(const value of values)check({...p,[field]:value});
 for(const pref of allPrefs)check({...p,prefs:new Set([pref])});
 }
 // Exact source weight boundaries and their valid immediate interior.
 if(t.id==='ethos-epush-hsa')for(const kg of [5,5.1,44.9,45])check({...defaults,cancer:'Hemangiosarcoma',weight_known:true,weight_lb:kg*2.2046226218});
 checks+=n;removed+=loss;added+=gain;
 const r=reviews.get(t.id);ledger.push({id:t.id,country:t.country,species:t.species,checks:n,removed_scenarios:loss,added_scenarios:gain,disposition:changed.has(t.id)?'corrected_with_source_derived_cases':'no_new_rule_change_from_this_selection_pass',independent_case_review_present:!!r,primary_criteria_reviewed_at:r?.reviewed_at||null,current_run_fresh_primary_for_correction:r?.source_visit_refreshed_this_run===true,scope:'automated selection and retained primary-derived cases; not a new recruitment confirmation'});
}
const report={baseline,public_records:rows.length,diagnosis_choices:families.length,checks,removed_scenarios:removed,added_scenarios:added,corrected_ids:[...changed],per_record:ledger};fs.writeFileSync(path.join(__dirname,'matrix-and-dispositions.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({records:rows.length,diagnoses:families.length,checks,removed_scenarios:removed,added_scenarios:added,corrected:changed.size}));
