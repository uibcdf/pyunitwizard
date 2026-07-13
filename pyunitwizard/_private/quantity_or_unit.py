from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias


if TYPE_CHECKING:
    import numpy as np
    import openmm.unit as openmm_unit
    import pint
    import quantities as pq
    import unyt
    from astropy import units as astropy_units
    from physipy.quantity.quantity import Quantity as PhysipyQuantity

    ArrayLike: TypeAlias = tuple | list | np.ndarray
    QuantityLike: TypeAlias = (
        pint.Quantity
        | openmm_unit.Quantity
        | unyt.unyt_quantity
        | astropy_units.Quantity
        | PhysipyQuantity
        | pq.quantity.Quantity
        | str
    )
    UnitLike: TypeAlias = (
        pint.Unit
        | openmm_unit.Unit
        | unyt.Unit
        | astropy_units.UnitBase
        | PhysipyQuantity
        | pq.quantity.Quantity
        | str
    )
    QuantityOrUnit: TypeAlias = QuantityLike | UnitLike
else:
    ArrayLike: TypeAlias = Any
    QuantityLike: TypeAlias = Any
    UnitLike: TypeAlias = Any
    QuantityOrUnit: TypeAlias = Any
