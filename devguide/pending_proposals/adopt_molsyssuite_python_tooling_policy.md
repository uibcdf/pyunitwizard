---
summary: Adopt the shared Python and Ruff development baseline.
issue: uibcdf/pyunitwizard#74
status: active
opened: 2026-09-12
closed:
verification: measured
area: [tooling, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Adopt the MolSysSuite Python tooling policy

## What

Align PyUnitWizard with the Python-library contract governed by
`uibcdf/molsyssuite#6`: Python `>=3.11,<3.14`, Python 3.13 for development,
and Ruff as formatter, import sorter, and linter with the common `E4`, `E7`,
`E9`, `F`, and `I` baseline.

## How

Configure Ruff in `pyproject.toml`, exclude synchronized root guides from host
formatting, add the suite-tested Ruff release to the development environment, replace
the active flake8 configuration, and invoke the reusable MolSysSuite conformance
workflow. Type checking remains repository-local and is not made a shared gate.

## Why

PyUnitWizard is one of the six wave-1 libraries being stabilized first. A shared quality
surface makes changes across its many MolSysSuite consumers easier to maintain while
leaving runtime argument validation and unit semantics under their proper contracts.

## Evidence

The policy 1.0 checker on 2026-09-12 reported `RUFF_CONFIG`,
`VENDORED_GUIDE_RUFF`, `RUFF_CI`, and active `flake8` configuration. The declared
Python range is already semantically correct.

## Acceptance criteria

- The central conformance checker reports no findings.
- Ruff lint and format checks pass with the suite-tested release.
- The PyUnitWizard test suite passes.
- The local issue and this record close together after the guard is published.

