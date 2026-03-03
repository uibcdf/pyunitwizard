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
- Current RC tag checkpoint: `0.19.1`.
- Latest stabilized tags before RC: `0.18.2`, `0.18.3`, `0.18.4`.
- Stable target: `1.0.0`.
- Supported Python versions: `3.11`, `3.12`, and `3.13` (daily operation in `3.13`).
- Current local test snapshot (2026-03-03): `263 passed` (full `pytest` suite).
- Shared collective E2E module established: `tests/e2e/test_collective_error_path.py`.

## Coordination scope

PyUnitWizard must stay aligned with:

- `argdigest`: argument normalization and API contract integration.
- `depdigest`: optional dependency governance and runtime loading.
- `smonitor`: diagnostics catalog, severity semantics, and traceability.
