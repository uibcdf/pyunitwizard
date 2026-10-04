import json
import subprocess
import sys

import pytest


def test_public_imports_do_not_attempt_optional_backend_imports():
    code = """
import importlib.abc
import sys

optional = {'ackredit', 'unyt', 'openmm', 'astropy', 'physipy', 'quantities'}
attempts = []

class BlockOptionalImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in optional:
            attempts.append(fullname)
            raise ModuleNotFoundError(fullname)

sys.meta_path.insert(0, BlockOptionalImports())
import pyunitwizard as puw
for name in puw.__all__:
    getattr(puw, name)
assert not attempts, attempts
assert not optional.intersection(name.split('.')[0] for name in sys.modules)
assert puw.configure.get_libraries_loaded() == []
"""
    subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)


@pytest.mark.parametrize("backend", ["openmm.unit", "unyt", "astropy.units", "physipy", "quantities"])
def test_explicit_loading_imports_only_the_requested_optional_backend(backend):
    code = """
import sys
import pyunitwizard as puw

backend = sys.argv[1]
optional = {'ackredit', 'unyt', 'openmm', 'astropy', 'physipy', 'quantities'}
puw.configure.load_library(backend)
imported = optional.intersection(name.split('.')[0] for name in sys.modules)
assert imported == {backend.split('.')[0]}, imported
assert puw.configure.get_libraries_loaded() == [backend]
assert 'pyunitwizard.forms.template_api_form' not in sys.modules
"""
    subprocess.run([sys.executable, "-c", code, backend], check=True, capture_output=True, text=True)


def test_external_quantity_loads_only_its_backend_adapter():
    code = """
import json
import pint
import pyunitwizard as puw

quantity = pint.UnitRegistry().Quantity(2.5, 'nanometer')
value = puw.get_value(quantity)
print(json.dumps({'value': value, 'loaded': puw.configure.get_libraries_loaded()}))
"""

    completed = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout.strip())

    assert result == {"value": 2.5, "loaded": ["pint"]}
