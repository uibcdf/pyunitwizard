---
summary: Specify and evaluate a tagged layout within QuantityRecord.
issue: uibcdf/pyunitwizard#102
status: resolved
opened: 2026-10-04
closed: 2026-10-23
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


## Public delivery addendum — 2026-10-23

The separately qualified public checkpoint is now **0.29.0**, replacing the
uncreated 0.28.2 plan. Original source and benchmark/wheel identities above
remain historical evidence. Exact-file Conda qualification and public outcomes
are retained in `devguide/completed_proposals/release_0.29.0.md` and
`devguide/evidence/release_0.29.0_2026-10-23.json`. MolSysSuite #132 owns this
version's availability and canonical-guide handoff; suite #46 retains the
separate consumer/adoption route. No client migration or stable API admission
is implied by publication.
