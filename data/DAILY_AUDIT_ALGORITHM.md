# Daily Veterinary Oncology Trial Audit Algorithm

This checklist is mandatory for every daily catalog update.

1. Recheck current catalog records against primary/current sources for recruitment status, deadlines, eligibility, contacts, funding and treatment access.
2. Search for new dog/cat anticancer treatment opportunities across all required regions and source layers.
   - Include The Perseus Foundation / CRUSH public clinical-trial posts and trial listings as a **secondary discovery source**. Review newly surfaced studies/leads, then follow each lead to the originating university, hospital, investigator or registry page before making any catalog decision. Perseus/CRUSH is for discovery only and is never sufficient by itself to confirm recruitment status, eligibility, deadline, funding or treatment access.
   - For major universities and oncology centers, reconcile the center's complete current oncology/dog/cat trial index against the full effective catalog, not just individual studies found by search. For each index entry, inspect the individual protocol page when available. If an index says recruiting/current but the individual page has an expired enrollment deadline or conflicting status, do not match it as active; place it into status/watchlist review until primary-source status is resolved.
3. Apply the treatment-scope filter. Keep true anticancer treatment opportunities in treatment matching; classify treatment-access/support programs separately; do not promote observational/diagnostic/sample-only/supportive/prevention-only research into treatment matching.
4. Verify recruitment/access from a primary source. If recruitment or protocol details are insufficient, keep the lead on the watchlist rather than matching it.
5. Normalize disease labels, species, geography, treatment modality and source URLs.
6. **MANDATORY PRE-MERGE DEDUPLICATION:** compare every proposed new/upserted record against the full effective catalog (`trials_base.json` + `trial_updates.json` after deletes/upserts), not only against the current day's additions.
   - Check exact ID and normalized URL matches.
   - Check semantic similarity of protocol title/intervention, cancer, species, center/investigator and eligibility.
   - Treat different source URLs or different IDs as possible representations of the same protocol.
   - A shared hospital/center index URL is **not** evidence of duplication by itself.
   - Similar titles for different interventions are **not** duplicates (for example, separate glioma protocols using CAR-neutrophils vs ferumoxytol).
   - When the same protocol appears through multiple sources, keep one canonical record and merge the freshest verified details/primary source into it.
   - Ambiguous candidate pairs require review; never auto-delete on similarity score alone.
7. Only after deduplication, merge confirmed additions/updates/deletes into `data/trial_updates.json`.
8. Recalculate catalog statistics from the deduplicated effective catalog. Treatment totals must count only records that actually qualify for strict treatment matching.
9. Validate JSON and matcher behavior, including cancer aliases and visibility of any `Other` opportunity intended to be searchable.
10. Commit only after all checks pass. Record additions, substantive updates, closures, duplicate merges and unresolved watchlist leads in the daily audit output.

## Non-negotiable dedup rule

No new catalog record is committed until it has been checked against the entire effective catalog for exact, fuzzy and semantic duplication. Candidate generation may be automated; destructive duplicate removal must be conservative and evidence-based.
