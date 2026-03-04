# Developer guide

This directory contains operational guidance for maintaining and releasing PyUnitWizard.

## Documents

- `smonitor.md`: diagnostics and instrumentation rules.
- `roadmap.md`: staged path from pre-`1.0.0` lines to stable `1.0.0`.
- `compatibility_matrix.md`: minimum supported sibling-library versions during RC.
- `release_0.19.x_rc_checklist.md`: historical RC checklist from the `0.19.x` phase (kept as evidence baseline).
- `release_1.0.0_checklist.md`: release gates and go/no-go checklist.
- `molsyssuite_collective_alignment.md`: PyUnitWizard alignment map against `../molsyssuite/devguide/collective_v1_checklist.md`.
- `collective_evidence_pack.md`: handoff-ready evidence pack for cross-repo RC closure.
- `performance_baseline_0.19.x.json`: current RC performance baseline snapshot.

## Current baseline

- Active release-candidate line (planned/final): `0.21.x`.
- `0.19.3` remains the historical checkpoint tag from the earlier pre-RC phase.
- Current head relative to tag: `0.19.3-15-g7f1b43d` (post-tag hardening in `main`).
- Latest stabilized tags before RC: `0.18.2`, `0.18.3`, `0.18.4`.
- Stable target: `1.0.0`.
- Supported Python versions: `3.11`, `3.12`, and `3.13` (daily operation in `3.13`).
- Current local test snapshot (2026-03-04): `356 passed` (`pytest -q tests --ignore=tests/test_import.py`).
- Shared collective E2E module established: `tests/e2e/test_collective_error_path.py`.
- Supported runtime backends:
  `pint` (hard), `openmm.unit` (soft), `unyt` (soft), `astropy.units` (soft),
  `physipy` (soft), `quantities` (soft), plus `string` form.

## 0.19.x checkpoint summary (historical baseline)

Completed in `0.19.x`:
- Public-contract hardening and cross-library smoke coverage are in place.
- Shared collective E2E scenario is implemented in all four library repos.
- Collective test execution policy is now explicit: tests run in library repos
  with CI, while `molsyssuite` remains coordination-only.
- Runtime integration support is implemented and tested for
  `pint`, `openmm.unit`, `unyt`, `astropy.units`, `physipy`, and `quantities`.
- Transparent integrations are now implemented and validated for:
  - NumPy (`setup_numpy` / `numpy_context`),
  - Pandas (`setup_pandas` / `pandas_context` + metadata-safe helpers),
  - Matplotlib (`setup_matplotlib` / `plotting_context`).
- Cross-backend frontend matrix coverage exists for mixed backend pairs across
  NumPy/Pandas/Matplotlib integration surfaces.

Pending before `1.0.0` go/no-go:
- sustain CI matrix continuity (`ubuntu`/`macos`, Python `3.11`/`3.12`/`3.13`);
- run and track `release_gates` on candidate commits during the RC window;
- close remaining collective finality items (traceability tag alignment and
  end-to-end evidence closure across the four libraries);
- complete release-owner go/no-go signoff with no open blockers/high-severity incidents.

Route update:
- `0.20.x` is reserved for interoperability expansion (NumPy/Matplotlib/Pandas).
- `0.21.x` is the RC consolidation window before `1.0.0`.

## Coordination scope

PyUnitWizard must stay aligned with:

- `argdigest`: argument normalization and API contract integration.
- `depdigest`: optional dependency governance and runtime loading.
- `smonitor`: diagnostics catalog, severity semantics, and traceability.

Collective testing policy:
- cross-library E2E tests belong to library repos with CI (including
  duplicated scenarios when needed for coverage and ownership clarity).
- `molsyssuite` is used for coordination artifacts/checklists, not as a test
  execution repository.
