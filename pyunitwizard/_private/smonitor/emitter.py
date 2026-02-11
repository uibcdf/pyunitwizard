from __future__ import annotations

from smonitor.integrations import DiagnosticBundle, emit_from_catalog, merge_extra
from .catalog import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve


def emit_probe_miss(value, caller: str):
    """Emit expected probe-miss diagnostics as DEBUG events."""
    emit_from_catalog(
        CATALOG["events"]["ProbeMiss"],
        package_root=PACKAGE_ROOT,
        extra=merge_extra(
            META,
            {
                "value": repr(value),
                "caller": caller,
            },
        ),
    )
