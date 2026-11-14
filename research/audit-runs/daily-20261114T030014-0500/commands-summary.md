# Command and validation summary

- `pwd`, `python --version`, `git --version` — PASS before audit execution.
- `python scripts/audit_execution_gate.py init research/audit-runs/daily-20261114T030014-0500 --scheduled` — PASS, scheduled 03:00–06:00 America/New_York window.
- Current traversal — 162 frozen sources processed; 139 master routes read and 23 exact restrictions preserved; 128 fallback route decisions, including two newly recorded official fallbacks.
- Country/language discovery — 96 real searches across 12 regions: current, deepened weak-output, and fresh seven-day signals.
- Deadline review — 321/321 canonical records compared; 254 unique primary routes; 41 current date-evidence routes not verified today and retained as NOT VERIFIED.
- `python scripts/audit_execution_gate.py check ...` — PASS accounting; clinical reconciliation INCOMPLETE.
- Strict receipt — expected INCOMPLETE, 157 current-evidence gaps. Gap-review validator — PASS.
- Catalog sanitation, schema, semantic dedupe, source inventory, evidence-key redaction/check, repository hygiene, matcher build, JS/Python selection and parity — PASS.
- `node scripts/test_matcher_catalog_loading.js` — PASS; USA 96, Japan 14; delayed/early/failure cases did not produce a false zero.
- `node scripts/test_matcher_logic.js` — PASS, 154 matcher records.
- `python scripts/validate_production_sync.py` — PASS, 154 records / 150 treatment / 4 other treatment access.
- Static build — PASS.

Detailed outputs and SHA-256 values are stored in `validation/` and `validation-results.json`.
