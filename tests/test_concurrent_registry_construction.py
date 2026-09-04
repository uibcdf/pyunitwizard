"""The forms registry must survive being built from two threads at once.

uibcdf/PyUnitWizard#70. Two top-level packages that both configure PyUnitWizard have two
different import locks, so nothing serializes them. The loser finds `pyunitwizard` already
in `sys.modules` -- put there by the winner -- and proceeds as though the package were
configured, reading `dict_translate_quantity['string']` before `'pint'` is in it.

The reproduction runs in a subprocess because it needs a cold interpreter: once this
process has imported and configured PyUnitWizard there is no half-built state left to race
against. Two synthetic packages stand in for the real clients, so the test depends on
nothing outside this repository.
"""

import subprocess
import sys
import textwrap

import pytest


RACE = textwrap.dedent(
    """
    import sys, threading, pathlib, tempfile

    root = pathlib.Path(tempfile.mkdtemp())
    for name in ("client_one", "client_two"):
        pkg = root / name
        pkg.mkdir()
        (pkg / "__init__.py").write_text(
            # The shape the MolSysSuite libraries actually use: each declares the same
            # policy and applies it only when none is active yet. That guard is a
            # check-then-act, so under two threads both clients enter it, and one reaches
            # `set_standard_units` while the other is still inside `load_library`.
            "import pyunitwizard as puw\\n"
            "if not puw.configure.has_active_policy():\\n"
            "    puw.configure.set_default_form('pint')\\n"
            "    puw.configure.set_default_parser('pint')\\n"
            "    puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'dalton'])\\n"
        )
    sys.path.insert(0, str(root))

    barrier = threading.Barrier(2)
    errors = []

    def imp(name):
        def run():
            barrier.wait()
            try:
                __import__(name)
            except BaseException as exc:
                errors.append(f"{type(exc).__name__}: {exc}")
        return run

    threads = [threading.Thread(target=imp("client_one")),
               threading.Thread(target=imp("client_two"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if errors:
        print(errors[0])
        sys.exit(1)
    """
)


@pytest.mark.parametrize("attempt", range(8))
def test_two_threads_may_configure_at_once(attempt):
    """Repeated because it is a race: one clean pass proves nothing on its own."""
    done = subprocess.run(
        [sys.executable, "-c", RACE], capture_output=True, text=True, timeout=300
    )
    assert done.returncode == 0, (
        f"concurrent configuration raised: {done.stdout.strip() or done.stderr.strip()}"
    )
