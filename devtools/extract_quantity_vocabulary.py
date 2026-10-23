"""Reproduce the bounded vocabulary from exact, locally supplied upstream files.

Usage: python devtools/extract_quantity_vocabulary.py INPUT_DIRECTORY OUTPUT
The input directory must contain qudt-units.ttl, qudt-kinds.ttl and uo.obo.
No network, ontology reasoning or uncontrolled vocabulary updates occur here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

INPUTS = {
    "qudt-units.ttl": "5e84f3e10ae6a3c535e2e7616dc2affee09dd52bea5229822188730493fd4418",
    "qudt-kinds.ttl": "b246c2f851e3c9353cafddf9640b18b696c410e176b29735218f7a266bcb9888",
    "uo.obo": "ade7be5a515551d3d653bda8ad256563df322e83c96b41da4f848e8a470c2846",
}
# Explicit local alignments reviewed against both published definitions and UO
# ancestry. Neither vocabulary publishes these as upstream exactMatch triples.
ALIGNMENTS = {
    "HZ": ("hertz", "UO:0000106", "UO:0000105"),
    "BQ": ("becquerel", "UO:0000132", "UO:0000128"),
    "RAD-PER-SEC": ("radian / second", "UO:0000079", "UO:0000049"),
}


def extract(directory: Path) -> dict:
    """Extract reviewed identifiers only after verifying all original input bytes."""
    for name, expected in INPUTS.items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Original vocabulary identity mismatch: {name}")
    from rdflib import RDF, Graph, Namespace, URIRef

    graph = Graph().parse(directory / "qudt-units.ttl", format="turtle")
    graph.parse(directory / "qudt-kinds.ttl", format="turtle")
    q = Namespace("http://qudt.org/schema/qudt/")
    terms = {}
    for stanza in (directory / "uo.obo").read_text().split("[Term]\n")[1:]:
        identity = re.search(r"^id: (UO:\d+)$", stanza, re.M)
        label = re.search(r"^name: (.+)$", stanza, re.M)
        if identity and label:
            terms[identity[1]] = {"label": label[1], "parents": re.findall(r"^is_a: (UO:\d+)", stanza, re.M)}

    def ancestors(identity):
        result, pending = set(), [identity]
        while pending:
            term = pending.pop()
            if term not in result:
                result.add(term)
                pending.extend(terms[term]["parents"])
        return result

    units = {}
    axes = {"A": "mol", "E": "A", "L": "m", "I": "cd", "M": "kg", "H": "K", "T": "s"}
    for name, (computing, obo_id, category) in ALIGNMENTS.items():
        identity = "http://qudt.org/vocab/unit/" + name
        subject = URIRef(identity)
        kinds = sorted(str(kind) for kind in graph.objects(subject, q.unitForQuantityKind))
        if not kinds or any((URIRef(kind), RDF.type, q.QuantityKind) not in graph for kind in kinds):
            raise ValueError(f"Missing authoritative quantity-kind relationship: {name}")
        vector = str(graph.value(subject, q.hasDimensionVector)).rsplit("/", 1)[-1]
        exponents = {axes[axis]: int(power) for axis, power in re.findall(r"([AELIMHT])(-?\d+)", vector) if int(power)}
        factor = float(graph.value(subject, q.conversionMultiplier))
        offset = float(graph.value(subject, q.conversionOffset) or 0)
        if category not in ancestors(obo_id):
            raise ValueError(f"UO semantic ancestry changed: {obo_id}")
        entry = {
            "computing_unit": computing,
            "kinds": kinds,
            "si": {"factor": factor, "offset": offset, "exponents": exponents},
            "ucum": str(graph.value(subject, q.ucumCode)),
        }
        units[identity] = {**entry, "source": "qudt"}
        obo_iri = "http://purl.obolibrary.org/obo/" + obo_id.replace(":", "_")
        units[obo_iri] = {
            **entry,
            "source": "uo",
            "label": terms[obo_id]["label"],
            "category": category,
            "qudt_alignment": identity,
        }
    return {
        "format": "pyunitwizard-vocabulary/0.1",
        "alignment": "PyUnitWizard reviewed local unit correspondence, not an upstream exactMatch or a general ontology reasoner. QUDT unitForQuantityKind and UO ancestry are retained separately; UO identifiers denote units, never quantity kinds.",
        "sources": {
            "qudt": {
                "release": "3.5.3",
                "commit": "07acd3f9ee2c7189341f322c85154ca63c9198f2",
                "url": "https://github.com/qudt/qudt-public-repo/tree/07acd3f9ee2c7189341f322c85154ca63c9198f2/src/main/rdf/vocab",
                "license": "CC-BY-4.0",
                "attribution": "QUDT.org, Inc., QUDT public unit and quantity-kind vocabularies",
                "files": {name: digest for name, digest in INPUTS.items() if name.startswith("qudt-")},
            },
            "uo": {
                "release": "2026-10-12",
                "commit": "311f3d222444fcf8adf032dfa58f3c1b55bd22af",
                "url": "https://github.com/bio-ontology-research-group/unit-ontology/blob/311f3d222444fcf8adf032dfa58f3c1b55bd22af/uo.obo",
                "license": "CC-BY-4.0",
                "attribution": "Units Ontology contributors, OBO Units Ontology",
                "files": {"uo.obo": INPUTS["uo.obo"]},
            },
        },
        "units": units,
    }


def main() -> None:
    """Write the reproducible, attributed catalogue from exact original sources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(extract(args.directory), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
