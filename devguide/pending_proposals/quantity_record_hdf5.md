---
summary: QuantityRecord HDF5 binding with explicit units and integrity checks.
issue: uibcdf/pyunitwizard#101
status: active
opened: 2026-10-04
closed:
verification: inspected
area: [serialization, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# QuantityRecord HDF5 binding with explicit units and integrity checks

What — Move the deferred HDF5/CF binding out of the implemented QuantityRecord MVP (#82).

How — Define an optional owner-local writer/reader over HDF5 datasets, with values, one authoritative unit descriptor, block/top digests and explicit reader expectations. A CF units attribute must agree with the descriptor and be covered by verification; derive supported CF spellings through the parser work in #85, never a guessed table.

Why — MolSysMT H5MSM exposed real unit-boundary failures under uibcdf/molsysmt#240. That issue now fixes legacy unit authority/fallbacks and explicitly leaves future codec adoption separate. A tested reusable provider operation should precede member integration.

Acceptance — Round trips for scalars/arrays/dtypes and affine units; refuse raw h5py value/unit edits, missing/conflicting manifests and units; keep explicit warned legacy handling consumer-owned. Record optional installation and performance on an identified consumer file. No MolSysMT source change or automatic stable format promotion is authorized by this issue.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.

## Implementation scope — 2026-10-05

The CF physical-unit slice is independently owned by #108 under #85. Use
its provider-verified spelling operation for an in-object `units` attribute;
include temperature semantics in the binding seal. HDF5 helpers belong in
`pyunitwizard.storage.hdf5`, with one group holding numeric `values` and a
sealed qrec envelope. Preserve qrec/0.3 bytes and digests; a distinct provisional
binding descriptor covers CF presentation metadata and references the record
seal. Readers reconstruct through QuantityRecord.from_dict and refuse missing
or conflicting metadata, edited values, changed dtype/shape and raw appends.
Existing H5MSM root/group/dataset fallback behavior stays MolSysMT-owned.

Creation must refuse overwrites and leave no published group on validation
failure. This is a snapshot reader/writer, not append support (#105), a
streaming verifier, a transaction across files or a MolSysMT codec migration.
Measure an identified published H5MSM array and the full-read seal cost.
