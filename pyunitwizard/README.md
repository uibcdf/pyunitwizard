# PyUnitWizard package contributor guide

This document gives human contributors a tour of the public package layout and explains how to make changes safely.

## Package overview

Importing `pyunitwizard` triggers `pyunitwizard.__init__`, which:
1. Boots the runtime by calling `kernel.initialize()` to zero out all module-level state.
2. Defers backend discovery and adapter loading until a form or external quantity first requires it.
3. Lazily re-exports the user-facing helpers from `api/` plus configuration utilities from `configure`, so most consumers only need `import pyunitwizard as puw`.
4. Registers `pyunitwizard.main` as a compatibility module for legacy imports.

Because initialization happens at import time, edits to any of the modules below must preserve idempotence and backward compatibility.

The default form follows the first backend request. The default parser stays
unset until a parser-capable backend is loaded; loading OpenMM or another
non-parser backend first must not prevent a later Pint request from parsing
strings. Explicit parser choices remain unchanged by subsequent backend loads.

## Layout highlights

- `api/` — Home of the top-level quantity/unit helpers (`convert`, `get_value`, `is_quantity`, etc.) grouped by concern (`conversion`, `construction`, `introspection`, `comparison`, etc.). Touch these modules when you add or modify high-level operations exposed to users.
- `__init__.py` — Lazy public re-export surface and import-time initialization (kernel bootstrap and `pyunitwizard.main` compatibility module).
- `parse.py` — Implements `parse()` and related helpers for string-to-quantity conversion. Use this module for parser-specific behavior. Keep changes in sync with the translation tables in `forms` when you add new representations.
- `kernel.py` — Defines `initialize()` and stores global registries (`loaded_libraries`, defaults, and dimensional standards). Only adjust it when you need to change how the runtime state is structured or reset.
- `configure/` — Hosts configuration utilities that manage the kernel (`load_library`, defaults setters/getters, standard unit helpers). Reach for this package when wiring new unit systems, customizing defaults, or resetting state for tests.
- Other packages:
  - `forms/` and `_private/` contain translation logic and implementation details used by the public modules.
  - `constants/` exposes physical constants and aliases.
  - `utils/` groups developer-facing helpers (I/O, conversions, and convenience routines).

Refer to `AGENTS.md` in the repository root for project-wide guidelines, and `pyunitwizard/AGENTS.md` for package-specific rules.

## Inert citation metadata

The package exposes offline software citation metadata without importing a
citation observer or unit backends. Ordinary scientific functions retain their
original callables and signatures. The bounded development pilot, tested lazy
activation and pending protocol review are documented in
`devguide/completed_proposals/function_citation_provider.md` (uibcdf/pyunitwizard#94).

## When to edit each module

- Start in `api/` if you are adding or adjusting APIs that users call directly. Keep signatures stable, introduce keyword-only parameters for new options, and backfill docstrings.
- Modify `configure/configure.py` when you need to change default library loading order, support a new library, or expose additional configuration helpers.
- Extend `parse.py` when parsing rules or grammar need to evolve. Add targeted tests that cover both string input and the resulting quantity form.
- Update `kernel.py` only when the core lifecycle or stored registries change. Ensure imports of `pyunitwizard` remain safe even if optional dependencies are missing.

## Testing expectations

- Run `python -m pytest tests` after modifying any of the public modules above.
- Add regression tests for any change in default behavior (e.g., different default form, new lazily loaded library, new parsing branch).
- When adjusting import-time side effects, include tests that exercise a fresh interpreter state (for example by using `importlib.reload`).
- Document user-visible changes in this README and the repository-level changelog or release notes as appropriate.

## Canonical-unit fast paths

`has_unit()` is the metadata-only exact-unit predicate used by `check(unit=...)`,
`convert()`, `standardize()`, `ensure_quantity()`, and registered `fast_track`
normalizers. When the input already has the requested canonical unit and output
form, these APIs preserve the original quantity object instead of extracting or
converting its magnitude. Requests that change backend form still use the full
conversion path.

Fast-track registration is idempotent: registering an existing name for the
same exact unit keeps the original normalizer. Reusing that name for a different
unit raises a catalog-backed `FastTrackConflictError` instead of silently
replacing process-global behavior.

## Quantities from another Pint registry

`is_quantity()` accepts Pint quantities from any `UnitRegistry`. `convert()`
rebuilds a foreign quantity or unit in PyUnitWizard's Pint registry before any
same-form fast path or translation. It compares named base units, dimensions,
scale and affine offset with relative tolerance `1e-12`; missing or different
definitions raise `ValueError`. This permits ordinary arithmetic with
PyUnitWizard-created Pint quantities after conversion.

## Stated scalar uncertainty

`pyunitwizard.measurement.MeasurementRecord` is a provisional inert envelope
for a scalar value and its source-stated SD, SEM, unspecified ± half-width or
confidence interval. It binds the association and optional level/replicate count
to a QuantityRecordBundle under `qrec-measurement/0.1`, preserving existing
record formats. It performs no statistical inference or uncertainty arithmetic.
Reader expectations and affine difference-unit conversion are tested in
`tests/test_measurement_record.py`. Importing the module loads no unit backend.

## Array string form

When `convert(..., to_form="string")` receives an array quantity, the API
formats its magnitude as a nested Python list before appending the source
backend's unit text. This avoids NumPy's comma-free display and honors full
numeric precision independently of global NumPy print options. Parsing the
string preserves the values and shape; the inert `record` form carries dtype
metadata when exact dtype preservation is required.


## Optional attribution development pilot

Inside explicit `with puw.attribution():` blocks, when the Ackredit development
provider is available, completed dispatched Pint and unyt construction, conversion and translation operations contribute software
references to the application's current session. unyt also contributes its JOSS
description article. Versions identify the actual executed software; loading an
adapter alone earns no credit. The provider is loaded lazily after execution;
absence preserves values and units, and provider failures emit a catalog warning.

This bounded source pilot is tracked in uibcdf/pyunitwizard#92 and
uibcdf/ackredit#75. It does not cover every adapter/internal call, claim complete
transitive attribution, change QuantityRecord, or establish a published optional
installation. Applications may pair the provisional Ackredit capture payload
with a QuantityRecord; reading those saved records does not credit a new calculation.


```python
import pyunitwizard as puw

with puw.attribution():
    quantity = puw.quantity(2.0, "meter", form="pint")
    result = puw.convert(quantity, to_unit="centimeter")
```

`attribution()` is provisional. It is context-local and nests without replacing
the application's Ackredit session. Ordinary conversions outside it do not load
the provider or pay active tracking cost. Scientific exceptions propagate and
the enclosing choice is restored on exit.
