# Manual continuation 03 — 2026-10-17

Scope: targeted current primary sources. Not 113-source audit. Publication of data: NONE; no records silently changed.

1. Tufts SBRT primary pulmonary carcinoma, https://vet.tufts.edu/clinical-trials/sbrt-canine-lung-tumor-study : study explicitly requires "No previous treatment for the lung tumor" (lines 44-48), not "no lifetime prior chemo/surgery/RT/immunotherapy." Existing `tufts-primary-pulmonary-carcinoma-sbrt` has unconditional `excludes.prior_chemo/prior_radiation/prior_surgery/prior_immunotherapy=true`. Requires matcher-scope correction with source-derived regression cases before catalog edit; avoid widening unsafe prior treatment of target tumor. The issue remains VERIFIED DISCREPANCY, NOT FIXED.

2. Penn CIP https://www.vet.upenn.edu/research/research-programs/comparative-immunotherapy-program/clinical-trials/ visibly lists B-cell CAR-T and preconditioning steps; former AVMA Suspended signal remains unresolved as same-cohort real-time enrollment conflict. NO status change.

3. Purdue https://vet.purdue.edu/wcorc/clinical-trials/ top-level "We are currently recruiting" under Emerging Canine Cancer Studies mentions "Immunotherapy Trial of New Cancer Vaccine", but protocol detail https://vet.purdue.edu/wcorc/clinical-trials/emerging-canine-cancer.php explicitly states 'Enrollment Closed' under PD-L1 vaccine. This is a primary-source within-site contradiction: study-level CLOSED takes precedence over umbrella summary. Do NOT add it as enrolling. Other Purdue HIFU lymphoma, OSA and H-FIRE liver studies have existing distinct canonical IDs `purdue-hifu-lymphoma`, `purdue-hifu-osteosarcoma`, `purdue-hfire-liver-cancer`. M029 has existing `purdue-m029-shp1-inhibitor` nonmatching due to early research/uncertain direct care. Do NOT conflate PD-L1 vaccine with Purdue bladder anti-PD-L1 monoclonal antibody.

4. Minnesota https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials : CAR-T CD20+ B-cell lymphoma 'On hold', ORBIT VSV+PD-1 'Open and enrolling', feline mammary olaparib+meloxicam 'Open and enrolling', AAV oral melanoma vaccine 'Open and enrolling'; early-detection COED and LyRA blood collection not treatment. These are master-index signals; primary protocol detail remains required for full-fresh review.

5. Cornell https://www.vet.cornell.edu/open-veterinary-clinical-trials-are-currently-recruiting : includes palliative cancer pain epidural study; must review actual study protocol to decide treatment-scope eligibility and identity rather than auto-add.

No new uniquely confirmed matchable trial in THIS bounded batch. Global NEW count remains NOT VERIFIED. No production code/data changes. 40 preexisting fresh protocol gaps remain distinct.

