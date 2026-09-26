---
summary: Array quantities emitted comma-free NumPy text that PyUnitWizard could not parse.
issue: uibcdf/pyunitwizard#81
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: high
verification: reproduced
area: [conversion, serialization]
guard: tests/pint/test_string_array_roundtrip.py::test_pint_string_roundtrip_preserves_numeric_values_and_shape
normative:
blocked_by: []
supersedes: []
---

# Array string form does not round-trip

## What

`convert(array_quantity, to_form="string")` delegated to each backend's display
format. NumPy magnitudes appeared without commas and respected process-wide
print precision, so `quantity(text)` could fail to parse or silently lose
precision.

## How

For array quantities, the conversion layer now emits the magnitude as a
Python nested-list representation and appends the backend's unit text. Scalar
formatting and unit-only conversion keep their prior paths. The parser already
accepts nested-list syntax. The regression covers scalar, 1-D and 2-D
magnitudes, integer and float arrays, a compound unit, and a low NumPy print
precision. Separate checks exercise unyt, Astropy and OpenMM source forms.

## Why

Text that looks like a serialized quantity must be readable by PyUnitWizard
before another component or session can safely use it. A NumPy display string
is not a stable serialization format.

## Acceptance criteria

- Scalar and array quantities round-trip through the string form with the same
  numeric values and array shape.
- Formatting is independent of NumPy's global print precision.
- The text from common non-Pint backends remains parseable by the Pint parser.

## Resolution

`tests/pint/test_string_array_roundtrip.py::test_pint_string_roundtrip_preserves_numeric_values_and_shape`
guards the original failure mechanism and numeric precision. String form does
not encode NumPy dtype; use QuantityRecord when exact dtype matters.
