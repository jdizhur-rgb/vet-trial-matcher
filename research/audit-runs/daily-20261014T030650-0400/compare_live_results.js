const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const root=path.resolve(__dirname,'../../..');
global.window={};global.document={querySelector:()=>null,querySelectorAll:()=>[]};
require(path.join(root,'seo/static/matcher/matcher.js'));
const rows=JSON.parse(fs.readFileSync(path.join(root,'seo/static/matcher/trials.json'),'utf8'));
const observations=JSON.parse(fs.readFileSync(path.join(__dirname,'live-search-observations.json'),'utf8'));
const tests=[];
for(const country of ['USA','Japan']){
 const p={species:'Dog',country,cancer:'Cancer — any type',diagnosis_status:"I don't know",age_known:false,weight_known:false,prefs:new Set(['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug']),approach:'',zip_code:''};
 const matches=rows.map(x=>window.__MATCHER_TEST__.matchTrial(x,p)).filter(Boolean);
 const actual=observations[country];
 assert.deepStrictEqual([...actual.titles].sort(),matches.map(x=>x.trial.title).sort());
 assert.strictEqual(actual.count,matches.length);
 assert.strictEqual(actual.species,p.species);assert.strictEqual(actual.cancer,p.cancer);assert.strictEqual(actual.diagnosis,p.diagnosis_status);
 for(const k of ['age','weight','zip','approach'])assert.strictEqual(actual[k],'');
 assert(country==='USA'?actual.prefs.length===6&&actual.prefs.every(x=>x.checked):actual.prefs_all_checked);
 const titles=matches.map(x=>x.trial.title).sort().join('\n');
 tests.push({country,status:'PASS',expected_count:matches.length,rendered_count:actual.count,complete_title_set_equal:true,title_set_sha256:crypto.createHash('sha256').update(titles).digest('hex'),checked_at:observations.checked_at});
}
fs.writeFileSync(path.join(__dirname,'live-search-validation.json'),JSON.stringify({status:'PASS',release_main_sha:'0350ec621a783f87dcd814de6f099c2a059d8423',catalog_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'seo/static/matcher/trials.json'))).digest('hex'),tests},null,2)+'\n');
console.log(JSON.stringify(tests));
