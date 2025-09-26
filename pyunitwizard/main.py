from ._private.exceptions import *
from ._private.forms import digest_form, digest_to_form
from ._private.parsers import digest_parser
from ._private.quantity_or_unit import ArrayLike, QuantityOrUnit, QuantityLike, UnitLike
from .forms import dict_is_form, dict_is_unit, dict_is_quantity, dict_dimensionality, dict_compatibility
from .forms import dict_get_unit, dict_get_value, dict_make_quantity
from .forms import dict_convert, dict_translate_quantity, dict_translate_unit, dict_change_value
from .import kernel
from .parse import parse as _parse
import numpy as np
from typing import Any, Dict, Optional, Union, Tuple

def get_form(quantity_or_unit: QuantityOrUnit) -> str:
    """ Returns the form of a quantity as a string.

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quanitity or a unit

        Returns
        -------
        {"string", "pint", "openmm.unit", "unyt"}
            The form of the quantity
    """
    try:
        return dict_is_form[type(quantity_or_unit)]
    except KeyError:
        try:
            return dict_is_form[quantity_or_unit]
        except KeyError:
            raise NotImplementedFormError(type(quantity_or_unit))


def is_quantity(quantity_or_unit: QuantityOrUnit, parser: Optional[str]=None) -> bool:
    """ Check whether an object is a quantity

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quanitity or a unit

        parser :  {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser for string quantities

        Returns
        -------
        bool
            False if it's not a quantity
    """
    if isinstance(quantity_or_unit, str):
        try:
            quantity_or_unit = convert(quantity_or_unit, to_form=kernel.default_form, parser=parser)
            output = dict_is_quantity[kernel.default_form](quantity_or_unit)
        except:
            return False
    else:
        try:
            form = get_form(quantity_or_unit)
            output = dict_is_quantity[form](quantity_or_unit)
        except:
            return False

    return output

def is_unit(quantity_or_unit: QuantityOrUnit, parser: Optional[str]=None) -> bool:
    """ Check whether an object is a unit

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit

        parser :  {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser for string quantities

        Returns
        -------
        bool
            False if it's not a unit
    """
    if isinstance(quantity_or_unit, str):
        try:
            quantity_or_unit = convert(quantity_or_unit, parser=parser)
            output = (get_value(quantity_or_unit)==1)
        except:
            return False
    else:
        try:
            form = get_form(quantity_or_unit)
            output = dict_is_unit[form](quantity_or_unit)
        except:
            return False

    return output

def get_value(quantity: QuantityLike,
              to_unit:  Optional[str]=None,
              parser:   Optional[str]=None,
              standardized: Optional[bool]=False)-> Union[np.ndarray, float, int]:
    """ Returns the value of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).
        
        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        np.ndarray or float or int
            An array with the quantity value or a a float or an int if it's a scalar.

    """

    if standardized:
        quantity = standardize(quantity)
        to_unit = None

    return convert(quantity, to_unit=to_unit, parser=parser, to_type='value')

def get_unit(quantity: QuantityLike, 
             to_form: Optional[str]=None, 
             parser:  Optional[str]=None,
             standardized: Optional[bool]=False)-> UnitLike:
    """ Returns the unit of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).
        
         form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            If passed the unit will be converted to that form. This is the type that will be returned

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        UnitLike
            The unit.

    """

    if standardized:
        quantity = standardize(quantity)

    return convert(quantity, to_form=to_form, parser=parser, to_type='unit')

def get_value_and_unit(quantity: QuantityLike,
              to_unit:  Optional[str]=None,
              to_form: Optional[str]=None,
              parser:   Optional[str]=None,
              standardized: Optional[str]=False) -> Tuple[Union[np.ndarray, float, int], UnitLike]:
    """ Returns the value and unit of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).
        
        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        np.ndarray or float or int
        UnitLike
            The value and unit of the input quantity.

    """

    if standardized:
        quantity = standardize(quantity)
        to_unit = None

    value = convert(quantity, to_unit=to_unit, parser=parser, to_type='value')
    unit = convert(quantity, to_unit=to_unit, to_form=to_form, parser=parser, to_type='unit')

    return value, unit

def change_value(quantity: QuantityLike,
                 value: Union[np.ndarray, float, int]) -> QuantityLike:

    form = get_form(quantity)
    return dict_change_value[form](quantity, value)

def similarity(quantity_or_unit_1: QuantityOrUnit,
              quantity_or_unit_2: QuantityOrUnit,
              relative_tolerance: float=1e-08) -> bool:

    return are_close(quantity_or_unit_1, quantity_or_unit_2, rtol=relative_tolerance)

def are_close(quantity_1: QuantityLike,
              quantity_2: QuantityLike,
              rtol: float=1e-05,
              atol: float=1e-08) -> bool:
    """ Compares whether two quantities are similiar within a specified tolerance.
    
        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit
        
        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        relative_tolerance : float
            The relative tolerance to compare the quantities.

        Returns
        -------
        bool
            Whether the quantities or units are similar.
    """
    compatible = are_compatible(quantity_1, quantity_2)

    if compatible:

        value_1, unit_1 = get_value_and_unit(quantity_1)
        value_2 = get_value(quantity_2, to_unit=unit_1)

        if isinstance(value_1, (list, tuple, np.ndarray)):

            return np.allclose(value_1, value_2, rtol=rtol, atol=atol)

        else:
            
            check_atol = (abs(value_1-value_2) < atol)
            check_rtol = (abs(value_1/value_2 - 1.0) < rtol)

            return (check_atol and check_rtol)

    return False

def are_equal(quantity_or_unit_1: QuantityOrUnit,
              quantity_or_unit_2: QuantityOrUnit,
              same_form=False) -> bool:
    """ Compares whether two quantities are similiar within a specified tolerance.
    
        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit
        
        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        relative_tolerance : float
            The relative tolerance to compare the quantities.

        Returns
        -------
        bool
            Whether the quantities or units are similar.
    """

    if same_form:
        form_1 = get_form(quantity_or_unit_1)
        form_2 = get_form(quantity_or_unit_2)
        if form_1!=form_2:
            return False

    compatible = are_compatible(quantity_or_unit_1, quantity_or_unit_2)

    if compatible:

        if is_quantity(quantity_or_unit_1) and is_quantity(quantity_or_unit_2):

            value_1, unit_1 = get_value_and_unit(quantity_or_unit_1)
            value_2 = get_value(quantity_or_unit_2, to_unit=unit_1)

            if isinstance(value_1, (list, tuple, np.ndarray)):

                return np.all(np.equal(value_1, value_2))

            else:
                
                return value_1==value_2

        elif is_unit(quantity_or_unit_1) and is_unit(quantity_or_unit_2):

            unit_1 = convert(quantity_or_unit_1)
            unit_2 = convert(quantity_or_unit_2)

            return unit_1==unit_2

    return False


def get_dimensionality(quantity_or_unit: QuantityOrUnit) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parmeters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit

        Returns
        -------
        dict
            A dictionary with the dimensionality of the unit.
    """
    dim = None

    if isinstance(quantity_or_unit, str):
        if is_quantity(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type='quantity')
        elif is_unit(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type='unit')

    form = get_form(quantity_or_unit)
    dim = dict_dimensionality[form](quantity_or_unit)

    return dim

def _dimensionality_dict_to_array(dimensionality: Dict[str, int]) -> np.ndarray:
    """ Returns a numpy array with the dimensionality. 

        Parameters
        ----------
        dimensionality : dict
            Dictionary which keys are fundamental units and values are the exponent of
            each unit in the quantity.

        Returns
        -------
        np.ndarray of shape (7,)
            Array where each entry represents the power of each fundamental unit in
            the quantity. The order of the fundamental units is given by the order of
            fundamental units.
    """
    dim_list = []

    for unit in kernel.order_fundamental_units:
        try:
            dim_list.append(dimensionality[unit])
        except KeyError:
            dim_list.append(0)

    return np.array(dim_list, dtype=float)


def compatibility(quantity_or_unit_1: QuantityOrUnit,
                  quantity_or_unit_2: QuantityOrUnit) -> bool:

    return are_compatible(quantity_or_unit_1, quantity_or_unit_2)

def are_compatible(quantity_or_unit_1: QuantityOrUnit,
                  quantity_or_unit_2: QuantityOrUnit) -> bool:
    """ Check whether two quantities or units are compatible.
        This means that they have the same dimensionalities.
        
        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit
        
        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        Returns
        -------
        bool
            Whether the quantities or units are compatible.
    """

    if is_dimensionless(quantity_or_unit_1) and is_dimensionless(quantity_or_unit_2):

        form1 = get_form(quantity_or_unit_1)
        form2 = get_form(quantity_or_unit_2)

        if form1!=form2:

            try:
                tmp = convert(quantity_or_unit_1, to_form=form2)
                is_compatible = dict_compatibility[form2](tmp, quantity_or_unit_2)
            except:
                tmp = convert(quantity_or_unit_2, to_form=form1)
                is_compatible = dict_compatibility[form1](tmp, quantity_or_unit_1)

        else:

            is_compatible = dict_compatibility[form1](quantity_or_unit_1, quantity_or_unit_2)

    else:

        dim1 = get_dimensionality(quantity_or_unit_1)
        dim2 = get_dimensionality(quantity_or_unit_2)

        is_compatible = _compatible_dimensionalities(dim1, dim2)

    return is_compatible

def is_dimensionless(quantity_or_unit: QuantityOrUnit) -> bool:
    """ Check wheter a quantity or unit is dimensionless.

        Parameters
        ----------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit
        
        Returns
        -------
        bool
            Whether the quantity or unit is dimensionless.
    """
    dim = get_dimensionality(quantity_or_unit)
    # If we find a non zero value in the dimensionality dict we return false
    for exponent in dim.values():
        if exponent != 0:
            return False
    return True
    
def _compatible_dimensionalities(dim1: Dict[str, int], dim2: Dict[str, int]) -> bool:
    """ Check whether two dimensionalities are compatible.

        Parameters
        ----------
        dim1 : dict
            Dimensionality dictionary.

        dim2 : dict
            Dimensionality dictionary.
        
        Returns
        ----------
        bool
            Whether the dimensiomnalities are compatible.

    """

    for dim in ['[L]', '[M]', '[T]', '[K]', '[mol]', '[A]', '[Cd]']:
        if dim not in dim1:
            dim1[dim]=0
        if dim not in dim2:
            dim2[dim]=0

    return dim1 == dim2

def quantity(value: Union[int, float, ArrayLike],
            unit: Optional[UnitLike]=None,
            form: Optional[str]=None,
            parser: Optional[str]=None,
            standardized: Optional[bool]=False) -> QuantityLike:
    """ Returns a quantity.

        Parameters
        ----------
        value : int, float or arraylike
            The value of the quantity. Can be a scalar or an array like type.

        unit : UnitLike
            Unit in of the quantity in any of the accepted form.

        form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            Output form of the quantity.

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        standardized : bool, optional
            Return a standardized quantity, default=False.

        Returns
        -------
        QuantityLike
            The quantity.
    """
    output = None

    form = digest_form(form)
    
    if type(value) is str:
        if unit is None:
            output = convert(value, to_form=form, parser=parser)
            if not is_quantity(output):
                raise BadCallError('value')
        elif type(unit) is str:
            output = convert(value+' '+unit, to_form=form, parser=parser)
        elif is_unit(unit):
            unit = convert(unit, to_form='string', parser=parser)
            output = convert(value+' '+unit, to_form=form, parser=parser)
    else:
        if unit is None:
            raise BadCallError('unit')

        unit = convert(unit, to_form=form, parser=parser, to_type='unit')

        try:
            output = dict_make_quantity[form](value, unit)
        except:
            raise NotImplementedMethodError()

    if standardized:
        output = standardize(output)

    return output

def unit(unit: str, form: Optional[str]=None, parser: Optional[str]=None) -> UnitLike:
    """ Returns a unit.

        Parameters
        ----------
        unit : str
            Name of the unit (i.e kcal/mol).
        
        form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            The form of the unit. This is the type that will be returned
        
        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.
        
        Returns
        -------
        Unitlike
            The unit.
    
    """
    return convert(unit, to_form=form, parser=parser, to_type='unit')

def convert(quantity_or_unit: Any, 
            to_unit: Optional[str]=None, 
            to_form: Optional[str]=None, 
            parser:  Optional[str]=None, 
            to_type: Optional[str]='quantity') -> Union[QuantityOrUnit, float, np.ndarray]:
    """ Converts a quantity or unit to a different unit and/or to a different
        form and/or type. 

        Parameters
        ----------
        to_unit : str, optional
            The unit to convert to.
        
        to_form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            The form to convert to.
        
        parser : {"pint", "openmm.unit", "astropy.units"}, optional
            The parser to use if a string is passed.
        
        to_type : {"quantity", "unit", "value"}, optional
            The type to convert to.

        Returns
        -------
        QuantityOrUnit or ArrayLike or float
            The converted quantity or unit. If to_type is passed the return value can
            be a float or a numpy array.
    """
    output = None

    form_in = get_form(quantity_or_unit)
    to_form = digest_to_form(to_form, form_in)
    parser = digest_parser(parser)

    if to_type not in ['unit', 'value', 'quantity']:
        raise BadCallError("to_type")

    if isinstance(to_unit, str):
        to_unit = _parse(to_unit, parser=parser, to_form=to_form)
        to_unit = dict_get_unit[to_form](to_unit)

    if form_in=='string':

        if to_form=='string':

            output = _parse(quantity_or_unit, parser=parser, to_form=parser)

            if to_unit is not None:
                output = dict_convert[parser](output, to_unit)
            if to_type == 'unit':
                if is_unit(output):
                    output=output
                else:
                    output = dict_get_unit[parser](output)
                output = dict_translate_quantity[parser]['string'](output)
            elif to_type == 'value':
                output = dict_get_value[parser](output)
                output = str(output)
            else:
                output = dict_translate_quantity[parser]['string'](output)

        else:

            output = _parse(quantity_or_unit, parser=parser, to_form=to_form)

            if to_unit is not None:
                output = dict_convert[to_form](output, to_unit)
            if to_type == 'unit':
                if is_unit(output):
                    output=output
                else:
                    output = dict_get_unit[to_form](output)
            elif to_type == 'value':
                output = dict_get_value[to_form](output)

    else:

        if to_form == 'string':

            output = quantity_or_unit

            if to_unit is not None:
                output = dict_convert[form_in](output, to_unit)

            if to_type == 'unit':
                if is_unit(output):
                    output=output
                else:
                    output = dict_get_unit[form_in](output)
                output = dict_translate_unit[form_in]['string'](output)
            elif to_type == 'value':
                output = dict_get_value[form_in](output)
                output = str(output)
            else:
                output = dict_translate_quantity[form_in]['string'](output)

        else:

            if form_in == to_form:
                output = quantity_or_unit
            else:
                if is_unit(quantity_or_unit):
                    output = dict_translate_unit[form_in][to_form](quantity_or_unit)
                else:
                    output = dict_translate_quantity[form_in][to_form](quantity_or_unit)

            if to_unit is not None:
                to_unit = convert(to_unit, to_form=to_form)
                output = dict_convert[to_form](output, to_unit)

            if to_type == 'unit':
                if is_unit(output):
                    output = output
                else:
                    output = dict_get_unit[to_form](output)
            elif to_type == 'value':
                output = dict_get_value[to_form](output)

    return output

def to_string(quantity_or_unit: Any, 
              to_unit: Optional[str]=None, 
              parser:  Optional[str]=None) -> str:
    """
    """

    return convert(quantity_or_unit, to_unit=to_unit, to_form='string', parser=parser, to_type='quantity')

def _standard_units_lstsq(solution: np.ndarray, standards: dict) -> str:
    """ Auxiliary function for get_standard_units.
        Returns standard units by using least squares method.
    """
    matrix = []
    standard_units = []

    for aux_unit, aux_dim_array in standards.items():
        standard_units.append(convert(aux_unit, to_type='unit'))
        matrix.append(aux_dim_array)

    matrix = np.array(matrix)
    x, _, _, _ = np.linalg.lstsq(matrix.T, solution, rcond=None)

    x = x.round(4)

    if np.allclose(np.dot(matrix.T, x), solution):
        output = 1
        for u, exponent in zip(standard_units, x):
            if not np.isclose(0.0, exponent):
                output *= u**exponent

        return convert(output, to_form='string', to_type='unit')

    else:

        return None

def get_standard_units(quantity_or_unit: Optional[QuantityOrUnit]=None,
                       dimensionality: Optional[dict]=None,
                       form: Optional[str]=None,
                       parser:  Optional[str]=None) -> UnitLike:
    """ Returns standard unit of the quantity or unit passed. 
    
        Parameters
        ----------
        quantity_or_unit: Any
            A quantity or unit
        
        Returns
        -------
        str
            The standard unit.
        
        Raises
        ------
        NoStandardsError
            If no standard units were defined.
    """

    form = digest_form(form)
    parser = digest_parser(parser)

    if quantity_or_unit is not None:
        dimensionality = get_dimensionality(quantity_or_unit)
    else:
        for unit in kernel.order_fundamental_units:
            if unit not in dimensionality:
                dimensionality[unit]=0

    solution = np.array([dimensionality[unit] for unit in kernel.order_fundamental_units], dtype=float)
    n_dims_solution = len(kernel.order_fundamental_units) - np.sum(np.isclose(solution, 0.0))

    output = None

    if n_dims_solution == 0:

        if len(kernel.adimensional_standards) == 0:
                raise NoStandardsError

        for standard_unit, _ in kernel.adimensional_standards.items():
            if are_compatible(quantity_or_unit, standard_unit):
                output = standard_unit
                break

    elif n_dims_solution == 1:

        for standard_unit, dim_array in kernel.dimensional_fundamental_standards.items():
            if np.allclose(solution, dim_array):
                output = standard_unit
                break

        if output is None:

            if len(kernel.tentative_base_standards) == 0:
                raise NoStandardsError

            output = _standard_units_lstsq(solution, kernel.tentative_base_standards)

    else:

        for standard_units, dim_array in kernel.dimensional_combinations_standards.items():
            if np.allclose(solution, dim_array):
                return standard_units

        if output is None:

            if len(kernel.dimensional_fundamental_standards) == 0:
                raise NoStandardsError

            output = _standard_units_lstsq(solution, kernel.dimensional_fundamental_standards)

        if output is None:

            if len(kernel.tentative_base_standards) == 0:
                raise NoStandardsError

            output = _standard_units_lstsq(solution, kernel.tentative_base_standards)

    output = convert(output, to_form=form, parser=parser, to_type='unit')

    return output

def standardize(quantity_or_unit: QuantityOrUnit,
                to_form: Optional[str]=None) -> QuantityOrUnit:
    """ Concert a quantity or unit to standard units.

        Parameters
        ----------
        quantity_or_unit : QuantityOrUnit
            The quantity or a unit that will be converted.
        
        to_form : str, optional.
            The form to transform to
        
        Returns
        -------
        QuantityOrUnit
            The quantity ot unit converted to standard units.

        Raises
        ------
        NoStandardsError
            If no standard units were defined.

    """
    to_form = digest_form(to_form)

    try:
        output = convert(quantity_or_unit, to_form=to_form)
        standard = get_standard_units(output)
        if standard is None:
            raise NoStandardsError
        output = convert(output, standard)
    except:
        standard = get_standard_units(quantity_or_unit)
        if standard is None:
            raise NoStandardsError
        output = convert(quantity_or_unit, to_unit=standard, to_form=to_form)

    return output

def check(quantity_or_unit: Any, 
          dimensionality: Optional[Dict[str, int]] = None, 
          value_type: Optional[Any] = None, 
          shape: Optional[tuple] = None, 
          unit: Optional[str] = None, 
          dtype_name: Optional[str] = None) -> bool:
    """ Check if a quantity or unit has the specified dimensionality, 
        value_type, shape, unit or data type.

        Parameters
        ---------
        quantity_or_unit: Any
            A quantity or unit object. If any other object is passed False will be returned.

        dimensionality: dict
            A dictionary specifying the dimensionality of the quantity or unit.

        value_type: Any
            The type of the quantity. Can be int, float, np.ndarray.

        shape: tuple of int
            For non scalar quantities. A tuple with the shape of the array.
        
        unit: str
            Name of the unit.
        
        dtype_name : str
            For non scalar quantities. The dtype of the array (i.e float64). 

        Returns
        -------
        bool
            True if the quantity or unit has the specified parameters.
    """

    if is_quantity(quantity_or_unit):

        if unit is not None:
            aux_unit = get_unit(quantity_or_unit)
            if not are_equal(aux_unit, unit):
                return False
        if value_type is not None:
            aux_value = get_value(quantity_or_unit)
            if not isinstance(aux_value, value_type):
                return False
        if shape is not None:
            value = get_value(quantity_or_unit)
            if np.shape(value)!=tuple(shape):
                return False
        if dimensionality is not None:
            aux_dimensionality = get_dimensionality(quantity_or_unit)
            if not _compatible_dimensionalities(aux_dimensionality, dimensionality):
                return False
        if dtype_name is not None:
            aux_value = get_value(quantity_or_unit)
            try:
                aux_dtype_name = aux_value.dtype.name
                if aux_dtype_name != dtype_name:
                    return False
            except:
                return False

    elif is_unit(quantity_or_unit):

        if unit is not None:
            if not are_equal(quantity_or_unit, unit):
                return False
        if dimensionality is not None:
            aux_dimensionality = get_dimensionality(quantity_or_unit)
            if not _compatible_dimensionalities(aux_dimensionality, dimensionality):
                return False

    else:

        return False

    return True


