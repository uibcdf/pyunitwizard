"""Keep inclusive cutoffs distinct when converting verified Pint lengths."""

from fractions import Fraction
from itertools import product

import numpy as np
import pint
import pytest

import pyunitwizard as puw
from pyunitwizard.forms import api_pint

# MolSysMT #666 covers these three exact scales and all nine source/target pairs.
_SCALE = {"nm": Fraction(1, 10**9), "angstrom": Fraction(1, 10**10), "pm": Fraction(1, 10**12)}


@pytest.mark.parametrize(("source", "target"), product(_SCALE, repeat=2))
@pytest.mark.parametrize("standard", _SCALE)
def test_pint_length_boundaries_round_once(source, target, standard):
    distance = Fraction(1, 2) * _SCALE["nm"]
    equal = float(distance / _SCALE[source])
    values = np.array([[np.nextafter(equal, -np.inf), equal, np.nextafter(equal, np.inf)]])
    expected = np.array([[float(Fraction(float(x)) * _SCALE[source] / _SCALE[target]) for x in values[0]]])
    distance_in_target = float(distance / _SCALE[target])

    with puw.context(default_form="pint", default_parser="pint", standard_units=[standard, "ps"]):
        standards = puw.configure.get_standard_units()
        quantity = puw.quantity(values.copy(), source)
        source_unit = quantity.units
        target_unit = puw.unit(target)
        converted = puw.convert(quantity, to_unit=target_unit)
        extracted = puw.get_value(quantity, to_unit=target)
        scalars = [puw.get_value(puw.quantity(float(x), source), to_unit=target) for x in values[0]]

        assert converted.units == target_unit
        assert extracted.shape == values.shape
        assert extracted.dtype == np.float64
        np.testing.assert_array_equal(converted.magnitude.view(np.uint64), expected.view(np.uint64))
        np.testing.assert_array_equal(extracted.view(np.uint64), expected.view(np.uint64))
        np.testing.assert_array_equal(np.array(scalars).view(np.uint64), expected[0].view(np.uint64))
        assert (distance_in_target <= extracted).tolist() == [[False, True, True]]
        np.testing.assert_array_equal(quantity.magnitude.view(np.uint64), values.view(np.uint64))
        assert quantity.units == source_unit
        assert puw.configure.get_standard_units() == standards


@pytest.mark.parametrize(("value", "unit"), [(5, "Å"), (500, "pm")])
def test_pint_integer_cutoffs_in_quantities_and_strings(value, unit):
    with puw.context(default_form="pint", default_parser="pint"):
        assert puw.get_value(puw.quantity(value, unit), to_unit="nm") == 0.5
        assert puw.convert(f"{value} {unit}", to_unit="nm", to_form="pint").magnitude == 0.5


def test_pint_length_rounding_at_float64_range_edges():
    tiny = np.nextafter(0.0, 1.0)
    values = np.array([-0.0, -tiny, tiny, np.finfo(np.float64).tiny])
    expected = np.array([-0.0, -0.0, 0.0, float(Fraction(float(values[-1])) / 1000)])
    with puw.context(default_form="pint", default_parser="pint"), np.errstate(over="ignore", under="ignore"):
        result = puw.get_value(puw.quantity(values, "pm"), to_unit="nm")
        assert np.isposinf(puw.get_value(puw.quantity(np.array([np.finfo(np.float64).max]), "nm"), to_unit="pm")).all()
    np.testing.assert_array_equal(result.view(np.uint64), expected.view(np.uint64))


def test_pint_length_float32_keeps_native_arithmetic():
    with puw.context(default_form="pint", default_parser="pint"):
        quantity = puw.quantity(np.array([5, 7], dtype=np.float32), "angstrom")
        expected = quantity.to("nm").magnitude
        actual = puw.get_value(quantity, to_unit="nm")
        assert actual.dtype == expected.dtype
        np.testing.assert_array_equal(actual, expected)


def test_approximate_foreign_registry_match_keeps_native_conversion():
    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("angstrom = 1.0000000000001e-10 * meter")
    quantity = foreign.Quantity(5.0, "angstrom")
    # Compatibility normalization accepts this small definition difference.
    # An approximate registry match cannot establish the exact-scale guarantee.
    expected = api_pint.ureg.Quantity(5.0, "angstrom").to("nm").magnitude
    assert puw.get_value(quantity, to_unit="nm", parser="pint") == expected
    assert puw.convert(quantity, to_form="record", to_unit="nm", to_type="value", parser="pint") == expected


def test_active_pint_context_can_redefine_a_length_scale():
    context = pint.Context("custom_length_scale")
    context.redefine("angstrom = 2e-10 * meter")
    with puw.context(default_form="pint", default_parser="pint"), api_pint.ureg.context(context):
        quantity = puw.quantity(5.0, "angstrom")
        expected = quantity.to("nm").magnitude
        assert expected == pytest.approx(1.0)
        assert puw.get_value(quantity, to_unit="nm") == expected
