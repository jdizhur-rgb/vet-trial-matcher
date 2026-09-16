(() => {
  'use strict';

  const UNKNOWN = "I don't know";
  const CURRENT = new Set(['current', 'confirmed_current']);
  const LYMPHOMA = new Set(['B-cell lymphoma', 'T-cell lymphoma', 'Lymphoma — other']);
  const EUROPE = new Set(['UK','United Kingdom','France','Italy','Portugal','Switzerland','Netherlands','The Netherlands','Belgium','Sweden','Slovenia','Spain','Germany','Cyprus','Austria','Poland','Norway','Denmark','Finland','Ireland','Czech Republic','Czechia','Hungary','Greece','Romania','Croatia','Estonia','Latvia','Lithuania','Luxembourg','Iceland']);
  const ALIASES = {
    'B-cell lymphoma':['Lymphoma','Lymphoma — other'], 'T-cell lymphoma':['Lymphoma','Lymphoma — other','Enteropathy-associated T-cell lymphoma'],
    'Lymphoma — other':['Lymphoma','Gastrointestinal lymphoma','Large cell lymphoma'], 'Brain tumor / glioma':['Brain tumor','Glioma'],
    'Feline mammary carcinoma':['Mammary carcinoma','Mammary tumor'], 'Mammary carcinoma':['Mammary tumor'], 'Mammary tumor — other':['Mammary tumor'],
    'Urothelial / transitional cell carcinoma':['Urothelial carcinoma','Transitional cell carcinoma'],
    'Urothelial carcinoma':['Urothelial / transitional cell carcinoma','Transitional cell carcinoma','Bladder cancer'],
    'Thyroid tumor / carcinoma':['Thyroid carcinoma'], 'Thyroid carcinoma':['Thyroid tumor / carcinoma'],
    'Hepatocellular carcinoma':['Hepatic carcinoma'], 'Primary lung tumor':['Pulmonary carcinoma'],
    'Oral squamous cell carcinoma':['Feline oral SCC'], 'Squamous cell carcinoma — other':['Squamous cell carcinoma'],
    'Oral tumor — other':['Oral tumor'], 'Ocular melanoma / iris melanocytic tumor':['Ocular melanoma','Iris melanocytic tumor'],
    'Chemodectoma':['Aortic body tumor','Aortic body tumors','Heart-base tumor','Heart base tumor','Paraganglioma','Non-chromaffin paraganglioma']
  };
  const FAMILIES = {
    'Gastric / stomach cancer':['solid_tumor','carcinoma'], 'Colorectal / rectal cancer':['solid_tumor','carcinoma'],
    'Salivary gland cancer':['solid_tumor','carcinoma'], 'Esophageal cancer':['solid_tumor','carcinoma'],
    'Thymoma / thymic tumor':['solid_tumor'], 'Gastrointestinal stromal tumor (GIST)':['solid_tumor','sarcoma'],
    'Peripheral nerve sheath tumor':['solid_tumor','sarcoma','soft_tissue_sarcoma'], 'Leiomyosarcoma':['solid_tumor','sarcoma','soft_tissue_sarcoma'],
    'Fibrosarcoma':['solid_tumor','sarcoma','soft_tissue_sarcoma'], 'Liposarcoma':['solid_tumor','sarcoma','soft_tissue_sarcoma'],
    'Rhabdomyosarcoma':['solid_tumor','sarcoma','soft_tissue_sarcoma'], 'Chondrosarcoma':['solid_tumor','sarcoma'],
    'Nasal tumor / nasal cancer':['solid_tumor','nasal_tumor'], 'Multiple myeloma / plasma cell cancer':['hematologic']
  };
  const BLOCKED = ['on hold','completed','closed enrollment','enrollment closed','closed for data review','suspended','past clinical study','not accepting','paused','not on current','do not match','coming soon','not yet independently confirmed','enrollment not confirmed','reconfirm before matching','previously active recruitment','sponsor page still lists study','current oncology archive listing','recent active trial; enrollment must be reconfirmed','patients needed; current enrollment should be reconfirmed','funded active-study evidence','current funded translational research'];
  const form = document.querySelector('#matcher-form');
  const results = document.querySelector('#matcher-results');
  let trials = [];

  const esc = value => String(value ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const value = name => form.elements[name]?.value ?? UNKNOWN;
  const checked = name => Boolean(form.elements[name]?.checked);
  const show = (selector, yes) => document.querySelectorAll(selector).forEach(el => { el.hidden = !yes; });
  const speciesMatches = (trialSpecies, selected) => (Array.isArray(trialSpecies) ? trialSpecies : String(trialSpecies || '').split('/')).map(x => String(x).trim()).includes(selected);
  const countryMatches = (trialCountry, selected) => selected === 'Europe — all countries' ? EUROPE.has(trialCountry) : trialCountry === selected;
  const uniq = items => [...new Set(items.map(String))];

  function diagnosisMatch(trial, diagnosis) {
    const cancers = new Set(trial.cancers || []);
    const exact = new Set([diagnosis, ...(ALIASES[diagnosis] || [])]);
    if (diagnosis === 'Spindle cell sarcoma') exact.add('Soft tissue sarcoma');
    if ([...exact].some(x => cancers.has(x))) return [true, false];
    const family = FAMILIES[diagnosis];
    if (!family) return [false, false];
    const broad = new Set(trial.broad_disease_families || []);
    if (broad.has('all_tumors') || cancers.has('Cancer — any type')) return [true, true];
    return [family.some(x => broad.has(x)), family.some(x => broad.has(x))];
  }

  function modalities(trial) {
    const text = ['title','intervention','notes'].map(k => trial[k] || '').join(' ').toLowerCase();
    const req = trial.requires || {}; const mods = new Set();
    const has = words => words.some(x => text.includes(x));
    if (req.planned_surgery || req.planned_amputation || req.planned_amputation_and_chemo || has(['surgery','surgical','mastectom','amputation'])) mods.add('Surgery');
    if (req.planned_radiation || has(['radiotherapy','radiation','sbrt','flash','lattice','radiosensiti','proton'])) mods.add('Radiation');
    if (req.planned_doxorubicin || req.planned_amputation_and_chemo || has(['chemotherapy','doxorubicin','carboplatin','lomustine','vinorelbine','toceranib','tigilanol','chemoembol'])) mods.add('Chemotherapy');
    if (has(['immunotherap','vaccine','car-t','car t','interleukin','il-2','checkpoint','pd-1','pd-l1','oncolytic','tlr agonist','bcg'])) mods.add('Immunotherapy');
    if (has(['targeted','toceranib','kinase inhibitor','adam-12','versican','antibody','radioimmunotherap','nanobody'])) mods.add('Targeted therapy');
    if (has(['phase i','phase 1','phase ii','phase 2','experimental','investigational','tigilanol','oxc-101','rimcazole','gcn2','oncofap','nebumet','cantrixil'])) mods.add('Experimental drug');
    return mods;
  }

  function patient() {
    const data = Object.fromEntries(new FormData(form).entries());
    data.age_known = checked('age_known'); data.weight_known = checked('weight_known');
    data.age = Number(value('age')); data.weight = Number(value('weight'));
    data.weight_lb = data.weight_known ? (value('weight_unit') === 'kg' ? data.weight * 2.2046226218 : data.weight) : null;
    data.prefs = new Set([...form.querySelectorAll('input[name="prefs"]:checked')].map(x => x.value));
    if (data.cancer === 'Brain tumor / glioma' && data.brain_present === 'Yes') data.tumor_status = 'Tumor still present / measurable';
    else if (data.cancer === 'Brain tumor / glioma' && data.brain_present === 'No visible tumor') data.tumor_status = 'No evidence of disease (NED)';
    if (LYMPHOMA.has(data.cancer) || data.cancer === 'Cutaneous epitheliotropic lymphoma') {
      if (['Newly diagnosed / untreated','Partial response','Progression during treatment','First relapse after remission','More than one relapse'].includes(data.lymphoma_response)) data.tumor_status = 'Tumor still present / measurable';
      else if (data.lymphoma_response === 'Complete remission') data.tumor_status = 'No evidence of disease (NED)';
    }
    if (data.cancer === 'Acute myeloid leukemia') {
      if (['Newly diagnosed / untreated','Relapsed','Refractory / progressive'].includes(data.leukemia_status)) data.tumor_status = 'Tumor still present / measurable';
      else if (data.leukemia_status === 'Responding to treatment / remission') data.tumor_status = 'No evidence of disease (NED)';
    }
    return data;
  }

  function limits(req) {
    return {
      minAge:req.min_age_years, maxAge:req.max_age_years,
      minLb:req.min_weight_lb ?? (req.min_weight_kg == null ? null : req.min_weight_kg * 2.2046226218),
      maxLb:req.max_weight_lb ?? (req.max_weight_kg == null ? null : req.max_weight_kg * 2.2046226218)
    };
  }

  function universalLimitPass(req, p) {
    const x = limits(req);
    if (x.minAge != null && p.age_known && p.age < x.minAge) return false;
    if (x.maxAge != null && p.age_known && p.age > x.maxAge) return false;
    if (x.minLb != null && p.weight_known && p.weight_lb < x.minLb) return false;
    if (x.maxLb != null && p.weight_known && p.weight_lb > x.maxLb) return false;
    return true;
  }

  function matchTrial(trial, p) {
    if (!CURRENT.has(trial.status_confidence) || !speciesMatches(trial.species, p.species) || !countryMatches(trial.country || 'USA', p.country)) return null;
    if (!['treatment','other_treatment_access'].includes(trial.study_type || 'treatment')) return null;
    if (BLOCKED.some(x => String(trial.status || '').toLowerCase().includes(x))) return null;
    const prefs = p.prefs; const mods = modalities(trial);
    if (prefs.size && mods.size && ![...mods].some(x => prefs.has(x))) return null;
    const unlisted = p.cancer === "My cancer type isn't listed";
    let broad = false;
    if (unlisted) {
      if (!(trial.broad_disease_families || []).includes('all_tumors') && !(trial.cancers || []).includes('Cancer — any type')) return null;
      if (!universalLimitPass(trial.requires || {}, p)) return null;
      const shown = String(p.unlisted_diagnosis || '').trim() || 'unlisted diagnosis';
      return {confidence:'Trial to review — diagnosis requires prescreening', trial, reasons:[`${shown} has not been mapped to a trial disease category`], unknown:['investigator must confirm diagnosis-specific eligibility']};
    }
    if (p.cancer === 'Cancer — any type') {
      if (!universalLimitPass(trial.requires || {}, p)) return null;
      const reasons = ['cancer type not specified — study shown for diagnosis review'];
      if (p.age_known) reasons.push('age is within any published study limit');
      if (p.weight_known) reasons.push('weight is within any published study limit');
      return {confidence:'Trial to review — cancer type not specified', trial, reasons, unknown:['disease-specific and protocol-specific eligibility requires prescreening']};
    }
    [broad] = [false]; const dm = diagnosisMatch(trial, p.cancer); if (!dm[0]) return null; broad = dm[1];
    const trialText = `${trial.title || ''} ${trial.notes || ''}`.toLowerCase();
    if ((trialText.includes('epitheliotropic') || trialText.includes('cutaneous lymphoma')) && p.cancer !== 'Cutaneous epitheliotropic lymphoma') return null;

    const req = trial.requires || {}, exc = trial.excludes || {}, reasons = [], unknown = [];
    let excluded = false;
    const addUnknown = text => unknown.push(text);
    if (req.confirmed) { if (p.diagnosis_status === 'Suspected / not confirmed') excluded = true; else if (p.diagnosis_status === UNKNOWN) addUnknown('pathology/cytology confirmation of the diagnosis'); }
    if (req.active_treatment_target) { if (['Completely removed — clean margins','No evidence of disease (NED)'].includes(p.tumor_status)) excluded = true; else if ([UNKNOWN,'Removed — margins unknown','Removed — incomplete/dirty margins'].includes(p.tumor_status)) addUnknown('whether an active treatment target is present'); }
    if (req.measurable_or_lung_metastasis) { if (!['Tumor still present / measurable','Local recurrence'].includes(p.tumor_status) && p.metastasis === 'No known metastases') excluded = true; else if (p.tumor_status === UNKNOWN || [UNKNOWN,'Suspected / staging incomplete'].includes(p.metastasis)) addUnknown('whether measurable disease or lung metastasis is present'); }
    for (const [key, field, text] of [['standard_therapy_unavailable','standard_therapy_unavailable','whether standard anticancer treatment is no longer appropriate or feasible'],['large_inoperable_or_rt_preferred','large_inoperable_or_rt_preferred','whether the tumor is large/inoperable or radiotherapy is preferred to surgery'],['surgery_or_rt_not_possible','surgery_or_rt_not_possible','whether curative surgery/radiotherapy is no longer possible'],['ct_and_current_biopsy','ct_and_current_biopsy','whether current CT and biopsy requirements can be met']]) if (req[key]) { if (p[field] === 'No') excluded = true; else if (p[field] === UNKNOWN) addUnknown(text); }
    const priorRules = [['prior_local_radiation','radiation',['Previously received','Currently receiving'],'whether prior local radiation is excluded'],['prior_surgery','surgery',['Yes'],'whether prior surgery is excluded'],['prior_chemo','chemo',['Previously received','Currently receiving'],'whether prior chemotherapy is excluded'],['prior_immunotherapy','immunotherapy_history',['Previously received','Currently receiving'],'whether prior immunotherapy is excluded']];
    for (const [key, field, bad, text] of priorRules) if (exc[key]) { if (bad.includes(p[field])) excluded = true; else if (p[field] === UNKNOWN) addUnknown(text); }
    if (exc.immunosuppressive) { if (p.immunosuppressive === 'Yes') excluded = true; else if (p.immunosuppressive === UNKNOWN) addUnknown('whether immunosuppressive medication is excluded'); }
    for (const [key, field, current, washout, label] of [['current_chemo','chemo','Currently receiving','chemo_washout_days','chemotherapy'],['current_steroids','steroids','Currently taking','steroid_washout_days','steroid'],['current_radiation','radiation','Currently receiving','radiation_washout_days','radiation']]) if (exc[key]) { if (p[field] === current) { if (req[washout]) addUnknown(`${label} washout of ${req[washout]} days`); else excluded = true; } else if (p[field] === UNKNOWN) addUnknown(`whether current ${label} is excluded`); }
    if (req.prior_radiation === false) { if (['Previously received','Currently receiving'].includes(p.radiation)) excluded = true; else if (p.radiation === UNKNOWN) addUnknown('whether prior radiation is excluded'); }
    if (req.prior_radiation === true) { if (p.radiation === 'Never') excluded = true; else if (p.radiation === UNKNOWN) addUnknown('whether prior radiation is required'); }
    if (req.planned_surgery || req.planned_amputation || req.planned_amputation_and_chemo) { if (!prefs.has('Surgery')) excluded = true; else addUnknown('required study surgery/amputation has not yet been confirmed'); }
    if (req.planned_radiation) { if (!prefs.has('Radiation') || p.radiation_affordability === 'Would not consider radiation') excluded = true; else addUnknown('required study radiation has not yet been confirmed'); }
    if (req.planned_doxorubicin || req.planned_amputation_and_chemo) { if (!prefs.has('Chemotherapy')) excluded = true; else addUnknown('required study chemotherapy/doxorubicin has not yet been confirmed'); }
    if (req.sex) { const allowed = Array.isArray(req.sex) ? req.sex : [req.sex]; if (p.sex === UNKNOWN) addUnknown('sex requirement'); else if (!allowed.some(x => p.sex.startsWith(x))) excluded = true; }
    if (req.localized) { if (p.localized === 'No') excluded = true; else if (p.localized === UNKNOWN) addUnknown('whether the disease is localized'); else reasons.push('localized disease reported'); }
    if (req.measurable && !['Tumor still present / measurable','Local recurrence'].includes(p.tumor_status)) { if (p.tumor_status === UNKNOWN) addUnknown('whether measurable disease is present'); else excluded = true; }
    if (req.metastatic) { if (p.metastasis === 'No known metastases') excluded = true; else if ([UNKNOWN,'Suspected / staging incomplete'].includes(p.metastasis)) addUnknown('whether metastasis is confirmed'); }
    if (req.no_metastasis) { if (p.metastasis === 'Confirmed metastases') excluded = true; else if ([UNKNOWN,'Suspected / staging incomplete'].includes(p.metastasis)) addUnknown('whether staging confirms no metastasis'); }
    const lim = limits(req);
    if (lim.minAge != null) { if (p.age_known && p.age < lim.minAge) excluded = true; else if (!p.age_known) addUnknown(`minimum age of ${lim.minAge} years`); }
    if (lim.maxAge != null) { if (p.age_known && p.age > lim.maxAge) excluded = true; else if (!p.age_known) addUnknown(`maximum age of ${lim.maxAge} years`); }
    if (lim.minLb != null) { if (p.weight_known && p.weight_lb < lim.minLb) excluded = true; else if (!p.weight_known) addUnknown(`minimum weight of ${lim.minLb.toFixed(1)} lb`); }
    if (lim.maxLb != null) { if (p.weight_known && p.weight_lb > lim.maxLb) excluded = true; else if (!p.weight_known) addUnknown(`maximum weight of ${lim.maxLb.toFixed(1)} lb`); }
    if (req.prior_chemo === false) { if (['Previously received','Currently receiving'].includes(p.chemo)) excluded = true; else if (p.chemo === UNKNOWN) addUnknown('whether prior chemotherapy is excluded'); }
    if (req.prior_chemo === true) { if (p.chemo === 'Never') excluded = true; else if (p.chemo === UNKNOWN) addUnknown('whether prior chemotherapy is required'); }
    if (req.prior_surgery === true) { if (p.surgery === 'No') excluded = true; else if (p.surgery === UNKNOWN) addUnknown('whether prior surgery is required'); }
    if (req.prior_surgery === false) { if (p.surgery === 'Yes') excluded = true; else if (p.surgery === UNKNOWN) addUnknown('whether prior surgery is excluded'); }
    if (req.post_splenectomy) { if (p.surgery === 'No' || p.prior_procedure === 'Other') excluded = true; else if (p.surgery === UNKNOWN) addUnknown('whether splenectomy has been performed'); else if (p.prior_procedure !== 'Splenectomy') addUnknown('whether the prior surgery was splenectomy'); }
    if (req.post_amputation) { if (p.surgery === 'No' || ['Limb-sparing surgery','Other'].includes(p.prior_procedure)) excluded = true; else if (p.surgery === UNKNOWN) addUnknown('whether amputation has been performed'); else if (p.prior_procedure !== 'Amputation') addUnknown('whether the prior surgery was amputation'); }
    if (req.pretreatment_biopsy) addUnknown('pretreatment biopsy requirement');
    if (req.resectable_or_minimal) addUnknown('whether disease is resectable/minimal as required');
    if (req.progressive) { if (LYMPHOMA.has(p.cancer) && p.lymphoma_response !== 'Progression during treatment') { if (p.lymphoma_response === UNKNOWN) addUnknown('whether disease is progressive'); else excluded = true; } else if (!LYMPHOMA.has(p.cancer)) addUnknown('whether disease is progressive'); }
    if (req.relapsed_or_refractory) { if (LYMPHOMA.has(p.cancer)) { if (!['Progression during treatment','First relapse after remission','More than one relapse'].includes(p.lymphoma_response)) { if (p.lymphoma_response === UNKNOWN) addUnknown('whether lymphoma is relapsed/refractory'); else excluded = true; } } else addUnknown('whether disease is relapsed/refractory'); }
    if (excluded) return null;
    reasons.push(broad ? 'broad disease-family eligibility supports investigator review' : `${p.cancer} matches the study disease category`);
    if (p.diagnosis_status === 'Confirmed by pathology/cytology') reasons.push('diagnosis reported as confirmed');
    if (p.tumor_status === 'Tumor still present / measurable') reasons.push('gross/measurable tumor reported');
    const checks = [];
    if (req.active_treatment_target) checks.push(['Tumor still present / measurable','Local recurrence'].includes(p.tumor_status));
    if (req.localized) checks.push(p.localized === 'Yes'); if (req.measurable) checks.push(['Tumor still present / measurable','Local recurrence'].includes(p.tumor_status));
    if (lim.minAge != null) checks.push(p.age_known && p.age >= lim.minAge); if (lim.maxAge != null) checks.push(p.age_known && p.age <= lim.maxAge);
    if (req.metastatic) checks.push(p.metastasis === 'Confirmed metastases'); if (req.no_metastasis) checks.push(p.metastasis === 'No known metastases');
    if (lim.minLb != null) checks.push(p.weight_known && p.weight_lb >= lim.minLb); if (lim.maxLb != null) checks.push(p.weight_known && p.weight_lb <= lim.maxLb);
    if (req.prior_chemo === false) checks.push(p.chemo === 'Never'); if (req.prior_chemo === true) checks.push(['Previously received','Currently receiving'].includes(p.chemo));
    if (req.prior_surgery === true) checks.push(p.surgery === 'Yes'); if (req.prior_surgery === false) checks.push(p.surgery === 'No');
    if (trial.special_requirement) addUnknown(trial.special_requirement);
    let confidence = Object.keys(req).length && checks.length && checks.every(Boolean) && !unknown.length ? 'Likely match' : 'Possible match';
    if (trial.owner_prescreen_required || trial.broad_disease_fallback || trial.requires_site_screening || trial.freshness_unresolved) confidence = broad ? 'Potential broad-treatment trial — prescreening required' : 'Possible match';
    if (trial.study_type === 'other_treatment_access') { confidence = 'Other treatment-access opportunity'; reasons.splice(0, reasons.length, 'funded/assisted standard anticancer treatment is available through this study pathway', ...reasons.filter(x => x !== 'diagnosis reported as confirmed')); }
    return {confidence, trial, reasons, unknown:uniq(unknown)};
  }

  function resultText(matches) {
    const lines = ['Clinical Trial Finder Results'];
    for (const m of matches) { const t=m.trial; lines.push('',m.confidence,t.center || '',t.title || '',`Why: ${m.reasons.join('; ')}.`,m.unknown.length?`Confirm: ${m.unknown.join('; ')}.`:'',`Contact: ${t.contacts || t.contact || 'Contact the study team through the official study page'}`,`Full study details: ${t.registry_url || t.url || ''}`,`Status: ${t.status || ''} · Last verified: ${t.verified || 'date not recorded'}`); }
    lines.push('','Recruitment and eligibility can change; confirm current status with the study team.'); return lines.filter(x => x !== '').join('\n');
  }

  function render(matches) {
    if (!matches.length) { results.innerHTML='<h2>Results</h2><div class="no-results">No plausible matches were found among the currently verified trials. This does not mean that no suitable study exists — recruitment and eligibility can change. Review the treatment options you selected or check again as recruitment changes.</div>'; return; }
    const cards = matches.map(m => { const t=m.trial, url=t.registry_url || t.url || '', sites=(t.sites || []).map(x=>`${esc(x.hospital)} — ${esc(x.city)}, ${esc(x.state)}`).join('; '); return `<article class="result-card"><h3>${esc(m.confidence)} · ${esc(t.center)}</h3><h4>${esc(t.title)}</h4><p><strong>Study type:</strong> ${esc(String(t.study_type || 'treatment').replaceAll('_',' '))}</p><p><strong>Why it may fit:</strong> ${esc(m.reasons.join('; '))}.</p>${m.unknown.length?`<p><strong>Needs confirmation:</strong> ${esc(m.unknown.join('; '))}.</p>`:''}<p><strong>Contact:</strong> ${esc(t.contacts || t.contact || 'Contact the study team through the official study page')}</p>${sites?`<p><strong>Participating sites:</strong> ${sites}</p>`:''}${url?`<a class="result-link" href="${esc(url)}" target="_blank" rel="noopener">View full study details →</a>`:''}<details><summary>Study information</summary>${t.intervention?`<p><strong>Study intervention:</strong> ${esc(t.intervention)}</p>`:''}<p><strong>What the study says:</strong> ${esc(t.notes || '')}</p><p><strong>Trial funding:</strong> ${esc(t.funding || 'Ask the study team about covered study costs')}</p><small>Status: ${esc(t.status || '')} · Last verified: ${esc(t.verified || 'date not recorded')}</small></details></article>`; }).join('');
    results.innerHTML=`<h2>Results</h2><p class="result-summary">${matches.length} oncology opportunity(ies) may be worth contacting</p>${cards}<div class="result-actions"><button type="button" id="copy-results">Copy results</button><button type="button" id="print-results">Save / print PDF</button></div>`;
    document.querySelector('#copy-results').addEventListener('click', async e => { await navigator.clipboard.writeText(resultText(matches)); e.currentTarget.textContent='Results copied'; });
    document.querySelector('#print-results').addEventListener('click', () => window.print());
  }

  function updateForm() {
    const p=patient(), cancer=p.cancer, browse=cancer==='Cancer — any type', unlisted=cancer==="My cancer type isn't listed", hematologic=LYMPHOMA.has(cancer)||['Cutaneous epitheliotropic lymphoma','Acute myeloid leukemia'].includes(cancer);
    show('.unlisted-only',unlisted); show('.specific-only',!browse&&!unlisted); show('.solid-only',!browse&&!unlisted&&!hematologic&&cancer!=='Brain tumor / glioma');
    show('.brain-only',cancer==='Brain tumor / glioma'); show('.lymphoma-only',LYMPHOMA.has(cancer)||cancer==='Cutaneous epitheliotropic lymphoma'); show('.aml-only',cancer==='Acute myeloid leukemia');
    show('.mct-only',cancer==='Mast cell tumor'); show('.osa-only',cancer==='Osteosarcoma'); show('.hsa-only',cancer==='Hemangiosarcoma'); show('.procedure-only',p.surgery==='Yes'&&['Osteosarcoma','Hemangiosarcoma'].includes(cancer));
    const candidates=trials.filter(t=>speciesMatches(t.species,p.species)&&countryMatches(t.country||'USA',p.country)&&(browse||unlisted||diagnosisMatch(t,cancer)[0])); const req=new Set(candidates.flatMap(t=>Object.keys(t.requires||{}))), exc=new Set(candidates.flatMap(t=>Object.keys(t.excludes||{})));
    show('.protocol-standard',!browse&&!unlisted&&req.has('standard_therapy_unavailable')); show('.protocol-large',!browse&&!unlisted&&req.has('large_inoperable_or_rt_preferred')); show('.protocol-no-local',!browse&&!unlisted&&req.has('surgery_or_rt_not_possible')); show('.protocol-ct-biopsy',!browse&&!unlisted&&req.has('ct_and_current_biopsy'));
    show('.steroids-only',!browse&&!unlisted&&(exc.has('current_steroids')||req.has('steroid_washout_days'))); show('.immunosuppressive-only',!browse&&!unlisted&&exc.has('immunosuppressive')); show('.radiation-plan-only',!browse&&!unlisted&&req.has('planned_radiation'));
    const note=document.querySelector('.browse-note'); note.hidden=!browse&&!unlisted; note.textContent=browse?'Browse mode: disease-specific eligibility is not used until a cancer type is selected.':'Unlisted diagnosis: only genuinely all-tumor treatment programs will be shown for investigator review.';
    form.elements.age.disabled=!checked('age_known'); form.elements.weight.disabled=!checked('weight_known'); form.elements.weight_unit.disabled=!checked('weight_known');
  }

  if (typeof window !== 'undefined') window.__MATCHER_TEST__ = {matchTrial, diagnosisMatch, modalities};
  if (!form || !results) return;
  form.addEventListener('change',updateForm);
  form.addEventListener('submit',e=>{e.preventDefault(); const p=patient(), matches=trials.map(t=>matchTrial(t,p)).filter(Boolean); matches.sort((a,b)=>{const rank=x=>x==='Likely match'?0:x==='Possible match'?1:2; return rank(a.confidence)-rank(b.confidence)+(Number(Boolean(a.trial.early_phase))-Number(Boolean(b.trial.early_phase)));}); render(matches); results.scrollIntoView({behavior:'smooth',block:'start'}); if(window.umami) window.umami.track('matcher-search');});
  const catalog = window.MATCHER_INLINE_DATA ? Promise.resolve(window.MATCHER_INLINE_DATA) : fetch(window.MATCHER_DATA_URL).then(r=>{if(!r.ok)throw new Error(`Catalog ${r.status}`);return r.json();});
  catalog.then(data=>{trials=data;updateForm();}).catch(()=>{results.innerHTML='<div class="no-results">The trial catalog could not be loaded. Please try again shortly.</div>';});
})();
