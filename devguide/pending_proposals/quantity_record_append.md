---
summary: Define verified append operations for block-based QuantityRecords.
issue: uibcdf/pyunitwizard#105
status: active
opened: 2026-10-04
closed:
verification: measured
area: [serialization, interoperability]
guard: tests/test_record_append.py
normative:
blocked_by: []
supersedes: []
---

# Define verified append operations for block-based QuantityRecords

What — Track the deferred growing-record scope from #82 independently.

How — Define a reusable codec operation that converts incoming quantities to the negotiated unit, writes/seals new blocks and binds their order/shape to the top manifest. Retain immutable snapshots and reader expectations; storage binding behavior is separately owned.

Why — The format describes blocks but the current writer produces a complete snapshot. Growing trajectories must not permit raw appends to bypass the seal.

Acceptance — Obtain a measured growing-data consumer; specify snapshot/atomic-failure behavior, exact dtype/unit conversion and shape constraints; refuse reordered, removed, truncated or raw-appended blocks; measure total and incremental costs. Do not mutate already published qrec/0.3 bytes or promise an HDF5/Zarr API from this issue.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.

## Maintainer-selected implementation — 2026-10-23

The maintainer selected #104, #102, #105 and #103 in that order and chose
both molecular arrays and heterogeneous observations from existing repositories.
The bounded contract is `docs/content/user/record-extensions.md`; no existing
consumer file/schema is migrated. Retained H5MSM coordinates and Sabueso's
343 ChEMBL observations supply actual input provenance. Repeated coordinate
frames in stress measurements are synthetic, not additional MD data.

The reusable owner operations are on QuantityRecord and the optional storage
modules; core forms and backend probe order are unchanged. Generic typed-array
restoration/metadata validation and metadata digests live in the codec, rather
than duplicated codecs in bindings. Zarr and Arrow use lazy DepDigest guards.
Domain failures retain RecordError/SMonitor diagnostics and original causes.
No new scientific method or attribution-session semantics are introduced; no
provider is imported or credited at startup. Optional profile versions are
Zarr 3.1.6 and PyArrow 25.0.0, published on PyPI/conda-forge. The development
profile declares them; baseline runtime/test requirements stay unchanged.

Tests were added before implementation. Source tests, real-boundary guards and
`devtools/benchmark_record_extensions.py` retain parity and raw timing samples.
Required full-suite, documentation and native optional installed matrix evidence
will be recorded at closeout. The public artifact and release remain separately
qualified; no new version is announced from source-only evidence.

## Local validation and retained measurements

Complete local Python 3.14.7 suite: **972 passed, one expected strict-JSON/NaN
skip and the existing main-module deprecation warning**, 51.46 seconds. Zarr
3.1.6/PyArrow 25.0.0 are real providers. Zarr and its transitive packages plus
physipy/quantities are task-local overlays; the shared environment is unchanged.
The sandbox blocks even a provider-only asynchronous Zarr group creation; the
owned probes were terminated and the same operations pass outside that sandbox.
This is an execution-environment restriction, not a hidden backend fallback.

Ruff lint/format passes (225 files). An owned-copy Sphinx build with
`-W --keep-going` completes without warnings. The updated storage workflow
retains the full optional source suite and copied installed tests outside
checkout on Linux/macOS arm64 and Python 3.11–3.14; its exact bytes are reviewed
in `devtools/dependency_routes.toml`. Native receipts will identify the tested
source/attempt rather than imply public-artifact qualification.

Raw operation samples, byte counts, versions, input provenance and source hashes:
`devguide/evidence/record_extensions_2026-10-23.json`. The reused measurement
tool has an executed parity/input-preservation guard. Three serial samples per
read/codec operation are retained; one complete initial write is reported,
including its initialization cost. Tiled coordinates are explicitly synthetic.
Tagged construction is compared with record/bundle construction without
including wire encoding in only one timed path. Wire sizes are separate.

Pre-rollout notice: https://github.com/uibcdf/molsyssuite/issues/46#issuecomment-6370463613 .
Actual consumer adoption and stable-format promotion remain centrally/locally
owned separately. After the next package and GitHub Release are published and
verified, the maintainer requests a separate MolSysSuite version-availability
issue; the pre-rollout notice does not satisfy that future handoff.

## #105 interpretation

For the tiled stress snapshot, adding one compatible coordinate frame takes
0.634 ms versus 1.83 ms for concatenate-and-reseal.
This reuses existing block hashes but still copies the full immutable array;
no O(new values)-only memory or file-streaming claim is made. The real frame
slice supplies the coordinate/units contract; repeated frames are synthetic.
Tests cover explicit angstrom-to-nanometer conversion, exact dtype/trailing
shape, source field/kind, integer precision/range, finite conversion overflow,
affine values, empty initial arrays, immutable failure and raw append refusal.
Scalar/tagged/file append remain outside this operation's contract.
