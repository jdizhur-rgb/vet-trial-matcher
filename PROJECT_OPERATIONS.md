# Vet Cancer Treatment Finder — Project Operations / Single Source of Truth

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

Exclude observational, diagnostic/biomarker-only, sample collection/biobank, microbiome, research-only PK, and supportive-care studies without an anticancer treatment objective.

Potential public categories:
- Clinical Trial
- Compassionate / Expanded Access
- Novel Treatment / Special Program

Pipeline/watchlist records that do not yet have a usable owner-facing treatment route must remain non-matchable.

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

## 11a. Private usage analytics

- Privacy-friendly analytics use Umami Cloud website ID `20597fc4-68b1-4552-94c8-0771d1d74673`.
- The dashboard is private to the owner's Umami account; no public counter or shared analytics URL is enabled.
- Generated static pages receive the tracker through `seo/site_shell.py`.
- The Streamlit finder records one `/matcher` pageview per Streamlit session and a `matcher-search` event when the search button is used.
- Matcher analytics must never send diagnosis, location, treatment choices, or other form values. Streamlit widget reruns must not be counted as additional visits.

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
