"""Real provider evidence for the bounded Pint/unyt dispatch pilot (#92)."""

import json
import subprocess
import sys

import numpy as np
import pytest

import pyunitwizard as puw


@pytest.fixture
def provider():
    ackredit = pytest.importorskip("ackredit")
    if not hasattr(ackredit, "capture"):
        pytest.skip("portable attribution requires the Ackredit development provider")
    with ackredit.session("pyunitwizard-pilot"), puw.attribution():
        yield ackredit


def _setup():
    pytest.importorskip("unyt")
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")


def test_loading_backends_earns_no_credit(provider):
    _setup()
    assert provider.get_used_items() == {}


def test_pint_software_without_unused_unyt_or_an_invented_article(provider):
    _setup()
    with provider.capture("pint") as run:
        q = puw.quantity([1.0, 2.0], "meter", form="pint")
        result = puw.convert(q, to_unit="centimeter")
    np.testing.assert_allclose(puw.get_value(result), [100.0, 200.0])
    data = run.attribution.to_dict()
    assert len(data["items"]) == 1
    assert data["items"][0]["type"] == "software"
    assert data["items"][0]["title"].startswith("Pint")
    assert {use["roles"][0] for use in data["uses"]} == {"executed_software"}


def test_reused_unyt_software_and_article_reach_each_result_and_workflow(provider):
    import unyt

    _setup()
    q = unyt.unyt_array([1.0, 2.0], "m")
    runs = []
    with provider.scope("application"):
        for name in ("first", "second"):
            with provider.capture(name, context={"producer": "pyunitwizard", "version": puw.__version__}) as run:
                result = puw.convert(q, to_unit=unyt.Unit("cm"), to_form="unyt")
            np.testing.assert_allclose(result.value, [100.0, 200.0])
            runs.append(run.attribution.to_dict())
    assert runs[0]["items"] == runs[1]["items"]
    assert len(runs[0]["items"]) == 2
    assert {item["type"] for item in runs[0]["items"]} == {"software", "article"}
    article = next(item for item in runs[0]["items"] if item["type"] == "article")
    assert article["doi"] == "10.21105/joss.00809"
    assert {use["context"]["version"] for use in runs[0]["uses"]} == {unyt.__version__}
    assert {use["context"]["software"] for use in runs[0]["uses"]} == {"unyt"}
    assert len(provider.get_attribution().to_dict()["items"]) == 2
    assert "pyunitwizard.forms.unyt.convert" in provider.current_session().usage_tree["application"]["children"]


def test_direct_translation_credits_both_executed_backends(provider):
    _setup()
    q = puw.quantity(2.0, "meter", form="pint")
    with provider.capture("translate") as run:
        result = puw.convert(q, to_form="unyt")
    assert float(result.value) == 2.0
    assert {use["context"]["software"] for use in run.attribution.to_dict()["uses"]} == {"pint", "unyt"}


def test_noop_and_failed_conversion_do_not_credit_a_completed_operation(provider):
    _setup()
    q = puw.quantity(2.0, "meter", form="pint")
    with provider.capture("noop") as run:
        assert puw.convert(q) is q
    assert run.attribution.to_dict()["items"] == []
    target = q._REGISTRY.second
    with provider.capture("failed") as failed:
        with pytest.raises(Exception):
            puw.convert(q, to_unit=target)
    assert failed.attribution.to_dict()["items"] == []


def test_empty_array_still_credits_completed_unit_conversion(provider):
    _setup()
    q = puw.quantity(np.array([]), "meter", form="pint")
    with provider.capture("empty") as run:
        result = puw.convert(q, to_unit="centimeter")
    assert puw.get_value(result).size == 0
    assert len(run.attribution.to_dict()["items"]) == 1


@pytest.mark.parametrize("failure", ["load", "register", "track"])
def test_provider_failure_has_catalog_diagnostic_and_preserves_science(monkeypatch, failure):
    from pyunitwizard import _ackredit
    from pyunitwizard._private.smonitor.warnings import AckreditTrackingWarning

    _setup()
    from contextlib import nullcontext

    class Broken:
        def scope(self, operation):
            return nullcontext()

        def register_item(self, **record):
            if failure == "register":
                raise RuntimeError("provider register failed")

        def track_item(self, *args, **kwargs):
            raise RuntimeError("provider track failed")

    def backend():
        if failure == "load":
            raise RuntimeError("provider load failed")
        return Broken()

    monkeypatch.setattr(_ackredit, "backend", backend)
    with puw.attribution(), pytest.warns(AckreditTrackingWarning) as diagnostics:
        q = puw.quantity(2.0, "meter", form="pint")
        result = puw.convert(q, to_unit="centimeter")
    assert diagnostics[0].message.code == "PUW-WARN-ACK-001"
    assert f"provider {failure} failed" in str(diagnostics[0].message)
    assert puw.get_value(result) == 200.0


def test_provider_absence_preserves_value_and_offline_reference_metadata(monkeypatch):
    from pyunitwizard import _ackredit
    from pyunitwizard._private.backend_references import records

    _setup()
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    q = puw.quantity(2.0, "meter", form="pint")
    assert puw.get_value(puw.convert(q, to_unit="centimeter")) == 200.0
    assert len(records("unyt")) == 2


def test_fresh_import_and_true_provider_absence():
    script = """
import importlib.abc, sys
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "ackredit" or fullname.startswith("ackredit."):
            raise ModuleNotFoundError("ackredit unavailable", name=fullname)
sys.meta_path.insert(0, NoAckredit())
import pyunitwizard as puw
assert "ackredit" not in sys.modules
assert "pint" not in sys.modules
with puw.attribution():
    assert "ackredit" not in sys.modules and "pint" not in sys.modules
    q = puw.quantity(2., "meter", form="pint")
    assert puw.get_value(puw.convert(q, to_unit="centimeter")) == 200.
assert "ackredit" not in sys.modules
"""
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr


def test_saved_record_and_bibliography_read_without_credit_or_backend_import(provider, tmp_path):
    _setup()
    q = puw.quantity([1.0, 2.0], "meter", form="pint")
    with provider.capture("saved") as run:
        result = puw.convert(q, to_form="unyt")
    data = {
        "quantity": puw.QuantityRecord.from_quantity(result, field="distance").to_dict(),
        "attribution": run.attribution.to_dict(),
    }
    path = tmp_path / "result.json"
    path.write_text(json.dumps(data))
    script = """
import json, pathlib, sys
import ackredit
from pyunitwizard.record import QuantityRecord
payload = json.loads(pathlib.Path(sys.argv[1]).read_text())
saved = ackredit.Attribution.from_dict(payload["attribution"])
assert saved.to_dict() == payload["attribution"]
assert "10.21105/joss.00809" in saved.report(format="bibtex")
assert ackredit.get_used_items() == {}
assert "pint" not in sys.modules and "unyt" not in sys.modules
record = QuantityRecord.from_dict(payload["quantity"])
assert record.values.tolist() == [1., 2.]
assert "unyt" not in sys.modules
assert ackredit.get_used_items() == {}
"""
    completed = subprocess.run([sys.executable, "-c", script, str(path)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr


def test_article_only_declaration_retains_relationship_to_executed_software(provider, monkeypatch):
    import unyt

    from pyunitwizard._private import backend_references

    _setup()
    monkeypatch.setitem(backend_references._SOFTWARE, "unyt", None)
    with provider.capture("article-only") as run:
        result = puw.convert(unyt.unyt_array([2.0], "m"), to_unit=unyt.Unit("cm"), to_form="unyt")
    assert result.value.tolist() == [200.0]
    data = run.attribution.to_dict()
    assert len(data["items"]) == 1 and data["items"][0]["type"] == "article"
    assert data["uses"][0]["context"] == {"software": "unyt", "version": unyt.__version__}


def test_normal_operations_do_not_load_provider_or_credit(monkeypatch):
    from pyunitwizard import _ackredit

    _setup()
    calls = []
    monkeypatch.setattr(_ackredit, "backend", lambda: calls.append(True))
    q = puw.quantity(2.0, "meter", form="pint")
    assert puw.get_value(puw.convert(q, to_unit="centimeter")) == 200.0
    assert calls == []


def test_nested_optin_restores_parent_and_then_normal_operation(provider):
    _setup()
    with puw.attribution():
        with puw.attribution():
            q = puw.quantity(2.0, "meter", form="pint")
        with provider.capture("still-active") as run:
            puw.convert(q, to_unit=q._REGISTRY.centimeter)
    assert len(run.attribution.to_dict()["items"]) == 1


def test_optin_is_isolated_between_async_tasks():
    import asyncio

    ackredit = pytest.importorskip("ackredit")
    if not hasattr(ackredit, "capture"):
        pytest.skip("requires the development provider")
    _setup()

    async def observed():
        with ackredit.capture("observed") as run, puw.attribution():
            await asyncio.sleep(0)
            puw.quantity(2.0, "meter", form="pint")
        return run.attribution.to_dict()

    async def ordinary():
        with ackredit.capture("ordinary") as run:
            await asyncio.sleep(0)
            puw.quantity(2.0, "meter", form="pint")
        return run.attribution.to_dict()

    async def together():
        return await asyncio.gather(observed(), ordinary())

    with ackredit.session():
        results = asyncio.run(together())
    assert len(results[0]["items"]) == 1
    assert results[1]["items"] == []


def test_scientific_exception_restores_ordinary_operation(monkeypatch):
    from pyunitwizard import _ackredit

    _setup()
    with pytest.raises(RuntimeError, match="scientific failure"):
        with puw.attribution():
            raise RuntimeError("scientific failure")
    calls = []
    monkeypatch.setattr(_ackredit, "backend", lambda: calls.append(True))
    puw.quantity(2.0, "meter", form="pint")
    assert calls == []
