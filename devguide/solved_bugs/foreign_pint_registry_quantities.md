---
summary: Pint quantities from another UnitRegistry were misclassified and could not enter the shared kernel.
issue: uibcdf/pyunitwizard#84
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: high
verification: reproduced
area: [forms, conversion]
guard: tests/pint/test_foreign_registry.py::test_foreign_pint_quantity_is_recognized_and_rebuilt_in_kernel_registry
normative:
blocked_by: []
supersedes: []
---

# Foreign Pint registry quantities

## What

A quantity created by another Pint `UnitRegistry` reported form `pint`, but
`is_quantity()` returned false because the adapter compared concrete types.
`convert(..., to_form="pint")` then returned the foreign object unchanged, so
ordinary arithmetic with PyUnitWizard's quantities failed across registries.

## How

The adapter now recognizes Pint quantities and units with `isinstance`.
`convert()` rebuilds a foreign Pint object in PyUnitWizard's registry before
same-form fast paths. It compares dimensionality, named base units, zero-point
offset and unit scale at relative tolerance `1e-12`; unknown or different
definitions raise `ValueError`. Tests cover classification, same-form and
unit-changing conversion, arithmetic, a changed unit definition, and an
affine temperature unit.

## Why

External libraries commonly create their own Pint registries. Silently
treating their quantities as bare values or returning them unchanged defeats
the shared unit kernel's interoperability contract.

## Acceptance criteria

- `is_quantity()` accepts a foreign Pint quantity and `is_unit()` accepts its
  unit.
- `convert()` returns an object in PyUnitWizard's registry, even when the
  requested form is already `pint` or is omitted.
- Differently defined units are rejected; compatible affine units retain
  their offsets.

## Resolution

`tests/pint/test_foreign_registry.py::test_foreign_pint_quantity_is_recognized_and_rebuilt_in_kernel_registry`
guards classification and registry normalization. The two neighboring tests
guard rejection of different definitions and affine conversion.
