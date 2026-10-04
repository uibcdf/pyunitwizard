---
summary: Record the accepted design and bounded provisional QuantityRecord implementation.
issue: uibcdf/pyunitwizard#83
status: resolved
opened: 2026-09-24
closed: 2026-10-04
verification: measured
area: [serialization, interoperability, design]
guard: tests/test_quantity_record.py::test_published_vectors_verify_and_are_reproduced_exactly
normative: devguide/api_freeze_pre_1.0_decision.md
blocked_by: []
supersedes: []
---

# Quantity interchange design record

## What and why

Persist values with their actual unit, rather than trusting field names, ambient
session policy or a separate convention. The motivating cases were Sabueso's
quantity-bearing card fields, MolSysViewer's nm assumption under an angstrom
policy, MolSysMT's conflicting unit locations/fallbacks, case-sensitive unit
spellings, and array string round trips. Their owning issues retain the original
reproductions: Sabueso #32, MolSysViewer #96, MolSysMT #240 and PyUnitWizard #81.

This is the durable record of the maintainer's 2026-09-24 decisions in #83 and
the delivered #82 MVP. It does not reopen decisions in consumer repositories.
Future quantity serialization proposals remain with PyUnitWizard and link this
record; shared platform contracts retain MOLI #12 and MolSysSuite #46.

## Alternatives and evidence

The original prototype measured 100,000 concentrations on Python 3.13.14/Pint
0.25.3, Linux/Xeon E5-2630 v4. Per-value value/unit JSON was roughly 4.3 times
raw size and five times the load cost; it also allocates one object per value.
Unit-once metadata was compact but left units and values independently mutable.
Tagged numeric arrays with a local table were compact for mixed-unit cases;
normalized Sabueso columns were subsequently chosen to be homogeneous.

| Alternative | Outcome and reason |
| --- | --- |
| Per-value value/unit objects for collections | Retain at application presentation boundaries where useful; avoid as the main large-array codec. |
| Strings and Pint tuples | Existing supported forms, with parser/backend costs and no shared integrity contract. |
| Unit-once metadata with no seal | Refuted for verified storage: raw writers can change values or metadata independently. |
| Container checksums alone | Detect bytes, not the negotiated unit/field meaning or writes outside the codec. |
| Global unit codes | Refuted: changing one global code would reinterpret stored data. |
| Separate live or tagged quantity class | Refuted for this MVP: the form is inert; tagged is a future layout of the same record. |
| Unit passport/cache of previous checks | Refuted: persisted records are verified on read, never accepted from a remembered classification. |

The original issue retains prototype timing and memory tables; these are
identified historical measurements, not current universal guarantees. The
delivered frozen vectors, tests and consumer records provide repeatable current
correctness evidence. No new benchmark or third-party standard compliance is
inferred here.

## Accepted contract and delivered scope

- One inert `QuantityRecord` form (`record`) and a `QuantityRecordBundle` for
  related document columns/scalars. They do not compute; computing backends
  remain the existing quantity libraries.
- A descriptor stores canonical long unit name plus SI factor, offset and base
  exponents, and optional quantity kind. Readers cross-check name/SI semantics.
- Values and manifest are bound by block and top blake2b-128 digests. Canonical
  tagged little-endian manifest bytes avoid language-dependent JSON formatting.
- Writers accept quantities. Readers may declare field, unit, dimensionality
  and kind; application boundary contracts must supply their own expectations,
  rather than derive expectations from the incoming document.
- Missing manifests/units and wrong expectations fail; strict JSON rejects
  non-finite numbers, while base64 preserves them. The standard-library reference
  reader and fixed vectors document the implemented binary/digest boundary.
- The threat model is mistakes. Deliberate forgery/resealing is not detected.
  A consistently wrong writer (meant nM, labelled pM everywhere) still requires
  consumer canaries, source checks or domain plausibility checks.

The dimensionality/definition tolerance is currently 1e-6. Original evidence
includes CODATA/UDUNITS drift; a materially different real consumer definition
must be measured and reviewed, not silently accepted. SI semantics and hashes
alone do not establish quantity-kind equivalence.

## Open questions have explicit owners

Broadcast versus per-value codes is settled conceptually: tagged and homogeneous
are layouts of one form, with explicit codes, a local descriptor table and an
explicit target unit/split on reading mixed data. Serialized layout and actual
implementation require #102 and a measured consumer; qrec/0.3 is not silently
extended to implement that design.

HDF5/CF (#101), Arrow/Parquet (#103), Zarr (#104), verified appends (#105),
and translation-hub evaluation (#106) are separate proposals. Dialect parsers
remain #85, OpenFF remains #86, stated uncertainty remains #90, and live
computation remains deferred under #87. Logarithmic kinds, legacy migration,
verification cost and stated precision require explicit consumer scope before
implementation; source precision remains verbatim consumer data.

## Resolution and guard

The design record is complete as maintained guidance for the delivered MVP.
Sabueso has real bundle adoption; TopoMT publishes sealed DFND scientific inputs
with explicit reader field/unit checks. MolSysMT #240 fixes legacy unit reads,
not the codec, and unpublished PharmacophoreMT work is not counted as delivered
adoption. Provider-owned TopoMT canaries verify the actual published qrec/0.3
inputs under a different session policy, without claiming to rerun its algorithm.

`test_published_vectors_verify_and_are_reproduced_exactly` binds the selected
descriptor/encoding/seal choices to byte-identical published cases. The record
suite also refuses altered units/values and wrong field/dimension/kind reads;
#100 adds immutable in-memory snapshot storage. These assertions guard the
decisions; they do not qualify unimplemented layouts or future public releases.

Keep the QuantityRecord APIs and qrec/0.3 formats provisional in the 1.0 scope,
as recorded in the API freeze decision and release checklist. Stable promotion
and exact-release admission remain explicit later decisions.
