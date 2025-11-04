from .._private.quantity_or_unit import ArrayLike, QuantityOrUnit, QuantityLike, UnitLike
from typing import Any, Dict, Optional, Union, Tuple

_constants = {
        'Avogadro': [6.02214076e+23, '1/mole'],
        'Universal gas': [8.31446261815324, 'J/(kelvin*mole)'], # Avogadro * Boltzmann
        'Boltzmann': [1.380649e-23, 'J/kelvin'],
        }

_constants_synonyms = {
        'NA': 'Avogadro',
        'R': 'Universal gas',
        'Molar gas': 'Universal gas',
        'KB': 'Boltzmann',
        }


def get_constant(constant_name: str,
                to_unit:  Optional[str]=None,
                to_form: Optional[str]=None,
                standardized: Optional[bool]=False)-> QuantityLike:

    if constant_name in _constants_synonyms:
        constant_name = _constants_synonyms[constant_name]

    try:

        value, unit = _constants[constant_name]
        output = quantity(value, unit, form=to_form, standardized=standardized)
        if to_unit is not None:
            output = convert(output, to_unit=to_unit)

        return output

    except:

        raise ValueError

def show_constants()-> dict:

    output = {}

    for constant_name, constant_value in _constants.items():
        names = [constant_name]
        value = f'{constant_value[0]} {constant_value[1]}'
        for ii, jj in _constants_synonyms.items():
            if jj==constant_name:
                names.append(ii)
        output[tuple(names)]=value

    return output

