from pyunitwizard._private.exceptions import *

try:
    import pint
except:
    raise LibraryNotFoundError('pint')

from typing import Any, Union, Dict
from pyunitwizard._private.quantity_or_unit import ArrayLike
## Create a unit UnitRegistry
## See: https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
U_ = ureg.Unit

##

form_name = 'pint'
parser = True

is_form={
    pint.Quantity:form_name,
    pint.Unit:form_name,
    Q_:form_name,
    U_:form_name,
    }

def is_quantity(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is an pint quantity.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if it's an pint quantity.
    """
    tmp_type = type(quantity_or_unit)
    return (tmp_type==pint.Quantity or tmp_type==Q_)

def is_unit(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is a pint unit.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if its an openmm.unit.Unit
    """
    tmp_type = type(quantity_or_unit)
    return (tmp_type==pint.Unit or tmp_type==U_)

_dimensions_translator={
    '[length]' : '[L]',
    '[mass]' : '[M]',
    '[time]' : '[T]',
    '[temperature]' : '[K]',
    '[substance]' : '[mol]',
    '[current]' : '[A]',
    '[luminosity]' : '[Cd]'
}

def dimensionality(quantity_or_unit: Union[pint.Quantity, pint.Unit]) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parameters
        -----------
        quantity_or_unit : pint.Quantity or pint.Unit
            A quanitity or a unit

        Returns
        -------
        dimensionality_dict : dict
            Dictionary which keys are fundamental units and values are the exponent of
            each unit in the quantity.

    """
    dimensionality_dict = {'[L]':0, '[M]':0, '[T]':0, '[K]':0, '[mol]':0, '[A]':0, '[Cd]':0}

    for dim, exponent in quantity_or_unit.dimensionality.items():
        dimensionality_dict[_dimensions_translator[dim]]=exponent

    return dimensionality_dict

def compatibility(quantity_or_unit_1: Union[pint.Quantity, pint.Unit], 
                  quantity_or_unit_2: Union[pint.Quantity, pint.Unit]) -> bool:
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

    return tmp_unit_1.is_compatible_with(tmp_unit_2)

def make_quantity(value: Union[float, int, ArrayLike], 
                  unit: str) -> pint.Quantity:
    """ Returns a pint quantity.

        Parmeters
        ---------
        value: int, float or ArrayLike
            The value of the quantity.

        unit : str
            Name of the unit.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """

    return Q_(value, unit)

def get_value(quantity: pint.Quantity) -> Union[int, float, ArrayLike]:
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
    return quantity.magnitude

def get_unit(quantity: pint.Quantity) -> pint.Unit:
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
    return quantity.units

def change_value(quantity: pint.Quantity,
                 value: Union[int, float, ArrayLike]) -> pint.Quantity:

    return make_quantity(value, get_unit(quantity))


def convert(quantity: pint.Quantity, unit_name: str) -> pint.Quantity:
    """ Converts the quantity to a different unit.

        Parameters
        -----------
        quantity : pint.Quantity
            A quanitity or a unit.
        
        unit : str
            The unit to convert to.
        
        Returns
        -------
        pint.Quantity
            The converted quantity.
    """
    return quantity.to(unit_name)


## Parser

def string_to_quantity(string: str) -> pint.Quantity:
    """ Get a quantity from a string.

        Parameters
        ----------
        string : str
            A string with the quantity.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """
    return Q_(string)

def string_to_unit(string: str) -> pint.Unit:
    """ Get a unit from a string.

        Parameters
        ----------
        string : str
            A string with the unit.
        
        Returns
        -------
        pint.Unit
            The unit.
    """
    return U_(string)


# To string

def quantity_to_string(quantity_or_item) -> str:
    """ Convert a quantity to string. 

        Parameters
        -----------
        quantity_or_item : pint.Quantity
            A quanitity or a unit.

        Returns
        -------
        str
            The quantitity as a string.
    """
    return quantity_or_item.__str__()

def unit_to_string(unit_or_item) -> str:
    """ Convert a unit to string. 

        Parameters
        -----------
        unit_or_item : pint.Unit
            A unit.

        Returns
        -------
        str
            The unit as a string.
    """
    return unit_or_item.__str__()


## To openmm.unit

def quantity_to_openmm_unit(quantity: pint.Quantity):
    """ Transform a quantity from a pint quantity to a openmm.unit quantity.
        
        Parameters
        -----------
        quantity : pint.Quantity
            A quanitity.
        
        Returns
        -------
        openmm_unit.Quantity
            The quantity.
    """
    from pint.util import ParserHelper as PintParserHelper
    try:
        import openmm.unit as openmm_unit
    except:
        raise LibraryNotFoundError('openmm')

    value = quantity.magnitude

    pint_parser = PintParserHelper.from_string(quantity.units.__str__())
    tmp_quantity = 1
    for unit_name, exponent in pint_parser.items():
        if unit_name == 'unified_atomic_mass_unit':
            unit_name = 'amu'
        tmp_quantity *= getattr(openmm_unit, unit_name)**exponent

    tmp_quantity *= value

    return tmp_quantity

def unit_to_openmm_unit(unit: pint.Unit):
    """ Transform a unit from a pint unit to a openmm.unit unit.
        
        Parameters
        -----------
        unit : pint.Unit
            A unit.
        
        Returns
        -------
        openmm_unit.Unit
            The unit.
    """

    from .api_openmm_unit import get_unit as get_openmm_unit_unit

    quantity = quantity_to_openmm_unit(1.0*unit)

    return get_openmm_unit_unit(quantity)

## To Unyt

def quantity_to_unyt(quantity: pint.Quantity):
    """ Transform a quantity from a pint quantity to a unyt quantity.
        
        Parameters
        -----------
        quantity : pint.Quantity
            A quantity.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The unyt quantity
    """
    from unyt import unyt_array

    return unyt_array.from_pint(quantity)

def unit_to_unyt(unit: pint.Unit):
    """ Transform a unit from a pint unit to a unyt unit.

        Parameters
        -----------
        unit : pint.Unit
            A unit.

        Returns
        -------
        unyt_array or unyt_quantity
            The unyt quantity
    """

    from .api_unyt import get_unit as get_unyt_unit

    quantity = quantity_to_unyt(1.0*unit)

    return get_unyt_unit(quantity)


## To astropy.units

def quantity_to_astropy_units(quantity: pint.Quantity):
    """ Transform a quantity from pint to astropy.units."""

    from .api_astropy_unit import make_quantity as make_astropy_quantity

    value = get_value(quantity)
    unit_name = unit_to_string(get_unit(quantity))

    return make_astropy_quantity(value, unit_name)


def unit_to_astropy_units(unit: pint.Unit):
    """ Transform a unit from pint to astropy.units."""

    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(1.0*unit)

    return get_astropy_unit(quantity)


