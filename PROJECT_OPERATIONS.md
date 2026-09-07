# Vet Cancer Treatment Finder — Project Operations / Single Source of Truth

**READ THIS FILE FIRST before modifying the app, catalog, workflows, SEO, or deployment.**

This file is the persistent engineering/operations memory for the project. Update it whenever a bug teaches us something, a workflow changes, or a new permanent rule is established. Do not rely on chat memory for operational knowledge.

## 1. Production

- Repository: `jdizhur-rgb/vet-trial-matcher`
- Production branch: `main`
- Live Streamlit app: `https://vet-cancer-trial-finder.streamlit.app/`
- SEO site: `https://jdizhur-rgb.github.io/vet-trial-matcher/`
- Streamlit deployment was verified on 2026-09-06 to deploy `main`. Do not assume another branch without fresh deployment evidence.

## 2. Product scope

The matcher is treatment-focused. Include only opportunities that can provide an actual anticancer treatment option to a client-owned dog or cat.

Exclude observational, diagnostic/biomarker-only, sample collection/biobank, microbiome, research-only PK, and supportive-care studies without an anticancer treatment objective.

Potential public categories:
- Clinical Trial
- Compassionate / Expanded Access
- Novel Treatment / Special Program

Pipeline/watchlist records that do not yet have a usable owner-facing treatment route must remain non-matchable.

## 3. Effective catalog

Production matching is based on the effective catalog assembled from:
- `data/trials_base.json`
- `data/trial_updates.json`

Effective-catalog semantics are: start with base by ID; MERGE partial upserts onto the existing record; then apply delete markers with FINAL precedence. All consumers (matcher, SEO, dedupe, smoke tests) must use the same semantics. Never replace a base record with a partial upsert, and never apply deletes before upserts in a way that lets a deleted upsert be resurrected.

A staging/research/catalog-patch file is NOT production. A script or workflow existing is NOT proof that its data reached production.

For public treatment matching, records normally need:
- `study_type == "treatment"`
- `available_for_matching == true`
- species/cancer/country values compatible with matcher normalization
- current/usable treatment access

## 4. Mandatory promotion pipeline

Every catalog update must be treated as incomplete until this full loop succeeds:

1. Research and verify source/status/access.
2. Build candidate record(s).
3. Run semantic dedupe against the FULL effective catalog (`base + updates`), not only the staging patch.
4. Merge/update an existing record when the same real-world study/program already exists.
5. Promote the record to `trial_updates.json` (or the canonical production source used by the app).
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

## 7. Staging patches

Files such as `data/catalog_patch_*` are staging inputs. Their presence must never cause a country/filter option to imply that production contains matching records unless the effective catalog actually contains them.

When multiple staging patches are created in one audit, promotion must be atomic or followed by a reconciliation that reports:
- staged count
- promoted count
- merged-as-duplicate count
- intentionally withheld count + reason
- failed count + reason

## 8. China/Asia incident — 2026-09-07

China, Taiwan, and Korea were researched and staging patches were created. China had four dog treatment records in `data/catalog_patch_china_20260907.json`, but China showed 0 results in the live matcher because staging data had not actually reached `trial_updates.json` even though a merger script/workflow had been created.

Lesson: workflow creation/triggering is not final-state verification. Always fetch/search the resulting `trial_updates.json` / effective catalog after the workflow and then test matcher behavior.

Do NOT “fix” this class of bug by merely removing the country from the selector when genuine verified treatment records exist in staging. Reconcile and promote the records correctly.

Species may be stored as a string (`Dog`, `Dog/Cat`) or a list (`["Dog"]`, `["Dog","Cat"]`). All matching, filtering, SEO/import logic and smoke tests must normalize both forms.

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

## 11. Deployment lessons

- Production Streamlit branch is `main` unless fresh evidence proves otherwise.
- Back up before risky UI/deployment edits.
- Verify the live app, not just repository source, for deployment/UI bugs.
- Do not infer workflow success from workflow-file creation.

## 12. Working rule for future chats/agents

Before touching this project:
1. Read this file.
2. Inspect the current production files involved in the requested change.
3. Do not rediscover settled architecture from scratch.
4. Add durable new lessons/rules to this file when the project changes.

This file is the canonical engineering handoff. Chat summaries are secondary.
