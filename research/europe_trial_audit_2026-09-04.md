# Deep Europe veterinary oncology trial audit — 2026-09-04

Scope: client-owned dogs/cats receiving an anticancer intervention. Exclude diagnostic/biomarker-only, observational, sample-only and supportive-care studies. Current status must be verified before promotion to matcher.

## Final audit result

A full cross-check was completed against the current ESVONC monthly list, the full Oncowaf database, primary university/referral-hospital pages, sponsor/development pages, investigator names, and local-language searches. The apparent large Europe gap found on 2026-09-04 was mostly a discovery/reporting gap rather than a remaining catalog gap: the treatment records below were already present in `pages/1_Clinical_Trial_Finder.py` from the September 3 audit. They must not be duplicated.

## Current treatment records confirmed present in the matcher catalog

### France
- CHV AniCura Armonia — HIFU for canine urothelial carcinoma. Current primary AniCura page and ESVONC/Oncowaf confirm the active anticancer study. Conventional treatment must be refused, infeasible, or failed; anesthesia must be possible.
- VetAgro Sup Lyon — intratumoral immunotherapy for stage I-III canine oral melanoma/oral SCC with measurable disease. Current Oncowaf/ESVONC listing; primary VetAgro program previously verified.
- CHV Frégis — thermoablation for canine primary HCC/limited hepatic metastases.
- CHV Frégis — local thermoablation for canine chemodectoma.
- CHV Frégis — embolization/chemoembolization for primary hepatic tumors or liver metastases.

### Belgium
- Ghent University — oral GCN2-IN-6 before and after mastectomy for feline mammary tumors. Primary Ghent owner and referring-veterinarian pages actively invite eligible cats; investigational drug is supplied without additional cost.

### Netherlands
- Utrecht University OnGo — local vaccinia/oncolytic viral therapy injected into/around primary canine osteosarcoma 7-10 days before planned surgery. Current Utrecht interventional page + ESVONC ongoing listing. Existing matcher row appropriately requires owner prescreen because slot availability is not explicitly published.
- RVC-led toceranib insulinoma study includes Veterinary Clinic Nieuwegein as a Netherlands site, but RVC metadata gave an end date of 31 May 2026; keep needs-reconfirmation rather than claiming a confirmed slot.
- Utrecht holmium-166 microsphere brain-tumor treatment and feline oral-SCC nanobody-PDT remain therapeutic research leads without explicit current owner enrollment; keep out of automatic matching.
- Versican-targeted urothelial-carcinoma vaccine and CimCure HSA vaccine remain contact/watch leads unless current enrollment is directly reconfirmed.

### Italy
- AniCura I Portoni Rossi Bologna + University of Teramo — autologous hydroxyapatite-based vaccine for canine mucosal melanoma. Oncowaf currently lists it as ongoing. Primary tumor tissue must still be available; FFPE-only after prior excision is not sufficient.
- University of Milan/Lodi — OncoFAP-MMAE Phase I-II targeted chemotherapy for FAP-positive advanced solid tumors is already in the catalog; owner-facing protocol page was previously verified.
- Bologna University historical appendicular OSA immunotherapy study is explicitly CONCLUDED; do not import.
- Pisa/EVVIVAX vaccine programs remain contactable but not matchable without current site-level enrollment confirmation.

### Portugal
- AniCura Atlântico, Mafra — microwave/radiofrequency thermoablation for HCC/limited hepatic metastases.
- AniCura Atlântico, Mafra — microwave treatment for chemodectoma. Keep detailed tumor-size gating out until the apparent public criterion typo is clarified.
- University of Évora — photodynamic therapy for canine mammary tumors remains listed by current Oncowaf; investigator-level status should still be confirmed before making stronger owner-facing claims than the database listing supports.

### United Kingdom
- Royal (Dick) School Edinburgh — intratumoral tigilanol tiglate for canine oral melanoma. Current ESVONC ongoing list and Edinburgh trial material support the existing record.
- RVC multicenter toceranib study for metastatic/recurrent insulinoma remains listed by ESVONC/Oncowaf, but RVC project metadata ended 31 May 2026; existing `needs_reconfirmation` handling is correct.
- Liverpool DOG-FIGhT ferumoxytol/radiotherapy glioma program and NDSR high-grade mammary carcinoma trial were already found in the prior deep pass.

### Spain
- Universidad Complutense de Madrid — CANCIMPET intratumoral CPMV immunotherapy for poor-prognosis mammary cancer in dogs/cats is already in the catalog from the local-language audit. This is a real owner-recruiting anticancer treatment project and remains a high-value Spain record.
- Immuvera Nebumet Spain is an announced multicenter registration-study lead only; sites/live owner enrollment not verified, so do not match yet.

### Sweden
- SLU/Oxcia — **Silver Bullet 2.0 / OXC-101** is a genuine new 2026-2030 therapeutic research program. SLU's current page, updated May 2026, states start September 2026 and evaluates home-based oral OXC-101 in dogs with lymphoma, hemangiosarcoma and mammary tumors. AACR 2026 reports the preceding open-label pilot in nine pet dogs with lymphoma/HSA. However, the SLU project page does not yet publish an owner recruitment notice, sites, or eligibility. Existing catalog watch row should remain `available_for_matching=False` until enrollment is explicitly opened. Important correction to old note: the new Silver Bullet 2.0 project runs **September 2026-August 2030**, not 2023-2025.
- Vivesto Cantrixil canine pilot remains planned H2 2026 with no verified owner-facing recruitment/site details; watch only.

### Switzerland
- Current Zurich treatment trials already represented include sinonasal heterogeneous-dose RT, high-grade glioma chemoradiation, large-tumor lattice/SBRT, feline oral-SCC FLASH, oral vinorelbine Phase I, ADAM-12 vaccine for feline STS, and PNST fluorescence-guided surgery. Imaging/diagnostic-only Zurich projects remain excluded under treatment-only rules.

## Deep negative regional sweep — no additional matchable treatment trial verified

### Germany
Deep searches of Hannover TiHo, FU Berlin, Leipzig/Giessen-style university sources, German-language trial terms, sponsor programs and Oncowaf did not produce an additional current owner-recruiting anticancer treatment study beyond the already cataloged/announced Immuvera Nebumet Germany lead. TiHo has substantial oncology infrastructure (chemotherapy, surgery, RT, cytogenetics, flow cytometry, gene therapy research), but infrastructure/research themes are not recruitment evidence.

### Austria
Vetmeduni Vienna has active specialist oncology/radiation oncology and comparative-oncology infrastructure. No additional current owner-recruiting experimental anticancer treatment protocol was verified. Historical/planned anti-EGFR canine IgE immunotherapy remains a translational lead, not a current match.

### Czechia
VETUNI Brno and Animed/Pfeifr remain important investigator/referral leads. The Animed canine melanoma 'biological/vaccine' treatment pathway has not been identified with enough certainty to create a new experimental-treatment trial record. No additional current recruiting treatment study verified.

### Poland
SGGW Warsaw nano-oncology remains active translational research: gold nanoparticles for canine OSA/metastases and feline injection-site sarcoma, targeted/photothermal platforms, and related delivery work. Current published evidence located remains preclinical/in-vitro/ex-ovo and no client-owned treatment recruitment was verified. Gdańsk canine PD-1/TIM3 antibody development is an important future immunotherapy lead but not yet a clinical treatment trial. Do not promote.

### Denmark
University of Copenhagen has strong comparative oncology and published clinical FLASH experience in canine spontaneous tumors. The indexed program describes the initial feasibility cohort and plans for subsequent Phase I/II work, but this audit did not verify a current 2026 owner-recruiting treatment protocol. Keep as research pipeline/watch, not matcher.

### Finland / Norway / Ireland / Hungary
Institutional/local-language searches did not verify a current owner-recruiting canine/feline anticancer treatment study meeting our rules. Clinical oncology services, ECT availability, publications, registries, or research projects alone were not treated as trials.

### Slovenia
Ljubljana ECT + canine IL-12 gene electrotransfer remains scientifically active and clinically important, but the prior funded protocol ended and no current owner-recruiting prospective protocol was verified. VetInspECT is useful for center discovery but is a registry/network, not a trial.

### Cyprus
FUSVET focused-ultrasound pilot treated spontaneous tumors in dogs/cats, but current continuation/recruitment was not verified. Watch only.

## Explicit exclusions retained

- Ghent fluorescence lifetime/ICG intraoperative imaging: diagnostic/surgical guidance, not a new anticancer treatment under current product rules.
- Liège urothelial biomarker/immune-response study: no anticancer intervention.
- Ghent doxorubicin cardiotoxicity ultrasound: monitoring/supportive research.
- Paccal Vet canine HSA and feline solid-tumor pilots: recruitment completed in 2026; watch results/new cohorts.
- Historical Bologna OSA immunotherapy: concluded.
- Generic oncology services, standard chemotherapy/RT/ECT, registries and tissue/sample projects: not treatment trials.

## Refresh rules after this audit

1. ESVONC monthly list and full Oncowaf must both be checked; ESVONC explicitly says its monthly list is non-exhaustive.
2. Verify each apparent ongoing trial against the primary center/investigator page when available.
3. Search local languages + investigator names + grants + referral hospitals; Europe frequently lacks a central owner-facing trial page.
4. Highest-priority watch items: SLU OXC-101 Silver Bullet 2.0, SGGW nano-oncology, Gdańsk PD-1/TIM3, Ljubljana IL-12 GET, Utrecht NB-PDT/holmium, CimCure vaccine programs, Immuvera Nebumet, Vivesto Cantrixil.
5. Never promote a grant, publication, laboratory project, historical cohort, or 'clinical capability' as current recruitment.
6. Zero results for a country/cancer is preferable to a false recruiting claim.
