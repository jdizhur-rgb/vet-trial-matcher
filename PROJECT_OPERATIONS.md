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
- The static site's canonical header navigation lives in `seo/site_shell.py`. Keep desktop dropdowns mutually exclusive and close them on pointer exit, outside click, link activation, focus exit and Escape; preserve native click-to-expand behavior at mobile widths.

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
- Optimization begins only after each master page is opened. An unchanged fingerprint and unchanged extracted protocol roster may skip rereading known protocol pages, except for a forced full protocol-level reread at least once every four weeks. Changed, stale, due, and unresolved sources always require deep review.
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
- Every public static-page `<h1>` receives the shared `page-title` component in `seo/site_shell.py`; route-specific H1 typography must not be added. The shared “Find oncology care” navigation group must retain links to both the nearby-care matcher and the complete center directory.
- `scripts/build_static_site.py` assembles the artifact and then runs cleanup, sentence-case enforcement, production synchronization, link/asset checks and matcher regressions.

Clinic pages and the oncology-care directory are text-only. Clinic-photo download/fallback code was retired; do not restore external clinic image fields or hotlinking helpers. Production validation rejects external images on center pages and retired preview routes, tracking markers, old navigation labels and obsolete claims.

IndexNow notifications run only after a successful GitHub Pages deployment. The notifier derives eligible URLs from the generated production sitemap, rejects non-canonical, noindex and redirect pages, and compares generated-page hashes with the last successful submission so only changed `https://vettrialfinder.com` pages are sent. IndexNow availability must never block deployment.

## 19. Technical SEO regression safeguards

Center directory addresses and ZIP/state filters must use the center's own location facts, never the first location of a multi-site study. Branch aliases should link directly to their destination; canonical URLs omit fragments. A participating site's stated country takes precedence over the study lead country.

Breadcrumb structured-data destinations must resolve to existing production pages. Sitemap `lastmod` is omitted until reliable per-page content modification dates are available; neither a fixed date nor a fresh build timestamp represents a content update. The production synchronization validator checks breadcrumb destinations, fragment-free canonicals, article schema and the multi-site center-address regression.

When an official clinic relocation conflicts with the ACVIM snapshot, exclude the stale profile ID and retain the replacement in the existing supplemental source so rebuilds cannot restore the old address. Update distance coordinates together with the address; document ZIP-centroid precision when used. Ally Veterinary moved from Waltham to 16 Mill St., Lincoln, MA 01773, verified on its official site September 25, 2026.
