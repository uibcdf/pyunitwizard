import pyunitwizard as puw
from pathlib import Path
import os
import sys
import importlib

def test_libraries_supported():
    assert puw.configure.get_libraries_supported()==['pint', 'openmm.unit', 'unyt', 'astropy.units', 'physipy', 'quantities']

def test_parsers_supported():
    assert puw.configure.get_parsers_supported() == ['pint', 'openmm.unit', 'unyt', 'astropy.units', 'physipy', 'quantities']

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

def test_set_standard_units_builds_cached_matrices_once_state_is_ready():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    puw.configure.set_standard_units(["nm", "ps", "nm*ps"])

    assert puw.kernel.dimensional_fundamental_standards_matrix is not None
    assert puw.kernel.dimensional_fundamental_standards_units is not None
    assert puw.kernel.tentative_base_standards_matrix is not None
    assert puw.kernel.tentative_base_standards_units is not None

def test_reset_clears_standardization_caches():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm", "ps", "nm*ps"])

    puw.configure.reset()

    assert puw.kernel.dimensional_fundamental_standards_matrix is None
    assert puw.kernel.dimensional_fundamental_standards_units is None
    assert puw.kernel.tentative_base_standards_matrix is None
    assert puw.kernel.tentative_base_standards_units is None

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


def _create_pkg_with_pyw_config(tmp_path: Path, package_name: str) -> None:
    pkg_dir = tmp_path / package_name
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "_pyunitwizard.py").write_text("FLAG = True\n", encoding="utf-8")


def test_resolve_config_module_runtime_over_env_and_file(tmp_path):
    _create_pkg_with_pyw_config(tmp_path, "mylib")

    previous = os.environ.get("PYUNITWIZARD_CONFIG")
    os.environ["PYUNITWIZARD_CONFIG"] = "env.config"
    sys.path.insert(0, str(tmp_path))
    importlib.invalidate_caches()

    try:
        output = puw.configure.resolve_config_module(
            config="runtime.config",
            root_package="mylib",
        )
    finally:
        sys.path.remove(str(tmp_path))
        importlib.invalidate_caches()
        if previous is None:
            os.environ.pop("PYUNITWIZARD_CONFIG", None)
        else:
            os.environ["PYUNITWIZARD_CONFIG"] = previous

    assert output == "runtime.config"


def test_resolve_config_module_env_over_file(tmp_path):
    _create_pkg_with_pyw_config(tmp_path, "mylib")
    previous = os.environ.get("PYUNITWIZARD_CONFIG")
    os.environ["PYUNITWIZARD_CONFIG"] = "env.config"
    sys.path.insert(0, str(tmp_path))
    importlib.invalidate_caches()

    try:
        output = puw.configure.resolve_config_module(root_package="mylib")
    finally:
        sys.path.remove(str(tmp_path))
        importlib.invalidate_caches()
        if previous is None:
            os.environ.pop("PYUNITWIZARD_CONFIG", None)
        else:
            os.environ["PYUNITWIZARD_CONFIG"] = previous

    assert output == "env.config"


def test_resolve_config_module_file_fallback(tmp_path):
    _create_pkg_with_pyw_config(tmp_path, "mylib")
    previous = os.environ.get("PYUNITWIZARD_CONFIG")
    os.environ.pop("PYUNITWIZARD_CONFIG", None)
    sys.path.insert(0, str(tmp_path))
    importlib.invalidate_caches()

    try:
        output = puw.configure.resolve_config_module(root_package="mylib")
    finally:
        sys.path.remove(str(tmp_path))
        importlib.invalidate_caches()
        if previous is not None:
            os.environ["PYUNITWIZARD_CONFIG"] = previous

    assert output == "mylib._pyunitwizard"


def test_resolve_config_module_none_when_no_candidate():
    previous = os.environ.get("PYUNITWIZARD_CONFIG")
    os.environ.pop("PYUNITWIZARD_CONFIG", None)

    try:
        output = puw.configure.resolve_config_module(root_package="mylib_that_does_not_exist")
    finally:
        if previous is not None:
            os.environ["PYUNITWIZARD_CONFIG"] = previous

    assert output is None
