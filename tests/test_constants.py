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


def test_get_constant_synonym_and_conversion():
    universal = puw.constants.get_constant('R', to_unit='kJ/(mole*kelvin)')
    value, unit = puw.get_value_and_unit(universal, to_form='string')

    assert value == pytest.approx(0.00831446261815324, rel=1e-6)
    assert unit == 'kilojoule / kelvin / mole'


def test_get_constant_standardized_string_form():
    raw = puw.constants.get_constant('Avogadro')
    standardized = puw.constants.get_constant('NA', standardized=True)

    assert puw.are_equal(standardized, puw.standardize(raw))

    string_form = puw.constants.get_constant('NA', to_form='string')
    assert string_form == '6.02214076e+23 / mole'


def test_get_constant_unknown_raises():
    with pytest.raises(ValueError):
        puw.constants.get_constant('Unknown constant')


def test_show_constants_lists_synonyms():
    registry = puw.constants.show_constants()

    assert ('Avogadro', 'NA') in registry
    assert registry[('Universal gas', 'R', 'Molar gas')] == '8.31446261815324 J/(kelvin*mole)'
