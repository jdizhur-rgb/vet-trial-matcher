// Execute the generated finder script and exercise country/state/ZIP transitions.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');
const root = path.resolve(__dirname, '..');
const file = process.argv[2] || path.join(root, 'seo/site/matcher/centers/index.html');
const html = fs.readFileSync(file, 'utf8');
const records = JSON.parse(fs.readFileSync(path.join(root, 'data/oncology_centers.json'))).centers;
const cards = [...html.matchAll(/<article class="p-card"([^>]+)>([\s\S]*?)<\/article>/g)].map(m => {
  const dataset = Object.fromEntries([...m[1].matchAll(/data-([a-z-]+)="([^"]*)"/g)].map(a => [a[1], a[2]]));
  const distance = {hidden: true, textContent: ''};
  return {dataset, hidden: false, distance, querySelector: () => distance};
});
const countrySelect = html.match(/<select id="country"[^>]*>([\s\S]*?)<\/select>/);
assert(countrySelect, 'Country selector must be visible and labelled');
assert(html.includes('id="country" aria-label="Filter by country"'));
const options = [...countrySelect[1].matchAll(/<option value="([^"]*)">/g)].map(m => m[1]);
assert.deepEqual(options.filter(Boolean).sort(), [...new Set(records.map(c => c.country))].sort());
assert(options.includes('Germany'));
assert(html.includes('<input id="zip" hidden disabled'));
assert(html.includes('<select id="state" hidden disabled'));
assert(html.includes('.portal [hidden]{display:none!important}'));
assert(!html.includes('<<<<<<<'));
const elements = Object.fromEntries(['country','q','zip','svc','state','cards','n','status','international','intl-cards','intl-n'].map(id => [id, {
  value: '', hidden: false, disabled: false, textContent: '', options: [], handlers: {},
  addEventListener(type, fn) { this.handlers[type] = fn; },
  appendChild() {},
}]));
let resolveZip;
let fetchCount = 0;
const context = vm.createContext({
  document: {querySelector: s => elements[s.slice(1)], querySelectorAll: () => cards},
  URLSearchParams, location: {search: ''},
  fetch: () => { fetchCount++; return new Promise(resolve => { resolveZip = resolve; }); },
});
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('async function zipFilter'));
assert(script);
vm.runInContext(script, context);
const visible = () => cards.filter(c => !c.hidden);
function selectCountry(country) {
  elements.country.value = country;
  elements.country.handlers.change();
}
function assertCountry(country) {
  const expected = records.filter(c => !country || c.country === country).length;
  assert.equal(visible().length, expected, country || 'All countries');
  assert.equal(+elements.n.textContent, expected);
  assert(visible().every(c => !country || c.dataset.country === country));
  assert.equal(elements.zip.hidden, country !== 'USA');
  assert.equal(elements.state.hidden, country !== 'USA');
  assert.equal(elements.zip.disabled, country !== 'USA');
  assert.equal(elements.state.disabled, country !== 'USA');
}
(async () => {
  assertCountry('');
  for (const country of options.filter(Boolean)) { selectCountry(country); assertCountry(country); }
  selectCountry('Germany');
  const germanCount = visible().length;
  assert(germanCount > 0, 'Germany must never become a false zero');
  elements.svc.value = 'chemotherapy';
  elements.svc.handlers.change();
  const chemo = cards.filter(c => c.dataset.country === 'Germany' && c.dataset.filters.split('|').includes('chemotherapy'));
  assert(chemo.length > 0);
  assert.deepEqual(visible(), chemo);
  elements.q.value = 'zzzz-no-such-hospital';
  elements.q.handlers.input();
  assert.equal(visible().length, 0);
  elements.q.value = '';
  elements.svc.value = '';
  elements.q.handlers.input();
  assert.equal(visible().length, germanCount);
  selectCountry('USA');
  elements.state.value = 'WA';
  elements.state.handlers.change();
  assert(visible().length > 0);
  assert(visible().every(c => c.dataset.country === 'USA' && c.dataset.region === 'WA'));
  elements.zip.value = '98516';
  const pending = vm.runInContext('zipFilter(zip.value,seq)', context);
  assert.equal(fetchCount, 1);
  selectCountry('Germany');
  assert.equal(elements.state.value, '');
  assert.equal(elements.zip.value, '');
  assertCountry('Germany');
  resolveZip({ok: true, json: async () => ({places: [{latitude: '47.1', longitude: '-122.8', 'place name': 'Lacey', 'state abbreviation': 'WA'}]})});
  await pending;
  assertCountry('Germany');
  assert(visible().every(c => c.distance.hidden), 'Stale ZIP results must not overwrite Germany');
  selectCountry('USA');
  elements.state.value = 'WA';
  await vm.runInContext("zipFilter('98516',seq)", context);
  assert(visible().length > 0);
  assert(visible().every(c => c.dataset.country === 'USA' && c.dataset.region === 'WA'));
  assert(visible().filter(c => c.dataset.lat === '').every(c => c.distance.hidden));
  selectCountry('');
  assertCountry('');
  console.log('ONCOLOGY_COUNTRY_FILTER_OK', options.length - 1, 'countries;', germanCount, 'German locations; combined filters, state reset, stale ZIP suppression');
})().catch(e => { console.error(e); process.exitCode = 1; });
