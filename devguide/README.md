# Developer guide

This directory contains operational guidance for maintaining and releasing PyUnitWizard.

## Documents

- `smonitor.md`: diagnostics and instrumentation rules.
- `roadmap.md`: staged path from pre-`1.0.0` lines to stable `1.0.0`.
- `compatibility_matrix.md`: minimum supported sibling-library versions during RC.
- `release_0.19.x_rc_checklist.md`: operational checklist for RC stability window management.
- `release_1.0.0_checklist.md`: release gates and go/no-go checklist.
- `molsyssuite_collective_alignment.md`: PyUnitWizard alignment map against `../molsyssuite/devguide/collective_v1_checklist.md`.
- `collective_evidence_pack.md`: handoff-ready evidence pack for cross-repo RC closure.
- `performance_baseline_0.19.x.json`: current RC performance baseline snapshot.

## Current baseline

- Active release-candidate line: `0.19.x` (RC window before `1.0.0`).
- Current RC tag checkpoint: `0.19.2`.
- Latest stabilized tags before RC: `0.18.2`, `0.18.3`, `0.18.4`.
- Stable target: `1.0.0`.
- Supported Python versions: `3.11`, `3.12`, and `3.13` (daily operation in `3.13`).
- Current local test snapshot (2026-03-03): `305 passed` (`pytest -q tests --ignore=tests/test_import.py`).
- Shared collective E2E module established: `tests/e2e/test_collective_error_path.py`.
- Supported runtime backends:
  `pint` (hard), `openmm.unit` (soft), `unyt` (soft), `astropy.units` (soft),
  `physipy` (soft), `quantities` (soft), plus `string` form.

## RC checkpoint summary (2026-03-03)

Completed in `0.19.x`:
- Public-contract hardening and cross-library smoke coverage are in place.
- Shared collective E2E scenario is implemented in all four library repos.
- Collective test execution policy is now explicit: tests run in library repos
  with CI, while `molsyssuite` remains coordination-only.
- Runtime integration support is implemented and tested for
  `pint`, `openmm.unit`, `unyt`, `astropy.units`, `physipy`, and `quantities`.

Pending before `1.0.0` go/no-go:
- sustain CI matrix continuity (`ubuntu`/`macos`, Python `3.11`/`3.12`/`3.13`);
- run and track `release_gates` on candidate commits during the RC window;
- close remaining collective finality items (traceability tag alignment and
  end-to-end evidence closure across the four libraries);
- complete release-owner go/no-go signoff with no open blockers/high-severity incidents.

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
