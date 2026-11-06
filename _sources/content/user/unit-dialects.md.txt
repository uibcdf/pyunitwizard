# UCUM, native ASDF and explicit vocabulary annotations

These optional tools implement bounded interoperability contracts under #85.
They are **provisional**, as are `qrec-asdf/0.1` and `qrec-vocabulary/0.1`.
Existing `qrec/0.3` and bundle bytes, computing forms and session parser selection
are unchanged. The [CF/HDF5 tools](hdf5-cf.md) retain their physical-unit scope;
calendar/reference-time coordinates need a separately justified consumer contract.

## Case-sensitive UCUM exchange

Install `ucumvert==0.3.2` (requires Python 3.11+ and Pint 0.25+). Imports remain
lazy; this provider is unnecessary for ordinary quantities or saved records.

```python
import numpy as np
from pyunitwizard.dialects import ucum

# Verify the label for unchanged numbers before writing it to a protocol.
code = ucum.validate_unit("nanomolar", "nmol/L")
quantity = ucum.parse_quantity([1000, 2000], code,
                               unit="micromolar", form="pint")
np.testing.assert_allclose(quantity.magnitude, [1.0, 2.0])
```

The output code is supplied explicitly and retained verbatim. It is validated
against the actual UCUM grammar and its physical scale/offset, rather than
guessed from Pint aliases. UCUM has no unique canonical spelling, and the
provider offers no general Pint-to-UCUM canonicalizer. `nM` and standalone `M`
are refused as UCUM codes. The committed Sabueso/ChEMBL fixture exercises 343
actual concentration/percentage observations using `nmol/L` and `%`.

The independently qualified atoms are `m s g rad K C cd mol sr Hz Bq N Pa J W A V
F Ohm S Wb T H l L % min h d`, plus the simple temperatures below. UCUM-legal
prefixes, products/quotients and integer powers of these atoms are supported.
Other atoms need separate conformance qualification; the beta provider's full
vocabulary is not advertised. In particular its arcminute/apostrophe mapping is
refused because it currently maps to a time minute.
Annotations, arbitrary biological units, logarithmic units and arbitrary numeric
scale expressions are refused. They cannot silently disappear into a physical
unit. No assay interpretation, missing-value policy or quantity kind is inferred.
Target units must also be supported by the requested computing backend; for
example, unyt concentrations can use `mole / liter` explicitly.

Temperatures require `units_metadata="temperature: on_scale"` or
`"temperature: difference"` at both ends, as in the CF tools. Simple `Cel`
supports affine conversion; other special temperatures and compound special
units are refused. The provider's bracketed Fahrenheit/Reaumur atoms are not
qualified across the supported Pint versions. Convert explicitly to Celsius or
kelvin before UCUM exchange. A difference needs a zero-offset computing unit, such as
`delta_degree_Celsius` or kelvin. Validation uses relative tolerance 1e-12.

These are unit tools, not a FHIR resource writer or a clinical schema validator.
They do not add UCUM codes to ordinary session parsers or qrec manifests.

## Native ASDF snapshots

Install `asdf=6.0.0` and `asdf-astropy=0.11.0` from conda-forge, or the same
versions with pip. Astropy remains an optional computing provider.

```python
import numpy as np
from astropy import units as u
from pyunitwizard.record import QuantityRecord
from pyunitwizard.storage import asdf

kind = "http://qudt.org/vocab/quantitykind/AngularVelocity"
record = QuantityRecord.from_quantity(
    np.array([1.0, 2.0]) * u.rad / u.s,
    field="proper_motion", kind=kind,
)
asdf.write("proper_motion.asdf", record)  # new local path only
restored = asdf.read("proper_motion.asdf", field="proper_motion",
                     unit="radian / second", kind=kind)
assert restored == record
```

The file contains a native Astropy `quantity`, readable with ordinary
`asdf.open`, and a `pyunitwizard` binding header. That header binds the native
unit spelling to the original qrec metadata. Reads verify native physical
dimensions/scale, dtype/shape, value seals and explicit receiver expectations.
ASDF block checksums are also enabled. The returned record is detached from
the closed file. `to_tree` and `from_tree` expose the same contract for callers
that already own an ASDF tree. Unit or dimensionality is required on reads.

Publication is exclusive: an owned same-directory temporary file is linked to
the destination atomically, and only that temporary is removed on failure.
Existing files are never replaced. Seals establish integrity, not authenticity.

The initial contract covers complete homogeneous scalar/empty/array snapshots
in multiplicative physical units. Convert affine temperatures explicitly to
kelvin first. Tagged arrays, coordinate frames/epochs, remote/partial reads,
disk append and migration of native unsealed archives are outside this binding.
A native archive without the binding manifest is refused. Consumers can read
such a legacy archive with its original provider and apply their own explicit
unit/schema migration before constructing a new record.

The real-data test retains six Gaia DR2 proper-motion pairs from Astropy's
HD 219829 tutorial, including original unit, source IDs, source commit and file
hash. The consumer converts mas/year to radians/second explicitly. The resulting
ASDF snapshot is newly produced from those observations; it was not originally
published by Gaia. Coordinate geometry and epoch propagation stay with Astropy
and the astronomy consumer.

## Explicit QUDT and OBO unit annotations

The packaged offline catalogue needs no ontology, UCUM or astronomy provider.
It admits three named meanings: hertz, becquerel and radians/second. Each has a
QUDT unit IRI and an OBO Units Ontology (UO) unit IRI. QUDT quantity-kind IRIs
remain separate from UO unit/category identifiers.

```python
from pyunitwizard.dialects import vocabulary

unit_iri = "http://qudt.org/vocab/unit/RAD-PER-SEC"
note = vocabulary.annotate(record, unit_iri=unit_iri, kind_iri=kind)
vocabulary.validate_annotation(restored, note,
                               unit_iri=unit_iri, kind_iri=kind)
```

Consumers choose the scientific kind before creating the record. Annotation
requires that existing kind, an admitted published unit/kind relationship,
the named computing unit and the authoritative SI definition to agree. Equal
dimensions alone never suffice: a Gaia angular rate cannot be relabelled as
frequency or radioactivity. Other scales and unnamed SI expressions require
explicit consumer conversion before annotation. Global tagged annotations are
refused; qualify homogeneous records independently.

The sidecar seals the original record digest, catalogue digest and selected
IRIs. Keep it with that record and supply the receiver's expected IRIs when
validating it. It does not prove that the consumer assigned the correct scientific
kind, authenticate a producer, modify the record or implement general ontology
reasoning. ASDF's initial binding does not embed this separate sidecar.

`vocabulary.catalog()` returns detached facts, attribution and exact upstream
identities: QUDT 3.5.3 and UO 2026-10-12, both CC BY 4.0. The QUDT/UO
correspondences are **reviewed local PyUnitWizard alignments**, not asserted
upstream `exactMatch` triples. The offline extractor refuses changed original
file hashes or missing quantity-kind/UO ancestry evidence. See the installed
`pyunitwizard/vocabularies/NOTICE.md` for provenance and reproduction.

Source/installed qualification and exact public artifact availability are
tracked in the owning #125, #126, #127 and release #128 records. A local test or
guide update alone does not establish a published package or consumer adoption.
