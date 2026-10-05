"""Offline declarations for the bounded Pint/unyt attribution pilot.

Sources: https://github.com/hgrecco/pint and
https://github.com/yt-project/unyt/blob/main/README.rst.
An article's publication year is independent of the executed software version.
"""

import sys
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Optional

_SOFTWARE = {
    "pint": {
        "type": "software",
        "title": "Pint: makes units easy",
        "authors": ["Pint contributors"],
        "url": "https://github.com/hgrecco/pint",
    },
    "unyt": {
        "type": "software",
        "title": "unyt",
        "authors": ["unyt developers"],
        "url": "https://github.com/yt-project/unyt",
    },
}
_ARTICLES = {
    "unyt": [
        {
            "id": "doi:10.21105/joss.00809",
            "type": "article",
            "title": "unyt: Handle, manipulate, and convert data with units in Python",
            "authors": [
                "Goldbaum, Nathan J.",
                "ZuHone, John A.",
                "Turk, Matthew J.",
                "Kowalik, Kacper",
                "Rosen, Anna L.",
            ],
            "doi": "10.21105/joss.00809",
            "year": 2018,
            "journal": "Journal of Open Source Software",
            "volume": 3,
            "number": 28,
            "pages": "809",
        }
    ],
}

_PLANS = {}


class _FrozenList(tuple):
    """Compare an immutable list snapshot with current mutable declaration values."""

    __slots__ = ()

    def __eq__(self, other):
        if not isinstance(other, (list, _FrozenList)):
            return False
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __ne__(self, other):
        return not self == other


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return _FrozenList(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError("Backend declarations must contain JSON values")


def _detach(value):
    if isinstance(value, MappingProxyType):
        return {key: _detach(item) for key, item in value.items()}
    if isinstance(value, _FrozenList):
        return [_detach(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_detach(item) for item in value)
    return value


@dataclass(frozen=True)
class _DeclarationPlan:
    version: str
    software: object
    articles: object
    declarations: object

    def records(self):
        """Return mutable records detached from this plan for provider registration."""
        return _detach(self.declarations)


def plan(library: str) -> Optional[_DeclarationPlan]:
    """Reuse an immutable plan only while executed version and metadata match.

    Comparisons inspect current values, including nested edits to the offline
    declarations. The cache retains only the latest plan for each pilot backend;
    old plans held by prepared credits keep their original immutable metadata.
    Does not import any backend/provider or perform bibliographic lookup.
    """
    module = sys.modules.get(library)
    if module is None or library not in _SOFTWARE:
        return None
    version = str(module.__version__)
    software = _SOFTWARE[library]
    articles = _ARTICLES.get(library, [])
    previous = _PLANS.get(library)
    if (
        previous is not None
        and previous.version == version
        and previous.software == software
        and previous.articles == articles
    ):
        return previous
    current = _DeclarationPlan(version, _freeze(software), _freeze(articles), _freeze(records(library)))
    _PLANS[library] = current
    return current


def records(library):
    """Detach bibliographic declarations for an already executed pilot backend.

    Does not import the backend or provider, or look up a DOI. Software-only,
    article-only and combined declarations have the same credit boundary.
    """
    module = sys.modules.get(library)
    if module is None or library not in _SOFTWARE:
        return []
    version = str(module.__version__)
    context = {"software": library, "version": version}
    result = []
    if _SOFTWARE[library] is not None:
        software = deepcopy(_SOFTWARE[library])
        software.update(id=f"software:{library}:{version}", version=version)
        result.append({"record": software, "roles": ["executed_software"], "context": deepcopy(context)})
    result.extend(
        {"record": deepcopy(article), "roles": ["software_description"], "context": deepcopy(context)}
        for article in _ARTICLES.get(library, [])
    )
    return result
