(() => {
  'use strict';

  const UNKNOWN = "I don't know";
  const CURRENT = new Set(['current', 'confirmed_current']);
  const LYMPHOMA = new Set(['B-cell lymphoma', 'T-cell lymphoma', 'Lymphoma — other', 'Lymphoma — any type']);
  const EUROPE = new Set(['UK','United Kingdom','France','Italy','Portugal','Switzerland','Netherlands','The Netherlands','Belgium','Sweden','Slovenia','Spain','Germany','Cyprus','Austria','Poland','Norway','Denmark','Finland','Ireland','Czech Republic','Czechia','Hungary','Greece','Romania','Croatia','Estonia','Latvia','Lithuania','Luxembourg','Iceland']);
  // BEGIN SHARED MATCHER TABLES (generated; edit data/*.json)
  const ALIASES = {"B-cell lymphoma": ["Lymphoma", "Lymphoma — other"], "T-cell lymphoma": ["Lymphoma", "Lymphoma — other", "Enteropathy-associated T-cell lymphoma"], "Lymphoma — other": ["Lymphoma", "Gastrointestinal lymphoma", "Large cell lymphoma"], "Brain tumor / glioma": ["Brain tumor", "Glioma"], "Feline mammary carcinoma": ["Mammary carcinoma", "Mammary tumor"], "Mammary carcinoma": ["Mammary tumor"], "Mammary tumor — other": ["Mammary tumor"], "Urothelial / transitional cell carcinoma": ["Urothelial carcinoma", "Transitional cell carcinoma"], "Urothelial carcinoma": ["Urothelial / transitional cell carcinoma", "Transitional cell carcinoma", "Bladder cancer"], "Thyroid tumor / carcinoma": ["Thyroid carcinoma"], "Thyroid carcinoma": ["Thyroid tumor / carcinoma"], "Hepatocellular carcinoma": ["Hepatic carcinoma"], "Primary lung tumor": ["Pulmonary carcinoma"], "Oral squamous cell carcinoma": ["Feline oral SCC"], "Squamous cell carcinoma — other": ["Squamous cell carcinoma"], "Oral tumor — other": ["Oral tumor"], "Ocular melanoma / iris melanocytic tumor": ["Ocular melanoma", "Iris melanocytic tumor"], "Chemodectoma": ["Aortic body tumor", "Aortic body tumors", "Heart-base tumor", "Heart base tumor", "Paraganglioma", "Non-chromaffin paraganglioma"], "Lymphoma — any type": ["Lymphoma", "B-cell lymphoma", "T-cell lymphoma", "Lymphoma — other", "Gastrointestinal lymphoma", "Large cell lymphoma", "Enteropathy-associated T-cell lymphoma"], "Leukemia — other": ["Leukemia", "Chronic lymphocytic leukemia"], "Melanoma — other": ["Melanoma"], "Other sarcoma": ["Sarcoma — other"], "Other solid tumor": ["Carcinoma — other"]};
  const FAMILIES = {"Gastric / stomach cancer": ["carcinoma", "solid_tumor"], "Colorectal / rectal cancer": ["carcinoma", "solid_tumor"], "Salivary gland cancer": ["carcinoma", "solid_tumor"], "Esophageal cancer": ["carcinoma", "solid_tumor"], "Thymoma / thymic tumor": ["solid_tumor"], "Gastrointestinal stromal tumor (GIST)": ["sarcoma", "solid_tumor"], "Peripheral nerve sheath tumor": ["sarcoma", "soft_tissue_sarcoma", "solid_tumor"], "Leiomyosarcoma": ["sarcoma", "soft_tissue_sarcoma", "solid_tumor"], "Fibrosarcoma": ["sarcoma", "soft_tissue_sarcoma", "solid_tumor"], "Liposarcoma": ["sarcoma", "soft_tissue_sarcoma", "solid_tumor"], "Rhabdomyosarcoma": ["sarcoma", "soft_tissue_sarcoma", "solid_tumor"], "Chondrosarcoma": ["sarcoma", "solid_tumor"], "Nasal tumor / nasal cancer": ["nasal_tumor", "solid_tumor"], "Multiple myeloma / plasma cell cancer": ["hematologic"], "Anal sac adenocarcinoma (AGASACA)": ["solid_tumor", "carcinoma"], "Gallbladder carcinoma": ["solid_tumor", "carcinoma"], "Hepatocellular carcinoma": ["solid_tumor", "carcinoma"], "Intestinal carcinoma": ["solid_tumor", "carcinoma"], "Mammary carcinoma": ["solid_tumor", "carcinoma"], "Feline mammary carcinoma": ["solid_tumor", "carcinoma"], "Pancreatic carcinoma": ["solid_tumor", "carcinoma"], "Primary lung tumor": ["solid_tumor", "carcinoma"], "Prostate cancer": ["solid_tumor", "carcinoma"], "Sinonasal carcinoma": ["solid_tumor", "carcinoma"], "Oral squamous cell carcinoma": ["solid_tumor", "carcinoma"], "Squamous cell carcinoma": ["solid_tumor", "carcinoma"], "Squamous cell carcinoma — other": ["solid_tumor", "carcinoma"], "Thyroid carcinoma": ["solid_tumor", "carcinoma"], "Thyroid tumor / carcinoma": ["solid_tumor", "carcinoma"], "Urothelial / transitional cell carcinoma": ["solid_tumor", "carcinoma"], "Urothelial carcinoma": ["solid_tumor", "carcinoma"], "Carcinoma — other": ["solid_tumor", "carcinoma"], "Soft tissue sarcoma": ["solid_tumor", "sarcoma", "soft_tissue_sarcoma"], "Spindle cell sarcoma": ["solid_tumor", "sarcoma", "soft_tissue_sarcoma"], "Feline injection-site sarcoma": ["solid_tumor", "sarcoma", "soft_tissue_sarcoma"], "Osteosarcoma": ["solid_tumor", "sarcoma"], "Hemangiosarcoma": ["solid_tumor", "sarcoma"], "Histiocytic sarcoma": ["solid_tumor", "sarcoma"], "Other sarcoma": ["solid_tumor", "sarcoma"], "Oral melanoma": ["solid_tumor", "melanoma"], "Melanoma — other": ["solid_tumor", "melanoma"], "Ocular melanoma / iris melanocytic tumor": ["solid_tumor", "melanoma"], "Mast cell tumor": ["solid_tumor"], "Adrenal tumor": ["solid_tumor"], "Chemodectoma": ["solid_tumor"], "Insulinoma": ["solid_tumor"], "Renal tumor": ["solid_tumor"], "Other bone tumor": ["solid_tumor"], "Other liver tumor": ["solid_tumor"], "Other solid tumor": ["solid_tumor"], "Oral tumor — other": ["solid_tumor"], "Mammary tumor — other": ["solid_tumor"], "Brain tumor / glioma": ["solid_tumor"], "B-cell lymphoma": ["hematologic", "lymphoma"], "T-cell lymphoma": ["hematologic", "lymphoma"], "Lymphoma — other": ["hematologic", "lymphoma"], "Lymphoma — any type": ["hematologic", "lymphoma"], "Cutaneous epitheliotropic lymphoma": ["hematologic", "lymphoma"], "Acute myeloid leukemia": ["hematologic", "leukemia"], "Leukemia — other": ["hematologic", "leukemia"]};
  const PROTOCOL_RULES = {"requires": {"active_treatment_target": {"label": "active treatment target", "handled": true}, "aggressive_lymphoma": {"label": "aggressive lymphoma"}, "anesthesia_candidate": {"label": "anesthesia candidate"}, "anesthesia_eligible": {"label": "anesthesia eligible"}, "anesthesia_fit": {"label": "anesthesia fit"}, "anticipated_survival_over_3_months": {"label": "anticipated survival over 3 months"}, "appendicular_location": {"label": "appendicular location", "field": "osa_location", "allowed": ["Appendicular — limb bone"]}, "appendicular_osteosarcoma": {"label": "appendicular osteosarcoma", "field": "osa_location", "allowed": ["Appendicular — limb bone"]}, "brain_tumor_biopsy": {"label": "brain tumor biopsy"}, "brain_tumor_present": {"label": "brain tumor present"}, "chemo_candidate": {"label": "chemo candidate"}, "chemo_washout_days": {"label": "chemo washout days"}, "confirmed": {"label": "confirmed", "handled": true}, "ct_screening": {"label": "ct screening"}, "current_chemo": {"label": "current chemo", "preference": "Chemotherapy"}, "extremity_sts": {"label": "extremity sts"}, "giant_breed": {"label": "giant breed"}, "insulinoma_or_pancreatic_neuroendocrine_tumor": {"label": "insulinoma or pancreatic neuroendocrine tumor"}, "intermediate_or_large_cell_multicentric_lymphoma": {"label": "intermediate or large cell multicentric lymphoma"}, "large_inoperable_or_rt_preferred": {"label": "large inoperable or rt preferred", "handled": true}, "limb_osteosarcoma": {"label": "limb osteosarcoma", "field": "osa_location", "allowed": ["Appendicular — limb bone"]}, "liver_tumor": {"label": "liver tumor"}, "localized": {"label": "localized", "handled": true}, "lymphoma_response": {"label": "lymphoma response", "handled": true}, "max_tumor_cm": {"label": "maximum tumor size (cm)"}, "max_vcog_performance_status": {"label": "max vcog performance status"}, "max_weight_kg": {"label": "max weight kg", "handled": true}, "max_weight_lb": {"label": "max weight lb", "handled": true}, "measurable": {"label": "measurable", "handled": true}, "measurable_lung_metastases": {"label": "measurable lung metastases"}, "measurable_or_lung_metastasis": {"label": "measurable or lung metastasis", "handled": true}, "metastatic": {"label": "metastatic", "handled": true}, "min_age_years": {"label": "min age years", "handled": true}, "min_expected_survival_weeks": {"label": "min expected survival weeks"}, "min_tumor_cm": {"label": "minimum tumor size (cm)"}, "min_weight_kg": {"label": "min weight kg", "handled": true}, "min_weight_lb": {"label": "min weight lb", "handled": true}, "newly_diagnosed": {"label": "newly diagnosed"}, "newly_diagnosed_brain_tumor": {"label": "newly diagnosed brain tumor"}, "no_metastasis": {"label": "no metastasis", "handled": true}, "nonresectable_or_high_surgical_risk": {"label": "nonresectable or high surgical risk"}, "nonsurgical_or_surgery_declined": {"label": "nonsurgical or surgery declined"}, "oral_mass": {"label": "oral mass"}, "planned_amputation": {"label": "planned amputation", "handled": true}, "planned_amputation_and_chemo": {"label": "planned amputation and chemo", "handled": true}, "planned_carboplatin": {"label": "planned carboplatin", "preference": "Chemotherapy"}, "planned_chop": {"label": "planned chop", "preference": "Chemotherapy"}, "planned_doxorubicin": {"label": "planned doxorubicin", "handled": true}, "planned_radiation": {"label": "planned radiation", "handled": true}, "planned_surgery": {"label": "planned surgery", "handled": true}, "planned_surgical_resection": {"label": "planned surgical resection", "preference": "Surgery"}, "post_amputation": {"label": "post amputation", "handled": true}, "post_splenectomy": {"label": "post splenectomy", "handled": true}, "pretreatment_biopsy": {"label": "pretreatment biopsy", "handled": true}, "previously_spayed": {"label": "previously spayed"}, "previously_untreated": {"label": "previously untreated"}, "primary_bone_tumor": {"label": "primary bone tumor"}, "primary_removed": {"label": "primary removed"}, "prior_chemo": {"label": "prior chemo", "handled": true}, "prior_radiation": {"label": "prior radiation", "handled": true}, "prior_surgery": {"label": "prior surgery", "handled": true}, "prostatic_cancer": {"label": "prostatic cancer"}, "radiation_therapy": {"label": "radiation therapy"}, "radiation_washout_days": {"label": "radiation washout days"}, "recurrent": {"label": "recurrent"}, "resectable": {"label": "resectable"}, "resectable_or_minimal": {"label": "resectable or minimal", "handled": true}, "serum_creatinine_lte_2": {"label": "serum creatinine lte 2"}, "standard_of_care_therapy": {"label": "standard of care therapy"}, "suitable_hifu_acoustic_window": {"label": "suitable hifu acoustic window"}, "superficial_accessible_tumor": {"label": "superficial accessible tumor"}, "superficial_or_oral_tumor": {"label": "superficial or oral tumor"}, "surgery_candidate": {"label": "surgery candidate"}, "surgery_planned": {"label": "surgery planned", "preference": "Surgery"}, "suspected_or_confirmed_glioma": {"label": "suspected or confirmed glioma"}, "target_lesion_over_20mm_or_persistent_hypoglycemia_after_surgery": {"label": "target lesion over 20mm or persistent hypoglycemia after surgery"}, "thyroid_tumor": {"label": "thyroid tumor"}, "untreated_newly_diagnosed": {"label": "untreated newly diagnosed"}, "visible_tumor": {"label": "visible tumor"}, "weight_bearing": {"label": "weight bearing"}, "standard_therapy_unavailable": {"label": "standard therapy unavailable", "handled": true}, "surgery_or_rt_not_possible": {"label": "surgery or rt not possible", "handled": true}, "ct_and_current_biopsy": {"label": "ct and current biopsy", "handled": true}, "sex": {"label": "sex", "handled": true}, "max_age_years": {"label": "max age years", "handled": true}, "progressive": {"label": "progressive", "handled": true}, "relapsed_or_refractory": {"label": "relapsed or refractory", "handled": true}, "planned_chemo": {"label": "planned chemotherapy", "preference": "Chemotherapy"}, "steroid_washout_days": {"label": "steroid washout days"}, "min_age_years_exclusive": {"label": "minimum age, exclusive boundary", "handled": true}, "min_weight_kg_exclusive": {"label": "minimum weight, exclusive boundary", "handled": true}, "max_weight_kg_exclusive": {"label": "maximum weight, exclusive boundary", "handled": true}, "prednisone_eligible": {"label": "ability to receive prednisone with a six-week taper"}, "anticancer_treatment_washout": {"label": "study-team-defined washout or stopping other anticancer treatment"}, "adequate_organ_function": {"label": "adequate organ function"}, "large_cell_multicentric_stage_iii_or_higher": {"label": "large-cell multicentric lymphoma at stage III or higher"}, "two_chop_cycles_completed": {"label": "partial or complete response after two CHOP cycles"}, "peripheral_bcell_lymphoma_stage_ii_to_iv": {"label": "peripheral B-cell lymphoma at stage II–IV with at least two nodes measuring 2 cm"}, "accessible_intratumoral_target": {"label": "tumor safely accessible for intratumoral injections"}, "distal_radius_osteosarcoma": {"label": "osteosarcoma specifically in the distal radius"}, "giant_breed_or_weight_at_least_40kg": {"label": "giant breed or body weight at least 40 kg"}, "nsaid_tolerant": {"label": "safe NSAID administration"}, "stable_pain_medication_7d": {"label": "stable oral pain medication for at least seven days"}, "bone_medication_washout_30d": {"label": "bone-medication washout of 30 days"}, "max_tumor_cm_exclusive": {"label": "tumor size strictly below (cm)"}, "min_tumor_cm_exclusive": {"label": "tumor size strictly above (cm)"}, "cytology_or_braf_and_visible_bladder_mass": {"label": "cytology or positive BRAF testing together with a visible bladder mass"}, "pulmonary_lesion_cm_exclusive": {"label": "lung metastatic lesion strictly above (cm)"}, "oral_melanoma_stage_ii_or_iii": {"label": "oral melanoma at stage II or III"}, "other_treatments_suspended": {"label": "suspension of other anticancer treatments"}, "circulating_leukemia_cells": {"label": "leukemia cells present in peripheral blood"}, "b7h3_expression_and_prior_carboplatin": {"label": "B7-H3 expression and prior 4–6 carboplatin doses"}, "prior_doxorubicin_and_carboplatin_review": {"label": "review of prior doxorubicin and carboplatin to determine a qualifying treatment arm"}, "bcell_lineage_and_non_gi_disease": {"label": "B-cell lineage, qualifying disease stage and absence of gastrointestinal lymphoma"}, "small_cell_gastrointestinal_lymphoma": {"label": "biopsy-confirmed small-cell gastrointestinal lymphoma"}, "within_six_hours_of_college_station": {"label": "residence within a six-hour drive of College Station"}, "immunosuppressant_washout_7d": {"label": "immunosuppressant washout of seven days"}, "survivin_expression_or_postmortem_consent": {"label": "survivin expression or the specified postmortem-consent pathway"}, "boxer_breed": {"label": "Boxer breed"}, "prescapular_or_popliteal_nodal_lymphoma": {"label": "nodal lymphoma in a prescapular or popliteal lymph node"}, "center_diagnosis_and_positive_mutation": {"label": "Nihon diagnosis and a qualifying positive tumor-mutation test"}, "multicentric_peripheral_node_lymphoma": {"label": "multicentric lymphoma diagnosed from a peripheral lymph node"}, "single_primary_pulmonary_carcinoma": {"label": "a single primary pulmonary carcinoma"}, "mandibular_or_maxillary_bone_lysis": {"label": "mandibular or maxillary bone invasion with CT-confirmed bone lysis"}, "immunotherapy_and_anti_ngf_washout_21d": {"label": "immunotherapy and anti-NGF washout of 21 days"}, "current_chop": {"label": "ongoing CHOP chemotherapy", "field": "chemo", "allowed": ["Currently receiving"]}, "single_telencephalic_glioma_on_mri": {"label": "a single telencephalic intraparenchymal lesion consistent with high-grade glioma on MRI"}, "immunotherapy_washout_days": {"label": "immunotherapy washout (days)"}, "surgery_washout_days": {"label": "surgery washout (days)"}, "prostatic_diagnosis_at_screening": {"label": "prostatic carcinoma diagnosis confirmed by study screening"}, "single_nonventricular_nonbrainstem_glioma": {"label": "a single glioma outside ventricles and brainstem"}, "immunotherapy_washout_months": {"label": "immunotherapy washout (months)"}, "prior_or_planned_mammary_surgery": {"label": "mammary-tumor surgical standard care, previously performed or planned", "history_or_preference": {"field": "surgery", "allowed": ["Yes"], "preference": "Surgery"}, "when_field": {"cancer": ["Mammary carcinoma", "Mammary tumor — other"]}}, "histology_or_long_bone_osa_exception": {"label": "histologic confirmation, or MedVet approval of a long-bone OSA lesion when amputation is declined", "confirmation_or_appendicular_osa": true}, "bcell_lymphoma_stage_iii_to_v_a": {"label": "B-cell lymphoma at stage III–V(a)", "field": "lymphoma_stage_substage", "allowed": ["IIIa", "IVa", "Va"]}, "kv9_concurrent_drugs_eligible": {"label": "Kv9-compatible concurrent medication (Apoquel, Cytopoint, Beransa and recent vaccination may be allowed)", "field": "kv9_concurrent_drugs_eligible", "allowed": ["Yes"]}, "distal_radius_osa": {"label": "osteosarcoma of the distal radius", "field": "osa_site_detail", "allowed": ["Distal radius"]}, "oral_tumor_not_excised": {"label": "oral melanoma has not been surgically excised (diagnostic biopsy is a separate procedure)", "field": "oral_tumor_excised", "allowed": ["No"]}, "eligible_cohorts": {"label": "eligible protocol cohort", "alternative_owner_cohorts": true}, "splenic_primary": {"label": "primary splenic hemangiosarcoma", "field": "hsa_site", "allowed": ["Spleen"]}, "pre_splenectomy": {"label": "enrollment before splenectomy", "when_field": {"surgery": ["Yes"]}, "field": "prior_procedure", "disallowed": ["Splenectomy"]}, "bcell_lymphoma_lineage": {"label": "confirmed B-cell lymphoma lineage", "when_family": "lymphoma", "field": "lymphoma_type", "allowed": ["B-cell"]}, "high_grade_abdominal_gi_lymphoma": {"label": "high-grade / large-cell gastrointestinal lymphoma confined to the abdomen"}, "felv_fiv_negative": {"label": "negative FeLV and FIV testing"}, "lymphoma_chemotherapy_backbone": {"label": "lymphoma treatment together with standard chemotherapy", "when_family": "lymphoma", "preference": "Chemotherapy"}}, "excludes": {"active_wounds": {"label": "active wounds"}, "adjacent_structure_invasion": {"label": "adjacent structure invasion"}, "advanced_disease": {"label": "advanced disease"}, "advanced_metastatic_disease": {"label": "advanced metastatic disease"}, "alternative_herbal_medications": {"label": "alternative herbal medications"}, "alternative_therapy": {"label": "alternative therapy"}, "anesthesia_contraindicated": {"label": "anesthesia contraindicated"}, "autoimmune_disease": {"label": "autoimmune disease"}, "bone_metastasis": {"label": "bone metastasis"}, "coagulation_disorder": {"label": "coagulation disorder"}, "concurrent_chemotherapy": {"label": "concurrent chemotherapy", "field": "chemo", "disallowed": ["Currently receiving"]}, "concurrent_immunomodulatory_drugs": {"label": "concurrent immunomodulatory drugs", "field": "immunosuppressive", "disallowed": ["Yes"]}, "concurrent_local_radiation": {"label": "concurrent local radiation", "field": "radiation", "disallowed": ["Currently receiving"]}, "concurrent_small_molecule_therapy": {"label": "concurrent small molecule therapy"}, "concurrent_surgery": {"label": "concurrent surgery"}, "corticosteroids": {"label": "corticosteroids", "field": "steroids", "disallowed": ["Currently taking"]}, "current_chemo": {"label": "current chemo", "handled": true}, "current_immunosuppressive_medications": {"label": "current immunosuppressive medications", "field": "immunosuppressive", "disallowed": ["Yes"]}, "current_radiation": {"label": "current radiation", "handled": true}, "current_steroids": {"label": "current steroids", "handled": true}, "current_supplements": {"label": "current supplements"}, "cytopoint": {"label": "cytopoint"}, "extranodal_lymphoma": {"label": "extranodal lymphoma"}, "immune_mediated_disease": {"label": "immune mediated disease"}, "immunodeficiency": {"label": "immunodeficiency"}, "immunosuppressive": {"label": "immunosuppressive", "handled": true}, "indolent_lymphoma": {"label": "indolent lymphoma"}, "librela": {"label": "librela"}, "major_systemic_comorbidity": {"label": "major systemic comorbidity"}, "metastases_outside_lungs": {"label": "metastases outside lungs"}, "metastatic": {"label": "metastatic", "field": "metastasis", "disallowed": ["Confirmed metastases"]}, "other_clinical_study": {"label": "other clinical study"}, "other_immunotherapy": {"label": "other immunotherapy"}, "other_life_threatening_disease": {"label": "other life threatening disease"}, "owner_declines_post_hfire_surgery": {"label": "owner declines post hfire surgery"}, "poor_general_health": {"label": "poor general health"}, "poor_performance_status": {"label": "poor performance status"}, "pregnant_or_lactating": {"label": "pregnant or lactating"}, "prior_brain_tumor_therapy": {"label": "prior brain tumor therapy"}, "prior_cancer_treatment": {"label": "prior cancer treatment"}, "prior_checkpoint_inhibitor": {"label": "prior checkpoint inhibitor"}, "prior_chemo": {"label": "prior chemo", "handled": true}, "prior_gilvetmab": {"label": "prior gilvetmab"}, "prior_immunotherapy": {"label": "prior immunotherapy", "handled": true}, "prior_local_radiation": {"label": "prior local radiation", "handled": true}, "prior_osteosarcoma_treatment": {"label": "prior osteosarcoma treatment"}, "prior_radiation": {"label": "prior radiation", "field": "radiation", "disallowed": ["Previously received", "Currently receiving"]}, "prior_steroids": {"label": "prior steroids", "handled": true}, "prior_surgery": {"label": "prior surgery", "handled": true}, "prior_systemic_chemotherapy": {"label": "prior systemic chemotherapy", "field": "chemo", "disallowed": ["Previously received", "Currently receiving"]}, "pulmonary_metastasis": {"label": "pulmonary metastasis"}, "recent_anticancer_treatment_7d": {"label": "anticancer treatment washout of 7 days"}, "recent_chemotherapy_14d": {"label": "chemotherapy washout of 14 days"}, "recent_chemotherapy_3w": {"label": "chemotherapy washout of 21 days"}, "recent_immunosuppressants_14d": {"label": "immunosuppressant washout of 14 days"}, "recent_prednisone_7d": {"label": "prednisone washout of 7 days"}, "recent_radiation_30d": {"label": "radiation washout of 30 days"}, "recent_steroids_2w": {"label": "steroid washout of 14 days"}, "recent_systemic_antibiotics_14d": {"label": "recent systemic antibiotics 14d"}, "regional_lymph_node_metastasis": {"label": "regional lymph node metastasis", "field": "node_status", "disallowed": ["Positive"]}, "severe_systemic_disease": {"label": "severe systemic disease"}, "severe_systemic_illness": {"label": "severe systemic illness"}, "significant_comorbidity": {"label": "significant comorbidity"}, "significant_liver_or_kidney_dysfunction": {"label": "significant liver or kidney dysfunction"}, "significant_other_organ_disease": {"label": "significant other organ disease"}, "significant_systemic_disease": {"label": "significant systemic disease"}, "small_cell_lymphoma": {"label": "small cell lymphoma"}, "stage_v_lymphoma": {"label": "stage v lymphoma"}, "unresectable_tumor": {"label": "unresectable tumor"}, "concurrent_immunotherapy": {"label": "concurrent immunotherapy", "field": "immunotherapy_history", "disallowed": ["Currently receiving"]}, "nonstop_antioxidant_supplements": {"label": "antioxidant supplements that cannot be stopped"}, "distant_metastasis": {"label": "cancer spread beyond nearby lymph nodes"}, "prior_target_tumor_treatment": {"label": "previous treatment for the lung tumor", "field": "target_tumor_treated", "disallowed": ["Yes"]}, "prior_lymphoma_treatment": {"label": "previous lymphoma treatment", "field": "lymphoma_previously_treated", "disallowed": ["Yes"]}, "prior_target_tumor_surgery": {"label": "previous surgery for this osteosarcoma", "field": "target_tumor_prior_surgery", "disallowed": ["Yes"]}, "tcell_lymphoma_lineage": {"label": "T-cell lymphoma lineage", "when_family": "lymphoma", "field": "lymphoma_type", "disallowed": ["T-cell"]}, "relapsed_lymphoma": {"label": "relapsed lymphoma", "field": "lymphoma_response", "disallowed": ["First relapse after remission", "More than one relapse"]}}};
  // END SHARED MATCHER TABLES
  const BLOCKED = ['on hold','completed','closed enrollment','enrollment closed','closed for data review','suspended','past clinical study','not accepting','paused','not on current','do not match','coming soon','not yet independently confirmed','enrollment not confirmed','reconfirm before matching','previously active recruitment','sponsor page still lists study','current oncology archive listing','recent active trial; enrollment must be reconfirmed','patients needed; current enrollment should be reconfirmed','funded active-study evidence','current funded translational research'];
  const URL_CANCER_LABELS = {'Leukemia — other':'Leukemia — other', 'Lymphoma — any type':'Lymphoma — any type'};
  const form = document.querySelector('#matcher-form');
  const results = document.querySelector('#matcher-results');
  let trials = [];

  const esc = value => String(value ?? '').replace(/\*\*/g, '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const value = name => form.elements[name]?.value ?? UNKNOWN;
  const checked = name => Boolean(form.elements[name]?.checked);
  const show = (selector, yes) => document.querySelectorAll(selector).forEach(el => { el.hidden = !yes; });
  const speciesMatches = (trialSpecies, selected) => (Array.isArray(trialSpecies) ? trialSpecies : String(trialSpecies || '').split('/')).map(x => String(x).trim()).includes(selected);
  const countryMatches = (trial, selected) => {
    const countries = Array.isArray(trial.countries) && trial.countries.length ? trial.countries : [trial.country || 'USA'];
    return selected === 'All countries' ? true : selected === 'Europe — all countries' ? countries.some(country => EUROPE.has(country)) : countries.includes(selected);
  };
  const uniq = items => [...new Set(items.map(String))];

  function diagnosisMatch(trial, diagnosis, species) {
    const scoped = trial.cancers_by_species;
    const allowed = scoped ? scoped[species] || [] : trial.cancers || [];
    if (scoped && !allowed.length) return [false, false];
    const cancers = new Set(allowed);
    const exact = new Set([diagnosis, ...(ALIASES[diagnosis] || [])]);
    if (diagnosis === 'Spindle cell sarcoma') exact.add('Soft tissue sarcoma');
    const excluded = new Set(trial.excluded_cancers || []);
    const family = FAMILIES[diagnosis] || [];
    if ([...exact].some(x => excluded.has(x)) || family.some(x => (trial.excluded_disease_families || []).includes(x)) || (trial.pending_diagnosis_review || []).includes(diagnosis)) return [false, false];
    if ([...exact].some(x => cancers.has(x))) return [true, false];
    const broad = new Set(trial.broad_disease_families || []);
    if (broad.has('all_tumors') || (!broad.size && cancers.has('Cancer — any type'))) return [family.length > 0, true];
    return [family.some(x => broad.has(x)), family.some(x => broad.has(x))];
  }

  function modalities(trial) {
    const text = ['title','intervention','notes'].map(k => trial[k] || '').join(' ').toLowerCase();
    const req = trial.requires || {};
    const supported = new Set(['Surgery','Radiation','Chemotherapy','Immunotherapy','Targeted therapy','Experimental drug']);
    const mods = new Set((trial.treatments || []).filter(x => supported.has(x)));
    const has = words => words.some(x => text.includes(x));
    if (req.planned_surgery || req.planned_amputation || req.planned_amputation_and_chemo || has(['surgery','surgical','mastectom','amputation'])) mods.add('Surgery');
    if (req.planned_radiation || has(['radiotherapy','radiation','sbrt','flash','lattice','radiosensiti','proton'])) mods.add('Radiation');
    if (req.planned_doxorubicin || req.planned_amputation_and_chemo || has(['chemotherapy','doxorubicin','carboplatin','lomustine','vinorelbine','toceranib','tigilanol','chemoembol'])) mods.add('Chemotherapy');
    if (has(['immunotherap','vaccine','car-t','car t','interleukin','il-2','checkpoint','pd-1','pd-l1','oncolytic','tlr agonist','bcg'])) mods.add('Immunotherapy');
    if (has(['targeted','toceranib','kinase inhibitor','adam-12','versican','antibody','radioimmunotherap','nanobody'])) mods.add('Targeted therapy');
    if (has(['phase i','phase 1','phase ii','phase 2','experimental','investigational','tigilanol','oxc-101','rimcazole','gcn2','oncofap','nebumet','cantrixil'])) mods.add('Experimental drug');
    return mods;
  }

  function researchApproaches(trial) {
    if (Array.isArray(trial.treatment_approaches)) return new Set(trial.treatment_approaches);
    const text = ['title','intervention','notes'].map(k => trial[k] || '').join(' ').toLowerCase();
    const out = new Set();
    const has = words => words.some(x => text.includes(x));
    if (has(['immunotherap','pd-1','pd-l1','checkpoint','vaccine','car-t','car t','car-inkt','car inkt','interleukin','il-2','il-12','trike','natural killer','sting','tlr agonist','bcg'])) out.add('immunotherapy');
    if (has(['vaccine','vaccination','mrna'])) out.add('cancer_vaccine');
    if (has(['car-t','car t','car-inkt','car inkt','engineered t cell','engineered immune cell'])) out.add('engineered_immune_cells');
    if (has(['trametinib','mek inhibitor','kinase inhibitor','targeted therap','toceranib','sorafenib','inhibitor'])) out.add('targeted_therapy');
    if (has(['oncolytic','listeria','vesicular stomatitis virus','vsv-'])) out.add('oncolytic_microbe');
    if (has(['histotrips','hifu','high-intensity focused ultrasound','high intensity focused ultrasound','h-fire','hfire','focused ultrasound'])) out.add('focused_ultrasound');
    if (has(['flash','proton','sbrt','stereotactic','lattice radiation','lattice radiotherapy'])) out.add('radiation_innovation');
    return out;
  }

  function patient() {
    const data = Object.fromEntries(new FormData(form).entries());
    data.age_known = value('age') !== '' && Number.isFinite(Number(value('age'))); data.weight_known = value('weight') !== '' && Number.isFinite(Number(value('weight')));
    data.age = data.age_known ? Number(value('age')) : null; data.weight = data.weight_known ? Number(value('weight')) : null;
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
      minAge:req.min_age_years, minAgeExclusive:req.min_age_years_exclusive, maxAge:req.max_age_years,
      minLb:req.min_weight_lb ?? (req.min_weight_kg == null ? null : req.min_weight_kg * 2.2046226218),
      maxLb:req.max_weight_lb ?? (req.max_weight_kg == null ? null : req.max_weight_kg * 2.2046226218),
      minLbExclusive:req.min_weight_kg_exclusive == null ? null : req.min_weight_kg_exclusive * 2.2046226218,
      maxLbExclusive:req.max_weight_kg_exclusive == null ? null : req.max_weight_kg_exclusive * 2.2046226218
    };
  }

  function universalLimitPass(req, p) {
    const x = limits(req);
    if (x.minAge != null && p.age_known && p.age < x.minAge) return false;
    if (x.minAgeExclusive != null && p.age_known && p.age <= x.minAgeExclusive) return false;
    if (x.maxAge != null && p.age_known && p.age > x.maxAge) return false;
    if (x.minLb != null && p.weight_known && p.weight_lb < x.minLb) return false;
    if (x.maxLb != null && p.weight_known && p.weight_lb > x.maxLb) return false;
    if (x.minLbExclusive != null && p.weight_known && p.weight_lb <= x.minLbExclusive) return false;
    if (x.maxLbExclusive != null && p.weight_known && p.weight_lb >= x.maxLbExclusive) return false;
    return true;
  }

  function ownerCohortPossible(cohorts, p) {
    return cohorts.some(cohort => Object.entries(cohort).every(([field, allowed]) => {
      if (field === 'required_preferences') return allowed.every(x => p.prefs.has(x));
      if (field === 'prior_procedure' && p.surgery === 'No') return true;
      const answer = p[field];
      return answer == null || [UNKNOWN, 'Suspected / staging incomplete'].includes(answer) || allowed.includes(answer);
    }));
  }

  function matchTrial(trial, p) {
    if (trial.available_for_matching === false) return null;
    if (!CURRENT.has(trial.status_confidence) || !speciesMatches(trial.species, p.species) || !countryMatches(trial, p.country)) return null;
    if (!['treatment','other_treatment_access'].includes(trial.study_type || 'treatment')) return null;
    // A closed site does not close a separately retained active site. Site
    // reconciliation is recorded explicitly, never inferred from prose alone.
    const activeSite = (trial.sites || []).some(site => site.available_for_matching !== false && !BLOCKED.some(x => String(site.status || '').toLowerCase().includes(x)));
    if (BLOCKED.some(x => String(trial.status || '').toLowerCase().includes(x)) && !((trial.inactive_sites || []).length && activeSite)) return null;
    const prefs = p.prefs; const mods = modalities(trial);
    if (prefs.size && mods.size && ![...mods].some(x => prefs.has(x))) return null;
    if (p.approach && !researchApproaches(trial).has(p.approach)) return null;
    const unlisted = p.cancer === "My cancer type isn't listed";
    let broad = false;
    if (unlisted) {
      if (!(trial.broad_disease_families || []).includes('all_tumors') && ((trial.broad_disease_families || []).length || !(trial.cancers_by_species ? trial.cancers_by_species[p.species] || [] : trial.cancers || []).includes('Cancer — any type'))) return null;
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
    [broad] = [false]; const dm = diagnosisMatch(trial, p.cancer, p.species); if (!dm[0]) return null; broad = dm[1];

    const req = trial.requires || {}, exc = trial.excludes || {}, reasons = [], unknown = [];
    if (!universalLimitPass(req, p)) return null;
    let excluded = false;
    const addUnknown = text => unknown.push(text);
    if (req.min_age_years_exclusive != null && !p.age_known) addUnknown(`age strictly above ${req.min_age_years_exclusive} years`);
    if (req.min_weight_kg_exclusive != null && !p.weight_known) addUnknown(`weight strictly above ${req.min_weight_kg_exclusive} kg`);
    if (req.max_weight_kg_exclusive != null && !p.weight_known) addUnknown(`weight strictly below ${req.max_weight_kg_exclusive} kg`);
    for (const group of ['requires', 'excludes']) for (const [key, criterion] of Object.entries(trial[group] || {})) {
      if (criterion == null || criterion === false) continue;
      const rule = PROTOCOL_RULES[group][key];
      if (!rule) throw new Error(`Unclassified matcher constraint: ${group}.${key}`);
      if (rule.when_family && !(FAMILIES[p.cancer] || []).includes(rule.when_family)) continue;
      if (rule.when_field && !Object.entries(rule.when_field).every(([field, allowed]) => allowed.includes(p[field]))) continue;
      if (rule.alternative_owner_cohorts) { excluded ||= !ownerCohortPossible(criterion, p); continue; }
      if (rule.handled) continue;
      if (rule.confirmation_or_appendicular_osa) {
        if (p.diagnosis_status === 'Suspected / not confirmed' &&
            (p.cancer !== 'Osteosarcoma' || p.osa_location === 'Axial — skull, spine, rib, or pelvis')) excluded = true;
        addUnknown(`required ${rule.label}`);
        continue;
      }
      if (rule.history_or_preference) {
        const option = rule.history_or_preference, answer = p[option.field];
        if (!option.allowed.includes(answer)) {
          if (answer != null && answer !== UNKNOWN && !prefs.has(option.preference)) excluded = true;
          else addUnknown(`required ${rule.label}`);
        }
        continue;
      }
      const answer = rule.field ? p[rule.field] : null;
      if (rule.allowed && answer != null && answer !== UNKNOWN) excluded ||= !rule.allowed.includes(answer);
      else if (rule.disallowed && answer != null && answer !== UNKNOWN) excluded ||= rule.disallowed.includes(answer);
      else if (rule.preference) { excluded ||= !prefs.has(rule.preference); addUnknown(`required study ${rule.preference.toLowerCase()}`); }
      else addUnknown(`${group === 'requires' ? 'required ' : 'exclusion: '}${rule.label}${criterion === true ? '' : ': ' + criterion}`);
    }
    if (req.confirmed) { if (p.diagnosis_status === 'Suspected / not confirmed') excluded = true; else if (p.diagnosis_status === UNKNOWN) addUnknown('pathology/cytology confirmation of the diagnosis'); }
    if (req.active_treatment_target) { if (['Completely removed — clean margins','No evidence of disease (NED)'].includes(p.tumor_status)) excluded = true; else if ([UNKNOWN,'Removed — margins unknown','Removed — incomplete/dirty margins'].includes(p.tumor_status)) addUnknown('whether an active treatment target is present'); }
    if (req.measurable_or_lung_metastasis) { if (!['Tumor still present / measurable','Local recurrence'].includes(p.tumor_status) && p.metastasis === 'No known metastases') excluded = true; else if (p.tumor_status === UNKNOWN || [UNKNOWN,'Suspected / staging incomplete'].includes(p.metastasis)) addUnknown('whether measurable disease or lung metastasis is present'); }
    for (const [key, field, text] of [['standard_therapy_unavailable','standard_therapy_unavailable','whether standard anticancer treatment is no longer appropriate or feasible'],['large_inoperable_or_rt_preferred','large_inoperable_or_rt_preferred','whether the tumor is large/inoperable or radiotherapy is preferred to surgery'],['surgery_or_rt_not_possible','surgery_or_rt_not_possible','whether curative surgery/radiotherapy is no longer possible'],['ct_and_current_biopsy','ct_and_current_biopsy','whether current CT and biopsy requirements can be met']]) if (req[key]) { if (p[field] === 'No') excluded = true; else if (p[field] === UNKNOWN) addUnknown(text); }
    const priorRules = [['prior_local_radiation','radiation',['Previously received','Currently receiving'],'whether prior local radiation is excluded'],['prior_surgery','surgery',['Yes'],'whether prior surgery is excluded'],['prior_chemo','chemo',['Previously received','Currently receiving'],'whether prior chemotherapy is excluded'],['prior_immunotherapy','immunotherapy_history',['Previously received','Currently receiving'],'whether prior immunotherapy is excluded'],['prior_steroids','steroids',['Previously took','Currently taking'],'whether previous systemic steroid treatment is excluded (topical-only use needs study-team review)']];
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
    if (Array.isArray(req.lymphoma_response)) { if (p.lymphoma_response === UNKNOWN || p.lymphoma_response == null) addUnknown('required lymphoma response to treatment'); else if (!req.lymphoma_response.includes(p.lymphoma_response)) excluded = true; }
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
    if (broad) { confidence = 'Potential broad-treatment trial — prescreening required'; addUnknown('investigator must confirm diagnosis-specific eligibility'); }
    if (trial.owner_prescreen_required || trial.broad_disease_fallback || trial.requires_site_screening || trial.freshness_unresolved) confidence = broad ? 'Potential broad-treatment trial — prescreening required' : 'Possible match';
    if (trial.study_type === 'other_treatment_access') { confidence = 'Other treatment-access opportunity'; reasons.splice(0, reasons.length, 'funded/assisted standard anticancer treatment is available through this study pathway', ...reasons.filter(x => x !== 'diagnosis reported as confirmed')); }
    return {confidence, trial, reasons, unknown:uniq(unknown)};
  }

  function resultText(matches) {
    const lines = ['Clinical Trial Finder Results'];
    for (const m of matches) { const t=m.trial, locations=(t.sites || []).map(x=>x.address || [x.hospital,x.city,x.state].filter(Boolean).join(', ')).join('; ') || t.address || [t.center,t.country].filter(Boolean).join(', '); lines.push('',m.confidence,t.center || '',t.title || '',`Where: ${locations}`,`Costs / coverage: ${t.funding || 'Ask the study team about covered study costs'}`,`Why: ${m.reasons.join('; ')}.`,m.unknown.length?`Confirm: ${m.unknown.join('; ')}.`:'',`Contact: ${t.contacts || t.contact || 'Contact the study team through the official study page'}`,`Full study details: ${t.registry_url || t.url || ''}`,`Status: ${t.status || ''} · Last verified: ${t.verified || 'date not recorded'}`); }
    lines.push('','Recruitment and eligibility can change; confirm current status with the study team.'); return lines.filter(x => x !== '').join('\n');
  }

  const milesBetween = (a, b) => {
    const rad = n => n * Math.PI / 180, r = 3958.8;
    const dLat=rad(b[0]-a[0]), dLon=rad(b[1]-a[1]), p1=rad(a[0]), p2=rad(b[0]);
    return 2*r*Math.asin(Math.sqrt(Math.sin(dLat/2)**2+Math.cos(p1)*Math.cos(p2)*Math.sin(dLon/2)**2));
  };
  async function sortByZip(matches, zip) {
    const cleaned=String(zip||'').replace(/\D/g,'').slice(0,5);
    if(cleaned.length!==5) return {matches, origin:''};
    try {
      const response=await fetch(`https://api.zippopotam.us/us/${cleaned}`);
      if(!response.ok) return {matches, origin:'ZIP code not recognized. Results are shown in their usual order.'};
      const data=await response.json(), place=data.places[0], origin=[Number(place.latitude),Number(place.longitude)];
      matches.forEach(m=>{const ds=(m.trial.sites||[]).filter(s=>Number.isFinite(s.lat)&&Number.isFinite(s.lon)).map(s=>milesBetween(origin,[s.lat,s.lon]));m.distance=ds.length?Math.min(...ds):null});
      matches.sort((a,b)=>(a.distance??Infinity)-(b.distance??Infinity));
      return {matches, origin:`Sorted by approximate distance from ${place['place name']}, ${place['state abbreviation']}.`};
    } catch { return {matches, origin:'ZIP lookup is unavailable. Results are shown in their usual order.'}; }
  }

  function render(matches) {
    if (!matches.length) { results.innerHTML='<h2>Results</h2><div class="no-results">No plausible matches were found among the currently listed trials. This does not mean that no suitable study exists — recruitment and eligibility can change. Review the treatment options you selected or check again as recruitment changes.</div>'; return; }
    const cards = matches.map(m => { const t=m.trial, url=t.registry_url || t.url || '', sites=(t.sites || []).map(x=>esc(x.address || [x.hospital,x.city,x.state].filter(Boolean).join(', '))).join('; '), where=sites || esc(t.address || [t.center,t.country].filter(Boolean).join(', ')); return `<article class="result-card"><h3>${esc(m.confidence)} · ${esc(t.center)}</h3><h4>${esc(t.title)}</h4><p><strong>Where:</strong> ${where}</p>${m.distance!=null?`<p><strong>Approximate distance:</strong> ${Math.round(m.distance)} miles</p>`:''}${t.intervention?`<p><strong>What is offered:</strong> ${esc(t.intervention)}</p>`:''}<p><strong>Costs / coverage:</strong> ${esc(t.funding || 'Ask the study team about covered study costs')}</p><p><strong>Study type:</strong> ${esc(String(t.study_type || 'treatment').replaceAll('_',' '))}</p><p><strong>Why it may fit:</strong> ${esc(m.reasons.join('; '))}.</p>${m.unknown.length?`<p><strong>Needs confirmation:</strong> ${esc(m.unknown.join('; '))}.</p>`:''}<p><strong>Contact:</strong> ${esc(t.contacts || t.contact || 'Contact the study team through the official study page')}</p>${url?`<a class="result-link" href="${esc(url)}" target="_blank" rel="noopener">View full study details →</a>`:''}<details><summary>Study information</summary><p><strong>What the study says:</strong> ${esc(t.notes || '')}</p><small>Status: ${esc(t.status || '')} · Last verified: ${esc(t.verified || 'date not recorded')}</small></details></article>`; }).join('');
    const distanceNote=matches.distanceNote?`<p class="distance-note">${esc(matches.distanceNote)}</p>`:'';
    results.innerHTML=`<h2>Results</h2>${distanceNote}<p class="result-summary">${matches.length} oncology opportunity(ies) may be worth contacting</p>${cards}<div class="result-actions"><button type="button" id="copy-results">Copy results</button><button type="button" id="print-results">Save / print PDF</button></div>`;
    document.querySelector('#copy-results').addEventListener('click', async e => { await navigator.clipboard.writeText(resultText(matches)); e.currentTarget.textContent='Results copied'; });
    document.querySelector('#print-results').addEventListener('click', () => window.print());
  }

  function updateForm() {
    const p=patient(), cancer=p.cancer, browse=cancer==='Cancer — any type', unlisted=cancer==="My cancer type isn't listed", hematologic=LYMPHOMA.has(cancer)||['Cutaneous epitheliotropic lymphoma','Acute myeloid leukemia'].includes(cancer);
    show('.unlisted-only',unlisted); show('.specific-only',!browse&&!unlisted); show('.solid-only',!browse&&!unlisted&&!hematologic&&cancer!=='Brain tumor / glioma');
    show('.brain-only',cancer==='Brain tumor / glioma'); show('.lymphoma-only',LYMPHOMA.has(cancer)||cancer==='Cutaneous epitheliotropic lymphoma'); show('.aml-only',cancer==='Acute myeloid leukemia');
    show('.mct-only',cancer==='Mast cell tumor'); show('.osa-only',cancer==='Osteosarcoma'); show('.hsa-only',cancer==='Hemangiosarcoma'); show('.procedure-only',p.surgery==='Yes'&&['Osteosarcoma','Hemangiosarcoma'].includes(cancer));
    const candidates=trials.filter(t=>speciesMatches(t.species,p.species)&&countryMatches(t,p.country)&&(browse||unlisted||diagnosisMatch(t,cancer,p.species)[0])); const req=new Set(candidates.flatMap(t=>Object.keys(t.requires||{}))), exc=new Set(candidates.flatMap(t=>Object.keys(t.excludes||{})));
    show('.protocol-standard',!browse&&!unlisted&&req.has('standard_therapy_unavailable')); show('.protocol-large',!browse&&!unlisted&&req.has('large_inoperable_or_rt_preferred')); show('.protocol-no-local',!browse&&!unlisted&&req.has('surgery_or_rt_not_possible')); show('.protocol-ct-biopsy',!browse&&!unlisted&&req.has('ct_and_current_biopsy'));
    show('.steroids-only',!browse&&!unlisted&&(exc.has('current_steroids')||exc.has('prior_steroids')||req.has('steroid_washout_days'))); show('.immunosuppressive-only',!browse&&!unlisted&&exc.has('immunosuppressive')); show('.radiation-plan-only',!browse&&!unlisted&&req.has('planned_radiation'));
    show('.zip-only',p.country==='USA');
    const note=document.querySelector('.browse-note'); note.hidden=!browse&&!unlisted; note.textContent=browse?'Browse mode: disease-specific eligibility is not used until a cancer type is selected.':'Unlisted diagnosis: only genuinely all-tumor treatment programs will be shown for investigator review.';
    form.querySelector('.matcher-submit').disabled=!cancer;
  }

  function applyUrlPreset() {
    const hash = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : '';
    const params = new URLSearchParams(hash || window.location.search);
    const species = params.get('species');
    const country = params.get('country');
    const cancer = params.get('cancer');
    const approach = params.get('approach');
    if (['Dog', 'Cat'].includes(species)) form.elements.species.value = species;
    if ([...form.elements.country.options].some(option => option.value === country)) form.elements.country.value = country;
    if (URL_CANCER_LABELS[cancer] && ![...form.elements.cancer.options].some(option => option.value === cancer)) form.elements.cancer.add(new Option(URL_CANCER_LABELS[cancer], cancer));
    if ([...form.elements.cancer.options].some(option => option.value === cancer)) form.elements.cancer.value = cancer;
    if (form.elements.approach && [...form.elements.approach.options].some(option => option.value === approach)) form.elements.approach.value = approach;
    return params.get('autostart') === '1' && Boolean(form.elements.cancer.value);
  }

  if (typeof window !== 'undefined') window.__MATCHER_TEST__ = {matchTrial, diagnosisMatch, modalities, researchApproaches};
  if (!form || !results) return;
  const autoStart = applyUrlPreset();
  form.addEventListener('change',event=>{ updateForm(); if(event.target.name==='country' && form.elements.cancer.value) form.requestSubmit(); });
  form.addEventListener('submit',async e=>{e.preventDefault(); if (!(await catalogReady)) return; const p=patient(), matches=trials.map(t=>matchTrial(t,p)).filter(Boolean); matches.sort((a,b)=>{const rank=x=>x==='Likely match'?0:x==='Possible match'?1:2; return rank(a.confidence)-rank(b.confidence)+(Number(Boolean(a.trial.early_phase))-Number(Boolean(b.trial.early_phase)));}); const sorted=await sortByZip(matches,p.country==='USA'?p.zip_code:''); sorted.matches.distanceNote=sorted.origin; render(sorted.matches); results.scrollIntoView({behavior:'smooth',block:'start'});});
  const catalogReady = fetch(window.MATCHER_DATA_URL).then(r=>{if(!r.ok)throw new Error(`Catalog ${r.status}`);return r.json();}).then(data=>{trials=data;updateForm();if(autoStart)form.requestSubmit();return true;}).catch(()=>{results.innerHTML='<div class="no-results">The trial catalog could not be loaded. Please try again shortly.</div>';return false;});
})();
