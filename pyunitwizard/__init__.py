"""PyUnitWizard
Quantities and units assistant.
"""

from __future__ import annotations

import sys
import types
import warnings
import importlib
from importlib.metadata import version, PackageNotFoundError

try:
    from ._version import __version__
except ImportError:
    try:
        __version__ = version("pyunitwizard")
    except PackageNotFoundError:
        __version__ = "0.0.0+unknown"

from smonitor.integrations import ensure_configured as _ensure_smonitor_configured
from ._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)


def __print_version__() -> None:
    print("PyUnitWizard version " + __version__)


# Central lazy-loading registry mapping public API submodules and functions
# to their respective internal import paths.
_LAZY_ATTRIBUTES = {
    # Submodules
    'configure': '.configure',
    'constants': '.constants',
    'utils': '.utils',

    # API functions
    'are_close': ('.api', 'are_close'),
    'are_compatible': ('.api', 'are_compatible'),
    'are_equal': ('.api', 'are_equal'),
    'compatibility': ('.api', 'compatibility'),
    'change_value': ('.api', 'change_value'),
    'check': ('.api', 'check'),
    'conversion_factor': ('.api', 'conversion_factor'),
    'convert': ('.api', 'convert'),
    'ensure_quantity': ('.api', 'ensure_quantity'),
    'get_dimensionality': ('.api', 'get_dimensionality'),
    'get_form': ('.api', 'get_form'),
    'get_standard_units': ('.api', 'get_standard_units'),
    'get_unit': ('.api', 'get_unit'),
    'get_value': ('.api', 'get_value'),
    'get_value_and_unit': ('.api', 'get_value_and_unit'),
    'is_dimensionless': ('.api', 'is_dimensionless'),
    'is_quantity': ('.api', 'is_quantity'),
    'is_unit': ('.api', 'is_unit'),
    'quantity': ('.api', 'quantity'),
    'similarity': ('.api', 'similarity'),
    'fast_track': ('.api', 'fast_track'),
    'register_fast_track': ('.api', 'register_fast_track'),
    'standardize': ('.api', 'standardize'),
    'to_string': ('.api', 'to_string'),
    'unit': ('.api', 'unit'),
    'context': ('.api', 'context'),
}

__all__ = sorted(list(_LAZY_ATTRIBUTES.keys()))


def __getattr__(name: str):
    if name in _LAZY_ATTRIBUTES:
        target = _LAZY_ATTRIBUTES[name]
        if isinstance(target, str):
            mod = importlib.import_module(target, __name__)
            globals()[name] = mod
            return mod
        elif isinstance(target, tuple):
            submod_path, attr_name = target
            mod = importlib.import_module(submod_path, __name__)
            val = getattr(mod, attr_name)
            globals()[name] = val
            return val

    # Dynamic fallback to fast_track for convenience (e.g. puw.to_nanometers)
    if name.startswith("to_"):
        ft = __getattr__("fast_track")
        if hasattr(ft, name):
            return getattr(ft, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_ATTRIBUTES.keys()))


def _create_main_compat_module() -> types.ModuleType:
    module = types.ModuleType(
        "pyunitwizard.main",
        """Compatibility module for historic imports.

        Deprecated in favour of importing from :mod:`pyunitwizard` directly.
        """.strip(),
    )
    warned = False

    def _emit_warning() -> None:
        nonlocal warned
        if not warned:
            warnings.warn(
                "Importing from 'pyunitwizard.main' is deprecated; import from 'pyunitwizard' instead.",
                DeprecationWarning,
                stacklevel=3,
            )
            warned = True

    def __getattr_compat__(name: str) -> object:
        if name in _LAZY_ATTRIBUTES:
            _emit_warning()
            # Defer attribute loading through our package level lazy loader
            return globals()[name] if name in globals() else __getattr__(name)

        # Dynamic fallback to fast_track for convenience (e.g. puw.to_nanometers)
        if name.startswith("to_"):
            _emit_warning()
            return __getattr__(name)

        raise AttributeError(f"module 'pyunitwizard.main' has no attribute {name!r}")

    def __dir_compat__() -> list[str]:
        return sorted(__all__)

    module.__getattr__ = __getattr_compat__  # type: ignore[assignment]
    module.__dir__ = __dir_compat__  # type: ignore[assignment]
    module.__all__ = tuple(__all__)
    return module


sys.modules.setdefault("pyunitwizard.main", _create_main_compat_module())

# Initialize core kernel state eagerly
from . import kernel as _kernel
_kernel.initialize()

# Eager library loading has been completely removed to achieve ultra-fast startup times.
# Backends are loaded perezosamente on first demand during form digestion.
