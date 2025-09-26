from sympy import im
from pyunitwizard._private.exceptions import *
from pyunitwizard._private.quantity_or_unit import ArrayLike
from typing import Any, Dict, Union

try:
    import unyt
    from unyt import unyt_array, unyt_quantity
    from unyt import Unit as unyt_unit
except:
    raise LibraryNotFoundError('unyt')

form_name = 'unyt'
parser = True

#is_form = {
#    unyt_array:    form_name,
#    unyt_quantity: form_name,
#    unyt_unit:          form_name,
#}

def is_form(quantity_or_unit: Any) -> bool:
    return is_quantity(quantity_or_unit) or is_unit(quantity_or_unit)

def is_quantity(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is a unyt quantity.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if it is a unyt.unyt_array or unyt.unyt_quantity.
    """
    return isinstance(quantity_or_unit, (unyt_array, unyt_quantity))

def is_unit(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is a unyt unit.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit.

        Returns
        -------
        bool
            True if it is a unyt_unit.
    """
    return isinstance(quantity_or_unit, unyt_unit)

def dimensionality(quantity_or_unit: Union[unyt_array, unyt_quantity, unyt_unit]
                  ) -> Dict[str, int]:
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
    # We get the dimensionality by transforming first to pint because
    # unyt handles dimensions in a different way. Might change this in
    # the future.
    from .api_pint import dimensionality as dimensionality_pint

    if is_unit(quantity_or_unit):
        temp_quantity = 1 * quantity_or_unit
    else:
        temp_quantity = quantity_or_unit
    temp_quantity = temp_quantity.to_pint()

    return dimensionality_pint(temp_quantity)
    

def compatibility(quantity_or_unit_1: Union[unyt_array, unyt_quantity, unyt_unit], 
                  quantity_or_unit_2: Union[unyt_array, unyt_quantity, unyt_unit]
                  ) -> bool:
    """ Check whether two quantities or units are compatible.

        Parameters
        ----------
        quantity_or_unit_1 : unyt_array or unyt_quantity or unyt_unit
            A quanitity or a unit.

        quantity_or_unit_2 : unyt_array or unyt_quantity or unyt_unit
            A quanitity or a unit.

        Returns
        -------
        bool
            True if they are compatible.
    """
    if is_quantity(quantity_or_unit_1):
        unit_1 = get_unit(quantity_or_unit_1)
    else:
        unit_1 = quantity_or_unit_1
    
    if is_quantity(quantity_or_unit_2):
        unit_2 = get_unit(quantity_or_unit_2)
    else:
        unit_2 = unit_2

    return unit_1.same_dimensions_as(unit_2)

def make_quantity(value: Union[int, float, ArrayLike], 
                  unit: Union[str, unyt_unit]) -> Union[unyt_array, unyt_quantity]:
    """ Returns a unyt quantity.

        Parmeters
        ---------
        value: int, float or ArrayLike
            The value of the quantity.

        unit : unyt_unit or str
            The unit.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The quantity.
    """ 
    if isinstance(value, (int, float)):
        return unyt_quantity(value, unit)
    else:
        return unyt_array(value, unit)

def get_value(quantity: Union[unyt_array, 
                        unyt_quantity]) -> Union[int, float, ArrayLike]:
    """ Returns the value of the quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        Returns
        -------
        int, float or ArrrayLike
            The value.
    """
    return quantity.value

def get_unit(quantity: Union[unyt_array, 
                       unyt_quantity]) -> unyt_unit:
    """ Returns the units of the quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        Returns
        -------
        unyt_unit
            The unit.
    """
    return quantity.units

def change_value(quantity: Union[unyt_quantity, unyt_array],
                 value: Union[int, float, ArrayLike]) -> Union[unyt_array, unyt_quantity]:

    return make_quantity(value, get_unit(quantity))

def convert(quantity: Union[unyt_array, unyt_quantity], 
            unit_name: str) -> Union[unyt_array, unyt_quantity]:
    """ Converts the quantity to a different unit.

        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        unit : str
            The unit to convert to.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The converted quantity.
    """
    return quantity.to(unit_name)


## Parser

def string_to_quantity(string):

    raise LibraryWithoutParserError("Unyt library has no string parser")

def string_to_unit(string):

    raise LibraryWithoutParserError("Unyt library has no string parser")


## To string

def quantity_to_string(quantity: Union[unyt_array, 
                                unyt_quantity]) -> str:
    """ Convert a quantity to string. 

        Parameters
        -----------
        quantity: unyt_array or unyt_quantity
            A quanitity or a unit.

        Returns
        -------
        str
            The quantitity as a string.
    """
    return str(quantity)

def unit_to_string(unit: unyt_unit) -> str:
    """ Convert a unit to string. 

        Parameters
        -----------
        unit: unyt_unit
            A unit.

        Returns
        -------
        str
            The unit as a string.
    """
    return str(unit)


## To Pint

def quantity_to_pint(quantity: Union[unyt_array, 
                       unyt_quantity]):
    """ Transform a quantity from unyt to a pint quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """
    from .api_pint import ureg
    return quantity.to_pint(unit_registry=ureg)

def unit_to_pint(unit: unyt_unit):
    """ Transform a unit from unyt to a pint unit.
        
        Parameters
        -----------
        unit : unyt_unit
            A unit.
        
        Returns
        -------
        pint.Unit
            The unit.
    """
    from .api_pint import get_unit as get_pint_unit

    quantity = quantity_to_pint(1.0*unit)

    return get_pint_unit(quantity)


## To openmm.unit

def quantity_to_openmm_unit(quantity: Union[unyt_array, unyt_quantity]):
    """ Transform a quantity from unyt to an openmm.unit quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity.
        
        Returns
        -------
        openmm.unit.Quantity
            The quantity.
    """
    # Convert to pint quantity first and then to openmm. Temporary solution
    from .api_pint import quantity_to_openmm_unit as pint_quantity_to_openmm

    return pint_quantity_to_openmm(quantity.to_pint())

def unit_to_openmm_unit(unit: unyt_unit):
    """ Transform a unit from unyt to a openmm.unit unit.

        Parameters
        -----------
        unit : unyt_unit
            A unit.

        Returns
        -------
        openmm_unit.Unit
            The unit.
    """
    from .api_openmm_unit import get_unit as get_openmm_unit_unit

    quantity = quantity_to_openmm_unit(1.0*unit)

    return get_openmm_unit_unit(quantity)


## To astropy.units

def quantity_to_astropy_units(quantity: Union[unyt_array, unyt_quantity]):
    """ Transform a quantity from unyt to astropy.units."""

    from .api_pint import quantity_to_astropy_units as pint_to_astropy_units

    pint_quantity = quantity.to_pint()

    return pint_to_astropy_units(pint_quantity)


def unit_to_astropy_units(unit: unyt_unit):
    """ Transform a unit from unyt to astropy.units."""

    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(1.0*unit)

    return get_astropy_unit(quantity)


