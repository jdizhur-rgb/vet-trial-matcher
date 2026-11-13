# Command and validation summary

- `pwd`, `python --version`, `git --version` — PASS before audit execution.
- `python scripts/audit_execution_gate.py init research/audit-runs/daily-20261113T030644-0500` — PASS, manual 180-minute execution window.
- Source traversal scripts in this run directory — 161 frozen sources processed; one newly discovered source and five linked protocol pages added to the same run.
- Country/language discovery batches — 96 real searches across 12 regions.
- `python scripts/audit_execution_gate.py check ... --receipt ... --queue-out data/audit_execution_queue.json` — PASS; clinical reconciliation INCOMPLETE.
- `python scripts/validate_audit_receipt.py ...` — expected INCOMPLETE, 161 current-evidence gaps.
- `python scripts/validate_audit_gap_review.py ... --receipt ...` — PASS; all 161 gaps classified as external blockers.
- Catalog sanitation, schema, semantic dedupe, source inventory, evidence keys, repository hygiene, matcher build, JS/Python selection and parity — PASS.
- `node scripts/test_matcher_catalog_loading.js` — PASS; USA 96, Japan 14, delayed/early/failure cases produced no false zero.
- `node scripts/test_matcher_logic.js` — PASS, 154 matcher records.
- `python scripts/validate_production_sync.py` — PASS, 154 records / 150 treatment / 4 other treatment access.
- Static build — PASS.
- GitHub Actions on published data commit — full catalog integrity, active links, catalog validation, evidence keys, semantic dedupe and deploy all PASS.
- Production readback — HTML, matcher JavaScript and trials catalog hashes match the local build; live USA and Japan UI searches PASS.

Detailed outputs and SHA-256 values are stored in `validation/`, `validation-results.json`, `production-readback.json`, `git-readback.json`, and the source/discovery evidence indexes.
