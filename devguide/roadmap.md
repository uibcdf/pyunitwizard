# Roadmap to 1.0.0

This roadmap defines the stabilization path from the `0.19.x` historical
checkpoint through `0.20.x`/`0.21.x` to a stable `1.0.0` release.

## Release stages

1. `0.17.x` - Hardening and correctness
2. `0.18.x` - API freeze and contract tests
3. `0.19.x` - Historical integration checkpoint (pre-RC)
4. `0.20.x` - Ecosystem interoperability expansion (NumPy/Matplotlib/Pandas path)
5. `0.21.x` - Release candidate consolidation window
6. `1.0.0` - Stable release

## 0.17.x - Hardening and correctness

### Objectives

- Fix known correctness defects in parser/configuration and form adapters.
- Increase confidence in public API behavior with focused regression tests.
- Keep docs synchronized with runtime behavior.

### Exit criteria

- No known high-severity defects in core APIs (`parse`, `convert`, `context`, compatibility checks).
- Full pytest suite green on Python `3.11`, `3.12`, `3.13`.
- Public docs and devguide reflect current behavior.

## 0.18.x - API freeze and contract tests

### Objectives

- Freeze public API surface and semantics for the stable line.
- Add explicit contract tests for exported symbols and key invariants.
- Remove ambiguity in parser capability and configuration behavior.
- Keep `release_gates` checks reproducible for Python `3.11`, `3.12`, `3.13`.

### Exit criteria

- Public exports and error contracts documented and tested.
- No planned breaking API change before `1.0.0`.
- Deprecation policy documented for any remaining legacy aliases.
- Manual `.github/workflows/release_gates.yaml` green on candidate commits.

## 0.19.x - Historical integration checkpoint

### Objectives

- Validate real integration scenarios with `argdigest`, `depdigest`, and `smonitor`.
- Run cross-repo smoke tests in clean environments.
- Run local-sibling smoke tests when `../argdigest`, `../depdigest`, and `../smonitor` are available.
- Collect and triage integrator feedback (blocking vs non-blocking).
- Complete deprecation contract for `pyunitwizard.main` (warning semantics and migration path).
- This line is closed as a historical checkpoint baseline.

### Current checkpoint (2026-03-04)

- Tag `0.19.3` created from `main` as RC checkpoint.
- Current head after RC checkpoint: run `git describe --tags --always`.
- Full suite baseline at current checkpoint: `376 passed` on local Python `3.13`
  (`pytest -q tests --ignore=tests/test_import.py`).
- Integration smoke coverage includes:
  - sibling repo import precedence and contract checks,
  - DepDigest contract/dependency assertions,
  - ArgDigest + PyUnitWizard pipeline checks (success and failure paths),
  - SMonitor catalog/probe diagnostic assertions.
  - shared collective E2E policy: scenario runs in each library repo CI
    (`pyunitwizard`, `argdigest`, `depdigest`, `smonitor`), while
    `molsyssuite` is evidence/coordination-only.
  - backend expansion and hardening for `physipy` and `quantities`.
  - transparent `matplotlib` bridge (`pyunitwizard.utils.matplotlib.setup_matplotlib`)
    to keep standard matplotlib workflows while accepting mixed backend quantities.
  - transparent `numpy` bridge (`pyunitwizard.utils.numpy.setup_numpy`) for
    quantity-aware dispatch in common operations (`mean`, `sum`, `std`, `var`,
    `dot`, `linalg.norm`, `trapezoid`) without changing `numpy` imports.
  - expanded `pandas` interoperability helpers in `pyunitwizard.utils.pandas`
    (`dataframe_from_quantities`, `add_quantity_column`, `get_quantity_column`,
    `get_units_map`, `set_units_map`, `sync_units_map`, `concat`, `merge`)
    with contract coverage.
  - advanced `matplotlib` layout tests (shared axes, twin axes, multi-backend
    compatible overlays).
  - cross-backend frontend matrix tests covering NumPy/Pandas/Matplotlib
    behavior for available backend forms and mixed-form pairs.

### Exit criteria (historical closure)

- Integration smoke checks green across the target ecosystem.
- Local sibling smoke test is passing in development workspaces and skip-safe in CI.
- No blocker incidents open in diagnostics flows.
- `pyunitwizard.main` deprecation policy is documented for pre-`1.0.0` and validated by tests.
- Release checklist for `1.0.0` fully actionable.
- Carry-over scope for `0.20.x`/`0.21.x` documented.

### Deprecation policy for `pyunitwizard.main`

- `0.18.x`: keep compatibility alias and emit `DeprecationWarning` on attribute access.
- `0.19.x`: keep alias without behavior changes, enforce warning/attribute contract by tests.
- `1.0.0`: keep alias only if no downstream blocker remains; otherwise drop in next minor after stable with migration notes.

## 0.20.x interoperability expansion policy

`0.20.x` is now reserved for integration expansion toward "transparent use" with:
- NumPy workflows,
- Matplotlib plotting,
- Pandas tabular pipelines.

Rules:
- keep API behavior additive and backward-compatible with `0.19.x`,
- preserve `pint` as hard dependency and optional backends as soft dependencies,
- avoid forcing users to replace `numpy/matplotlib/pandas` imports with
  `puw.*` imports for common workflows,
- provide explicit `puw.*` helpers as an optional strict mode for integrators.

## 0.21.x RC consolidation policy (active RC track)

`0.21.x` is the final stabilization window before `1.0.0`:
- validate interoperability additions under CI matrix continuity,
- close remaining collective blockers and traceability contracts,
- freeze behavior and docs for release-owner go/no-go.
- operate with `devguide/release_0.21.x_rc_checklist.md` as the active tracker.

## 1.0.0 - Stable release

### Objectives

- Publish stable API/contracts suitable for production use in scientific libraries.
- Confirm documentation, tests, and release automation are consistent and reproducible.

### Exit criteria

- Full test matrix and release pipeline green.
- `release_1.0.0_checklist.md` completed.
- No open blocker/high-severity bugs in PyUnitWizard core paths.
