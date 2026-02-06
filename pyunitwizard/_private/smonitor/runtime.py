from __future__ import annotations

from pathlib import Path

_configured = False


def ensure_configured() -> None:
    global _configured
    if _configured:
        return
    import smonitor

    package_root = Path(__file__).resolve().parents[2]
    smonitor.configure(config_path=package_root)
    _configured = True
