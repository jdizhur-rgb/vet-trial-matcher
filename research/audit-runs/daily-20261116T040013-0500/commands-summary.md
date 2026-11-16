# Command and validation summary

Run: `daily-20261116T040013-0500`

- Environment: `pwd`, `python --version`, `git --version` — PASS.
- Scheduled gate init and final gate check — PASS for execution accounting; clinical reconciliation and discovery remain INCOMPLETE.
- Strict receipt — INCOMPLETE, 142 current-evidence gaps, schema errors 0. Gap review — PASS.
- Sources: 162 decisions, 289 master/fallback route decisions, 241 actual requests, 48 exact restrictions not retried.
- Discovery: 96 queries across 12 regions and 32 country/language slots; 12 lead decisions.
- Daily deadline ledger: 321/321 records; 21 structured cutoffs, three historical past cutoffs already nonmatchable, zero active records beyond cutoff.
- Fresh full protocol review gate — INCOMPLETE, 0/154; current primary route readable 121/154, exact restrictions 33/154; historical independent selection review 143/154.
- Matcher loading, matcher logic, catalog/source validators, sanitation, selection/duplicates, static build, production sync, links, hygiene and evidence-key scan — PASS. Ancillary Streamlit check unavailable; core preflight PASS_WITH_INCONCLUSIVE.
- Git Data API publication to main — PASS; data commit `0262feccf2c7fdf4fc4852ecb82b125d2585b75c`.
- GitHub Actions deploy 43840878883 — PASS.
- Production HTML, matcher JS and catalog exact byte readback — PASS.
- Rendered searches — USA 96/96 PASS; Japan 14/14 PASS.
