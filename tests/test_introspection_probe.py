import subprocess
import sys

import pytest
import smonitor

import pyunitwizard as puw
from pyunitwizard.api import introspection


@pytest.fixture
def debug_probe_manager():
    with puw.context(default_form="pint", default_parser="pint"):
        # Finish legacy first-use provider setup before selecting the test level.
        puw.unit("nm")
        manager = smonitor.get_manager()
        previous = manager.config
        manager.configure(level="DEBUG", event_buffer_size=200)
        try:
            yield manager
        finally:
            manager.configure(level=previous.level, event_buffer_size=previous.event_buffer_size)


def test_is_quantity_emits_probe_miss_for_non_quantity_string(debug_probe_manager):
    manager = debug_probe_manager
    start = len(manager.recent_events())

    assert introspection.is_quantity("not_a_quantity") is False
    recent = manager.recent_events()[start:]

    probe_events = [
        event
        for event in recent
        if event.get("code") == "PUW-DBG-PROBE-001" and event.get("source") == "pyunitwizard.debug.probe_miss"
    ]
    assert len(probe_events) >= 1
    assert any(
        event.get("extra", {}).get("caller") == "pyunitwizard.api.introspection.is_quantity" for event in probe_events
    )


def test_is_unit_emits_probe_miss_for_non_unit_string(debug_probe_manager):
    manager = debug_probe_manager
    start = len(manager.recent_events())

    assert introspection.is_unit("not_a_unit") is False
    recent = manager.recent_events()[start:]

    probe_events = [
        event
        for event in recent
        if event.get("code") == "PUW-DBG-PROBE-001" and event.get("source") == "pyunitwizard.debug.probe_miss"
    ]
    assert len(probe_events) >= 1
    assert any(
        event.get("extra", {}).get("caller") == "pyunitwizard.api.introspection.is_unit" for event in probe_events
    )


def test_filtered_probe_skips_payload_and_follows_live_debug_level():
    script = """
import pyunitwizard as puw
import smonitor

class Unrecognized:
    repr_calls = 0

    def __repr__(self):
        self.repr_calls += 1
        return 'ordinary metadata'

value = Unrecognized()
manager = smonitor.get_manager()
manager.configure(level='INFO', args_summary=False, handlers=[], event_buffer_size=50)
assert puw.is_quantity(value) is False
assert value.repr_calls == 0

manager.configure(level='DEBUG')
assert puw.is_quantity(value) is False
events = [e for e in manager.recent_events() if e.get('code') == 'PUW-DBG-PROBE-001']
assert len(events) == 1
assert events[0]['extra']['caller'] == 'pyunitwizard.api.introspection.is_quantity'
assert events[0]['extra']['value'] == 'ordinary metadata'
assert value.repr_calls == 1

manager.configure(level='WARNING')
assert puw.is_quantity(value) is False
assert value.repr_calls == 1
"""
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
