# Developer guide

This directory contains operational guidance for maintaining and releasing PyUnitWizard.

## Documents

- `smonitor.md`: diagnostics and instrumentation rules.
- `roadmap.md`: staged path from pre-`1.0.0` lines to stable `1.0.0`.
- `interop_future_directions.md`: consolidated long-term interoperability ideas (conceptual, non-operational).
- `minimum_quantity_protocol_contract.md`: minimum backend-agnostic quantity contract for pre-`1.0.0` hardening.
- `frontend_transparent_mode_contract.md`: contract for transparent frontend integrations (`numpy`/`pandas`/`matplotlib`).
- `api_freeze_pre_1.0_decision.md`: explicit decision record for no planned breaking API changes before `1.0.0`.
- `serialization_contract_draft.md`: draft canonical serialization contract for post-`1.0.0` promotion.
- `compatibility_matrix.md`: minimum supported sibling-library versions during RC.
- `release_0.21.x_rc_checklist.md`: active RC checklist for consolidation before `1.0.0`.
- `release_0.21.x_notes_draft.md`: draft release notes for RC scope, risks, compatibility, and migration guidance.
- `docs_api_alignment_0.21.x.md`: evidence that user/API docs match shipped behavior in the active RC line.
- `stability_monitoring_0.21.x.md`: CI matrix and release-gates incident ledger for RC stability tracking.
- `ecosystem_validation_0.21.x.md`: integration smoke and sibling-repo validation evidence for RC.
- `rc_close_readiness_0.21.x.md`: closure evidence for RC go/no-go items before release-owner approval.
- `release_1.0.0_checklist.md`: release gates and go/no-go checklist.
- `molsyssuite_collective_alignment.md`: PyUnitWizard alignment map against `../molsyssuite/devguide/collective_v1_checklist.md`.
- `collective_evidence_pack.md`: handoff-ready evidence pack for cross-repo RC closure.

## Current baseline

- Active release-candidate line (planned/final): `0.21.x`.
- Latest maintenance tag in RC line: `0.21.1`.
- RC consolidation closure checkpoint tag: `0.21.0`.
- `0.19.3` remains the historical checkpoint tag from the earlier pre-RC phase.
- Current head relative to tag: run `git describe --tags --always` (post-tag hardening in `main`).
- Latest stabilized tags before RC: `0.18.2`, `0.18.3`, `0.18.4`.
- Stable target: `1.0.0`.
- Supported Python versions: `3.11`, `3.12`, and `3.13` (daily operation in `3.13`).
- Current local test snapshot (2026-03-04): `391 passed` (`pytest --import-mode=importlib -q --cov=pyunitwizard --cov-config=.coveragerc --cov-report=term-missing`).
- Current local coverage snapshot (2026-03-04): `94%` total.
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

Current RC-close status before `1.0.0` go/no-go:
- CI matrix continuity evidence is recorded (see `stability_monitoring_0.21.x.md`);
- release-gates evidence is recorded, including blocker/fix closure;
- ecosystem collective validation evidence is recorded
  (see `ecosystem_validation_0.21.x.md`);
- release-owner explicit RC-close approval is recorded.
- post-RC maintenance hardening in `0.21.1` includes:
  - recursion bugfix for `quantities` unit conversion path,
  - CI/Codecov alignment for optional backend coverage (`physipy`, `quantities`).

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

## 🥇 Performance Optimization (March 2026)

### Numpy Fast Path
The `get_value` API now implements a high-performance bypass for raw numpy arrays. If the input is already a numpy array and no conversion or standardization is requested, it is returned immediately. This reduces the overhead of the `arg_digest` decorator in tight loops.
