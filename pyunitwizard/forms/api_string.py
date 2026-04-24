from typing import Any, Dict, Union
from pyunitwizard._private.quantity_or_unit import ArrayLike

form_name = 'string'
parser = False

#is_form={
#    str:form_name,
#    }

def is_form(quantity_or_unit: Any) -> bool:
    """Check whether an object belongs to the ``string`` form.

    Parameters
    ----------
    quantity_or_unit : Any
        Candidate object.

    Returns
    -------
    bool
        ``True`` when the object is a Python string.
    """

    return isinstance(quantity_or_unit, str)


def is_quantity(quantity_or_unit: str) -> bool:
    """ Check whether a string is a quantity.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if it's a quantity.
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, is_quantity as _is_quantity

    tmp_quantity_or_unit = _convert(quantity_or_unit, to_form=default_form, parser=default_parser)
    return _is_quantity(tmp_quantity_or_unit)

def is_unit(quantity_or_unit: str) -> bool:
    """ Check whether a string is a unit.

        Parameters
        -----------
        quantity_or_unit : str
            A quanitity or a unit

        Returns
        -------
        bool
            True if its a unit.
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, get_value as _get_value

    # Parse the string as-is (quantity, not forced to unit) and check whether
    # its numeric value is 1.  A pure unit string like "nanometer" parses as
    # Quantity(1, 'nm'); a quantity string like "250 ms" parses as
    # Quantity(250, 'ms').  This is consistent with the public puw.is_unit
    # heuristic in api/introspection.py.
    tmp = _convert(quantity_or_unit, to_form=default_form, parser=default_parser)
    return _get_value(tmp) == 1

def dimensionality(quantity_or_unit: str) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parameters
        -----------
        quantity_or_unit : str
            A quanitity or a unit

        Returns
        -------
        dimensionality_dict : dict
            Dictionary which keys are fundamental units and values are the exponent of
            each unit in the quantity.

    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, get_dimensionality as _get_dimensionality

    tmp_quantity_or_unit = _convert(quantity_or_unit, to_form=default_form, parser=default_parser)
    return _get_dimensionality(tmp_quantity_or_unit)


def compatibility(quantity_or_unit_1: str, quantity_or_unit_2: str) -> bool:
    """ Check whether two quantities or units are compatible.

        Parameters
        -----------
        quantity_or_unit_1 : str
            A quanitity or a unit.

        quantity_or_unit_2 : str
            A quanitity or a unit.

        Returns
        -------
        bool
            True if they are compatible.
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, are_compatible as _are_compatible

    tmp_quantity_or_unit_1 = _convert(quantity_or_unit_1, to_form=default_form, parser=default_parser)
    tmp_quantity_or_unit_2 = _convert(quantity_or_unit_2, to_form=default_form, parser=default_parser)
    return _are_compatible(tmp_quantity_or_unit_1, tmp_quantity_or_unit_2)

def make_quantity(value: Union[int, float, ArrayLike], 
                  unit_name: str) -> str:
    """ Returns a string quantity.

        Parmeters
        ---------
        value: int, float or ArrayLike
            The value of the quantity.

        unit : str
            Name of the unit.
        
        Returns
        -------
        str
            The quantity.

        Examples
        --------
        >>> make_quantity(1.0, "nanometer")
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, quantity as _quantity

    tmp_quantity_or_unit = _quantity(value, unit=unit_name, form=default_form, parser=default_parser)
    return _convert(tmp_quantity_or_unit, to_form='string', parser=default_parser)

def get_value(quantity: str) -> str:
    """ Returns the value of the quantity.
        
        Parameters
        -----------
        quantity : pint.Quantity
            A quanitity or a unit.
        
        Returns
        -------
        int, float or ArrrayLike
            The value.
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert, get_value as _get_value

    tmp_quantity_or_unit = _convert(quantity, to_form=default_form, parser=default_parser)
    return str(_get_value(tmp_quantity_or_unit))

def get_unit(quantity: str) -> str:
    """ Returns the units of the quantity.
        
        Parameters
        -----------
        quantity : pint.Quantity
            A quanitity or a unit.
        
        Returns
        -------
        pint.Unit
            The unit.
    """
    from pyunitwizard.kernel import default_parser
    from pyunitwizard import convert as _convert, get_unit as _get_unit

    tmp_quantity_or_unit = _convert(quantity, to_form=default_parser)
    tmp_unit = _get_unit(tmp_quantity_or_unit)
    return _convert(tmp_unit, to_form='string')

def change_value(quantity: str,
                 value: Union[int, float, ArrayLike]) -> str:
    """Return a string quantity with updated value and preserved unit.

    Parameters
    ----------
    quantity : str
        Input quantity in string form.
    value : int or float or ArrayLike
        New numeric value.

    Returns
    -------
    str
        Quantity with replaced value and original unit.
    """

    return make_quantity(value, get_unit(quantity))

def convert(quantity: str, unit_name: str) -> str:
    """ Converts the quantity to a different unit.

        Parameters
        -----------
        quantity : str
            A quanitity-
        
        unit : str
            The unit to convert to.
        
        Returns
        -------
        str
            The converted quantity.
    """
    from pyunitwizard.kernel import default_form, default_parser
    from pyunitwizard import convert as _convert

    tmp_quantity_or_unit = _convert(quantity, to_form=default_form, parser=default_parser)
    tmp_quantity_or_unit = _convert(tmp_quantity_or_unit, to_unit=unit_name, parser=default_parser)
    return _convert(tmp_quantity_or_unit, to_form='string')


## Parser

#def string_to_quantity(string: str) -> str:
#    """ Returns the same string. """
#    return string
#
#def string_to_unit(string: str) -> str:
#    """ Returns the same string. """
#    return string


## To openmm.unit

def quantity_to_openmm_unit(quantity: str):
    """Convert a string quantity into an OpenMM quantity.

    Parameters
    ----------
    quantity : str
        Quantity in string form.

    Returns
    -------
    openmm.unit.Quantity
        Quantity represented in OpenMM units.
    """

    # This function will raise an error.
    from .api_openmm_unit import string_to_quantity as string_to_openmm_unit_quantity

    tmp_quantity_or_unit = string_to_openmm_unit_quantity(quantity)

    return tmp_quantity_or_unit

def unit_to_openmm_unit(unit: str):
    """Convert a string unit into an OpenMM unit.

    Parameters
    ----------
    unit : str
        Unit name in string form.

    Returns
    -------
    openmm.unit.Unit
        Unit represented in OpenMM backend.
    """

    from .api_openmm_unit import get_unit as get_openmm_unit_unit

    quantity = quantity_to_openmm_unit(unit)

    return get_openmm_unit_unit(quantity)


## To pint

def quantity_to_pint(quantity: str):
    """ Transform a quantity from a string quantity to a pint quantity.
        
        Parameters
        -----------
        quantity : str
            A quanitity.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """
    from .api_pint import string_to_quantity as _string_to_quantity

    return _string_to_quantity(quantity)

def unit_to_pint(unit: str):
    """ Transform a quantity from a string quantity to a pint quantity.

        Parameters
        -----------
        quantity : str
            A quanitity.

        Returns
        -------
        pint.Quantity
            The quantity.
    """
    from .api_pint import get_unit as get_pint_unit

    quantity = quantity_to_pint(unit)

    return get_pint_unit(quantity)


## To unyt

def quantity_to_unyt(quantity: str):
    """Convert a string quantity into a unyt quantity.

    Parameters
    ----------
    quantity : str
        Quantity in string form.

    Returns
    -------
    unyt.unyt_array or unyt.unyt_quantity
        Quantity represented in unyt backend.
    """
    raise NotImplementedError

def unit_to_unyt(quantity: str):
    """Convert a string unit into a unyt unit.

    Parameters
    ----------
    quantity : str
        Unit name in string form.

    Returns
    -------
    unyt.Unit
        Unit represented in unyt backend.
    """
    raise NotImplementedError


## To astropy.units

def quantity_to_astropy_units(quantity: str):
    """Convert a string quantity into an Astropy quantity.

    Parameters
    ----------
    quantity : str
        Quantity in string form.

    Returns
    -------
    astropy.units.Quantity
        Quantity represented in Astropy backend.
    """
    from .api_astropy_unit import string_to_quantity as _string_to_quantity

    return _string_to_quantity(quantity)


def unit_to_astropy_units(unit: str):
    """Convert a string unit into an Astropy unit.

    Parameters
    ----------
    unit : str
        Unit name in string form.

    Returns
    -------
    astropy.units.UnitBase
        Unit represented in Astropy backend.
    """
    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(unit)

    return get_astropy_unit(quantity)


## To physipy

def quantity_to_physipy(quantity: str):
    """Convert a string quantity into a physipy quantity."""
    from .api_pint import string_to_quantity as _string_to_quantity
    from .api_physipy import quantity_to_physipy as _quantity_to_physipy

    pint_quantity = _string_to_quantity(quantity)
    return _quantity_to_physipy(pint_quantity)


def unit_to_physipy(unit: str):
    """Convert a string unit into a physipy unit-like object."""
    from .api_physipy import get_unit as _get_unit

    quantity = quantity_to_physipy(unit)
    return _get_unit(quantity)


## To quantities

def quantity_to_quantities(quantity: str):
    """Convert a string quantity into a quantities quantity."""
    from .api_pint import string_to_quantity as _string_to_quantity
    from .api_quantities import quantity_to_quantities as _quantity_to_quantities

    pint_quantity = _string_to_quantity(quantity)
    return _quantity_to_quantities(pint_quantity)


def unit_to_quantities(unit: str):
    """Convert a string unit into a quantities unit-like object."""
    from .api_quantities import get_unit as _get_unit

    quantity = quantity_to_quantities(unit)
    return _get_unit(quantity)
