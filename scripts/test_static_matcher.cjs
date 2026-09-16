const assert = require('assert');
const fs = require('fs');

global.window = {};
global.document = {querySelector: () => null, querySelectorAll: () => []};
require('../seo/matcher/matcher.js');

const engine = window.__MATCHER_TEST__;
const trials = JSON.parse(fs.readFileSync('seo/site/matcher/trials.json', 'utf8'));
const UNKNOWN = "I don't know";
const prefs = new Set(['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug']);

const base = {
  species:'Dog', sex:'Male — neutered', country:'USA',
  diagnosis_status:'Confirmed by pathology/cytology', cancer:'Mast cell tumor',
  unlisted_diagnosis:'', tumor_status:'Tumor still present / measurable',
  metastasis:'No known metastases', localized:'Yes', brain_present:UNKNOWN,
  lymphoma_type:UNKNOWN, lymphoma_response:UNKNOWN, leukemia_status:UNKNOWN,
  mct_grade:UNKNOWN, node_status:UNKNOWN, osa_location:UNKNOWN, hsa_site:UNKNOWN,
  standard_therapy_unavailable:UNKNOWN, large_inoperable_or_rt_preferred:UNKNOWN,
  surgery_or_rt_not_possible:UNKNOWN, ct_and_current_biopsy:UNKNOWN,
  surgery:'No', prior_procedure:'Other', chemo:'Never', immunotherapy_history:'Never',
  radiation:'Never', steroids:UNKNOWN, immunosuppressive:UNKNOWN,
  radiation_affordability:'Would consider radiation', age_known:true, age:8,
  weight_known:true, weight_lb:55, prefs
};

function matches(input) {
  return trials.map(t => engine.matchTrial(t, input)).filter(Boolean);
}

const yasha = {...base, cancer:'Histiocytic sarcoma', age:13, weight_lb:24.25,
  tumor_status:'Removed — incomplete/dirty margins', surgery:'Yes', chemo:'Currently receiving'};
assert.strictEqual(matches(yasha).length, 0, 'Yasha control case must not receive false hope');

const controls = [
  ['Mast cell tumor', 5],
  ['B-cell lymphoma', 9],
  ['Oral melanoma', 11],
  ['Soft tissue sarcoma', 15],
  ['Osteosarcoma', 20],
];
for (const [cancer, expected] of controls) {
  const input = {...base, cancer};
  if (cancer === 'B-cell lymphoma') input.lymphoma_response = 'Newly diagnosed / untreated';
  assert.strictEqual(matches(input).length, expected, `${cancer} parity count changed`);
}

for (const trial of trials) {
  assert.ok(['current','confirmed_current'].includes(trial.status_confidence));
  assert.ok(['treatment','other_treatment_access'].includes(trial.study_type || 'treatment'));
  assert.ok(!Object.hasOwn(trial, 'available_for_matching'), 'internal matching flag leaked');
}
console.log(`STATIC_MATCHER_OK trials=${trials.length} controls=${controls.length + 1}`);
