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
- Use AVMA structured fields to enrich existing canonical records when verified, especially funding/owner-cost range, investigator, intervention and participation details. Do not create a duplicate merely because the AVMA title differs from the canonical catalog title.
- If AVMA lists a study but the current sponsor/institution source no longer lists it as open, do not expose it to matching; retain it on the watchlist/inactive history until recruitment is reconfirmed.

## Catalog structure — read this before editing

- `data/trials_base.json` is the legacy/base catalog. Do **not** routinely append new discoveries to this large file.
- `data/trial_updates.json` is a legacy consolidated patch file. Do **not** default to editing or rewriting it for new discoveries.
- New audited additions/updates should be kept in **small modular JSON patch files** in `data/` (`{"upsert": [...], "delete": [...]}`), with descriptive/date-based names. Existing examples include `discovery_aurelius_20260905.json` and other audit/discovery patch files.
- Before creating a new record, inspect the **effective catalog exactly as the patient-facing loader builds it**: base + legacy updates + every approved modular catalog patch, with deletes and ID upserts applied. Do not infer absence from one component file.
- **GitHub code search is discovery/navigation only. A zero-result code search is never evidence that a protocol is absent from the catalog.** Large JSON files and generated/effective records may not be indexed or returned reliably.
- Do not create institution-specific duplicate-avoidance exceptions or memory lists. The same effective-catalog semantic-dedup procedure applies to every university, hospital, company and registry.
- A small discovery/audit patch is not useful to owners unless the patient-facing catalog loader actually consumes it. Every confirmed modular patch intended for matching must be connected to the effective catalog and then tested in the matcher.
- Do not blindly load every JSON file in `data/`: the directory also contains statistics, watchlists, audit reports, ECT-center data and other non-catalog documents. Only explicitly approved catalog patch files belong in the matcher input set.

1. For the **daily** run, discover only material published/posted during the immediately preceding calendar day. Existing-record status sweeps belong to the weekly deep/control audit unless a new daily lead directly reveals a material status correction.
2. Search for new dog/cat anticancer treatment opportunities across all required regions and source layers within that daily publication window.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - Include the AVMA Veterinary Clinical Trials Registry under the required registry/source rules above.
   - Complete center-wide reconciliation is part of the weekly deep/control audit. When a new daily publication points to a center/protocol, inspect the relevant individual protocol and primary source immediately.
3. Apply the treatment-scope filter. Keep true anticancer treatment opportunities in treatment matching; classify treatment-access/support programs separately; do not promote observational/diagnostic/sample-only/supportive/prevention-only research into treatment matching.
4. Verify recruitment/access from a primary source. If recruitment or protocol details are insufficient, keep the lead on the watchlist rather than matching it.
5. Normalize disease labels, species, geography, treatment modality and source URLs.
6. **MANDATORY PRE-MERGE DEDUPLICATION:** compare every proposed new/upserted record against the full effective catalog: base + legacy updates + all approved modular catalog patches, after applying the same merge/delete semantics as the live loader.
   - Check exact ID and normalized URL matches.
   - Check semantic similarity of protocol title/intervention, cancer, species, center/investigator and eligibility.
   - Treat different source URLs or different IDs as possible representations of the same protocol.
   - A shared hospital/center index URL is **not** evidence of duplication by itself.
   - Similar titles for different interventions are **not** duplicates (for example, separate glioma protocols using CAR-neutrophils vs ferumoxytol).
   - When the same protocol appears through multiple sources, keep one canonical record and merge the freshest verified details/primary source into it.
   - Ambiguous candidate pairs require review; never auto-delete on similarity score alone.
   - **Never create a new record merely because GitHub code search, filename search, or a single catalog component returns no match. Absence must be established against the constructed effective catalog.**
7. Only after deduplication, write confirmed additions/updates/deletes to a small modular catalog patch. Avoid growing the legacy consolidated file unless a migration/compaction is intentionally being performed.
8. Ensure every approved modular patch intended for matching is included by the patient-facing catalog loader; verify at least one representative query after connecting it.
9. Recalculate catalog statistics from the deduplicated effective catalog. Treatment totals must count only records that actually qualify for strict treatment matching.
   - Every daily run must collect and report the post-run effective-catalog statistics: total effective records; current strict treatment opportunities (`study_type == treatment` and `available_for_matching == true`); treatment opportunities by country; treatment opportunities by species; and the IDs/counts added, substantively updated, deleted/closed, or left on the watchlist during that run. Statistics are reporting only and must be calculated from the same effective-catalog loader used by the patient-facing matcher; collecting statistics must not itself alter catalog records.
10. Validate JSON and matcher behavior, including cancer aliases and visibility of any `Other` opportunity intended to be searchable.
11. Commit only after all checks pass. Record additions, substantive updates, closures, duplicate merges and unresolved watchlist leads in the daily audit output.

## Weekly deep/control audit

Once per week, perform a broader control pass independent of publication date. Recheck existing catalog records and institutional indexes against current primary sources; detect closures, pauses, recruitment/status changes, eligibility/contact/funding changes, silently edited or undated pages, late-indexed discoveries, stale records and historical gaps. **Reconcile the complete current AVMA Veterinary Clinical Trials Registry oncology set against the effective catalog, classifying each registry record as canonical match, genuinely new candidate, status/detail mismatch, or stale/unconfirmed registry entry.** This weekly pass is the safety net for anything that cannot reliably be discovered through the preceding-day publication filter.

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the **constructed effective live catalog** for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based. Search-index misses are not catalog misses, and institution-specific exception lists must not substitute for this universal check.
