# RC Close Readiness (`0.21.x`)

This note records closure evidence for the RC go/no-go checklist before release
owner approval.

## Date

- 2026-03-04

## 1. High-severity open issues in core public APIs

Status: none identified.

Evidence:
- Open issue query reviewed:
  - `gh issue list --state open --limit 200 --json number,title,labels,url`
- Current open issues do not include high-severity labeling or active blocker
  classification for core public API paths.

## 2. Open blocker incidents from ecosystem validation

Status: none open.

Evidence:
- Ecosystem validation is green (`6 passed`) and documented in
  `devguide/ecosystem_validation_0.21.x.md`.
- `Release Gates` blocker on first attempt (missing `PYTHONPATH`) was fixed and
  closed by green rerun:
  - failed run: `https://github.com/uibcdf/pyunitwizard/actions/runs/22656334939`
  - passing rerun: `https://github.com/uibcdf/pyunitwizard/actions/runs/22656402041`

## 3. `release_1.0.0_checklist.md` actionable/current

Status: ready.

Evidence:
- checklist now includes an explicit evidence index and standard verification
  commands aligned with the active `0.21.x` RC workflow.

## Remaining RC close step

- Release owner explicit approval to close the RC window.
