# Release 0.19.x RC Checklist

Use this checklist to operate the `0.19.x` release-candidate window before
tagging `1.0.0`.

All sections must be complete at least once during RC, and the "RC close"
section must be complete on the candidate commit that will lead to `1.0.0`.

## 1. RC entry (open the stability window)

- [ ] Confirm baseline policy: Python `3.11`, `3.12`, `3.13` supported.
- [ ] Confirm `0.19.x` is documented as RC in README/devguide/docs.
- [ ] Confirm no planned breaking API change remains before `1.0.0`.
- [ ] Publish RC scope and known risks for integrators.

## 2. Stability monitoring during RC

- [ ] Run full `pytest` suite regularly on local `3.13` and CI matrix.
- [ ] Keep CI matrix green on Ubuntu and macOS for supported Python versions.
- [ ] Run `.github/workflows/release_gates.yaml` on candidate commits.
- [ ] Track flaky tests and close or quarantine with explicit issue links.
- [ ] Record blocker vs non-blocker incidents for conversion/parser/config paths.

## 3. Ecosystem validation during RC

- [ ] Validate integration smoke checks with `argdigest`.
- [ ] Validate integration smoke checks with `depdigest`.
- [ ] Validate integration smoke checks with `smonitor`.
- [ ] Validate local-sibling smoke (`../argdigest`, `../depdigest`, `../smonitor`) when repos are available.
- [ ] Confirm no unresolved cross-repo contract drift is open.

## 4. Documentation and migration quality

- [ ] User docs and API docs match shipped behavior.
- [ ] Developer docs include current release process and RC policy.
- [ ] `pyunitwizard.main` deprecation contract is documented and test-backed.
- [ ] Release notes draft includes any migration notes and compatibility statements.

## 5. RC close (go/no-go to 1.0.0 candidate)

- [ ] No high-severity open issues in core public APIs.
- [ ] No open blocker incidents from ecosystem validation.
- [ ] `devguide/release_1.0.0_checklist.md` is fully actionable and current.
- [ ] Release owner explicitly approves closing RC window.

