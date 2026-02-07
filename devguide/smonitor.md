# SMonitor integration

PyUnitWizard uses SMonitor as the single diagnostics layer.

## Files

- `pyunitwizard/_smonitor.py`
- `pyunitwizard/_private/smonitor/catalog.py`
- `pyunitwizard/_private/smonitor/meta.py`

## Rules

- Emit through catalog entries only.
- Keep user messages explicit and helpful.
- Keep URLs in `meta.py` so hints remain consistent.

## Telemetry & Traceability

Key API functions are instrumented with `@smonitor.signal` to ensure that unit management processes are visible in the diagnostic breadcrumb trails.

**Instrumented areas:**
- **Conversion**: `convert`, `to_string`.
- **Construction**: `quantity`, `unit`.
- **Standardization**: `standardize`, `get_standard_units`.
- **Validation**: `check`.
- **Parsing**: `parse`.
- **Introspection**: `get_form`, `get_dimensionality`.
- **Extraction**: `get_value`, `get_unit`, `get_value_and_unit`.
