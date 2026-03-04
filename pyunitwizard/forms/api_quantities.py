from typing import Any, Dict, Union

import numpy as np

from pyunitwizard._private.exceptions import LibraryNotFoundError, LibraryWithoutParserError
from pyunitwizard._private.quantity_or_unit import ArrayLike

try:
    import quantities as pq
    from quantities.quantity import Quantity as QuantitiesQuantity
    from quantities.unitquantity import UnitQuantity
except Exception as exc:  # pragma: no cover - optional dependency
    raise LibraryNotFoundError("quantities") from exc

form_name = "quantities"
parser = False


def _is_quantity_obj(obj: Any) -> bool:
    return isinstance(obj, QuantitiesQuantity)


def _is_scalar_magnitude_one(obj: QuantitiesQuantity) -> bool:
    mag = np.asarray(obj.magnitude)
    return mag.shape in [(), (1,)] and float(mag) == 1.0


def is_form(quantity_or_unit: Any) -> bool:
    return is_quantity(quantity_or_unit) or is_unit(quantity_or_unit)


def is_unit(quantity_or_unit: Any) -> bool:
    if isinstance(quantity_or_unit, UnitQuantity):
        return True
    if _is_quantity_obj(quantity_or_unit):
        return _is_scalar_magnitude_one(quantity_or_unit)
    return False


def is_quantity(quantity_or_unit: Any) -> bool:
    return _is_quantity_obj(quantity_or_unit)


def dimensionality(quantity_or_unit: QuantitiesQuantity) -> Dict[str, int]:
    from .api_pint import dimensionality as dimensionality_pint

    return dimensionality_pint(quantity_to_pint(quantity_or_unit))


def compatibility(quantity_or_unit_1: QuantitiesQuantity, quantity_or_unit_2: QuantitiesQuantity) -> bool:
    return dimensionality(quantity_or_unit_1) == dimensionality(quantity_or_unit_2)


def make_quantity(value: Union[int, float, ArrayLike], unit: Union[str, QuantitiesQuantity]) -> QuantitiesQuantity:
    from .api_pint import make_quantity as make_pint_quantity

    if isinstance(unit, str):
        pint_quantity = make_pint_quantity(value, unit)
        return quantity_to_quantities(pint_quantity)
    return value * unit


def get_value(quantity: QuantitiesQuantity) -> Union[int, float, ArrayLike]:
    return quantity.magnitude


def get_unit(quantity: QuantitiesQuantity) -> QuantitiesQuantity:
    if is_unit(quantity):
        return quantity
    return quantity.units


def change_value(quantity: QuantitiesQuantity, value: Union[int, float, ArrayLike]) -> QuantitiesQuantity:
    return make_quantity(value, get_unit(quantity))


def convert(quantity_or_unit: QuantitiesQuantity, unit: Union[str, QuantitiesQuantity]) -> QuantitiesQuantity:
    from .api_pint import convert as pint_convert

    if is_unit(quantity_or_unit):
        source_quantity = make_quantity(1.0, quantity_or_unit)
        converted = convert(source_quantity, unit)
        return get_unit(converted)

    pint_quantity = quantity_to_pint(quantity_or_unit)
    pint_target = unit_to_pint(unit) if not isinstance(unit, str) else unit
    pint_converted = pint_convert(pint_quantity, pint_target)
    return quantity_to_quantities(pint_converted)


def string_to_quantity(string: str):
    raise LibraryWithoutParserError("quantities")


def string_to_unit(string: str):
    raise LibraryWithoutParserError("quantities")


def quantity_to_string(quantity: QuantitiesQuantity) -> str:
    return str(quantity)


def unit_to_string(unit: QuantitiesQuantity) -> str:
    if isinstance(unit, UnitQuantity):
        return str(unit.symbol)
    return str(unit.dimensionality)


def quantity_to_pint(quantity_or_unit: QuantitiesQuantity):
    from .api_pint import make_quantity as make_pint_quantity

    if is_unit(quantity_or_unit):
        return make_pint_quantity(1.0, unit_to_string(quantity_or_unit))

    simplified = quantity_or_unit.simplified
    return make_pint_quantity(simplified.magnitude, str(simplified.dimensionality))


def unit_to_pint(unit: QuantitiesQuantity):
    from .api_pint import get_unit as get_pint_unit

    return get_pint_unit(quantity_to_pint(unit))


def quantity_to_quantities(quantity):
    from .api_pint import convert as pint_convert

    quantity = pint_convert(quantity, quantity.units)
    quantity = quantity.to_base_units()
    unit_expr = f"{quantity.units:~}"
    unit_obj = eval(unit_expr, {}, pq.__dict__)
    return quantity.magnitude * unit_obj


def unit_to_quantities(unit):
    from .api_pint import make_quantity as make_pint_quantity

    pint_quantity = make_pint_quantity(1.0, str(unit))
    return get_unit(quantity_to_quantities(pint_quantity))


def quantity_to_openmm_unit(quantity: QuantitiesQuantity):
    from .api_pint import quantity_to_openmm_unit as pint_to_openmm

    return pint_to_openmm(quantity_to_pint(quantity))


def unit_to_openmm_unit(unit: QuantitiesQuantity):
    from .api_openmm_unit import get_unit as get_openmm_unit

    quantity = quantity_to_openmm_unit(unit)
    return get_openmm_unit(quantity)


def quantity_to_unyt(quantity: QuantitiesQuantity):
    from .api_pint import quantity_to_unyt as pint_to_unyt

    return pint_to_unyt(quantity_to_pint(quantity))


def unit_to_unyt(unit: QuantitiesQuantity):
    from .api_unyt import get_unit as get_unyt_unit

    quantity = quantity_to_unyt(unit)
    return get_unyt_unit(quantity)


def quantity_to_astropy_units(quantity: QuantitiesQuantity):
    from .api_pint import quantity_to_astropy_units as pint_to_astropy

    return pint_to_astropy(quantity_to_pint(quantity))


def unit_to_astropy_units(unit: QuantitiesQuantity):
    from .api_astropy_unit import get_unit as get_astropy_unit

    quantity = quantity_to_astropy_units(unit)
    return get_astropy_unit(quantity)


def quantity_to_physipy(quantity: QuantitiesQuantity):
    from .api_pint import quantity_to_physipy as pint_to_physipy

    return pint_to_physipy(quantity_to_pint(quantity))


def unit_to_physipy(unit: QuantitiesQuantity):
    from .api_physipy import get_unit as get_physipy_unit

    quantity = quantity_to_physipy(unit)
    return get_physipy_unit(quantity)
