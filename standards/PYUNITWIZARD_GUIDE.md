# PyUnitWizard Guide (Canonical)

Source of truth for integrating and using **PyUnitWizard** in this library.

Metadata
- Source repository: `pyunitwizard`
- Source document: `standards/PYUNITWIZARD_GUIDE.md`
- Source version: `pyunitwizard@1.0.0`
- Last synced: 2026-02-06

## What is PyUnitWizard

PyUnitWizard is a "Quantities and Units Assistant" designed to provide a unified API over multiple Python unit backends. It allows libraries to work with physical quantities regardless of their internal representation (`pint`, `unyt`, `openmm.unit`, `astropy.units`, or `string`).

## Why this matters in this library

- **Interoperability**: Allows this library to accept and return quantities in any format chosen by the user.
- **Consistency**: Centralizes unit conversion, standardization, and validation logic.
- **Transparency**: Integrates with `smonitor` to provide traceable unit operations.

## Dependency Management

PyUnitWizard follows a strict separation between Hard and Soft dependencies:

- **Hard Dependencies**: `numpy` and `pint`. These are always available.
- **Soft Dependencies**: `unyt`, `openmm.unit`, `astropy.units`. These are optional and managed via `depdigest`.

## Minimum initialization (recommended)

Libraries using PyUnitWizard should configure it upon import to define their preferred standards:

```python
import pyunitwizard as puw

# Load required backends
puw.configure.load_library(['pint', 'openmm.unit'])

# Set default form for outputs
puw.configure.set_default_form('pint')

# Define standard units for the project
puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole', 'K'])
```

## Essential API for Developers

### 1. Construction
Always use the factory functions to ensure consistent behavior:
```python
q = puw.quantity(10.0, 'nm')
u = puw.unit('angstroms')
```

### 2. Extraction & Coercion
Avoid manual attribute access (e.g., `.value` or `.unit`). Use the API instead:
```python
val = puw.get_value(q, to_unit='angstroms')
unit = puw.get_unit(q)
```

### 3. Conversion & Standardization
Bridge between different formats effortlessly:
```python
# Convert to a specific form and unit
q_openmm = puw.convert(q, to_unit='nm', to_form='openmm.unit')

# Standardize to the project's canonical units
q_std = puw.standardize(q)
```

### 4. Validation
Verify inputs without worrying about the underlying backend:
```python
if not puw.check(q, dimensionality={'[L]': 1}):
    raise ValueError("Expected a length quantity")
```

## SMonitor Integration

PyUnitWizard is instrumented with `@smonitor.signal`. All major unit operations (conversion, standardization, validation) appear in the diagnostic breadcrumb trail.

**Conventions:**
- **Tags**: Functions use tags like `['conversion']`, `['standardization']`, `['validation']`.
- **Errors**: Unit mismatch errors are emitted through the SMonitor catalog.

## Required behavior (non-negotiable)

1.  **Lazy Backend Checks**: Do not assume optional backends are installed. Use `puw.is_quantity()` or catch `LibraryNotFoundError`.
2.  **No Direct Backend Imports**: Avoid importing `pint` or `unyt` directly in your scientific logic. Rely on the `puw` API.
3.  **Use Contexts for Tests**: When testing unit-sensitive code, use `puw.context` to ensure a deterministic environment.

```python
with puw.context(default_form='pint', standard_units=['nm', 'ps']):
    # Test logic here...
    ...
```

## Naming conventions

- **Form names**: Use canonical strings (`'pint'`, `'unyt'`, `'openmm.unit'`, `'astropy.units'`, `'string'`).
- **Dimensionality**: Use standard notation (`'[L]'`, `'[M]'`, `'[T]'`, etc.).

---
*Document created on February 6, 2026, as the authority for PyUnitWizard integration.*
