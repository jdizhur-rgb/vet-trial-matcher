# Daily execution evidence contract — 2026-11-01

This is the executable accounting contract for the daily trial audit, not a
replacement for clinical judgment, the strict receipt validator or access rules.
`scripts/audit_execution_gate.py` makes no network requests and does not change
canonical clinical data or verification dates. Historical run scripts/receipts
remain immutable. Do not clone a historical `finalize.py` into a new run.

## Start and finish

Before reading external sources, from fresh main run:

```sh
python scripts/audit_execution_gate.py init research/audit-runs/<run_id> --scheduled
```

This freezes source/catalog/public IDs, input hashes and unresolved trial issues
in `execution-baseline.json`, plus a deliberately empty `execution-review.json`.
When no durable queue exists, seed from the actual previous daily full-review
ledger, the protocol-selection progress receipt, missing independent cases and
canonical verification ages (28 days or unknown). No visits, completion or new
clinical dates are claimed by initialization. Preserve independently resolved
issues in the handoff so an obsolete historical pending list cannot reopen them;
an actually due/new issue still requires a new review.
Omit `--scheduled` for an off-schedule run (180 minutes from actual start).
Initialization freezes the real execution deadline; finalization cannot replace
it with an arbitrary earlier cutoff.

Complete the fields below from actual evidence, then run before final accounting:

```sh
python scripts/audit_execution_gate.py check research/audit-runs/<run_id> --receipt research/audit-runs/<run_id>/receipt-final.json --queue-out data/audit_execution_queue.json
```

The gate writes `execution-validation.json`. Invalid accounting returns nonzero
and cannot replace the durable queue. Save the invalid/current checkpoint and
all unresolved work in the run directory; fix permitted missing work now or
report the precise failure. Valid accounting can still report clinically
INCOMPLETE. Independently verified corrections may publish with an honest
INCOMPLETE receipt; never forge a PASS to authorize publication. Run the existing
strict receipt and gap-review validators as well. This new contract is required
for future actual daily runs; do not retrofit or overwrite earlier snapshots.

## Current source decisions

`source_reviews` must cover every frozen `source_id` exactly once. Each row has:

| Field | Meaning |
|---|---|
| `source_id`, `reviewed_at` | Actual decision identity and timezone-aware time within this run |
| `finding`, `evidence_refs` | Individual substantive finding and nonempty local saved evidence paths |
| `remaining_available_steps` | Explicit list, including an empty list only if none remain |
| `completion_basis` | Why available reconciliation is complete, distinct from sufficiency |
| `current_official_content`, `roster_complete` | True only after reviewing the actual current official roster |
| `protocols`, `catalog_comparison` | Current enumerated identities and individual catalog dispositions; an empty roster must be explicitly evidenced |
| `roster_evidence_refs` | Current retrieved roster artifacts from actual receipt attempts; restriction reviews are not visits |
| `change_reviews` | One `{current_evidence, finding, catalog_impact}` for every changed compared page |

Sufficiency is derived from these CURRENT fields, never yesterday's sufficient
flag. A previous partial source may become sufficient. A previous complete
source may become partial. One equal page cannot mask an unexamined changed
page. The receipt's per-source `content_sufficient` and total must agree with
the derivation. Paths refer to nonempty saved files relative to the repo (or
resolved local paths); bare URLs/prose are not saved evidence.

Discovery/news/pipeline pages need actual link/lead reconciliation, not an
invented clinical roster. Their available processing can finish while clinical
roster sufficiency remains false. For restrictions record the exact prior
artifact and scope; do not invent a fresh visit, HTTP403 or institution-wide ban.

Newly verified sources may be declared in `added_source_ids`. Each must exist in
the actual current inventory and receive the same complete current decision and
receipt accounting. Every frozen source remains mandatory; undeclared additions,
missing original IDs and rewriting the baseline are not permitted.

## Durable trial issues

Each baseline issue needs one `issue_updates` row, preserving `issue_id`,
`trial_id`, `kind`. Newly found issues must also be added. Kinds are
`full_protocol` and `independent_selection`; source questions and dates retain
their separate existing ledgers. Each update records actual `reviewed_at`,
`finding`, `evidence_refs` and one state:

| State | Required evidence |
|---|---|
| `RESOLVED` | Full protocol `facts_checked`: identity, recruitment_sites, eligibility, funding, contacts; independent review `cases_checked`: positive, negative, unknown |
| `OPEN_AVAILABLE` | Concrete remaining question and next permitted action; do it within the run |
| `BLOCKED` | Question, next action and `restriction_or_unpublished_evidence_refs` establishing the exact gap |
| `DEFERRED` | Question, next action, explicit future timezone-aware `recheck_after` and `deferral_basis`; never defer a crossed deadline or new primary signal |
| `OWNER_DECISION` | Exact unresolved medical/editorial/status decision, with existing evidence and next action; no invented consent |

Do not copy the queue and change its date. An unchanged blocker may retain its
original primary evidence, but today's decision must identify why no permitted
step is due/available. Update canonical verified/funding dates only after a real
completed full review of those facts, and update independent cases separately.
Source visits, text scans, generated tests and queue accounting do not do this.
Persist unresolved AND resolved issue identities; totals derive from actual rows.

## Discovery and deadlines

`discovery_queries`: `{region, pass, country, language, query, evidence_refs}`.
Use the 12 region keys and `current_undated` / `recent_seven_days` in the script.
Separate country/language searches instead of concatenating many languages into
one query. Plan the actual country frontier, inspect returned official links,
expand regions with weak results and record missing countries/languages. Two
queries per region is not a completeness rule or a permitted stopping quota.

`discovered_urls` contains all returned candidate/index URLs selected for
examination; retain the complete search responses so exclusions are auditable.
Every URL gets exactly one `leads` row with `url`, `disposition`, `reason`,
`evidence_refs`. Treatment candidates identify `primary_url`; if unavailable,
PENDING_EVIDENCE/BLOCKED must state `missing_primary_reason`. Use:
ADDED / VERIFIED_EXISTING / DUPLICATE / CLOSED_CONFIRMED / NOT_TREATMENT /
PENDING_EVIDENCE / BLOCKED / SOURCE_INDEX_REVIEWED. Existing-source-only labels
are rejected. ADDED/VERIFIED_EXISTING/DUPLICATE require exact `canonical_ids`
and `identity_comparison` by protocol/cohort/intervention/disease/sites, not
hostname. SOURCE_INDEX_REVIEWED requires actual `protocol_links_examined`;
an index is not itself a duplicate study. Add secondary source signals only as
leads until protocol-level evidence resolves them. Preserve full multicenter
rosters. Unprocessed permitted lead work belongs in `unperformed_steps`.

`deadline_review_ref` points to the existing per-record daily deadline ledger;
its rows must cover every frozen canonical `record_id` exactly once. Continue
the full deadline semantics/extension/PDF/local-time rules in the main algorithm;
this gate checks accounting, not semantic correctness of date extraction.

## Why execution stopped

Record `ended_at` and `stop: {reason, detail, evidence_refs}`. Allowed reasons:

- `completed_available_work`: no available source/issue/lead steps remain.
- `time_limit`: record `deadline`; actual end must reach the real planned limit.
- `runtime_failure`: save actual failure evidence; list the unperformed work.

The morning limit is 06:00 America/New_York; an off-schedule run has 180 minutes
from actual start. A declared arbitrary earlier deadline cannot shorten it.
Nothing requires idle waiting when only documented external gaps remain. A
failure/time boundary is honest INCOMPLETE, not clinical completion. Record
source sufficient/total, issue before/resolved/remaining and available work,
discovery candidate decisions and clinical completion separately. Gate PASS
does not prove exhaustive world coverage or medically correct adjudication.
