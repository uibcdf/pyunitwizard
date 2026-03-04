# Minimum Quantity Protocol Contract (Pre-1.0)

This document defines the minimum interoperability contract that PyUnitWizard
guarantees before `1.0.0`.

## Purpose

Provide a stable, backend-agnostic baseline so integrators can rely on core
quantity behavior without depending on backend internals.

## Mandatory capabilities

A quantity handled by PyUnitWizard must support, through public API:

1. Value extraction
- `get_value(quantity_like, ...)`

2. Unit extraction
- `get_unit(quantity_like, ...)`

3. Dimensional compatibility checks
- `are_compatible(a, b)`
- `check(quantity_like, dimensionality=...)`

4. Unit conversion
- `convert(quantity_like, to_unit=..., ...)`

5. Backend form introspection
- `get_form(quantity_like)`

## Behavioral guarantees

1. Determinism
- Given the same configuration (`libraries`, default parser/form, standard
  units), results are deterministic.

2. Explicit failure
- Incompatible dimensional operations must fail with explicit exceptions.
- Unsupported parser/backend routes must fail explicitly (no silent fallback).

3. No silent unit stripping in core API
- Core API calls must preserve or transform units explicitly; they must not
  discard units silently.

4. Unit-string robustness across parsers
- `to_unit` accepts canonical unit strings (for example, `"meter"`) even when
  the active parser requires quantity-like strings internally.

## Out of scope for this minimum contract

- Full parity of semantics across all backend-native edge cases.
- Implicit parser inference beyond configured/explicit parser policy.
- Advanced protocol extensions (array broadcasting semantics, serialization
  schema, dataframe/plotting behavior details).

Those belong to separate contracts and extension guides.

## Evidence requirement before `1.0.0`

- Contract tests exist and are green for supported runtime backends.
- Known deviations are documented with explicit scope.
- Current contract evidence module:
  - `tests/test_minimum_quantity_protocol_contract.py`
  - `tests/test_conversion_branches.py` (unit-string conversion regression path)
