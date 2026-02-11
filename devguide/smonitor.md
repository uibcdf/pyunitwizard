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
- Keep `CODES` and `SIGNALS` wired from `pyunitwizard/_private/smonitor/catalog.py` as the single source of truth.
- Do not silence emission failures with `except Exception: pass`; use a fallback warning/log instead.

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

## Probing Contract

Exploratory checks (`is_quantity`, `is_unit`, and detection paths that parse
candidate strings) must follow this severity contract:

- Expected probe miss (input is not a quantity/unit): `DEBUG`.
- Recoverable anomaly with user impact: `WARNING`.
- Real operation failure: `ERROR`.

For cross-library consistency, expected probe misses should use explicit
diagnostic codes/tags (for example `PUW-DBG-PROBE-001`) and must not surface
as actionable errors in `user` profile.
