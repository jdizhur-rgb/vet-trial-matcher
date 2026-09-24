#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
global.window = {};
global.document = {querySelector: () => null, querySelectorAll: () => []};
require(path.join(root, 'seo/static/matcher-preview/matcher.js'));

const rows = JSON.parse(
  fs.readFileSync(path.join(root, 'seo/static/matcher-preview/trials.json'), 'utf8')
);
const matcher = window.__MATCHER_TEST__;
if (!matcher) throw new Error('Matcher test API is unavailable');

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
if (!osteosarcoma.some(row => row.trial.id === 'wisc-osa-flash-radiotherapy')) {
  throw new Error('USA/Dog/Osteosarcoma regression did not return Wisconsin FLASH radiotherapy');
}
if (osteosarcoma.some(row => row.trial.id === 'vt-osa-histotripsy')) {
  throw new Error('Closed Virginia Tech histotripsy cohort remained in treatment matching');
}
if (osteosarcoma.some(row => row.trial.id === 'vt-osa-standard')) {
  throw new Error('Virginia Tech observational control appeared in treatment matching');
}

const bladder = matches(patient({cancer: 'Urothelial carcinoma'}));
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
if (scc.some(row => row.trial.id === 'lsu-scc-intratumoral-chemo')) {
  throw new Error('Unresolved LSU intratumoral SCC protocol remained in USA/Dog/SCC matching');
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
if (matcher.matchTrial(blocked, patient()) !== null) {
  throw new Error('Closed enrollment record was not blocked');
}

console.log(`MATCHER_LOGIC_OK trials=${rows.length} mct=${mct.length} yasha=${yasha.length} mammary=${mammary.length} osteosarcoma=${osteosarcoma.length} bladder=${bladder.length} brain=${brain.length}`);
