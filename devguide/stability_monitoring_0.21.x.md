# Stability Monitoring Log (`0.21.x`)

This file tracks CI/release-gate stability evidence during the active RC line.

## Run ledger

### 2026-03-04 - Post-RC maintenance hardening (`0.21.1`)

- Scope:
  - fixed recursion defect in `forms/api_quantities.py` unit-conversion path,
  - aligned CI coverage environment to include `physipy` and `quantities`.
- Local validation:
  - `pytest --import-mode=importlib -q --cov=pyunitwizard --cov-config=.coveragerc --cov-report=term-missing`
  - Result: `391 passed`, total coverage `94%`.
- Classification:
  - Defect class: correctness bugfix (core conversion adapter path),
  - CI class: coverage observability alignment (non-breaking).

### 2026-03-04 - CI Full Matrix (manual dispatch)

- Workflow: `CI Full Matrix`
- Run URL: `https://github.com/uibcdf/pyunitwizard/actions/runs/22656333302`
- Result: `success`
- Coverage evidence:
  - Ubuntu: Python `3.11`, `3.12`, `3.13` passed.
  - macOS: Python `3.11`, `3.12`, `3.13` passed.
- Notes:
  - cache-reserve warnings observed in two Ubuntu jobs (non-blocking).

### 2026-03-04 - Release Gates (manual dispatch, first attempt)

- Workflow: `Release Gates`
- Run URL: `https://github.com/uibcdf/pyunitwizard/actions/runs/22656334939`
- Result: `failure`
- Job status summary:
  - `Packaging Smoke`: pass.
  - `Docs Build`: pass.
  - `Tests and Contracts` (`3.11`, `3.12`, `3.13`): fail during collection.
- Root cause:
  - `ModuleNotFoundError: No module named 'tests'` for modules importing
    `tests.helpers`.
  - Workflow lacked `PYTHONPATH` export before pytest execution.
- Classification:
  - Incident type: blocker (workflow/configuration).
  - Domain: release-gate execution environment.
- Resolution applied:
  - Added `export PYTHONPATH=$PYTHONPATH:$(pwd)` to both test steps in
    `.github/workflows/release_gates.yaml`.
- Follow-up:
  - re-run `Release Gates` on the fixing commit and record outcome.

### 2026-03-04 - Release Gates (manual dispatch, after fix)

- Workflow: `Release Gates`
- Run URL: `https://github.com/uibcdf/pyunitwizard/actions/runs/22656402041`
- Result: `success`
- Job status summary:
  - `Tests and Contracts` (`3.11`, `3.12`, `3.13`): pass.
  - `Packaging Smoke`: pass.
  - `Docs Build`: pass.
- Resolution status:
  - blocker from first attempt is closed by workflow fix and green rerun.

## Flaky-test tracking

- Current status: no flaky test identified in latest `CI Full Matrix` run.
- Current status: no flaky test identified in latest `CI Full Matrix` and
  `Release Gates` successful runs.
- Policy:
  - if a flaky test appears, add issue link and mitigation (quarantine/fix)
    in this file.
