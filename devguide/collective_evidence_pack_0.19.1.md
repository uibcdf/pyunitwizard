# Collective Evidence Pack (`0.19.1`)

This pack is the handoff artifact for cross-repo validation with:
- `../smonitor`
- `../depdigest`
- `../argdigest`

It is designed to be mirrored/adapted in sibling repositories so the collective
closure can be decided from comparable evidence.

Date: `2026-03-03`
PyUnitWizard tag baseline: `0.19.1`
PyUnitWizard head reference for this pack: `df57d25`

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
