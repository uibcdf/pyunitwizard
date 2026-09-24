# Why QuantityRecord

If your data move between tools, files, databases or services, sooner or later a number
arrives without its unit, or with a unit the receiver misreads. This page explains the
problem, what already exists to address it, and where
[QuantityRecord](quantity-records.md) stands among those solutions: what it does better,
what it does worse, and what it makes possible.

The full design record, with measurements and every alternative considered, is
[uibcdf/pyunitwizard#83](https://github.com/uibcdf/pyunitwizard/issues/83).

## The problem: a valid-looking number with the wrong unit

- **Mars Climate Orbiter (1999).** The interface specification required thruster impulse
  in newton-seconds, but the ground software wrote pound-force-seconds into the file. The
  factor was 4.45, and the spacecraft was lost
  ([NASA lessons learned](https://llis.nasa.gov/lesson/641)). The unit had been agreed in a
  *document*; it did not travel with the *data*.
- **Bioactivity databases.** ChEMBL flags records whose values differ by exactly 3 or 6
  orders of magnitude from otherwise identical entries as a *potential transcription
  error*, a likely µM-for-nM confusion
  ([ChEMBL FAQ](https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/chembl-data-questions)).
  A dimension check cannot catch this: both values are concentrations.
- **Our own ecosystem.** While designing this form we found a viewer that took a
  standardized length, dropped its unit and assumed nanometres. Under a user whose standard
  length was ångström, a simulation box was drawn ten times too large, with no error
  ([uibcdf/molsysviewer#96](https://github.com/uibcdf/molsysviewer/issues/96)). We also
  found a file format whose readers could take the unit from different places, or fall
  back silently to a default
  ([uibcdf/molsysmt#240](https://github.com/uibcdf/molsysmt/issues/240)).

The common thread: **the unit is lost, or assumed, at a boundary.** Units libraries keep
units right *inside* one program. They do not, by themselves, keep them right *between*
programs.

## What already exists

| Approach | What it gives | What it leaves open |
|---|---|---|
| **Unit libraries** (pint, astropy, unyt, openmm.unit) | Correct units and conversions in memory | No storage format of their own. Pint suggests `str(q)` or `to_tuple()` ([docs](https://pint.readthedocs.io/en/stable/advanced/serialization.html)). Quantities from different pint registries cannot be combined. Pint has no notion of quantity *kinds* ([pint#676](https://github.com/hgrecco/pint/issues/676), closed). |
| **Per-value `{value, unit}` records** (for example OpenFF: [openff-units](https://github.com/openforcefield/openff-units), [openff-models](https://github.com/openforcefield/openff-models)) | The unit next to every value; simple and readable | No integrity check and no reader handshake. Costly for arrays: in our measurements, 4.3× the size and 5× the load time of the bare numbers. |
| **CF conventions / UDUNITS** (NetCDF, and Zarr by convention) | A required `units` attribute per variable, and `standard_name` as a kind; decades of use ([CF units](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/build/ch03.html)) | Nothing detects a unit or a value changed by a tool that ignores the convention. The reader is not required to state what it expects. |
| **ASDF** (astronomy) | A `quantity` type with value and unit, and binary blocks with a checksum ([quantity schema](https://www.asdf-format.org/projects/asdf-standard/en/latest/generated/stsci.edu/asdf/unit/quantity-1.2.0.html)) | The MD5 checksum is **optional**, covers the **block bytes only**, not the unit, and the behaviour on a mismatch is **not defined** ([file layout](https://www.asdf-format.org/projects/asdf-standard/en/latest/file_layout.html)). |
| **Container checksums** (HDF5 Fletcher32, Parquet page CRC, BagIt manifests) | Detect corruption of bytes or files | Any writer recomputes them, so they cannot tell a correct write from one that bypassed the rules. They say nothing about units. |
| **UCUM** (HL7/FHIR, LOINC) | A formal, portable spelling of units (`mol/L`; no `M` for molar, since `M` is mega) ([ucum.org](https://ucum.org/ucum)) | A spelling only: no container, no integrity. |
| **QUDT** and the **OBO Units Ontology** | Unit identifiers, conversion multipliers to SI, dimension vectors and quantity kinds ([QUDT](https://www.qudt.org/pages/QUDToverviewPage.html), [UO](http://obofoundry.org/ontology/uo.html)) | Semantics only: no data format. |
| **D-SI** (metrology, PTB) | Strict SI exchange of measurement data ([D-SI](https://www.dmet.ptb.de/d-si)) | Built for calibration certificates; heavy for large arrays. |

Each of these solves part of the problem well. None of the ones we examined combines all
three things a boundary needs: **the unit and the values protected together, a reader
that must say what it expects, and no default when something is missing.**

## Where QuantityRecord stands

| | QuantityRecord | Best existing alternative | |
|---|---|---|---|
| Unit travels with the values | Inside the same object | CF, ASDF, OpenFF | equal |
| Integrity of unit **and** values together | Digest over the unit description and the values' bytes | ASDF: optional, bytes only | **better** |
| Detects writes that bypassed the library | Only the codec produces the digest | Container checksums are recomputed by any writer | **better** |
| Behaviour on failure | Always an error; never a default unit | ASDF: undefined; CF: a required attribute, but readers are not held to it | **better** |
| Reader states its expectations | Field, unit, dimensionality, kind | Not formalized elsewhere | **better** |
| A record copied into another field | Refused | Not detected elsewhere | **better** |
| Unit renamed and then resealed | Caught: name and SI description must agree | QUDT holds both, but does not check one against the other | **better** |
| Quantity kinds (Hz vs Bq, J vs N·m) | Optional `kind`, with QUDT or UO identifiers | QUDT, CF `standard_name` | equal (reused) |
| Readable without the library | A reference reader in the Python standard library, and published test vectors | CF needs UDUNITS; ASDF needs its library | **better** |
| Portable across languages | Canonical binary encoding of the manifest; strict JSON (no NaN) | CF and ASDF, within their ecosystems | equal |
| Many units across backends | pint, openmm.unit, astropy.units, unyt… through PyUnitWizard | OpenFF: pint; ASDF: astropy | **better** |
| Cost | Base64: 1.33× raw size; JSON text: 2.4×; a digest at about 0.3–0.6 GB/s | Bare numbers: no cost | **worse**, by design |
| Maturity and adoption | New and provisional | CF: decades; UCUM: a clinical standard | **worse** |
| Editing data by hand | Refused unless resealed through the library | Free | **worse** in comfort, which is the protection |
| Deliberate forgery | Out of scope: the threat model is mistakes | D-SI certificates carry signatures | **worse** |

Our reading: QuantityRecord wins exactly in the gap nobody covered (integrity, handshake,
no defaults) and loses in maturity and convenience. It does not compete with the
standards. It reuses them: QUDT and UO for kinds, QUDT's semantics for the SI description,
and CF for containers (a planned HDF5 binding writes CF's `units` attribute too).

## What it makes possible

- **CF-compatible and verified data.** Every CF tool still reads the unit, and
  QuantityRecord additionally proves that nobody changed it or the values.
- **Finding who broke a record.** A failed verification means something wrote outside the
  contract, instead of a silently wrong number further down the pipeline.
- **One bridge between unit ecosystems.** Records convert to and from every form
  PyUnitWizard supports, with the same checks at every step.
- **Compact, verified data with mixed units.** A planned layout gives every value a
  one-byte unit code, for tables where the units really vary from row to row.

## What no format can do

A writer that is wrong *and* consistent (it meant nM, built pM and wrote pM) produces a
record that is coherent with itself. That case is covered by contracts at your API
boundaries, by tests that compare values across tools, and by domain checks such as
ChEMBL's orders-of-magnitude flag. QuantityRecord makes sure that such a mistake is the
*only* kind left.

## Measured

The measurements come from the prototype and from this implementation (Python 3.13,
pint 0.25.3); the full tables are in
[#83](https://github.com/uibcdf/pyunitwizard/issues/83) and
[#82](https://github.com/uibcdf/pyunitwizard/issues/82).

- A prototype was subjected to deliberate slips: hand edits, raw appends, renamed or
  respelled units, reordered, truncated or pasted values, deleted manifests, and records
  copied between fields. Every slip was refused.
- Base64 encoding: 100,000 values are written in about 5 ms and read, verified, in about
  4 ms.
- A bundle stores the scalars of a document at about half the size of separate records.
