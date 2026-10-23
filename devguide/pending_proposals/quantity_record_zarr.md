---
summary: Evaluate an optional Zarr binding for QuantityRecord.
issue: uibcdf/pyunitwizard#104
status: active
opened: 2026-10-04
closed:
verification: measured
area: [serialization, interoperability]
guard: tests/storage/test_zarr.py
normative:
blocked_by: []
supersedes: []
---

# Evaluate an optional Zarr binding for QuantityRecord

What — Track the deferred chunked storage binding from #82 independently.

How — Start from an identified consumer array. Design one authoritative in-object descriptor and verified chunks, using documented reusable operations. A units attribute must agree with the sealed descriptor; chunk checksums alone do not establish unit integrity.

Why — Chunked storage may serve large datasets, but consumer demand and actual costs remain unmeasured.

Acceptance — Record a real workload and supported optional installation; preserve dtype/shape/unit/kind across round trips; refuse missing or conflicting manifests, raw chunk writes, metadata changes and truncation; measure verification costs. Keep append API, format version changes and stable promotion separately owned.

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

## #104 interpretation

The real one-frame input has no partial-read advantage: full 6.708 ms,
partial 6.632 ms. The 1,024-times tiled stress case reads/verifies
one row in 14.193 ms versus 89.405 ms for the full snapshot.
This demonstrates a bounded partial-access benefit, not an observed trajectory
or constant-cost metadata work. Tampering, missing zero chunks, physical chunk
shape, partial-read data access and empty-selection metadata checks have guards.
Zarr supports homogeneous snapshots only; tagged/file append/sharding/cloud
qualification is intentionally not implied.

## Exact-artifact route coverage

The publication review also found the staged Conda storage profile still
selected only CF/HDF5. Its setup now includes Zarr 3.1.6 and PyArrow 25.0.0;
all profiles execute the new core codec guards, and storage executes all
bindings plus both consumer fixtures. The actual staged XML check rejects
missing/skipped required module guards. A regression first fails against the
old profile; 28 workflow/release-route/dependency checks pass after correction.
The actual XML-check code extracted from the workflow accepts a real 52-test
source JUnit run. This verifies the checker, not a staged Conda file. Future
publication must still execute the updated route against the exact archive.

The pinned shared provider verifies all 22 declared/installed dependency routes;
workflow identities retain reviewed exact bytes. Runtime codec/binding files
and measurement inputs are unchanged by this publication-route correction.

## Installed probe failure propagation

Review of the optional source-installed step found that its custom Bash shell
could continue after a failed dependency/import probe. A regression executes
the actual workflow commands with an owned shim: pip check exits 42, pytest
would succeed, and the old step incorrectly exits zero. Adding explicit
`set -euo pipefail` makes it stop at 42 before pytest. The updated workflow's
exact bytes are reviewed in the dependency inventory; 14 workflow/dependency
checks and all 22 pinned dependency routes pass.

The original optional run retains producer source 7605732 and its original
workflow bytes. Native job logs independently verify actual successful pip
checks, installed origins, provider versions and non-skipped installed test
results; a shell correction does not by itself invalidate those executed facts.
New runtime codec/binding files and numerical measurement inputs are unchanged.
No skipped, failed or unexecuted gate is being converted to success.
