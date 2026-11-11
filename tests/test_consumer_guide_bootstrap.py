"""Exercise the canonical consumer example in independent interpreters."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

GUIDE = Path(__file__).resolve().parents[1] / "standards/PYUNITWIZARD_GUIDE.md"


@pytest.mark.parametrize("initial_state", ["cold", "pint_loaded", "application_policy"])
def test_consumer_guide_bootstrap_preserves_existing_registry_and_policy(initial_state, tmp_path):
    snippet = re.search(r"```python\n(# mylib/_pyunitwizard\.py\n.*?)\n```", GUIDE.read_text(), re.S)
    assert snippet is not None
    script = """
import sys
import warnings
from pathlib import Path

import platformdirs
import pyunitwizard as puw

# Isolate the automatic cache on every supported platform.
platformdirs.user_cache_path = lambda **kwargs: Path(sys.argv[3])

state = sys.argv[1]
registry = None
if state != 'cold':
    puw.configure.set_pint_registry_cache(False)
    registry = puw.quantity(2.0, 'nm', form='pint', parser='pint')._REGISTRY
if state == 'application_policy':
    puw.configure.set_default_form('pint')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(['angstrom', 'ps'], provenance='application')
else:
    assert not puw.configure.has_active_policy()

with warnings.catch_warnings():
    warnings.filterwarnings('error', message='The pint backend is already loaded', category=RuntimeWarning)
    exec(sys.argv[2], {})

expected = 'application' if state == 'application_policy' else 'mylib'
report = puw.configure.report()
assert report['provenance'] == expected, report
assert puw.get_value(puw.to_nanometers(puw.quantity(20, 'angstrom'))) == 2.0
if registry is None:
    assert puw.configure.get_pint_registry_cache() == ':auto:'
else:
    assert puw.quantity(2.0, 'nm')._REGISTRY is registry
    assert puw.configure.get_pint_registry_cache() is None
if state == 'application_policy':
    assert puw.get_standard_units(puw.quantity(2.0, 'nm')) == puw.unit('angstrom')
"""
    completed = subprocess.run(
        [sys.executable, "-c", script, initial_state, snippet.group(1), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
