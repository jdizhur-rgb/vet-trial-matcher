const fs=require('fs'),assert=require('assert');global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};require('../seo/static/matcher/matcher.js');
const rows=new Map(JSON.parse(fs.readFileSync('data/trials_base.json')).map(x=>[x.id,x]));
const d=JSON.parse(fs.readFileSync('research/audit-runs/daily-20261020T030334-0400/status-reconciliation.json'));
for(const c of d.independent_cases){assert.strictEqual(rows.get(c.trial_id).available_for_matching,false);assert.strictEqual(window.__MATCHER_TEST__.matchTrial(rows.get(c.trial_id),{diagnosis_status:"I don't know",tumor_status:"I don't know",...c.patient,prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'])}),null,c.trial_id+':'+c.name);}
console.log('DAILY20_SOURCE_DERIVED_STATUS_PASS cases='+d.independent_cases.length);
