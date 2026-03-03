# Configuration

`puw.configure` defines runtime behavior. Treat it as application/library
configuration, not as per-call business logic.

A reliable integration starts with one centralized initialization path. That
single decision removes a large amount of hidden runtime drift.

## Core controls

- `load_library(...)`: register backend adapters.
- `set_default_form(...)`: define canonical output form.
- `set_default_parser(...)`: define parser for string inputs.
- `set_standard_units(...)`: define normalization targets.
- `reset()`: clear mutable configuration (useful in tests).

## Recommended baseline

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])
```

## Read-back checks

```python
print(puw.configure.get_libraries_loaded())
print(puw.configure.get_default_form())
print(puw.configure.get_default_parser())
print(puw.configure.get_standard_units())
```

Use these checks in CI tests to ensure deterministic setup.

## Operational guidance

- Keep one canonical initialization path in your package.
- Do not reconfigure inside computational functions.
- In tests, call `reset()` before scenario-specific setup.
- If you support multiple backends, define one canonical production backend
  first, then expand with explicit cross-backend tests.

For backend-specific expectations, continue with
[Backend Coverage and Expectations](backend-coverage.md).
