# AGENTS.md — Vet Trial Finder persistent project instructions

Read `PROJECT_OPERATIONS.md` in full before changing code, catalog data, source inventory, SEO, UI, workflows, or deployment. It is the canonical engineering and operations memory for this repository. Do not rely on chat history and do not rediscover settled architecture from scratch.

## Project purpose

Vet Trial Finder is a free, treatment-focused service for owners of dogs and cats with cancer. The public matcher must favor accuracy over record count and must not create false hope. A truthful “no matches” result is acceptable.

Production repository: `jdizhur-rgb/vet-trial-matcher`
Production branch: `main`
Canonical cancer catalog: `data/trials_base.json`
Source audit state: `data/source_inventory.json` and `data/audit_state.json`

## Non-negotiable catalog rules

- Match only a currently usable treatment opportunity or verified treatment-access program.
- Do not match observational, diagnostic-only, sample-collection, biomarker-only, biobank, research-only PK, or unsupported pipeline records.
- Never activate a record from a search snippet, news article, aggregator, disappearance from a master page, or an old registry status alone.
- Use the current institution page plus protocol-level primary evidence whenever available. Resolve conflicts conservatively.
- Preserve historical phases and useful provenance, but keep only the confirmed current cohort or protocol matchable.
- `available_for_matching` must reflect confirmed present owner access, not historical existence.
- Eligibility must be conservative. Explicit exclusions override broad cancer labels. Unknown material criteria remain for study-team confirmation.
- Funding language must be literal and precise: distinguish fully funded, partial coverage, reimbursement, incentive, free study drug, and owner-paid standard care. Never infer “free.”
- A multicenter protocol is one trial with multiple sites unless primary evidence shows distinct protocols or cohorts.
- Perform semantic dedupe by real-world identity, not ID equality or shared URL alone.
- Do not create partial metadata-only rows in the canonical catalog.

## Research and source rules

- Prefer official institution master pages, direct protocol pages/PDFs, sponsor pages, and recognized registries.
- Treat AVMA listings and other registries as evidence, not automatic proof of current recruitment.
- Do not close a trial solely because it disappeared from a center master page.
- Do not create a record from one search-engine snippet.
- Record unresolved conflicts honestly and keep them non-matchable until confirmed.
- Update `data/source_inventory.json` when a durable new master source is established.
- Use verification dates and source notes so future audits do not repeat settled work unnecessarily.

## Required completion loop

Before reporting a catalog/site change as complete:

1. Inspect the current canonical files and relevant history.
2. Verify the requested facts with primary sources.
3. Make the smallest coherent change; preserve unrelated user work.
4. Run the catalog validator and sanitation checks appropriate to the changed files.
5. Run unique-ID and semantic-dedupe checks for catalog changes.
6. Run matcher smoke/regression tests for every affected country/species/cancer combination.
7. Run source-inventory validation when source inventory changes.
8. Run relevant SEO/build checks when generated pages or site shell changes.
9. Inspect the final diff.
10. Commit and push only the verified final state, then verify the remote SHA.

A script, patch, local commit, intended workflow, or successful push attempt is not proof that production data is correct. Report exact commands and results. Never say “live” without deployment evidence.

## Product and editorial conventions

- Use sentence case, not Title Case, except for proper names, abbreviations, and official study titles.
- In owner-facing copy, prefer “owner”; do not use “pet mom.”
- Prefer “senior” to “old” for animals.
- Keep prose direct, humane, cautious, and free of generic AI optimism or sentimental filler.
- Do not make medical promises. Final eligibility and treatment decisions belong to the study/veterinary team.
- SEO structure is frozen except for explicit requests, database-driven updates, or verified bugs.
- Do not touch the live site or deployment configuration casually. Verify the branch and build path first.
- Osteoarthritis work remains isolated from the production cancer matcher unless explicitly approved.

## Working behavior

- If instructions conflict with current repository evidence, stop and explain the conflict.
- If a primary source is unavailable or ambiguous, preserve the existing record unless there is sufficient evidence for a conservative correction.
- Do not perform broad cleanup during a targeted reconciliation.
- Never overwrite or discard unrelated changes.
- Add durable new operational lessons to `PROJECT_OPERATIONS.md`.
- Keep task-specific research notes outside the canonical production catalog.
