# Rollback snapshot — 2026-09-09 current UI

Stable checkpoint for the current approved visual state.

## Cancer pages
- Current cancer-page layout: disease information first, then current opportunities/trials.
- Source: `seo/cancer_page_enhancements.py`
- Owner-facing disease copy: `seo/cancer_owner_content.py`

## Center / hospital pages
- Current approved center-page rendering, profiles, addresses, study cards and layout.
- Source/rendering layer: `seo/generate_seo_strict.py`

## Finder / database UI
- Current Streamlit application appearance: `app.py`
- Current Clinical Trial Finder page appearance and behavior: `pages/1_Clinical_Trial_Finder.py`

## Exact source versions saved
- `cancer_page_enhancements.py` blob: `e7b138a82e8eefafa4c0f150c56dc4ae4b9a1dd9`
- `cancer_owner_content.py` blob: `f9335b077fa23d0feb9d54e1f69d60f4247d7cde`
- `generate_seo_strict.py` blob: `3c0f4dc1a67ec35d4511a4a7373395ef8fce013c`
- `app.py` blob: `7d8ad731c223a1aef30c46edcf51f414efc311b6`
- `pages/1_Clinical_Trial_Finder.py` blob: `eb03b09722e2d57ba371a4642b35638c29f5256e`

This snapshot is intended as the rollback reference before further visual changes. Restore these exact blob versions if a later redesign needs to be undone.
