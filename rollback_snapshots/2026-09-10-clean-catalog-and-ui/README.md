# Full rollback checkpoint — 2026-09-10

This checkpoint intentionally captures the ENTIRE repository state, including the Streamlit UI/shell, finder logic, catalog, patches, archive/tomb machinery, SEO/site code, scripts and workflows.

## Immutable restore point

- Commit: `f754dab142dfee64a0bff292d0ee98e14891151e`
- Tree: `b8b2c264ebf9704cc11135f4be454f9889b9a80b`
- Branch at capture: `main`
- Captured: 2026-09-10

Because the Git tree is immutable, this is a complete snapshot of every tracked file at that moment; it is not a partial list of selected files.

## Included state

- Full Streamlit shell/UI and all pages, including `pages/1_Clinical_Trial_Finder.py`
- Finder matching/filter/count logic
- Trial catalog base, updates and all catalog patches
- Current dedupe/integrity cleanup state
- Closed/inactive trial archive (“tomb”) tooling and workflows present at the captured commit
- SEO/source code and generated tracked site assets present in the repository
- Validation/audit scripts and GitHub Actions workflows
- Configuration and all other tracked repository files

## Restore

To restore absolutely everything to this checkpoint, restore the repository tree from commit:

`f754dab142dfee64a0bff292d0ee98e14891151e`

For selective rollback, restore the required path(s) from the same commit. The commit itself is the authoritative snapshot; this README is only the human-readable marker.

## Why this checkpoint exists

Known-good state after the September 10 catalog integrity/deduplication work and creation of the inactive/closed-study archive machinery. Preserve both data and presentation together so later catalog or UI changes can be rolled back without reconstructing the shell separately.
