from pyunitwizard import forms
from pyunitwizard import kernel
from pyunitwizard._private.forms import digest_form
from pyunitwizard._private.lists_and_tuples import is_list_or_tuple
from pyunitwizard.api import convert, get_dimensionality
from pyunitwizard.constants import _constants, _constants_synonyms
import numpy as np
import os
from importlib.util import find_spec
from typing import List, Dict, Union, Optional

libraries = ['pint', 'openmm.unit', 'unyt', 'astropy.units', 'physipy', 'quantities']
parsers   = ['pint', 'openmm.unit', 'unyt', 'astropy.units', 'physipy', 'quantities']
_aux_dict_modules = {
    'pint': 'pint',
    'openmm.unit': 'openmm',
    'unyt': 'unyt',
    'astropy.units': 'astropy',
    'physipy': 'physipy',
    'quantities': 'quantities',
}

def resolve_config_module(
    config: Optional[str] = None,
    root_package: Optional[str] = None,
    env_var: str = "PYUNITWIZARD_CONFIG",
) -> Optional[str]:
    """Resolve configuration module using ``runtime > env > file`` precedence.

    Parameters
    ----------
    config : str, optional
        Explicit runtime configuration module path.
    root_package : str, optional
        Root package name used to probe ``<root_package>._pyunitwizard``.
    env_var : str, default="PYUNITWIZARD_CONFIG"
        Environment variable name used for config-module discovery.

    Returns
    -------
    str or None
        Resolved module path, or ``None`` when no candidate is found.
    """
    if config:
        return config

    from_env = os.getenv(env_var)
    if from_env:
        return from_env

    if root_package:
        module_path = f"{root_package}._pyunitwizard"
        try:
            if find_spec(module_path) is not None:
                return module_path
        except ModuleNotFoundError:
            return None

    return None

def reset() -> None:
    """Reset runtime configuration state to defaults.

    Returns
    -------
    None
        This function mutates global runtime configuration in place.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.reset()
    """
    kernel.loaded_libraries = []
    kernel.loaded_parsers = []
    kernel.default_form=None
    kernel.default_parser=None
    kernel.standards = {}
    kernel.dimensional_fundamental_standards = {}
    kernel.dimensional_combinations_standards = {}
    kernel.adimensional_standards = {}
    kernel.tentative_base_standards = {}
    kernel.dimensional_fundamental_standards_matrix = None
    kernel.dimensional_fundamental_standards_units = None
    kernel.tentative_base_standards_matrix = None
    kernel.tentative_base_standards_units = None
    from pyunitwizard.api.introspection import _TYPE_TO_FORM_CACHE
    _TYPE_TO_FORM_CACHE.clear()

def get_libraries_loaded() -> List[str]:
    """Return currently loaded backend libraries.

    Returns
    -------
    list of str
        Loaded library identifiers.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_libraries_loaded()
    """
    return kernel.loaded_libraries

def get_libraries_supported() -> List[str]:
    """Return backend libraries supported by this installation.

    Returns
    -------
    list of str
        Supported library identifiers.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_libraries_supported()
    """
    return libraries

def get_parsers_loaded() -> List[str]:
    """Return currently loaded parsers.

    Returns
    -------
    list of str
        Loaded parser identifiers.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_parsers_loaded()
    """
    return kernel.loaded_parsers

def get_parsers_supported() -> List[str]:
    """Return parser backends supported by this installation.

    Returns
    -------
    list of str
        Supported parser identifiers.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_parsers_supported()
    """
    return parsers


def load_library(library_names: Union[str, List[str]]):
    """Load one or more backend libraries into runtime configuration.

    Parameters
    ----------
    library_names : str or list of str
        Library name or list of library names to load.

    Returns
    -------
    None
        Loaded libraries are registered in global runtime state.

    Raises
    ------
    TypeError
        If `library_names` is not a string or a list/tuple of strings.
    """
    if not is_list_or_tuple(library_names):
        if isinstance(library_names, str):
            library_names = [library_names]
        else:
            raise TypeError("Expected string or list of strings for library_names")

    for ii in range(len(library_names)):
        library_names[ii]=digest_form(library_names[ii])

    for library in library_names:
        if library not in kernel.loaded_libraries:
            forms.load_library(library)

    if kernel.default_form is None:
        kernel.default_form = library_names[0]

    if kernel.default_parser is None:
        fallback_parser = None
        for library_name in library_names:
            if fallback_parser is None:
                fallback_parser = library_name
            if library_name in kernel.loaded_parsers:
                kernel.default_parser = library_name
                break
        if kernel.default_parser is None:
            kernel.default_parser = fallback_parser


def get_default_form() -> str:
    """Return the configured default form for quantities and units.

    Returns
    -------
    str
        Default runtime form.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_default_form()
    """
    return kernel.default_form

def set_default_form(form: str) -> None:
    """Set the default form for quantities and units.

    Parameters
    ----------
    form : str
        New default form identifier.

    Returns
    -------
    None
        Runtime default form is updated in place.
    """
    form = digest_form(form)
    kernel.default_form = form

def get_default_parser() -> str:
    """Return the configured default parser.

    Returns
    -------
    str
        Default parser identifier.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_default_parser()
    """
    return kernel.default_parser

def set_default_parser(parser: str) -> None:
    """Set the default parser for string quantities.

    Parameters
    ----------
    parser : str
        New default parser identifier.

    Returns
    -------
    None
        Runtime default parser is updated in place.
    """
    form = digest_form(parser)
    kernel.default_parser = form

def get_standard_units() -> Dict[str, Dict[str, int]]:
    """Return configured standard units mapped to dimensionality definitions.

    Returns
    -------
    dict
        Dictionary keyed by standard unit string with dimensionality mappings.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.configure.get_standard_units()
    """
    return kernel.standards

def set_standard_units(standard_units: List[str]) -> None:
    """Configure project standard units used by standardization helpers.

    Parameters
    ----------
    standard_units : list of str
        Standard unit names used as normalization references.

    Returns
    -------
    None
        Runtime standard-unit maps are rebuilt in place.

    Raises
    ------
    ValueError
        If `standard_units` is neither a string nor list/tuple.
    """

    kernel.standards={}
    kernel.dimensional_fundamental_standards={}
    kernel.dimensional_combinations_standards={}
    kernel.adimensional_standards={}

    n_dimensions = len(kernel.order_fundamental_units)

    if type(standard_units) is str:
        standard_units=[standard_units]
    elif type(standard_units) not in [list, tuple]:
        raise ValueError

    for standard_unit in standard_units:

        dim = get_dimensionality(convert(standard_unit, to_type='unit'))
        dim_array = np.array([dim[ii] for ii in kernel.order_fundamental_units], dtype=float)
        n_dims_array = n_dimensions - np.isclose(dim_array,0.0).sum()

        if n_dims_array == 1:

            kernel.dimensional_fundamental_standards[standard_unit] = dim_array

        elif n_dims_array == 0:

            kernel.adimensional_standards[standard_unit] = dim_array

        else:

            kernel.dimensional_combinations_standards[standard_unit] = dim_array

        kernel.standards[standard_unit] = dim

    # Tentative base standards

    kernel.tentative_base_standards=kernel.dimensional_fundamental_standards.copy()

    already = np.zeros(shape=n_dimensions)
    for unit, array in kernel.tentative_base_standards.items():
        already += array

    for ii in range(n_dimensions):
        if np.isclose(already[ii],0):
            candidate = None
            candidate_array = None
            candidate_n_dims = np.inf
            candidate_n_ii = np.inf
            for standard_unit, array in kernel.dimensional_combinations_standards.items():
                if array[ii]>0:
                    if array[ii]<candidate_n_ii:
                        candidate = standard_unit
                        candidate_array = array
                        candidate_n_dis = (n_dimensions - np.isclose(array,0.0).sum())
                        candidate_n_ii = array[ii]
                    elif np.isclose(array[ii],candidate_n_ii):
                        if (n_dimensions - np.isclose(array,0.0).sum()) <candidate_n_dims:
                            candidate = standard_unit
                            candidate_array = array
                            candidate_n_dis = (n_dimensions - np.isclose(array,0.0).sum())
                            candidate_n_ii = array[ii]

            if candidate is not None:
                kernel.tentative_base_standards[candidate] = candidate_array
                for jj in range(ii, n_dimensions):
                    if candidate_array[jj]>0:
                        already[jj]=1

    if len(kernel.dimensional_fundamental_standards) > 0:
        kernel.dimensional_fundamental_standards_units = [
            convert(u, to_type="unit")
            for u in kernel.dimensional_fundamental_standards.keys()
        ]
        kernel.dimensional_fundamental_standards_matrix = np.array(
            list(kernel.dimensional_fundamental_standards.values())
        )
    else:
        kernel.dimensional_fundamental_standards_units = None
        kernel.dimensional_fundamental_standards_matrix = None

    if len(kernel.tentative_base_standards) > 0:
        kernel.tentative_base_standards_units = [
            convert(u, to_type="unit")
            for u in kernel.tentative_base_standards.keys()
        ]
        kernel.tentative_base_standards_matrix = np.array(
            list(kernel.tentative_base_standards.values())
        )
    else:
        kernel.tentative_base_standards_units = None
        kernel.tentative_base_standards_matrix = None

def add_constant(constant_name, value, unit) -> None:
    """Register a runtime constant.

    Parameters
    ----------
    constant_name : str
        Constant identifier.
    value : float or int
        Numeric constant value.
    unit : str
        Unit associated with the constant value.

    Returns
    -------
    None
        Constant mapping is updated in global constants registry.
    """

    _constants[constant_name]=[value, unit]
    pass
