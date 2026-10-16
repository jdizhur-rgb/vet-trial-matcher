// Regression: approved identities survive rebuilding, and mobile regions never
// acquire fabricated ZIP distances from mailbox/zero coordinates.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const path = require('path');
const root = path.resolve(__dirname, '..');
const centers = JSON.parse(fs.readFileSync(path.join(root, 'data/oncology_centers.json'))).centers;
const one = name => {
  const found = centers.filter(c => c.name === name);
  assert.equal(found.length, 1, name);
  return found[0];
};
assert.equal(one('Four Seasons Veterinary Specialists').street, '4120 Clydesdale Parkway');
assert.equal(one('Four Seasons Veterinary Specialists').postal_code, '80538');
assert.equal(one('Melinda Lou Upton, DVM, PLLC').street, '4055 S. 102nd E. Ave.');
assert.equal(one('Guardian Veterinary Specialists').oncologists.length, 2);
assert(one('VCA Deer Creek Animal Hospital').availability_note.includes('Fridays'));
for (const name of ['Ivaoes', 'LAVet Hospital', 'Dr. Sue Cancer Vet PLLC', 'colorado veterinary oncology', 'Four Seasons Veterinary Specialist']) {
  assert(!centers.some(c => c.name === name), name);
}
assert.deepEqual(one('Kentuckiana Animal Clinic').services, ['Oncology referral']);
assert.deepEqual(one('Hillcrest Animal Hospital').services, ['Local oncology care']);
assert(one('Long Island Veterinary Specialists').services.includes('Surgical oncology'));
assert(!one('Long Island Veterinary Specialists').services.includes('Chemotherapy'));
assert(one('Integrative Veterinary Oncology, PC').services.includes('Chemotherapy'));
assert(!one('Integrative Veterinary Oncology, PC').availability_note.includes('not accepting'));
for (const name of ['Hope Veterinary Oncology Services', 'Mobile Veterinary Cancer Care']) {
  const c = one(name);
  assert.equal(c.location_type, 'mobile');
  assert.equal(c.latitude, null);
  assert.equal(c.longitude, null);
  assert.equal(c.postal_code, '');
  assert.equal(c.street, '');
}

const html = fs.readFileSync(path.join(root, 'seo/site/matcher/centers/index.html'), 'utf8');
const cards = [...html.matchAll(/<article class="p-card"([^>]+)>([\s\S]*?)<\/article>/g)].map(m => {
  const attrs = Object.fromEntries([...m[1].matchAll(/data-([a-z-]+)="([^"]*)"/g)].map(a => [a[1], a[2]]));
  const distance = {hidden: true, textContent: ''};
  return {dataset: attrs, hidden: false, body: m[2], querySelector: () => distance, distance};
});
assert.equal(cards.length, centers.length);
const elements = Object.fromEntries(['country','q','zip','svc','state','cards','n','status','international','intl-cards','intl-n'].map(id => [id, {value:'', hidden:false, textContent:'', options:[], children:[], addEventListener(){}, appendChild(c){this.children.push(c);}}]));
const sandbox = {
  document: {querySelector: s => elements[s.slice(1)], querySelectorAll: () => cards},
  URLSearchParams, location: {search:''},
  fetch: async () => ({ok:true, json:async () => ({places:[{latitude:'47.1',longitude:'-122.8','place name':'Lacey','state abbreviation':'WA'}]})})
};
const context = vm.createContext(sandbox);
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('async function zipFilter'));
assert(script);
vm.runInContext(script, context);
(async () => {
  elements.country.value = 'USA';
  elements.state.value = 'WA';
  await vm.runInContext("zipFilter('98516',seq)", context);
  const mobile = cards.filter(c => c.dataset.region === 'WA' && c.dataset.lat === '');
  assert.equal(mobile.length, 2);
  assert(mobile.every(c => !c.hidden && c.distance.hidden && !c.distance.textContent));
  assert(cards.filter(c => c.dataset.region !== 'WA').every(c => c.hidden));
  assert(cards.filter(c => !c.hidden && c.dataset.lat !== '').every(c => !c.distance.hidden));
  assert.equal(+elements.n.textContent, cards.filter(c => !c.hidden).length);
  console.log('A01_CARE_REGRESSION_OK identities, service flags, WA ZIP/state sorting, mobile distance suppression');
})().catch(e => {console.error(e);process.exitCode=1;});
