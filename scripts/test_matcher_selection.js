#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
global.window = {};
global.document = {querySelector: () => null, querySelectorAll: () => []};
require(path.join(root, 'seo/static/matcher/matcher.js'));
const {matchTrial, diagnosisMatch} = window.__MATCHER_TEST__;
const rows = JSON.parse(fs.readFileSync(path.join(root, 'data/trials_base.json')));
const browser = JSON.parse(fs.readFileSync(path.join(root, 'seo/static/matcher/trials.json')));
const taxonomy = JSON.parse(fs.readFileSync(path.join(root, 'data/diagnosis_taxonomy.json')));
const rules = JSON.parse(fs.readFileSync(path.join(root, 'data/matcher_protocol_rules.json')));
const active = rows.filter(t => t.available_for_matching !== false && ['current','confirmed_current'].includes(t.status_confidence) && ['treatment','other_treatment_access'].includes(t.study_type || 'treatment'));
const byId = new Map(active.map(t => [t.id,t]));
const UNKNOWN = "I don't know";
function patient(t, overrides={}) {
  const r=t.requires || {};
  return {species:(Array.isArray(t.species)?t.species:String(t.species).split('/'))[0],country:t.country || 'USA',cancer:(t.cancers || ['Other solid tumor'])[0] === 'Cancer — any type' ? Object.keys(taxonomy.families).find(c => diagnosisMatch(t,c,(Array.isArray(t.species)?t.species:String(t.species).split('/'))[0])[0]) : (t.cancers || ['Other solid tumor'])[0],diagnosis_status:'Confirmed by pathology/cytology',tumor_status:'Tumor still present / measurable',metastasis:r.metastatic?'Confirmed metastases':'No known metastases',localized:'Yes',age_known:true,age:r.min_age_years || 8,weight_known:true,weight_lb:r.min_weight_lb || (r.min_weight_kg || 25)*2.2046226218,prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug']),surgery:r.prior_surgery || r.post_splenectomy || r.post_amputation?'Yes':'No',prior_procedure:r.post_splenectomy?'Splenectomy':r.post_amputation?'Amputation':UNKNOWN,chemo:r.prior_chemo?'Previously received':'Never',radiation:r.prior_radiation?'Previously received':'Never',immunotherapy_history:'Never',steroids:'Never',immunosuppressive:'No',osa_location:'Appendicular — limb bone',node_status:'Negative',lymphoma_response:r.lymphoma_response?.[0] || UNKNOWN,standard_therapy_unavailable:UNKNOWN,large_inoperable_or_rt_preferred:UNKNOWN,surgery_or_rt_not_possible:UNKNOWN,ct_and_current_biopsy:UNKNOWN,radiation_affordability:UNKNOWN,sex:UNKNOWN,...overrides};
}
let checks=0;
function check(t, overrides, expected, message) {
  assert.strictEqual(Boolean(matchTrial(t,patient(t,overrides))),expected,`${t.id}: ${message}`);checks++;
}
// Every public record, every stored criterion, both species, foreign geography,
// universal boundary values, and public/hidden-catalog identity.
assert.deepStrictEqual(browser.map(t=>t.id).sort(),active.map(t=>t.id).sort());
const matrix=[];
for (const t of rows) {
  if (!byId.has(t.id)) {
    for (const species of ['Dog','Cat']) check(t,{species,cancer:'Cancer — any type'},false,'inactive record must not leak');
    continue;
  }
  check(t,{cancer:'Cancer — any type'},true,'public record must be browsable');
  // With material answers unknown, the record must have at least one
  // disease-specific path to review. This does not assert clinical acceptance.
  const unknownPatient=patient(t,{diagnosis_status:UNKNOWN,tumor_status:UNKNOWN,
    metastasis:UNKNOWN,localized:UNKNOWN,age_known:false,weight_known:false,
    surgery:UNKNOWN,prior_procedure:UNKNOWN,chemo:UNKNOWN,radiation:UNKNOWN,
    immunotherapy_history:UNKNOWN,steroids:UNKNOWN,immunosuppressive:UNKNOWN,
    osa_location:UNKNOWN,node_status:UNKNOWN,lymphoma_response:UNKNOWN});
  const diseaseChoices=[...new Set([...Object.keys(taxonomy.families),...t.cancers])]
    .filter(c=>c!=='Cancer — any type');
  assert(diseaseChoices.some(c=>matchTrial(t,{...unknownPatient,cancer:c})),
    `${t.id}: no disease-specific retrieval witness`);
  checks++;
  const selected=patient(t).species;
  const allowedSpecies=Array.isArray(t.species)?t.species:String(t.species).split('/');
  for (const species of ['Dog','Cat']) if (!allowedSpecies.includes(species)) check(t,{species,cancer:'Cancer — any type'},false,'wrong species');
  check(t,{country:'__not_a_country__',cancer:'Cancer — any type'},false,'wrong geography');
  check({...t,available_for_matching:false},{cancer:'Cancer — any type'},false,'explicit unavailable flag');
  for (const group of ['requires','excludes']) for (const key of Object.keys(t[group] || {})) assert(rules[group][key],`${t.id}: unclassified ${group}.${key}`);
  const r=t.requires || {},e=t.excludes || {};
  for (const [key,field,bad] of [['prior_chemo','chemo','Previously received'],['prior_surgery','surgery','Yes'],['prior_local_radiation','radiation','Previously received'],['prior_immunotherapy','immunotherapy_history','Previously received'],['prior_steroids','steroids','Previously took']]) if(e[key]) check(t,{[field]:bad},false,key);
  if(r.no_metastasis) check(t,{metastasis:'Confirmed metastases'},false,'metastatic exclusion');
  if(r.metastatic) check(t,{metastasis:'No known metastases'},false,'metastasis required');
  if(r.measurable) check(t,{tumor_status:'Completely removed — clean margins'},false,'measurable disease required');
  if(r.active_treatment_target) check(t,{tumor_status:'No evidence of disease (NED)'},false,'active target required');
  for(const [k,delta] of [['min_weight_kg',-0.1],['max_weight_kg',0.1]]) if(r[k]!=null) check(t,{cancer:'Cancer — any type',weight_lb:(r[k]+delta)*2.2046226218},false,k);
  for(const [k,delta] of [['min_weight_lb',-0.1],['max_weight_lb',0.1]]) if(r[k]!=null) check(t,{cancer:'Cancer — any type',weight_lb:r[k]+delta},false,k);
  for(const [k,delta] of [['min_age_years',-0.1],['max_age_years',0.1]]) if(r[k]!=null) check(t,{cancer:'Cancer — any type',age:r[k]+delta},false,k);
  for(const key of ['appendicular_location','appendicular_osteosarcoma','limb_osteosarcoma']) if(r[key]) check(t,{osa_location:'Axial — skull, spine, rib, or pelvis'},false,key);
  for(const key of ['planned_surgery','planned_amputation','planned_surgical_resection','surgery_planned']) if(r[key]) check(t,{prefs:new Set(['Chemotherapy','Radiation','Immunotherapy','Targeted therapy','Experimental drug'])},false,key);
  const diagnoses=Object.fromEntries(['Dog','Cat'].map(s=>[s,Object.keys(taxonomy.families).filter(c=>diagnosisMatch(t,c,s)[0])]));
  matrix.push({id:t.id,species:allowedSpecies,diagnoses,constraints:{requires:Object.keys(r),excludes:Object.keys(e)}});
}
const tufts=byId.get('tufts-z007-broad-solid-2026');
for(const cancer of ['Soft tissue sarcoma','Oral melanoma','Primary lung tumor','Mammary carcinoma','Urothelial carcinoma']) check(tufts,{cancer},true,`missing solid diagnosis ${cancer}`);
for(const cancer of ['B-cell lymphoma','Acute myeloid leukemia','Other liver tumor']) check(tufts,{cancer},false,`out of scope or unresolved ${cancer}`);
// HCC is a carcinoma candidate, with the ambiguous liver exclusion disclosed.
const tuftsLiver=matchTrial(tufts,patient(tufts,{cancer:'Hepatocellular carcinoma'}));
assert(tuftsLiver,'Tufts HCC candidate must remain discoverable');
assert.notStrictEqual(tuftsLiver.confidence,'Likely match');
assert(tuftsLiver.unknown.some(x=>x.includes('Tufts must confirm eligibility') && x.includes('liver-disease exclusion') && x.includes('repeated-biopsy')));
check(tufts,{cancer:'Hepatocellular carcinoma',immunotherapy_history:'Previously received'},false,'HCC must retain prior immunotherapy exclusion');
check(tufts,{cancer:'Hepatocellular carcinoma',weight_lb:6*2.2046226218},false,'HCC must retain minimum weight');
const caalm=byId.get('ucd-pdl1-metastatic');
check(caalm,{cancer:'Oral melanoma'},true,'named CAALM cohort');
for(const cancer of ['Soft tissue sarcoma','Gastric / stomach cancer','Hepatocellular carcinoma']) check(caalm,{cancer},false,`false broad CAALM match ${cancer}`);
assert(!byId.has('mizzou-cotc027-hypomethylating'), 'COTC027 dose/PK research must stay outside the treatment catalog');
check(byId.get('leah-bcell-cart-2026'),{},true,'active site must survive inactive-site prose');
check(byId.get('msu-tcell-lymphoma'),{cancer:'T-cell lymphoma'},true,'exclusion text must not hide the accepted PTCL cohort');
check(byId.get('msu-tcell-lymphoma'),{cancer:'Cutaneous epitheliotropic lymphoma'},false,'cutaneous lymphoma excluded');
check(byId.get('cornell-smart-start-bcell-lymphoma'),{cancer:'T-cell lymphoma'},false,'B-cell-only Cornell cohort');
check(byId.get('china-petcura-personalized-mrna-iit-2026'),{cancer:'T-cell lymphoma'},false,'explicit PETcura T-cell exclusion');
check(byId.get('china-petcura-personalized-mrna-iit-2026'),{cancer:'Brain tumor / glioma'},false,'explicit PETcura brain exclusion');
for(const t of [byId.get('jp-tokyo-organoid-guided-targeted-therapy-2026'),byId.get('jp-tokyo-macromolecular-pirarubicin-solid-tumors')]) {
  check(t,{cancer:'Hepatocellular carcinoma'},true,'Tokyo solid-tumor scope');
  check(t,{cancer:'B-cell lymphoma'},false,'Tokyo blood cancer exclusion');
  check(t,{cancer:'Hepatocellular carcinoma',standard_therapy_unavailable:'No'},false,'standard therapy still available');
}
// An explicitly species-scoped empty cohort may not be rescued by broad labels.
assert.deepStrictEqual(diagnosisMatch({...tufts,cancers_by_species:{Dog:[],Cat:['Other solid tumor']}},'Soft tissue sarcoma','Dog'),[false,false]);
const sentinel={...tufts,requires:{confirmed:true,measurable:true,anesthesia_candidate:true},excludes:{},special_requirement:null,owner_prescreen_required:false};
assert(matchTrial(sentinel,patient(sentinel,{cancer:'Other sarcoma'})).unknown.some(x=>x.includes('anesthesia candidate')));
// Independent Python comparison validates every species/diagnosis pair against
// the same reviewed taxonomy used in the browser and static diagnosis pages.
require('./test_matcher_protocol_sources.js');
if(process.argv.includes('--matrix')) console.log(JSON.stringify(matrix));
else console.log(`MATCHER_SELECTION_OK canonical=${rows.length} public=${active.length} checks=${checks} criteria=${Object.keys(rules.requires).length+Object.keys(rules.excludes).length}`);
