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
if (mct.length !== 5) {
  throw new Error(`Mast-cell regression expected 5 matches, got ${mct.length}`);
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

console.log(`MATCHER_LOGIC_OK trials=${rows.length} mct=${mct.length} yasha=${yasha.length}`);
