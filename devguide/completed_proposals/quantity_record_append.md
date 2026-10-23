---
summary: Define verified append operations for block-based QuantityRecords.
issue: uibcdf/pyunitwizard#105
status: resolved
opened: 2026-10-04
closed: 2026-10-23
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

## Resolution and qualification

Implemented under the maintained provisional contract and durable module guard
above. The original source 7605732461ccf74547e6fb7645cbe38e0c2bc778 passes
CI 39993982540, policy 39993983037 and all eight source/installed storage cells
in run 39994006616 (attempt 1). Each cell actually passes pip check, imports
the selected public provider versions from the environment, and executes
**125 installed tests without skips** outside checkout. Native jobs/steps,
original installed origins, summaries and producer-wheel digests are retained
in `devguide/evidence/record_extensions_initial_installed_2026-10-23.json`.
This independent log evidence preserves real original results after the
fail-fast shell correction; no failed/unexecuted probe is declared successful.

Final local code also rejects negative/inferred tagged wire shapes even when
a seal is recomputed. Its regression first fails and then passes. The hardened
reader snapshot has separate fresh measurements in
`devguide/evidence/record_extensions_final_2026-10-23.json`; preserve the
original report as history. Final local suite: **975 passed, one expected
strict-JSON/NaN skip and the existing main-module deprecation warning**,
Python 3.14.7, 46.93 seconds. Ruff lint/format and report/diff checks pass.
The owned Sphinx build is warning-free.

The final source checkpoint executes CI/policy and the complete optional
matrix again, including explicit fail-fast installed probes and the hardened
wire-shape guard. Exact final producer/attempt receipts are exported in the
owning GitHub issue before closure; no source/installed/public-file identity
is silently substituted. The staged Conda route remains unexecuted until
there is a separately owned exact candidate archive to qualify. Source/wheel
success does not publish 0.28.2 or promote these provisional contracts.

The concurrent central guide delivery 3763b047058f3de17eda70e8622d47cf85c7e9ac
was merged without rewriting either branch. Its new MolSysSuite #129 notice
policy is retained. No release/package event exists from these feature commits;
issue #46 retains the advance provider/adoption handoff, while future actual
publication requires its own version-specific central notice and availability
update as requested by the maintainer. No client copy or dependency pin was
changed in a consumer repository.
