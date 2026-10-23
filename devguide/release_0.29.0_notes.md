# PyUnitWizard 0.29.0

This additive release expands verified quantity exchange while retaining the
existing computing APIs, session policy and qrec/0.3 / bundle bytes.

- Tagged QuantityRecord arrays share unit/kind descriptors; homogeneous immutable
  append checks conversion, dtype and trailing shape (#102/#105).
- Zarr snapshots support verified first-axis partial reads; typed Arrow tables
  and complete local Parquet bindings retain explicit unit/kind handshakes
  (#104/#103).
- Case-sensitive UCUM tools validate explicit output codes and import biomedical
  values through actual ucumvert 0.3.2 (#125). Only independently qualified
  physical atoms are admitted; unchecked provider aliases are refused.
- Native ASDF/Astropy quantities carry an additional sealed snapshot binding;
  readers check named unit meaning, SI scale, dtype/shape, value seals and their
  own expectations (#126).
- Explicit QUDT/UO annotations bind a record and selected identifiers to an
  offline attributed catalogue for hertz, becquerel and radians/second (#127).
  Quantity kinds are chosen by consumers, never inferred from SI dimensions.
- Earlier source fixes preserve OpenMM angstrom meaning in unyt, reuse unyt
  registries, preserve atomic-mass names/prefixes and record actual benchmark
  interpreter provenance (#120–#124).

All record extensions, optional dialects/storage bindings, measurement statements
and attribution surfaces remain **provisional**. New format identifiers are
explicit; old readers must not interpret them as old formats. QUDT/UO
correspondences are reviewed local alignments, not upstream exactMatch claims.

Limits remain explicit: immutable append copies values; Zarr selection verifies
selected chunk contents; Arrow nulls are refused and Parquet reads whole files.
ASDF is homogeneous/multiplicative only; affine temperatures need explicit
conversion to Kelvin. Unknown vocabularies, arbitrary/nonlinear/annotated UCUM
units, CF calendar coordinates, full clinical/astronomy schemas and consumer
migrations are outside this checkpoint. Seals establish integrity, not producer
authentication or scientific truth of an asserted kind.

Baseline support remains Linux/macOS arm64, Python 3.11–3.14. Optional profiles
retain their own provider/interpreter constraints, including OpenFF 0.4.0 on
Python 3.12–3.14 with Pint <0.26 and UCUM's Pint >=0.25 requirement.

Exact source, immutable Conda artifact, installed matrix and publication receipts
are tracked in [release #128](https://github.com/uibcdf/pyunitwizard/issues/128).
Publication of this version does not admit the provisional contracts as stable
or establish adoption in consuming repositories.
