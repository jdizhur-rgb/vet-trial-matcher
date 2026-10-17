const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../../..');global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};require(path.join(root,'seo/static/matcher/matcher.js'));
const rows=JSON.parse(fs.readFileSync(path.join(root,'seo/static/matcher/trials.json'),'utf8'));
const out={generated_at:new Date().toISOString(),catalog_public_total:rows.length,countries:{}};
for(const country of ['USA','Japan']){
 const patient={species:'Dog',country,cancer:'Cancer — any type',diagnosis_status:"I don't know",age_known:false,weight_known:false,prefs:new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug']),approach:'',zip_code:''};
 const matches=rows.map(t=>window.__MATCHER_TEST__.matchTrial(t,patient)).filter(Boolean),titles=matches.map(m=>m.trial.title).sort(),s=JSON.stringify(titles);let a=2166136261,b=5381;
 for(let i=0;i<s.length;i++){a=Math.imul(a^s.charCodeAt(i),16777619)>>>0;b=(Math.imul(b,33)^s.charCodeAt(i))>>>0;}
 out.countries[country]={count:matches.length,ids:matches.map(m=>m.trial.id).sort(),titles,title_set_checksum:[a,b,s.length]};
}
fs.writeFileSync(path.join(__dirname,'expected-live-search.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(Object.fromEntries(Object.entries(out.countries).map(([k,v])=>[k,{count:v.count,title_set_checksum:v.title_set_checksum}]))));
