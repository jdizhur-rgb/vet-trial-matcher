# Osteoarthritis trial discovery — 2026-09-16

Research-only inventory. Not connected to the live matcher or cancer catalog. Candidate studies are included only after checking a current primary institutional/clinical source where possible. Closed/historical studies are tracked separately to avoid false positives.

## Active / current candidates

### NC State — GOS prebiotic / gut-health study — canine OA pain
- Species: Dog
- Type: interventional, supplement, double-blind
- Current evidence: NC State page published 2026-08-12 states enrolling dogs with osteoarthritis or mobility problems.
- Key matching fields visible: OA or mobility problems; imaging and gait/standing assessment performed by study.
- Source: https://cvm.ncsu.edu/clinical-trial/gi-supplement-clinical-study/
- Status: ACTIVE / PRIMARY SOURCE CONFIRMED

### NC State / Duke — emotional and cognitive domains in dogs with/without chronic OA pain
- Species: Dog
- Type: observational/assessment, not treatment
- Enrollment window: 2026-01-05 through 2026-12-31
- Key eligibility: healthy OR signs of OA pain; age 2–10 years; medium/large breed; comfortable with new places/people.
- Source: https://cvm.ncsu.edu/clinical-trial/assessing-emotional-and-cognitive-domains-in-dogs/
- Status: ACTIVE / PRIMARY SOURCE CONFIRMED / OBSERVATIONAL

### University of Minnesota — FEHI / feline SEHI for OA
- Species: Cat
- Type: interventional pain treatment
- Current evidence: UMN Current Clinical Trials lists FEHI as Open and enrolling.
- Key eligibility visible at catalog level: radiographic evidence of osteoarthritis; novel painkiller.
- Source: https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials
- Status: ACTIVE / PRIMARY SOURCE CONFIRMED

### Cornell — radiofrequency therapy for chronic OA pain
- Species: Dog
- Type: interventional pain treatment; RFA / pulsed radiofrequency
- Key eligibility: Cornell CUHA patient; stifle/knee pain difficult to control with other treatments.
- Follow-up: force-mat evaluation; procedure under heavy sedation/anesthesia; reassessment at 2 weeks, 4 weeks, and 3 months.
- Source: https://www.vet.cornell.edu/hospitals/clinical-trials/radiofrequency-therapy-pain-management-dogs
- Status: CURRENT CORNELL CLINICAL-TRIAL PAGE / ENROLLMENT WORDING TO RECONFIRM

### Cornell — FDA-approved stem-cell trial for musculoskeletal disease including OA
- Species: Dog (also horses in broader protocol)
- Type: interventional regenerative medicine
- Conditions include osteoarthritis, hip/elbow dysplasia and other musculoskeletal/nerve disease.
- Cornell Sports Medicine page currently directs owners to contact the service to determine candidacy and describes this as a new clinical trial.
- Sources:
  - https://www.vet.cornell.edu/hospitals/services/sports-medicine-and-rehabilitation
  - https://www.vet.cornell.edu/about-us/news/20240611/fda-approves-cornell-stem-cell-trial-dogs-and-horses
- Status: CURRENT PROGRAM / ENROLLMENT TO RECONFIRM

### University of Tennessee — collar for lameness and osteoarthritis in dogs
- Species: Dog
- Type: listed under Active Clinical Trials
- Source: https://vetmed.tennessee.edu/research/clinical-trials/
- Status: ACTIVE LISTING / DETAIL PAGE AND ELIGIBILITY STILL NEEDED

## Current institutional sources checked with no confirmed additional OA treatment trial yet
- University of Florida current small-animal trials: mobility/osteoarthritis research category exists; the readily indexed mitragynine OA trial is explicitly CLOSED and is not an active candidate.
- UC Davis VCCT: current-trial portal checked; old indexed OA medication trial is historical and not accepted as current without a present StudyPages record.
- Penn Vet current recruiting catalog checked; no OA candidate established in this pass.
- Texas A&M current clinical-trials program checked; historical orthopedic/OA-related studies were not treated as current.
- Illinois: current OA educational material found, but no current OA clinical trial confirmed in this pass.

## Excluded / historical — do not import as active

### University of Florida — mitragynine for naturally occurring canine OA pain
- Official page explicitly says CURRENTLY CLOSED.
- Source: https://research.vetmed.ufl.edu/research-programs/clinical-trials/small-animal/evaluation-of-the-effect-of-mitragynine-on-naturally-occurring-osteoarthritic-pain-in-a-canine-model-a-prospective-randomized-crossover-double-blinded-placebo-controlled-clinical-trial/

### Cornell — bedinvetmab for naturally occurring elbow OA
- Grant/project period July 2024–June 2025; not treated as recruiting in 2026.
- Source: https://www.vet.cornell.edu/research/awards/prospective-double-blind-randomized-placebo-controlled-clinical-trial-bedinvetmab-dogs-naturally

### University of Minnesota — historical OA studies
- UMN completed-studies page includes prior feline amantadine, canine nutraceutical and synovial-fluid biomarker OA studies; all excluded from active inventory.
- Source: https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/completed-clinical-studies

## Matching-field schema emerging from current trials
- species
- age / age range
- weight / size class
- confirmed OA vs owner-observed mobility signs
- radiographic OA required / obtained at screening
- affected joint / stifle-specific vs any appendicular joint vs multi-joint
- duration of pain / lameness
- refractory or inadequately controlled pain
- current analgesics / NSAIDs / anti-NGF monoclonal antibodies
- medication washout requirements
- prior intra-articular injections / orthobiologics
- prior orthopedic surgery and timing
- joint instability / underlying orthopedic disease
- neurologic disease affecting gait
- major systemic comorbidity
- temperament / ability to complete gait or behavioral testing
- geographic/site requirement and follow-up burden
- treatment vs observational study

## Discovery rules
1. Aggregators and search results are discovery signals only.
2. Prefer a current university, hospital, sponsor, CRO or registry primary page before marking active.
3. A multicenter protocol is one trial with multiple sites, not multiple trials.
4. Match duplicates by intervention + condition + protocol/PI + eligibility, not title alone.
5. Do not import closed, completed, stale, or ambiguous historical pages as active.
6. Keep observational OA studies separate from treatment trials so the future matcher can default to treatment options.
