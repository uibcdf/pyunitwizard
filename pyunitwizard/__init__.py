"""PyUnitWizard
Quantities and units assistant."""

from __future__ import annotations

import sys
import types
import warnings
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyunitwizard")
except PackageNotFoundError:
    # Package is not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "0.0.0+unknown"

from smonitor.integrations import ensure_configured as _ensure_smonitor_configured
from ._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)


def __print_version__() -> None:
    print("PyUnitWizard version " + __version__)


from . import api as _api

# Add imports here
from .api import (
    are_close,
    are_compatible,
    are_equal,
    compatibility,
    change_value,
    check,
    convert,
    get_dimensionality,
    get_form,
    get_standard_units,
    get_unit,
    get_value,
    get_value_and_unit,
    is_dimensionless,
    is_quantity,
    is_unit,
    quantity,
    similarity,
    standardize,
    to_string,
    unit,
    context,
)
from . import configure
from . import kernel as _kernel
from . import constants
from . import utils

__all__ = list(_api.__all__)


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

    def __getattr__(name: str) -> object:
        if name in _api.__all__:
            _emit_warning()
            return getattr(_api, name)
        raise AttributeError(f"module 'pyunitwizard.main' has no attribute {name!r}")

    def __dir__() -> list[str]:
        return sorted(__all__)

    module.__getattr__ = __getattr__  # type: ignore[assignment]
    module.__dir__ = __dir__  # type: ignore[assignment]
    module.__all__ = tuple(__all__)
    return module


sys.modules.setdefault("pyunitwizard.main", _create_main_compat_module())

_kernel.initialize()

try:
    import pint
    configure.load_library('pint')
except:
    pass

try:
    import openmm.unit as openmm_unit
    configure.load_library('openmm.unit')
except:
    pass

try:
    import unyt
    configure.load_library('unyt')
except:
    pass

try:
    import astropy.units  # noqa: F401
    configure.load_library('astropy.units')
except:
    pass
