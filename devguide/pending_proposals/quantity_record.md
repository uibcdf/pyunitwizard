---
summary: QuantityRecord — an inert interchange form that never loses or misreads a unit (provisional MVP implemented).
issue: uibcdf/pyunitwizard#82
status: active
opened: 2026-09-24
closed:
verification: measured
area: [serialization, interoperability, forms]
guard:
normative:
blocked_by: []
supersedes: []
---

# QuantityRecord: PyUnitWizard's inert interchange form

## What

A form, `"record"`, whose objects (`QuantityRecord`) carry values together with a verified
description of their unit, so that a number is never read in a unit it was not written in.
It is inert like `"string"`: it converts to and from every form and does not compute.
`QuantityRecordBundle` seals many small quantities of one document (a card) together.

The design, its motivation, the alternatives evaluated (per-value `{value, unit}`, unit
strings, pint tuples, unenforced container manifests, ASDF, CF/UDUNITS, OpenFF, HDF5 and
Parquet checksums, UCUM, QUDT, UO, D-SI) and the prior art (ArgDigest's removed passport
and declined value certification) are recorded in uibcdf/pyunitwizard#83. It supersedes
`devguide/serialization_contract_draft.md`, whose safety rules it meets and whose
promotion gate (two real integration cases) is met by uibcdf/sabueso#32 and
uibcdf/molsysmt#240.

## How

Implemented in this MVP (`pyunitwizard/record.py`, `forms/api_record.py`):

- **Manifest**: `format` (`qrec/0.3`), `field` (or null), `unit` (canonical name: pint's
  default long form, whatever display format a registry is configured with), `si`
  (`factor`, `offset`, `exponents` over `m, kg, s, A, K, mol, cd`, with QUDT's semantics),
  optional `kind` (quantity-kind IRI), `dtype`, `shape` and `blocks`.
- **Seal**: blake2b-128 per block, and a record digest over the canonical manifest and the
  block digests. The manifest is encoded with a tagged little-endian binary encoding,
  because JSON text is not canonical across languages; the values are C-order
  little-endian bytes with NaN canonicalized.
- **Reading**: `from_dict` refuses a missing manifest (there is no default unit), an
  unknown format, a malformed dtype or shape, a broken seal, or a unit whose canonical name
  disagrees with its SI description beyond a relative 1e-6. `to_quantity(field=, unit=,
  dimensionality=, kind=, form=)` is the handshake.
- **Encodings**: strict JSON, which refuses NaN and infinity because other languages
  cannot read them, and base64.
- **Form integration**: `get_form` detects records. `convert` delegates whenever the
  source or the target is `"record"`. The form's dispatch entries make `get_value`,
  `get_unit`, `get_dimensionality`, `change_value` and `quantity(..., form="record")` work.
  Records never import a backend at load time.
- **Diagnostics**: `RecordError` (`PUW-ERR-REC-001`) in the SMonitor catalog.
- **Third parties**: `_private/record_reference_reader.py` reads and verifies records with
  the Python standard library only. `tests/quantity_record_vectors/` holds frozen vectors,
  with SI values written by hand, and `devtools/generate_quantity_record_vectors.py`
  regenerates them.

Deferred, each to be justified by a consumer case:

- the HDF5 binding with a CF `units` attribute (needed by uibcdf/molsysmt#240);
- the tagged layout for mixed units (TaggedQuantities; #83);
- UCUM and CF spellings derived with real parsers (#85);
- Arrow and Zarr bindings;
- growing records by appended blocks;
- OpenFF (#86);
- foreign pint registries (#84);
- a live, computing form (#87).

## Why

A unit lost at a boundary produces a wrong number with no error: the Mars Climate Orbiter
case, uibcdf/molsysviewer#96 (10× under a user Å policy), and the latent H5MSM mechanisms of
uibcdf/molsysmt#240. PyUnitWizard owns units across MOLI and MolSysSuite
(uibcdf/moli#13, uibcdf/molsyssuite#46), so one implementation here prevents every
consumer from inventing a format.

## What is measured and what is assumed

Measured with the prototype (#82, `qrec/0.2`; Python 3.13, pint 0.25.3):

- JSON base64: 1.33× raw size; 100k values written in 5 ms and read in 4 ms.
- A bundle holds 50 scalars at 166 B each, against 347 B for separate records.
- The digest runs at about 0.3–0.6 GB/s.
- 20 deliberate slips were refused across records, HDF5 and bundles.
- CF strings were validated with cf-units 3.3.1.

Measured with this implementation:

- 58 tests: exact round trips (NaN, −0.0, float32, int32, n-D, compound and affine
  units); 11 slips refused; a resealed lie caught by the SI redundancy; the CODATA
  tolerance; records independent of the session policy; canonical spelling independent of
  pint's display format; the form's integration; bundles; published vectors reproduced
  byte for byte; the reference reader agreeing.
- Full suite: 626 passed.

Assumed: the 1e-6 tolerance separates definition drift (≤ ~7e-7 observed between UDUNITS
and pint) from different units. It must be re-measured if a consumer meets a larger
legitimate difference.

## What was refuted

- **Per-value `{value, unit}` for collections**: 4.3× the size, 5× the load time.
- **A container manifest without a seal**: this is the H5MSM failure mode.
- **Container-native checksums** (Fletcher32, Parquet CRC, ASDF MD5): any writer
  recomputes them.
- **A global unit-code catalogue**: codes that change meaning between versions misread old
  files.
- **A separate TaggedQuantities class**: two classes for one concept diverge, as the
  passport showed.

## Scope and exclusions

- Protection against deliberate falsification needs signatures and is out of scope.
- A writer that is consistently wrong (meant nM, wrote pM) cannot be detected by any
  format. That is covered by API contracts (ArgDigest), cross-tool canaries and
  conformance tests under a non-default session policy.

## Acceptance criteria

- MVP: `record` form, bundles, strict JSON and base64 encodings, seal, handshake, no
  defaults, `RecordError`, reference reader, vectors and user documentation. Done in this
  change.
- Closure of #82: the deferred items above are either implemented or split into their own
  issues; Sabueso (#32) and one MolSysSuite member consume the form; the 1.0 checklist
  decides between promotion and continued provisional status. The guard at closure will be
  `tests/test_quantity_record.py::test_every_change_outside_the_codec_is_refused`.

## Dependencies and risks

- **The format may change before promotion.** Consumers pin the `qrec/<version>` they
  read, and the vectors make any change visible.
- **pint is required to build or read records into quantities.** Verification alone needs
  only hashlib (see the reference reader).
- **The first record in a process builds pint's registry** (0.3–0.5 s).
