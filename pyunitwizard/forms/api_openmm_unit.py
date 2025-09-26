from pyunitwizard._private.exceptions import *
from pyunitwizard._private.quantity_or_unit import ArrayLike
from typing import Any, Dict, Union

try:
    import openmm.unit as openmm_unit
except:
    raise LibraryNotFoundError('openmm')

form_name = 'openmm.unit'
parser = True

is_form={
    openmm_unit.Quantity:form_name,
    openmm_unit.Unit:form_name,
    }

def is_quantity(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is an openmm quantity.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if it's an openmm.unit.Quantity
    """
    return isinstance(quantity_or_unit, openmm_unit.Quantity)

def is_unit(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is an openmm unit.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if its an openmm.unit.Unit
    """
    return isinstance(quantity_or_unit, openmm_unit.Unit)

_dimensions_translator={
    'length' : '[L]',
    'mass' : '[M]',
    'time' : '[T]',
    'temperature' : '[K]',
    'amount' : '[mol]',
    'luminous intensity' : '[Cd]'
}

def dimensionality(quantity_or_unit: Union[openmm_unit.Quantity, openmm_unit.Unit]) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parameters
        -----------
        quantity_or_unit : openmm_unit.Quantity or openmm_unit.Unit
            A quanitity or a unit

        Returns
        -------
        dimensionality_dict : dict
            Dictionary which keys are fundamental units and values are the exponent of
            each unit in the quantity.

    """
    dimensionality_dict = {'[L]':0, '[M]':0, '[T]':0, '[K]':0, '[mol]':0, '[A]':0, '[Cd]':0}

    if is_quantity(quantity_or_unit):
        tmp_unit = quantity_or_unit.unit
    elif is_unit(quantity_or_unit):
        tmp_unit = quantity_or_unit
    else:
        raise TypeError


    for base, exponent in tmp_unit.iter_base_dimensions():
        if base.name == 'charge':
            dimensionality_dict['[A]'] += exponent
            dimensionality_dict['[T]'] += exponent
        else:
            if base.name in _dimensions_translator:
                dimensionality_dict[_dimensions_translator[base.name]]=exponent

    return dimensionality_dict

def compatibility(quantity_or_unit_1: Union[openmm_unit.Quantity, openmm_unit.Unit], 
                  quantity_or_unit_2: Union[openmm_unit.Quantity, openmm_unit.Unit]) -> bool:
    """ Check whether two quantities or units are compatible.

        Parameters
        -----------
        quantity_or_unit_1 : openmm_unit.Quantity or openmm_unit.Quantity
            A quanitity or a unit.

        quantity_or_unit_2 : openmm_unit.Quantity or openmm_unit.Quantity
            A quanitity or a unit.

        Returns
        -------
        bool
            True if they are compatible.
    """
   
    if is_quantity(quantity_or_unit_1):
        tmp_unit_1 = get_unit(quantity_or_unit_1)

    if is_quantity(quantity_or_unit_2):
        tmp_unit_2 = get_unit(quantity_or_unit_2)

    return tmp_unit_1.is_compatible(tmp_unit_2)


def make_quantity(value: Union[int, float, ArrayLike], 
                  unit: openmm_unit.Unit) -> openmm_unit.Quantity:
    """ Returns an openmm quantity.

        Parmeters
        ---------
        value: int, float or ArrayLike
            The value of the quantity.

        unit : openmm_unit.Unit
            The unit.
        
        Returns
        -------
        openmm_unit.Quantity
            The quantity.
    """

    return openmm_unit.Quantity(value, unit)


def get_value(quantity: openmm_unit.Quantity) -> Union[int, float, ArrayLike]:
    """ Returns the value of the quantity.
        
        Parameters
        -----------
        quantity : openmm.unit.Quantity
            A quanitity or a unit.
        
        Returns
        -------
        int, float or ArrrayLike
            The value.
    """
    return quantity._value


def get_unit(quantity: openmm_unit.Quantity) -> openmm_unit.Unit:
    """ Returns the units of the quantity.
        
        Parameters
        -----------
        quantity : openmm.unit.Quantity
            A quanitity or a unit.
        
        Returns
        -------
        openmm.unit.Unit
            The unit.
    """
    return quantity.unit


def change_value(quantity: openmm_unit.Quantity,
                 value: Union[int, float, ArrayLike]) -> openmm_unit.Quantity:

    return make_quantity(value, get_unit(quantity))


def convert(quantity: openmm_unit.Quantity, 
            unit: openmm_unit.Unit) -> openmm_unit.Quantity:
    """ Converts the quantity to a different unit.

        Parameters
        -----------
        quantity : openmm.unit.Quantity
            A quanitity or a unit.
        
        unit : openmm.unit.Unit
            The unit to convert to.
        
        Returns
        -------
        openmm.unit.Quantity
            The converted quantity.
    """

    return quantity.in_units_of(unit)


## Parser

def string_to_quantity(string):

    raise LibraryWithoutParserError('openmm.unit')

def string_to_unit(string):

    raise LibraryWithoutParserError('openmm.unit')


## To string

def quantity_to_string(quantity: openmm_unit.Quantity) -> str:
    """ Convert a quantity to string. 

        Parameters
        -----------
        quantity : openmm_unit.Quantity
            A quanitity.

        Returns
        -------
        str
            The quantitity as a string.
    """
    return quantity.__str__()

def unit_to_string(unit: openmm_unit.Unit) -> str:
    """ Convert a unit to string. 

        Parameters
        -----------
        unit : openmm_unit.Unit
            A unit.

        Returns
        -------
        str
            The quantitity as a string.
    """
    return unit.__str__()


## To Pint

def quantity_to_pint(quantity: openmm_unit.Quantity):
    """ Transform a quantity from openmm.unit to a pint quantity.
        
        Parameters
        -----------
        quantity : openmm.unit.Quantity
            A quanitity.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """
    from .api_pint import make_quantity as make_pint_quantity

    value = get_value(quantity)
    unit_name = unit_to_string(get_unit(quantity))

    return make_pint_quantity(value, unit_name)

def unit_to_pint(unit: openmm_unit.Unit):
    """ Transform a unit from openmm.unit to a pint unit.
        
        Parameters
        -----------
        unit : openmm.unit.Unit
            A unit.
        
        Returns
        -------
        pint.Unit
            The unit.
    """
    from .api_pint import get_unit as get_pint_unit

    quantity = quantity_to_pint(1.0*unit)

    return get_pint_unit(quantity)


## To Unyt

def quantity_to_unyt(quantity: openmm_unit.Quantity):
    """ Transform a quantity from openmm.unit to a unyt quantity.
        
        Parameters
        -----------
        quantity : openmm.unit.Quantity
            A quanitity or a unit.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The quantity.
    """
    from .api_unyt import make_quantity as make_unyt_quantity

    value = get_value(quantity)
    unit_name = get_unit(quantity).get_symbol()

    return make_unyt_quantity(value, unit_name)

def unit_to_unyt(unit: openmm_unit.Unit):
    """ Transform a unit from openmm.unit to a unyt unit.

        Parameters
        -----------
        unit : openmm.unit.Unit
            A unit.

        Returns
        -------
        unyt_unit
            The unit.
    """
    from .api_unyt import get_unit as get_unyt_unit

    quantity = quantity_to_unyt(1.0*unit)

    return get_unyt_unit(quantity)


## To astropy.units

def quantity_to_astropy_units(quantity: openmm_unit.Quantity):
    """ Transform a quantity from openmm.unit to astropy.units."""

    from .api_pint import quantity_to_astropy_units as pint_to_astropy_units

    pint_quantity = quantity_to_pint(quantity)

    return pint_to_astropy_units(pint_quantity)


def unit_to_astropy_units(unit: openmm_unit.Unit):
    """ Transform a unit from openmm.unit to astropy.units."""

    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(1.0*unit)

    return get_astropy_unit(quantity)

