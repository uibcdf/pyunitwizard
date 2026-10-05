---
summary: QuantityRecord HDF5 binding with explicit units and integrity checks.
issue: uibcdf/pyunitwizard#101
status: resolved
opened: 2026-10-04
closed: 2026-10-05
verification: measured
area: [serialization, interoperability]
guard: tests/storage/test_hdf5.py::test_edits_missing_metadata_and_raw_appends_are_refused
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

## Reader-temperature hardening — 2026-10-05

The first optional matrix passes at 381ca5a, but review identifies a remaining
reader handshake ambiguity: both Kelvin points and differences otherwise return
the same computing unit. Add a failing expectation test before strengthening
`read`: require matching explicit `units_metadata` for temperature and validate
any requested unit through the public CF import operation. A declared difference
cannot target an absolute Celsius unit. Keep the qrec schema unchanged and
require callers to retain this binding context for subsequent conversion.
Qualification must retain the initial producer identity and execute the adjusted
reader's installed/optional gates on its own source rather than relabel old results.

## Resolution and qualification — 2026-10-05

Implemented at initial source `381ca5a43801fff488bed9cd0fba13f8de3a3c7e`,
then strengthened the temperature reader handshake at final source
`d4c6089be2f4b8d4c975f31238209ce7348ee4c0`. The final optional eight-cell
Linux/macOS Python 3.11–3.14 matrix 37277539184 passes 822 tests/14 skips
per cell with actual cf-units 3.3.1/h5py 3.16.0. All eight normally installed
consumers pass 69 copied guards outside checkout and pip check; site-packages
origins and versions are printed in native logs. Local final full suite passes
824/12; the baseline without CF passes 764/12 with the integration modules
unexecuted at collection and separate absence guards active. Ruff, docs and
reporting guards pass.

The final normal wheel `pyunitwizard-0.27.0+75.gd4c6089-py3-none-any.whl`
has SHA-256 `0d77f6a499e62d43c9d475274e58d2a5971d2c37f2b4c1ca555b7e2709835746`.
Installed in an actual Conda-solved environment, it passes 69 outside-checkout
guards and pip check; all 85 shipped package files match the original wheel.
The earlier wheel and matrix keep their original identity, without being
relabelled as the strengthened reader.

Initial baseline eight-cell matrix 37276227352 passes 762/14 per cell;
release gates 37276231080 pass four full suites with those counts, four 16-case
smokes, packaging and docs. The final change affects only the optional reader,
its tests and guidance: baseline scientific code, core tests, dependency inputs,
metadata and workflows remain unchanged. Final-source routine CI 37277485846
executes 762/14 and style checks but still fails Codecov ingestion; policy
37277486550 passes. Missing upload evidence stays owned by #107, to recover
through successful exact-head coverage/test-result execution after service recovery.

Receipt: `devguide/evidence/cf_hdf5_interop_2026-10-05.json`. Original qrec/0.3
bytes and seals remain unchanged. No aggregate CI green, new public release,
calendar/full-CF conformance, streaming/append or consumer adoption is claimed.

The HDF5 edit guard refuses raw changes to values, CF labels, binding/record
metadata, dtype and shape, missing declarations, raw appends and competing
unit locations. The temperature guard requires matching writer/reader semantics;
unknown expectations cannot silently treat a Kelvin difference as a point.
Creation refuses overwrites and removes staged data on a caught write error.

The immutable MolSysMT consumer file at published source
`77abb38d407096c87ac4b26628ab8523e6dcc10c` has SHA-256
`c8618b439694df3f4c41ec3451ac5a5981ea89446e50946cf5b8846918f29874`.
Its coordinates are float32, shape (1,22,3), 264 raw bytes with explicit root
nanometer declaration. The frozen boundary fixture preserves those values and
checks a round trip under an angstrom session policy. No MolSysMT source is
modified or adoption inferred.

For this small array only, warm median read time over 30 runs is 2.025 ms
verified versus 0.174 ms raw; in-memory write is 1.540 ms versus 0.636 ms.
Both HDF5 files occupy 10624 bytes at this allocation size, which does not
establish zero metadata overhead for other files. Whole-array materialization,
verification and envelope allocation are explicit costs. Larger workloads,
streaming verification and verified appends remain outside this qualification.
