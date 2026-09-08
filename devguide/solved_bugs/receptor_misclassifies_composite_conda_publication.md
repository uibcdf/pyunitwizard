---
summary: Use the release profile for action-internal Conda publication.
issue: uibcdf/pyunitwizard#73
status: resolved
opened: 2026-09-08
closed: 2026-09-08
severity: low
verification: reproduced
area: [tooling, release]
guard: tests/test_gh_run_receptor_policy.py
normative:
blocked_by: []
supersedes: []
---

# The configured Conda matrix is not visible to GitHub

## What

PyUnitWizard's GH Run Receptor configuration selects `conda` and requires `linux-64`,
`osx-64`, and `osx-arm64` for its release-triggered Conda workflow. GitHub exposes jobs
for Python 3.11, 3.12, and 3.13; the native platforms are inputs to
`uibcdf/action-build-and-upload-conda-packages@v2.0.1` and are built inside that action.

The receptor therefore has no platform-named job or GitHub artifact from which to satisfy
`expected_platforms`. The same topology produced a false derived `FAIL` in
`uibcdf/smonitor#10`.

## How

Select `release` for the observable publication workflow. This retains GitHub's status,
conclusion, event, SHA, ref, and visible package/publish steps without claiming that a
hidden platform or external registry was verified. Keep Anaconda as an independent
publication gate. Structured support for action-internal platform matrices remains
provider work in `uibcdf/gh-run-receptor#35`.

## Why

The current rule is structurally valid but semantically stronger than the available
evidence. It can turn a successful GitHub run into a receptor failure solely because the
configured platform identities never exist in GitHub's observable topology. That makes
the preferred first-inspection path noisy and risks teaching maintainers to ignore a
real required-platform failure later.

## What is measured and what is assumed

Source inspection confirms one Python-version matrix and three true native-platform
inputs inside the shared publishing action. SMonitor run `34278594890` measured the same
evidence shape against gh-run-receptor and is the provider reproduction linked above.

No PyUnitWizard release run has yet been inspected for this report. The diagnosis assumes
the shared action preserves its current boundary at runtime; the workflow source and the
SMonitor measurement make that assumption explicit rather than presenting it as a local
run result.

## What was refuted

- The workflow filename and release trigger do not make a native matrix visible.
- Action inputs request work but do not prove a platform package was produced or uploaded.
- Removing only `expected_platforms` would hide the evidence mismatch behind zero observed
  platforms.
- Selecting `release` does not prove Anaconda delivery; the profile explicitly reports
  the registry as not observed.

## Scope and exclusions

This local change does not modify the publishing workflow, infer package delivery, or
implement the provider-side structured matrix contract. It changes only the interpretation
of evidence already visible to GitHub.

## Acceptance criteria

- The exact workflow rule selects `release` and carries no `expected_platforms`.
- GH Run Receptor 0.19.0 accepts the configuration and explains that exact match.
- A regression guard prevents restoration of the unobservable native-matrix contract.
- The local report links the provider issue and states that Anaconda remains independent.

## Dependencies and risks

The safe local profile change is not blocked by `uibcdf/gh-run-receptor#35`. When that
provider issue supplies reviewed structured producer evidence, PyUnitWizard should
reevaluate whether the workaround can be removed.

## Resolution

The workflow rule now selects `release` and no longer declares native platforms absent
from GitHub's observable evidence. The test-first guard failed against the former rule and
passes after the correction. GH Run Receptor 0.19.0 accepts the configuration and explains
the exact workflow match as `profile=release`; external registry verification remains a
separate publication gate.
