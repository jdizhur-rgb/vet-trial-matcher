# Publication of latest unpublished clinic packages

Owner authorization: publish all latest unpublished clinic packages. Baseline main: `39f0f3b30450b65b7af148d991dfc9bab428e068`.

Scope: E01 (25 identities), E02 (25), E03 (21), E04 (25), remaining E05/E06 plus four Australian clinics (31): **127 source identities**. This includes network sources and overlapping aliases, not 127 new hospitals. Earlier A/B/C/D/P00 publications are preserved. Original proposals are retained unchanged; `integration.json` records field integration, exceptions and open questions. Proposal-only statuses describe the original historical artifacts, not current publication state.

Conservative reconciliation: later branch-specific TMC evidence overrides E01 network-level modality claims; retain Medical oncology, correct Brittanie Partridge and retain group/branch allocation questions. Spring remains separate. Exclude the verified stale Partner/Annapolis public representation while preserving raw history and source inventory. Caldwell's general Surgery is not surgical oncology. Unknown coordinates are explicitly null and excluded from distance ranking; physical clinics are not relabelled mobile. Empty confirmed service lists preserve clinics as service-unconfirmed. SAGE Redwood City's official branch URL must survive the final builder override. Owner-facing availability notes are English translations of reviewed access facts.

Results: 511 preserved unique source inventory identities; 439 public clinical representations; zero duplicate normalized physical addresses. No unrelated inventory rows changed. Original source attempt timestamps are preserved or advanced only from documented receipts; integration is not a fresh visit.

Validation passed: full static production build (including 439 center cards / 52 US regions, production synchronization, matcher and shell checks), A01/A02/B01/B02/C01 care regressions, E package branch/mobile/unknown-state regression, delayed-catalog-loading regression, evidence key check, and diff whitespace check. New explicit unknown states required narrowly scoped builder/validator support; no interface redesign or trial data changes.

Outstanding source questions remain in original package reviews and source inventory. They include clinician branch assignments, local versus referred radiation, mobile/locum schedules and local modality delivery. They do not become confirmed positive service flags merely because a package is published. External website access limitations are preserved in original attempt receipts.

Publication and exact deployed-byte verification are recorded separately after the push.
