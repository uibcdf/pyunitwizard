# Utilities package guidelines

This file defines expectations for contributors working in `pyunitwizard.utils` and any of its subpackages.

## Quantity-preserving helpers
- Utility helpers must never drop unit metadata. Functions that return numeric values must wrap them with `pyunitwizard.quantity` unless explicitly documented as returning raw values.
- When normalizing sequences, preserve the original ordering and dimensionality so the helper can round-trip the original quantity when `standardized=False`.
- Avoid mutating user-supplied quantities in place. Create derived data structures using `get_value` / `quantity` instead.

## Unit conversion controls (`to_unit` / `to_form`)
- Every helper that can emit new quantities must accept `to_unit` and `to_form` keyword arguments mirroring the behavior of the core API. Defaults should match the source quantity if the argument is omitted.
- Never infer incompatible units. When `to_unit` is `None`, infer the unit from the first quantity in the input collection and validate the remainder for dimensional consistency.
- Propagate `standardized` flags when creating new quantities so downstream code can opt into canonical representations.

## Error handling
- Raise explicit `ValueError` or domain-specific exceptions when encountering unsupported `value_type` options or inconsistent dimensionality. Do not silently coerce or drop invalid entries.
- Include the invalid option or summary of the inconsistent input in the error message to aid debugging.
- Prefer early validation before performing array operations so failures occur before heavy computation.

## Documentation and tests
- Update `README.md` in this directory when adding or substantially changing helper behavior.
- Add or update unit tests under `tests/utils` to cover new helpers, especially conversions between value types and unit consistency checks.
