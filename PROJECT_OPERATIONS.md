## E01–E04 and remaining E05/E06 clinic packages — 2026-10-13

The owner authorized publication of all latest unpublished clinic packages. The five proposal files cover 127 source identities (network sources and aliases included); they are not 127 new hospitals. Preserve earlier A/B/C/D/P00 changes and raw ACVIM history. Evidence, original decisions, integration exceptions and remaining questions are in `research/audit-runs/e-packages-publish-20261012/`.

Later branch-scoped TMC evidence takes precedence over E01 group-level modalities: retain Medical oncology only until local chemotherapy, surgery and radiation delivery are confirmed. Correct the group doctor name to Brittanie Partridge; group membership is not branch assignment. Keep Spring and Houston separate. Exclude the verified stale Partner/Annapolis physical representation, preserving its raw profile and source inventory; do not merge organizations from a shared clinician history.

Veterinary Cancer Services is a mobile Colorado Front Range service, not a treatment office at Carnation Circle. Preserve the existing distance-free mobile behavior. A changed address without verified building coordinates or an available ZIP centroid may have `coordinates_unknown: true`, null latitude/longitude and an explanatory `coordinate_source`; it remains a physical clinic, never labelled mobile merely because coordinates are unknown. The finder omits distance calculation using its existing finite-coordinate guard. Validators must permit this explicit state instead of forcing invented coordinates.

An empty confirmed service list with `services_confirmation_status: unconfirmed` preserves the clinic and the next-pass question; it does not mean no cancer treatment. Caldwell’s general Surgery label cannot be retained where the finder interprets it as surgical oncology. Current clinicians/credentials and local services remain separate. Short Pump radiation is paused; Charlottesville is the distinct VVSE branch. ONE/BVSC and Veterinary Cancer Group modalities remain branch-specific.

Actual source-attempt timestamps come from package receipts. Integration and publication times are not fresh visits. Original audit reports can contain Russian internal notes; owner-facing availability copy is reconciled into English without expanding access claims. Build both source data and static output, run earlier A/B/C regressions plus branch/mobile/unconfirmed-service tests, and verify the remote commit and deployed page bytes before reporting publication.

## Six-worker oncology-care test publication — 2026-10-13

The owner authorized publication of confirmed data/technical results after the bounded six-worker test. Preserve its final reports, evidence, proposals and discovery queries in `research/audit-runs/six-worker-test-publish-20261012/`; do not treat intermediate evidence as worker completion. Integration is field-scoped against current main and records already-applied values separately from conflicts.

Publish only candidates that met the workers' saved completeness gate: worker 5's three fully verified clinics and worker 6's Bristol and Hokkaido records marked `core_fields_sufficient=true`. ChesterGates, Liverpool, Nagoya and JSAMC remain deferred with their concrete questions; current-treatment evidence alone is not a complete public clinic record. Sponsor-listed ECI access at MedVet New Orleans remains evidence, not a public service claim, until the hospital confirms active branch booking and treatment delivery. Date-only Web review updates `last_checked` without inventing `last_checked_at`; exact timestamps require saved actual request receipts.

# Vet Cancer Treatment Finder — Project Operations / Single Source of Truth

## Minnesota systematic care discovery — 2026-10-27

Owner requested a full state search. Add37 physical local/surgical locations and6 visiting/mobile services; reconcile the6 existing records. Current MN directory:43physical+6mobile,8physical chemotherapy listings and5locations with named medical oncologists. Borgatti appears at UMN and Arden Hills and is one person. AERC Oakdale now explicitly lists both Briana Keller and Sam Keepman; St.Paul ER is not another oncology site. New local chemotherapy is Northern Valley Rochester and Dougherty Duluth. General treatment discussions at Blue Cross do not confirm local chemotherapy/radiation; publish its separately explicit mass surgery only. UMN gains confirmed surgical oncology.

Preserve the two different Alexandria clinics: PetCare Center,710 3rd Ave W/3207628112, and Animal Doctor,902 Hwy29No/3207639955. The builder initially falsely merged them by similar name/sharedZIP; one individually evidenced pair in oncology_care_distinct_sites.json preserves both. No arbitrary different-ID exception. Golden Valley BluePearl is current760BooneAveN, surgery only; old EdenPrairie addresses and oncology hiring advertisements do not prove a second medical oncologist. HIGHLINE's published DACVS is Large Animal, not Small Animal or Oncology. House Paws surgery occurs at partner clinics, not its vans; Synergy,RCM,TCVS,HIGHLINE and Arrowwood retain visiting/mobile geography without mailing-address distance pins.

The retrieved secondary inventory is139city pages/634numbered rows+154single-town rows,788raw entries across293town labels, not788current primary clinical verifications. The10AnimalShelter pages are an independent discovery layer; page7 used Web after native timeout. VCA national-to-Minnesota sitemap yields767URLs; Cascade alone has explicit oncology/chemotherapy routes. CareCredit examples, testimonials, generic meta titles, allergy immunotherapy and directory-wide chemotherapy/radiation tags are not local delivery evidence.80exact later queries,988native request receipts, Web date-only receipts and per-host dispositions are retained in research/audit-runs/mn-care-20261027/. Raw page payloads stay local; concise reviewed facts and source dates are persisted.

The systematic discovery pass retains concrete exceptions, not a statewide absence claim: PineCone/MeadowView403team/access gaps; AlliedEdenPrairie blog versus BrooklynPark booking allocation; Morris605W5th versus separate CareVet820W5th identity/operation question; DirectVeterinarySurgery's current northernBayArea wording versus oldMinnesota titles/forms; CityofLakes specific tumor-service gap; Brainerd/FergusFalls current operating-veterinarian gap; Antenucci current404. Do not infer that these do not treat cancer, transfer services across namesake towns or publish historical Minnesota access from the651phone alone. No outreach or new state guide/UI/editorial change. Web-only successful source reviews retain a date without invented exact timestamps; actual failed native attempts stay in receipts. Exact accepted-row inverse projection extends the historical regression without weakening its original country hashes/pairs.

## Daily audit completion incident — 2026-10-26

The morning daily-20261026T030132-0400 finalizer assigned processing_complete=True to every source and external_blocker to every gap despite an empty reviews.json. Its generic route-attempt prose did not prove available reconciliation. The old receipt/report remain historical; the later gap-recovery-20261026T204639-0400 amendment withdraws unproven completion claims and retains actual original source timestamps. Do not clone that finalizer or treat its successful schema validation as semantic acceptance.

For every new daily source decision, persist an individual nonempty review with observed published protocol identities/statuses, canonical comparison/dispositions, actual evidence paths/URLs, remaining facts and accessible steps. Generate completion counts only from those reviewed decisions. Route coverage, unchanged fingerprints and prior roster copies are not independent decisions. Unreviewed sources default to not_established, processing_complete=false; never automatically label all residual gaps external. validate_audit_gap_review.py now rejects the known route-coverage placeholder, repeated blanket completion prose and complete flags conflicting with not_established/executor_unfinished.

The targeted recovery read eight Illinois PDFs, two Cornell protocols, Auburn and Tokyo primary protocols; it found a missed Tokyo feline-lapatinib notice already present in morning evidence. The organizer says target enrollment reached and study ending October31,2026; owner-paid drug use is separate from open trial recruitment. Preserve historical clinical cases but disable the fully enrolled trial, without creating a new commercial-access record or hiding other Tokyo cohorts. Web's cached version omitted the notice; retain that discrepancy explicitly and use the fresh complete organizer response. Completed full protocol rereads update verified/funding_verified only for facts actually reviewed.

## European six-agent controller — owner decision 2026-10-16

One controller now launches six real parallel country workers with `fork_turns=none`, replacing six independent European scheduled streams and the old weekday directions for this controller. Each worker receives exactly the parent's frozen run/slot/country/baseline assignment and its own `worker-N` directory, never a country list to choose from. No ten-candidate, sixty-round or old test-time ceiling applies to whole-country European work. Preserve fixed slot queues and original cursors; `INCOMPLETE` takes precedence over cursor=1, publication and suggested next country. Repeat runs on one local day retain the slot's country. Missing slot-3/5 receipts do not establish earlier Polish/French national work. Historical Austria/Czechia/Germany/Netherlands publications and Germany's October16 recovery are baseline, not current NEW.

The parent freezes assignments before spawn, records actual returned agent IDs and honest timing precision, and checks six nonempty worker files with exact run/slot/country/baseline identity before accepting results (`scripts/validate_europe_worker_result.py`). The parent also independently reviews evidence/branch scope, field deltas, dates and semantic identity; identity validation alone is insufficient. Workers never edit shared production/state or publish. Under the owner's October16 10:06/14:24 decision, first finish the entire documented accessible national frontier for every assigned country and independently accept all six substantive final reports; only then integrate/build/publish the site. A ready checkpoint, proposal volume, elapsed time or integration capacity cannot close research or authorize a partial publication. Update slot-state only after accepting results; preserve own unfinished work separately from external/access/owner-decision gaps. One country's report cannot be copied into another slot. Policy and README in `research/oncology-care-queue/` describe this architecture; old receipts remain history. Excluded new-discovery countries remain Russia, Belarus and Ukraine. Do not create/enable other automations or alter the morning trial task.

Research preservation is not site publication. Before new research, verify actual workflow branch/path triggers and save recovered evidence, queries, proposals, remaining and restrictions on a separate remote research branch, without PR/merge/deployment. The parent serializes immutable incremental checkpoints after each semantic block/restriction and at least every15minutes, verifies remote SHA and exact control/archive readback, and tests restoration into an empty directory. A local commit/hash/ready flag alone is not backup proof. Do not merge the research branch or ship snapshots into canonical data. Publication uses an all-six approval with exact file hashes and field old/new against fresh main, `scripts/integrate_europe_recovery.py`, the care/identity/source-date/filter/matcher/build gates and actual deploy/production-byte readback. The older checkpoint-publication receipts remain historical, not current permission.

Care access restrictions and recoverable evidence are indexed in `research/oncology-care-queue/access-restriction-index.json`. Read their exact saved scopes before source requests; missing old scope is not permission or a blanket group ban. Retain source dates and original visit-run attribution; publication/build timestamps cannot refresh them. Explicit unknown coordinates/postcodes remain unknown. The distinct-site exception data in `data/oncology_care_distinct_sites.json` contains only individually reviewed pairs, never a general different-ID rule. A later accepted complete country result supersedes its historical incomplete assignment for selection, without rewriting old receipts or advancing an already advanced cursor again.

## Stopped 68-source review: documentary closeout — 2026-10-14

The owner requested publication of nine confirmed corrections first, then documentary closeout of the 68-source remainder. The first package is deployed at eca20a12c3b67348db3de18935ac874a81a98e98; retain its exact tests/live proof in research/audit-runs/publish-nine-20261014T183019-0400/. The closeout is a new execution, finalize-68-20261014T185109-0400, using stopped-run evidence from reconcile-68-20261014T070053-0400 and separately dated targeted primary follow-up. Its receipt-final names the source-visit run in run_id and the new documentary execution in finalized_by_run_id. It is a reconstructed evidence snapshot, not a claim that all sources were revisited in the evening or that the stopped run already had completed paperwork. Preserve the original daily receipt unchanged.

Source outcomes are separate from processing proof and protocol impact. Twenty-four sources have sufficient saved roster/comparison evidence; 36 are partial, three unreachable and five deliberately not revisited after prior explicit gates. Each row has its own manual completion judgment and actual route evidence; do not infer completion from the outcome label. Keep the six European current-access decisions separate for the owner's next block; this closeout does not change their matching state. P1 prescreening expenses/sites and P2 inactive leads do not imply that every public trial from a partial source is unverified.

Correct report identities before closing gaps: NC State has seven dog/cat oncology identities after excluding FCGS; Penn CIP/Atherton has five actual protocol identities rather than the four incorrectly copied parent labels; Red Bank has five all-condition non-oncology studies and zero oncology. Immunocidin is not an existing canonical trial. A previously missed CCA link was followed to the manufacturer research/product pages and 2019 retrospective presentation: distinguish the unconfirmed OSA/solid-tumour/bladder trial signals from current commercial mammary-tumour product access. The named current NCSU bladder protocol uses IL12, not MCWF. Do not add a trial or make a semantic merge from the shared term immunotherapy.

## Literal protocol boundaries — 2026-10-14

Honor strict age/weight limits in both browser and legacy Python matching, including browse and unlisted-diagnosis paths. CAALM requires weight strictly above 15 kg and below 36 kg; the UCD oral theranostic protocol requires age above one year, and VROC Study 5 requires weight above 2.5 kg. Unknown values remain screening questions. Keep inclusive limits unchanged and test exact boundary values independently from inside/outside values. Do not weaken the frozen selection baseline; changed public selections require current primary-derived review cases.

UTSW VROC Studies 4 and 5 already existed in canonical data but lacked status_confidence, excluding them from public assembly despite available_for_matching=true. Current protocol brochures and the official master support their present intake. Restoring those two records is not discovery of two new studies. Preserve owner-paid coverage and arm-specific treatment limits. The focused nine-record publication inherits actual October 14 morning source timestamps; it does not complete the remaining 68-source reconciliation or renew source visit dates.

## Daily bounded oncology-care queue — owner authorized 2026-10-13

The current owner instruction supersedes the historical all-world weekly sweep: one daily task at 22:00 America/New_York, up to six actual parallel workers, finite non-overlapping packages, persistent progress in `research/oncology-care-queue/`. Keep the prior Weekly Oncology Care Audit disabled and the morning trial audit unchanged. Read the queue README and current state before selecting work; Monday physical review, Tuesday US discovery, Wednesday Canada/Europe, Thursday existing/mobile/tele, Friday other international territories in rotation, Saturday US continuation, Sunday due specific pending items. Five existing records or one limited territory/up to ten deep discovery candidates per worker (owner-approved increase, 2026-10-14). Current machine-readable limits are in `research/oncology-care-queue/policy.json`; saved three-candidate assignments remain historical. Do not treat unprocessed leads as verified or partial geographic discovery as completed national coverage.

The first daily package covers ND/SD/WV/AR/NE/KY, with real assignments and receipts in `research/audit-runs/care-discovery-20261013T220028-0400/`. New local chemotherapy can be provided by general veterinarians. Explicit tumor removal supports the existing Cancer surgery filter without inventing oncology board credentials; general Surgery text without tumor/cancer procedures does not. Conservative Local oncology care cards may retain unconfirmed specific modalities. Strict worker full verification and sufficient core data for a limited public card are separate counts. Preserve date-only Web visits without adding an invented exact successful timestamp. The parent serializes publication against fresh main and checks deploy/production bytes. For discovery, process saved unprocessed leads within the assigned direction before searching for more candidates; stop after ten, retaining exact unresolved questions. Up to six workers means up to sixty discovery candidates per run, not sixty promised additions. Do not reduce evidence quality to fill a quota.

## Catalog-wide selection audit — 2026-10-12

Owner additionally requested correcting the audit algorithm after the selection incident. `data/DAILY_AUDIT_ALGORITHM.md` now requires independent source-derived positive/negative/unknown cases plus a catalog-wide diagnosis witness and all-key eligibility coverage; one representative query is retired. `data/DAILY_AUDIT_TASK.md`, audit preflight and catalog CI invoke the selection gates. Passing generated parity is not medical-source verification.

Diagnosis matching is shared through `data/diagnosis_taxonomy.json` and `matcher_taxonomy.py`. The browser tables are generated by `scripts/sync_matcher_taxonomy.py` during matcher-data assembly. Keep browser, legacy Python matcher and species-scoped diagnosis-page listings aligned. Family matches always require investigator prescreening; explicit diagnosis/family exclusions and empty species cohorts override broad labels. `pending_diagnosis_review` preserves unresolved diagnoses outside matching without misrepresenting them as confirmed protocol exclusions.

Every public `requires`/`excludes` key must be classified in `data/matcher_protocol_rules.json`. Owner-answerable contradictions are enforced; criteria absent from the form remain visible screening items and cannot silently produce Likely match. Do not add anatomy/laboratory questions or UI text without owner approval. `Cancer — any type` remains browse mode, not a disease/history eligibility assessment.

Never use a substring in protocol notes to identify the accepted diagnosis: MSU CHOP/LOPP says cutaneous lymphoma is excluded, and the former text heuristic hid its eligible peripheral T-cell cohort. Keep the Missouri epitheliotropic cohort and Cornell B-cell cohort explicitly scoped. The CAALM protocol is oral melanoma with lung metastases, not a broad solid-tumor basket. COTC027 solid tumors must be non-sarcomatous. An explicitly retained active site must not disappear solely because the trial status also describes separate inactive sites (LEAH).

Receipt and full before/after diagnosis matrices: `research/audit-runs/matcher-selection-20261012/`. This is a selection audit of 307 canonical/165 public records, not a fresh global recruitment audit. Preserve source visit dates. Unresolved: Tufts Z-007 primary liver eligibility (HCC now shown only as a candidate under the owner-approved clarification below); TVT dedicated diagnosis option; COTC033 broad/site-specific scope; Tufts actionable OSA cohort assignment. Run `node scripts/test_matcher_selection.js` and `python scripts/test_matcher_selection.py`; both are production build gates.

## C03/C04/D01/D02 combined reconciliation — 2026-10-12

The owner authorized joint publication of the four reviewed packages (95 assigned source identities). Preserve current P00 and previous A/B/C decisions; integrate field values against current main rather than replace whole snapshots. Evidence, proposals, unresolved questions and per-field integration results are in `research/audit-runs/c03-c04-d01-d02-20261012/`.

C03 retains local chemotherapy independently of credentials, removes only unsupported confirmed chemotherapy tags at Highlands/Pahle/Roswell/Rutherford, adds verified branch immunotherapy and ONCEPT, and retains Mountain View radiation as delivery-unconfirmed. Northwest's local IMRT/SRT and Palm Beach's local IMRT have equipment evidence. Keep current clinician information separate from services; residency-trained is not board-certified.

C04 corrects the mixed Norwalk CT/Bedford Hills NY representation. Exclude the stale Jessica Chin imported physical profile while preserving raw history. Norwalk is 123 W. Cedar Street, CT 06854, 203-854-9960, with official branch JSON-LD coordinates 41.105345/-73.431517. The remaining NY ACVIM cluster can choose the non-clinical Focused Ultrasound Foundation label and disappear; retain the distinct current VCA Katonah Bedford branch at 546 Bedford Road, 914-241-7700 in supplemental. Its retained distance point is an existing ZIP centroid, not a building geocode. This preservation correction does not expand its modality list.

D01/D02 distinguish owner, owner-with-vet and veterinarian-only access, written review and live consultation, geography and actual assignment. Sarah Boston's current remote route is unconfirmed and excluded from public cards, preserving inventory/watchlist evidence; the active remote count is 60. Keep both count gates and the exclusion assertion aligned. D01 actual attempt timestamps are inherited from its receipt; D02 supplies date-only review evidence, so do not invent a time or overwrite its older visit timestamp with integration time. Source review completion and actual fresh visit dates remain separate.

**READ THIS FILE FIRST before modifying the app, catalog, workflows, SEO, or deployment.**

This file is the persistent engineering/operations memory for the project. Update it whenever a bug teaches us something, a workflow changes, or a new permanent rule is established. Do not rely on chat memory for operational knowledge.

Editorial style rule: use sentence case for Vet Trial Finder navigation labels, page titles, headings, cards and buttons. Preserve capitalization in proper names, institution names, abbreviations and official study titles. The production build runs `seo/enforce_sentence_case.py` last so generated pages cannot silently reintroduce Title Case.

Diagnosis landing pages use the existing canonical URLs and the heading pattern `{diagnosis} in {dogs|cats}: treatment, prognosis and clinical trials`. Do not add `costs` or a year unless the page contains sourced, maintainable information that supports those claims.

## 1. Production

- Repository: `jdizhur-rgb/vet-trial-matcher`
- Production branch: `main`
- Live Streamlit app: `https://vet-cancer-trial-finder.streamlit.app/`
- SEO site: `https://jdizhur-rgb.github.io/vet-trial-matcher/`
- Streamlit deployment was verified on 2026-09-06 to deploy `main`. Do not assume another branch without fresh deployment evidence.

## 2. Product scope

The matcher is treatment-focused. Include only opportunities that can provide an actual anticancer treatment option to a client-owned dog or cat.

Owner benefit is the controlling inclusion test. Do not publicly match a first-in-animal or Phase I protocol whose primary purpose is safety, pharmacokinetics, target engagement or dose finding when clinical benefit is only exploratory and the protocol offers no defined standard-treatment backbone or other credible therapeutic benefit. Free experimental drug alone is not a treatment benefit. Keep such studies in research/watchlist status with `available_for_matching == false`. A Phase I study may remain matchable only when the protocol still provides a credible treatment opportunity for the patient, not merely research participation.

Exclude observational, diagnostic/biomarker-only, sample collection/biobank, microbiome, research-only PK, and supportive-care studies without an anticancer treatment objective.

Potential public categories:
- Clinical Trial
- Compassionate / Expanded Access
- Novel Treatment / Special Program

Pipeline/watchlist records that do not yet have a usable owner-facing treatment route must remain non-matchable.

New clinical outcome evidence is also an access-screening signal, not only a trial-discovery signal. Every daily and weekly evidence sweep must ask whether the studied treatment is currently reachable through veterinary prescribing (including lawful off-label use), a regulated product, a specialty center or a verified treatment-access program. When meaningful disease-specific clinical evidence and a real present access route coexist, evaluate it for the relevant cancer/treatment page or Additional Oncology Options. Keep it separate from recruiting-trial counts, state the evidence design and limitations, and require oncology supervision and relevant safety monitoring. Publication without current practical access remains watchlist only.

## 3. Effective catalog

Production matching uses one canonical catalog: `data/trials_base.json`.

Do not create or load `trial_updates.json`, `catalog_patch_*.json`, or other layered patch files. A verified catalog change must be merged directly into the canonical record set, followed by full-catalog dedupe and matcher/SEO validation. A script or workflow existing is not proof that its data reached production.

For public treatment matching, records normally need:
- `study_type == "treatment"`
- `available_for_matching == true`
- species/cancer/country values compatible with matcher normalization
- current/usable treatment access

## 4. Mandatory promotion pipeline

Every catalog update must be treated as incomplete until this full loop succeeds:

1. Research and verify source/status/access.
2. Build candidate record(s).
3. Run semantic dedupe against the full canonical catalog, not only the proposed records.
4. Merge/update an existing record when the same real-world study/program already exists.
5. Write the reviewed final record directly to `data/trials_base.json`.
6. Rebuild/read the effective catalog.
7. Run post-promotion duplicate checks again.
8. Run matcher smoke tests for the affected species/country/cancer combinations.
9. Verify the committed production data from `main` after the write.
10. When practical, verify live Streamlit behavior after deployment.

**Never report “added”, “fixed”, “live”, or “done” merely because a patch, script, workflow, or commit that is supposed to do the work exists. Report completion only after final-state verification.**

## 5. Duplicate policy

ID equality alone is insufficient.

Pre-promotion and post-promotion dedupe must compare real-world identity using as many of these as available:
- normalized source URL / protocol URL
- institution / center / site
- protocol/study identifier
- title and semantic title similarity
- cancer/diagnosis
- intervention/treatment
- principal investigator / sponsor when useful
- enrollment route/contact

Same study under a different ID or slightly different title = merge/update, not a second public record.

When a clearly recruiting site publishes sufficient protocol and owner-access details but an older, non-matchable record at another institution may be the same protocol, do not suppress the confirmed recruiting opportunity while awaiting cross-institution identity confirmation. Match the verified site, keep the unverified site non-matchable, document the provisional identity in both records/source notes, and merge into one multisite record if the study teams later confirm a shared protocol. Do not report the inactive candidate as a second current opportunity.

**Do not dedupe on shared URL alone.** Universities often use one master clinical-trials page for many unrelated protocols. URL equality is supporting evidence, never sufficient identity by itself. Likewise, a shared drug/agent name (for example Z-007) can represent different protocols/sites. Prefer explicit protocol IDs (for example COTC033), or same-institution + highly similar title + overlapping disease/intervention evidence.

Dedupe automation is audit-first: identify conservative probable pairs, inspect the evidence, then apply. After applying, rebuild the full effective catalog and require the same detector to return zero remaining probable duplicates.

Known historical duplicate families that require caution include TriKE, Penn CAR-iNKT, UTSW protocols, COTC records, and other records imported from multiple source audits.

## 6. Required smoke tests

For every newly promoted matchable record, automated validation should assert:
- ID exists in the effective catalog after promotion.
- It is not simultaneously deleted/disabled.
- `study_type` is correct.
- `available_for_matching` is true when intended.
- Species normalization works.
- Country normalization works.
- Cancer normalization works.
- The affected country/species combination can return at least one result for the appropriate broad search (including `Any cancer type` behavior where applicable).
- A diagnosis-specific query returns the record when its cancer is selected.
- No semantic duplicate was introduced.

A failed assertion means the update FAILED. It must not be described as completed.

## 7. Research staging

Do not stage catalog changes as patch files inside `data/`. Keep research notes outside the production catalog. Only reviewed final records belong in `data/trials_base.json`.

## 8. China/Asia incident — 2026-09-07

China, Taiwan, and Korea were previously researched through staging patch files. China once showed 0 results in the live matcher because those records had not reached the production catalog even though a merger workflow existed. The layered patch system was retired on 2026-09-13; all retained records now live directly in `data/trials_base.json`.

Lesson: workflow creation/triggering is not final-state verification. Always fetch/search the canonical catalog after the workflow and then test matcher behavior.

Do NOT “fix” this class of bug by merely removing the country from the selector when genuine verified treatment records exist in staging. Reconcile and promote the records correctly.

Species may be stored as a string (`Dog`, `Dog/Cat`) or a list (`["Dog"]`, `["Dog","Cat"]`). All matching, filtering, SEO/import logic and smoke tests must normalize both forms.

For a single protocol with different eligible cancers in dogs and cats, retain one canonical record and supply `cancers_by_species` with exact `Dog` and `Cat` lists; `cancers` is their union for general catalog display. Both browser matching and species-specific cancer-page counts must use the scoped lists. A general cancer union alone would produce false cross-species matches, while splitting the same protocol into two IDs would inflate study counts. Requirements such as tumor size or anatomical involvement that the owner form cannot capture remain explicit prescreening conditions in the record rather than inferred matches.

## 9. Safety / false-hope rule

Eligibility matching must be conservative. A broad cancer label must not override explicit exclusions. If a program excludes a diagnosis (for example a particular lymphoma or brain tumor), do not map that excluded diagnosis merely because the program otherwise accepts many malignant tumors.

Final eligibility always belongs to the treating/research team.

## 10. SEO rules

SEO design is generally frozen except for bugs/database-driven updates unless explicitly requested.

Primary query clusters:
- treatment options
- clinical trials
- advanced treatments
- experimental treatments

Support dogs/canine AND cats/feline. Avoid thin doorway pages and avoid implying that a diagnosis page contains non-trial commercial/compassionate options unless those options are actually included in that page's data source.

**SEO must use exactly the same effective-catalog merge/delete semantics as production.** A bug found 2026-09-07 applied delete markers before upserts, causing deleted duplicate records (including old Auburn palbociclib) to be resurrected on generated SEO pages even though the production catalog had deleted them. Delete markers now have final precedence, and SEO generation must smoke-test that known deleted records do not reappear.

Production indexing policy added 2026-09-12:
- All canonical and sitemap URLs must use `https://vettrialfinder.com` only.
- Partially translated `de`, `fr`, `es`, `it`, and `nl` cancer pages are retired and excluded from the deployment artifact until a language is fully localized and reviewed.
- Legacy `/uk-europe/` and partially translated cancer pages are removed before deployment. They must remain absent from the production artifact and sitemap so retired URLs return the site's 404 page and leave the search index. North America is the active cancer-page SEO scope. Center pages remain indexable regardless of region because useful international institutions and active research programs are intentionally part of the directory.
- The primary page generator itself is restricted to English North American cancer pages. The final indexing cleanup still deletes the retired language and `/uk-europe/` directories as a second safety layer. Do not restore either generator branch without a fully translated, reviewed content set and an explicit indexing decision.
- The center directory includes real hospitals, research organizations and multicenter studies. These entities must be labeled by type and use type-appropriate page titles rather than presenting every program as a physical center.
- Diagnosis/species/region pages with zero current treatment opportunities remain available to owners but are `noindex, follow` and excluded from the sitemap.
- Search-indexing changes are applied after the static production build by `seo_index_cleanup.py`; they must not modify or couple to the Streamlit matcher runtime.
- The indexed `/how-we-verify/` page explains sources, inclusion rules, status checks, conservative eligibility matching, funding language, duplicate handling and the limits of the site. It is linked from the footer on every static page.
- The indexed `/veterinary-cancer-clinical-trials/` page is the central search landing page for general veterinary cancer trial queries. Its catalog counts and diagnosis links are generated from the current effective catalog, and it must remain linked from the shared navigation, homepage and footer.

## 11. Deployment lessons

- Production Streamlit branch is `main` unless fresh evidence proves otherwise.
- Back up before risky UI/deployment edits.
- Verify the live app, not just repository source, for deployment/UI bugs.
- Do not infer workflow success from workflow-file creation.
- The static site's canonical header navigation lives in `seo/site_shell.py`. Keep desktop dropdowns mutually exclusive and close them on pointer exit, outside click, link activation, focus exit and Escape; At mobile widths, the owner-approved navigation is a centered, scrollable blue panel below the existing white header; show bold group headings with native click-to-expand submenus, as requested by the owner. Opening locks background scrolling and makes page content inert. Close on the toggle, link activation or Escape, restore focus on Escape, and reset on the desktop breakpoint. Desktop dropdown behavior stays separate. The mobile closed-menu selector must outrank the panel display rule; verify the menu is hidden initially and after closing, not just styled correctly when open. Mobile navigation must use flex-wrap:nowrap and vertical scrolling: expanded groups on short screens must stay in one column, with Resources and About reachable below.

## 11a. Privacy and usage tracking

- Vet Trial Finder does not use website analytics or advertising trackers. Umami was removed on 2026-09-25.
- Do not add pageview, session, search-event, heatmap, replay, advertising or similar tracking without an explicit privacy review and owner approval.
- Matcher medical answers remain in the browser and must not be logged or transmitted.
- The optional US ZIP-code distance feature may send only the ZIP code to Zippopotam.us. It must never send diagnosis, treatment choices or other matcher answers with that request.
- Privacy and Terms pages are generated by `seo/site_shell.py` and linked from every shared footer.

## 11b. Image rights and clinic-directory disclosure

- Clinic-directory pages are text-only. Do not hotlink or republish photographs from clinic, university, news or sponsor websites merely because they are publicly accessible or credited. Add a clinic image only with explicit, documented reuse permission and owner approval.
- Center-directory service information may be compiled from clinic websites and professional public directories. The directory must state that Vet Trial Finder does not independently verify clinicians, licenses, credentials or quality of care; inclusion is not a recommendation; users must confirm the clinician, service, cost and availability directly with the clinic.

## 12. Working rule for future chats/agents

Before touching this project:
1. Read this file.
2. Inspect the current production files involved in the requested change.
3. Do not rediscover settled architecture from scratch.
4. Add durable new lessons/rules to this file when the project changes.

This file is the canonical engineering handoff. Chat summaries are secondary.

## 13. Osteoarthritis research matcher

- OA work remains isolated in `research/oa-matcher` until manual approval. Do not merge it to `main` as part of research or audit work.
- `data/oa_trials.json` is protocol-level: one multicenter protocol has one record and a `sites` list. `protocol_key` is required and unique.
- Patient-independent eligibility logic lives in `oa_matcher.py`; the Streamlit page only collects answers and renders results.
- Every `requires` or `excludes` key must be declared and implemented in `oa_matcher.py`. Validation fails on an unknown key so catalog changes cannot silently bypass matching.
- A known hard mismatch returns no result. An unknown answer or explicit study-team screening item remains a `Possible match — needs confirmation`. Records with limited public criteria can never be promoted to `Potential match`.
- Lack of existing X-rays is not a hard exclusion when the official source says study screening can provide or confirm radiographs.
- Run both `python scripts/validate_oa_prototype.py` and `python scripts/test_oa_matcher.py` after every OA catalog or matcher change.
- Cancer data and eligibility remain in `data/trials_base.json` and `pages/1_Clinical_Trial_Finder.py`; OA rules must not be added to that page.


## 14. Audit health-gate severity and repository sanitation

The weekly/deep audit must not stop because of a single ancillary or stale test failure.

Classify preflight findings before deciding whether to continue:
- **BLOCKING:** canonical JSON cannot be parsed/read; canonical catalog validator fails on a current public record; production matcher cannot load; canonical/production synchronization is materially broken; matcher import/compile fails; or multiple independent core checks show production/data corruption. Stop before source reconciliation.
- **NON-BLOCKING / INCONCLUSIVE:** a stale UI test selector/index, missing CI status, Chromium/session setup failure, one external page being unavailable, or another isolated harness/infrastructure issue when core catalog and matcher checks pass. Record it and continue the complete source audit.
- **DATA ISSUE:** a legacy/inactive/partial row or questionable historical metadata. Investigate that record during the audit; do not abort the whole source sweep unless it contaminates current public matching or makes identity/status unsafe to resolve.

Completion status is determined primarily by required source coverage and reconciliation. A full audit may finish with explicitly reported non-blocking/inconclusive items; it may not be called complete when mandatory source groups were not attempted.

UI smoke tests must locate widgets by stable labels/semantics, never by positional indexes. Positional Streamlit widget indexes are considered test-harness debt and must not be introduced.

Repository sanitation rule: data/trials_base.json is the only canonical cancer catalog. Metadata-only remnants from retired patch/overlay workflows are technical debt, not valid canonical records. Do not create new partial rows that contain only funding/status/contact metadata. Updates to an existing trial must merge into the complete canonical record. Any newly discovered metadata-only orphan must be either reconstructed from a verified primary source/full historical record or placed in unresolved; never silently treated as a complete trial.


## 15. Cost-controlled audit state

2026-10-13: apply `Partial triage by catalog impact` in data/DAILY_AUDIT_ALGORITHM.md. Source completeness, active-core access, ancillary fields and inactive leads require separate decisions. A generic hospital/oncology homepage is not proof that a protocol page does not exist: Armonia's current-studies section and VetAgro Sup's CICV index/direct oral-tumor invitation were found during targeted reconciliation after a previous partial pass missed them. Preserve that execution correction; do not relabel the previous pass as primary-verified. Published research/CVs can establish trial identity but cannot alone confirm present owner enrollment. Retain uncertain existing records pending the required status decision, with explicit issue impact and no refreshed successful verification date.

Use scripts/audit_preflight.py as the deterministic first gate. It distinguishes blocking core failures from ancillary/inconclusive smoke-test failures. Run scripts/validate_catalog_sanitation.py to reject any newly introduced partial canonical record while allowing explicitly tracked historical debt to remain quarantined in data/audit_unresolved.json until verified.

Persistent audit scheduling lives in data/audit_state.json. Source fingerprints remain in data/source_inventory.json. Deep audits should prioritize changed fingerprints, stale verification, unresolved items whose recheck_after is due, and a periodic forced full reread. An unchanged master page is a cost-saving signal, not proof that every protocol is current; forced rereads and protocol-level checks remain required on schedule.

Do not repeatedly research the same unresolved item before recheck_after unless its source fingerprint changes or new evidence appears. This is the default credit-saving behavior.

## 16. Integrity vs discovery audits

Catalog integrity and external-source discovery are separate audit products.

- `scripts/full_catalog_audit.py` audits records already present in the canonical catalog. It does not browse external sources and must never be described as a complete, global, or source-discovery audit.
- A source-discovery audit must actually open every mandatory master source in `data/source_inventory.json`, extract its current recruiting/open/current oncology-treatment protocols, compare them semantically with the canonical catalog, and open protocol-level primary pages for every new, changed, ambiguous, or missing candidate.
- Presence in the inventory is not evidence of coverage. `last_checked: null`, `last_result: pending`, or a source not opened during the current run means NOT CHECKED.
- Every completed source-discovery audit must write a coverage row for each mandatory source: opened_this_run, master_result, protocols_seen, candidates_found, protocol_pages_checked, fingerprint_changed, and last_checked_written.
- If any mandatory source was not opened or its current check metadata was not written, the source-discovery audit is INCOMPLETE and the overall run must be reported as NOT COMPLETE, even when all catalog validators pass.
- **2026-10-05 traversal lesson:** roster evidence is an execution gate, not merely a receipt-format check. A successful fetch/fingerprint must not advance the worker past a source when `protocols_seen` is still unknown. The worker must enumerate the current roster or exhaust every official inventory fallback and obvious official current-trial/protocol route; reachable partial sources remain on the pending queue until sufficient or until applicable official routes are exhausted; sixty minutes is a checkpoint and visible interim-report boundary, not an execution cutoff. The receipt validator must return INCOMPLETE whenever any mandatory source lacks sufficient current-run roster evidence, and must flag unattempted official fallbacks.
- Optimization begins only after each master page is opened **and its current roster is established**. An unchanged fingerprint plus a newly enumerated unchanged roster may skip rereading known protocol pages, except for a forced full protocol-level reread at least once every four weeks. A fingerprint by itself never satisfies the source. Changed, stale, due, and unresolved sources always require deep review.
- Before protocol-level verification, describe an apparent absence from the catalog as a “candidate for review,” never as a confirmed new trial or planned addition.

## 17. New cancer-trial intake order

Use this sequence for every newly reported cancer trial. A social post, news item, aggregator, or developer page is a discovery lead only; it is not sufficient evidence for publication.

1. Record the item as a candidate and identify the actual study by intervention, cancer, institution/PI, protocol ID when available, and public eligibility—not by title alone.
2. Check the effective canonical catalog for the same study before researching an addition. Compare `data/trials_base.json` semantically by protocol, center, diagnosis, intervention, and source URL. A shared drug or page does not by itself make two site-specific protocols duplicates.
3. Open the institution's current-trials index or registry entry and the direct protocol page, PDF, or enrollment form. The primary center source controls over an aggregator when status conflicts.
4. Confirm that enrollment is currently open, or that a real current entry path exists for new patients. Closed, on-hold, pipeline-only, and unconfirmed programs do not enter active matching.
5. Extract and verify, without inference: species and disease scope, treatment, public inclusion/exclusion criteria, site, contact, study type, current status, verification date, and owner-facing prescreening limits.
6. Verify funding and owner costs from the primary protocol source before publication. Distinguish precisely among fully funded, partially funded, treatment-only coverage, reimbursement, incentives, and costs not publicly stated; never convert any of these into a generic “free.”
7. Classify the candidate as Active Treatment Trial, Other Treatment Access, Watchlist, or Reject. Add only a confirmed missing active record, preserving existing records and avoiding broad cleanup during intake.
8. Update the complete canonical record in `data/trials_base.json`, then synchronize all production consumers: matcher logic, generated cancer pages, and any derived production catalog required by the repository.
9. Run catalog/schema and sanitation validation, unique-ID checks, production synchronization checks, matcher regression cases for the new eligibility rules, and relevant page/build checks. Hard exclusions must hide a trial; an unknown material criterion remains `Possible` and requires study-team confirmation.
10. Only after the checks pass, commit and push the completed change, then verify the SHA of the remote branch. Do not write partial research results to `main`.

## 18. Static-site source and artifact ownership

The deployable static site has one build entry point: `python scripts/build_static_site.py`. It deletes and recreates `seo/site/`; that directory is a disposable build artifact, is ignored by Git, and must never be committed or edited as source.

Source ownership is intentionally split by responsibility:
- `data/trials_base.json` is the canonical cancer opportunity catalog.
- `data/oncology_centers.json` is the canonical oncology-care directory; `data/acvim_oncology_profiles.json` provides its source profiles.
- `seo/static/matcher/` contains the browser matcher HTML/CSS/JavaScript templates. There is no separate preview or rollback template tree.
- `seo/generate_seo.py`, orchestrated only through `seo/build_production_site.py`, creates the SEO page base. The remaining named SEO modules are deterministic enrichment stages; they are not alternate deploy entry points.
- `seo/site_shell.py` owns the shared header, desktop/mobile navigation, footer, privacy/terms pages and global structured data.
- Every public static-page `<h1>` receives the shared `page-title` component in `seo/site_shell.py`; route-specific H1 typography must not be added. Keep the nearby-care matcher under “Find oncology care” and the research-center directory under “Find trials”; the latter is a trial-site directory, not a general care directory.
- `scripts/build_static_site.py` assembles the artifact and then runs cleanup, sentence-case enforcement, production synchronization, link/asset checks and matcher regressions.

Clinic pages and the oncology-care directory are text-only. Clinic-photo download/fallback code was retired; do not restore external clinic image fields or hotlinking helpers. Production validation rejects external images on center pages and retired preview routes, tracking markers, old navigation labels and obsolete claims.

IndexNow notifications run only after a successful GitHub Pages deployment. The notifier derives eligible URLs from the generated production sitemap, rejects non-canonical, noindex and redirect pages, and compares generated-page hashes with the last successful submission so only changed `https://vettrialfinder.com` pages are sent. IndexNow availability must never block deployment.

## 19. Technical SEO regression safeguards

Center directory addresses and ZIP/state filters must use the center's own location facts, never the first location of a multi-site study. Branch aliases should link directly to their destination; canonical URLs omit fragments. A participating site's stated country takes precedence over the study lead country.

The research-center directory's USA-by-state view and its three center-type views overlap intentionally. Include US centers in the type views as well as the state view. This directory uses category and state/country pickers, without a separate free-text search.

Global site search is generated from all public HTML pages by `scripts/build_site_search.py` after the static site has been assembled; search engine `noindex` does not remove a useful page from internal search. Keep a visible search form in the shared desktop header. On mobile, the owner-approved magnifying-glass button sits beside the menu button and expands the search form below the top row; opening search closes the menu and opening the menu closes search. Escape closes search and restores button focus. Without JavaScript the search form stays visible. Its results page uses the same field, without a duplicate search box. Queries run against the local page index and are not sent to an external search service. Verify that a center such as UC Davis is discoverable by name; the research-center directory itself has no separate text search.
Search results show a passage containing the match, with query terms highlighted, so incidental mentions in another diagnosis page have visible context. Keep dog and cat diagnosis pages as distinct results because their clinical content and trial listings differ.
Keep `scripts/build_site_search.py` in the deployment workflow's push path filter. A change only to the search builder must trigger a new build.

Breadcrumb structured-data destinations must resolve to existing production pages. Sitemap `lastmod` is omitted until reliable per-page content modification dates are available; neither a fixed date nor a fresh build timestamp represents a content update. The production synchronization validator checks breadcrumb destinations, fragment-free canonicals, article schema and the multi-site center-address regression.

When an official clinic relocation conflicts with the ACVIM snapshot, exclude the stale profile ID and retain the replacement in the existing supplemental source so rebuilds cannot restore the old address. Update distance coordinates together with the address; document ZIP-centroid precision when used. Ally Veterinary moved from Waltham to 16 Mill St., Lincoln, MA 01773, verified on its official site September 25, 2026.

## 20. Oncology teleconsultation directory

`seo/oncology_teleconsultations.py` is the canonical source for `/online-oncology-consultations/`. It contains one record per independently described service, not per clinician or branch. The production build calls it from `seo/site_shell.py`; the result is wrapped with the shared shell and included in the sitemap. Maintain the practice country separately from any verified service geography. A clinician named on a team page is not automatically the clinician assigned to remote appointments; preserve the assignment label and direct service and biography URLs. Separate owner access for an initial case review from conditional owner follow-up. Confirm changing prices, formats, credentials and availability with primary service pages before editing a record. The client-side search and filters process public listing text locally; do not collect or transmit medical queries.
When a specialist confirms owner video consultations in their own published interview or professional post, this is evidence of the service even if the practice has no standalone teleconsult booking page. Link that statement, the official clinician biography and the practice contact; mark undisclosed scheduling, fee and cross-border eligibility for confirmation. Do not exclude a service solely because the booking page is missing.
Search for teleconsultation services in the original language of each region. Japanese clinic booking platforms and Spanish- and Portuguese-language oncology practices yielded eligible services missed by English-only searches. Preserve native clinician and clinic names alongside transliterations so owners can find the actual booking entry. For Japan, distinguish an oncology-specific second-opinion booking menu from generic online practice visits, and add reservation fees to the base consultation fee when reporting the total. An oncology-trained staff member is not necessarily the assigned online consultant; confirm the appointment and any geographic limits in the listing. By the project owner's editorial decision on September 26, 2026, exclude practices based in Russia from this public teleconsultation directory.

## 21. Australia cancer-trial intake

The static matcher country selector in `seo/static/matcher/index.html` is hardcoded; a new country in `data/trials_base.json` must also be added there. `seo/generate_seo_strict.py` requires a verified complete address for each named hospital and active physical site and a substantive sourced introduction for each new center or research coordinator; add the latter through `seo/center_profiles_extra.py`. For Australian trial discovery, PetTrials is a lead directory, not proof of current recruitment. The ANZCVS oncology chapter points to a repository that requires member login. The undated CanineCancer.org.au research state guide preserves old auranofin and Kvax recruitment announcements that already have published historical results; always cross-check against a current organizer page.

Clinic research rosters can reveal protocols missing from national directories. In September 2026, MediPaws Sydney listed active enrollment in a University of Melbourne-led multicentre splenic haemangiosarcoma vaccine study (ethics project 35274); count the study once and add only individually verified participating sites. Separate a sponsor's open expressions-of-interest form from an ethics-approved study offering present treatment: Gamgee accepts case registrations, but its multicentre treatment activation has conflicting public evidence and must stay outside matching until direct confirmation. BVSC's broadly labeled current research themes include completed or observational projects; inspect each protocol before promoting it.

ANZCVS Vet Science Week programs and proceedings are investigator/discovery sources, not recruitment rosters. The public 2025 proceedings show preclinical CAR-T work and immune-profiling research; the 2026 program lists sessions but no owner enrollment details. The Oncology Chapter news can be stale and its Chapter Repository can require member access. Follow conference leads to current official hospital/sponsor recruitment pages before counting them.

## 22. Archived expanded-access directory

The owner-facing expanded-access directory was retired September 26, 2026 because its UT Southwestern entry duplicates a matchable clinical trial and the VMD Sciences listing is import assistance for a veterinarian-selected drug, not a named available cancer treatment. The former static page is preserved in `research/archive/expanded-access-2026-09-26.html` outside the deployable site. Do not restore a public navigation entry until a specific, currently accessible anticancer treatment and owner pathway have been verified. This archival decision does not change other verified treatment-access records in the canonical catalog.

## 23. Separate genomic testing from treatment listings

The owner-facing `/matcher/genomic-tests/` page contains tumor profiling services, while `/matcher/advanced/` contains treatments. A test that only provides diagnostic information or drug guidance must not appear as an administered treatment option or inflate treatment counts. Keep the separate navigation labels and deduplicate by actual service across regional entries. The retired Streamlit Additional Oncology Options page does not control the public static site.

## 24. News voice and share images

News articles start with the verified development, then explain the treatment, eligible animals and cancers, practical screening limits, funding if published, uncertainties, location/contact and official source. Keep connected, plain paragraphs, useful headings in sentence case and the original editorial skepticism; avoid promotional or sentimental copy. Facebook summaries should name the cancer and treatment plainly, use the established leading ◉ and bold headline, and give a concrete reason to open the article.

For new news items, prepare a restrained photographic or illustrative cover that reflects the eligible species; do not imply generated animals are actual study patients. Use the site's dark blue palette, clear type and no hearts, paw icons or decorative medical symbols. Place the image below the article heading and set a distinct `og:image` so link shares have an image. Confirm any clinic address shown in artwork against its official site and keep the full address legible when it belongs on the cover. Facebook may crop wide images to a center square even when the source is about 1.91:1: keep **all** share-image text and animal faces inside that central square, with safe margins, and check the resulting preview. An article's wide cover and its crop-safe sharing image may be separate assets. Existing Facebook posts may retain cached previews after an image is changed.

## 25. Source-check date persistence and reporting — 2026-09-30

Every audit must verify persisted source dates, not only request their update. Follow the mandatory date-verification gate in `data/DAILY_AUDIT_ALGORITHM.md`: snapshot previous values, timestamp each actual attempt (including partial/unreachable attempts), read back local files, commit the audit receipt and metadata even with no catalog changes, and fetch/read remote main to verify each attempted source's date, timestamp and result. Same-day reruns require a new timezone-aware `last_checked_at` even when `last_checked` stays the same. A fresh attempt timestamp does not mean successful source coverage.

Always report «Даты проверки источников» with total/attempted/remote-verified counts, date/timestamp range, stale or missing source IDs/names and before/after dates, visit results, remote SHA and PASS/FAIL. Missing visit evidence and failed persistence are separate failures; both make the run incomplete. Never backdate or refresh source dates from an intended run or an unchanged page assumption. Repair missing writes from actual coverage evidence without repeating the entire discovery sweep. The September 30 incident showed that published catalog updates and a general completion report can coexist with stale inventory dates; neither proves a full recorded source audit.

## 26. Nearby-care state filter — 2026-10-04

The oncology-care finder at `/matcher/centers/` has a native US-state selector generated by `seo/generate_oncology_center_finder.py`. Filter by the clinic’s exact `data-country` and `data-region`, never substring matches in its name or address. Apply the selected state in both ordinary search and ZIP distance sorting, together with the service filter. An empty state selection includes all locations; a state with no listed locations returns zero rather than nearby out-of-state clinics. The free-text input is labeled “Hospital or city”; keep the directory disclosure below the results in smaller, readable type so it does not push matches below the mobile viewport.


## 27. Weekly oncology-care methodology — separated 2026-10-05

Oncology clinics, specialists, branch-specific services and remote oncology consultations are audited in a separate weekly task every Saturday at 01:00 America/New_York. They are explicitly excluded from the daily 03:00 trial audit. The mandatory deep-pass procedure is in `data/DAILY_AUDIT_ALGORITHM.md`, section "Mandatory weekly oncology-care deep pass — Saturday 01:00, separated 2026-10-05". Read it together with the historical `data/oncology_center_source_audit.json`, ACVIM import/catalog-builder scripts and `scripts/research_vca_oncology.py`. Preserve the national specialist extraction, network/local-branch reconciliation, BluePearl marker-by-marker maps, VCA national/state sitemap-to-service-page route, Ethos brand sweep and separate state/local/mobile-clinic discovery. Historical partial coverage is not current completeness. Teleconsultation section 20 remains binding, including original-language discovery, direct owner vs vet-to-vet access and the Russia-based-practice exclusion. Record actual care-source visit receipts and remote-verified timestamps; include coverage and changes in the weekly oncology-care report. Verified factual updates are authorized for tested main/production publication; editorial/UI changes and ambiguity still require the owner's decision.

### October 10 correction — discovery before rechecks

Weekly oncology care is **discovery-first**, searching 50 US states + DC/PR and all 12 global regions (Japan in Japanese), for missing/new clinics, branch-specific cancer services, specialists, ECT/radiation and teleconsultations before checking all familiar sources. A recent-date search alone is insufficient: old/undated currently operational services missing from the directory are also leads. Save actual queries and classifications by location in `research/audit-runs/<run_id>/care-discovery-receipt.json` and run `scripts/validate_weekly_care_discovery.py`. Report separately verified NEW physical sites, NEW services at existing sites, NEW specialists and remote offerings, duplicate/rebrand/unresolved, plus coverage denominators. Empty/unperformed per-state or per-region discovery is INCOMPLETE, not NO CHANGE. Network master failures require `supporting_urls` and brand/hospital-level official routes, and VCA requires an actually executed national/state sitemap-to-service-page pass with numerical completion evidence. This is a technical/process correction; editorial/UI/CSS/navigation remain unchanged.

## 28. Homepage trial examples removed — 2026-10-04

By the owner’s request, remove the entire “Examples listed as recruiting” section from the homepage, including its three cards, funding summaries and trailing action/disclosure. The homepage is generated by `seo/site_shell.py`; do not restore these hardcoded examples during rebuilds.


## 29. October 5 audit incident and completion gates

The scheduled receipt `daily-20261005T050044-0400` recorded 76 trial attempts (71 sufficient, 1 partial, 4 unreachable) and also included the care sweep. The repeat receipt `daily-20261005T062751-0400` recorded 76 trial attempts (62 claimed sufficient, 4 partial, 10 unreachable), plus 487 care attempts (244 claimed sufficient). These are saved claims, not independent proof of complete coverage. All 76 repeat trial rows have `protocols_seen: null`; the 62 sufficient rows therefore lack required roster evidence. Historical fingerprints were retained. Remote timestamp persistence PASS is distinct from content reconciliation PASS. Do not rewrite these historical receipts as successful or manufacture missing evidence.

The operational fix initially separated daily trial-only coverage at 05:00 (the current schedule is in section 30) from weekly care coverage on Saturday at 01:00 America/New_York; preserves per-run snapshots/reports; adds the audit-receipt evidence gate; requires checkpoints, bounded network attempts and a visible partial/failure report; elapsed time alone is not an execution cutoff. See the execution/report gate in the algorithm. Report delivery failures must be repaired by resending the persisted report, not repeating hundreds of source checks. Current automation APIs do not expose push/email preference controls; previous claims that disabled notifications caused the missing report are not independently verified here.


### 2026-10-06 audit execution lessons

- Public protocol content in StudyPages/AVMA and the CSU trial portal can live in JSON data islands despite an empty visible-text shell. Read the public study content, eligibility, funding and locations before declaring a protocol unreadable; never persist unrelated keys or use internal endpoints.
- Preserve every genuine attempt by `(url, attempted_at, method)`, including later reader attempts and redirect metadata. URL-only deduplication can silently discard later real visits. Local decoding/OCR is evidence extraction, not another source visit.
- Directory resource counts are not protocol counts. Count oncology protocols separately from all-condition trial sections; preserve unknown roster counts where the current primary source does not expose a roster.
- Production HTML readback must compare against the wrapped artifact in `seo/site/`, not its source template in `seo/static/`; catalog/JS and HTML use the generated deployment tree for byte-level checks.


## 30. Restored single-pass morning audit — revised 2026-10-08

By Yulia's decision, restore the main September 25–October 1 traversal method while retaining all current source inventory entries and the newer source-evidence/date-integrity checks. Follow `data/DAILY_AUDIT_TASK.md` and algorithm section “Restored single-pass traversal — 2026-10-08”. One complete inventory traversal (master, required official fallbacks, available protocol/whole-roster reconciliation), then global discovery, verified publication and visible report. Do not automatically requeue partial/unreachable sources or repeat deep unresolved research without a changed-master/new-primary signal or due recheck date. Remove the temporary per-source minute budgets and mandatory follow-up pass introduced earlier October 8. Network timeouts and one transient retry remain finite. Processing coverage is separate from evidence sufficiency: a blocked/unpublished source is not successful coverage, and unperformed available work is not an external blocker. Keep the strict receipt validator, actual previous/new timestamps, same-day rerun rules, local/remote readback, immutable artifacts and mandatory Russian report. Plan the 03:00–06:00 window with the final half-hour reserved for validation/publication/report. Weekly care remains Saturday 01:00 and outside this daily task. No source inventory, historical receipt, catalog, site/UI or source-date changes are authorized by this methodology restoration.

### Source retrieval through shell and Web — 2026-10-08

Keep Work shell/Python/Git for files, validators, canonical edits, publication and production readback. For ordinary shell retrieval failures, blocked transport, interstitial/security content or empty JS pages, try the same official URL through the available Web open tool before classifying the source inaccessible. Preserve actual method/time/URL/content provenance and apply unchanged current-roster/primary-verification standards; search snippets or uncertain cached freshness are not current enrollment proof. A transport failure does not abort other sources. Never use tool switching to circumvent an explicit action/approval prohibition or authentication/attestation/CAPTCHA; distinguish these from ordinary retrieval failures. If permitted methods fail, record the gap once and proceed. The source inventory and source-date/evidence integrity gates are unchanged.

### StudyPages managed-location extraction — 2026-10-08

For StudyPages v3, empty initial HTML location/investigator islands do not establish that sites are unpublished. Follow the public page frontend’s current-content and public-study-locations GET routes; reconcile `managed_locations` when `org_study_sites_management_enabled` is true. Save the public protocol content and whole managed-site roster separately. The MVH HIFU/doxorubicin lymphoma protocol 140763 exposed VCA Dallas and its investigators through this public data while its HTML islands were empty. Never claim the page has no locations after reading only the HTML shell.

### Source URL identity — 2026-10-09

Source-inventory URL validation preserves identity-bearing query parameters (for example WordPress `page_id`). Different official protocol pages on the same path must not be rejected as duplicate URLs. Known tracking parameters and fragments are ignored; query order is normalized. Verified by query-identity regression checks during the 2026-10-09 audit.

### Matcher catalog loading — 2026-10-09

Manual search and country-change auto-submit must await the catalog-loading promise. A pending request previously searched the initial empty array and rendered false zero results that persisted after loading. Reproduced with delayed catalog responses for Japan and USA; failed loading must retain the existing load-error message rather than render no matches. Test the submit event path with `node scripts/test_matcher_catalog_loading.js`, not just the pure matchTrial function. Refresh the matcher JS asset version for this fix.

## 2026-10-10: Direct protocol status, public primary JSON and prior steroids

A direct current sponsor protocol can explicitly close one cohort while the sponsor master still labels it open. Resolve by protocol identity: ECIP-OSA-01 closure does not close the separate ECI-plus-chemotherapy cohort or commercial ECI access. CSU public StudyPages content endpoints recovered from real official redirects provide study-specific eligibility, funding and locations despite a JS text shell; persist only public study fields, never unrelated embedded service keys. Recognized direct registry study IDs can establish semantic duplicate identity; generic shared master URLs cannot. The matcher must enforce explicit previous systemic-steroid exclusion (Daunomustine); topical-only exceptions remain for study-team review. Retain the catalog-loading regression gate and verify rendered USA/Japan searches after deployment.

## Gap diagnosis and completion proof — 2026-10-10

Do not equate insufficient evidence with an unavailable source. For every insufficient source save `gap-review.json` with its source ID, exact missing fact, actual attempted evidence, next permitted action, and separate `processing_assessment`: `external_blocker`, `executor_unfinished` or `not_established`. Classify the cause as source unavailable, roster unestablished, freshness uncertain, discovery source without a trial roster, or individual protocol uncertainty. A directory/news/pipeline source is reviewed for links and leads; do not pretend it publishes an exhaustive recruiting roster. Preserve source inventory and the strict coverage gate; these diagnostic categories do not turn partial evidence into PASS.

A known source roster and missing details for one trial are separate results. Name the trial/site/fact; do not call the whole source inaccessible. An `external_blocker` requires source-specific evidence that applicable permitted routes were exhausted AND available reconciliation completed. A blanket `processing_complete=True` / `executor_incomplete=False` assignment proves neither. If completion is unproven, report NOT VERIFIED, not zero unfinished work or all-external gaps. Do not reuse a prior roster as today's roster without an explicit comparison to today's retrieved content. Historical snapshots are comparison evidence only.

Run `python scripts/validate_audit_gap_review.py research/audit-runs/<run_id>/gap-review.json --receipt research/audit-runs/<run_id>/receipt-final.json` alongside the unchanged strict receipt validator. Report the cause counts and separate protocol uncertainties, plus concrete executor steps or unverified completion. Do not automatically requeue all partial sources or repeat forbidden routes. Work on specifically identified permitted unfinished steps within the finite run; retained protocol questions follow the existing changed-signal/due-date rule.

BluePearl/VCA/Ethos *clinical trial* pages remain in scope of the daily trial audit. The exclusion applies to care-location/service/specialist directories, not to a network merely because its name also appears in the weekly care task. This scope clarification does not override an action denial, access gate or automatic approval rejection.

## Cancer scope: UGA pituitary macroadenoma — 2026-10-10

By the owner’s decision, `uga-sorafenib-radiation-pituitary-macroadenoma` remains outside active cancer matching. The official protocol names macroadenomas with Cushing’s disease and does not confirm malignant pituitary-tumor eligibility. Radiation and an anticancer drug do not by themselves establish a cancer diagnosis. Preserve the open recruitment status and historical record, but set `available_for_matching=false`; do not classify the study as closed or restore it from an unchanged master listing. Reactivation requires official protocol-level malignant-tumor eligibility evidence and the owner’s decision.

## Directory cards — 2026-10-10

The owner authorized publication of CanCan K9-LiquiDX under genomic tests and Oncept, Laverdia and Tanovea under advanced treatments. Both directories are authored in `seo/static/matcher/`; preserve their filters and separate evidence/access disclosures. Visible card copy explains what the option is, how it works and why it is used in a short owner-facing paragraph. Blood-based cancer monitoring belongs with tests, never with administered therapies or trial counts. Cancer-wide test filtering describes service scope, not validated sensitivity for every diagnosis. Keep Oncept limited to oral melanoma with stage/local-control limits, and show Tanovea’s major pulmonary warning. Approval or commercial access must not imply superiority to standard care.

## Evidence disclosure quality — 2026-10-10

An Evidence disclosure must explain what was studied, the observed result and the practical limitation in plain language. Naming the study design or regulatory approval and then repeating that evidence exists is insufficient. Keep response, stable disease, progression time and survival separate; a complete response is not a cure. State when controls were historical, no comparison exists or publication is pending. Link the specific study/approval assessment inside the disclosure. Test validation and finding a potential drug target do not by themselves prove improved survival.

## 38. Resuming paginated trial portals — 2026-10-10

When a StudyPages gallery is an empty reader shell, inspect its publicly advertised frontend route `/<gallery-name>/studies/search/json/` and traverse skip/take pagination until the returned unique count equals the stated total. AVMA currently has 850 records over two 500-sized requests; this is a retrieval count, not a treatment total. CSU, UC Davis and Mars expose the same public gallery mechanism. Preserve public protocol fields only; discard unrelated embedded service keys. PetTrials embeds its trial array directly in the public page. VetTrials caps API responses at 100 regardless of a larger requested limit: traverse every page and verify its total. Penn uses `filter[paged]=2` for Load More; a guessed `/page/2/` can return the first page again. Always verify different record identities and the final pagination boundary.

A targeted resume inherits actual prior evidence and its dates without reopening already sufficient sources. Keep immutable parent and resume receipts; explicitly distinguish newly attempted source count from cumulative coverage. Do not inherit the morning blanket processing-complete flags. Missing provider detail, stale cached roster, directories and unavailable sources remain separate gaps even when pagination is repaired.

## 39. Third-party browser keys in audit evidence — 2026-10-11

The weekly care run copied three Google API keys (four occurrences) from BluePearl's public hospital-finder JavaScript and UF/Chattanooga Google Maps embeds into research JSON. Current official public-page readback confirmed all three values; these were copied source-page keys, not Vet Trial Finder configuration. Public visibility does not justify republishing credential values. Do not test or use third-party keys, claim they are revoked, or classify them as false positives solely because they were public.

Use `scripts.check_evidence_keys.redact_text` before writing public-page payloads, extracted script data, maps, links, or JSON evidence. For ad hoc exports, run `python scripts/check_evidence_keys.py --redact research/audit-runs/<run_id>` before sealing evidence. Run `python scripts/check_evidence_keys.py` before every publication; it scans tracked and non-ignored new text files and rejects Google API key values without printing them. `scripts/test_evidence_keys.py` covers map/script redaction, JSON preservation and safe diagnostic output. The all-push evidence workflow checks research-only commits; the deployment workflow also rejects keys before building. This is a targeted Google-key gate, not comprehensive secret detection.

Preserve sealed manifests as historical receipts. Security redactions made after sealing require an append-only amendment recording affected paths, previous/new hashes, reason and actual remediation timestamp; never rewrite the original visit dates or pretend the original hashes describe redacted bytes. The October 11 amendment is `research/audit-runs/care-20261011T065613-0400/evidence-redaction-amendment.json`.

Removing values from main does not remove old Git history or automatically resolve GitHub secret alerts. Rotation belongs to the third-party key owner. History rewriting requires a separately reviewed action; do not force-push an unrelated audit/security cleanup.


## Page search titles — 2026-10-11

By the owner's request, omit Vet Trial Finder from all page `<title>` and matching social-title metadata. Keep the site name, WebSite/Organization schema, og:site_name, visible headings, navigation and body copy unchanged. `seo/enforce_sentence_case.py` applies this policy in the final build pass, including the approved homepage, trial-matcher and oncology-care-finder title overrides. Do not restore automatic title branding in the shared shell.

## Historical center URLs — 2026-10-11

The strict center generator shortens university names in slugs and removes raw-name pages. Preserve former full-name URLs with `seo/center_url_redirects.py`, run by the production builder after center enrichment. The BARC historical suffix has an explicit same-center mapping. GitHub Pages uses instant HTML meta refresh plus destination canonical, not an HTTP 301. Redirect stubs are noindex and excluded from the sitemap/internal search; never overwrite a live page, guess a replacement, or redirect a retired institution to another hospital. Pages absent because the effective catalog no longer supplies their center require separate reconciliation, not an invented URL equivalence. Validate source/destination identity, real targets, absence of chains and final production responses.

By the owner's subsequent explicit restoration request, retain the historical AMC, LSU, MedVet Clinical Studies, Anivive and Floryne Buishand profiles through `seo/retained_center_profiles.py`. Organization pages must not disappear merely because a trial's lead-center field changes. The MedVet, Anivive and European coordinator views use existing effective trial IDs; they never add trials or alter canonical eligibility/status. Scope MedVet's view to its participating hospitals and MedVet-specific source terms. AMC/LSU have no currently matchable entries and remain available as noindex reference profiles with an explicit catalog-availability statement, not reactivated studies. Preserve old URLs; do not overwrite a regenerated same-organization page. These retained profiles do not change the active research-center directory or matcher counts.

## Fetch branch-specific ECT correction — 2026-10-11

Fetch lists ECT explicitly on its Clearwater, Fort Myers and Bonita Springs branch pages. Preserve these branch URLs in the care inventory and the supplemental records so rebuilds do not reduce services to ACVIM specialty labels. The corrected Fort Myers phone is 239-308-9770; 239-260-4100 belongs to Bonita Springs. Targeted service reconciliation does not establish a completed network/credentials audit; retain the inventory partial status.

## Resumable care reconciliation — 2026-10-11

The owner authorized completion in independently published batches, without manual hospital checks. The durable queue is `research/audit-runs/care-batched-20261011T143110-0400/queue.json`; it references immutable prior source plans and discovery leads instead of duplicating them. Record individual semantic decisions in `reviews.json`; a fetched page or linked URL is not a completed source. Publish verified intermediate corrections while keeping the unfinished batch and global receipt visibly in progress.

Public-page extraction must retain relative hyperlinks as well as absolute and root-relative links. Follow actual local service and clinician links; the previous parser discarded plain relative hrefs. Separate current branch treatment from network navigation, referral-only services, research possibilities and clinicians listed at more than one site. Fetch radiation explicitly names Brandon and Bonita Springs; a radiation specialist on Fort Myers' team does not establish local radiation equipment. Preserve raw ACVIM profiles; exclude a stale/unverified physical-address representation only after retaining its confirmed current treatment location in supplemental data.

## Care execution order and local modality scope — 2026-10-11

By the owner's latest instruction, reconcile single-practice candidates before small networks and then large networks. Preserve original source_order for historical receipts; execution_order controls the new traversal. Ownership grouping is provisional until primary evidence confirms it. Each network requires a complete location roster and individually verified local treatment availability. General BluePearl FAQ treatment lists are not branch-level delivery proof. Public AVSC service/doctor/appointment content is published in client route modules; static reading preserves exact source URLs/timestamps and is not an HTML page visit or browser execution. Keep tumour-specific electroporation (TSE) literal and separate from generic ECT filter provenance.


## A01 clinic reconciliation — 2026-10-11

Owner approved the A01 review decisions: Four Seasons at 4120 Clydesdale Parkway/80538; Upton at 4055; Ivaoes is not a clinic; no current LAVet oncology representation from a past clinician biography. Dr. Sue is represented at Guardian, and Colorado Veterinary Oncology at VCA Deer Creek with the visiting Friday oncologist. Hillcrest is local care without verified chemotherapy; Kentuckiana is oncology referral; LIVS has verified surgical oncology. Keep Integrative Oncology/chemotherapy; the undated COVID intake notice is not current availability proof. Preserve raw ACVIM profiles and exclude superseded physical representations from catalog construction.

Hope WA and Mobile Veterinary Cancer Care are mobile services, not mailbox locations. Keep one service-area card each; null coordinates must never produce a distance from zero or a mailing-address point. ZIP sorting may show these matching regional services without a distance after fixed locations. Hope already has one teleconsultation listing: update it rather than duplicate it, separating owner Zoom review from written veterinarian plans and remote diagnosis/prescribing limits. A01 evidence and remaining questions are in `research/audit-runs/a01-approved-20261011/review.json`; this is not a completed global/network audit.

## A02 clinic reconciliation — 2026-10-11

Owner approved A02 changes after reviewing eight questions. Keep Mount Anthony without currently verified chemotherapy; exclude retired Alan Hammer/North Coast from active care, preserving raw ACVIM evidence. Platt Park remains a watchlist source until opening is confirmed, not an active treatment card. NWVOS/Megan Breit has physical partner appointments in Gig Harbor and Puyallup; Black Diamond is a postal contact. The stale Breit Renton profile must not swallow the distinct Veterinary Oncology Center/Luminita Sarbu profile in the same ZIP. VOC provides oral treatment and veterinarian-only written remote consultations, not injectable chemotherapy, surgery, radiation or ECT. Keep separate remote services and preserve their audiences.

Jennifer Hauss is DVM/residency-trained without a board-certification label. Parkersburg/Vienna chemotherapy remains practice-level with the branch to confirm when booking; no unverified Vienna treatment row. Owner explicitly assigns Pet Cancer Group services to both current branches and retains ONCEPT at RISE; mark these as owner decisions separately from the generic official wording. Pompano is mobile/home care in Broward/Palm Beach, with superficial SRT-100 radiation; neither its contact address nor its radiation credential establishes stereotactic RT/IMRT. Address changes and mobile conversions must update coordinates in catalog construction, not leave an old distance point. New WA/FL partner ZIP points are public ZIP centroids, not exact hospital geocodes. A02 evidence, original representations and decision provenance are in `research/audit-runs/a02-approved-20261011/review.json`; run `python scripts/test_a02_care_reconciliation.py` and the A01 regression after rebuilding. This is not a completed global/network care audit.

## A03 owner-approved care reconciliation — 2026-10-11

Retain Orange Park as temporarily closed until further notice, based on the owner's observed notice; the official reader still exposes older hours/clinician entries, so do not manufacture an extracted closure quote or new availability. Southern Colorado has two medical oncologists, Keira Sztukowski and Emily Lunger. Remove Summit's unsupported specific ELIAS ECI tag by owner decision while retaining general immunotherapy. Retain Parkway chemotherapy provisionally. Treeline lists two practice oncologists and refers radiation externally; confirm the clinician assigned to Boulder. Upleash tumor surgery remains unconfirmed. Vestavia has local cancer assessment/referral rather than a named in-house oncologist; its unconfirmed local modalities must not appear as confirmed service filters. Milford remains operation-unconfirmed, not permanently closed. Preserve Manhattan's modalities including gene-electrotransfer per owner review. Louisville offers local chemotherapy through internists; SAIM does not confer oncology certification and remote oncologist participation is unconfirmed.

A03 evidence, baseline and separate owner decisions are in `research/audit-runs/a03-approved-20261011/review.json`. Keep original visit timestamps/fingerprints unchanged when integrating existing evidence. Normalize literal TSE to the established `Tumour specific electroporation (TSE)` service label, separate from generic ECT. SERV and Southwest use documented ZIP centroids for distance estimates, not building coordinates; Toronto's updated 11 Maitland Street address has an address-level geocode retained in the same seed identity and supplemental record so the builder cannot retain null coordinates. This is a targeted A03 reconciliation, not completed global/network coverage.


## A04 care reconciliation — 2026-10-11

Owner approved A04 branch corrections. The imported Allstadt profile mixes VSNT's organization with UTSW's Dallas address/phone; exclude that raw profile from regeneration and retain UTSW Veterinary Research and Oncology Clinic at 5801 Forest Park Road with current official sources. Allstadt's current VSNT biography describes her return from UTSW. Do not reassign her to Dallas, infer medical-oncology board certification for Jonathan Maddox, or turn research-dependent drug access into unrestricted chemotherapy access.

Westbridge lists tumor removals/oncologic procedures; the owner approved surgery-only representation after reviewing the current roster. Townsend is a DACVS surgeon, without an inferred surgical-oncology credential. Preserve local RT at VSNT Fort Worth, VSC Bannockburn and WAVES San Leandro; VSC Feinmehl is residency-trained, not represented as board-certified. Manhattan and Violet Crown explicitly do not deliver radiation locally. Keep San Marcos radiation location and VSS clinician/modality allocation unresolved. The owner's likely-both-sites assessment is not branch-level proof. A04 receipt is research/audit-runs/a04-approved-20261011/review.json; historical raw ACVIM profiles and source visit timestamps remain intact.


## Explore navigation — 2026-10-11

The owner approved direct Advanced treatments and Genomic tests links in the shared Explore menu, targeting `/matcher/advanced/` and `/matcher/genomic-tests/`. Remove Browse clinical trials, which duplicated the About clinical trials destination. Keep the separate Other treatments overview and existing navigation behavior.


## Focused molecular cancer tests — 2026-10-11

Owner approved CADET BRAF/BRAF-PLUS and LABOKLIN c-KIT as two service cards under Genomic tests. CADET is urine-based canine bladder/prostate testing, grouped once across verified USA/Canada/UK access. LABOKLIN sequences KIT exons 8/9/11 from canine mast-cell tumor tissue, with verified Europe/UK access. Keep diagnosis-specific filter tags and limitations; neither is a broad pan-cancer panel or proof of drug benefit. The page now has six cards; update both production count gates together.


## C01 VCA branch reconciliation — 2026-10-11

Owner approved publication of the 25-source C01 audit and conservative conclusions. Retain the network sitemap as discovery-only, not a clinic or proof of branch services. Replace the unnamed San Francisco VCA representation with SAGE San Francisco and its dedicated Fenger/Trang-Hoang roster; retain the conflicting Andres source without declaring departure. Replace both stale Albuquerque ACVIM representations with the current 8850 Holly Avenue NE, Suite K / 87122 branch, main 505-292-5353 and the current official branch JSON-LD coordinate point; preserve raw profiles and the separately published referral number in evidence.

Keep hospital-listed chemotherapy at Airport Irvine, Amherst VA, AMC NE Alabama, Aventura and Bering Sea. At Aledo, Alpine, Amherst MT, Animal Care Clinic, Richland, Bath and Boonsboro retain Local oncology care and suppress only the unsupported Chemotherapy filter. Generic Oncology text is not modality proof; a branch Available Services/Chemotherapy entry is an explicit hospital offering, without proving a named specialist or every treatment protocol. Preserve residency-trained wording for Anne Skope and Sonia Honkisz.

Keep local Halcyon RT at Fishers/Aurora and current hospital-listed RT at Albuquerque without inventing its device or assigned radiation clinician. ASG Los Angeles explicitly has no local RT; retain chemotherapy, surgical oncology, targeted therapy, immunotherapy and ECT. San Diego explicitly offers ONCEPT; Baring's unnamed melanoma therapy is not enough to assign a product. Evidence/decisions are in research/audit-runs/c01-approved-20261011/review.json. This is targeted C01 coverage, not a completed national VCA audit.

## B02 care reconciliation — publication authorized, 2026-10-11

Owner initially authorized local implementation and subsequently authorized publication. BluePearl Tacoma's old 5608 S Durango seed representation is superseded by one current Tacoma–Lakewood card at 2510 84th St S, Suite 30D; retain both inventory identities with the Tacoma source as an alias. Greenbrier/Chesapeake reception is consolidated into Town Center Virginia Beach at 364 S Independence Blvd.; exclude the stale Brewer physical profile from regeneration, preserving raw history. Virginia Beach uses a documented public ZIP centroid for distance estimates, not a hospital geocode.

Keep Rockville ECT/immunotherapy and external radiation referral separate. Keep verified local radiation at Sandy Springs, Studio City, Southfield and Tampa; Raleigh/Jacksonville/Grand Rapids radiation delivery remains unresolved after official and indirect-source review and must not enter confirmed local filters. Remove FAQ-only immunotherapy tags from Raleigh/Sandy Springs/Studio City. Keep Tacoma's explicitly described ELIAS, small-molecule treatment and Stelfonta. Gendler is DVM/surgery resident, with no inferred DACVS from a neighboring clinician card. Research and old representations are in `research/audit-runs/b02-local-20261011/review.json`; run `scripts/test_b02_care_reconciliation.py` after rebuilding. Publication requires the tested combined catalog, remote SHA and successful production readback; retain the initial local-only authorization in the historical receipt.

## B01 BluePearl branch reconciliation — publication authorized, 2026-10-11

Owner finalized conservative decisions and authorized publication after local-only preparation. Preserve the 25 assigned source IDs and separate Malvern Hospital at 40 Three Tun Rd. from CyberKnife Cancer Center at 50 Three Tun Rd.; shared phone/ZIP must not merge them. Radiation at the separate Cancer Center must not become a hospital-at-40 service. Retain confirmed branch RT at Midtown, Brentwood, Cary, Levittown and Maitland; RT at Augusta, Brandon, Clearwater, Durham, Fort Myers, Nashville, Northfield and Port Washington remains unconfirmed and outside confirmed filters, without asserting absence.

Retain explicit local ECT at Arden Hills, Auburn Hills, Fort Myers, Lafayette and Northfield. Cary immunotherapy attribution is an explicitly documented inference from Ruslander's current branch roster plus actual use in his published interview. Maitland's published medical oncology/chemotherapy remains; Goodson is not a confirmed current clinician. Ten assigned inventory rows have next-oncology-care-pass review flags and concrete questions; preserve source visit timestamps when recording decisions. Research/field evidence is in `research/audit-runs/B01-20261012/`; run B01, B02, C01 and A01/A02 regressions with the combined build. This package is not a global/network audit.

## C02 scoped chemotherapy decision — 2026-10-11

Owner authorized adding chemotherapy where a current local oncology team and branch chemotherapy service coexist, retaining all other C02 services and disputed tags unchanged, with no publication yet. Encina (Atwater/Bennett) and Great Lakes (Morgan Clark) previously had only Medical oncology from the ACVIM import; same-location supplemental overrides retain Chemotherapy across rebuilds. Dallas, Capital Area, Colonial and Family/Oahu already include it. Do not apply the broader C02 audit recommendations or infer radiation/surgical-oncology credentials from this decision. This is a two-branch service update, not complete VCA network validation. Evidence and authorization are in research/audit-runs/c02-local-chemotherapy/review.json.

Publication subsequently authorized by the owner on 2026-10-11; preserve all concurrently published C01/B01/B02 changes when integrating.

## P00 archived-check reconciliation — 2026-10-12

Reconcile P00 against current main, never replace it with the e810b140 working snapshot. The 15 source identities represent 14 physical branches: both Animal Cancer Care Specialists IDs resolve to the existing Littleton clinic, with the second retained as an inventory alias. Preserve the Acton profile exclusion and raw historical evidence. Eastern Carolina Veterinary Referral is the same Wilmington branch now named Eastern Carolina Veterinary Medical Center.

P00 adds only missing branch modalities/contact corrections, retaining existing HEAL, Dunes and Franklin Lakes services. Local chemotherapy is independent of board certification. ACCS, BARC, HEAL and Eclipse external radiation routes do not establish local radiation; generic radiation discussion at other P00 sites also stays outside confirmed filters. Venner is residency-trained, Lee is practice-limited, and SAIM/surgery credentials must not be converted to oncology certification. Keep clinician evidence separate from service labels. P00 evidence and before/after decisions are in `research/audit-runs/p00-reconciled-20261012/review.json`; source checks are inherited from October 11 with their actual timestamps, not renewed by local reconciliation. Remaining provider/format/brand/opening questions are recorded there and in assigned inventory rows for the next care pass.

## Tufts Z-007 HCC candidate — owner-approved correction, 2026-10-12

The owner approved showing hepatocellular carcinoma as a potential option requiring Tufts confirmation. The official protocol admits carcinomas and excludes significant underlying liver disease, without explicitly excluding primary liver carcinoma or explaining that distinction. Do not turn this uncertainty into a diagnosis-level exclusion. HCC uses the carcinoma-family route, remains prescreening-only, and carries an explicit warning about the liver exclusion, liver function and repeated-biopsy feasibility. Existing weight, measurable disease and prior-immunotherapy constraints remain enforced. Other liver tumor remains pending because that label does not establish an eligible histology. This decision confirms discoverability, not study acceptance or efficacy. Receipt: `research/audit-runs/tufts-hcc-candidate-20261012/review.json`.

The static builder versions MATCHER_DATA_URL by the SHA-256 of the deployed catalog; production synchronization checks the hash. A correct new server file can coexist with an old catalog in an already opened browser. Preserve content-based cache invalidation for data-only updates.

## Independent protocol-selection baseline — started 2026-10-12

The owner authorized both a full current-public protocol review and permanent algorithm integration. The baseline/queue is in `research/audit-runs/protocol-selection-20261012/` (165 baseline records). Initial source retrieval attempted 152 unique protocol/registry URLs; a fetched source is not a completed medical review. `data/protocol_selection_cases.json` stores independently derived cases with primary URLs and review times; `scripts/test_matcher_protocol_sources.js` is invoked by the catalog-wide selection gate in build/CI/preflight, including no-change runs. First corrections concern 15 records: missing UF limb scope, required standard/combination treatments, omitted prior-treatment exclusions and MRI/radiographic screening incorrectly requiring pathology. Full cohort/site reconciliation is still pending and must not be described as a clean complete catalog. Preserve per-record pending dispositions and perform a complete independent rereview at least every 28 days. Raw downloaded page payloads stay in scratch; public receipts retain source attempts and concise reviewed facts, never unrelated service configuration or credentials.

Source-derived cases now cover 23 records at the second checkpoint. The frozen `data/protocol_selection_baseline.json` contains pre-review selection signatures only; any new/changed public selection requires matching review signatures and passing independent cases. Do not refresh the baseline to make an unreviewed change pass. The full independent review remains in progress.

Owner medical/editorial decision during the independent review: retain MSU CMP-002 in potential treatment search with an explicit dose-finding/unproven-benefit disclosure, rather than remove it. The official MSU purpose is dose determination, with anticancer evaluation in later studies. This scoped exception does not automatically retain other research-only dose/safety programs; assess and raise those individually.


## European current-access quarantine — owner-approved 2026-10-13

Yulia approved the prepared temporary exclusion of eu-pt-hepatic-thermoablation, eu-pt-chemodectoma-microwave, eu-pt-mammary-pdt and eu-it-mucosal-melanoma-autologous-vaccine. Set available_for_matching=false and status_confidence=unconfirmed; preserve complete records, prior verified dates and history. This is not a confirmed closure. Keep the exact access/protocol/site questions in data/audit_unresolved.json; restore matching only after current protocol-level organizer evidence. The approval applies to these four records, not a blanket disposition of other European/source partials. Prior evidence is in research/audit-runs/europe-six-20261013T190857-0400/. Applying the decision is not a new source visit or new global audit.


## CanCan feline Tissue Core — owner-approved news and test listing, 2026-10-13

Owner requested the feline test news on the site after reviewing the Facebook explanation, and explicitly requested CanCan’s own image. The new news article and separate Cat genomic-test card describe the 75-gene tissue panel, FFPE/FNA requirements and up-to-three-week turnaround from the official feline page/brochure. Price (£300/$400), international patient access, evidence extrapolated from human/canine research and planned safety/dosing studies come from direct manufacturer correspondence shown by the owner on October 13. No recruiting feline treatment study is established. Keep tissue testing distinct from the planned Q2 2027 liquid biopsy and outside treatment/trial counts. Both genomic-card count gates are seven; preserve the Cat filter. The local image is the unchanged CAT-W2-scaled.jpg from CanCan’s official feline page, requested by the owner and credited in the article; it does not establish that the pictured cat was a patient. Source provenance is in research/audit-runs/cancan-feline-20261013/review.json.


## Public brand — owner-authorized 2026-10-14

The public site is now Pet Cancer Trail. Apply the name consistently to the shared header/footer, About/Help/contact/privacy/terms copy, article bylines, image descriptions, social site-name metadata, breadcrumbs and WebSite/Organization publisher identity. The domain remains https://vettrialfinder.com; preserve all canonical paths, email addresses, social links and existing logo assets. Historical research receipts are not renamed or rewritten. The October 11 descriptive, unbranded page-title policy still applies: strip Pet Cancer Trail from page-title suffixes and retain the approved search-title overrides. The owner explicitly authorized implementation and production publication of this rebrand.

## Canada/Europe bounded care discovery — 2026-10-14

Six real workers reviewed ten candidates each in Ontario, Quebec, UK, Germany, France and Netherlands. Preserve `research/audit-runs/care-discovery-20261014T215849-0400/`: 60 processed, 35 strict fully verified, 46 core-sufficient physical additions plus one VOS remote service. These are bounded territorial searches, not completed country audits. Specific branch-modality/clinician questions remain due October 21; saved unprocessed leads must precede new general searches.

Keep CENTREDMVET Montreal, St-Hubert and Blainville at confirmed Medical oncology only until treatment delivery is allocated by branch. Cancer Vet Montreal's Monkland in-person consultations are distinct from tele-11 and do not establish on-site chemotherapy. Lakeshore AHP's historical 2025 interruption must be assessed alongside its current official Gabriella Allegrini oncology roster, not treated as proof of present closure. Cambridge and Laval have saved successful worker source evidence even though the parent's later retrieval encountered 502/reader errors; do not renew successful source timestamps from that failed retry. French Web-only review dates are recorded as October 15 UTC, with no fabricated exact successful request time.

VOS is a UK-registered remote provider with Polish/English written and 40-minute online oncology services; its direct service form and terms establish owner/vet access and worldwide advisory service with local-veterinarian implementation. Do not make a physical clinic from its registered office. The tele directory now has 61 records: 47 with owner initial access, 13 veterinarian-only, and one conditional owner-follow-up service. Keep the count gate and A02 count regression aligned while preserving all earlier exclusions and branch decisions.


## Public brand restored — owner-authorized 2026-10-15

The owner ended the Pet Cancer Trail experiment and explicitly requested restoring Vet Trial Finder throughout the site and publication. Restore the public identity in shared navigation, copy, metadata, structured data, article bylines and the three original branded image assets. This supersedes the October 14 public-brand decision; preserve that historical note. Keep the domain, current catalogs, subsequent content/data changes and the descriptive unbranded page-title policy unchanged. The production brand gate now rejects the experimental name.


## Oncology-care country selector — owner-approved 2026-10-15

The care finder now has an explicit country selector populated from its actual directory countries, defaulting to All countries. Match country exactly alongside text, service and US-state filters. Show and enable US-state/ZIP controls only when USA is selected; switching away clears their values and invalidates pending ZIP results. International countries remain directly selectable without knowing the hidden text-search country support. Preserve mobile/unknown-coordinate distance suppression and existing service filters. The owner approved this UI correction after the Germany discovery problem. Remove the stray leading conflict-marker text from the finder template; it is not page content.


## European care discovery: whole-country tasks — owner-authorized 2026-10-15

For Europe, one task covers one entire country, with no automatic ten-candidate stop, sixty-candidate run ceiling or regional splitting inherited from the bounded non-European queue. Apply research/oncology-care-queue/policy.json European override and europe-country-queue.json. Search local languages, all regions, university hospitals, networks and branches, independent/local chemotherapy providers and radiotherapy/ECT/visiting/mobile/remote services; retain both current/undated and new-signal layers. Prior leads are a starting point, not national coverage. Publish verified results as ready; only evidence-backed coverage closes a country. Interrupted execution retains exact remaining work, never fabricated completeness. Russia and Belarus are excluded from new care discovery, and Ukraine is temporarily excluded until the owner decides otherwise. This does not delete existing records or rewrite historical receipts. Other day directions and non-European package limits remain unchanged. Updating the paused care automation's prompt does not authorize resuming it.

## Austrian branch identity — 2026-10-15

The Austrian care pass exposed four false merges from similar names within one Vienna postal code: TIERplus Kagran/Stadlau, Döbling/Hutter, Vetklinikum/Mauer and Pragerstraße/Strebersdorf. Current official branch/contact evidence confirms different addresses and telephone numbers. Preserve these four verified identity separations in the builder without changing unrelated historical matching behavior. The production build now checks that every Austrian supplemental identity survives catalog assembly with its own address, phone, services and location type. Evidence and remaining coverage questions are in research/audit-runs/europe-slot-1-20261015/; publishing a verified batch does not itself close national coverage.


## Daily primary reconciliation — 2026-10-16

Current Missouri embedded LEAH protocol and fresh same-URL Web read now agree on enrollment, superseding the older cached ON HOLD page. Restore Missouri within the existing LEAH record; retain Minnesota hold and the separate sponsor-only Ohio slot question. Missouri >10kg/72-hour prednisone washout/seven visits in21days/$4000 adverse-event allowance/$2000 completion stipend are site-specific and must not become universal Ohio criteria. Update the obsolete paused-Missouri regression to the current primary roster.

OVC individual canine Palladia and HIFU pages were recovered and fully read. Previous melanoma vaccine allowance does not make Palladia a vaccine intervention. Distal-radius OSA HIFU excludes axial OSA; an appendicular answer still requires exact distal-radius screening. Source-derived cases precede these corrections; preserve the immutable selection baseline. Three UTSW AVMA statuses changed to Completed while current institutional brochures still invite enrollment: record the exact conflicts and proposed temporary nonmatchable dispositions for owner decision, preserving present clinical state until that decision. Evidence and full daily receipt: `research/audit-runs/daily-20261016T025651-0400/`.


October16 production readback additionally exposed a shared-name address-resolution defect: Metropolitan Cleveland and Akron study sites both displayed the Akron address. Reuse the already verified October12 branch identities (Cleveland East:734AlphaDr,HighlandHeightsOH44143; Akron:1053S.Cleveland-MassillonRd,Akron/CopleyOH44321) without redating care sources. Pass the explicit site city to shared address resolution in matcher/SEO builders, and do not reuse old coordinates across same-name branches or changed addresses. The same live-card check found VERC Honolulu incorrectly inheriting the Pensacola alias; use the existing canonical Hawaii branch at345N.NimitzHighwayUnitC,HonoluluHI96817 for explicit Honolulu sites while preserving the Florida alias. Clinical site rosters remain unchanged. Evidence: `metropolitan-address-fix.json` in the same run.


October16 traversal also exposed a planning error: deriving inherited restrictions only from whole-source not_checked rows missed an old explicit403 master in a partial Ethos source. The one erroneous native404request is preserved as a deviation, with no retry/bypass. Persist its original Web denial in inventory access_restrictions and filter exact denied URLs before queuing, while retaining permitted official fallbacks and original source timestamps. Algorithm section Preserve URL-specific access restrictions records the rule.

## Three UTSW AVMA completions — owner decision 2026-10-16

The owner explicitly directs that AVMA Completed governs utsw-solid-cpmv, vroc-rt-histotripsy and utsw-vroc-melanoma-crtnp-hifu-pdl1. Set available_for_matching=false and status_confidence=confirmed_completed; preserve the records, prior protocol/funding verification dates and institutional conflict evidence. Do not restore them from unchanged institutional brochures. This is a scoped decision for three exact protocols, not a general registry-only activation rule. The six European access questions remain unchanged pending disposition. Decision and checks: research/audit-runs/utsw-owner-completed-20261016/.

## Six European access exclusions — owner decision 2026-10-16

After reviewing the exact six questions, the owner approved hiding fr-fregis-hepatic-tumor-thermoablation, fr-fregis-chemodectoma-thermoablation, fr-fregis-hepatic-embolization, eu-ch-sinonasal-heterogeneous-rt, uk-rvc-insulinoma-toceranib and nl-utrecht-osteosarcoma-oncolytic-virus-access. Set available_for_matching=false and status_confidence=unconfirmed; retain all records, prior source dates, historical status and exact access questions. This supersedes the preceding note that the six remained pending. These are temporary current-access exclusions, not confirmed completions; do not reactivate without new protocol-level current-access evidence. Same decision receipt as the three UTSW completions above.

## Owner-requested eligibility restart — 2026-10-16

The owner requested a new review of the entire public matcher, not just histiocytic sarcoma. The frozen starting state is main `2f709930`, with310 canonical/156 public records. Receipts, all156 per-record dispositions,49 verified catalog corrections and explicit unresolved questions are in `research/audit-runs/selection-restart-20261016/`. This is NOT a completed medical/recruitment audit:116 source-derived case reviews were refreshed after this run's first source request, and40 fresh-verification gaps remain. Same-day morning OVC reviews are not new afternoon reviews. Preserve exact timestamp offsets and do not replace this cutoff with a calendar-date comparison.

Confirmed fixes include omitted mandatory treatment backbones, AML-only and oral-SCC scope, strict age/weight boundaries, Penn OSA cohort requirements, postoperative Tufts HSA/NVLU access, molecular/MRI screening and the explicit MedVet long-bone OSA confirmation exception. Vaxleukin's mammary indication allows previously performed surgical standard care; it does not universally require another future surgery. Preserve the history-or-preference rule in browser and Python. The preference classifier must include recognized structured `treatments`; omission hid IL15 when the prose used immunoadjuvant rather than immunotherapy.

Keep all previously valid independent cases. The one retired MSU MCT current-chemo hard-rejection case is documented in `superseded-cases.json` and replaced with a source-supported seven-day washout screening assertion. The frozen selection baseline was not refreshed. Tests now distinguish public reviewed/total/pending from retained historical reviews. `node scripts/test_matcher_protocol_sources.js --reviewed-since=2026-10-16T18:59:47.653454Z --require-full-review` intentionally remains failing for40 records; normal regression success is not full fresh medical coverage.

Do not automatically close a current cohort from an old similarly named AVMA study. OSU's feline mammary registry entry is not Minnesota's olaparib protocol; an unidentified single-injection B-cell study is not established as Aurelius/LTX315. A fresh clinical-criteria review also does not resolve Penn B-cell CAR-T's current AVMA Suspended/inaccessible-institution status conflict. Preserve the owner-decision proposals for MSU quasiorganelle safety/dosing inclusion, Mexico's news-only access evidence, Tufts Z007 HS-specific scope and the inaccurate shared funded/assisted owner-facing reason for commercial access. Those proposed medical/text changes were not applied. Tokyo's polymer-pirarubicin primary explicitly includes HS; do not remove it merely because its record uses a broad solid-tumor route.


## Germany clinical recovery and publication — owner-authorized 2026-10-16

The owner prioritized Germany and required finishing its available search before publication. The isolated recovery preserves55 verified new physical locations,2 remote services and the existing Am Westend temporary-closure/future-move note. Evidence, all87 named dispositions and explicit residual gaps are in research/audit-runs/germany-finish-20261016/ on the same-named research branch. Do not treat the country as complete without remaining clinical evidence:9 automatic-review holds,1 genuine403,3 unreachable and26 insufficient-primary candidates remain. Processing a candidate is distinct from proving its treatment scope.

Local oncology care can be published with verified current clinical treatment scope, named veterinary role, contact and intake while specific modalities remain unstated. Apply the same threshold to Preetz, Bockenheim and Britta Richter. Schafflund surgery allocation is supported by explicit transfer of operations from Tarp to the main operating practice; chemotherapy is not allocated to either branch by that fact. A group tumor-removal page does not establish cancer surgery at every filu branch. Keep Am Westend's announced19October move in its availability note until the actual move is confirmed.

Use explicit evidence allowlists and incremental source receipts. If automatic review rejects polling a mixed source batch, neither replay it nor read its result file as a substitute. Preserve exact targets and the stated reason; continue independent unaffected work. Original missing approval receipts must be reported as missing, not reconstructed as a guessed denial reason. Publication uses a prepared branch and atomic PR merge after fresh-main reconciliation, followed by deployed-byte readback.


## Germany39 followup: action scope versus source restrictions —2026-10-16

The owner asked to resolve all39 deferred Germany candidates. A denied mixed request/poll action is not proof that every independent provider has a403. Separate the risky source from independent domains before considering a materially safer alternative. New individual public requests excluding restricted AniCura roster targets recovered six providers; old rejected outputs were never used. Preserve actual exact-URL/redirect denials and remaining action restrictions. Do not turn one blocked aggregate action into a global Germany ban, or reduce the clinical evidence threshold.

The finite followup verifies17 additional physical locations and one mobile home-chemotherapy service, with explicit service-area and no treatment-office inference. Twelve earlier insufficient-primary cases were resolved through full saved clinical pages and targeted advertised child pages, including a verified receiving hospital for the Anke Wendel lead. The candidate does not establish a separate mobile oncology service or personal oncology assignment. Current local diagnosis and therapy can support limited Local oncology care without inventing chemotherapy or tumor surgery. Service, veterinary qualification and branch allocation remain separate fields.

All39 outcomes and unsent German confirmation questions are retained in research/audit-runs/germany-remaining39-20261016/; no clinic messages or forms were sent. Ten open filu branches still need explicit local cancer-service allocation; Prenzlauer Berg and Waiblingen remain pre-opening. Tarp maps complex operations to published Schafflund without a new Tarp modality. KlickVet has no current owned cancer-care claim; that is not proof it does not treat cancer. Three restricted AniCura targets, one genuine403 and three inaccessible primary sites retain concrete resolution questions. Do not automatically restart a broad discovery sweep or create background tasks from these records.

Germany followup 2026-10-16: final finite remaining39 disposition and continuation pointer are research/audit-runs/germany-remaining39-20261016/germany-continuation.json. Do not restart87/39 discovery. Narrow identity guard preserves separate AmSteinhuebel/Waschbuesch providers, including baseline no-new-clients intake.

## Network-level care access — owner-approved 2026-10-17

When the current official network site explicitly offers a usable cancer treatment but does not allocate it to branches, retain that useful owner route as ONE `location_type: network`, `service_scope: network` listing with an official common phone/email or booking link and branch finder. State clearly that the owner must confirm the branch, clinician and appointment availability. A branch phone is not a central contact. A corporate office is not a treatment address. Keep street/city/postcode empty and coordinates null; suppress distance and label the entry as a network contact. Count it as a listing, not a physical clinic. Apply country/service filters to the explicitly confirmed NETWORK services; do not clone the service to branches or merge network identity with branch identity. Local service claims still require branch evidence. Do not infer chemotherapy, radiation or specialist certification. This supplements the earlier branch-only publication gate for network entries only; historical branch evidence and genuine access restrictions remain unchanged.

Applied to filu as one Germany network Surgery listing with service@filu.vet, its official booking portal and branch finder. Ten existing open-branch leads are usable through this network route; their specific surgery allocation remains for the owner to confirm when booking. Two future openings and seven other provider gaps are unchanged. No messages or bookings were submitted. Receipt: research/audit-runs/filu-network-20261017/.

## Daily restrictions include later protocol-review receipts — 2026-10-17

The morning planner must read data/source_access_restrictions.json and current inventory access_restrictions before every native/Web/protocol plan, in addition to the previous daily receipt. The October16 afternoon independent review recorded49 exact403 routes after the daily receipt; selecting only the last daily ignored these restrictions. The October17 premature requests are explicitly recorded in execution-deviations.json, not erased or labelled compliant. Treat a prior explicit master-denial narrative as binding even when the serialized attempted_urls contains only its fallback; preserve the original evidence rather than infer permission from missing rows. Normalize www/trailing slash aliases for the same denied route without banning unrelated domains or permitted protocol pages. The new run wrapper checks exact restrictions again at dispatch; its no-network guard check covers all49 known denials. No current roster/date claims may be fabricated from a skipped route.

## VGS-002 identity and conservative closure — 2026-10-19

The newly read entire Vetigenics sponsor pipeline names VGS-002 anti-PD1 canine urothelial carcinoma and marks both Ethos and BARC Closed. The historical sponsor primary identifies this exact protocol; fresh complete AVMA object15973/VCT23005729 is Completed. Hide existing penn-anti-pd1-urothelial-carcinoma, preserving original clinical/funding dates. This is not Purdue anti-PDL1/AKS-701d or CHECKMATE-K9. The fresh VSH North County primary still says OPEN and lists CASE Boulder, Metropolitan Cleveland East and VSH North County; preserve that source conflict, not a new active third site. The sponsor's other two closed families do not establish additional currently active canonical trials. Evidence: research/audit-runs/daily-20261019T032107-0400/.

The original40 full-fresh-review backlog now has4 independently reviewed,3 confirmed closures and33 still pending; a current unchanged full page/object is not a new clinical-review date. For an unvisited restricted source, source_result=not_checked describes this run, while new_last_result/last_checked/last_checked_at must remain the actually persisted previous inventory values. Do not invent a new inventory result from a skipped visit. October19 retained one NOT VERIFIED Cambridge alias/action question rather than claim all-source processing complete. Exact rejected mixed-batch output is excluded by an explicit publication allowlist.

## Osteosarcoma cohort contradictions — 2026-10-21

Tufts actionable-targets has two alternative cohorts, not one unrestricted OSA basket. `requires.eligible_cohorts` preserves one protocol identity while browser and shared Python screening require at least one cohort consistent with known owner answers. Group A is limb OSA before amputation without obvious spread; Group B is metastatic OSA after amputation and prior carboplatin or study drugs. Do not force prior chemotherapy for Group B: the form cannot identify prior non-chemotherapy study drugs. Unknown staging/history remains prescreening, never a confirmed match. Surgery procedure type is ignored when surgery=No. Browse mode remains diagnosis-only. Full primary criteria and source-derived regression cases are in the existing protocol review; do not refresh the frozen baseline. This focused selection correction does not constitute a fresh recruitment audit of every OSA study.

## CMP-002 treatment-matcher exclusion — owner decision 2026-10-21

Following the explanation of MSU's CMP-002 dose-escalation study and its two experimental arms, the owner directed removal from treatment matching. Set `msu-sting-cmp002-solid-tumors.available_for_matching=false` across all diagnoses. Preserve the record, actual recruiting/status confidence, clinical/funding/source dates and both-arm evidence; this is an owner scope decision, not a trial closure. Do not restore from an unchanged MSU recruiting page. The owner's subsequent condition retains Ghent only if the operation is funded. The official English veterinary information page confirms free pathology and no additional study costs, but no surgery coverage. Therefore also disable `be-ghent-fluorescence-lifetime-cancer-surgery` for matching; preserve its recruiting status and historical evidence. This supersedes the interim intention to retain it based on standard surgery alone. No AOI decision is implied.

## Cancer-wide owner-answer reconciliation — 2026-10-21

The follow-up to the osteosarcoma review checks the full150-record public selection set while reusing dated primary-derived reviews; it is not a fresh all-source recruitment audit. Ten data corrections enforce known primary splenic HSA site, pre-splenectomy entry/strict EPUSH bounds, Melbourne adjunct doxorubicin/splenectomy, Johns Hopkins brain chemoradiation, SOLID-Relapse intake and chemotherapy, chemotherapy-naive Purdue/Aurelius lymphoma intake, and known lymphoma lineage restrictions for Nihon/PETcura. Evidence dates remain original for reused restricted sources; refreshed primary criteria reviews are identified separately.

Every owner-answerable condition must be enforced where the form already collects it. `when_family` scopes phenotype rules to lymphoma so stale hidden controls cannot exclude sarcoma/myeloma. `when_field` scopes procedure history to surgery=Yes. Do not treat a prior diagnostic biopsy as cancer-treatment surgery, infer a particular anatomic subtype from a broad diagnosis, or enforce an unavailable field as a known answer. Unknown medical criteria stay visible for investigator screening.

Treatment-backbone and inclusion-policy reviews are separate from code parity. MSU quasiorganelle, Auburn dose-finding palbociclib, Penn STEAP1 pilot, Mexico news-only access and AOI superficial-tumor mapping retain explicit owner/primary-evidence questions; this reconciliation does not silently settle those previously pending medical decisions. Preserve the frozen protocol-selection baseline and previous owner exclusions. Receipt, full public-ID dispositions and changed cases are in `research/audit-runs/cancer-selection-wide-20261021/`.

## Rhode Island local cancer-care discovery — 2026-10-22

Owner prioritized poorly covered US states and selected Rhode Island for the first single-executor pass. No automation was created or modified. Ten verified local physical care listings expand RI from one to eleven; OSVS gains its independently confirmed local tumor surgery. General-practice tumor removal is not specialist certification. Wood River explicitly lists chemotherapy, ECT and cancer vaccines, without a verified vaccine brand or assigned oncologist. Newport clinician interests alone remain insufficient for chemotherapy delivery. PCC Providence remains pre-opening. CloudVet is relief staffing, not an owner-bookable cancer-care practice. Receipts, primary facts, exact remaining gaps and old/new row preservation are in research/audit-runs/ri-care-20261022/. RI remains incomplete in territories.json; do not restart resolved candidates merely from unsupported directory tags.

The historical European recovery test froze whole-directory counts and hashes. Later verified care deltas must be checked against exact accepted current-row hashes and reversed before applying the unchanged historical baseline assertions; the RI baseline-projection.json does this without weakening European identities, dates, service hashes or country-completion gates. The Help validator verifies its mandatory wording case-insensitively because shared sentence-case normalization can already have run; this changes no displayed text.

## FAM-010 Urbana upcoming listing — owner decision 2026-10-23

The owner explicitly requested publication of FAM-010 after reviewing its dose-finding purpose and Enrolling soon status. Publish this one splenic-hemangiosarcoma protocol in potential treatment search with Enrolling soon in the visible title and status; do not describe treatment enrollment as open. The current sponsor's Contact the study team button was actually clicked and opened a three-step inquiry form. No personal information was entered or sent. The sponsor's placeholder phone/email footer does not negate this working inquiry route. `status_confidence=current` records the accepted current published protocol/inquiry listing, while `recruitment_status=enrolling_soon` and its explicit confidence basis preserve the unconfirmed treatment-start status. This scoped owner decision does not activate other pipeline or safety-only programs.

Owners with splenectomy scheduled or pathology pending may inquire. Do not require another future surgery after a completed splenectomy, or imply histology is unnecessary before actual enrollment. The first dose must fit within21days after surgery; chemotherapy, radiation and other investigational-drug history and breeding restrictions remain literal. Funded study screening/treatment/follow-up does not establish funded prior surgery or travel. Retain dose/safety, unproven survival/cardiac benefit and expected permanent male infertility disclosures. Source-derived cases and fresh Web/browser receipts are in `research/audit-runs/fam010-owner-publish-20261023T061829-0400/`. Keep the morning audit report unchanged; this is a later targeted intake, not a new global traversal.

## Tufts SABR public verification date — 2026-10-23

The SABR card retained October3 although the independent criteria review was dated October16 and daily retrievals compared the full unchanged protocol. A fresh complete primary review confirms current recruitment, pulmonary-metastasis criteria, funding and contact; synchronize canonical verified/funding_verified to October23 and use the current official lung-metastases redirect destination. Future completed full protocol reviews must persist their actual public date, including unchanged clinical fields; retrieval/equality checks alone still do not refresh it. Fibrosarcoma remains a legitimate sarcoma-family prescreening candidate under this canine protocol, only for qualifying progressive lung metastases. Independent cases cover no metastases (exclude), confirmed/unknown spread (prescreening) and cats (exclude). Screenshots alone do not reveal the submitted staging answers. No form or public-copy change is made. Receipt: research/audit-runs/tufts-sabr-verification-20261023/review.json.


## Rhode Island systematic pass closeout —2026-10-23

Owner requested finishing RI after the six inaccessible-source followup. The current pass screens44 locality directory pages/122 profiles and maps geographic discovery to39 municipalities; this is not122 primary service verifications or an exhaustive Maps census. Prior24 dispositions are inherited with their actual dates and resolved into publication/exclusion/future-opening/current-service uncertainties. Publish only two new surgery locations: Hope and Cumberland. Hope's announced renovation throughNovember2026 may affect surgery scheduling. Keep Ferguson's ocular tumor removal outside publication under the owner's explicit correction. PCC Providence announcesNovember30opening and names existingOSVS physicianCalebAlexander; do not infer another new current oncologist or current departure fromOSVS. VCCS published mobile area isCT/NY. RISPCA public-owner access is confirmed from official infographic, but generic mass removal is not a confirmed malignant-tumor service.

Queue completed=true describes a systematic discovery pass with named exceptions, not exhaustive verification of every practice or proof that no other oncologist exists. Six current-service/identity uncertainties and three exact403 professional-directory routes remain documented; no broad automatic rediscovery or messages are authorized. Receipts and continuation triggers:research/audit-runs/ri-finish-20261023/. Later exact two-row inverse projection preserves the unchanged historical European hashes andOctober22RIprojection.


## Rhode Island six-exception final followup —2026-10-23

Owner explicitly requested finishing the remaining six after systematic closeout. Add Foster as Local oncology care only: its current official canine-service list explicitly offers cancer treatment, and current contact/veterinarian roster meet the existing core-local-care gate. Unknown modality must not exclude an otherwise verified local-care clinic; do not infer chemotherapy or cancer-specific surgery from generic mass removals. TotalRI14physical/2chemotherapy/1ECT, no new specialist. Newport recovered story describes2007–2008care, not2022/current therapy. Current VOS onco.vet contact roster listsNY/FL/AK, noRI; secondary2026RIreference remains insufficient. Caldwell native200 is an empty redirect to /lander, not a recovered clinical page or closure evidence. WestPaws503 and AnimalCareServicesFacebookDisabledError leave primary gaps. All six decisions and actual receipts are in research/audit-runs/ri-six-final-20261023/; four insufficient primary sources and one unconfirmedRIassignment cannot honestly be converted to verified services. No outreach or broad rediscovery.


## Rhode Island SEO state-page pilot —2026-10-23

Owner approved one substantive Rhode Island care landing page to test search discovery, not automatic pages for all states. `seo/oncology_state_pages.py` generates `/veterinary-oncology/rhode-island/` from exact USA/RI physical rows in the canonical care catalog. Keep dedicated oncology, local chemotherapy/ECT and other local/surgical care distinct; never present all locations as specialist oncologists. Individual record dates are inherited, not refreshed by page generation. The coverage review date describes the October23 state work, not fourteen new source visits. The global care finder links to this guide. Build it before indexing cleanup and site search so canonical/sitemap/internal-search content are generated normally; no alternate static copy or new tracking. Counts/services/contact details update with the catalog. Only this one state is approved; no doorway-page expansion. Search Console URL inspection requires actual access; sitemap inclusion alone is not a submitted request or proof of Google indexing/ranking.


## Nebraska saved-lead discovery —2026-10-23

Owner selected a further large poorly covered US state; current NE catalog had3locations. Single-executor pass reviews all11saved leads plus10new/due identities, adding8primary-verified physical locations (3chemotherapy,5tumor surgery);11NElocations total,6chemotherapy. Holdrege branch explicitly links its Internal Medicine/chemotherapy service and has a named branch roster; confirm its schedule and assigned clinician when booking. Do not duplicate Kearney or infer oncology certification. Other7new places have separately verified local treatment/contact/rosters. Preserve all previous rows and actual dates.

21candidate dispositions and13primary/access gaps are saved in research/audit-runs/ne-care-20261023/. Stransky third-party radiation/chemotherapy, Pitts supportive care during chemotherapy and VCA80Dodge historical chemotherapy remain insufficient. Exact403/429routes are recorded in the care restriction index, not a statewide/domain prohibition. This packet is complete but statewide small-town discovery remains partial; queue completed=false. The8-row exact inverse projection extends the historical European preservation test without weakening its frozen counts/hashes or RI checks. No new state SEO page, UI, navigation or automation is authorized by the care pass.


## North Dakota local-care discovery —2026-10-24

Owner selected a genuinely underserved large state and requested dense single-executor discovery. Publish12 new physical locations (8explicit tumor/mass-removal surgery,4limited local cancer-care offerings), plus ONE Oakes/Edgeley/Ellendale network surgery contact via shared email; do not clone its service to3branches or use a branch telephone as central. Lisbon’s main office has full medical/surgical scope; its satellite oncology allocation stays unconfirmed. Casselton and Fargo have explicit branch oncology/Internal Medicine pages, but chemotherapy and assigned clinicians are unconfirmed; owned roster/careers routes returned403.

State Ave Dickinson gains chemotherapy from its clinic-authored February12,2026 NDVTA recruitment advertisement, corroborated by current owned oncology treatment/referral and team pages. No oncologist credential, protocol or open chemotherapy appointment inferred. Red River Fargo still explicitly rejects new oncology patients; retain false intake despite generic service text below the notice. Rugby receives a service-page inventory check only, not a fresh full-team/public verification date. Result15physical+1network inND does not mean15specialist centers; no new specialist established.

Evidence, individual dispositions, exact access restrictions, dated request locators, field old/new hashes and unfinished rural/source frontier are in research/audit-runs/nd-care-20261024/. ND remains completed=false. No specific three-hour drive time or exhaustive statewide absence claimed. A later exact ND inverse projection preserves the frozen EU/RI/NE regression baselines. No new state SEO page or automation.


## North Dakota systematic discovery closeout —2026-10-24

Owner requested finishing the remaining ND search. All12multi-entry city pages and40single-entry localities of the chosen secondary directory were screened (96raw entries; duplicates/non-clinical noise retained in coverage), with additional NDVMA/rural/mobile discovery. Its118raw professional labels are not118clinics. Golden Valley’s owned services recovered; Northwest/Bowman lack current owned cancer-service evidence; All Pets Bismarck has generic professional copy and a blocked Facebook page. Preserve those as source/service uncertainties, not unprocessed candidate work or proof of no treatment. Queue completed=true means this documented systematic discovery pass is closed with named exceptions, not a complete independent clinical census.

Publish4more local surgery locations: Enderlin, Valley Veterinary Fargo, Two Rivers West Fargo and New Salem. Current owned procedure lists explicitly support tumor/mass/lump removal; none establishes chemotherapy or oncologist certification. Red River’s separate current surgery page supports oncologic operations and referral appointments with residency-trained David Silliman; add Surgery while retaining accepting_new_patients=false for oncology and explicitly requiring confirmation of surgical-case acceptance. Do not infer reopened medical oncology or board certification. TotalND19physical+1network; no further chemotherapy or medical oncologist established. Exact4addition/1update inverse projection preserves all historical EU/RI/NE/ND assertions. Receipts and exceptions:research/audit-runs/nd-finish-20261024/. No new state SEO page, outreach or automation.


## North Dakota additional-search followup —2026-10-24

The owner continued the drug/clinician/partner search in a new chat. Gilbertson Cavalier now has current owned mass-removal/surgical-biopsy, veterinarian and contact evidence: add one local Surgery location, bringing ND to20physical+1network. This resolves the earlier unestablished-service disposition without rewriting its receipt. Torigen appears only in a Facebook search excerpt whose author/date/clinic attribution could not be verified; no cancer-vaccine or chemotherapy service is confirmed. The clinic’s historical opening announcement said surgery would be added later; the current owned Services page explicitly lists it. No oncologist credential or intake schedule inferred. Preserve prior rural/source exceptions; this is an additional focused pass, not a new independent statewide census. Evidence and exact-row inverse projection: research/audit-runs/nd-extra-20261024/.


## North Dakota state guide — owner-authorized 2026-10-24

The owner requested the North Dakota page after publication of the Cavalier addition. Add only /veterinary-oncology/north-dakota/ alongside the approved Rhode Island pilot, through seo/oncology_north_dakota.py and the existing production build. Use all exact USA/ND canonical identities:20physical locations and1network contact at this baseline. Show Red River separately under intake restrictions, never among currently accessible chemotherapy contacts; retain the literal oncology closure and distinct surgery-referral question. Dickinson local chemotherapy remains protocol/appointment-to-confirm. Network surgery is one email route, not three branch cards. Inherit clinic dates and service limits; page creation is not a fresh source review. Shared existing guide CSS is extracted without changing Rhode Island output. Link from the care finder and include canonical, sitemap, ItemList and internal search. No other state page is approved by this request. Build checks scripts/test_north_dakota_page.py and the unchanged Rhode Island scope checks; verify deployed guide and finder bytes before reporting live.


## Wyoming systematic local-care discovery —2026-10-26

Owner authorized the next full state pass. Publish20new physical locations and one visiting surgical service, update evidence for3existing chemotherapy clinics: Wyoming23physical+1mobile,5chemotherapy. New chemotherapy is Lifetime Cody and Jackson Animal Hospital. Of the remaining18newphysical,17explicitly support tumor/mass/lump surgery and Salt Creek supports local cancer treatment with modality unconfirmed. Lifetime also supports surgery. Ace Mobile Vet Surgery is one service coveringWY, with no fixedWYoffice or invented coordinates; Jayce Lineberger is ACVS, not a medical oncologist. No new radiation/ECT or boardedmedicaloncologist established. Existing3modalities preserved.

The chosen50locality routes/132profile-category rows include duplicate, nonclinical and historical noise; they are not a verified clinic census. Discovery is closed with named primary/access/clinician/branch exceptions, not statewide absence claims. GemCity,CheyennePet,AlpineLaramie,BestFriendsCasper,BearRiver,MoxeySchreiber,WesternVet and historicalTharp remain separately qualified. Never copy Montana namesake chemotherapy to Casper or COAlpine to Laramie, splitWesternVet tumor surgery into unverified branches, or clone Uinta treatment to relatedCastleRock. Regional referral options stay outsideWYidentities.

Evidence, exact source attempts, discovery ledgers, exceptions and accepted-row inverse projections are in research/audit-runs/wy-care-20261026/. Preserve all unrelated hashes and frozen historical regression assertions. Main staticbuild and caregates pass; E-package ancillary street assertion fails on existing networkcontacts already present at6254ff7 and is documented as baseline. No new stateSEOpage,UI,navigation,outreach or automation is authorized by this carepass.


## Wyoming independent discovery followup —2026-10-26

Owner challenged the one-directory closeout and requested finishing first. IndependentAnimalShelter82raw/VetLookup102raw/LostPet50visible records, localcommunitysources,98savedqueries and54individualdispositions broaden discovery. LostPetpage2repeats50entries despiteadvertised75; don'tcountit as75reviews. These rawinventories include doctors/aliases/nonclinicalnoise, not clinicalcensuses. Do not infer everylicensedvet's currentclinicalservice fromtheboard.

Add3physicaltumor/mass-surgery clinics:AnimalHealthCenterLaramie,ElevateCheyenne,WesternVetBigPiney; addHeartland asONE mobile surgical service. Heartland's ownsiteidentifiesmobileunitandregular411EagleLaneparking, not anofficeatsecondary353EagleLane. Usecontactfooter3073339961; headeralso6771617. Western's clinician gap is resolved by currentstateactive-license788and2026firsthand clinicinterview; ownedsmallanimalpage, nothorseinterview, establishesdog/cattumorremoval. Kemmererallocationunconfirmed; noclone. VCASpringCreekgainssurgeryandvisitingACVSsurgeonsJoshuaJackson/JasonWheeler, withcurrentBridger/2026ACVScredentialcorroboration; schedulestoconfirm. NevertransferBridgerMTmedical/radiationoncologytoWY. TotalWY26physical+2mobile,5chemo.

Evidence:research/audit-runs/wy-finish-20261026/. Oldfirstpasscompleteclaimisqualifiedbymulti-sourcefollowup, not replacedwithastatewideprimarycensus. GemCity,CheyennePet,AlpineLaramie,BestFriendsCasper,BearRiver,Moxeyandothernamedlocalitiesretainexactservice/access/freshnessquestions. BigHornBuffalocancertestimonial isnotcurrentmodalityevidence; GillettePetVetadvertiseddomain'sMainecontentandFremontShoshoni.toplistingtemplatearenotclinic-ownedcancerprooforclosureproof. Nooutreach/newstatepage/UI/editorialchange. Preservehistoricaltesthashesusingexact5-rowfollowupprojectiononly.

## Wyoming state guide — owner-authorized 2026-10-27

The owner requested the Wyoming page after the care data was published. Generate only `/veterinary-oncology/wyoming/` through `seo/oncology_wyoming.py` and the existing production build, using exact USA/WY canonical identities. At this baseline it contains26physical locations and2mobile services, with5physical chemotherapy listings. Separate local chemotherapy, other local cancer care/surgery and mobile services; do not turn a chemotherapy or Medical oncology service label into a board-certified clinician claim. VCA Spring Creek's visiting Bridger surgeons are surgical specialists, not proof of local medical/radiation oncology. Heartland and Ace stay one mobile listing each, with service area and no invented fixed address/distance pin. Salt Creek's unconfirmed modality must not become surgery or chemotherapy.

Reuse the existing guide layout, inherit individual source dates and the October26coverage-review date; publication is not a new source audit or a statewide primary clinical census. Link from the care finder and include canonical/sitemap/ItemList/internal search normally. No other state guide, redesign or catalog re-verification is implied. Run `scripts/test_wyoming_page.py` with the existing Rhode Island/North Dakota and production build checks, then verify remote and deployed guide/finder bytes.

## Targeted completion of stopped trial audit — 2026-10-27

The owner requested finishing the stopped pass. The targeted continuation is `research/audit-runs/finish-20261027T063052-0400/`, linked to the actual morning traversal and October26 recovery. Its consolidated `receipt-final.json` preserves the ORIGINAL daily run ID, visits and timestamps; it is not a second traversal. The continuation separately records its one new official Missouri thesis read. Do not call an inherited visit a new visit or retroactively complete October26. Ninety old source-processing questions were compared with individual current decisions. A substantive omission was found: Nihon had four fully read treatment protocols but only two canonical records. Add the distinct head/neck alternating-field and glioma IL12 studies from the official current index and individual pages; study-related field-treatment examinations/treatment are free, IL12 costs are unpublished. Preserve canine-only scope, anesthesia/device-fit screening and the glioma diagnostic-pathway ambiguity; mouse results are not canine efficacy.

AVMA15839 supports MIMIC's mandatory thoracoscopic lung metastasectomy: preserve site/intake uncertainty but reject a patient declining surgery. VetAgro's full published primary/funding/contact reread and four source cases were completed without turning secondary numeric filters into primary facts. Edinburgh's2024 invitation supports species/disease regression cases, not current2026 intake. Explicit `full_protocol_reverified:false` case reviews must not satisfy the timestamp-based fresh full-review gate. Normal source-case coverage is142/155 with13 gaps; the stricter post-October16 full-review gate remains INCOMPLETE for31 protocols, including28 restricted primary routes. Missouri's May2026 thesis reports prospective enrollment August2024–August2025; that result and master-page absence alone do not establish closure or a new cohort. Preserve the Mexico news-only owner-decision proposal. Processing completion and strict evidence completeness remain different results; never use a processing flag in place of canonical protocol reconciliation.


## Homepage search-title brand restored — owner-authorized 2026-10-28

The owner explicitly requested restoring Vet Trial Finder to the homepage search title after reviewing branded-query results. The final sentence-case pass now uses `Vet Trial Finder | Find cancer care for dogs and cats` for the homepage title and matching social-title metadata. This is a homepage-only exception to the October11 unbranded-title policy; other routes, visible headings, UI, schema and navigation remain unchanged. Keep both title validators aligned with this narrow exception so later rebuilds preserve it. The observed ranking issue does not prove that the previous title caused it or that restoring branding guarantees ranking recovery.
