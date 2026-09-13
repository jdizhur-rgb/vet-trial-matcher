# Daily Veterinary Oncology Trial Audit Algorithm

This checklist is mandatory for every daily catalog update.

## Daily cadence and search window

- The daily discovery run is scheduled for **06:00 America/New_York**.
- Daily discovery is **incremental**: search only publications, posts, announcements and newly published pages from the **immediately preceding calendar day** in America/New_York.
- Do not rerun the same broad historical discovery searches every morning and do not re-process older material already reviewed on previous days.
- A source without a reliable publication/post date is not treated as a new daily-discovery item.
- Every genuinely new lead must still be followed to the primary/current source and checked for current recruitment/access, eligibility, funding, contacts and treatment relevance before any catalog change.
- Every proposed addition must be deduplicated against the **entire effective live catalog**, not merely against the previous day's discoveries.
- If no qualifying new publication appeared during the preceding day, the daily result is simply: no new publication to add.
- A separate **weekly deep/control audit** handles work that the 24-hour discovery window intentionally does not: status changes to existing trials, silently edited/undated pages, missed or late-indexed publications, complete institutional trial-index reconciliation, stale records and broader historical gap checks.

## Required registry/source coverage

- **AVMA Veterinary Clinical Trials Registry (veterinaryclinicaltrials.org) is a mandatory discovery and reconciliation source for U.S. veterinary oncology trials.** Check newly surfaced registry studies during daily discovery when they have a reliable new/updated date, and perform a full oncology reconciliation against the registry during the weekly deep/control audit.
- Treat the AVMA registry as a discovery/structured-detail source, not as sufficient proof of current recruitment by itself. For every AVMA lead, verify current recruitment/access against the sponsoring university, hospital, investigator or study page whenever a current primary source is available.
- **MANDATORY PROTOCOL-LEVEL CHECK:** follow a lead to the individual study/protocol page whenever one exists. Verify that the page describes the same intervention/protocol, not merely the same cancer, investigator or institution. Read the study-level status, eligibility, funding/support, contacts and recruitment timeline before classifying it.
- An institutional trial index is navigation evidence, not definitive negative evidence. **Absence from a general university/hospital/center trial list is not proof that a study is closed.** Before moving a registry-listed study to inactive/watchlist for this reason, check the individual study page, PI/investigator page and current registry record; if those conflict, record the conflict rather than infer closure.
- Conversely, an individual page for a different protocol in the same cancer must never be used to confirm another protocol. Match identity by intervention, investigator/sponsor, disease population and eligibility, not by a generic page title such as “Osteosarcoma Clinical Trial.”
- Use AVMA structured fields to enrich existing canonical records when verified, especially recruitment start/end dates, funding/owner-cost range, investigator, intervention and participation details. Do not create a duplicate merely because the AVMA title differs from the canonical catalog title.
- If current protocol-level sources conflict and current recruitment cannot be established for the exact study, do not expose it to matching; retain it on the watchlist/inactive history with the conflicting evidence recorded until recruitment is reconfirmed.

## Catalog structure — read this before editing

- `data/trials_base.json` is the single canonical catalog used by the matcher and SEO generator.
- Do **not** create runtime update layers or modular catalog patch files.
- Keep unverified discoveries in research notes or watchlists. Promote only verified changes directly into the canonical catalog.
- Before creating a new record, inspect the full canonical catalog exactly as the patient-facing loader reads it. Do not infer absence from code search or from a research-note file.
- **GitHub code search is discovery/navigation only. A zero-result code search is never evidence that a protocol is absent from the catalog.** Large JSON files and generated/effective records may not be indexed or returned reliably.
- Do not create institution-specific duplicate-avoidance exceptions or memory lists. The same effective-catalog semantic-dedup procedure applies to every university, hospital, company and registry.
- Do not load other JSON files in `data/` into the matcher. The directory also contains statistics, watchlists, audit reports and ECT-center data; only `trials_base.json` is catalog input.

1. For the **daily** run, discover only material published/posted during the immediately preceding calendar day. Existing-record status sweeps belong to the weekly deep/control audit unless a new daily lead directly reveals a material status correction.
2. Search for new dog/cat anticancer treatment opportunities across all required regions and source layers within that daily publication window.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - Include the AVMA Veterinary Clinical Trials Registry under the required registry/source rules above.
   - Complete center-wide reconciliation is part of the weekly deep/control audit. When a new daily publication points to a center/protocol, inspect the relevant individual protocol and primary source immediately.
3. Apply the treatment-scope filter. Keep true anticancer treatment opportunities in treatment matching; classify treatment-access/support programs separately; do not promote observational/diagnostic/sample-only/supportive/prevention-only research into treatment matching.
4. Verify recruitment/access from a protocol-level primary source whenever available. If recruitment or protocol details are insufficient or conflicting, keep the lead on the watchlist rather than matching it.
5. Normalize disease labels, species, geography, treatment modality and source URLs.
6. **MANDATORY PRE-MERGE DEDUPLICATION:** compare every proposed record or update against the full canonical catalog.
   - Check exact ID and normalized URL matches.
   - Check semantic similarity of protocol title/intervention, cancer, species, center/investigator and eligibility.
   - Treat different source URLs or different IDs as possible representations of the same protocol.
   - A shared hospital/center index URL is **not** evidence of duplication by itself.
   - Similar titles for different interventions are **not** duplicates.
   - When the same protocol appears through multiple sources, keep one canonical record and merge the freshest verified details/primary source into it.
   - Ambiguous candidate pairs require review; never auto-delete on similarity score alone.
   - **Never create a new record merely because GitHub code search, filename search, or a single catalog component returns no match. Absence must be established against the constructed effective catalog.**
7. Only after deduplication, write confirmed additions, updates or deletions directly to `data/trials_base.json`.
8. Reload the canonical catalog and verify at least one representative matcher query.
9. Recalculate catalog statistics from the deduplicated effective catalog. Treatment totals must count only records that actually qualify for strict treatment matching.
   - Every daily run must collect and report the post-run effective-catalog statistics: total effective records; current strict treatment opportunities (`study_type == treatment` and `available_for_matching == true`); treatment opportunities by country; treatment opportunities by species; and the IDs/counts added, substantively updated, deleted/closed, or left on the watchlist during that run. Statistics are reporting only and must be calculated from the same effective-catalog loader used by the patient-facing matcher; collecting statistics must not itself alter catalog records.
10. Validate JSON and matcher behavior, including cancer aliases and visibility of any `Other` opportunity intended to be searchable.
11. Commit only after all checks pass. Record additions, substantive updates, closures, duplicate merges and unresolved watchlist leads in the daily audit output.

## Weekly deep/control audit

Once per week, perform a broader control pass independent of publication date. Recheck existing catalog records and institutional indexes against current primary sources; detect closures, pauses, recruitment/status changes, eligibility/contact/funding changes, silently edited or undated pages, late-indexed discoveries, stale records and historical gaps. **Reconcile the complete current AVMA Veterinary Clinical Trials Registry oncology set against the effective catalog, classifying each registry record as canonical match, genuinely new candidate, status/detail mismatch, or stale/unconfirmed registry entry. For each candidate or mismatch, drill down to the individual study/protocol page before changing live status.** This weekly pass is the safety net for anything that cannot reliably be discovered through the preceding-day publication filter.

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the **constructed effective live catalog** for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based. Search-index misses are not catalog misses, and institution-specific exception lists must not substitute for this universal check.
