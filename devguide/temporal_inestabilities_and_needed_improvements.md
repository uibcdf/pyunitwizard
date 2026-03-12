# Temporal Instabilities and Needed Improvements (March 2026)

This document records the instabilities detected during the pre-1.0 stabilization work, what was confirmed as real, what has already been corrected, and which optimization ideas remain optional future work.

## 1. Current Status

The critical instabilities originally motivating this document have now been addressed in `main`.

Resolved recently:

- Astropy recursion in `get_value()` and `pytest.approx` comparisons.
- String conversion fast paths that incorrectly returned raw strings without parsing.
- Standardization matrix prebuild placement and reset hygiene.
- Introspection type-to-form cache cleanup on `configure.reset()`.

As of the latest validation pass, these relevant blocks are green:

- `tests/astropy_units`
- `tests/integration`
- `tests/forms`
- `tests/utils`
- `tests/test_get.py`
- `tests/test_parse.py`
- `tests/test_conversion_branches.py`
- `tests/test_configure.py`
- `tests/test_standardize.py`
- `tests/test_check.py`
- `tests/test_get_form.py`
- `tests/test_introspection_probe.py`

## 2. Confirmed Instabilities and Resolution

### 2.1 Astropy `RecursionError`

This was a real bug, not just a test artifact.

- **Root cause**: `astropy.units.Quantity` is a subclass of `numpy.ndarray`.
- **Faulty behavior**: `pyunitwizard.api.extraction.get_value()` had a fast path using `isinstance(quantity, np.ndarray)`.
- **Effect**: Astropy quantities were returned as raw quantity objects instead of numeric values, and downstream NumPy / `pytest.approx` logic entered recursive scalar probing.

Resolution:

- The fast path now only accepts plain `numpy.ndarray` objects, not arbitrary subclasses.
- Regression coverage was added in `tests/test_get.py`.

### 2.2 String Fast-Path Fragility in `convert()`

This was also a real bug.

- **Faulty behavior**: `convert("1 meter")` or `convert("1 meter", parser="pint")` could return the original string unchanged when no explicit target form was requested.
- **Effect**: downstream code could receive a raw string where a parsed quantity was expected.

Resolution:

- Conversion fast paths no longer apply to inputs with `form_in == "string"`.
- Regression coverage was added in `tests/test_conversion_branches.py`.

### 2.3 Parser Resolution / Parse Cache Fragility

This was a real state-dependent issue.

- **Faulty behavior**: `parse()` was cached while still depending on runtime parser resolution.
- **Effect**: parsing behavior could drift depending on the active default parser, especially in mixed `pint` / `astropy.units` contexts.
- **Observed symptom**: array-like quantity strings such as `"[2, 5, 7] joules"` could break when the active parser path reached Astropy parsing.

Resolution:

- Effective parser resolution now happens before the cached parsing function.
- Array-like strings preferentially use Pint parsing when appropriate.
- Regression coverage was added in `tests/test_parse.py`.

### 2.4 Standardization Matrix Rebuild Overhead

The optimization idea was valid, but the first local implementation was not placed correctly.

- **Original issue**: `get_standard_units()` rebuilt least-squares matrices repeatedly.
- **Initial flawed implementation**: matrix prebuild was inserted inside an inner loop in `set_standard_units()`.

Resolution:

- Kernel-level prebuilt matrices and unit lists are now generated once, after standard-unit configuration has been fully assembled.
- `configure.reset()` also clears those caches.
- Regression coverage was added in `tests/test_configure.py`.

### 2.5 Introspection Cache Hygiene

This was not a major runtime bug, but it was a real hygiene issue.

- **Issue**: `_TYPE_TO_FORM_CACHE` in `pyunitwizard.api.introspection` survived `configure.reset()`.
- **Effect**: type-to-form state could persist across test/runtime resets unnecessarily.

Resolution:

- `configure.reset()` now clears `_TYPE_TO_FORM_CACHE`.
- Regression coverage was added in `tests/test_get_form.py`.

## 3. What Is No Longer an Active Instability

The following points should no longer be treated as active release blockers:

- `RecursionError` in Astropy integration.
- Cross-backend frontend matrix instability as an active failure mode.
- String fast-path misbehavior in `convert()`.
- Standardization matrix rebuild cost as an unaddressed issue.

These topics remain useful as historical context, but not as open blockers for 1.0 stabilization.

## 4. Optional Optimization Work Still Open

The following ideas remain reasonable, but they are now optional optimization or architecture work, not urgent stabilization fixes.

### 4.1 Unit String Caching

Potential direction:

- cache parsed unit objects keyed by a stable tuple such as `(unit_string, parser, target_form)`.

Current status:

- not implemented.
- should only be introduced with explicit regression tests and a benchmark showing repeated parser cost matters.

Assessment:

- useful candidate for heavy repeated construction workloads;
- not necessary before 1.0 without measurement.

### 4.2 Dimensionality Caching

Potential direction:

- cache dimensionality dictionaries for normalized unit identities or canonical string forms.

Current status:

- not implemented.

Assessment:

- likely useful in validation-heavy or argument-digestion-heavy workflows;
- should not be added before 1.0 without careful key normalization and benchmark evidence.

### 4.3 Further Introspection Hardening

Potential direction:

- review whether `_TYPE_TO_FORM_CACHE` should cache `str`,
- review whether Astropy fast detection should be made explicit rather than relying solely on dispatch lookup,
- review whether cache invalidation needs anything beyond `configure.reset()`.

Current status:

- no active bug remains here after reset cleanup.

Assessment:

- reasonable hardening work;
- not urgent.

## 5. Architecture Direction for Host Libraries

The offloading strategy remains valid and important, but it belongs to ecosystem integration strategy rather than PyUnitWizard core stabilization.

Recommended direction:

- perform `standardize()` and `get_value()` at API boundaries in host libraries;
- pass plain arrays in canonical units into inner computational kernels;
- keep quantity objects at the integration edge, not in hot loops.

This is especially aligned with coordinated use alongside:

- `argdigest`
- `depdigest`
- `smonitor`

## 6. Practical Conclusion

The urgent instability work tracked by this document is now largely complete.

What remains before 1.0 in this area is no longer emergency hardening, but disciplined optional work:

- benchmark-driven caching only where it clearly helps,
- continued architectural cleanup,
- host-library integration guidance at the ecosystem boundary.
