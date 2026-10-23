# Release 1.0.0 Checklist

Use this checklist as a hard release gate. All items must be complete before creating the final `1.0.0` tag.

## Evidence index

Current published checkpoint: `0.29.0` (2026-10-23). Its source/installed/public
receipts are in `completed_proposals/release_0.29.0.md` and
`evidence/release_0.29.0_2026-10-23.json`; current floors are in
`compatibility_matrix.md`. These establish that release's scope and do not
qualify a future 1.0 candidate or admit provisional contracts.

Retain these historical RC records and maintained contracts as context while
collecting fresh candidate evidence for each section:
- `devguide/stability_monitoring_0.21.x.md`
- `devguide/ecosystem_validation_0.21.x.md`
- `devguide/docs_api_alignment_0.21.x.md`
- `devguide/minimum_quantity_protocol_contract.md`
- `devguide/frontend_transparent_mode_contract.md`
- `devguide/api_freeze_pre_1.0_decision.md`
- `devguide/release_0.21.x_notes_draft.md`

## Standard commands for verification

- Local full suite:
  - `pytest --receptor=ci -q tests`
- Docs build:
  - `make -C docs html`
- RC release gates (GitHub):
  - `.github/workflows/release_gates.yaml` via `workflow_dispatch`
- Matrix continuity (GitHub):
  - `.github/workflows/CI_full_matrix.yaml` via `workflow_dispatch` or weekly schedule.

## 1. Quality gates

- [ ] `pytest` full suite is green locally and in CI.
- [ ] Linux and macOS arm64 CI matrices are green for Python `3.11`–`3.14`.
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
- [ ] Provisional `QuantityRecord` / `QuantityRecordBundle` API and `qrec` format (#82): either promoted (frozen, contract-tested, format version fixed) or explicitly kept provisional in the release notes. Admitted as a provisional surface on 2026-09-24 under the change-control policy of `api_freeze_pre_1.0_decision.md`.
  Scope decision 2026-10-04: retain the API and `qrec/0.3` / `qrec-bundle/0.3`
  as provisional; final release notes must carry that status. MVP/design issue
  closure does not satisfy the release gate. Independent extensions are #101–#106.
- [ ] State the provisional status of `MeasurementRecord` and
  `qrec-measurement/0.1` (#90) in final release notes. The bounded scalar-statement
  exception is admitted on 2026-10-04; future stable admission is a separate review.

## 3. Diagnostics and observability

- [ ] SMonitor catalog codes used by PyUnitWizard are stable and documented.
- [ ] Probe severity contract (`DEBUG`/`WARNING`/`ERROR`) is respected.
- [ ] User-facing diagnostics include actionable remediation hints.

## 4. Ecosystem coordination

- [ ] Optional OpenFF 0.4.0 evidence (#86): Python 3.12–3.14/Pint <0.26
  consumer matrix and installed-reader tests are identified for the candidate;
  baseline Python 3.11 absence diagnostics and dependencies remain supported.
  The val/unit tools leave the verified domain and do not promote qrec formats.

- [ ] Integration smoke checks passed with `argdigest`.
- [ ] Integration smoke checks passed with `depdigest`.
- [ ] Integration smoke checks passed with `smonitor`.
- [ ] Local sibling smoke test (`../argdigest`, `../depdigest`, `../smonitor`) is green when repos are present.
- [ ] Cross-repo compatibility notes are updated in each devguide as needed.

## 5. Packaging and release

- [ ] `pyproject.toml` metadata and Python support range are correct.
- [ ] Linux and macOS build and installation workflows are green (`sdist`, wheel, conda).
- [ ] Release artifacts do not claim or publish Windows support.
- [ ] README and devguide documents are synchronized with shipped behavior.
- [ ] Serialization status is explicit in release notes: `devguide/serialization_contract_draft.md` is superseded by `QuantityRecord` (#82), whose API and `qrec` format are provisional unless promoted.
- [ ] Tag/release notes prepared with migration notes (if any).

## 6. Final go/no-go

- [ ] No high-severity open issues.
- [ ] All checklist items completed and reviewed.
- [ ] Release owner approves `1.0.0` tag creation.

## Optional CF/HDF5 scope (#108/#101)

- [ ] Keep `pyunitwizard.dialects.cf`, `pyunitwizard.storage.hdf5` and
  `qrec-hdf5/0.1` explicitly provisional in release notes; qrec/0.3 stays unchanged.
- [ ] Retain actual cf-units/UDUNITS + h5py installed qualification and the
  supported optional Linux/macOS Python 3.11–3.14 matrix before making claims.
- [ ] State physical-unit/temperature scope and the absence of calendar,
  streaming/append, whole-CF-dataset and H5MSM consumer-migration qualification.
- [ ] Development qualification and public artifact evidence retain their own
  candidate/file identities. The 0.28.0/0.28.1 records supply public evidence
  for those releases; the 1.0 candidate needs its own mandatory executed gates.
  Codecov #107 is closed after actual uploads recovered; verify current required
  uploads rather than carrying that historical incident as open debt.

## Provisional record extensions (#104/#102/#105/#103)

- [ ] State the provisional tagged layout, immutable append and Zarr/Arrow
  bindings in release notes. Keep qrec/0.3 and bundle bytes compatible.
- [ ] Identify the optional source/installed Linux/macOS arm64 Python 3.11–3.14
  matrix, including real consumer fixtures, lazy/absence/transitive-failure
  guards and the explicit reader unit/kind handshakes.
- [ ] Retain benchmark scope: tiled coordinates are synthetic, partial Zarr
  verification covers selected chunk contents, immutable append still copies
  total values, Arrow nulls are refused and Parquet reads complete files.
- [ ] Qualify the exact required public artifact; source tests do not establish
  installed-public dependency closure or migration in consumer repositories.
- [ ] Follow the central release/package notice policy delivered under
  MolSysSuite #129: open/update a version-specific issue for each actual release
  or package event, including an explicit pending/unpublished package state.

## Bounded UCUM/ASDF/vocabulary inventory (#85)

- [ ] Keep #125/#126/#127 tools and `qrec-asdf/0.1` /
  `qrec-vocabulary/0.1` provisional and name their bounded exclusions in notes.
- [ ] Identify exact source/installed Linux/macOS Python 3.11–3.14 evidence for
  ucumvert 0.3.2, asdf 6.0.0 and asdf-astropy 0.11.0; required provider guards
  must execute, and vocabulary resources must come from the installed artifact.
- [ ] Retain actual ChEMBL/Gaia provenance, attribution and ontology extraction
  inputs. UO unit IRIs remain separate from QUDT kinds; reviewed local alignments
  do not become upstream exactMatch assertions or automatic kind inference.
- [ ] Future CF calendar coordinates, complete clinical/astronomy schemas,
  unknown vocabulary expansion and consumer migrations need their own contracts.
  Following the maintainer's 2026-10-23 request, announce availability once the
  package and GitHub Release are verified; reuse that version's notice and retain
  links, scope and installed evidence. Pre-rollout impact notices stay separate.


## 0.29.0 checkpoint — 2026-10-23

The bounded #85 inventory and #102–#105 extensions are delivered and qualified
in public 0.29.0. The original source, separate qualifier and immutable file
have distinct retained receipts. MolSysSuite #132 owns availability and guide
coordination. The unchecked gates above remain obligations for the future
1.0 candidate; this checkpoint neither admits provisional contracts as stable
nor qualifies migrations in consuming repositories.
