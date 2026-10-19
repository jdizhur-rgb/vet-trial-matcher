const fs=require('fs'),assert=require('assert');global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};require('../seo/static/matcher/matcher.js');
const t=JSON.parse(fs.readFileSync('data/trials_base.json')).find(x=>x.id==='penn-anti-pd1-urothelial-carcinoma');
const d=JSON.parse(fs.readFileSync('research/audit-runs/daily-20261019T032107-0400/vgs002-closure.json'));
assert.strictEqual(t.available_for_matching,false);
for(const c of d.independent_negative_cases){assert.strictEqual(window.__MATCHER_TEST__.matchTrial(t,{...c.patient,prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'])}),null,c.name);}
console.log('VGS002_SOURCE_DERIVED_CLOSURE_PASS cases='+d.independent_negative_cases.length);
