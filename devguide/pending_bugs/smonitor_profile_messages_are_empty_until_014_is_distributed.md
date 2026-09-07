---
summary: QA and agent catalog messages remain empty until SMonitor 0.14 is distributed.
issue: uibcdf/pyunitwizard#71
status: blocked
opened: 2026-09-06
closed:
severity: medium
verification: reproduced
area: [diagnostics, deps]
guard:
normative:
blocked_by: [uibcdf/smonitor#8]
supersedes: []
---

# QA and agent catalog messages remain empty until SMonitor 0.14 is distributed

## What

PyUnitWizard catalog entries define `user_message` and `dev_message`. With the SMonitor
0.13 line currently resolved by the conda CI environment, all eleven catalog codes
resolve to an empty message under the `qa` and `agent` profiles.

## How

SMonitor before 0.14 selects only the profile-specific message field. Its current source
implements a fallback chain, but that behavior is not yet available through the
dependency path exercised by PyUnitWizard CI. A temporary downstream guard and 0.14
floor in commit `75a3604` reproduced the empty output in Actions run `34161369362`; the
premature requirement was withdrawn in `313eb3e`, after which run `34165675202` passed.

## Why

The `agent` profile exists for machine triage, so an event with a code but no message is
materially incomplete. Duplicating the same text into `qa_message` and `agent_message`
for every local code would conceal a provider defect and create permanent catalog drift.
The provider release is tracked by `uibcdf/smonitor#8` under the shared-stewardship rule.

## What is measured and what is assumed

Measured in CI: the eleven codes listed by the failure all render empty under `qa` and
`agent` with the resolved dependency environment. Inspected in the SMonitor source: its
current manager contains the intended fallback chain. Assumed until provider release:
the published 0.14 artifact will contain that exact behavior.

## What was refuted

Raising the PyUnitWizard minimum version alone is not currently viable. The project
installation step uses `--no-deps` after the conda environment is solved, so metadata
cannot turn an unavailable provider build into the required runtime behavior.

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
