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


## Published outcome — 2026-10-23

Stable Release [0.29.0](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.0)
and independently dereferenced annotated tag identify original source
`cfe067bcc4545c60aaca4c6950f6d84075ee6c36`. All 29 mandatory exact-source jobs
and actual CI/Codecov uploads passed. Eight optional source-wheel probes passed
247 cases each without skips. The pre-tag decision is
https://github.com/uibcdf/pyunitwizard/issues/128#issuecomment-6374828043.

Original producer 40014661788, attempt 1, built
`pyunitwizard-0.29.0-py_0.tar.bz2`, 94,325 bytes, SHA-256
`9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34`.
Installed run 40018157605/1 passed 30 cells plus the producer verifier. Native
jobs belong to qualifier `821231dbf188656b6872b5f6866b20e9114c87fb`; the owner
receipt separately binds it to the original source/file. #131 selected core
Astropy rather than unrelated recommended cloud extras. No package was rebuilt.
Every required storage/dialect module executed unskipped in eight storage cells,
and every prepared module in eight prepared cells. Intentional strict-JSON/NaN
and unavailable prepared APIs elsewhere remain classified. The installed Conda
lane excludes its nested source-wheel builder, which source suites execute.

Promotion 40025174221 preserved the original digest. The independent pinned
public verifier confirms both main label and solver index. Release-event route
40025139973 verified the staged decision and skipped both build branches.
Tag policy 40025122590 and archive CI/policy 40024974249/40024974932 passed.
Documentation publication 40025140029 used the original release source; the
served UCUM/ASDF/vocabulary, record-extension and quantity-record pages return
200 with 0.29.0 titles. The gh-pages README identifies the same original source.
The direct HTTP probe requires a browser User-Agent (the default Python agent
received 403); cached search content is not used as current evidence.

A fresh public-only Linux/Python 3.14.9 installation imported the original file
and passed 39 record-array/tagged/append/vocabulary guards without skips, plus
version/origin/digest/resource, empty-base64 and same-dimension refusal checks.
Pip reports no broken requirements. Its freely resolved ArgDigest 0.17.0,
DepDigest 0.15.1, SMonitor 0.22.0, NumPy 2.5.4 and Pint 0.26.2 are retained
separately from the pinned required-floor matrix; this smoke does not claim a
new full matrix for those versions. No publication exception was needed.

Complete safe receipts are `devguide/evidence/release_0.29.0_2026-10-23.json`,
with separately retained source, producer, original archive, installed binding,
all 30 Conda/pip closures and JUnit case classifications alongside it.
Earlier failed candidates/qualifications remain recorded under #129/#130/#131.
The selected guard protects the prepared public-provider profile and required
real regression/reader guards; it does not replace executed science or actual
public availability observations.

The version-specific availability/guide handoff is
[MolSysSuite #132](https://github.com/uibcdf/molsyssuite/issues/132). Canonical
`standards/PYUNITWIZARD_GUIDE.md` SHA-256 is
`4d8ffa308b0a004b0b1caa1fa58a871fb715f200f4864b2c1b18416184afc184`.
Suite receiving owners synchronize client copies and pins; source adoption is
not claimed. All provisional and unsupported-scope limits above remain.
