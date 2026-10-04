---
summary: QuantityRecord — an inert interchange form that never loses or misreads a unit (provisional MVP implemented).
issue: uibcdf/pyunitwizard#82
status: resolved
opened: 2026-09-24
closed: 2026-10-04
verification: measured
area: [serialization, interoperability, forms]
guard: tests/test_quantity_record.py::test_every_change_outside_the_codec_is_refused
normative: devguide/api_freeze_pre_1.0_decision.md
blocked_by: []
supersedes: []
---

# QuantityRecord: PyUnitWizard's inert interchange form

## MVP scope resolution — 2026-10-04

The delivered inert QuantityRecord/Bundle MVP is complete. Keep the API,
`qrec/0.3` and `qrec-bundle/0.3` provisional in the 1.0 scope; this explicit
decision is recorded in `api_freeze_pre_1.0_decision.md` and the release
checklist. Closing this implementation issue neither promotes the format nor
qualifies a new public package. Final release notes and exact-candidate gates
remain the release owner's responsibility.

Every deferred item now has an independent owning issue: HDF5/CF binding #101,
tagged layout #102, Arrow/Parquet #103, Zarr #104, verified appends #105,
translation-hub evaluation #106, dialect parsing #85, OpenFF #86 and deferred
live computation #87. Foreign Pint registry recognition was resolved in #84.
None of these features is inferred from the implemented homogeneous form.

Two real published consumers are identified:

- Sabueso #32: source `4b98b84` records negotiated quantity columns, bundle
  verification and scalar/column quantity access; its owning resolution names
  JSON/SQLite canaries and tests. That is owner-reported receiving evidence,
  not a scientific suite rerun here.
- TopoMT: published source `bfbd28f8c3d25a438c7b3d1e526097dd56f63d3c`
  reads sealed coordinate, atom-radius and epsilon records with explicit field
  and angstrom-unit expectations in `tests/test_dfnd_closed_shell_reference.py`.
  Its published DFND showcase retains those actual scientific input records.
  Their original file digest is
  `ef19995751b2df58c8b1556011f74fa4774e924b9cd499138b8741988b650157`.
  Three local provider-owned canaries read these exact unchanged records under
  a metre session policy, explicitly convert angstroms to nanometres and refuse
  wrong field names. This checks the codec boundary; no TopoMT algorithm,
  latest whole-suite success or public consumer release is claimed.

Correction to the earlier promotion-gate wording below: MolSysMT #240 resolved
legacy unit authority and missing/conflicting declarations in `396e6979f`, and
explicitly leaves the integrity codec for future work. It is motivating
consumer evidence, not QuantityRecord adoption. PharmacophoreMT has local
unpublished uses in a dirty working tree; they are not counted as delivered
adoption and were neither edited nor executed here. TopoMT supplies the real
published MolSysSuite receiving example.

The guard `test_every_change_outside_the_codec_is_refused` tests raw append,
value/unit/SI changes, removed manifests/digests and reordering/truncation.
Frozen vectors protect the current wire format, and the new TopoMT canaries
protect cross-component units and reader expectations. Integrity defect #100
additionally refuses public NumPy write-flag reactivation through immutable
backing storage. Runtime qualification and archive-source checkpoints are
retained in their owning issue/receipt; source changes do not invent a package
release or promote the optional citation pilots.

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
two-real-consumer criterion is now met by Sabueso's bundle adoption and TopoMT's
published sealed DFND input pipeline. MolSysMT #240 motivates a future HDF5
binding and does not implement the codec, as corrected above.

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

- the HDF5 binding with a CF `units` attribute (#101; motivation in uibcdf/molsysmt#240);
- the tagged layout for mixed units (#102; design in #83);
- UCUM and CF spellings derived with real parsers (#85);
- Arrow/Parquet (#103) and Zarr (#104) bindings;
- growing records by appended blocks (#105);
- translation-hub evaluation (#106);
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
