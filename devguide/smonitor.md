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
