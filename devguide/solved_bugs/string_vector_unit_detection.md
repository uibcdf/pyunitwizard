---
summary: Classify vector quantity strings without ambiguous array truth values.
issue: uibcdf/pyunitwizard#80
status: resolved
opened: 2026-09-23
closed: 2026-09-23
severity: medium
verification: reproduced
area: [forms, standardization]
guard: tests/forms/test_api_string.py::test_vector_quantity_string_is_not_a_unit_and_standardizes
normative:
blocked_by: []
supersedes: []
---

# Vector quantity strings in unit detection

## What

`puw.standardize("[0, 0, 0] nm")` raises `ValueError: The truth value of an array with more than one element is ambiguous`.

## How

`forms.api_string.is_unit` compares the parsed numeric value with `1` and returns a NumPy boolean array for vector quantities. `standardize` uses that return value as a scalar predicate. The regression test exercises direct unit classification and the consumer's standardization path.

## Why

Six tests constructing spherical interaction sites in `uibcdf/pharmacophoremt#3` fail on this path, blocking the Python policy migration. Unit detection must always return a scalar boolean.

## What is measured and what is assumed

Measured with `python -m pytest --receptor=llm tests/forms/test_api_string.py::test_vector_quantity_string_is_not_a_unit_and_standardizes` and the PharmacophoreMT test suite. The direct vector classification fails before the fix.

## What was refuted

Changing PharmacophoreMT import order restored its API initialization but did not remove this PyUnitWizard failure.

## Scope and exclusions

This defect concerns vector-valued strings. Scalar unit and quantity handling remains covered by existing tests.

## Acceptance criteria

The regression guard passes and returns a scalar `False` for vector quantities; standardization succeeds without an ambiguous array predicate.

## Dependencies and risks

None.

## Resolution

The string-form classifier and the public `is_unit` predicate now reject vector-valued magnitudes with a scalar `False` before comparing them with one. The regression test first failed because string-form detection returned a NumPy array, then exposed the same predicate defect in the public API, and now passes through `standardize`. Its two assertions directly exercise the failure mechanism.

The full local suite passed with pytest-receptor: 537 passed and 7 skipped.
