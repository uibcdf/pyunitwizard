# Forms and adapters overview

This directory documents how form adapters integrate with the dispatchers in `pyunitwizard.forms` and what each implementation currently supports.

## Existing adapters

### `api_pint.py`
- Boots a dedicated `pint.UnitRegistry` and exposes helpers for identifying quantities, units, dimensionality, and compatibility checks (`is_quantity`, `is_unit`, `dimensionality`, `compatibility`).【F:pyunitwizard/forms/api_pint.py†L13-L119】
- Provides quantity construction, value/unit accessors, conversion helpers, and a parser that maps strings into Pint quantities (`parser = True`).【F:pyunitwizard/forms/api_pint.py†L120-L213】
- Implements translators to other forms, including string serialization plus conversions to OpenMM, Unyt, and Astropy backends following the `quantity_to_<target>`/`unit_to_<target>` naming convention.【F:pyunitwizard/forms/api_pint.py†L231-L374】

### `api_openmm_unit.py`
- Wraps `openmm.unit` quantities and units, exposing predicate helpers and dimensionality translation into the shared SI basis.【F:pyunitwizard/forms/api_openmm_unit.py†L5-L95】
- Implements compatibility, quantity creation, conversions, and flags `parser = True` even though the string parser stubs currently raise `LibraryWithoutParserError` placeholders.【F:pyunitwizard/forms/api_openmm_unit.py†L10-L211】
- Supplies translators to other forms (via functions such as `quantity_to_pint`, `quantity_to_unyt`, and their `unit_to_*` counterparts) so the dispatcher can bridge OpenMM data.【F:pyunitwizard/forms/api_openmm_unit.py†L215-L350】

### `api_unyt.py`
- Adapts Unyt arrays, quantities, and units, reusing Pint conversions to compute dimensionality and compatibility across forms.【F:pyunitwizard/forms/api_unyt.py†L6-L126】
- Implements creation, value/unit extraction, and conversion helpers; parser stubs raise `LibraryWithoutParserError` because Unyt lacks a native string parser.【F:pyunitwizard/forms/api_unyt.py†L127-L213】
- Offers translators to string, Pint, OpenMM, and Astropy modules, ensuring round-trip conversions across the supported ecosystems.【F:pyunitwizard/forms/api_unyt.py†L214-L350】

### `api_astropy_unit.py`
- Integrates `astropy.units` quantities and units, normalizing dimensionality through SI base decomposition and exposing compatibility checks.【F:pyunitwizard/forms/api_astropy_unit.py†L6-L96】
- Provides a working parser (`parser = True`) along with factory, accessor, and converter helpers mirroring other adapters.【F:pyunitwizard/forms/api_astropy_unit.py†L73-L106】
- Relies on Pint as a hub for translators, routing conversions through Pint-backed helpers before delegating to OpenMM or Unyt adapters.【F:pyunitwizard/forms/api_astropy_unit.py†L118-L164】

### `api_string.py`
- Represents the pure string form, marking `parser = False` and delegating structural queries (`is_quantity`, `dimensionality`, etc.) to the current kernel defaults after temporarily converting through the active parser/form pair.【F:pyunitwizard/forms/api_string.py†L1-L99】
- Implements quantity creation, conversion, and serialization helpers that bounce through the configured defaults to maintain consistency with non-string adapters.【F:pyunitwizard/forms/api_string.py†L100-L188】

## Dispatcher wiring

`pyunitwizard.forms.load_library` imports each adapter module, records its primary helpers (identity checks, conversions, dimensionality, compatibility), and collects translator functions whose names start with `quantity_to_`/`unit_to_` for every form that is already loaded.【F:pyunitwizard/forms/__init__.py†L3-L88】 When an adapter advertises `parser = True`, the kernel marks that form as a parser-capable backend so string parsing can be delegated accordingly.【F:pyunitwizard/forms/__init__.py†L36-L70】

## Checklist for adding a new form

- [ ] Add or update unit tests that cover the new adapter’s predicates, conversions, translators, and parser behavior.
- [ ] Register the adapter module in `_forms_apis_modules` and ensure every required dispatcher dictionary is populated inside `load_library`.
- [ ] Implement translators following the established naming pattern (`quantity_to_<target>`, `unit_to_<target>`) and update `api_string.py` to provide reciprocal helpers.
- [ ] Decide whether the form provides a parser. Expose a module-level `parser` flag and, if `True`, include `string_to_quantity`/`string_to_unit` implementations. If parsing is unavailable, set the flag to `False` and raise a clear `LibraryWithoutParserError` from the stubs.
- [ ] Update this README with a summary of the new adapter and document any parser requirements or limitations.
