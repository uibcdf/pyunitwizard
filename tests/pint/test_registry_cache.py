"""The opt-in on-disk cache for pint's parsed definitions.

Parsing pint's definitions costs about 180 ms in every process that uses units.
Pint can cache the parsed result on disk, which brings that down to about 17 ms,
but it raises rather than degrading when the folder cannot be used -- and a
units library has no business writing to a user's filesystem uninvited.
"""

import subprocess
import sys


PROBE = """
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw
puw.configure.load_library(['pint'])
from pyunitwizard.forms.api_pint import ureg
print(ureg.cache_folder)
print(puw.get_value(puw.quantity(2.0, 'nanometer', form='pint')))
"""


def _run(env_value, tmp_path=None):
    import os

    env = dict(os.environ)
    env.pop("PYUNITWIZARD_PINT_CACHE", None)
    if env_value is not None:
        env["PYUNITWIZARD_PINT_CACHE"] = env_value

    result = subprocess.run(
        [sys.executable, "-c", PROBE],
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr[-2000:]
    cache_folder, value = result.stdout.strip().splitlines()
    return cache_folder, value


def test_no_cache_folder_is_used_unless_asked():
    """Writing to disk is a side effect nobody requested by importing us."""
    cache_folder, value = _run(None)

    assert cache_folder == "None"
    assert value == "2.0"


def test_opting_in_with_a_path_populates_that_folder(tmp_path):
    cache = tmp_path / "pint-cache"
    cache.mkdir()

    cache_folder, value = _run(str(cache))

    assert cache_folder == str(cache)
    assert value == "2.0"
    assert list(cache.glob("*.pickle")), "expected pint to have written its cache"


def test_an_unusable_cache_folder_falls_back_instead_of_failing():
    """Read-only containers and shared HPC homes must not break imports.

    pint raises PermissionError or FileNotFoundError here rather than
    degrading, so the fallback is ours to provide.
    """
    cache_folder, value = _run("/proc/this-path-cannot-exist/cache")

    assert cache_folder == "None"
    assert value == "2.0"


def test_explicit_off_is_honoured():
    for value in ("0", "false", "off", "no"):
        cache_folder, _ = _run(value)
        assert cache_folder == "None", f"{value!r} should disable the cache"


def test_the_cache_can_be_enabled_programmatically(tmp_path):
    """A library should not have to write to os.environ to opt in.

    This works because naming a form no longer loads the backend, so there is
    a window between configuring and the registry being built.
    """
    cache = tmp_path / "programmatic"
    cache.mkdir()

    probe = f"""
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw
puw.configure.set_pint_registry_cache({str(cache)!r})
puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm'])
from pyunitwizard.forms.api_pint import ureg
print(ureg.cache_folder)
"""
    import os

    env = dict(os.environ)
    env.pop("PYUNITWIZARD_PINT_CACHE", None)
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, env=env, timeout=300
    )

    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == str(cache)
    assert list(cache.glob("*.pickle"))


def test_setting_the_cache_after_the_backend_loaded_warns():
    """Silently doing nothing would be worse than saying so."""
    probe = """
import warnings
import pyunitwizard as puw
puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm'])
with warnings.catch_warnings(record=True) as captured:
    warnings.simplefilter('always')
    puw.configure.set_pint_registry_cache(True)
print(captured[0].category.__name__ if captured else 'NONE')
"""
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, timeout=300
    )

    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "RuntimeWarning"
