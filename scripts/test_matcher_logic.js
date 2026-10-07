#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
global.window = {};
global.document = {querySelector: () => null, querySelectorAll: () => []};
require(path.join(root, 'seo/static/matcher/matcher.js'));

const rows = JSON.parse(
  fs.readFileSync(path.join(root, 'seo/static/matcher/trials.json'), 'utf8')
);
const matcher = window.__MATCHER_TEST__;
if (!matcher) throw new Error('Matcher test API is unavailable');

const matcherHtml = fs.readFileSync(path.join(root, 'seo/static/matcher/index.html'), 'utf8');
if (!matcherHtml.includes('<option value="Japan">Japan</option>')) {
  throw new Error('Matcher country selector is missing Japan');
}

const UNKNOWN = "I don't know";
function patient(overrides = {}) {
  return {
    species: 'Dog',
    country: 'USA',
    cancer: 'Mast cell tumor',
    diagnosis_status: 'Confirmed by pathology/cytology',
    tumor_status: 'Tumor still present / measurable',
    metastasis: 'No known metastases',
    localized: 'Yes',
    age_known: true,
    age: 8,
    weight_known: true,
    weight_lb: 55,
    prefs: new Set(['Surgery', 'Radiation', 'Chemotherapy', 'Immunotherapy', 'Targeted therapy', 'Experimental drug']),
    surgery: 'No',
    radiation: 'Never',
    chemo: 'Never',
    immunotherapy_history: 'Never',
    steroids: 'Never',
    immunosuppressive: 'No',
    standard_therapy_unavailable: UNKNOWN,
    large_inoperable_or_rt_preferred: UNKNOWN,
    surgery_or_rt_not_possible: UNKNOWN,
    ct_and_current_biopsy: UNKNOWN,
    prior_procedure: UNKNOWN,
    lymphoma_response: UNKNOWN,
    leukemia_status: UNKNOWN,
    radiation_affordability: UNKNOWN,
    sex: UNKNOWN,
    ...overrides,
  };
}

const matches = p => rows.map(row => matcher.matchTrial(row, p)).filter(Boolean);
const mct = matches(patient());
if (mct.length !== 4) {
  throw new Error(`Mast-cell regression expected 4 confirmed-current matches, got ${mct.length}`);
}

if (rows.some(row => row.id === 'uf-mct')) {
  throw new Error('UF toceranib biomarker study must remain outside treatment matching');
}
const boxerGliomaId = 'uf-boxer-glioma-autogenic-vaccine';
for (const species of ['Dog', 'Cat']) {
  const found = matches(patient({species, cancer:'Brain tumor'})).some(row => row.trial.id === boxerGliomaId);
  if (found !== (species === 'Dog')) throw new Error('UF Boxer glioma vaccine has incorrect species/cancer matching');
}
const sineId = 'anivive-sine-osa-carboplatin';
for (const [surgery, chemo, expected] of [['No','Never',false], ['Yes','Never',true], ['Yes','Previously received',false]]) {
  const found = matches(patient({cancer:'Osteosarcoma', surgery, chemo, tumor_status:'Completely removed — clean margins'})).some(row => row.trial.id === sineId);
  if (found !== expected) throw new Error('Cornell SINE must require amputation and exclude previous chemotherapy');
}

const goldId = 'barc-gold-nanoparticle-photothermal-2026';
const gold = rows.filter(row => row.id === goldId);
if (gold.length !== 1 || gold[0].sites[0]?.state !== 'WA' || gold[0].sites[0]?.city !== 'Edmonds') {
  throw new Error('BARC gold trial must be one record at the Edmonds, Washington site');
}
for (const cancer of ['Mast cell tumor', 'Soft tissue sarcoma', 'Oral melanoma', 'Melanoma — other']) {
  if (!matches(patient({species: 'Dog', cancer})).some(row => row.trial.id === goldId)) {
    throw new Error(`BARC gold did not match its canine ${cancer} cohort`);
  }
}
for (const cancer of ['Oral squamous cell carcinoma', 'Mast cell tumor', 'Soft tissue sarcoma', 'Squamous cell carcinoma — other', 'Other sarcoma']) {
  if (!matches(patient({species: 'Cat', cancer})).some(row => row.trial.id === goldId)) {
    throw new Error(`BARC gold did not match its feline ${cancer} cohort`);
  }
}
for (const [species, cancer] of [['Dog','Oral squamous cell carcinoma'],['Cat','Oral melanoma'],['Cat','Melanoma — other']]) {
  if (matches(patient({species,cancer})).some(row => row.trial.id === goldId)) {
    throw new Error(`BARC gold incorrectly crossed species for ${species}/${cancer}`);
  }
}
if (matches(patient({species:'Dog',cancer:'Mast cell tumor',country:'Switzerland'})).some(row => row.trial.id === goldId)) {
  throw new Error('BARC gold appeared outside the USA');
}
for (const [species,slug,expected] of [
  ['dogs','oral-melanoma',true],
  ['cats','oral-melanoma',false],
  ['dogs','oral-squamous-cell-carcinoma',false],
  ['cats','oral-squamous-cell-carcinoma',true],
]) {
  const page = fs.readFileSync(path.join(root,'seo/site/north-america',species,slug,'index.html'),'utf8');
  if (page.includes(gold[0].title) !== expected) {
    throw new Error(`BARC gold has an incorrect ${species}/${slug} cancer-page listing`);
  }
}

const yasha = matches(patient({
  cancer: 'Histiocytic sarcoma',
  tumor_status: 'Completely removed — clean margins',
  surgery: 'Yes',
  chemo: 'Currently receiving',
  prefs: new Set(['Chemotherapy', 'Immunotherapy', 'Targeted therapy', 'Experimental drug']),
}));
if (yasha.length !== 0) {
  throw new Error(`Post-surgery HS regression expected 0 matches, got ${yasha.length}`);
}

const mammary = matches(patient({
  cancer: 'Mammary carcinoma',
  sex: 'Female',
  weight_lb: 45,
}));
if (!mammary.some(row => row.trial.id === 'ncsu-mammary-inspire')) {
  throw new Error('USA/Dog/Mammary regression did not return ncsu-mammary-inspire');
}
if (mammary.some(row => row.trial.id === 'ncsu-liver-inspire')) {
  throw new Error('USA/Dog/Mammary regression incorrectly returned ncsu-liver-inspire');
}

const osteosarcoma = matches(patient({cancer: 'Osteosarcoma'}));
const ufOsaIds = ['uf-osa-vaccine', 'uf-osa-mrna'];
const ufOsaRecords = rows.filter(row => row.center === 'University of Florida' && row.species === 'Dog' && row.cancers.includes('Osteosarcoma'));
if (JSON.stringify(ufOsaRecords.map(row => row.id).sort()) !== JSON.stringify([...ufOsaIds].sort()) ||
    ufOsaRecords.some(row => row.sites?.[0]?.state !== 'FL')) {
  throw new Error(`USA/Florida/Dog/Osteosarcoma expected exactly two distinct UF protocols: ${ufOsaRecords.map(row => row.id).join(', ')}`);
}
const ufPreAmputation = matches(patient({cancer: 'Osteosarcoma'})).filter(row => ufOsaIds.includes(row.trial.id));
if (JSON.stringify(ufPreAmputation.map(row => row.trial.id).sort()) !== JSON.stringify([...ufOsaIds].sort())) {
  throw new Error('Florida osteosarcoma prescreening did not return both UF protocols');
}
const ufPostAmputation = matches(patient({cancer: 'Osteosarcoma', surgery: 'Yes', prior_procedure: 'Amputation', tumor_status: 'No evidence of disease (NED)'}));
if (!ufPostAmputation.some(row => row.trial.id === 'uf-osa-vaccine') ||
    ufPostAmputation.some(row => row.trial.id === 'uf-osa-mrna')) {
  throw new Error('UF post-amputation chemotherapy/vaccine protocol was conflated with radiation/RNA protocol');
}
const ufNoRadiation = matches(patient({cancer: 'Osteosarcoma', radiation_affordability: 'Would not consider radiation'}));
if (!ufNoRadiation.some(row => row.trial.id === 'uf-osa-vaccine') ||
    ufNoRadiation.some(row => row.trial.id === 'uf-osa-mrna')) {
  throw new Error('UF RNA protocol must require radiation; separate post-amputation protocol must remain');
}
if (!osteosarcoma.some(row => row.trial.id === 'wisc-osa-flash-radiotherapy')) {
  throw new Error('USA/Dog/Osteosarcoma regression did not return Wisconsin FLASH radiotherapy');
}
if (osteosarcoma.some(row => row.trial.id === 'vt-osa-histotripsy')) {
  throw new Error('Closed Virginia Tech histotripsy cohort remained in treatment matching');
}
if (osteosarcoma.some(row => row.trial.id === 'vt-osa-standard')) {
  throw new Error('Virginia Tech observational control appeared in treatment matching');
}

const auOsteosarcoma = matches(patient({country: 'Australia', cancer: 'Osteosarcoma'}));
const auIds = new Set(auOsteosarcoma.map(row => row.trial.id));
for (const id of ['au-uq-appendicular-osteosarcoma-vaccine']) {
  if (!auIds.has(id)) throw new Error(`Australia/Dog/Osteosarcoma did not return ${id}`);
}
if (auIds.has('au-gamgee-personalized-mrna-vaccine')) {
  throw new Error('Gamgee mast-cell-only trial incorrectly matched osteosarcoma');
}
const auMct = matches(patient({country: 'Australia', cancer: 'Mast cell tumor'}));
if (!auMct.some(row => row.trial.id === 'au-gamgee-personalized-mrna-vaccine')) {
  throw new Error('Australia/Dog/Mast cell tumor omitted the confirmed-current Gamgee trial');
}
const auBroad = matches(patient({country: 'Australia', cancer: 'Cancer — any type'}));
if (!auBroad.some(row => row.trial.id === 'au-melbourne-hsa-autologous-vaccine-multicenter')) {
  throw new Error('Australia/Dog/Any cancer type omitted the Melbourne haemangiosarcoma trial');
}
const auHsa = matches(patient({country: 'Australia', cancer: 'Hemangiosarcoma', surgery: 'Yes', tumor_status: 'Completely removed — clean margins'}));
if (!auHsa.some(row => row.trial.id === 'au-melbourne-hsa-autologous-vaccine-multicenter')) {
  throw new Error('Australia/Dog/Hemangiosarcoma did not return the MediPaws site');
}
if (matches(patient({country: 'Australia', cancer: 'Hemangiosarcoma', metastasis: 'Confirmed metastases', surgery: 'Yes'})).some(row => row.trial.id === 'au-melbourne-hsa-autologous-vaccine-multicenter')) {
  throw new Error('Melbourne nonmetastatic HSA protocol matched confirmed metastasis');
}
if (matches(patient({country: 'Australia', species: 'Cat', cancer: 'Osteosarcoma'})).length !== 0) {
  throw new Error('Australia cat search returned a dog-only trial');
}
if (matches(patient({country: 'Australia', cancer: 'Osteosarcoma', metastasis: 'Confirmed metastases'})).some(row => row.trial.id === 'au-uq-appendicular-osteosarcoma-vaccine')) {
  throw new Error('UQ nonmetastatic vaccine trial matched metastatic osteosarcoma');
}
if (osteosarcoma.some(row => row.trial.id.startsWith('au-'))) {
  throw new Error('Australia-only trial appeared in USA search');
}

const japanBroad = matches(patient({country: 'Japan', cancer: 'Cancer — any type'}));
if (!japanBroad.some(row => row.trial.id === 'jp-nvlu-survivin-peptide-vaccine-2026')) {
  throw new Error('Japan/Dog/Any cancer type omitted the NVLU survivin vaccine trial');
}

const bladder = matches(patient({cancer: 'Urothelial carcinoma'}));
if (rows.some(row => row.id === 'csu-ucc-icg-surgery') ||
    bladder.some(row => row.trial.id === 'csu-ucc-icg-surgery')) {
  throw new Error('CSU ICG diagnostic imaging protocol remained in USA/Dog/Bladder matching');
}
const purdueBladderIds = bladder
  .map(row => row.trial.id)
  .filter(id => id.startsWith('purdue-bladder') || id === 'purdue-ucc-aks701d');
if (JSON.stringify(purdueBladderIds) !== JSON.stringify(['purdue-bladder-pdl1-vinblastine-deracoxib'])) {
  throw new Error(`USA/Dog/Bladder expected only the current Purdue combination protocol, got ${purdueBladderIds.join(', ')}`);
}

const brain = matches(patient({cancer: 'Brain tumor'}));
const minnesotaBrainIds = brain
  .map(row => row.trial.id)
  .filter(id => id.startsWith('umn-'));
for (const expected of ['umn-glioma-zika-autologous-vax', 'umn-glioma-nanoparticle-gene']) {
  if (!minnesotaBrainIds.includes(expected)) {
    throw new Error(`USA/Dog/Brain Tumor did not return ${expected}`);
  }
}
if (minnesotaBrainIds.includes('umn-canine-brain-tumor-program')) {
  throw new Error('Minnesota program umbrella remained in treatment matching');
}

const scc = matches(patient({cancer: 'Squamous cell carcinoma'}));
const barcSccId = 'barc-scc-intratumoral-carboplatin-2026';
const barcScc = rows.filter(row => row.id === barcSccId);
if (barcScc.length !== 1 || barcScc[0].sites?.[0]?.city !== 'Edmonds' || barcScc[0].sites?.[0]?.state !== 'WA') {
  throw new Error('BARC SCC must be one current Edmonds, Washington opportunity');
}
for (const cancer of ['Squamous cell carcinoma', 'Squamous cell carcinoma — other']) {
  if (!matches(patient({species:'Dog',country:'USA',cancer})).some(row => row.trial.id === barcSccId)) {
    throw new Error(`BARC SCC did not match USA/Washington Dog/${cancer}`);
  }
}
for (const overrides of [
  {species:'Cat',cancer:'Squamous cell carcinoma — other'},
  {country:'Switzerland',cancer:'Squamous cell carcinoma — other'},
  {cancer:'Oral squamous cell carcinoma'},
  {cancer:'Squamous cell carcinoma — other',metastasis:'Confirmed metastases'},
  {cancer:'Squamous cell carcinoma — other',chemo:'Previously received'},
  {cancer:'Squamous cell carcinoma — other',immunotherapy_history:'Previously received'},
  {cancer:'Squamous cell carcinoma — other',radiation:'Previously received'},
]) {
  if (matches(patient(overrides)).some(row => row.trial.id === barcSccId)) {
    throw new Error(`BARC SCC falsely matched ${JSON.stringify(overrides)}`);
  }
}
if (!matches(patient({species:'Dog',country:'USA',cancer:'Cancer — any type'})).some(row => row.trial.id === barcSccId)) {
  throw new Error('BARC SCC missing from USA/Dog/Any cancer browse');
}
if (scc.some(row => row.trial.id === 'lsu-scc-intratumoral-chemo')) {
  throw new Error('Unresolved LSU intratumoral SCC protocol remained in USA/Dog/SCC matching');
}
if (scc.some(row => row.trial.id === goldId)) {
  throw new Error('BARC gold trial matched canine SCC, a feline-only cohort');
}

const medvetVaccine = rows.find(row => row.id === 'medvet-egfr-her2-vaccine-2026');
if (!medvetVaccine?.sites?.some(site => site.state === 'WA' && site.city === 'Edmonds')) {
  throw new Error('Existing EGFR/HER2 trial is missing its BARC Edmonds site');
}
if (!medvetVaccine.sites.find(site => site.city === 'Edmonds')?.notes?.includes('records review')) {
  throw new Error('BARC-specific EGFR screening details are missing from its site');
}
const egfrActiveCities = new Set(medvetVaccine.sites.map(site => site.city));
for (const city of ['Ventura','Edmonds','Pullman','Salt Lake City','Cleveland','McMurray','Fairfax','Phoenix','Stamford']) {
  if (!egfrActiveCities.has(city)) throw new Error(`EGFR/HER2 active site missing: ${city}`);
}
for (const city of ['Chicago','Richmond','Columbia']) {
  if (egfrActiveCities.has(city)) throw new Error(`EGFR/HER2 inactive site remained active: ${city}`);
  if (!medvetVaccine.inactive_sites?.some(site => site.city === city && /not enrolling/i.test(site.status || ''))) {
    throw new Error(`EGFR/HER2 inactive site status missing: ${city}`);
  }
}
if (!medvetVaccine.sites.find(site => site.city === 'Stamford')?.source_url?.includes('vetcancerconcierge.com')) {
  throw new Error('EGFR/HER2 Stamford site lacks separate treatment-center confirmation');
}
const siteKey = site => [site.hospital || site.name || '', site.city || '', site.state || ''].join('|').toLowerCase();
for (const trial of [medvetVaccine, rows.find(row => row.id === 'leah-bcell-cart-2026')]) {
  const active = trial?.sites || [], inactive = trial?.inactive_sites || [];
  if (new Set(active.map(siteKey)).size !== active.length || new Set(inactive.map(siteKey)).size !== inactive.length) {
    throw new Error(`${trial?.id} contains duplicate site rows`);
  }
  if (active.some(site => new Set(inactive.map(siteKey)).has(siteKey(site)))) {
    throw new Error(`${trial?.id} lists the same site as active and inactive`);
  }
}
const leah = rows.find(row => row.id === 'leah-bcell-cart-2026');
if (!leah || leah.sites.length !== 1 || leah.sites[0].state !== 'OH' ||
    !['MN', 'MO'].every(state => leah.inactive_sites?.some(
      site => site.state === state && /hold/i.test(site.status || '')
    ))) {
  throw new Error('LEAH site reconciliation must retain sponsor-listed Ohio and exclude paused Minnesota/Missouri from active sites');
}
for (const cancer of ['Osteosarcoma','Hemangiosarcoma','Urothelial carcinoma']) {
  if (!matches(patient({cancer})).some(row => row.trial.id === medvetVaccine.id)) {
    throw new Error(`EGFR/HER2 vaccine did not match its USA/Washington ${cancer} cohort`);
  }
}
for (const cancer of ['Pulmonary carcinoma','Mast cell tumor']) {
  if (matches(patient({cancer})).some(row => row.trial.id === medvetVaccine.id)) {
    throw new Error(`BARC-only EGFR indication leaked into the shared ${cancer} cohort`);
  }
}
if (rows.some(row => row.id === 'penn-bendamustine-relapsed-lymphoma')) {
  throw new Error('Unconfirmed Penn bendamustine enrollment remained in matcher data');
}
const pennHsId = 'penn-atherton-steap1-car-t-hs';
const pennHs = rows.filter(row => row.id === pennHsId);
if (pennHs.length !== 1 || pennHs[0].sites?.[0]?.address !== '3900 Spruce Street, Philadelphia, PA 19104') {
  throw new Error('Penn Atherton HS CAR-T is missing or has an incorrect site');
}
for (const cancer of ['Histiocytic sarcoma', 'Cancer — any type']) {
  if (!matches(patient({species:'Dog', country:'USA', cancer})).some(row => row.trial.id === pennHsId)) {
    throw new Error(`Penn Atherton CAR-T missing from USA/Dog/${cancer}`);
  }
}
for (const overrides of [
  {species:'Cat', cancer:'Histiocytic sarcoma'},
  {country:'Canada', cancer:'Histiocytic sarcoma'},
  {cancer:'Lymphoma'},
  {cancer:'Histiocytic sarcoma', tumor_status:'Removed — incomplete/dirty margins'},
  {cancer:'Histiocytic sarcoma', tumor_status:'No evidence of disease (NED)'},
  {cancer:'Histiocytic sarcoma', chemo:'Currently receiving'},
]) {
  if (matches(patient(overrides)).some(row => row.trial.id === pennHsId)) {
    throw new Error(`Penn Atherton CAR-T falsely matched ${JSON.stringify(overrides)}`);
  }
}
if (!matches(patient({cancer:'Histiocytic sarcoma', tumor_status:'Local recurrence', chemo:'Previously received'})).some(row => row.trial.id === pennHsId)) {
  throw new Error('Penn Atherton CAR-T missing for measurable recurrence after prior chemotherapy');
}
for (const species of ['Dog','Cat']) {
  if (matches(patient({species,cancer:'Hemangiosarcoma'})).some(row => row.trial.id.includes('paccal'))) {
    throw new Error(`${species} Paccal falsely appears as recruiting`);
  }
}
for (const cancer of ['Cancer — any type','Hemangiosarcoma']) {
  if (matches(patient({country:'Switzerland',species:'Dog',cancer})).some(row => row.trial.id === 'ch-zurich-oral-vinorelbine-phase1-2026')) {
    throw new Error(`Single-dose Zurich Phase I falsely matches Switzerland/Dog/${cancer}`);
  }
}

const oralScc = matches(patient({cancer: 'Oral squamous cell carcinoma'}));
if (!oralScc.some(row => row.trial.id === 'ucd-oral-margin')) {
  throw new Error('UC Davis PDL1-IRDye800 oral-cancer protocol is missing from matching');
}

const liver = matches(patient({cancer: 'Hepatocellular carcinoma'}));
if (!liver.some(row => row.trial.id === 'ucd-liver-tae-tace')) {
  throw new Error('Current UC Davis liver TAE/TACE protocol is missing from matching');
}
if (liver.some(row => row.trial.id === 'ucd-liver-rna')) {
  throw new Error('Unconfirmed UC Davis liver RNA protocol remained in matching');
}

const prostate = matches(patient({cancer: 'Prostate cancer'}));
if (prostate.some(row => row.trial.id === 'ucd-prostate-liquid-treatment')) {
  throw new Error('UC Davis blood/urine sampling protocol appeared as a treatment match');
}

const nasal = matches(patient({cancer: 'Nasal tumor / nasal cancer'}));
for (const expected of ['ucd-nasal-chemo-radiation', 'ucd-nasal-tae']) {
  if (!nasal.some(row => row.trial.id === expected)) {
    throw new Error(`USA/Dog/Nasal Tumor did not return ${expected}`);
  }
}

const glioma = matches(patient({cancer: 'Glioma'}));
if (!glioma.some(row => row.trial.id === 'ucd-care-canine-glioma')) {
  throw new Error('UC Davis CARE glioma protocol is missing from brain-tumor matching');
}

if (rows.some(row => row.id === 'bluepearl-hsa-paccal')) {
  throw new Error('Completed BluePearl Paccal Vet pilot remained in treatment matching');
}

const cotc033 = rows.find(row => row.id === 'csu-cotc033-vaccine-immunity');
if (!cotc033 || !cotc033.sites.some(site => site.state === 'MO')) {
  throw new Error('COTC033 matcher record is missing the confirmed Missouri site');
}

const blocked = {
  id: 'blocked-test',
  species: 'Dog',
  country: 'USA',
  cancers: ['Mast cell tumor'],
  status: 'Enrollment closed',
  status_confidence: 'confirmed_current',
  study_type: 'treatment',
};

// Current primary protocols checked on 2026-10-06: prevent disease, species,
// treatment-response and procedure requirements from leaking into matching.
const hasTrial = (id, overrides) => matches(patient(overrides)).some(row => row.trial.id === id);
for (const cancer of ['Soft tissue sarcoma', 'Spindle cell sarcoma']) {
  if (hasTrial('ucd-oral-margin', {cancer})) throw new Error('UC Davis oral SCC/melanoma protocol falsely matches sarcoma');
}
const csuStsId = 'csu-sarcoma-engineered-tcells';
if (!hasTrial(csuStsId, {cancer:'Soft tissue sarcoma'})) throw new Error('CSU current STS cohort missing');
for (const overrides of [{cancer:'Osteosarcoma'}, {cancer:'Soft tissue sarcoma', weight_lb:20}, {cancer:'Soft tissue sarcoma', immunotherapy_history:'Previously received'}]) {
  if (hasTrial(csuStsId, overrides)) throw new Error(`CSU STS falsely matched ${JSON.stringify(overrides)}`);
}
const hbrtId = 'wisc-lymphoma-half-body-rt-chop';
for (const response of ['Partial response','Complete remission']) {
  if (!hasTrial(hbrtId, {cancer:'Lymphoma', chemo:'Currently receiving', lymphoma_response:response})) throw new Error(`UW HBRT missing ${response}`);
}
for (const response of ['Newly diagnosed / untreated','Progression during treatment','First relapse after remission']) {
  if (hasTrial(hbrtId, {cancer:'Lymphoma', chemo:'Currently receiving', lymphoma_response:response})) throw new Error(`UW HBRT falsely matched ${response}`);
}
const unknownResponse = matcher.matchTrial(rows.find(t => t.id === hbrtId), patient({cancer:'Lymphoma', chemo:'Currently receiving'}));
if (!unknownResponse?.unknown.includes('required lymphoma response to treatment')) throw new Error('UW HBRT unknown response must require prescreening');
if (hasTrial('wisc-osa-flash-radiotherapy', {cancer:'Osteosarcoma', prefs:new Set(['Radiation'])})) throw new Error('UW FLASH must respect current consent amputation requirement');
const gifuId = 'jp-gifu-feline-oscc-radiotherapy-lavurchin';
if (!hasTrial(gifuId, {species:'Cat', country:'Japan', cancer:'Oral squamous cell carcinoma'})) throw new Error('Gifu feline OSCC trial missing');
for (const overrides of [{species:'Dog', country:'Japan', cancer:'Oral squamous cell carcinoma'}, {species:'Cat', country:'Japan', cancer:'Oral squamous cell carcinoma', prefs:new Set(['Immunotherapy'])}]) {
  if (hasTrial(gifuId, overrides)) throw new Error('Gifu species/radiation requirement leaked');
}
const hokkaidoId = 'jp-hokkaido-canine-oral-melanoma-anti-pdl1';
if (!hasTrial(hokkaidoId, {country:'Japan', cancer:'Oral melanoma', metastasis:'Confirmed metastases'})) throw new Error('Hokkaido metastatic oral melanoma trial missing');
if (hasTrial(hokkaidoId, {country:'Japan', cancer:'Oral melanoma'})) throw new Error('Hokkaido must not match dogs without known metastases');
for (const id of ['ucd-care-canine-glioma','ucd-prism-canine-glioma']) {
  if (!hasTrial(id, {cancer:'Glioma'})) throw new Error(`UC Davis radiation pathway missing ${id}`);
  for (const overrides of [{cancer:'Glioma', prefs:new Set(['Chemotherapy'])}, {cancer:'Glioma', radiation_affordability:'Would not consider radiation'}]) {
    if (hasTrial(id, overrides)) throw new Error(`UC Davis radiation requirement leaked for ${id}`);
  }
}
if (matcher.matchTrial(blocked, patient()) !== null) {
  throw new Error('Closed enrollment record was not blocked');
}

console.log(`MATCHER_LOGIC_OK trials=${rows.length} mct=${mct.length} yasha=${yasha.length} mammary=${mammary.length} osteosarcoma=${osteosarcoma.length} bladder=${bladder.length} brain=${brain.length}`);
