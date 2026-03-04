# TypeVars to represent unit, quantities and arraylike objects

from typing import TypeVar
import numpy as np

quantity_types=[]
unit_types=[]
quantity_or_unit_types=[]

try:
    import pint
    quantity_types.append(pint.Quantity)
    unit_types.append(pint.Unit)
except:
    pass

try:
    import openmm.unit as openmm_unit
    quantity_types.append(openmm_unit.Quantity)
    unit_types.append(openmm_unit.Unit)
except:
    pass

try:
    import unyt
    quantity_types.append(unyt.unyt_quantity)
    unit_types.append(unyt.Unit)
except:
    pass

try:
    from astropy import units as astropy_units
    quantity_types.append(astropy_units.Quantity)
    unit_types.append(astropy_units.UnitBase)
except:
    pass

try:
    from physipy.quantity.quantity import Quantity as physipy_quantity
    quantity_types.append(physipy_quantity)
    unit_types.append(physipy_quantity)
except:
    pass

try:
    import quantities as pq
    quantity_types.append(pq.quantity.Quantity)
    unit_types.append(pq.quantity.Quantity)
except:
    pass

quantity_or_unit_types = quantity_types + unit_types + [str]
quantity_types.append(str)
unit_types.append(str)

ArrayLike = TypeVar("ArrayLike",
                    tuple,
                    list,
                    np.ndarray)

QuantityLike = TypeVar("QuantityLike",
                    *quantity_types)

UnitLike = TypeVar("UnitLike",
                str,
                *unit_types)

QuantityOrUnit = TypeVar("QuantityOrUnit",
                str,
                *quantity_or_unit_types)
