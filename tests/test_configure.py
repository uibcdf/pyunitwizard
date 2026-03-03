import pyunitwizard as puw
from pyunitwizard.configure import configure as configure_module

def test_libraries_supported():
    assert puw.configure.get_libraries_supported()==['pint', 'openmm.unit', 'unyt', 'astropy.units']

def test_parsers_supported():
    assert puw.configure.get_parsers_supported() == ['pint', 'openmm.unit', 'unyt', 'astropy.units']

def test_load_library():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])
    assert puw.configure.get_libraries_loaded()==['pint', 'openmm.unit']

def test_load_library_rejects_non_string_or_sequence():
    puw.configure.reset()
    try:
        puw.configure.load_library(3.14)
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError when loading a non-string scalar")

def test_default_form():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])
    assert puw.configure.get_default_form()=='pint'

def test_default_parser():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])
    assert puw.configure.get_default_parser()=='pint'

def test_set_default_parser_normalizes_input_form():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    puw.configure.set_default_parser('PINT')
    assert puw.configure.get_default_parser() == 'pint'

def test_set_standard_units_accepts_single_string():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units('nm')
    assert 'nm' in puw.configure.get_standard_units()

def test_set_standard_units_rejects_non_list_tuple_or_string():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    try:
        puw.configure.set_standard_units(10)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid standard_units type")

def test_set_standard_units_tie_candidate_path_with_combination_units():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm*ps', 'm*s'])
    # Ensure combination standards are still registered and no crash on tie path.
    standards = puw.configure.get_standard_units()
    assert 'nm*ps' in standards
    assert 'm*s' in standards

def test_add_constant_registers_new_constant():
    from pyunitwizard.configure import configure as configure_module
    from pyunitwizard.constants import _constants

    constant_name = 'TestConstantConfigure'
    if constant_name in _constants:
        del _constants[constant_name]

    configure_module.add_constant(constant_name, 42.0, 'meter')
    assert _constants[constant_name] == [42.0, 'meter']
    del _constants[constant_name]

def test_get_parsers_loaded_only_reports_backends_with_parser_support():
    puw.configure.reset()
    puw.configure.load_library(['openmm.unit', 'unyt'])
    assert puw.configure.get_parsers_loaded() == []

def test_init_openmolecularsystems():
    puw.configure.load_library(['pint','openmm.unit'])
    puw.configure.set_default_form('openmm.unit')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'amu', 'e',
                                 'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees'])

    assert True

def test_all():
    puw.configure.reset()
    libraries = ['pint', 'openmm.unit', 'unyt']
    try:
        import astropy.units  # noqa: F401
    except Exception:
        puw.configure.load_library(libraries)
    else:
        puw.configure.load_library(libraries + ['astropy.units'])

    assert True


def test_resolve_config_module_runtime_over_env_and_file(monkeypatch):
    monkeypatch.setenv("PYUNITWIZARD_CONFIG", "env.config")
    monkeypatch.setattr(configure_module, "find_spec", lambda _: object())

    output = puw.configure.resolve_config_module(
        config="runtime.config",
        root_package="mylib",
    )

    assert output == "runtime.config"


def test_resolve_config_module_env_over_file(monkeypatch):
    monkeypatch.setenv("PYUNITWIZARD_CONFIG", "env.config")
    monkeypatch.setattr(configure_module, "find_spec", lambda _: object())

    output = puw.configure.resolve_config_module(root_package="mylib")

    assert output == "env.config"


def test_resolve_config_module_file_fallback(monkeypatch):
    monkeypatch.delenv("PYUNITWIZARD_CONFIG", raising=False)
    monkeypatch.setattr(
        configure_module,
        "find_spec",
        lambda module_path: object() if module_path == "mylib._pyunitwizard" else None,
    )

    output = puw.configure.resolve_config_module(root_package="mylib")

    assert output == "mylib._pyunitwizard"


def test_resolve_config_module_none_when_no_candidate(monkeypatch):
    monkeypatch.delenv("PYUNITWIZARD_CONFIG", raising=False)
    monkeypatch.setattr(configure_module, "find_spec", lambda _: None)

    output = puw.configure.resolve_config_module(root_package="mylib")

    assert output is None
