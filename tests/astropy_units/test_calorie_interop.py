"""Thermochemical calories retain their meaning at every Astropy boundary."""

import subprocess
import sys

import pytest

pytest.importorskip("astropy.units")
pytest.importorskip("openmm.unit")
pytest.importorskip("unyt")

import pyunitwizard as puw
from pyunitwizard.forms import api_astropy_unit

FORMS = ["pint", "openmm.unit", "unyt", "astropy.units"]


@pytest.mark.parametrize("source_form", FORMS)
@pytest.mark.parametrize("default_form", FORMS)
def test_energy_per_mole_with_every_source_and_default(source_form, default_form):
    with puw.context(default_form=default_form, default_parser="pint"):
        quantity = puw.quantity(12.552, "kJ/mol", form=source_form)
        assert puw.get_value(quantity, to_unit="kcal/mol", value_type=float) == pytest.approx(3)
        target = puw.unit("kcal/mol")
        assert puw.get_form(target) == default_form
        assert puw.get_dimensionality(quantity) == puw.get_dimensionality(target)
        converted = puw.convert(quantity, to_form=default_form, to_unit=target)
        assert puw.get_value(converted, to_unit="kJ/mol", value_type=float) == pytest.approx(12.552)


@pytest.mark.parametrize("name,scale", [("cal", 4.184), ("calorie", 4.184), ("kcal", 4184), ("kilocalorie", 4184)])
def test_native_parser_and_unit_objects_use_thermochemical_calories(name, scale):
    from astropy import units as u

    unit = api_astropy_unit.string_to_unit(name + "/mol")
    assert unit.to(u.J / u.mol) == pytest.approx(scale)
    quantity = api_astropy_unit.string_to_quantity("-2.5 " + name + "/mol")
    assert quantity.value == -2.5
    assert quantity.to_value(u.J / u.mol) == pytest.approx(-2.5 * scale)
    assert api_astropy_unit.make_quantity(2, unit).to_value(u.J / u.mol) == pytest.approx(2 * scale)
    assert api_astropy_unit.convert(12.552 * u.kJ / u.mol, "kcal/mol").value == pytest.approx(3)


def test_calorie_parsing_preserves_application_policy_and_native_registry():
    from astropy import units as u

    with puw.context(default_form="unyt", default_parser="astropy.units"):
        quantity = puw.quantity("3 kcal/mol", form="astropy.units")
        assert quantity.to_value(u.kJ / u.mol) == pytest.approx(12.552)
        assert puw.get_form(puw.quantity(1, "nm")) == "unyt"
    for spelling in ("cal", "kcal"):
        with pytest.raises(ValueError):
            u.Unit(spelling)
    with pytest.raises(ValueError):
        api_astropy_unit.string_to_unit("kcal / nonexistent_unit")
    with pytest.raises(ValueError):
        u.Unit("kcal")
    with pytest.raises(u.UnitConversionError):
        api_astropy_unit.convert(1 * u.m, "kcal/mol")


def test_conflicting_astropy_calorie_definition_is_not_overwritten():
    from astropy import units as u

    wrong = u.def_unit("kcal", 1000 * u.J)
    with u.add_enabled_units([wrong]):
        with pytest.raises(ValueError):
            api_astropy_unit.string_to_unit("kcal/mol")
        assert u.Unit("kcal").to(u.J) == 1000
    with pytest.raises(ValueError):
        api_astropy_unit.unit_to_pint(wrong / u.mol)


def test_foreign_pint_calorie_scale_cannot_be_silently_relabelled():
    import pint

    registry = pint.UnitRegistry()
    registry.define("calorie = 5 * joule = cal")
    with pytest.raises(ValueError):
        puw.convert(registry.Quantity(3, "kcal/mol"), to_form="astropy.units")


def test_first_astropy_use_in_a_fresh_process_needs_no_manual_enable():
    script = """
from astropy import units as u
import pyunitwizard as puw
with puw.context(default_form='astropy.units'):
    q = puw.quantity(3, 'kcal/mol')
    assert abs(q.to_value(u.kJ/u.mol) - 12.552) < 1e-12
try:
    u.Unit('kcal')
except ValueError:
    pass
else:
    raise AssertionError('Astropy global calorie registration leaked')
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_modified_shared_pint_calorie_is_not_silently_relabelled():
    script = """
import pyunitwizard as puw
from pyunitwizard.forms.api_pint import ureg
ureg.define('calorie = 5 * joule = cal')
try:
    puw.convert(ureg.Quantity(3, 'kcal/mol'), to_form='astropy.units')
except ValueError:
    pass
else:
    raise AssertionError('Changed shared calorie definition was silently relabelled')
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
