# SMonitor integration

PyUnitWizard uses **SMonitor** to standardize warnings, errors, and diagnostics.

## Files

- `pyunitwizard/_smonitor.py`
- `pyunitwizard/_private/smonitor/catalog.py`
- `pyunitwizard/_private/smonitor/meta.py`

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

## Guidance

- Keep user messages explicit and actionable.
- Keep hints concise and link to docs/issues when useful.
- Avoid hardcoded messages outside the catalog.
