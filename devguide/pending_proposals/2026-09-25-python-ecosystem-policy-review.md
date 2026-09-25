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
No claim is made that all optional integrations are active in the existing
environments.

Routine CI `36102753740` passed at source commit `c8cd856`, with 622 passed and
5 skipped. Its native log confirms the exact `uibcdf` Conda package
`pytest-receptor 1.1.0 py_1` and the `--receptor=ci` command. The policy run
`36102754343`, release gates `36102768017`, and the eight-cell full matrix
`36102767731` passed; the release gates include the full test suite on Python
3.11 through 3.14. All four were first inspected with gh-run-receptor.

For the support-library review, SMonitor is a runtime dependency used for
diagnostic signals and covered by catalog and error-path tests. DepDigest is a
runtime dependency used for optional backend availability, with declaration
and integration tests. PyUnitWizard owns the physical-quantity conversion and
dimensional checks. ArgDigest's PyUnitWizard adapter has six passing local
ecosystem smoke and collective error-path tests, but the hosted Conda test
environments do not install ArgDigest, so these optional tests cannot establish published
integration on all claimed Python minors. The public API also has native
nontrivial argument checks; the issue must decide where ArgDigest is applicable
without creating an unnecessary library cycle before the support-library
review can be called complete.

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
