# UI consolidation plan — 2026-09-10

Goal: keep the live Finder stable while moving presentation code into one dedicated UI module.

## Current problem
- `app.py` contains global CSS, navigation, Streamlit monkey-patches, result-card transformations, contact/link formatting, feedback UI, and Copy/PDF behavior.
- `pages/1_Clinical_Trial_Finder.py` also owns result-card rendering and local CSS.
- Because presentation is split across both files, UI changes can bypass or overwrite each other.

## Target structure
- `ui.py`: one source of truth for visual shell and reusable result presentation helpers.
- `app.py`: page config, navigation wiring, and one call into the UI shell.
- `pages/1_Clinical_Trial_Finder.py`: matching/business logic and calls to reusable UI helpers; no duplicated styling rules.

## Permanent components to centralize
1. Global CSS and responsive layout.
2. Finder title/subtitle and top navigation.
3. Result heading formatting.
4. Study-information expander behavior.
5. Contact/site/link presentation.
6. Funding renderer:
   - Fully funded -> green success block.
   - Partially funded -> yellow warning block.
   - Unknown/unfunded/other -> neutral text.
7. Copy/PDF controls.
8. Eligibility feedback block.

## Safety rules for the refactor
- No changes to trial matching logic or catalog data.
- No text-replacement GitHub Actions touching live Python files.
- Work on a non-live branch first.
- Run `python -m py_compile app.py ui.py pages/1_Clinical_Trial_Finder.py pages/2_Additional_Oncology_Options.py` before main is updated.
- Compare rendered-facing strings and navigation behavior before promoting.
- Main is updated only after checks pass.
