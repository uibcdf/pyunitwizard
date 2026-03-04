# Release 0.21.x RC Checklist

Use this checklist for the active RC consolidation window before `1.0.0`.

## Status snapshot (starting point after `0.20.0`)

- Interoperability expansion shipped in `0.20.0` (NumPy/Pandas/Matplotlib).
- Current baseline command: `pytest -q tests --ignore=tests/test_import.py`.
- Current performance baseline file: `devguide/performance_baseline_0.20.x.json`.

## 1. RC entry

- [x] Confirm baseline policy: Python `3.11`, `3.12`, `3.13` supported.
- [x] Confirm `0.21.x` is documented as active RC in README/devguide/docs.
- [x] Confirm no planned breaking API change remains before `1.0.0`.
- [x] Publish RC scope and known risks for integrators.

## 2. Stability monitoring during RC

- [x] Keep CI matrix green on Ubuntu and macOS for supported Python versions.
- [x] Run `.github/workflows/release_gates.yaml` on candidate commits.
- [x] Track flaky tests and close or quarantine with explicit issue links.
- [x] Record blocker vs non-blocker incidents for conversion/parser/config paths.

## 3. Ecosystem validation during RC

- [x] Validate integration smoke checks with `argdigest`.
- [x] Validate integration smoke checks with `depdigest`.
- [x] Validate integration smoke checks with `smonitor`.
- [x] Validate local-sibling smoke (`../argdigest`, `../depdigest`, `../smonitor`) when repos are available.
- [x] Confirm no unresolved cross-repo contract drift is open.

## 4. Documentation and migration quality

- [x] User docs and API docs match shipped behavior.
- [x] Developer docs include current release process and RC policy.
- [x] `devguide/minimum_quantity_protocol_contract.md` is aligned with actual tested behavior.
- [x] `devguide/frontend_transparent_mode_contract.md` is aligned with actual tested behavior.
- [x] Release notes draft includes migration notes and compatibility statements.

## 5. RC close (go/no-go to `1.0.0`)

- [x] No high-severity open issues in core public APIs.
- [x] No open blocker incidents from ecosystem validation.
- [x] `devguide/release_1.0.0_checklist.md` is fully actionable and current.
- [ ] Release owner explicitly approves closing RC window.
