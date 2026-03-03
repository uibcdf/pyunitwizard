# Roadmap to 1.0.0

This roadmap defines the stabilization path from the `0.19.x` release-candidate
line to a stable `1.0.0` release.

## Release stages

1. `0.17.x` - Hardening and correctness
2. `0.18.x` - API freeze and contract tests
3. `0.19.x` - Release candidate (ecosystem validation and stability window)
4. `0.20.x` - Release candidate extension (only if blockers remain)
5. `1.0.0` - Stable release

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

## 0.19.x - Release candidate

### Objectives

- Validate real integration scenarios with `argdigest`, `depdigest`, and `smonitor`.
- Run cross-repo smoke tests in clean environments.
- Run local-sibling smoke tests when `../argdigest`, `../depdigest`, and `../smonitor` are available.
- Collect and triage integrator feedback (blocking vs non-blocking).
- Complete deprecation contract for `pyunitwizard.main` (warning semantics and migration path).
- Keep this line open for a stability observation window before `1.0.0`.

### Exit criteria

- Integration smoke checks green across the target ecosystem.
- Local sibling smoke test is passing in development workspaces and skip-safe in CI.
- No blocker incidents open in diagnostics flows.
- `pyunitwizard.main` deprecation policy is documented for pre-`1.0.0` and validated by tests.
- Release checklist for `1.0.0` fully actionable.
- RC closure checks in `devguide/release_0.19.x_rc_checklist.md` are complete.

### Deprecation policy for `pyunitwizard.main`

- `0.18.x`: keep compatibility alias and emit `DeprecationWarning` on attribute access.
- `0.19.x`: keep alias without behavior changes, enforce warning/attribute contract by tests.
- `1.0.0`: keep alias only if no downstream blocker remains; otherwise drop in next minor after stable with migration notes.

## 0.20.x contingency policy

`0.20.x` must only be used if `0.19.x` RC closure criteria are not met by the
planned close date.

When this contingency is activated:

- keep API behavior additive and backward-compatible with `0.19.x`,
- carry unresolved RC items explicitly from `release_0.19.x_rc_checklist.md`,
- treat `0.20.x` as an extension of the same stabilization window, not a reset.

## 1.0.0 - Stable release

### Objectives

- Publish stable API/contracts suitable for production use in scientific libraries.
- Confirm documentation, tests, and release automation are consistent and reproducible.

### Exit criteria

- Full test matrix and release pipeline green.
- `release_1.0.0_checklist.md` completed.
- No open blocker/high-severity bugs in PyUnitWizard core paths.
