# Stable rollback snapshot — 2026-09-09

Known-good production state after the systematic center/address repair.

Stable commit: `16ed00267698999c370f47a4914ce28b88e74564`
Workflow: Build and deploy SEO site #112
Workflow run ID: `34375856452`
Status at verification: build SUCCESS, deploy SUCCESS, live verify SUCCESS.

This snapshot marker is intentionally stored in the repository so the exact known-good state can be restored without copying generated files or duplicating the whole repository.

## Rollback source
Restore files from commit:
`16ed00267698999c370f47a4914ce28b88e74564`

## What this stable point includes
- central institution / hospital / clinic address directory
- shared name normalization and aliases
- catalog-wide address preflight
- country-aware address validation
- international center pages, not USA-only
- physical participating-site addresses where known
- network/partner-hospital coverage handled without inventing a physical address
- corrected center-page heading/photo layout
- CI failure for newly unmapped physical centers
- successful live-page verification against rebuilt output

Do not delete this folder when cleaning generated SEO files. It is the rollback reference for the stable 2026-09-09 production version.
