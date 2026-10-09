'use strict';
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../seo/static/matcher/matcher.js'), 'utf8');
const rows = JSON.parse(fs.readFileSync(path.join(__dirname, '../seo/static/matcher/trials.json'), 'utf8'));
async function test(country, fail = false) {
  let resolveFetch, rejectFetch;
  const response = new Promise((resolve, reject) => { resolveFetch = resolve; rejectFetch = reject; });
  const listeners = {}, result = {innerHTML: '', scrollIntoView() {}};
  const fields = {species:'Dog', country, cancer:'Cancer — any type', diagnosis_status:"I don't know", age:'', weight:'', weight_unit:'lb', approach:'', zip_code:''};
  const elements = Object.fromEntries(Object.entries(fields).map(([name,value]) => [name,{value,options:[{value}]}]));
  const dummy = {addEventListener(){}};
  const form = {elements, addEventListener(name,fn){listeners[name]=fn;}, querySelector(){return dummy;}, querySelectorAll(){return ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug'].map(value=>({value}));}, requestSubmit(){return listeners.submit({preventDefault(){}});}};
  const doc = {querySelector(selector){return selector==='#matcher-form'?form:selector==='#matcher-results'?result:dummy;}, querySelectorAll(){return [];}};
  vm.runInNewContext(source,{window:{location:{hash:'',search:''},MATCHER_DATA_URL:'./trials.json'},document:doc,FormData:class{entries(){return Object.entries(fields);}},URLSearchParams,fetch:()=>response,console});
  const submission = form.requestSubmit();
  await new Promise(resolve=>setImmediate(resolve));
  assert(!result.innerHTML.includes('No plausible matches'), `${country}: loading misreported as zero matches`);
  if(fail) rejectFetch(new Error('network unavailable'));
  else resolveFetch({ok:true,json:async()=>rows});
  await submission;
  await new Promise(resolve=>setImmediate(resolve));
  if(fail) assert(result.innerHTML.includes('catalog could not be loaded') && !result.innerHTML.includes('No plausible matches'));
  else {
    assert(result.innerHTML.includes('result-card'), `${country}: pending search never completed`);
    if(country==='Japan') assert(result.innerHTML.includes('Nihon University Animal Medical Center'));
    console.log(`${country}: ${((result.innerHTML.match(/class="result-card"/g))||[]).length} results after delayed load`);
  }
}
(async()=>{await test('Japan');await test('USA');await test('USA',true);console.log('Catalog-loading regression PASS');})().catch(e=>{console.error(e);process.exitCode=1;});
