"""Immutable declaration plans must validate values rather than borrowed identity."""

import sys
from copy import deepcopy
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

from pyunitwizard._private import backend_references as references


@pytest.fixture
def backend(monkeypatch):
    monkeypatch.setitem(sys.modules, "unyt", SimpleNamespace(__version__="3.1.0"))
    monkeypatch.setattr(references, "_SOFTWARE", deepcopy(references._SOFTWARE))
    monkeypatch.setattr(references, "_ARTICLES", deepcopy(references._ARTICLES))
    return "unyt"


def test_unchanged_declarations_reuse_an_immutable_value_validated_plan(backend, monkeypatch):
    first = references.plan(backend)
    detached = first.records()
    monkeypatch.setitem(references._SOFTWARE, backend, deepcopy(references._SOFTWARE[backend]))
    monkeypatch.setitem(references._ARTICLES, backend, deepcopy(references._ARTICLES[backend]))

    def unnecessary_copy(_):
        pytest.fail("unchanged declarations were detached again")

    monkeypatch.setattr(references, "records", unnecessary_copy)
    assert references.plan(backend) is first
    assert first.records() == detached


@pytest.mark.parametrize(
    "change",
    [
        "software_author",
        "article_author",
        "article_title",
        "version",
        "add_article",
        "article_only",
        "software_only",
    ],
)
def test_nested_metadata_version_and_declaration_changes_invalidate_the_plan(backend, change):
    first = references.plan(backend)
    original = first.records()
    if change == "software_author":
        references._SOFTWARE[backend]["authors"].append("Another developer")
    elif change == "article_author":
        references._ARTICLES[backend][0]["authors"].append("Another author")
    elif change == "article_title":
        references._ARTICLES[backend][0]["title"] = "Updated description"
    elif change == "version":
        sys.modules[backend].__version__ = "3.2.0"
    elif change == "add_article":
        references._ARTICLES[backend].append({"id": "article:extra", "type": "article", "title": "Extra"})
    elif change == "software_only":
        references._ARTICLES[backend].clear()
    else:
        references._SOFTWARE[backend] = None
    updated = references.plan(backend)
    assert updated is not first
    assert updated.records() == references.records(backend)
    assert first.records() == original
    assert references.plan(backend) is updated


def test_plan_owns_immutable_metadata_and_detaches_exports(backend):
    plan = references.plan(backend)
    expected = references.records(backend)
    with pytest.raises(FrozenInstanceError):
        plan.version = "changed"
    with pytest.raises(TypeError):
        plan.declarations[0]["record"]["title"] = "changed"
    with pytest.raises(AttributeError):
        plan.declarations[1]["record"]["authors"].append("changed")
    detached = plan.records()
    detached[0]["record"]["authors"].append("changed")
    detached[1]["context"]["version"] = "changed"
    assert plan.records() == expected


def test_missing_backend_or_declarations_do_not_reuse_a_stale_plan(backend, monkeypatch):
    first = references.plan(backend)
    monkeypatch.delitem(sys.modules, backend)
    assert references.plan(backend) is None
    monkeypatch.setitem(sys.modules, backend, SimpleNamespace(__version__="3.1.0"))
    assert references.plan(backend) is first
    monkeypatch.delitem(references._SOFTWARE, backend)
    assert references.plan(backend) is None


def test_supported_tuple_metadata_is_detached_without_changing_its_representation(backend):
    first = references.plan(backend)
    references._SOFTWARE[backend]["authors"] = tuple(references._SOFTWARE[backend]["authors"])
    updated = references.plan(backend)
    assert updated is not first
    assert updated.records() == references.records(backend)
    assert isinstance(updated.records()[0]["record"]["authors"], tuple)
    assert references.plan(backend) is updated
