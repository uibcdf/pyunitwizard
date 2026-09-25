---
summary: Review inherited Python ecosystem policy in PyUnitWizard.
issue: uibcdf/pyunitwizard#89
status: active
opened: 2026-09-25
closed:
verification: inspected
area: [development, integration]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in PyUnitWizard

## What

Review PyUnitWizard's adoption of the MOLI Python developer-tool and support-library
policies under `uibcdf/molsyssuite#6`. Record the two conclusions independently.

## How

Pin pytest-receptor 1.1.0 in the test, development, and release-gate Conda
environments. Select its `ci` profile in every hosted pytest command while retaining
the existing tests, coverage, JUnit report, xdist, and release gates. Use `llm` for
local agent testing. Inspect hosted runs through gh-run-receptor and check the
installed Conda package and command in a native log when needed.

Review SMonitor diagnostics, DepDigest optional-dependency checks, ArgDigest's
optional quantity adapter, and PyUnitWizard's own quantity boundary. Distinguish
tested runtime integration from optional tests skipped by an environment.

## Why

PyUnitWizard is a priority support library in MolSysSuite. Its integration status
cannot be inferred from guide copies or dependency declarations alone. A member-local
issue and evidence are needed before changing the suite inventory.

## What is measured and what is assumed

At filing, all three pytest environments lacked pytest-receptor, and routine CI,
the full matrix, and release gates invoked plain pytest. After the changes,
`PYTHONPATH=. pytest --receptor=llm -q tests` passed locally with 596 passed and
8 skipped. The initial run failed one local-sibling import test because this
temporary checkout's SMonitor sibling was sparse; completing that temporary
clone and repeating the unchanged suite made the test pass. Ruff check and
format, the report-index check, and the MolSysSuite repository checker pass.
Hosted results will be added after validation. No claim is made that all
optional integrations are active in the existing environments.

## What was refuted

Installing pytest-receptor alone would not select the compact CI presentation;
the explicit profile is required in each hosted command.

## Scope and exclusions

This review does not change PyUnitWizard's scientific behavior or resolve unrelated
product issues. It does not redesign the shared MOLI policy.

## Acceptance criteria

- All hosted pytest gates invoke `--receptor=ci` with exact published dependency.
- Local tests and Ruff checks pass; hosted routine CI and selected matrix or release
  gates provide evidence for claimed interpreter support.
- The support-library assessment names exercised paths, skips, and any remaining
  limitation in this issue and the MolSysSuite inventory.

## Dependencies and risks

The full matrix currently has an open failure monitor, `uibcdf/pyunitwizard#77`.
Its cause must be distinguished from the receptor change before claiming complete
developer-tool adoption.
