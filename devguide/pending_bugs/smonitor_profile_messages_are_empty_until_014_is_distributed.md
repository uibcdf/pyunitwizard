---
summary: QA and agent catalog messages remain empty until SMonitor 0.14 is distributed.
issue: uibcdf/pyunitwizard#71
status: active
opened: 2026-09-06
closed:
severity: medium
verification: reproduced
area: [diagnostics, deps]
guard: tests/test_smonitor_catalog_contract.py
normative:
blocked_by: []
supersedes: []
---

# QA and agent catalog messages remain empty until SMonitor 0.14 is distributed

## What

PyUnitWizard catalog entries define `user_message` and `dev_message`. With the SMonitor
0.13 line currently resolved by the conda CI environment, all eleven catalog codes
resolve to an empty message under the `qa` and `agent` profiles.

## How

SMonitor before 0.14 selects only the profile-specific message field. Its current source
implements a fallback chain, and 0.14.0 is now available through the UIBCDF Conda channel.
A temporary downstream guard and 0.14 floor in commit `75a3604` reproduced the empty
output in Actions run `34161369362`; the premature requirement was withdrawn in
`313eb3e`, after which run `34165675202` passed. Provider publication completed in
`uibcdf/smonitor#8`; the dependency floors and guard are now active here.

## Why

The `agent` profile exists for machine triage, so an event with a code but no message is
materially incomplete. Duplicating the same text into `qa_message` and `agent_message`
for every local code would conceal a provider defect and create permanent catalog drift.
The provider release is tracked by `uibcdf/smonitor#8` under the shared-stewardship rule.

## What is measured and what is assumed

Measured in the earlier CI run: the eleven codes listed by the failure all rendered empty
under `qa` and `agent` with SMonitor 0.13. Inspected in the SMonitor source and release
record: 0.14.0 contains the intended fallback chain and 12 Conda distributions cover the
supported Python/platform matrix. The remaining measurement is PyUnitWizard's own remote
matrix with the raised floor and permanent guard.

## What was refuted

Raising the PyUnitWizard minimum version before provider publication was not viable. The
project installation step uses `--no-deps` after the conda environment is solved, so
metadata could not turn an unavailable provider build into the required runtime behavior.
That constraint remains useful: the Conda recipe floor must move with project metadata.

## Scope and exclusions

This report covers profile-message fallback and the PyUnitWizard dependency floor. The
shape of catalog exception constructors is resolved separately by
`uibcdf/pyunitwizard#68`.

## Acceptance criteria

1. SMonitor 0.14 or a later release containing the fallback is available through the
   dependency path used by PyUnitWizard CI.
2. PyUnitWizard raises both project and conda recipe floors to that version.
3. A regression test asserts that every catalog code renders a non-empty message under
   `user`, `dev`, `qa`, `agent` and `debug`.
4. The full supported Python matrix passes with the released provider artifact.
