import pyunitwizard as puw
import pytest


@pytest.fixture(autouse=True)
def configure_pint():
    loaded_libraries = list(puw.configure.get_libraries_loaded())
    default_form = puw.configure.get_default_form()
    default_parser = puw.configure.get_default_parser()
    standard_units = list(puw.configure.get_standard_units().keys())

    puw.configure.reset()
    puw.configure.load_library('pint')
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    yield

    puw.configure.reset()

    if loaded_libraries:
        puw.configure.load_library(loaded_libraries)

    if standard_units:
        puw.configure.set_standard_units(standard_units)

    if default_form is not None:
        puw.configure.set_default_form(default_form)

    if default_parser is not None:
        puw.configure.set_default_parser(default_parser)


@pytest.fixture
def constants_module(monkeypatch):
    from pyunitwizard.constants import constants as const_mod

    monkeypatch.setattr(const_mod, 'quantity', puw.quantity, raising=False)
    monkeypatch.setattr(const_mod, 'convert', puw.convert, raising=False)

    return const_mod


def test_get_constant_synonym_and_conversion(constants_module):
    universal = constants_module.get_constant('R', to_unit='kJ/(mole*kelvin)')
    value, unit = puw.get_value_and_unit(universal, to_form='string')

    assert value == pytest.approx(0.00813446, rel=1e-6)
    assert unit == 'kilojoule / kelvin / mole'


def test_get_constant_standardized_string_form(constants_module):
    raw = constants_module.get_constant('Avogadro')
    standardized = constants_module.get_constant('NA', standardized=True)

    assert puw.are_equal(standardized, puw.standardize(raw))

    string_form = constants_module.get_constant('NA', to_form='string')
    assert string_form == '6.02214076e+23 / mole'


def test_get_constant_unknown_raises(constants_module):
    with pytest.raises(ValueError):
        constants_module.get_constant('Unknown constant')


def test_show_constants_lists_synonyms(constants_module):
    registry = constants_module.show_constants()

    assert ('Avogadro', 'NA') in registry
    assert registry[('Universal gas', 'R', 'Molar gas')] == '8.13446261815324 J/(kelvin*mole)'
