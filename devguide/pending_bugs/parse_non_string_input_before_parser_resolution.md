---
summary: Validate non-string parse input before parser resolution.
issue: uibcdf/pyunitwizard#79
status: active
opened: 2026-09-22
closed:
severity: high
verification: reproduced
area: [api, parsing, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Validate parse input before parser resolution

## What

With Pint loaded, `parse(3.0, to_form="string")` raises an internal
`AttributeError` from `_resolve_parser` rather than PyUnitWizard's
`ArgumentError`. The public function promises string input and an existing
test expected the domain exception, but the test's result depended on the
loaded parser state.

## How

`parse` currently resolves the output form and parser before checking the
type of `string`. The type check is inside `_parse_cached`, too late for the
`_resolve_parser` branch that calls `string.startswith`. Validate at the
public boundary before either resolver runs. Keep the private cached check
as a defensive guard for internal callers.

## Why

This is a public error-contract defect and a release-gate blocker. A
Python 3.12 hosted matrix cell failed while the same test sometimes passed
under different test ordering. The generic scheduled monitor
`uibcdf/pyunitwizard#77` is not a durable defect record.

## What is measured and what is assumed

- Hosted full-matrix run `35714401355` at `45cc18a` failed
  `tests/test_parse.py::test_parse_rejects_non_string_input` in
  Ubuntu/Python 3.12 with `AttributeError: 'float' object has no attribute
  'startswith'` at `pyunitwizard/parse.py:79`.
- Strengthening the existing test to load Pint and request `to_form="string"`
  reproduced the same failure locally on Python 3.13 with
  `python -m pytest --receptor=llm -q
  tests/test_parse.py::test_parse_rejects_non_string_input`.
- The same validation-order defect is expected on any Python version where
  the resolver reaches that branch; this is an inference from the code path,
  not a separately measured interpreter matrix.

## What was refuted

This is not a Python 3.14-specific incompatibility: the deterministic
reproduction fails locally under Python 3.13.

## Scope and exclusions

Fix the argument boundary and regression guard. Do not change valid string
parsing, parser selection, output forms, or the generic CI monitor lifecycle.

## Acceptance criteria

- Invalid non-string input raises `ArgumentError` before parser resolution,
  including when Pint is loaded and the requested output is `string`.
- Valid parsing tests and the full supported-platform matrix pass.
- The report closes with the deterministic test selector as its guard.

## Dependencies and risks

This blocks the final exact-commit full matrix and 0.26.0 publication.
