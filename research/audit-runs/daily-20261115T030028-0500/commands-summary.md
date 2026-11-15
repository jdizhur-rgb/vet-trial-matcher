# Command and validation summary

Run: `daily-20261115T030028-0500`

- Environment: `pwd`, `python --version`, `git --version` — PASS.
- Gate: `python scripts/audit_execution_gate.py init research/audit-runs/daily-20261115T030028-0500 --scheduled` — PASS.
- Final accounting: `python scripts/audit_execution_gate.py check ...` — execution PASS; clinical reconciliation INCOMPLETE; discovery INCOMPLETE.
- Gap review: `python scripts/validate_audit_gap_review.py ...` — PASS, 157 external gaps.
- Strict receipt: `python scripts/validate_audit_receipt.py ...` — INCOMPLETE, 157 coverage gaps, no schema errors.
- Matcher loading: `node scripts/test_matcher_catalog_loading.js` — PASS (USA 96, Japan 14; no false zero).
- Matcher logic: `node scripts/test_matcher_logic.js` — PASS.
- Production sync: `python scripts/validate_production_sync.py` — PASS.
- Other required schema, sanitation, duplicate/selection, link, source inventory, build and hygiene checks — PASS, except documented fresh protocol review incompleteness 8/154 and ancillary Streamlit unavailability.
- Publication: Git Data API update of `main` — PASS; GitHub Actions deploy 43695394035 — PASS.
- Production asset byte comparison and rendered USA/Japan searches — PASS.
