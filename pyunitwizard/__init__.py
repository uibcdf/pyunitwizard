"""
PyUnitWizard
Quantities and units assistant
"""

# versioningit
from ._version import __version__

def __print_version__():
    print("PyUnitWizard version " + __version__)


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
)
from . import configure
from . import kernel as _kernel
from . import constants
from . import utils

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

