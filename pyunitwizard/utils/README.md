# `pyunitwizard.utils`

The utilities package collects helper functions that operate on PyUnitWizard quantities without exposing the internals of the kernel. Each subpackage focuses on a specific integration surface:

- `numpy` – array-like helpers that wrap NumPy stacking and repetition utilities while preserving quantity metadata.
- `pandas` – tabular helpers to move quantities into/out of DataFrames without losing unit metadata.
- `sequences` – light-weight tools for validating and manipulating Python sequences of quantities.
- `matplotlib` (placeholder) – reserved for plotting adapters that inject unit-aware axes helpers.
- `plot` (placeholder) – shared plotting shortcuts that will reuse the `matplotlib` integration when implemented.

When you add a new helper, follow these principles:

1. **Preserve quantity semantics.** Extract raw values with `get_value`, but always return new data with `quantity(...)` so unit metadata survives the transformation.
2. **Expose conversion controls.** Accept `to_unit`, `to_form`, and `standardized` keyword arguments when a helper produces new quantities. Omitted arguments must default to the input unit/form.
3. **Validate aggressively.** Detect incompatible units and unsupported options early, and raise informative `ValueError` instances instead of coercing silently.
4. **Document and test.** Extend this README and add regression coverage under `tests/utils` whenever you change observable behavior.

## Adding new helpers

1. Pick a subpackage that matches the domain (e.g., numerical arrays belong in `numpy`). Create a new module or extend an existing one.
2. Mirror the import pattern used elsewhere (`from pyunitwizard import quantity, get_value, get_unit`). This keeps unit conversion logic consistent with the public API.
3. Implement value-type handling (`value_type='tuple'`, `'list'`, `'numpy.ndarray'`, etc.) by converting the processed values just before calling `quantity`. Reject unsupported options explicitly.
4. Write unit tests that verify:
   - Units are inferred from inputs when `to_unit` is omitted.
   - Passing `to_unit` / `to_form` returns quantities converted to the desired representation.
   - Every supported `value_type` produces the expected Python/Numpy container and that invalid values raise.
5. Update this README with any new options or behaviors so future contributors can follow the established contract.

## Subpackage notes

### `utils.numpy`

Array helpers accept iterables of quantities and expose a `value_type` parameter controlling the container of the resulting values. Current functions support `'tuple'`, `'list'`, and `'numpy.ndarray'`. Defaults should mirror existing modules (`'tuple'` today) and may be extended with explicit documentation.

Unit inference relies on the first quantity in the first sequence argument. Validate remaining entries with `get_unit` (or by converting via `get_value(..., to_unit=output_unit)`) to guarantee consistent dimensions before stacking. Tests must cover:

- Successful stacking with homogeneous units and multiple `value_type` choices.
- Conversion when `to_unit` or `to_form` is provided.
- Failure cases for mismatched units or unsupported `value_type` values.

Transparent NumPy mode is available through:
- `setup_numpy(enable=True)` to patch selected NumPy calls (`np.mean`, `np.sum`,
  `np.std`, `np.var`, `np.dot`, `np.linalg.norm`, `np.trapezoid`) so quantity inputs dispatch through
  PyUnitWizard wrappers.
- `numpy_context()` for temporary patching in a context manager.

### `utils.sequences`

Sequence utilities provide validation helpers (e.g., `is_sequence`, `is_quantity_value_sequence`) and slice/concatenate operations that should preserve quantity ordering. When building new helpers:

- Accept iterables of quantities or raw values but document the expected input clearly.
- Infer default units from the first quantity when emitting new quantities, mirroring the pattern used in the NumPy helpers.
- Cover edge cases such as empty inputs, nested lists, and mixing quantity/value types with targeted tests under `tests/utils/sequences` (create the directory if missing).

Required tests should confirm:

- Detection of valid vs. invalid sequences.
- Correct propagation of `to_unit`, `to_form`, and `standardized` flags for helpers that produce quantities.
- Informative errors when encountering unsupported operations or inconsistent dimensionality.

### `utils.pandas`

Pandas interoperability is implemented as an additive layer:

- `dataframe_from_quantities(...)` builds a numeric `DataFrame` and stores per-column units in `DataFrame.attrs["pyunitwizard_units"]`.
- `add_quantity_column(...)` appends/updates one column from a quantity and keeps unit metadata synchronized.
- `get_quantity_column(...)` reconstructs a quantity from a DataFrame column using metadata or an explicit `unit_name`.
- `get_units_map(...)` returns the units metadata dictionary.
- `set_units_map(...)` injects/replaces units metadata with validation.
- `sync_units_map(...)` drops stale metadata keys not present in columns.
- `concat(...)` and `merge(...)` preserve and validate units metadata across table operations.
- `setup_pandas(enable=True)` injects an optional transparent accessor (`DataFrame.puw`).
- `pandas_context()` enables that accessor only inside a context manager.

These helpers keep standard pandas imports/workflows intact (`import pandas as pd`) and allow either explicit boundary calls or transparent `df.puw.*` usage.
