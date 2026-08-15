import pytest

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

def test_add_standard_units_adds_new_dimensionality():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])
    puw.configure.add_standard_units(['K'])
    standards = puw.configure.get_standard_units()
    assert 'nm' in standards
    assert 'ps' in standards
    assert 'K' in standards


def test_add_standard_units_replaces_same_dimensionality():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])
    puw.configure.add_standard_units(['angstrom'])
    standards = puw.configure.get_standard_units()
    # angstrom replaces nm (both are length); ps must survive
    assert 'angstrom' in standards
    assert 'nm' not in standards
    assert 'ps' in standards


def test_add_standard_units_accepts_single_string():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm'])
    puw.configure.add_standard_units('ps')
    standards = puw.configure.get_standard_units()
    assert 'nm' in standards
    assert 'ps' in standards


def test_add_standard_units_rejects_invalid_type():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    try:
        puw.configure.add_standard_units(42)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid type")


def test_add_standard_units_rebuilds_matrices():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])
    puw.configure.add_standard_units(['K'])
    assert puw.kernel.dimensional_fundamental_standards_matrix is not None
    assert puw.kernel.dimensional_fundamental_standards_units is not None


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


def test_has_active_policy_reports_whether_units_are_configured():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    assert puw.configure.has_active_policy() is False

    puw.configure.set_standard_units(["nm", "ps"])

    assert puw.configure.has_active_policy() is True


def test_report_states_the_active_policy_and_its_provenance():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm", "ps"], provenance="mylib")
    puw.register_fast_track("nanometers_for_report_test", puw.unit("nm"))

    report = puw.configure.report()

    assert report["default_form"] == "pint"
    assert report["default_parser"] == "pint"
    assert report["standard_units"] == ["nm", "ps"]
    assert report["provenance"] == "mylib"
    assert "pint" in report["loaded_libraries"]
    assert "nanometers_for_report_test" in report["fast_tracks"]


def test_provenance_is_cleared_by_reset_and_replaced_by_a_new_policy():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm"], provenance="first")

    assert puw.configure.report()["provenance"] == "first"

    puw.configure.set_standard_units(["angstrom"], provenance="second")
    assert puw.configure.report()["provenance"] == "second"

    # A caller that does not identify itself leaves no stale attribution.
    puw.configure.set_standard_units(["nm"])
    assert puw.configure.report()["provenance"] is None

    puw.configure.reset()
    assert puw.configure.report()["provenance"] is None


def test_context_restores_the_policy_provenance():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm", "ps"], provenance="outer")

    with puw.context(standard_units=["angstrom", "fs"]):
        assert puw.configure.report()["provenance"] is None

    assert puw.configure.report()["provenance"] == "outer"


def test_setting_a_default_form_does_not_import_the_backend():
    """Naming a form is not using it.

    Importing a backend is expensive -- `pint` costs about 480 ms between its
    own import and building a registry -- and a library that records a
    preference at import time should not pay it. The first operation that
    actually needs the backend loads it through `digest_form()`.
    """
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, warnings; warnings.filterwarnings('ignore')\n"
            "import pyunitwizard as puw\n"
            "puw.configure.set_default_form('pint')\n"
            "puw.configure.set_default_parser('pint')\n"
            "print('pint' in sys.modules)\n"
            "puw.quantity(1.0, 'nm')\n"
            "print('pint' in sys.modules)\n",
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )

    assert result.returncode == 0, result.stderr[-2000:]
    loaded_after_configuring, loaded_after_use = result.stdout.split()

    assert loaded_after_configuring == "False"
    assert loaded_after_use == "True"


def test_declaring_a_policy_does_not_import_numpy_or_the_api_package():
    """`puw.configure` must stay cheap to reach.

    Configuring is often the first thing a consumer does. Importing the module
    used to drag in the whole `pyunitwizard.api` package and numpy -- about
    63 ms -- before any unit work had been requested. Both are now imported by
    the functions that need them.
    """
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, warnings; warnings.filterwarnings('ignore')\n"
            "import pyunitwizard as puw\n"
            "puw.configure.set_default_form('pint')\n"
            "puw.configure.set_default_parser('pint')\n"
            "print('numpy' in sys.modules, 'pyunitwizard.api' in sys.modules)\n"
            "puw.configure.set_standard_units(['nm'])\n"
            "print('numpy' in sys.modules, 'pyunitwizard.api' in sys.modules)\n",
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )

    assert result.returncode == 0, result.stderr[-2000:]
    declaring, after_standard_units = result.stdout.strip().splitlines()

    assert declaring == "False False"
    assert after_standard_units == "True True"


def test_default_form_is_still_validated_without_loading():
    puw.configure.reset()

    with pytest.raises(ValueError):
        puw.configure.set_default_form("not_a_form")

    puw.configure.set_default_form("pint")
    assert puw.configure.get_default_form() == "pint"
