# Roadmap to 1.0.0

This roadmap defines the stabilization path from the current `0.18.x` line to a stable `1.0.0` release.

## Release stages

1. `0.17.x` - Hardening and correctness
2. `0.18.x` - API freeze and contract tests
3. `0.19.x` - Ecosystem validation (ArgDigest/DepDigest/SMonitor)
4. `1.0.0` - Stable release

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

## 0.19.x - Ecosystem validation

### Objectives

- Validate real integration scenarios with `argdigest`, `depdigest`, and `smonitor`.
- Run cross-repo smoke tests in clean environments.
- Collect and triage integrator feedback (blocking vs non-blocking).

### Exit criteria

- Integration smoke checks green across the target ecosystem.
- No blocker incidents open in diagnostics flows.
- Release checklist for `1.0.0` fully actionable.

## 1.0.0 - Stable release

### Objectives

- Publish stable API/contracts suitable for production use in scientific libraries.
- Confirm documentation, tests, and release automation are consistent and reproducible.

### Exit criteria

- Full test matrix and release pipeline green.
- `release_1.0.0_checklist.md` completed.
- No open blocker/high-severity bugs in PyUnitWizard core paths.
