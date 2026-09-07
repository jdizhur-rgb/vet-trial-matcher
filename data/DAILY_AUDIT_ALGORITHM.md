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

## Catalog structure — read this before editing

- `data/trials_base.json` is the legacy/base catalog. Do **not** routinely append new discoveries to this large file.
- `data/trial_updates.json` is a legacy consolidated patch file. Do **not** default to editing or rewriting it for new discoveries.
- New audited additions/updates should be kept in **small modular JSON patch files** in `data/` (`{"upsert": [...], "delete": [...]}`), with descriptive/date-based names. Existing examples include `discovery_aurelius_20260905.json` and other audit/discovery patch files.
- Before creating a new record, search the base, legacy updates, and existing modular patch files. Never conclude that a treatment is missing after checking only `trials_base.json` or GitHub code search.
- A small discovery/audit patch is not useful to owners unless the patient-facing catalog loader actually consumes it. Every confirmed modular patch intended for matching must be connected to the effective catalog and then tested in the matcher.
- Do not blindly load every JSON file in `data/`: the directory also contains statistics, watchlists, audit reports, ECT-center data and other non-catalog documents. Only explicitly approved catalog patch files belong in the matcher input set.

1. For the **daily** run, discover only material published/posted during the immediately preceding calendar day. Existing-record status sweeps belong to the weekly deep/control audit unless a new daily lead directly reveals a material status correction.
2. Search for new dog/cat anticancer treatment opportunities across all required regions and source layers within that daily publication window.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - Complete center-wide reconciliation is part of the weekly deep/control audit. When a new daily publication points to a center/protocol, inspect the relevant individual protocol and primary source immediately.
3. Apply the treatment-scope filter. Keep true anticancer treatment opportunities in treatment matching; classify treatment-access/support programs separately; do not promote observational/diagnostic/sample-only/supportive/prevention-only research into treatment matching.
4. Verify recruitment/access from a primary source. If recruitment or protocol details are insufficient, keep the lead on the watchlist rather than matching it.
5. Normalize disease labels, species, geography, treatment modality and source URLs.
6. **MANDATORY PRE-MERGE DEDUPLICATION:** compare every proposed new/upserted record against the full effective catalog: base + legacy updates + all approved modular catalog patches.
   - Check exact ID and normalized URL matches.
   - Check semantic similarity of protocol title/intervention, cancer, species, center/investigator and eligibility.
   - Treat different source URLs or different IDs as possible representations of the same protocol.
   - A shared hospital/center index URL is **not** evidence of duplication by itself.
   - Similar titles for different interventions are **not** duplicates (for example, separate glioma protocols using CAR-neutrophils vs ferumoxytol).
   - When the same protocol appears through multiple sources, keep one canonical record and merge the freshest verified details/primary source into it.
   - Ambiguous candidate pairs require review; never auto-delete on similarity score alone.
7. Only after deduplication, write confirmed additions/updates/deletes to a small modular catalog patch. Avoid growing the legacy consolidated file unless a migration/compaction is intentionally being performed.
8. Ensure every approved modular patch intended for matching is included by the patient-facing catalog loader; verify at least one representative query after connecting it.
9. Recalculate catalog statistics from the deduplicated effective catalog. Treatment totals must count only records that actually qualify for strict treatment matching.
10. Validate JSON and matcher behavior, including cancer aliases and visibility of any `Other` opportunity intended to be searchable.
11. Commit only after all checks pass. Record additions, substantive updates, closures, duplicate merges and unresolved watchlist leads in the daily audit output.

## Weekly deep/control audit

Once per week, perform a broader control pass independent of publication date. Recheck existing catalog records and institutional indexes against current primary sources; detect closures, pauses, recruitment/status changes, eligibility/contact/funding changes, silently edited or undated pages, late-indexed discoveries, stale records and historical gaps. This weekly pass is the safety net for anything that cannot reliably be discovered through the preceding-day publication filter.

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the entire effective catalog for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based.
