# Daily update runbook

## Core rule
Daily automation may update verified data and content, but must not rewrite `app.py`, matcher UI code, navigation code, or presentation code. UI/code changes are separate work and require their own smoke test.

## Order of operations
1. Health-check the public app first.
2. Confirm the clinical trial matcher loads.
3. Confirm `USA` is the default country.
4. Run a broad browse check: `USA` + `Cancer — any type` + `Find potential trials`; require at least one real result.
5. Check navigation to Oncology Centers, Advanced Treatments, and Expanded Access.
6. Check mobile rendering and browser console/page errors.
7. Only if the live health-check passes, research new trials, hospital studies, expanded-access programs, and unusual treatment options.
8. Verify every candidate against an official/current source before adding it.
9. Add changes as data/content patches on a separate update branch. Do not mix data, content, and UI/code changes in one commit.
10. Validate structure before deploy: valid JSON, unique IDs, current recruitment/access status, country/species/cancer tags, contacts, funding only when explicitly verified.
11. Run local/CI smoke on the candidate: compile, desktop, mobile, matcher browse results, navigation, Advanced Treatments geography filter.
12. Merge/deploy only after candidate smoke passes.
13. Run public smoke on `https://c-trials.streamlit.app/` after deploy.
14. If public smoke fails, rollback only the last update commit. Do not stack unrelated fixes on top of a failed deployment.

## Change classes
- **Data update:** trials, centers, addresses, status, contacts, eligibility metadata. May be frequent/daily after verification.
- **Content update:** cancer descriptions, explanatory text, links. Keep separate from data when practical.
- **Code/UI update:** matcher logic, `app.py`, navigation, CSS. Separate change with full smoke; never part of the daily data bot.

## Verification standard
A record is patient-facing only when current recruitment/access is verified. `No matches` is acceptable; uncertain or stale records must not be promoted merely to increase result count.

## Daily research scan
After health-check, scan for:
- newly recruiting veterinary oncology clinical trials;
- hospital/university oncology studies not present in major registries;
- expanded/managed-access programs;
- unusual currently accessible treatments with veterinary evidence (for example ECT combinations, immunotherapy, HIFU, targeted local treatments);
- status changes, closures, new sites, contacts, eligibility changes, and verified funding changes for existing records.

Prefer official university/hospital/sponsor/registry sources. Research findings do not go live until verified and smoke-tested.
