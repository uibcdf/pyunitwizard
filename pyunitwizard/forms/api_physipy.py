from typing import Any, Dict, Union

import numpy as np

from pyunitwizard._private.exceptions import LibraryNotFoundError, LibraryWithoutParserError
from pyunitwizard._private.quantity_or_unit import ArrayLike

try:
    import physipy
    from physipy import units as physipy_units
    from physipy.quantity.quantity import Quantity as PhysipyQuantity
except Exception as exc:  # pragma: no cover - optional dependency
    raise LibraryNotFoundError("physipy") from exc

form_name = "physipy"
parser = False

_DIMENSIONS_TRANSLATOR = {
    "L": "[L]",
    "M": "[M]",
    "T": "[T]",
    "I": "[A]",
    "theta": "[K]",
    "N": "[mol]",
    "J": "[Cd]",
}


def _empty_dimensionality_dict() -> Dict[str, int]:
    return {"[L]": 0, "[M]": 0, "[T]": 0, "[K]": 0, "[mol]": 0, "[A]": 0, "[Cd]": 0}


def _is_physipy_quantity(obj: Any) -> bool:
    return isinstance(obj, PhysipyQuantity)


def is_form(quantity_or_unit: Any) -> bool:
    return is_quantity(quantity_or_unit) or is_unit(quantity_or_unit)


def is_unit(quantity_or_unit: Any) -> bool:
    if not _is_physipy_quantity(quantity_or_unit):
        return False
    if not np.isscalar(getattr(quantity_or_unit, "value", None)):
        return False
    symbol = str(getattr(quantity_or_unit, "symbol", ""))
    return symbol != "UndefinedSymbol" and not symbol.startswith("UndefinedSymbol*")


def is_quantity(quantity_or_unit: Any) -> bool:
    return _is_physipy_quantity(quantity_or_unit) and not is_unit(quantity_or_unit)


def dimensionality(quantity_or_unit: PhysipyQuantity) -> Dict[str, int]:
    out = _empty_dimensionality_dict()
    for dim_symbol, exponent in quantity_or_unit.dimension.dim_dict.items():
        if dim_symbol in _DIMENSIONS_TRANSLATOR:
            out[_DIMENSIONS_TRANSLATOR[dim_symbol]] = exponent
    return out


def compatibility(quantity_or_unit_1: PhysipyQuantity, quantity_or_unit_2: PhysipyQuantity) -> bool:
    return dimensionality(quantity_or_unit_1) == dimensionality(quantity_or_unit_2)


def unit_to_string(unit: PhysipyQuantity) -> str:
    symbol = str(getattr(unit, "symbol", ""))
    if symbol and symbol != "UndefinedSymbol":
        return symbol
    return unit.dimension.str_SI_unit()


def make_quantity(value: Union[int, float, ArrayLike], unit: Union[str, PhysipyQuantity]) -> PhysipyQuantity:
    from .api_pint import make_quantity as make_pint_quantity

    if is_unit(unit):
        unit_name = unit_to_string(unit)
    else:
        unit_name = unit
    pint_quantity = make_pint_quantity(value, unit_name)
    return quantity_to_physipy(pint_quantity)


def get_value(quantity: PhysipyQuantity) -> Union[int, float, ArrayLike]:
    return quantity.value


def get_unit(quantity: PhysipyQuantity) -> PhysipyQuantity:
    if is_unit(quantity):
        return quantity
    favunit = getattr(quantity, "favunit", None)
    if favunit is not None:
        return favunit
    return quantity._SI_unitary_quantity


def change_value(quantity: PhysipyQuantity, value: Union[int, float, ArrayLike]) -> PhysipyQuantity:
    return make_quantity(value, get_unit(quantity))


def convert(quantity_or_unit: PhysipyQuantity, unit: Union[str, PhysipyQuantity]) -> PhysipyQuantity:
    from .api_pint import convert as pint_convert

    if is_unit(quantity_or_unit):
        source_quantity = make_quantity(1.0, quantity_or_unit)
        converted = convert(source_quantity, unit)
        return get_unit(converted)

    pint_quantity = quantity_to_pint(quantity_or_unit)
    pint_target = unit_to_pint(unit) if not isinstance(unit, str) else unit
    pint_converted = pint_convert(pint_quantity, pint_target)
    return quantity_to_physipy(pint_converted)


def string_to_quantity(string: str):
    raise LibraryWithoutParserError("physipy")


def string_to_unit(string: str):
    raise LibraryWithoutParserError("physipy")


def quantity_to_string(quantity: PhysipyQuantity) -> str:
    return str(quantity)


def quantity_to_pint(quantity_or_unit: PhysipyQuantity):
    from .api_pint import make_quantity as make_pint_quantity

    if is_unit(quantity_or_unit):
        return make_pint_quantity(1.0, unit_to_string(quantity_or_unit))

    unit_obj = get_unit(quantity_or_unit)
    unit_name = unit_to_string(unit_obj)
    magnitude = quantity_or_unit.value / unit_obj.value
    return make_pint_quantity(magnitude, unit_name)


def unit_to_pint(unit: PhysipyQuantity):
    from .api_pint import get_unit as get_pint_unit

    pint_quantity = quantity_to_pint(unit)
    return get_pint_unit(pint_quantity)


def quantity_to_physipy(quantity):
    from .api_pint import get_unit as get_pint_unit
    from .api_pint import get_value as get_pint_value

    unit_expr = f"{get_pint_unit(quantity):~}"
    physipy_unit = eval(unit_expr, {}, physipy_units)
    value_si = get_pint_value(quantity) * physipy_unit.value
    return PhysipyQuantity(value_si, physipy_unit.dimension, favunit=physipy_unit)


def unit_to_physipy(unit):
    from .api_pint import make_quantity as make_pint_quantity

    pint_quantity = make_pint_quantity(1.0, str(unit))
    return get_unit(quantity_to_physipy(pint_quantity))


def quantity_to_openmm_unit(quantity: PhysipyQuantity):
    from .api_pint import quantity_to_openmm_unit as pint_to_openmm

    return pint_to_openmm(quantity_to_pint(quantity))


def unit_to_openmm_unit(unit: PhysipyQuantity):
    from .api_openmm_unit import get_unit as get_openmm_unit

    quantity = quantity_to_openmm_unit(unit)
    return get_openmm_unit(quantity)


def quantity_to_unyt(quantity: PhysipyQuantity):
    from .api_pint import quantity_to_unyt as pint_to_unyt

    return pint_to_unyt(quantity_to_pint(quantity))


def unit_to_unyt(unit: PhysipyQuantity):
    from .api_unyt import get_unit as get_unyt_unit

    quantity = quantity_to_unyt(unit)
    return get_unyt_unit(quantity)


def quantity_to_astropy_units(quantity: PhysipyQuantity):
    from .api_pint import quantity_to_astropy_units as pint_to_astropy

    return pint_to_astropy(quantity_to_pint(quantity))


def unit_to_astropy_units(unit: PhysipyQuantity):
    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(unit)
    return get_astropy_unit(quantity)


def quantity_to_quantities(quantity: PhysipyQuantity):
    from .api_pint import quantity_to_quantities as pint_to_quantities

    return pint_to_quantities(quantity_to_pint(quantity))


def unit_to_quantities(unit: PhysipyQuantity):
    from .api_quantities import get_unit as get_quantities_unit

    quantity = quantity_to_quantities(unit)
    return get_quantities_unit(quantity)
