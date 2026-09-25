# Daily Veterinary Oncology Trial Audit Algorithm

This checklist is mandatory for every daily catalog update.

## Daily cadence and coverage

- The daily discovery run is scheduled for **06:00 America/New_York**.
- Daily discovery is a **full catalog and source audit**, not a preceding-day news search. It must reconcile the persistent source inventory, review current catalog sources, and search the open web for new sources every day.
- Do not exclude an official page because it is old, undated, newly indexed or silently edited. Treat it as a lead and establish present recruitment/access from a current protocol-level official signal.
- The weekly deep/control audit is an additional independent safety net; it never replaces or narrows the required daily sweep.
- Every genuinely new lead must still be followed to the primary/current source and checked for current recruitment/access, eligibility, funding, contacts and treatment relevance before any catalog change.
- Every proposed addition must be deduplicated against the **entire effective live catalog**, not merely against the previous day's discoveries.
- If the full source sweep and open-web expansion find no qualifying current opportunity, report that the complete daily discovery ran and found none.

## Persistent source inventory

- `data/source_inventory.json` is the canonical discovery-source inventory. It contains registries, directories, universities, hospitals, specialty networks, sponsors/CROs, foundations and investigator/lab master pages.
- Every inventory entry is mandatory daily coverage. Record `last_checked`, `last_result` and a normalized-content SHA-256 fingerprint after each attempted visit. `unreachable` and `partial` are valid outcomes, but they must be reported; they are not permission to call the sweep complete without qualification.
- Add every newly discovered official master/index source to the inventory in the same run, even when its immediate trial lead is a duplicate, closed, ineligible or unresolved. A useful source must not disappear because its first lead was not added to the matcher.
- Never remove a source merely because it currently lists no eligible trials. Removal requires evidence that the source is permanently retired or replaced; preserve the replacement relationship in the audit record.
- Run `python scripts/validate_source_inventory.py` before committing. IDs and normalized master URLs must be unique, required fields must be present, and checked-state metadata must be internally consistent.
- Fingerprints detect a changed master page; they do not establish clinical meaning. A changed page must be opened and reconciled at protocol level before any catalog update.

## Required registry/source coverage

- **AVMA Veterinary Clinical Trials Registry (veterinaryclinicaltrials.org) is a mandatory daily discovery and reconciliation source for U.S. veterinary oncology trials.** Reconcile its current oncology set on every daily pass and repeat the reconciliation during the weekly deep/control audit.
- **UK Veterinary Clinical Studies Registry (veterinarystudiesregistry.co.uk/studies) is a mandatory UK discovery source.** Exclude cards marked sample/demo/AI-generated. A listing without that label is still only a lead: confirm that the investigator, institution, protocol and present recruitment are real with independent primary evidence before considering it for the dog/cat oncology catalog. Track changes in its actual recruiting count and relevant protocol-level records.
- Treat the AVMA registry as a discovery/structured-detail source, not as sufficient proof of current recruitment by itself. For every AVMA lead, verify current recruitment/access against the sponsoring university, hospital, investigator or study page whenever a current primary source is available.
- **MANDATORY PROTOCOL-LEVEL CHECK:** follow a lead to the individual study/protocol page whenever one exists. Verify that the page describes the same intervention/protocol, not merely the same cancer, investigator or institution. Read the study-level status, eligibility, funding/support, contacts and recruitment timeline before classifying it.
- An institutional trial index is navigation evidence, not definitive negative evidence. **Absence from a general university/hospital/center trial list is not proof that a study is closed.** Before moving a registry-listed study to inactive/watchlist for this reason, check the individual study page, PI/investigator page and current registry record; if those conflict, record the conflict rather than infer closure.
- Conversely, an individual page for a different protocol in the same cancer must never be used to confirm another protocol. Match identity by intervention, investigator/sponsor, disease population and eligibility, not by a generic page title such as “Osteosarcoma Clinical Trial.”
- Use AVMA structured fields to enrich existing canonical records when verified, especially recruitment start/end dates, funding/owner-cost range, investigator, intervention and participation details. Do not create a duplicate merely because the AVMA title differs from the canonical catalog title.
- If current protocol-level sources conflict and current recruitment cannot be established for the exact study, do not expose it to matching; retain it on the watchlist/inactive history with the conflicting evidence recorded until recruitment is reconfirmed.

## Catalog structure — read this before editing

- `data/trials_base.json` is the single canonical production catalog.
- Do not create update layers or catalog patch files. After review and deduplication, write the complete verified record directly to the canonical catalog.
- Before creating a new record, inspect the entire canonical catalog exactly as the patient-facing loader reads it. Do not infer absence from search indexes or audit reports.
- **GitHub code search is discovery/navigation only. A zero-result code search is never evidence that a protocol is absent from the catalog.** Large JSON files and generated/effective records may not be indexed or returned reliably.
- Do not create institution-specific duplicate-avoidance exceptions or memory lists. The same effective-catalog semantic-dedup procedure applies to every university, hospital, company and registry.
- Do not load other JSON files in `data/` into the matcher: the directory also contains statistics, watchlists, audit reports, ECT-center data and other non-catalog documents.

1. For the **daily** run, first visit every source in `data/source_inventory.json`, enumerate its current/open/recruiting oncology protocols, and reconcile them against the canonical catalog. Then perform open-web discovery for sources and protocols not yet represented in the inventory.
2. Search for dog/cat anticancer treatment opportunities across all required regions and source layers without a publication-date cutoff.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - Search public LinkedIn posts and news announcements from veterinary oncology researchers, study sponsors, hospitals, professional organizations, registries and credible veterinary publications for dog/cat cancer treatment recruitment, results and protocol updates. Use diagnosis and treatment terms with `clinical trial`, `study`, `recruiting`, `enrolling` and regional wording; include `site:linkedin.com/posts/` and official news/press-release searches because posts may not be visible in LinkedIn's own search. Compare leads against the effective catalog, then verify the actual protocol, current enrollment, eligibility and owner costs on the official study or sponsor page. A post or news story is a discovery lead, not proof of current access; do not treat inaccessible or unindexed posts as evidence that no study exists.
   - Include the AVMA Veterinary Clinical Trials Registry under the required registry/source rules above.
   - Complete master-page reconciliation is required daily. The weekly pass repeats it with deeper manual review, source-fingerprint comparison and unresolved-watchlist follow-up.
3. Apply the treatment-scope filter. Keep true anticancer treatment opportunities in treatment matching; classify treatment-access/support programs separately; do not promote observational/diagnostic/sample-only/supportive/prevention-only research into treatment matching.
4. Verify recruitment/access from a protocol-level primary source whenever available. If recruitment or protocol details are insufficient or conflicting, keep the lead on the watchlist rather than matching it.
   - Treat **new clinical evidence** as a separate discovery signal even when it does not announce a recruiting trial. For each new prospective study, comparative clinical cohort, randomized trial, regulatory decision or other material patient-outcome evidence, ask: **Is the treatment currently accessible to owners through ordinary veterinary prescribing, legal off-label use, a regulated product, a specialty center or a verifiable treatment-access program?**
   - If both the clinical evidence and a real current access route are present, evaluate the treatment for a diagnosis-specific cancer page or the Additional Oncology Options layer. Record the studied population, outcomes, study design and limitations, practical access route, contraindications and required monitoring. Do not add it to the clinical-trial count unless a separate current recruiting protocol exists.
   - A publication alone is not proof of access. Preclinical work, case reports, tiny uncontrolled series, hypothetical compassionate use and a drug being commercially sold without a realistic veterinary prescribing pathway remain watchlist signals only.
5. Normalize disease labels, species, geography, treatment modality and source URLs.
6. **MANDATORY PRE-MERGE DEDUPLICATION:** compare every proposed record or edit against the full canonical catalog.
   - Check exact ID and normalized URL matches.
   - Check semantic similarity of protocol title/intervention, cancer, species, center/investigator and eligibility.
   - Treat different source URLs or different IDs as possible representations of the same protocol.
   - A shared hospital/center index URL is **not** evidence of duplication by itself.
   - Similar titles for different interventions are **not** duplicates.
   - When the same protocol appears through multiple sources, keep one canonical record and merge the freshest verified details/primary source into it.
   - Ambiguous candidate pairs require review; never auto-delete on similarity score alone.
   - **Never create a new record merely because GitHub code search, filename search, or a single catalog component returns no match. Absence must be established against the constructed effective catalog.**
7. Only after deduplication, write confirmed additions, updates, or removals directly to `data/trials_base.json`.
8. Verify at least one representative matcher query after every catalog edit.
9. Recalculate catalog statistics from the deduplicated effective catalog. Treatment totals must count only records that actually qualify for strict treatment matching.
   - Every daily run must collect and report the post-run effective-catalog statistics: total effective records; current strict treatment opportunities (`study_type == treatment` and `available_for_matching == true`); treatment opportunities by country; treatment opportunities by species; and the IDs/counts added, substantively updated, deleted/closed, or left on the watchlist during that run. Statistics are reporting only and must be calculated from the same effective-catalog loader used by the patient-facing matcher; collecting statistics must not itself alter catalog records.
10. Validate JSON and matcher behavior, including cancer aliases and visibility of any `Other` opportunity intended to be searchable.
11. Commit only after all checks pass. Record additions, substantive updates, closures, duplicate merges and unresolved watchlist leads in the daily audit output.

## Weekly deep/control audit

Once per week, perform a broader independent control pass. Recheck existing catalog records and the entire persistent source inventory against current primary sources; detect closures, pauses, recruitment/status changes, eligibility/contact/funding changes, silently edited or undated pages, late-indexed discoveries, stale records and historical gaps.

The weekly pass must verify that `data/source_inventory.json` still includes the complete Veterinary Cancer Society resource list: the AVMA Veterinary Clinical Trials Registry, every listed university clinical-trial center, and every listed private/other center. For every reachable master/index page, enumerate all CURRENT, ACTIVE or RECRUITING oncology treatment protocols and reconcile every protocol against `data/trials_base.json`. Compare title and former title, intervention/drug, cancer type, center, participating sites, protocol identifiers and synonyms. A different title alone never makes a trial new. Compare current source fingerprints with the preceding recorded values so undated additions and silent edits are investigated. Report every unreachable or unchecked source explicitly; a partial pass must not be described as complete.

**Reconcile the complete current AVMA Veterinary Clinical Trials Registry oncology set against the effective catalog, classifying each registry record as canonical match, genuinely new candidate, status/detail mismatch, or stale/unconfirmed registry entry. Apply the same classification to every active protocol found on institutional and private-center indexes. For each candidate or mismatch, drill down to the individual study/protocol page before changing live status.** Absence from an index, conflicting status labels, or a renamed cohort is evidence for investigation, not automatic closure or a new record. This weekly pass is an independent safety net for sources, changes and unresolved leads missed by daily discovery.

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the **entire canonical live catalog** for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based. Search-index misses are not catalog misses, and institution-specific exception lists must not substitute for this universal check.


## Health-gate severity for daily and weekly audits

Health checks are diagnostic gates, not an all-or-nothing stop on any red signal.

- **BLOCKING:** unreadable/invalid canonical JSON; failure of the canonical validator on a current public opportunity; matcher compile/import failure; material canonical-to-production mismatch; production matcher unavailable together with another independent core failure; or another defect that makes the current public catalog unsafe to interpret. Stop and report.
- **NON-BLOCKING / INCONCLUSIVE:** stale UI-test assumptions, positional widget-selector failures, unavailable CI status, Chromium/session setup failure, or an isolated external-source/network failure while the core catalog/matcher checks pass. Record the problem and continue the source sweep.
- **DATA ISSUE:** legacy/inactive/partial records or historical metadata defects. Reconcile them during the run. They block only the affected record unless they contaminate public matching or cannot be safely distinguished from a current protocol.

Never terminate a weekly deep audit solely because one ancillary smoke test fails when production, canonical validation, compile/import, matcher logic and synchronization otherwise pass. The weekly run is complete only when mandatory source coverage has actually been attempted and reconciled.

Smoke tests must identify Streamlit widgets by stable labels/semantics rather than positional indexes so harmless form reordering does not create false health-gate failures.
