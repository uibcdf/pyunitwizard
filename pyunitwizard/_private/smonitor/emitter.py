from __future__ import annotations

from smonitor import get_manager
from smonitor.integrations import DiagnosticBundle, emit_from_catalog, merge_extra

from .catalog import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve


def emit_probe_miss(value, caller: str):
    """Emit expected probe-miss diagnostics as DEBUG events."""
    level = get_manager().config.level
    # SMonitor excludes DEBUG below its global threshold before routing events.
    # Check the live policy before repr() and catalog registration do any work.
    if isinstance(level, str) and level.upper() in {"INFO", "WARNING", "ERROR", "CRITICAL"}:
        return
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
