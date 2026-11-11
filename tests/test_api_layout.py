import importlib
import subprocess
import sys
import warnings

import pytest

import pyunitwizard as puw

API_SYMBOLS = [
    "are_close",
    "are_compatible",
    "are_equal",
    "change_value",
    "check",
    "compatibility",
    "context",
    "convert",
    "ensure_quantity",
    "get_dimensionality",
    "get_form",
    "get_standard_units",
    "get_unit",
    "get_value",
    "get_value_and_unit",
    "has_unit",
    "is_dimensionless",
    "is_quantity",
    "is_unit",
    "quantity",
    "similarity",
    "standardize",
    "to_string",
    "unit",
]


def test_main_reexports_api():
    api = importlib.import_module("pyunitwizard.api")
    main = importlib.import_module("pyunitwizard.main")

    for name in API_SYMBOLS:
        assert getattr(main, name) is getattr(api, name)


def test_package_reexports_api():
    api = importlib.import_module("pyunitwizard.api")

    for name in API_SYMBOLS:
        assert getattr(puw, name) is getattr(api, name)


def test_api_all_contains_only_real_public_attributes():
    api = importlib.import_module("pyunitwizard.api")

    missing = [name for name in api.__all__ if not hasattr(api, name)]

    assert missing == []


def test_main_deprecation_warning_emitted_once_for_attribute_access():
    sys.modules["pyunitwizard.main"] = puw._create_main_compat_module()
    main = importlib.import_module("pyunitwizard.main")

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        _ = main.convert
        _ = main.convert

    dep_warnings = [w for w in captured if issubclass(w.category, DeprecationWarning)]
    assert len(dep_warnings) == 1


def test_main_unknown_attribute_raises_attribute_error():
    main = importlib.import_module("pyunitwizard.main")

    try:
        _ = main.__definitely_unknown_attr__
    except AttributeError:
        pass
    else:
        raise AssertionError("Expected AttributeError for unknown pyunitwizard.main attribute")


@pytest.mark.parametrize("state", ["cold", "application_policy"])
def test_main_compatibility_module_exposes_its_creator_origin(state):
    code = """
import importlib
import importlib.util
import inspect
from pathlib import Path
import sys
import warnings

import pyunitwizard as puw

main = sys.modules['pyunitwizard.main']
assert not puw.configure.get_libraries_loaded()
if sys.argv[1] == 'application_policy':
    puw.configure.set_default_form('pint')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(['angstrom', 'fs'], provenance='application')
    assert puw.configure.has_active_policy()
before = puw.configure.report()
backend_modules = {name for name in sys.modules if name.startswith('pyunitwizard.forms.api_')}

with warnings.catch_warnings(record=True) as captured:
    warnings.simplefilter('always', DeprecationWarning)
    assert importlib.import_module('pyunitwizard.main') is main
    creator = Path(puw.__file__).resolve()
    assert Path(main.__file__).resolve() == creator
    assert Path(inspect.getsourcefile(main)).resolve() == creator
    assert '_create_main_compat_module' in inspect.getsource(main)
    spec = importlib.util.find_spec('pyunitwizard.main')
    assert spec is main.__spec__
    assert spec.name == 'pyunitwizard.main'
    assert Path(spec.origin).resolve() == creator
    assert main.__package__ == spec.parent == 'pyunitwizard'
    assert spec.has_location
    assert spec.loader is main.__loader__ is None

assert not captured, [str(item.message) for item in captured]
assert puw.configure.report() == before
assert {name for name in sys.modules if name.startswith('pyunitwizard.forms.api_')} == backend_modules
"""
    completed = subprocess.run(
        [sys.executable, "-c", code, state],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
