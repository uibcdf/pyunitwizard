"""Concurrent readers must wait for cold backend and parser admission (#151)."""

import os
import subprocess
import sys
import textwrap

import pytest

SCENARIOS = ["factory", "explicit_pint", "configured_pint", "context_pint", "openmm.unit", "unyt", "astropy.units"]

PROGRAM = textwrap.dedent(
    """
    import json
    import sys
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from contextvars import copy_context
    from contextlib import ExitStack

    import pyunitwizard as puw
    import pyunitwizard.forms as forms

    scenario, stage = sys.argv[1:]
    form = scenario if scenario in ('openmm.unit', 'unyt', 'astropy.units') else 'pint'
    scope = ExitStack()
    original_policy = puw.configure.report()
    if scenario == 'context_pint':
        scope.enter_context(puw.context(default_form='pint', default_parser='pint'))
    elif scenario not in ('factory', 'explicit_pint'):
        puw.configure.set_default_form(form)
        puw.configure.set_default_parser('pint')
    # Resolve orchestration imports without loading a numerical backend.
    quantity, get_value = puw.quantity, puw.get_value
    assert puw.configure.get_libraries_loaded() == []
    before = puw.configure.report()
    arguments = {'form': 'pint', 'parser': 'pint'} if scenario == 'explicit_pint' else {}

    def operation():
        result = quantity(1.0, 'angstrom', **arguments)
        assert puw.get_form(result) == form
        assert get_value(result, to_unit='angstrom', parser='pint') == 1.0
        return 1.0

    if stage == 'natural':
        barrier = threading.Barrier(2)
        def start():
            barrier.wait(timeout=15)
            return operation()
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(copy_context().run, start) for _ in range(2)]
            assert [f.result(timeout=30) for f in futures] == [1.0, 1.0]
    else:
        entered, release, attempted = (threading.Event() for _ in range(3))
        original = forms.load_library
        def paused(library):
            if library != form:
                return original(library)
            if stage == 'registered':
                original(library)
            entered.set()
            assert release.wait(timeout=15), 'parent did not release initialization'
            if stage == 'unregistered':
                original(library)
        forms.load_library = paused
        def second():
            attempted.set()
            return operation()
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(copy_context().run, operation)
            try:
                assert entered.wait(timeout=15), 'first reader did not enter initialization'
                following = pool.submit(copy_context().run, second)
                assert attempted.wait(timeout=15)
                try:
                    following.result(timeout=0.3)
                except TimeoutError:
                    pass
                else:
                    raise AssertionError('reader returned before initialization completed')
            finally:
                release.set()
            assert first.result(timeout=30) == following.result(timeout=30) == 1.0

    libraries = puw.configure.get_libraries_loaded()
    parsers = puw.configure.get_parsers_loaded()
    assert libraries.count(form) == 1 and parsers.count('pint') == 1
    after = puw.configure.report()
    for field in ('standard_units', 'provenance', 'fast_tracks'):
        assert after[field] == before[field]
    if scenario not in ('factory', 'explicit_pint'):
        assert after['default_form'] == before['default_form']
        assert after['default_parser'] == before['default_parser']
    assert set(libraries) <= {form, 'pint'}
    scope.close()
    if scenario == 'context_pint':
        restored = puw.configure.report()
        for field in ('default_form', 'default_parser', 'standard_units', 'provenance', 'fast_tracks'):
            assert restored[field] == original_policy[field]
    print(json.dumps({'scenario': scenario, 'stage': stage, 'values': [1.0, 1.0]}))
    """
)


def _run(program, *arguments):
    environment = os.environ.copy()
    environment["OPENBLAS_NUM_THREADS"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", program, *arguments],
        capture_output=True,
        text=True,
        timeout=90,
        env=environment,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_concurrent_public_first_use_in_fresh_process(scenario):
    _run(PROGRAM, scenario, "natural")


@pytest.mark.parametrize("scenario", ["factory", "configured_pint", "openmm.unit"])
@pytest.mark.parametrize("stage", ["unregistered", "registered"])
def test_concurrent_reader_waits_until_backend_and_parser_ready(scenario, stage):
    _run(PROGRAM, scenario, stage)


def test_recursive_configuration_and_initialization_failure_remain_usable():
    _run(
        textwrap.dedent(
            """
            import pyunitwizard as puw
            import pyunitwizard.forms as forms

            original = forms.load_library
            class ExpectedFailure(RuntimeError):
                pass
            def fail(library):
                raise ExpectedFailure('backend initialization failed')
            forms.load_library = fail
            try:
                puw.quantity(1.0, 'angstrom', form='pint')
            except ExpectedFailure as error:
                assert str(error) == 'backend initialization failed'
            else:
                raise AssertionError('backend failure was swallowed')
            assert puw.configure.get_libraries_loaded() == []
            forms.load_library = original
            puw.configure.load_library(['openmm.unit', 'pint'])
            assert set(puw.configure.get_libraries_loaded()) == {'openmm.unit', 'pint'}
            assert puw.configure.get_libraries_loaded().count('pint') == 1
            assert puw.configure.get_default_form() == 'openmm.unit'
            assert puw.configure.get_default_parser() == 'pint'
            assert puw.get_value(puw.quantity(1.0, 'angstrom'), to_unit='angstrom') == 1.0
            """
        )
    )


def test_waiting_reader_can_initialize_after_native_failure():
    _run(
        textwrap.dedent(
            """
            import threading
            from concurrent.futures import ThreadPoolExecutor
            import pyunitwizard as puw
            import pyunitwizard.forms as forms

            quantity, get_value = puw.quantity, puw.get_value
            entered, release, attempted = (threading.Event() for _ in range(3))
            original = forms.load_library
            calls = []
            class ExpectedFailure(RuntimeError):
                pass
            def fail_once(library):
                calls.append(library)
                if len(calls) == 1:
                    entered.set()
                    assert release.wait(timeout=15)
                    raise ExpectedFailure('native initialization failure')
                return original(library)
            forms.load_library = fail_once
            def operation():
                return get_value(quantity(1.0, 'angstrom'), to_unit='angstrom')
            def second():
                attempted.set()
                return operation()
            with ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(operation)
                try:
                    assert entered.wait(timeout=15)
                    following = pool.submit(second)
                    assert attempted.wait(timeout=15)
                    try:
                        following.result(timeout=0.3)
                    except TimeoutError:
                        pass
                    else:
                        raise AssertionError('waiting reader bypassed initialization')
                finally:
                    release.set()
                try:
                    first.result(timeout=30)
                except ExpectedFailure as error:
                    assert str(error) == 'native initialization failure'
                else:
                    raise AssertionError('native failure was swallowed')
                assert following.result(timeout=30) == 1.0
            assert calls == ['pint', 'pint']
            assert puw.configure.get_libraries_loaded() == ['pint']
            assert puw.configure.get_parsers_loaded() == ['pint']
            """
        )
    )
