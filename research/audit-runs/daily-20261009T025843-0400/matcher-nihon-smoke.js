'use strict';
const fs=require('fs'), path=require('path'), assert=require('assert');
const root=path.resolve(__dirname,'../../..');
global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};
require(path.join(root,'seo/static/matcher/matcher.js'));
const rows=JSON.parse(fs.readFileSync(path.join(root,'data/trials_base.json'),'utf8'));
const api=window.__MATCHER_TEST__;
const base={species:'Dog',country:'Japan',cancer:'B-cell lymphoma',diagnosis_status:'Confirmed by pathology/cytology',tumor_status:'Tumor still present / measurable',metastasis:'No known metastases',localized:'Yes',age_known:true,age:8,weight_known:true,weight_lb:22,prefs:new Set(['Chemotherapy','Targeted therapy','Experimental drug']),surgery:'No',radiation:'Never',chemo:'Never',immunotherapy_history:'Never',steroids:'Never',immunosuppressive:'No'};
const b=rows.find(r=>r.id==='jp-nihon-proteasome-inhibitor-b-cell-tumors'),l=rows.find(r=>r.id==='jp-nihon-mutation-positive-lung-cancer');
let cases=0;
function check(r,overrides,expected){const match=api.matchTrial(r,{...base,...overrides});assert.strictEqual(Boolean(match),expected,JSON.stringify(overrides));if(match)assert.strictEqual(match.confidence,'Possible match');cases++;}
for(const species of ['Dog','Cat']){check(b,{species},true);check(b,{species,cancer:'Multiple myeloma / plasma cell cancer'},true);check(b,{species,cancer:'Chronic lymphocytic leukemia'},true);check(b,{species,cancer:'T-cell lymphoma'},false);check(b,{species,country:'USA'},false);}
check(b,{approach:'targeted_therapy'},true);
check(l,{cancer:'Primary lung tumor'},true);
check(l,{cancer:'Primary lung tumor',approach:'targeted_therapy'},true);
check(l,{cancer:'Primary lung tumor',species:'Cat'},false);
check(l,{cancer:'Primary lung tumor',weight_lb:3*2.2046226218},false);
check(l,{cancer:'Primary lung tumor',weight_lb:4*2.2046226218},true);
check(l,{cancer:'Primary lung tumor',tumor_status:'No evidence of disease (NED)'},false);
check(l,{cancer:'Primary lung tumor',country:'USA'},false);
assert(api.matchTrial(l,{...base,cancer:'Primary lung tumor'}).unknown.some(x=>x.includes('mutation')));
console.log(`NIHON_MATCHER_SMOKE_PASS cases=${cases}; qualifying mutation remains investigator-prescreened`);
