---
summary: PR CI can be skipped and direct-push debt is unchecked
issue: uibcdf/pyunitwizard#91
status: partial
opened: 2026-09-29
closed:
severity: high
verification: inspected
area: [ci, governance]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# PR CI can be skipped and direct-push debt is unchecked

## What

At `4ffe2f1`, the primary `CI.yaml` PR test ignored documentation paths and
allowed `[skip ci]` in PR titles or `skip-ci` in branch names to skip its test
job. `main` had no effective branch rules. Direct-push skip markers had no
daily full-suite recovery. The
[weekly eight-cell matrix](https://github.com/uibcdf/pyunitwizard/actions/runs/36457307824)
passed at that exact commit, including executed `Run tests` steps in all four
Linux cells. This is a routing and enforcement gap, not a failed test suite.

## How

Run the complete Linux 3.13 PR test without workflow path or title/branch
skip conditions. Require its stable check on PRs, while administrators retain
direct pushes. Preserve the existing weekly and manual full matrix. Add a
conditional daily full matrix at 00:57 America/Mexico_City that detects
skipped commits since the last executed, green Linux matrix. If run history
or API evidence is unavailable, run it. A probe input checks the backlog
without dispatching test jobs. Keep the scheduled-failure monitor tied to
the original weekly trigger so a debt-free daily run does not open a false
failure issue.

## Why

PyUnitWizard is a shared support library. A green weekly matrix does not
guard a PR whose test job never ran, and repeated skipped direct pushes can
leave regressions unseen. The conditional daily route implements the suite
policy in `uibcdf/molsyssuite#39` without requiring a full matrix after each
commit. The current collaborator list contains only `dprada` and `LMMV`,
both administrators; external contributors use the protected PR route.

## What is measured and what is assumed

The existing weekly matrix at `4ffe2f1` passed all eight jobs, including
executed test steps. The actual 00:57 schedule, a hosted PR and the public
platform claims have not yet been reviewed.

## What was refuted

A successful workflow with its matrix job skipped is not evidence of a full
suite run. A weekly failure monitor that also evaluates the debt-free daily
schedule would incorrectly report a skipped matrix as failed.

## Scope and exclusions

This record covers CI routing, skip debt and branch protection. Scientific
test assertions and release publishing remain component-owned work.

## Acceptance criteria

- The required PR test cannot be omitted by local filters or skip conditions.
- Skipped direct pushes stay due until an executed full Linux matrix passes.
- Hosted routine, full-matrix and probe evidence are recorded.
- Branch protection preserves direct pushes for the named internal maintainers.
- A debt-free nightly does not trigger the weekly failure monitor.
- The first real nightly and PR route are observed before calling this adopted.

## Dependencies and risks

The nightly schedule may be delayed or dropped by GitHub; the detector keeps
the backlog due until an executed green matrix provides a new watermark.

## Resolution

Commit `4b7f5ed` implements the workflow and detector. At that exact commit,
[routine CI](https://github.com/uibcdf/pyunitwizard/actions/runs/36536757396)
and [MolSysSuite policy](https://github.com/uibcdf/pyunitwizard/actions/runs/36536758336)
passed. The [probe-only dispatch](https://github.com/uibcdf/pyunitwizard/actions/runs/36536772026)
recognized the executed weekly matrix `36457307824` at `4ffe2f1` as its
watermark, found zero later skipped commits, and omitted all matrix and
weekly-monitor jobs.

The `main` branch now requires the strict `Test on ubuntu-latest, Python 3.13`
check. The current collaborators, administrators `dprada` and `LMMV`, can
bypass it for direct pushes. The direct
push of `cdccfa8` with `[skip ci]` exercised that bypass. Its
[probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36537194515)
chose full recovery but reported no usable watermark and counted 63
historical skipped commits. Inspection showed that GitHub's workflow-run
listing with `branch=main` omitted the recent `36457307824` matrix and other
recent runs, while the unfiltered listing included them with
`head_branch=main`. The detector now filters `head_branch` itself. The
[second hosted probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36538129589)
recognized the weekly watermark and counted exactly the one intentionally
skipped commit `cdccfa8`; its matrix and monitor jobs were omitted. Keep this
issue open until recovery, the first actual nightly, hosted PR route, and
platform-claim review.

The [manual full matrix](https://github.com/uibcdf/pyunitwizard/actions/runs/36538496360)
at `8dc7f63` executed all eight test jobs; seven passed and Linux 3.13
failed its `Run tests` step with one `LibraryWithoutParserError` in
`tests/utils/sequences/test_slice.py::test_get_value_pint` (636 passed,
3 skipped). This is a component test behavior outside this governance change.
The [following probe](https://github.com/uibcdf/pyunitwizard/actions/runs/36539355874)
still reported one skipped commit since the `4ffe2f1` weekly watermark, as
required: a failed full matrix cannot erase the debt. The component team owns
the test failure; this issue remains partial until a green recovery run.

## Routine policy 1.5.4 adoption — 2026-10-03

The maintainer authorized publication and adoption of policy-v1.5.4 under
uibcdf/molsyssuite#39. The immutable tag points to central e459ea0; the
component now calls that published gate and receives the byte-identical
canonical guide through the suite synchronizer. Routine development uses
Python 3.14. The existing full Python 3.11–3.14 matrices and skipped-commit
recovery semantics are preserved; no public package is published here.
Local conformance and changed-workflow Actionlint checks pass. Hosted
policy and applicable routine checks are dispatched separately from skipped
direct pushes; their exact commits and outcomes remain to be measured.

The single Linux routine package suite moves to Python 3.14; the required
PR check must use its new name while preserving strict checks and administrator
direct-push bypass. The complete weekly matrix still includes every older minor.

