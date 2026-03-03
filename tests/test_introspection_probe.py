import smonitor
from pyunitwizard.api import introspection


def test_is_quantity_emits_probe_miss_for_non_quantity_string():
    manager = smonitor.get_manager()
    manager.configure(level="DEBUG", event_buffer_size=200)
    start = len(manager.recent_events())

    assert introspection.is_quantity("not_a_quantity") is False
    recent = manager.recent_events()[start:]

    probe_events = [
        event
        for event in recent
        if event.get("code") == "PUW-DBG-PROBE-001"
        and event.get("source") == "pyunitwizard.debug.probe_miss"
    ]
    assert len(probe_events) >= 1
    assert any(
        event.get("extra", {}).get("caller") == "pyunitwizard.api.introspection.is_quantity"
        for event in probe_events
    )


def test_is_unit_emits_probe_miss_for_non_unit_string():
    manager = smonitor.get_manager()
    manager.configure(level="DEBUG", event_buffer_size=200)
    start = len(manager.recent_events())

    assert introspection.is_unit("not_a_unit") is False
    recent = manager.recent_events()[start:]

    probe_events = [
        event
        for event in recent
        if event.get("code") == "PUW-DBG-PROBE-001"
        and event.get("source") == "pyunitwizard.debug.probe_miss"
    ]
    assert len(probe_events) >= 1
    assert any(
        event.get("extra", {}).get("caller") == "pyunitwizard.api.introspection.is_unit"
        for event in probe_events
    )
