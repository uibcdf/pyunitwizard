import pyunitwizard as puw
from pyunitwizard.api import conversion
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
