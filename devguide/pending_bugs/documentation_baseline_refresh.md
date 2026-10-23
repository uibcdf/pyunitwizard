---
summary: Refresh developer documentation against the current supported baseline.
issue: uibcdf/pyunitwizard#119
status: active
opened: 2026-10-22
closed:
severity: low
verification: inspected
area: [documentation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Documentation baseline refresh

## What

Current public/developer pages retain old dependency floors, removed environment
helpers, the wrong test-profile filename and an obsolete Python 3.13 test command
that excludes import coverage. The contributor README incorrectly promises a
deployment after every main push and conflates two Sphinx output layouts.
Rendered-link validation also reproduces a shared footer URL with a nonexistent
`contents/` path and no depth handling. The homepage badge omits Python 3.14.

## How

Reconcile current pages with package metadata, maintained compatibility/release
records, actual Conda profiles, Makefile and publishing workflow. Keep historic
release evidence intact. Correct the canonical client guide's mandatory dependency
inventory; client-copy delivery is owned by uibcdf/molsyssuite#126, opened before
publication. Do not edit clients or claim runtime adoption from guide delivery.
Use Sphinx's `pathto` for the footer and include Python 3.14 on the homepage.
An explicit H1 on the homepage resolves its four pre-existing heading warnings.

## Why

Returning contributors need executable setup instructions and an accurate public
baseline. Missing mandatory dependencies can yield incomplete source environments;
incorrect deployment instructions can leave the served site stale.

## What is measured and what is assumed

Source inspection establishes drift against pyproject.toml and workflow events.
Local HTML generation and fresh served-page checks will establish build and actual
publication separately. No numerical regression is established. Global shared
environment conflicts remain with uibcdf/molsyssuite#82.

## What was refuted

A main-branch push is not a publication trigger. Makefile `-b html` output is
`docs/_build/index.html`, whereas the hosted action's `-M html` output is
`docs/_build/html/index.html`. A delivered optional-provider guide does not raise
the qualified fallback floor.

## Scope and exclusions

Prose, documentation template, accepted instructions and guide inventory only. No runtime,
workflow, dependency declaration, environment mutation, tag or artifact changes.
Existing 0.28.1 qualification remains evidence for its original source/file.

## Acceptance criteria

- Current pages agree with metadata, profiles and release-title instructions.
- Local HTML builds; removed commands and incorrect paths are absent from current pages.
- Authorized docs workflow succeeds and fresh public HTML contains the update.
- MolSysSuite receives the canonical guide source commit/digest and owns client delivery.
- Archive this record and regenerate indexes after publication verification.

## Dependencies and risks

Public serving can lag the workflow. Preserve its source identity and verify
actual content before closing. Client synchronization is an independent central
deliverable; local closure does not close uibcdf/molsyssuite#126.

## Local validation — 2026-10-22

Python 3.14.7: `make -C docs html` in an owned source copy passes with zero
warnings. Sphinx `-M html SOURCE OUTPUT -W --keep-going` also passes and
produces the distinct hosted `html/index.html` layout. Rendered-content checks
pass on eleven pages, including 399 relative link targets, corrected floors,
Python 3.14, source-install dependencies and release-title examples. All four
documented Conda profile paths exist and the floors agree with project metadata.
`python -m pytest --receptor=llm tests/test_reporting_protocol.py` passes all
nine tests; index and diff checks pass. No scientific code or workflow changed;
these documentation checks do not requalify another platform or public artifact.
Deployment and fresh public-page verification remain required before closure.
