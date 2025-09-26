from typing import Dict, Union
from pyunitwizard._private.quantity_or_unit import ArrayLike

form_name = 'string'
paser = False

is_form={
    str:form_name,
    }

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
    from pyunitwizard import convert as _convert, is_unit as _is_unit

    tmp_quantity_or_unit = _convert(quantity_or_unit, to_form=default_form, parser=default_parser)
    return _is_unit(tmp_quantity_or_unit)

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

    # This function will raise an error.
    from .api_openmm_unit import string_to_quantity as string_to_openmm_unit_quantity

    tmp_quantity_or_unit = string_to_openmm_unit_quantity(quantity)

    return tmp_quantity_or_unit

def unit_to_openmm_unit(unit: str):

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
    raise NotImplementedError

def unit_to_unyt(quantity: str):
    raise NotImplementedError


## To astropy.units

def quantity_to_astropy_units(quantity: str):
    from .api_astropy_unit import string_to_quantity as _string_to_quantity

    return _string_to_quantity(quantity)


def unit_to_astropy_units(unit: str):
    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(unit)

    return get_astropy_unit(quantity)

