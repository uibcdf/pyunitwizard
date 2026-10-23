---
summary: Specify and evaluate a tagged layout within QuantityRecord.
issue: uibcdf/pyunitwizard#102
status: active
opened: 2026-10-04
closed:
verification: measured
area: [serialization, interoperability]
guard: tests/test_record_tagged.py
normative:
blocked_by: []
supersedes: []
---

# Specify and evaluate a tagged layout within QuantityRecord

What — Track the deferred heterogeneous layout from #82/#83 as its own proposal.

How — Retain one QuantityRecord class with a local unit-descriptor table and explicit per-value or broadcast codes. Define the serialized layout before implementation; compatibility requires an explicit version decision, not reinterpretation of existing qrec/0.3 records.

Why — The maintainer decided that homogeneous and tagged representations are layouts of one inert form. Normalized Sabueso columns are homogeneous, so mixed-unit implementation requires a measured consumer case.

Acceptance — Identify an actual heterogeneous workload and measure alternatives; seal descriptors, codes, dtype/shape and values together; require an explicit target unit or split when reading to a computing backend; reject dimension/kind conflicts and altered codes. No implicit mixed-unit coercion or live arithmetic.

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

## #102 interpretation

The existing heterogeneous query contains 343 observations and five explicit
unit/kind descriptors (Ki, IC50, Inhibition, Kd, ED50), including nM and percent.
Serialized tagged JSON is 3984 bytes versus 116990 bytes for
individual records and 53868 for the per-observation bundle baseline.
These are named baselines, not proof that no grouped alternative could be smaller.
A single normalized computing array cannot preserve both concentration and
percentage semantics. The new layout keeps original magnitudes/codes; incompatible
dimensions or kinds require splitting, while compatible records require an
explicit target unit. Empty-array/code shape and lossy mixed-dtype promotion
have regression-first guards. Old qrec/0.3 vectors remain unchanged.
