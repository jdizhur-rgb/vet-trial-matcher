# Clinical Trial Matcher — Product Contract

This document defines the patient-facing matcher behavior. Changes to this contract require matching engine and Streamlit regression tests before deployment.

## Geography

- Every catalog country remains searchable and is treated as equally important.
- `USA` is the default selection only; it has no ranking or eligibility advantage.
- The top-level choices are `USA`, `Canada`, `Europe`, `Other countries`, and `All countries`.
- `Europe` opens a country submenu whose default is `All Europe`.
- `Other countries` opens a submenu populated from the catalog.
- ZIP is optional, appears only for USA, sorts by approximate distance, and never excludes a study.

## Questions

- Cancer type has no default and searching is disabled until it is selected.
- `I don't know` is available wherever uncertainty is reasonable.
- The form stays short. Extra questions appear only when a currently relevant protocol uses the answer in matching.
- Specialist-only requirements are disclosed under `Needs confirmation`; they are not presented as owner-confirmed facts.

## Results

- Results are plausible opportunities, never declarations of eligibility.
- Cards prioritize location, intervention, funding/cost coverage, and approximate distance when available.
- Recruitment, final eligibility, costs, travel, and treatment details must be confirmed with the study team.
- A missing or invalid ZIP does not remove results.

## Architecture and release safety

- The Streamlit page owns questions and rendering.
- `matcher_engine.py` owns eligibility screening and ranking.
- `trial_catalog.py` owns catalog loading, cancer taxonomy, and modality inference.
- `location_sort.py` owns optional ZIP distance ordering.
- No matcher change goes directly to production. It is verified on the test branch with unit tests, the full species/cancer matrix, Streamlit smoke tests, and named control cases before merge.
