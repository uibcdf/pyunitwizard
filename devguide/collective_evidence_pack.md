# Collective Evidence Pack

This document is the handoff artifact for cross-repo validation with:
- `../smonitor`
- `../depdigest`
- `../argdigest`

It is designed to be mirrored/adapted in sibling repositories so collective
closure can be decided from comparable evidence without ambiguity.

## What this is

`collective_evidence_pack.md` is the canonical checkpoint record for:
- current PyUnitWizard local evidence,
- required cross-library E2E evidence,
- pending closures that cannot be completed from this repository alone.

This file is intentionally self-contained so a maintainer can understand:
- what has already been demonstrated,
- what remains pending,
- how to report status in a compatible format across all sibling repos.

## How to use this file

Use this file in three moments:

1. Before tagging a new RC checkpoint (`0.19.x`):
- refresh local evidence and references (tests, docs, performance baseline).

2. During cross-repo synchronization:
- copy the shared status template into sibling repositories,
- compare local statuses and identify collective blockers.

3. At go/no-go discussions:
- use the decision placeholders at the bottom to capture owner, date,
  evidence links, and blocker resolution plan.

## How to update this file

When updating, follow this protocol:

1. Update the checkpoint metadata (`Date`, `tag baseline`, `head reference`).
2. Refresh local quality numbers from current runs.
3. Keep only evidence that is reproducible and present in-repo.
4. Never mark collective closure from local-only evidence.
5. If scope changes, update pending closures and decision placeholders.

Date: `2026-03-03`
PyUnitWizard tag baseline: `0.19.1`
PyUnitWizard head reference for this pack: `fd62f3e`

## 1. Local quality baseline (PyUnitWizard)

- Full suite: `pytest -q` -> `263 passed` (Python `3.13`).
- Performance baseline snapshot:
  `devguide/performance_baseline_0.19.x.json`
  (generated via `devtools/benchmarks/conversion_baseline.py`).

## 2. Contract evidence index (PyUnitWizard)

- Unified config precedence (`runtime > env > file`):
  `tests/test_configure.py`
- DepDigest dependency policy contract:
  `tests/test_depdigest_contract.py`
- SMonitor catalog code/hint contract:
  `tests/test_smonitor_catalog_contract.py`
- SMonitor profile contract (consumer side):
  `tests/test_smonitor_profiles_contract.py`
- Kernel isolation and restoration:
  `tests/test_context.py`
- Fundamental dimensions lock:
  `tests/test_kernel_contract.py`
- Backend exception translation to catalog-backed hierarchy:
  `tests/test_exception_translation_contract.py`
- Cross-library integration smoke:
  `tests/integration/test_ecosystem_smoke.py`
  `tests/integration/test_local_sibling_repos.py`
- Shared collective error-path E2E module:
  `tests/e2e/test_collective_error_path.py`

## 3. Collective E2E target scenario (must be validated across repos)

Goal:
- an error triggered at PyUnitWizard unit/conversion layer is surfaced as:
  1. ArgDigest contract error with caller context,
  2. SMonitor diagnostic event/log with stable code,
  3. DepDigest remediation hint (when dependency-related),
  4. coherent profile behavior (`user` vs `dev`/`qa`/`agent`).

Minimum acceptance evidence:
- reproducible command/workflow reference,
- captured output/events (or artifact) with stable code + hint,
- per-library references to test/commit proving the path.

Execution policy:
- shared/collective tests must run inside library repos with CI (`pyunitwizard`,
  `argdigest`, `depdigest`, `smonitor`).
- `molsyssuite` is coordination-only for this workflow (runbook, checklist,
  captured evidence), not a test host.
- when useful for resilience, duplicate collective E2E tests across libraries
  instead of centralizing them in `molsyssuite`.

## 4. Shared status template (copy to sibling repos)

Use this exact block when reporting progress:

```md
Status note (YYYY-MM-DD):
- smonitor: <done locally|in progress|blocked|pending> (<reference>)
- depdigest: <done locally|in progress|blocked|pending> (<reference>)
- argdigest: <done locally|in progress|blocked|pending> (<reference>)
- pyunitwizard: <done locally|in progress|blocked|pending> (<reference>)
- collective validation: <pending|in progress|done> (<evidence>)
```

## 5. Pending collective closures (from PyUnitWizard perspective)

- SMonitor traceability tag alignment by failure category in cross-repo E2E.
- CI matrix continuity evidence (ubuntu/macos for supported Python versions).
- `release_gates` candidate runs tracked during RC window.
- Open-issues sweep proving no unresolved blocker/high severity at RC close.

## 6. Decision log placeholders

Use these entries to avoid decision drift:

- `go/no-go owner`:
- `date`:
- `collective evidence links`:
- `open blockers`:
- `resolution plan`:

## 7. Sibling reference anchors (2026-03-03)

- `smonitor`: `cabb2d0` (adds `devguide/collective_evidence_pack.md`)
- `depdigest`: `d0f93b4` (adds `devguide/collective_evidence_pack.md`)
- `argdigest`: `a207058` (adds `devguide/collective_evidence_pack.md`)
