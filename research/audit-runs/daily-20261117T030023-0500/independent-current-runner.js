const fs=require('fs'),path=require('path');
global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};
require(path.join(process.cwd(),'seo/static/matcher/matcher.js'));
const t=new Map(require(path.join(process.cwd(),'data/trials_base.json')).map(v=>[v.id,v]));
const rows=JSON.parse(fs.readFileSync(process.argv[2])), tests=[];
for(const [id,country,species,cancer,positive,negative,unknown] of rows){
 const base={country,species,cancer,diagnosis_status:'Confirmed by pathology/cytology', tumor_status:"I don't know",metastasis:"I don't know",localized:"I don't know",surgery:"I don't know",chemo:"I don't know",radiation:"I don't know",immunotherapy_history:"I don't know", steroids:"I don't know",immunosuppressive:"I don't know",lymphoma_type:"I don't know",loss_of_disease:"I don't know",age_known:false,weight_known:false,standard_therapy_unavailable:"I don't know",prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug'])};
 const test=(p)=>{if(Array.isArray(p.prefs))p.prefs=new Set(p.prefs); return window.__MATCHER_TEST__.matchTrial(t.get(id),p);};
 const out={pos:test({...base,...positive}),neg:test({...base,...positive,...negative}),unknown:test({...base,diagnosis_status:"I don't know",...unknown})};
 const ok={positive:!!out.pos,negative:!out.neg,unknown:!!out.unknown&&out.unknown.confidence!=='Likely match'};
 tests.push({id,...ok,pass:Object.values(ok).every(Boolean),positive_class:out.pos?.confidence,negative_class:out.neg?.confidence,unknown_class:out.unknown?.confidence,unknown_notes:out.unknown?.unknown});
}
console.log(JSON.stringify({at:new Date().toISOString(),test_count:tests.length,passed:tests.filter(t=>t.pass).length,tests},null,2));
process.exitCode=tests.some(x=>!x.pass)?1:0;
