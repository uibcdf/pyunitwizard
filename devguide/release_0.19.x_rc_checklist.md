# Release 0.19.x RC Checklist

Use this checklist to operate the `0.19.x` release-candidate window before
tagging `1.0.0`.

All sections must be complete at least once during RC, and the "RC close"
section must be complete on the candidate commit that will lead to `1.0.0`.

## Status snapshot at `0.19.1` (2026-03-03)

- RC checkpoint tag published: `0.19.1`.
- Full test suite on local Python `3.13`: `252 passed`.
- Ecosystem integration smoke tests for `argdigest`, `depdigest`, `smonitor`: green.
- Local sibling smoke (`../argdigest`, `../depdigest`, `../smonitor`): green when repos are present.
- Remaining work toward RC close: CI/release-gates continuity over time, sustained incident tracking, and final release-owner go/no-go.

## 1. RC entry (open the stability window)

- [x] Confirm baseline policy: Python `3.11`, `3.12`, `3.13` supported.
- [x] Confirm `0.19.x` is documented as RC in README/devguide/docs.
- [ ] Confirm no planned breaking API change remains before `1.0.0`.
- [ ] Publish RC scope and known risks for integrators.

## 2. Stability monitoring during RC

- [x] Run full `pytest` suite regularly on local `3.13` and CI matrix.
- [ ] Keep CI matrix green on Ubuntu and macOS for supported Python versions.
- [ ] Run `.github/workflows/release_gates.yaml` on candidate commits.
- [ ] Track flaky tests and close or quarantine with explicit issue links.
- [ ] Record blocker vs non-blocker incidents for conversion/parser/config paths.

## 3. Ecosystem validation during RC

- [x] Validate integration smoke checks with `argdigest`.
- [x] Validate integration smoke checks with `depdigest`.
- [x] Validate integration smoke checks with `smonitor`.
- [x] Validate local-sibling smoke (`../argdigest`, `../depdigest`, `../smonitor`) when repos are available.
- [ ] Confirm no unresolved cross-repo contract drift is open.

## 4. Documentation and migration quality

- [ ] User docs and API docs match shipped behavior.
- [x] Developer docs include current release process and RC policy.
- [x] `pyunitwizard.main` deprecation contract is documented and test-backed.
- [ ] Release notes draft includes any migration notes and compatibility statements.

## 5. Collective 1.0 alignment during RC (ecosystem-wide checklist)

- [x] Unified configuration contract documented and validated with the same precedence used across sibling libraries (`runtime > env > file`).
- [x] All critical public API functions are instrumented with `@smonitor.signal`.
- [x] Optional dependency policy is aligned with DepDigest governance for heavy/optional backends.
- [x] User/dev diagnostics expose stable `CODE` and actionable `hint` semantics.
- [x] Compatibility matrix defines minimum supported versions for `argdigest`, `depdigest`, and `smonitor`.
- [ ] SMonitor profile consistency (`user`, `dev`, `qa`, `agent`) is validated from the PyUnitWizard consumer side.
- [ ] SMonitor traceability tags used by PyUnitWizard are aligned with cross-library failure categories.
- [x] DepDigest audit path is validated against PyUnitWizard dependency declarations.
- [x] ArgDigest integration confirms unit error mapping from PyUnitWizard into contract-layer errors with caller context.
- [x] PyUnitWizard kernel isolation behavior is explicitly validated and documented.
- [ ] Third-party/backend exceptions are translated into PyUnitWizard cataloged exception hierarchy.
- [x] Fundamental dimensions (`[L]`, `[M]`, `[T]`, `[K]`, `[mol]`, `[A]`, `[Cd]`) are treated as a locked serialization contract.
- [ ] Performance baseline exists for conversion/introspection hot paths and is tracked for regressions.

## 6. RC close (go/no-go to 1.0.0 candidate)

- [ ] No high-severity open issues in core public APIs.
- [ ] No open blocker incidents from ecosystem validation.
- [x] `devguide/release_1.0.0_checklist.md` is fully actionable and current.
- [ ] Release owner explicitly approves closing RC window.

## 7. Contingency decision: extend RC to `0.20.x` if needed

- [ ] If blocker items remain unresolved at planned RC close, open `0.20.x` as the next RC window instead of forcing `1.0.0`.
- [ ] Preserve no-breaking-change policy when moving from `0.19.x` RC to `0.20.x` RC.
- [ ] Publish explicit carry-over scope (`pending`, `blocked`, `deferred`) before creating the first `0.20.x` tag.
- [ ] Keep `1.0.0` gated by completion of this checklist and `devguide/release_1.0.0_checklist.md`.

## Evidence log (2026-03-03)

- Local quality baseline: `pytest -q` -> `252 passed` on Python `3.13`.
- RC checkpoint tag published: `0.19.1`.
- Integration evidence:
  - `tests/integration/test_ecosystem_smoke.py` (ArgDigest/DepDigest/SMonitor smoke and pipeline checks).
  - `tests/integration/test_local_sibling_repos.py` (local sibling imports + contract checks).
- Configuration precedence evidence (`runtime > env > file`) validated with real temporary-module tests in `tests/test_configure.py`.
- Deprecation contract evidence for `pyunitwizard.main` covered by `tests/test_api_layout.py` and documented in developer docs.
- DepDigest policy contract evidence covered by `tests/test_depdigest_contract.py`.
- SMonitor code/hint contract evidence covered by `tests/test_smonitor_catalog_contract.py`.
- Fundamental dimensions serialization contract evidence covered by `tests/test_kernel_contract.py`.
- Kernel isolation/restoration evidence covered by `tests/test_context.py` (including restoration after exception).
