# Release 1.0.0 Checklist

Use this checklist as a hard release gate. All items must be complete before creating the final `1.0.0` tag.

## 1. Quality gates

- [ ] `pytest` full suite is green locally and in CI.
- [ ] CI matrix is green for Python `3.11`, `3.12`, `3.13`.
- [ ] Coverage trend is stable or improving in critical API modules.
- [ ] No flaky tests in release-critical paths.
- [ ] `.github/workflows/release_gates.yaml` (manual `workflow_dispatch`) is green for the candidate commit.

## 2. API and behavior

- [ ] Public API exports are frozen and covered by contract tests.
- [ ] Parser/default configuration behavior is deterministic and documented.
- [ ] No open blockers in conversion, standardization, parsing, or compatibility workflows.

## 3. Diagnostics and observability

- [ ] SMonitor catalog codes used by PyUnitWizard are stable and documented.
- [ ] Probe severity contract (`DEBUG`/`WARNING`/`ERROR`) is respected.
- [ ] User-facing diagnostics include actionable remediation hints.

## 4. Ecosystem coordination

- [ ] Integration smoke checks passed with `argdigest`.
- [ ] Integration smoke checks passed with `depdigest`.
- [ ] Integration smoke checks passed with `smonitor`.
- [ ] Cross-repo compatibility notes are updated in each devguide as needed.

## 5. Packaging and release

- [ ] `pyproject.toml` metadata and Python support range are correct.
- [ ] Build and installation workflows are green (`sdist`, wheel, conda).
- [ ] README and devguide documents are synchronized with shipped behavior.
- [ ] Tag/release notes prepared with migration notes (if any).

## 6. Final go/no-go

- [ ] No high-severity open issues.
- [ ] All checklist items completed and reviewed.
- [ ] Release owner approves `1.0.0` tag creation.
