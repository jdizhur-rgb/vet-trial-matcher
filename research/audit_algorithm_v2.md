# Veterinary Oncology Discovery Audit v2

Updated: 2026-09-06

## Goal
Find current dog/cat opportunities that provide an actual anticancer treatment. Discovery is source-class based, not just registry/university based.

## Mandatory source classes on every full audit
1. Veterinary university/teaching-hospital current trial catalogs.
2. Private referral and specialty oncology hospitals/networks, including VCS-listed non-university trial sources.
3. CROs, sponsors and multicenter study networks (e.g. ACI-style networks; Europe CRO equivalents).
4. Human medical centers running comparative/translational veterinary oncology programs, NCI comparative oncology programs, PRECINCT-like networks and individual PI/lab pages.
5. Institutional newsrooms, press releases, study announcements, social/recruitment posts and PDFs, not only pages titled Clinical Trials.
6. Separate feline-only discovery pass.
7. Treatment-modality pass independent of cancer name.
8. Compassionate-use / investigational-treatment / expanded-access-style veterinary programs where a real animal patient can receive anticancer treatment.
9. Registries/aggregators (AVMA/VCS/ESVONC etc.) as discovery leads only; current status must be confirmed at a primary source whenever possible.

## Query families
Run combinations of dog/canine, cat/feline, cancer/tumor/neoplasm/oncology plus:
- recruiting, enrolling, now enrolling, seeking dogs/cats, dogs/cats needed, patients wanted, cases wanted, participants wanted, study open, trial open, current study, clinical study, pilot study, funded study, free treatment, new study, experimental treatment, investigational treatment
- chemotherapy, targeted therapy, immunotherapy, checkpoint inhibitor, vaccine, cell therapy, CAR-T, CAR-NK, T-cell engager, cytokine, viral/oncolytic therapy, intratumoral, nanoparticle, mRNA/RNA, gene therapy
- radiation, radiotherapy, stereotactic, SBRT/SRT, proton, FLASH
- surgery, image-guided surgery, ablation, cryoablation/cryotherapy, thermal ablation, microwave ablation, radiofrequency ablation, HIFU, focused ultrasound, histotripsy, photodynamic therapy/PDT, electrochemotherapy/ECT, radioembolization, chemoembolization
- compassionate use, investigational access, special access, treatment access

For Europe, translate the recruitment and treatment concepts into the local languages used in the multilingual sweep.

## Feline pass
Search feline terms independently rather than relying on mixed dog/cat queries. Include at minimum oral SCC, lymphoma, mammary carcinoma, injection-site sarcoma, mast-cell tumor, melanoma, brain tumors and broad solid-tumor studies.

## Inclusion gate
A record enters the matcher only when all are true:
- dog and/or cat patient;
- cancer/neoplasm indication;
- patient receives an anticancer therapeutic intervention (drug, biologic, vaccine, radiation, surgery/device/ablation or therapeutic combination);
- recruitment/access is current enough to support owner matching;
- sufficient disease/intervention/site information exists to make the record useful.

Exclude diagnostic-only, imaging-only, biomarker, sample collection/biobank, observational/natural-history, retrospective, research-only PK and supportive/palliative-only studies where the study itself supplies no anticancer treatment. A mixed study can be represented only by a clearly separable treatment arm.

## Freshness hierarchy
1. Current primary trial page with explicit recruiting/open status.
2. Fresh institutional recruitment announcement/news/PDF with contact and eligibility.
3. Current sponsor/CRO page identifying recruitment and usable indication/intervention/site.
4. Registry/aggregator lead requiring primary-source confirmation.

Closed, completed, suspended/on-hold and stale unconfirmed recruitment go to exclusions/watchlist, not matching.

## Semantic dedup BEFORE insertion
Never treat a new title as a new protocol. Compare candidate against effective catalog (base + updates - deletes) using:
- institution/site/network;
- species;
- cancer/indication and stage/setting;
- intervention(s);
- protocol/study ID when available;
- PI/sponsor;
- recruitment URL(s);
- key eligibility design.

News article + trial page + registry entry + participating-site page for the same protocol = ONE canonical opportunity unless they are genuinely distinct cohorts/protocols with different treatment/eligibility. Keep alternate source URLs as evidence instead of separate records.

## Multisite rule
One protocol offered at several hospitals is one protocol record unless the product UI intentionally models sites separately. Site availability belongs in sites/locations metadata, not duplicate trial records.

## Audit output
For every full pass record:
- sources/classes checked;
- candidates reviewed;
- canonical new treatment protocols added;
- existing protocols refreshed;
- semantic duplicates skipped/collapsed;
- excluded diagnostic/observational/supportive/closed candidates;
- watchlist items needing recruitment confirmation;
- final effective treatment count.

## Learning rule
Whenever a real missed treatment opportunity is found, classify WHY it was missed (source class, wording, language, modality, stale index, hidden PDF/news/PI page, sponsor/CRO, etc.) and add that discovery path to this document and to the recurring audit prompt. The purpose is to reduce repeated blind spots, not merely patch individual records.
