'use strict';
const fs=require('fs'); global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};require('../seo/static/matcher/matcher.js');
const rows=JSON.parse(fs.readFileSync('seo/static/matcher/trials.json'));
const cases=['USA','Japan'].map(country=>{
 const patient={species:'Dog',country,cancer:'Cancer — any type',diagnosis_status:"I don't know",age:'',weight:'',zip_code:'',approach:'',prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'])};
 const matches=rows.map(t=>window.__MATCHER_TEST__.matchTrial(t,patient)).filter(Boolean);
 return {country,patient:{...patient,prefs:[...patient.prefs]},count:matches.length,records:matches.map(m=>({id:m.trial.id,title:m.trial.title,center:m.trial.center}))};
});
fs.writeFileSync('research/audit-runs/daily-20261023T030510-0400/expected-live-searches.json',JSON.stringify({at:new Date().toISOString(),catalog:'seo/static/matcher/trials.json',cases},null,2)+'\n');console.log(cases.map(c=>({country:c.country,count:c.count})));
