from __future__ import annotations

from contextlib import contextmanager

import numpy as np


def _iterable_values(obj):
    if isinstance(obj, (list, tuple)):
        return obj
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return None


def _first_quantity_like(obj):
    import pyunitwizard as puw

    if puw.is_quantity(obj) or puw.is_unit(obj):
        return obj

    values = _iterable_values(obj)
    if values is None:
        return None

    for item in values:
        if puw.is_quantity(item) or puw.is_unit(item):
            return item
    return None


class _PyUnitWizardMplConverter:
    @staticmethod
    def default_units(x, axis):
        import pyunitwizard as puw

        first = _first_quantity_like(x)
        if first is None:
            return None

        if puw.is_quantity(first):
            unit = puw.get_unit(first)
        else:
            unit = first

        if axis.units is not None and not puw.are_compatible(unit, axis.units):
            raise ValueError("Incompatible units for shared matplotlib axis")
        return unit

    @staticmethod
    def axisinfo(unit, axis):
        import matplotlib.units as munits
        import pyunitwizard as puw

        label = puw.convert(unit, to_form="string", to_type="unit")
        return munits.AxisInfo(label=f"{label}")

    def convert(self, value, unit, axis):
        import pyunitwizard as puw

        if puw.is_quantity(value):
            return puw.get_value(value, to_unit=unit)
        if puw.is_unit(value):
            return puw.get_value(puw.quantity(1.0, value), to_unit=unit)

        values = _iterable_values(value)
        if values is not None:
            return [self.convert(item, unit, axis) for item in values]

        return value


def _discover_mpl_types():
    types = []

    try:
        import pint

        types.append(pint.Quantity)
    except Exception:
        pass

    try:
        import openmm.unit as openmm_unit

        types.append(openmm_unit.Quantity)
    except Exception:
        pass

    try:
        import unyt

        types.extend([unyt.unyt_array, unyt.unyt_quantity])
    except Exception:
        pass

    try:
        from astropy import units as astropy_units

        types.append(astropy_units.Quantity)
    except Exception:
        pass

    try:
        from physipy.quantity.quantity import Quantity as PhysipyQuantity

        types.append(PhysipyQuantity)
    except Exception:
        pass

    try:
        import quantities as pq

        types.append(pq.quantity.Quantity)
    except Exception:
        pass

    return tuple(dict.fromkeys(types))


def setup_matplotlib(enable: bool = True) -> None:
    """Enable or disable PyUnitWizard converters in matplotlib.

    Parameters
    ----------
    enable : bool, default=True
        ``True`` registers converters for supported quantity classes.
        ``False`` unregisters those converters.
    """
    import matplotlib.units as munits

    quantity_types = _discover_mpl_types()
    if enable:
        converter = _PyUnitWizardMplConverter()
        for cls in quantity_types:
            munits.registry[cls] = converter
    else:
        for cls in quantity_types:
            munits.registry.pop(cls, None)


@contextmanager
def plotting_context():
    """Temporarily register PyUnitWizard converters in matplotlib."""
    import matplotlib.units as munits

    quantity_types = _discover_mpl_types()
    previous = {cls: munits.registry.get(cls) for cls in quantity_types}
    setup_matplotlib(enable=True)
    try:
        yield
    finally:
        for cls in quantity_types:
            old = previous[cls]
            if old is None:
                munits.registry.pop(cls, None)
            else:
                munits.registry[cls] = old


__all__ = ["setup_matplotlib", "plotting_context"]
