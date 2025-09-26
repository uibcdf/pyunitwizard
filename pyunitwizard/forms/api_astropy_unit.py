from typing import Any, Dict, Union

from pyunitwizard._private.exceptions import LibraryNotFoundError
from pyunitwizard._private.quantity_or_unit import ArrayLike

try:
    from astropy import units as astropy_units
except Exception as exc:  # pragma: no cover - handled through exception
    raise LibraryNotFoundError('astropy') from exc

AstropyQuantity = astropy_units.Quantity
AstropyUnitBase = astropy_units.UnitBase

form_name = 'astropy.units'
parser = True

is_form = {
    AstropyQuantity: form_name,
    AstropyUnitBase: form_name,
}


def _to_unit(quantity_or_unit: Union[AstropyQuantity, AstropyUnitBase]) -> AstropyUnitBase:
    if is_quantity(quantity_or_unit):
        return get_unit(quantity_or_unit)
    if is_unit(quantity_or_unit):
        return quantity_or_unit
    raise TypeError('Expected an astropy quantity or unit')


def is_quantity(quantity_or_unit: Any) -> bool:
    return isinstance(quantity_or_unit, AstropyQuantity)


def is_unit(quantity_or_unit: Any) -> bool:
    return isinstance(quantity_or_unit, AstropyUnitBase)


_dimensions_translator = {
    'm': '[L]',
    'kg': '[M]',
    's': '[T]',
    'K': '[K]',
    'mol': '[mol]',
    'A': '[A]',
    'cd': '[Cd]',
}


def dimensionality(quantity_or_unit: Union[AstropyQuantity, AstropyUnitBase]) -> Dict[str, float]:
    unit = _to_unit(quantity_or_unit)
    decomposed = unit.decompose(bases=astropy_units.si.bases)
    dimensionality_dict = {'[L]': 0, '[M]': 0, '[T]': 0, '[K]': 0, '[mol]': 0, '[A]': 0, '[Cd]': 0}

    for base, power in zip(decomposed.bases, decomposed.powers):
        key = _dimensions_translator.get(base.to_string())
        if key is None:
            raise ValueError(f"Unrecognized base unit: {base.to_string()} in {unit}")
        dimensionality_dict[key] += float(power)

    return dimensionality_dict


def compatibility(quantity_or_unit_1: Union[AstropyQuantity, AstropyUnitBase],
                  quantity_or_unit_2: Union[AstropyQuantity, AstropyUnitBase]) -> bool:
    unit_1 = _to_unit(quantity_or_unit_1)
    unit_2 = _to_unit(quantity_or_unit_2)
    return unit_1.is_equivalent(unit_2)


def make_quantity(value: Union[int, float, ArrayLike],
                  unit: Union[str, AstropyUnitBase]) -> AstropyQuantity:
    unit_obj = astropy_units.Unit(unit)
    return astropy_units.Quantity(value, unit_obj)


def get_value(quantity: AstropyQuantity) -> Union[int, float, ArrayLike]:
    return quantity.value


def get_unit(quantity: AstropyQuantity) -> AstropyUnitBase:
    return quantity.unit


def change_value(quantity: AstropyQuantity,
                 value: Union[int, float, ArrayLike]) -> AstropyQuantity:
    return make_quantity(value, get_unit(quantity))


def convert(quantity: AstropyQuantity,
            unit: Union[str, AstropyUnitBase]) -> AstropyQuantity:
    unit_obj = astropy_units.Unit(unit)
    return quantity.to(unit_obj)


# Parser

def string_to_quantity(string: str) -> AstropyQuantity:
    return astropy_units.Quantity(string)


def string_to_unit(string: str) -> AstropyUnitBase:
    return astropy_units.Unit(string)


# To string

def quantity_to_string(quantity: AstropyQuantity) -> str:
    return str(quantity)


def unit_to_string(unit: AstropyUnitBase) -> str:
    return unit.to_string()


# To pint

def quantity_to_pint(quantity: AstropyQuantity):
    from .api_pint import make_quantity as make_pint_quantity

    value = get_value(quantity)
    unit_name = unit_to_string(get_unit(quantity))
    return make_pint_quantity(value, unit_name)


def unit_to_pint(unit: AstropyUnitBase):
    from .api_pint import get_unit as get_pint_unit

    quantity = quantity_to_pint(1.0 * unit)
    return get_pint_unit(quantity)


# To openmm.unit

def quantity_to_openmm_unit(quantity: AstropyQuantity):
    from .api_pint import quantity_to_openmm_unit as pint_to_openmm_unit

    pint_quantity = quantity_to_pint(quantity)
    return pint_to_openmm_unit(pint_quantity)


def unit_to_openmm_unit(unit: AstropyUnitBase):
    from .api_openmm_unit import get_unit as get_openmm_unit

    quantity = quantity_to_openmm_unit(1.0 * unit)
    return get_openmm_unit(quantity)


# To unyt

def quantity_to_unyt(quantity: AstropyQuantity):
    from .api_pint import quantity_to_unyt as pint_to_unyt

    pint_quantity = quantity_to_pint(quantity)
    return pint_to_unyt(pint_quantity)


def unit_to_unyt(unit: AstropyUnitBase):
    from .api_unyt import get_unit as get_unyt_unit

    quantity = quantity_to_unyt(1.0 * unit)
    return get_unyt_unit(quantity)
