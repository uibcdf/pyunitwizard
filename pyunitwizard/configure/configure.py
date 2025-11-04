from pyunitwizard import forms
from pyunitwizard import kernel
from pyunitwizard._private.forms import digest_form
from pyunitwizard._private.lists_and_tuples import is_list_or_tuple
from pyunitwizard.api import convert, get_dimensionality
from pyunitwizard.constants import _constants, _constants_synonyms
import numpy as np
from importlib.util import find_spec
from typing import List, Dict, Union

libraries = ['pint', 'openmm.unit', 'unyt', 'astropy.units']
parsers   = ['pint', 'openmm.unit', 'unyt', 'astropy.units']
_aux_dict_modules = {
    'pint': 'pint',
    'openmm.unit': 'openmm',
    'unyt': 'unyt',
    'astropy.units': 'astropy',
}

def reset() -> None:
    """Resets all kernel variables."""
    kernel.loaded_libraries = []
    kernel.loaded_parsers = []
    kernel.default_form=None
    kernel.default_parser=None
    kernel.standards = {}
    kernel.dimensional_fundamental_standards = {}
    kernel.dimensional_combinations_standards = {}
    kernel.adimensional_standards = {}
    kernel.tentative_base_standards = {}

def get_libraries_loaded() -> List[str]:
    """ Returns loaded libraries.

        Returns
        -------
        list of str
            A list with the loaded libraries.
    """
    return kernel.loaded_libraries

def get_libraries_supported() -> List[str]:
    """ Returns supported libraries.

        Returns
        -------
        list of str
            A list with the loaded libraries. 
    """
    return libraries

def get_parsers_loaded() -> List[str]:
    """ Returns loaded parsers.

        Returns
        -------
        list of str
            A list with the loaded parsers. 
    """
    return kernel.loaded_parsers

def get_parsers_supported() -> List[str]:
    """ Returns supported parsers.

        Returns
        -------
        list of str
            A list with the supported parsers. 
    """
    return parsers


def load_library(library_names: Union[str, List[str]]):
    """ Loads library or libraries.

        Parameters
        ----------
        library : str, list of str
            Name of the library or list with the name of the libraries.
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
        for library_name in library_names:
            if library_name in parsers:
                kernel.default_parser = library_name
                break


def get_default_form() -> str:
    """ Returns the default form of the quantities and units.

        Returns
        -------
        str
            The default form.
    """
    return kernel.default_form

def set_default_form(form: str) -> None:
    """ Sets the default form of the quantities and units.

        Parameters
        ----------
        form : str
            The new default form.
    """
    form = digest_form(form)
    kernel.default_form = form

def get_default_parser() -> str:
    """ Returns the default parser.

        Returns
        -------
        str
            The default form.
    """
    return kernel.default_parser

def set_default_parser(parser: str) -> None:
    """ Sets the default form of the quantities and units.

        Parameters
        ----------
        form : str
            The new default form.
    """
    form = digest_form(parser)
    kernel.default_parser = parser

def get_standard_units() -> Dict[str, Dict[str, int]]:
    """ Returns a nested dictionary where each subdictionary corresponds
        to the dimensionality of the standard units set in the
        configuration.

        Returns
        -------
        dict
            Dictionary with standard units. 
    """
    return kernel.standards

def set_standard_units(standard_units: List[str]) -> None:
    """ Sets the standard units.

        Parameters
        ----------
        standard_units : list of str
            List with the standard units
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

def add_constant(constant_name, value, unit) -> None:

    _constants[constant_name]=[value, unit]
    pass
