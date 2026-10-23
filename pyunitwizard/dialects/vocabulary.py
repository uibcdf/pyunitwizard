"""Bounded explicit QUDT/UO annotations bound to existing sealed records.

Only hertz, becquerel and radians per second are admitted. Identifiers and
quantity kinds are never inferred from dimensions. UO identifiers denote units;
the reviewed local alignment does not turn them into quantity-kind identifiers.
"""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from importlib.resources import files
from typing import Any, Dict, Mapping

import numpy as np

from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest

__all__ = ["FORMAT", "catalog", "annotate", "validate_annotation"]
FORMAT = "qrec-vocabulary/0.1"


@lru_cache(maxsize=1)
def _catalog():
    data = json.loads(files("pyunitwizard.vocabularies").joinpath("physical_units.json").read_text())
    if data["format"] != "pyunitwizard-vocabulary/0.1":
        raise RecordError(reason="unsupported installed physical-unit catalogue")
    return data, metadata_digest(data)


def catalog() -> Dict[str, Any]:
    """Return the detached authoritative subset and reviewed-alignment provenance.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        Pinned QUDT/UO facts, source commits/digests, attribution and license.

    Raises
    ------
    RecordError
        If the installed catalogue format is unsupported.

    Examples
    --------
    >>> catalog()['sources']['qudt']['release']
    '3.5.3'
    """
    return copy.deepcopy(_catalog()[0])


def annotate(record: QuantityRecord, *, unit_iri: str, kind_iri: str) -> Dict[str, Any]:
    """Bind explicit unit/kind identifiers to an already kind-tagged record.

    Parameters
    ----------
    record : QuantityRecord
        Homogeneous record whose existing ``kind`` equals ``kind_iri`` and
        whose named unit matches the bounded catalogue exactly after codec
        canonicalization. Convert explicitly before annotating other scales
        or unnamed SI expressions. Values and the original seal stay unchanged.
    unit_iri : str
        Registered QUDT unit or OBO UO unit IRI.
    kind_iri : str
        Registered QUDT quantity-kind IRI, explicitly selected by the consumer.

    Returns
    -------
    dict
        Provisional sealed annotation sidecar bound to the original record
        digest and the installed catalogue. Retain it alongside that record.

    Raises
    ------
    RecordError
        For missing/unknown kinds or units, mismatched named meanings or SI
        definitions, or unsupported layout. This is not semantic inference or
        proof that a consumer assigned its scientific kind correctly.

    Examples
    --------
    >>> note = annotate(record, unit_iri='http://qudt.org/vocab/unit/HZ',
    ...                 kind_iri='http://qudt.org/vocab/quantitykind/Frequency')
    """
    if not isinstance(record, QuantityRecord) or record.layout != "homogeneous":
        raise RecordError(reason="vocabulary annotation requires a homogeneous QuantityRecord")
    data, catalog_digest = _catalog()
    if not isinstance(unit_iri, str) or unit_iri not in data["units"]:
        raise RecordError(reason="unit IRI is outside the bounded vocabulary catalogue")
    entry = data["units"][unit_iri]
    if not isinstance(kind_iri, str) or kind_iri not in entry["kinds"] or record.kind != kind_iri:
        raise RecordError(reason="explicit record kind, quantity-kind IRI and published unit semantics disagree")
    if record.unit != entry["computing_unit"]:
        raise RecordError(
            reason="named computing unit does not match the vocabulary meaning; convert explicitly first"
        )
    actual, expected = record.si, entry["si"]
    if actual["exponents"] != expected["exponents"] or not np.allclose(
        [actual["factor"], actual["offset"]], [expected["factor"], expected["offset"]], rtol=1e-12, atol=0
    ):
        raise RecordError(reason="computing unit disagrees with the authoritative SI definition")
    node = {
        "format": FORMAT,
        "record_digest": record.digest,
        "catalog_digest": catalog_digest,
        "unit_iri": unit_iri,
        "kind_iri": kind_iri,
    }
    node["digest"] = metadata_digest(node)
    return node


def validate_annotation(
    record: QuantityRecord,
    annotation: Mapping[str, Any],
    *,
    unit_iri: str,
    kind_iri: str,
) -> None:
    """Check a complete annotation against its record, catalogue and reader intent.

    Parameters
    ----------
    record : QuantityRecord
        Independently verified source snapshot.
    annotation : mapping
        Complete sidecar previously produced by ``annotate``.
    unit_iri, kind_iri : str
        Required identifiers expected by the receiving consumer.

    Returns
    -------
    None

    Raises
    ------
    RecordError
        For disagreement, corruption, unsupported format/catalogue or changed
        record identity. The digest establishes integrity, not authentication.

    Examples
    --------
    >>> validate_annotation(record, note, unit_iri=note['unit_iri'],
    ...                     kind_iri='http://qudt.org/vocab/quantitykind/Frequency')
    """
    expected = annotate(record, unit_iri=unit_iri, kind_iri=kind_iri)
    if not isinstance(annotation, Mapping) or dict(annotation) != expected:
        raise RecordError(reason="vocabulary annotation disagrees with its record, catalogue or receiver expectations")
