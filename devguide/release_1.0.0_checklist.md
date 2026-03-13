# Release 1.0.0 Checklist

Use this checklist as a hard release gate. All items must be complete before creating the final `1.0.0` tag.

## Evidence index (current RC line)

Use these documents as the primary evidence sources while closing each section:
- `devguide/stability_monitoring_0.21.x.md`
- `devguide/ecosystem_validation_0.21.x.md`
- `devguide/docs_api_alignment_0.21.x.md`
- `devguide/minimum_quantity_protocol_contract.md`
- `devguide/frontend_transparent_mode_contract.md`
- `devguide/api_freeze_pre_1.0_decision.md`
- `devguide/release_0.21.x_notes_draft.md`

## Standard commands for verification

- Local full suite:
  - `pytest -q tests --ignore=tests/test_import.py`
- Docs build:
  - `make -C docs html`
- RC release gates (GitHub):
  - `.github/workflows/release_gates.yaml` via `workflow_dispatch`
- Matrix continuity (GitHub):
  - `.github/workflows/CI_full_matrix.yaml` via `workflow_dispatch` or weekly schedule.

## 1. Quality gates

- [ ] `pytest` full suite is green locally and in CI.
- [ ] CI matrix is green for Python `3.11`, `3.12`, `3.13`.
- [ ] Coverage trend is stable or improving in critical API modules.
- [ ] No flaky tests in release-critical paths.
- [ ] `.github/workflows/release_gates.yaml` (manual `workflow_dispatch`) is green for the candidate commit.

## 2. API and behavior

- [ ] Public API exports are frozen and covered by contract tests.
- [ ] Parser/default configuration behavior is deterministic and documented.
- [ ] Minimum quantity protocol contract is frozen and test-backed (`devguide/minimum_quantity_protocol_contract.md`).
- [ ] Transparent frontend mode contract is frozen and test-backed (`devguide/frontend_transparent_mode_contract.md`).
- [ ] Legacy `pyunitwizard.main` deprecation contract is tested and documented.
- [ ] No open blockers in conversion, standardization, parsing, or compatibility workflows.

## 3. Diagnostics and observability

- [ ] SMonitor catalog codes used by PyUnitWizard are stable and documented.
- [ ] Probe severity contract (`DEBUG`/`WARNING`/`ERROR`) is respected.
- [ ] User-facing diagnostics include actionable remediation hints.

## 4. Ecosystem coordination

- [ ] Integration smoke checks passed with `argdigest`.
- [ ] Integration smoke checks passed with `depdigest`.
- [ ] Integration smoke checks passed with `smonitor`.
- [ ] Local sibling smoke test (`../argdigest`, `../depdigest`, `../smonitor`) is green when repos are present.
- [ ] Cross-repo compatibility notes are updated in each devguide as needed.

## 5. Packaging and release

- [ ] `pyproject.toml` metadata and Python support range are correct.
- [ ] Build and installation workflows are green (`sdist`, wheel, conda).
- [ ] README and devguide documents are synchronized with shipped behavior.
- [ ] Serialization draft status is explicit in release notes (`devguide/serialization_contract_draft.md`: draft/non-stable unless promoted).
- [ ] Tag/release notes prepared with migration notes (if any).

## 6. Final go/no-go

- [ ] No high-severity open issues.
- [ ] All checklist items completed and reviewed.
- [ ] Release owner approves `1.0.0` tag creation.
