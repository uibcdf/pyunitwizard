# Temporal Instabilities and Needed Improvements (March 2026)

This document details the instabilities detected during the 1.0.0 stabilization sprint and provides a technical roadmap for performance optimizations.

## 1. Detected Instabilities

### 1.1 RecursionError in Astropy Integration
A critical `RecursionError: maximum recursion depth exceeded` has been detected in the `main` branch, specifically affecting `tests/astropy_units/test_astropy_units.py`.
- **Symptom**: When comparing an Astropy Quantity with `pytest.approx`, the system enters an infinite loop.
- **Context**: This appears more frequently in Python 3.13 environments.
- **Hypothesis**: The interaction between `pyunitwizard` introspection and Astropy's `__array_function__` protocol might be triggering circular calls when `numpy.isscalar` or `asarray` is invoked during testing.

### 1.2 Cross-Backend Matrix Failures
Several tests in `tests/integration/test_frontend_cross_backend_matrix.py` are failing with `UnitConversionError`.
- **Issue**: Converting between `astropy.units` and other backends (like `pint` or `unyt`) sometimes fails to resolve "absement" (m·s) or other compound dimensions.
- **Status**: These failures persist even after reverting all performance optimizations, indicating a pre-existing fragility in the inter-library translation logic.

### 1.3 Registry Dispatch Fragility
The use of dynamic dictionaries (`dict_is_form`, `dict_convert`, etc.) is powerful but highly sensitive to the order of library loading. Manual attempts to bypass these lookups often result in `KeyError: None` or returning raw strings where the API expects quantity objects.

---

## 2. Performance Roadmap (Proposed & Reverted Improvements)

The following strategies were implemented and subsequently reverted to ensure 1.0.0 stability. They should be revisited with stricter safety guards.

### 2.1 Fast Form Introspection (High Priority)
The current `get_form()` performs a linear search across all loaded libraries.
- **Proposed Optimization**: Use a `_TYPE_TO_FORM_CACHE: Dict[type, str]` mapping.
- **The Catch**: Must exclude `str` type from caching and ensure that class name detection (e.g., checking if "pint" is in the type name string) doesn't fail when libraries are reloaded or shadowed.

### 2.2 Conversion Fast Path
Avoiding backend calls when the input is already in the target form.
- **Proposed Logic**: If `to_unit` is None and `form_in == to_form`, return the object immediately.
- **The Catch**: This MUST NOT trigger for strings. Strings must always pass through a parser to become objects. Failing to do so results in downstream `AttributeError` (e.g., `'1.0 meter' has no attribute 'unit'`).

### 2.3 Unit String Caching
Parsing strings like `'nanometers'` is the most expensive operation in construction.
- **Proposed Optimization**: A global `_UNIT_STRING_CACHE: Dict[Tuple[str, form, parser], UnitObject]`.
- **Impact**: This would provide near-zero latency for repeated unit creation in MolSysMT loops.

### 2.4 Pre-calculated Standard Matrices
The `standardize()` function currently rebuilds the dimensionality matrix for least-squares solving on every call.
- **Proposed Optimization**: Store `dimensional_fundamental_standards_matrix` and its corresponding `units` list in the `kernel` upon calling `set_standard_units()`.
- **Status**: This is the most stable mathematical optimization. It avoids thousands of `convert()` and `get_dimensionality()` calls during a simulation trajectory normalization.

---

## 3. Mathematical & Numba Potential

### 3.1 Is Numba Necessary?
Analysis of `_standard_units_lstsq` suggests that the systems of equations are too small ($7 \times N$) for Numba's JIT overhead to be worthwhile.
- **Verdict**: Focus on **avoiding matrix construction** (caching) rather than accelerating the `lstsq` call itself. The linear algebra cost is negligible compared to the object-creation cost of the units.

### 3.2 Dimensionality Caching
Dimension extraction (`get_dimensionality`) is deterministic and immutable for a given unit.
- **Strategy**: Cache the resulting dictionary using the unit's string representation as a key. This will speed up `puw.check()` calls used extensively in MolSysMT argument digestion.

---

## 4. Offloading Strategy: Making Host Libraries Lighter

To reduce the performance impact of `pyunitwizard` on large-scale processing (like MolSysMT), we propose an "Offloading at the Edge" strategy:

### 4.1 Decorator-Level Normalization
Utilize `argdigest` pipelines (`sci:to_float64_array`) to perform `standardize()` and `get_value()` only once at the function entry point.
- **Goal**: Host library internal "Kernels" should receive raw NumPy arrays in standardized units (e.g., nm, ps, K).
- **Benefit**: This eliminates the need for any `pyunitwizard` calls inside the computational loops, rendering the library's internal latency irrelevant for the most heavy tasks.

### 4.2 Zero-Quantity Kernels
Encourage a design where `Quantity` objects are "Border Citizens". They exist at the API level for user convenience but are stripped away before reaching the Numba/JIT layers.

---

## 5. Conclusion for 1.0.0
Due to the proximity of the 1.0.0 release, **correctness takes precedence over speed**. All experimental optimizations have been reverted. Future work must address the `RecursionError` in the test suite before re-introducing any caching mechanisms.
