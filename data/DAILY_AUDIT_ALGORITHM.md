# Daily Veterinary Oncology Trial Audit Algorithm

This checklist is mandatory for every daily catalog update.

## Catalog structure — read this before editing

- `data/trials_base.json` is the legacy/base catalog. Do **not** routinely append new discoveries to this large file.
- `data/trial_updates.json` is a legacy consolidated patch file. Do **not** default to editing or rewriting it for new discoveries.
- New audited additions/updates should be kept in **small modular JSON patch files** in `data/` (`{"upsert": [...], "delete": [...]}`), with descriptive/date-based names. Existing examples include `discovery_aurelius_20260905.json` and other audit/discovery patch files.
- Before creating a new record, search the base, legacy updates, and existing modular patch files. Never conclude that a treatment is missing after checking only `trials_base.json` or GitHub code search.
- A small discovery/audit patch is not useful to owners unless the patient-facing catalog loader actually consumes it. Every confirmed modular patch intended for matching must be connected to the effective catalog and then tested in the matcher.
- Do not blindly load every JSON file in `data/`: the directory also contains statistics, watchlists, audit reports, ECT-center data and other non-catalog documents. Only explicitly approved catalog patch files belong in the matcher input set.

1. Recheck current catalog records against primary/current sources for recruitment status, deadlines, eligibility, contacts, funding and treatment access.
2. Search for new dog/cat anticancer treatment opportunities across all required regions and source layers.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - For major universities and oncology centers, reconcile the center's complete current oncology/dog/cat trial index against the full effective catalog, not just individual studies found by search. For each index entry, inspect the individual protocol page when available. If an index says recruiting/current but the individual page has an expired enrollment deadline or conflicting status, do not match it as active; place it into status/watchlist review until primary-source status is resolved.
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

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the entire effective catalog for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based.
