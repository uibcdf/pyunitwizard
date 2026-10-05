"""Real producer evidence for provisional Ackredit declarations (#94)."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import pyunitwizard as puw


@pytest.fixture
def observer():
    ackredit = pytest.importorskip("ackredit")
    if not hasattr(ackredit, "observe_calls"):
        pytest.skip("requires the provisional Ackredit function observer")
    return ackredit


@pytest.fixture
def provider(observer):
    puw.configure.reset()
    puw.configure.load_library("pint")
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    with observer.session("real-function-provider"):
        yield observer


def test_puw_calls_and_actual_backends_have_separate_reference_roles(provider):
    with provider.observe_calls(puw), puw.attribution():
        with provider.capture("construct") as first:
            q = puw.quantity(2.0, "meter", form="pint")
        with provider.capture("convert") as second:
            result = puw.convert(q, to_unit=q._REGISTRY.centimeter)
    assert puw.get_value(result) == 200.0
    for capture in (first, second):
        data = capture.attribution.to_dict()
        assert {use["context"]["software"] for use in data["uses"]} == {"pyunitwizard", "pint"}
        own = [item for item in data["items"] if item.get("doi") == "10.5281/zenodo.8092688"]
        assert len(own) == 1 and own[0]["version"] == puw.__version__
        assert all(item["type"] == "software" for item in data["items"])
        assert {role for use in data["uses"] for role in use["roles"]} == {"executed_software"}
    used = {use["used_by"] for use in second.attribution.to_dict()["uses"]}
    assert "pyunitwizard.convert" in used
    assert all("unyt" not in target for target in used)
    assert "10.5281/zenodo.8092688" in second.attribution.report(format="bibtex")


@pytest.mark.parametrize("operation", ["conversion_factor", "standardize"])
def test_factor_and_standardization_capture_the_declared_function(provider, operation):
    puw.configure.set_standard_units(["centimeter"])
    q = puw.quantity(2.0, "meter", form="pint")
    with provider.observe_calls(puw), provider.capture(operation) as run:
        if operation == "conversion_factor":
            result = puw.conversion_factor("meter", "centimeter")
        else:
            result = puw.standardize(q)

    if operation == "conversion_factor":
        assert result == 100.0
    else:
        assert puw.get_value(result) == 200.0
        assert result.units == q._REGISTRY.centimeter
    data = run.attribution.to_dict()
    assert len(data["items"]) == len(data["uses"]) == 1
    assert data["items"][0]["doi"] == "10.5281/zenodo.8092688"
    assert data["items"][0]["version"] == puw.__version__
    assert data["uses"][0]["used_by"] == f"pyunitwizard.{operation}"
    assert data["uses"][0]["roles"] == ["executed_software"]
    assert data["uses"][0]["context"] == {"software": "pyunitwizard", "version": puw.__version__}


def test_repeated_dispatch_prepares_credit_once_and_reaches_each_capture(provider, monkeypatch):
    if not hasattr(provider, "prepare_credit"):
        pytest.skip("requires the provisional Ackredit prepared-credit API")
    from pyunitwizard import _ackredit

    _ackredit._PREPARED.clear()
    original = provider.prepare_credit
    prepared = []

    def prepare(*args, **kwargs):
        prepared.append((args, kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(provider, "prepare_credit", prepare)
    q = puw.quantity(2.0, "meter", form="pint")
    runs = []
    with puw.attribution():
        for name in ("first", "reused"):
            with provider.capture(name) as run:
                assert puw.get_value(puw.convert(q, to_unit=q._REGISTRY.centimeter)) == 200.0
            runs.append(run.attribution.to_dict())
    assert len(prepared) == 1
    assert runs[0]["items"] == runs[1]["items"]
    assert len(runs[0]["uses"]) == len(runs[1]["uses"]) == 1


def test_prepared_backend_metadata_replacement_reports_gap_and_preserves_science(provider):
    if not hasattr(provider, "prepare_credit"):
        pytest.skip("requires the provisional Ackredit prepared-credit API")
    from ackredit.core.registry import Registry

    from pyunitwizard import _ackredit
    from pyunitwizard._private.smonitor.warnings import AckreditTrackingWarning

    _ackredit._PREPARED.clear()
    q = puw.quantity(2.0, "meter", form="pint")
    with puw.attribution(), provider.capture("warm") as warm:
        puw.convert(q, to_unit=q._REGISTRY.centimeter)
    item_id = warm.attribution.to_dict()["items"][0]["id"]
    original = Registry.items[item_id]
    Registry.items[item_id] = {**original, "version": "replaced"}
    try:
        with puw.attribution(), provider.capture("gap") as gap, pytest.warns(AckreditTrackingWarning) as diagnostics:
            result = puw.convert(q, to_unit=q._REGISTRY.centimeter)
        assert puw.get_value(result) == 200.0
        assert diagnostics[0].message.code == "PUW-WARN-ACK-001"
        assert "replaced or removed" in str(diagnostics[0].message)
        assert gap.attribution.to_dict()["items"] == []
    finally:
        Registry.items[item_id] = original


def test_released_portable_provider_fallback_retains_reused_credits(provider, monkeypatch):
    from pyunitwizard import _ackredit

    class ReleasedSurface:
        scope = staticmethod(provider.scope)
        register_item = staticmethod(provider.register_item)
        track_item = staticmethod(provider.track_item)

    monkeypatch.setattr(_ackredit, "backend", ReleasedSurface)
    q = puw.quantity(2.0, "meter", form="pint")
    runs = []
    with puw.attribution():
        for name in ("first", "reused"):
            with provider.capture(name) as run:
                assert puw.get_value(puw.convert(q, to_unit=q._REGISTRY.centimeter)) == 200.0
            runs.append(run.attribution.to_dict())
    assert runs[0]["items"] == runs[1]["items"]
    assert len(runs[0]["uses"]) == len(runs[1]["uses"]) == 1
    assert runs[0]["uses"][0]["context"]["software"] == "pint"


def test_noop_and_failed_calls_keep_entry_evidence_without_backend_success(provider):
    q = puw.quantity(2.0, "meter", form="pint")
    with provider.observe_calls(puw), puw.attribution():
        with provider.capture("noop") as noop:
            assert puw.convert(q) is q
        with provider.capture("failed") as failed:
            with pytest.raises(Exception):
                puw.convert(q, to_unit=q._REGISTRY.second)
    for run in (noop, failed):
        data = run.attribution.to_dict()
        assert len(data["items"]) == 1
        assert data["uses"][0]["used_by"] == "pyunitwizard.convert"
        assert data["uses"][0]["context"] == {"software": "pyunitwizard", "version": puw.__version__}


def test_translation_and_description_article_preserve_public_parent(provider):
    unyt = pytest.importorskip("unyt")
    q = puw.quantity([1.0, 2.0], "meter", form="pint")
    with provider.scope("pipeline"), provider.observe_calls(puw), puw.attribution():
        with provider.capture("translation") as run:
            result = puw.convert(q, to_form="unyt")
    assert result.value.tolist() == [1.0, 2.0]
    data = run.attribution.to_dict()
    assert {use["context"]["software"] for use in data["uses"]} == {"pyunitwizard", "pint", "unyt"}
    article = next(item for item in data["items"] if item["type"] == "article")
    assert article["doi"] == "10.21105/joss.00809"
    description = next(use for use in data["uses"] if use["item_id"] == article["id"])
    assert description["roles"] == ["software_description"]
    assert description["context"] == {"software": "unyt", "version": unyt.__version__}
    assert "pyunitwizard.convert" in data["usage_tree"]["pipeline"]["children"]
    parent = data["usage_tree"]["pyunitwizard.convert"]
    assert "pyunitwizard.forms.pint.quantity_to_unyt" in parent["children"]
    assert "10.21105/joss.00809" in run.attribution.report(format="bibtex")


def test_import_declaration_and_lazy_activation_do_not_credit_or_load_backends(observer):
    script = """
import sys
import pyunitwizard as puw
assert 'ackredit' not in sys.modules and 'pint' not in sys.modules
assert 'convert' not in vars(puw)
assert puw.__ackredit__['software']['version'] == puw.__version__
import ackredit
with ackredit.session('lazy'), ackredit.observe_calls(puw):
    assert 'convert' in vars(puw)
    assert 'pint' not in sys.modules and 'unyt' not in sys.modules
    assert ackredit.get_used_items() == {}
assert ackredit.get_used_items() == {}
"""
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr


def test_normally_installed_consumer_outside_checkout(observer, tmp_path):
    root = Path(__file__).resolve().parents[2]
    source = tmp_path / "producer-source"
    shutil.copytree(
        root,
        source,
        ignore=shutil.ignore_patterns(".git", "build", "dist", "*.egg-info", "__pycache__", ".pytest_cache"),
    )
    target = tmp_path / "installed"
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    builder = tmp_path / "builder"
    created = subprocess.run([sys.executable, "-m", "venv", str(builder)], capture_output=True, text=True)
    assert created.returncode == 0, created.stderr
    builder_python = builder / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    installed = subprocess.run(
        [str(builder_python), "-m", "pip", "install", "--no-deps", "--target", str(target), str(source)],
        cwd=consumer,
        capture_output=True,
        text=True,
    )
    assert installed.returncode == 0, installed.stdout + installed.stderr
    script = """
import importlib.abc, importlib.metadata, pathlib, sys
sys.path.insert(0, sys.argv[1])
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('optional provider unavailable', name=fullname)
block = NoAckredit()
sys.meta_path.insert(0, block)
import pyunitwizard as puw
assert pathlib.Path(puw.__file__).is_relative_to(pathlib.Path(sys.argv[1]))
assert puw.__version__ == importlib.metadata.version('pyunitwizard')
with puw.attribution():
    q = puw.quantity(2., 'meter', form='pint')
    assert puw.get_value(puw.convert(q, to_unit='centimeter')) == 200.
assert 'ackredit' not in sys.modules
"""
    absent = subprocess.run([sys.executable, "-c", script, str(target)], cwd=consumer, capture_output=True, text=True)
    assert absent.returncode == 0, absent.stderr
    script = """
import importlib.metadata, pathlib, sys
sys.path.insert(0, sys.argv[1])
import ackredit
import pyunitwizard as puw
assert pathlib.Path(puw.__file__).is_relative_to(pathlib.Path(sys.argv[1]))
assert puw.__version__ == importlib.metadata.version('pyunitwizard')
q = puw.quantity(2., 'meter', form='pint')
with ackredit.session('installed'), ackredit.scope('pipeline'), ackredit.observe_calls(puw), puw.attribution():
    runs = []
    for name in ('first', 'reused'):
        with ackredit.capture(name) as run:
            converted = puw.convert(q, to_unit=q._REGISTRY.centimeter)
        assert puw.get_value(converted) == 200.
        runs.append(run.attribution.to_dict())
assert runs[0]['items'] == runs[1]['items']
for data in runs:
    assert {u['context']['software'] for u in data['uses']} == {'pyunitwizard', 'pint'}
    assert 'pyunitwizard.convert' in data['usage_tree']['pipeline']['children']
    own = next(i for i in data['items'] if i.get('doi') == '10.5281/zenodo.8092688')
    assert own['version'] == puw.__version__
    assert 'Prada-Gracia' in ackredit.Attribution.from_dict(data).report(format='bibtex')
"""
    completed = subprocess.run(
        [sys.executable, "-c", script, str(target)], cwd=consumer, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_saved_own_reference_survives_reader_without_producer(provider, tmp_path):
    with provider.observe_calls(puw), provider.capture("producer") as run:
        q = puw.quantity(2.0, "meter", form="pint")
        puw.convert(q, to_unit=q._REGISTRY.centimeter)
    path = tmp_path / "result.json"
    path.write_text(json.dumps(run.attribution.to_dict()))
    script = """
import importlib.abc, json, pathlib, socket, sys
class NoProducer(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'pyunitwizard', 'pint', 'unyt'}:
            raise ModuleNotFoundError('producer unavailable', name=fullname)
sys.meta_path.insert(0, NoProducer())
def no_network(*args, **kwargs):
    raise AssertionError('saved attribution must not access the network')
socket.socket.connect = no_network
socket.create_connection = no_network
import ackredit
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
saved = ackredit.Attribution.from_dict(data)
assert saved.to_dict() == data
assert '10.5281/zenodo.8092688' in saved.report(format='bibtex')
assert ackredit.get_used_items() == {}
assert not {'pyunitwizard', 'pint', 'unyt'} & sys.modules.keys()
"""
    completed = subprocess.run([sys.executable, "-c", script, str(path)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
