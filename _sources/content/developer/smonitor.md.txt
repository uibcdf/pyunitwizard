# SMonitor integration

PyUnitWizard uses **SMonitor** as its diagnostics layer for warnings, errors,
and traceable operational events.

## Files

- `pyunitwizard/_smonitor.py`
- `pyunitwizard/_private/smonitor/catalog.py`
- `pyunitwizard/_private/smonitor/meta.py`
- `pyunitwizard/_private/smonitor/emitter.py`

## Core rules

- Emit diagnostics through catalog entries only.
- Keep user messages explicit, concise, and actionable.
- Keep docs/issues/API URLs in `meta.py` so hints remain consistent.
- Keep `CODES` and `SIGNALS` in `catalog.py` as the single source of truth.
- Do not silence emission failures with `except Exception: pass`; use a safe fallback warning/log path.
- Keep `ensure_configured(PACKAGE_ROOT)` in `pyunitwizard.__init__` to initialize diagnostics at import time.
- Use `DiagnosticBundle` helpers (`warn`, `warn_once`, `resolve`) from `emitter.py` where applicable.

## Emission pattern

```python
from smonitor.integrations import emit_from_catalog
from pyunitwizard._private.smonitor import CATALOG, META, PACKAGE_ROOT

emit_from_catalog(
    CATALOG["pyunitwizard.unit_conversion"],
    package_root=PACKAGE_ROOT,
    meta=META,
    extra={"unit": unit},
)
```

## Telemetry and traceability

Key API paths are instrumented with `@smonitor.signal` to keep unit operations
visible in diagnostic breadcrumb trails.

Instrumented areas include:
- conversion (`convert`, `to_string`),
- construction (`quantity`, `unit`),
- standardization (`standardize`, `get_standard_units`),
- validation (`check`),
- parsing (`parse`),
- introspection (`get_form`, `get_dimensionality`),
- extraction (`get_value`, `get_unit`, `get_value_and_unit`),
- comparison (`are_close`, `are_equal`, `are_compatible`).

## Probing severity contract

Exploratory checks (`is_quantity`, `is_unit`, and probe-style parsing paths)
must follow this severity contract:

- expected probe miss: `DEBUG`,
- recoverable anomaly with user impact: `WARNING`,
- real operation failure: `ERROR`.

Expected probe misses should use explicit diagnostic codes/tags and must not
surface as actionable errors in `user` profile.

`emit_probe_miss()` in `pyunitwizard/_private/smonitor/emitter.py` is the
canonical helper for probe-miss reporting.
