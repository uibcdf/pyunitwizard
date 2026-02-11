from pyunitwizard.api import introspection


def test_is_quantity_emits_probe_miss_for_non_quantity_string(monkeypatch):
    calls = []

    def _fake_emit(value, caller):
        calls.append((value, caller))

    monkeypatch.setattr(introspection, "emit_probe_miss", _fake_emit)

    assert introspection.is_quantity("not_a_quantity") is False
    assert len(calls) == 1
    assert calls[0][1] == "pyunitwizard.api.introspection.is_quantity"


def test_is_unit_emits_probe_miss_for_non_unit_string(monkeypatch):
    calls = []

    def _fake_emit(value, caller):
        calls.append((value, caller))

    monkeypatch.setattr(introspection, "emit_probe_miss", _fake_emit)

    assert introspection.is_unit("not_a_unit") is False
    assert len(calls) == 1
    assert calls[0][1] == "pyunitwizard.api.introspection.is_unit"
