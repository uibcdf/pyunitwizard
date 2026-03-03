import pyunitwizard as puw
import smonitor
from pyunitwizard.api import conversion
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


def test_get_dimensionality_string_uses_unit_branch_when_quantity_probe_fails(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    called_to_type = []

    monkeypatch.setattr(introspection, "is_quantity", lambda _: False)
    monkeypatch.setattr(introspection, "is_unit", lambda _: True)

    def _fake_convert(quantity_or_unit, to_type=None, **kwargs):
        called_to_type.append(to_type)
        return puw.forms.api_pint.ureg.meter

    monkeypatch.setattr(conversion, "convert", _fake_convert)

    dim = introspection.get_dimensionality("meter")
    assert called_to_type == ["unit"]
    assert dim["[L]"] == 1
