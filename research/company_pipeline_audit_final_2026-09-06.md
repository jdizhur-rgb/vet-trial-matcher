# Companion-animal oncology developer/access audit — 2026-09-06

Scope: US/Canada-focused drug developers, biotech/pharma, academic translational programs, CRO/specialty networks, regulatory disclosures, and non-trial treatment access. Dogs/cats only. Treatment-focused filter applied. Duplicate identity is based on protocol/drug/site/indication rather than title alone.

## A. Active treatment opportunities — retain/add only after effective-DB identity check

### LEAH Labs — CAR-T for canine B-cell lymphoma
- Status: **OPEN / actively enrolling**.
- Sites: University of Minnesota, Ohio State University, University of Missouri.
- Funding: fully funded; treatment provided at no cost to enrolled families.
- Source: https://leahlabs.com/
- DB disposition: no exact LEAH hit found by repo code search; **candidate for production add**.

### Aurelius Biotherapeutics + Lytix Biopharma — canine B-cell lymphoma
- Treatment: oncolytic peptide + T-cell immunotherapy.
- Status: **RECRUITING initial pilot**.
- Key public eligibility: previously untreated B-cell lymphoma, stage 3–5(a); most study treatment in Bellingham, WA.
- Funding: fully funded; no additional owner expense stated.
- Source: https://aureliusbio.com/
- DB disposition: no exact Aurelius hit found by repo code search; **candidate for production add**.

### University of Minnesota — TriKE + hypofractionated RT for canine sarcoma
- Status: **OPEN / enrolling**.
- Treatment: novel TriKE immunotherapy plus hypofractionated radiation.
- Public criteria include confirmed sarcoma >=2 cm and weight >=7 kg.
- Source: https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/trike-new
- DB disposition: no exact TriKE repo-code hit in audit search; **candidate for production add unless effective merged DB contains title variant**.

### Akston AKS-701d — canine bladder/urothelial cancer, Purdue
- Status: client-owned dogs are being treated in Purdue clinical program; SEC disclosure reported 34 enrolled as of March 2026. Higher-dose work and a later-2026 pivotal multi-site program are planned.
- Source: https://www.sec.gov/Archives/edgar/data/1776612/000110465926041980/tm2516611-24_s1a.htm
- DB disposition: **do not create from SEC alone until current owner-facing enrollment route is confirmed**. Keep current Purdue program separate from planned pivotal program.

### Akston AKS-619d — PD-L1-directed program, Purdue
- Status: client-owned dogs have been dosed in a multi-tumor clinical program.
- DB disposition: **verify current owner enrollment route before production matching**; otherwise watchlist.

### CASTR / VRCCO T-cell engager study — canine STS
- Status: enrolling; all qualifying dogs receive investigational intratumoral TCE, followed by surgery; no placebo for study drug.
- Source: https://vrcvet.com/clinical-trials/
- Duplicate disposition: **CASTR and VRCCO references are the same study unless protocol evidence proves otherwise. Merge, never count twice.**

### ELIAS ECIP-OSA-01 — ECI + novel adjuvant after surgery
- Status: **NOW ENROLLING** at University of Missouri.
- Source: https://eliasanimalhealth.com/clinical-studies/canine-osteosarcoma-combined-immunotherapy/
- Duplicate disposition: compare protocol ID. This is distinct from closed ECI-OSA-04, but existing project ELIAS records may already represent ECIP-OSA-01.

### ELIAS ASCENT / ECIC-OSA-01 — ECI + chemotherapy
- Status: ELIAS current clinical-studies page says enrollment open.
- Source: https://eliasanimalhealth.com/clinical-studies/eci-combined-with-chemotherapy/
- Important: no financial assistance is provided for this study.
- Duplicate disposition: protocol identity **ECIC-OSA-01**; do not duplicate generic ECI osteosarcoma entries.

### UT Southwestern VROC — therapeutic protocols
Current VROC page lists multiple treatment protocols, including ferumoxytol + RT for canine glioma, combination novel therapeutics/devices, intratumoral CPMV for solid tumors, RT + histotripsy, CRT-NP/HIFU +/- anti-PD-L1 for melanoma, and intratumoral vs IV carboplatin +/- HIFU for melanoma.
- Source: https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/clinical-trials.html
- DB disposition: **split by actual protocol and deduplicate against existing UTSW records; never create one broad duplicate umbrella record if specific protocols already exist.**

### Johns Hopkins canine osteosarcoma program
- Current Hopkins page reports recruiting treatment research involving cryotherapy/immunotherapy around amputation/chemotherapy.
- Source: https://www.hopkinsmedicine.org/radiology/veterinarians/clinical-trials
- DB disposition: exact protocol/title comparison required before add; likely academic-source overlap.

## B. Other Treatment Access — not ordinary recruiting trials

### ELIAS Cancer Immunotherapy (ECI)
- USDA-licensed autologous prescription product for canine osteosarcoma; commercial treatment access is distinct from ELIAS clinical studies.
- Source: https://eliasanimalhealth.com/elias-cancer-immunotherapy/
- Category: **licensed/novel treatment access**.

### Gilvetmab
- Caninized anti-PD-1; conditionally licensed by USDA for dogs with mast cell tumors or melanoma; available through veterinary oncology specialists.
- Reference: AAHA 2026 oncology guidelines and Merck Animal Health.
- Category: **conditionally licensed treatment**.

### Laverdia / verdinexor
- FDA full approval for canine lymphoma in 2026.
- Category: **approved treatment**, not trial.

### STELFONTA / tigilanol tiglate
- Approved intratumoral treatment for eligible canine mast cell tumors.
- Category: **approved treatment**, not trial.

### UT Southwestern compassionate-use protocol
- Prospective single-arm compassionate-use pathway for advanced non-resectable tumors in dogs and cats using investigational therapy, chemotherapy, immunotherapy and combinations.
- Source: https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/clinical-trials.html
- Category: **Compassionate / Special Access**.

### Precision-oncology access services
- FidoCure and Anivive SearchLight can identify genomic targets and facilitate/guide targeted treatment choices, often involving off-label human oncology drugs.
- Category: **precision-oncology / treatment-selection access**, with evidence-strength caution. Do not present sequencing itself as anticancer treatment.

## C. Watchlist — real oncology development, but no verified current owner enrollment

- **Vivesto / Paccal Vet — splenic hemangiosarcoma:** recruitment complete June 2026; topline results expected Q3 2026. Watch next study/regulatory step.
- **Unleash Therapeutics / Ardent — K9-ACV + CD200AR-L osteosarcoma:** developer says multicenter randomized efficacy recruitment complete. Do not show as open despite stale/contradictory pages elsewhere.
- **Vetigenics VGS-001 / VGS-002 / CHECKMATE-K9:** current pipeline page labels component studies closed and combination fully enrolled. Watch next cohorts.
- **Anivive eBAT — hemangiosarcoma:** mid-stage; safety/dose and pilot field efficacy completed; manufacturing/CMC validation planning. No verified current owner-enrollment route.
- **Anivive osteosarcoma oral product, INAD I-013511:** in development; no verified current owner-enrollment route.
- **OS Animal Health OST-HER2:** phase 2 results published; company pursuing USDA regulatory path; no current owner enrollment established.
- **Akston AKS-701d pivotal multicenter:** planned for late 2026 when pre-license serial batches are available; do not expose until actually open.
- **University of Minnesota ORBIT (VSV + anti-PD-1 lymphoma):** enrollment **ON HOLD** as of August 2026; no matching while on hold.
- **EVVIVAX Tel-eVax / Erb-eVax listings:** developer site still displays old AAHSD studies, but at least AAHSD000085 carries historic 2019–2021 recruitment dates. Treat developer page as stale until current recruitment is independently confirmed. Do not add as current from the developer page alone.
- **Allogeneic canine NK-cell solid-tumor program (UW/UMN collaborators):** 2026 publication supports active development/future dose escalation, but publication alone is not evidence of current owner enrollment. Watch for next cohort.

## D. Reject from treatment matcher

- NCI longitudinal/sample-collection/biomarker-only studies without protocol-delivered anticancer treatment.
- Prevention studies in healthy/high-risk animals.
- Diagnostic-only genomic tests when no treatment access is part of the opportunity.
- Cancer pain/supportive-care programs whose purpose is not tumor treatment.
- Closed/fully enrolled/on-hold studies presented by stale third-party pages as if open.
- Pipeline assets with only INAD/regulatory/development status and no current client-owned enrollment route.

## E. Duplicate rules established by this audit

1. Match identity using **protocol ID > investigational agent + indication > site/sponsor + treatment schedule**, not page title.
2. Developer page + university page + CRO page for the same protocol = **one opportunity**.
3. Commercial availability and a clinical study of the same product are **different access types**, but must not inflate the clinical-trial count.
4. Planned next-phase/pivotal study is **watchlist**, not a second active trial, until enrollment opens.
5. A closed historic protocol with the same product is not the same record as a new protocol if protocol IDs/designs differ (e.g. ECI-OSA-04 vs ECIP-OSA-01/ECIC-OSA-01).
6. If status conflicts, use the sponsor/developer or recruiting institution's current explicit status; conservative default is **not matchable** until resolved.

## F. Developer/source layer to keep in recurring audits

High-value sources identified: LEAH Labs; Aurelius Biotherapeutics/Lytix; Akston Biosciences SEC disclosures + Purdue; ELIAS Animal Health; Vetigenics; Anivive; Vivesto; Unleash/Ardent; OS Animal Health; CASTR Alliance/VRCCO; UT Southwestern VROC; NCI Comparative Oncology/COTC/PRECINCT; university translational programs (UMN, Purdue, Hopkins, UC Davis, CSU, Tufts, etc.).

## Final disposition

Production matcher should receive only opportunities with **current, verifiable owner enrollment and actual anticancer treatment**. Non-trial but genuinely accessible treatments belong in a separate **Other Treatment Access** layer. Closed/on-hold/planned development stays in **Watchlist**. Stale, supportive, diagnostic, observational and sample-only items stay out.
