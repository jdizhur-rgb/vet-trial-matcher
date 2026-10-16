#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
const crypto=require('crypto');
const root=path.resolve(__dirname,'..');
global.window=global.window||{};
global.document=global.document||{querySelector:()=>null,querySelectorAll:()=>[]};
require(path.join(root,'seo/static/matcher/matcher.js'));
const {matchTrial}=window.__MATCHER_TEST__;
const byId=new Map(JSON.parse(fs.readFileSync(path.join(root,'data/trials_base.json'))).map(t=>[t.id,t]));
const {reviews}=JSON.parse(fs.readFileSync(path.join(root,'data/protocol_selection_cases.json')));
const baseline=JSON.parse(fs.readFileSync(path.join(root,'data/protocol_selection_baseline.json')));
function stable(value){
 if(Array.isArray(value))return value.map(stable);
 if(value&&typeof value==='object')return Object.fromEntries(Object.keys(value).sort().map(k=>[k,stable(value[k])]));
 return value;
}
function signature(t){return crypto.createHash('sha256').update(JSON.stringify(stable(Object.fromEntries(baseline.signature_fields.map(k=>[k,t[k]??null]))))).digest('hex');}
const reviewById=new Map(reviews.map(r=>[r.trial_id,r]));
assert.strictEqual(reviewById.size,reviews.length,'Duplicate independent review IDs');
for(const t of byId.values()){
 if(t.available_for_matching===false||!['current','confirmed_current'].includes(t.status_confidence)||!['treatment','other_treatment_access'].includes(t.study_type))continue;
 if(signature(t)!==baseline.signatures[t.id])assert.strictEqual(reviewById.get(t.id)?.selection_sha256,signature(t),`Changed/new public selection needs an independent source review: ${t.id}`);
}
const unknown="I don't know";
const defaults={species:'Dog',country:'USA',diagnosis_status:unknown,tumor_status:unknown,metastasis:unknown,localized:unknown,age_known:false,weight_known:false,surgery:unknown,prior_procedure:unknown,chemo:unknown,radiation:unknown,immunotherapy_history:unknown,steroids:unknown,immunosuppressive:unknown,osa_location:unknown,node_status:unknown,lymphoma_response:unknown,standard_therapy_unavailable:unknown,large_inoperable_or_rt_preferred:unknown,surgery_or_rt_not_possible:unknown,ct_and_current_biopsy:unknown,radiation_affordability:unknown,sex:unknown};
let cases=0;
for(const r of reviews){
 assert(r.source_url&&r.criteria&&r.reviewed_at,`Missing independent provenance: ${r.trial_id}`);
 assert(byId.has(r.trial_id),`Unknown reviewed record ${r.trial_id}`);
 assert.strictEqual(r.selection_sha256,signature(byId.get(r.trial_id)),`Independent review is stale: ${r.trial_id}`);
 assert(r.cases.some(c=>c.expected==='review')&&r.cases.some(c=>c.expected==='exclude'),`Missing positive/negative cases: ${r.trial_id}`);
 for(const c of r.cases){
  const p={...defaults,...c.patient,prefs:new Set(c.patient.prefs||['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'])};
  const result=matchTrial(byId.get(r.trial_id),p),label=`${r.trial_id}: ${c.name} ${JSON.stringify(c.patient)}`;
  // Retain the source-derived clinical cases after closure; inactive records must reject every case.
  if(byId.get(r.trial_id).available_for_matching===false)assert.strictEqual(result,null,`${label}: inactive protocol`);
  else if(c.expected==='exclude')assert.strictEqual(result,null,label);
  else{assert(result,label);assert.notStrictEqual(result.confidence,'Likely match',label);for(const term of c.unknown_contains||[])assert(result.unknown.some(x=>x.toLowerCase().includes(term.toLowerCase())),`${label}: missing screening ${term}`);}
  cases++;
 }
}
if(!process.argv.includes('--matrix')) console.log(`SOURCE_DERIVED_SELECTION_OK reviewed=${reviews.length} cases=${cases}`);
