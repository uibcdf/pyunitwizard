# Developer guide

This directory contains operational guidance for maintaining and releasing PyUnitWizard.

## Documents

- `smonitor.md`: diagnostics and instrumentation rules.
- `roadmap.md`: staged path from pre-`1.0.0` lines to stable `1.0.0`.
- `interop_future_directions.md`: consolidated long-term interoperability ideas (conceptual, non-operational).
- `minimum_quantity_protocol_contract.md`: minimum backend-agnostic quantity contract for pre-`1.0.0` hardening.
- `frontend_transparent_mode_contract.md`: contract for transparent frontend integrations (`numpy`/`pandas`/`matplotlib`).
- `api_freeze_pre_1.0_decision.md`: explicit decision record for no planned breaking API changes before `1.0.0`.
- `serialization_contract_draft.md`: historical draft superseded by provisional QuantityRecord.
- `compatibility_matrix.md`: current required sibling floors and optional provider qualification.
- `release_0.29.0_notes.md`: published additive scope, exact source/file identity and limits.
- `completed_proposals/release_0.29.0.md`: executed source/installed/public publication route.
- `release_0.28.1_notes.md` and `completed_proposals/release_0.28.1.md`: immutable prior patch history.
- `completed_proposals/backend_declaration_plans.md`: completed #111 optimization and measurement limits.
- `completed_proposals/quantity_record_hub.md`: completed #106 evaluation,
  live-translation decision and before/after measurements.
- `release_0.21.x_rc_checklist.md`: completed historical RC checklist for consolidation before `1.0.0`.
- `release_0.21.x_notes_draft.md`: historical RC release notes and migration scope.
- `docs_api_alignment_0.21.x.md`: historical RC user/API alignment evidence.
- `stability_monitoring_0.21.x.md`: historical RC matrix and release-gate incident ledger.
- `ecosystem_validation_0.21.x.md`: historical RC integration and sibling evidence.
- `rc_close_readiness_0.21.x.md`: historical RC go/no-go closure evidence.
- `release_1.0.0_checklist.md`: release gates and go/no-go checklist.
- `molsyssuite_collective_alignment.md`: PyUnitWizard alignment map against `../molsyssuite/devguide/collective_v1_checklist.md`.
- `collective_evidence_pack.md`: historical March 2026 cross-repo RC evidence pack.
- `dependency_declaration_placement.md`: why backend dependencies are declared
  in `_depdigest.py` and enforced in `load_library()`, not on `convert()`.
- `performance_baseline_0.24.x.json`: baseline snapshot after the post-RC
  performance work, in both telemetry modes.
- `reporting_protocol.md`: issue-backed lifecycle for durable bugs and proposals.
- `resource_lifecycle_review.md`: owner dispositions for temporary resources,
  development tools, caller evidence and retained workspace outputs (#116).
- `pending_bugs/`: active defect reports.
- `pending_proposals/`: active, deferred, or implementation-pending technical proposals.
- `archive/`: generated index of resolved and historical reports.
- `completed_proposals/`: implemented proposals retained as design and benchmark evidence.
- `declined_proposals/`: proposals considered and not adopted, retained as design
  evidence with the reasoning and any condition for revisiting them.

## Current baseline

- Latest public release: [`0.29.0`](release_0.29.0_notes.md), published on
  2026-10-23 through GitHub and the public `uibcdf` Conda channel.
- Current pre-`1.0.0` line: `0.29.x`. Published provisional capabilities are
  separate from stable-contract admission and member source adoption.
- Completed release-candidate line: `0.21.x`.
- Latest maintenance tag in RC line: `0.21.1`.
- RC consolidation closure checkpoint tag: `0.21.0`.
- `0.19.3` remains the historical checkpoint tag from the earlier pre-RC phase.
- Current head relative to tag: run `git describe --tags --always` (post-tag hardening in `main`).
- Latest stabilized tags before RC: `0.18.2`, `0.18.3`, `0.18.4`.
- Stable target: `1.0.0`.
- Publicly supported Python versions: `3.11`–`3.14`; routine CI uses `3.14`.
  The qualified baseline, storage/dialect and prepared-attribution installed profiles
  cover Linux and macOS arm64 on all four minors. OpenFF 0.4.0 covers
  Python `3.12`–`3.14` with Pint `>=0.24,<0.26`.
- Supported platforms: Linux and macOS arm64. Windows support is deferred until a
  concrete ecosystem requirement appears.
- Historical local test snapshot (2026-03-04): `391 passed` (`pytest --import-mode=importlib -q --cov=pyunitwizard --cov-config=.coveragerc --cov-report=term-missing`).
- Historical local coverage snapshot (2026-03-04): `94%` total.
- Shared collective E2E module established: `tests/e2e/test_collective_error_path.py`.
- Supported runtime backends:
  `pint` (hard), `openmm.unit` (soft), `unyt` (soft), `astropy.units` (soft),
  `physipy` (soft), `quantities` (soft), `openff.units` (soft, bounded above),
  plus `string` and the provisional inert `record` form (QuantityRecord).

## Resume after 0.29.0

[Publication #128](completed_proposals/release_0.29.0.md) is complete. The
canonical tag and stable GitHub Release identify original source
`cfe067bcc4545c60aaca4c6950f6d84075ee6c36`. The exact Conda file, original
producer, separate infrastructure qualifier, all 29 required source jobs,
30 installed cells, public main/index/install observations and served docs
are retained in `evidence/release_0.29.0_2026-10-23.json` and the linked
source/installed closure receipts. Previous release receipts retain their own
identities. This release replaces the uncreated 0.28.2 plan.

The bounded [#85 inventory](completed_proposals/interop_unit_dialects.md) is
complete: OpenFF and physical CF/HDF5 plus actual-provider UCUM #125, native
ASDF #126 and offline QUDT/UO annotation #127. Its maintained contract is
`docs/content/user/unit-dialects.md`. Future calendar coordinates, full
clinical/astronomy schemas and unmeasured vocabulary expansion need independently
justified consumers and separate contracts.

The release also delivers the qualified record extensions:
[#104 Zarr](completed_proposals/quantity_record_zarr.md),
[#102 tagged layout](completed_proposals/quantity_record_tagged.md),
[#105 immutable append](completed_proposals/quantity_record_append.md), and
[#103 Arrow/Parquet](completed_proposals/quantity_record_arrow.md).
Their maintained contract is `docs/content/user/record-extensions.md`; original
measurements and per-cell wheel identities remain separate from this Conda file.
Conversion fixes #120/#122/#123/#124 and benchmark provenance #121 are included.
The #106 decision still retains direct/live Pint translation rather than sealed
records as a universal computation intermediate.

The optional Ackredit floor remains 0.9.0; the separate prepared profile qualifies
public 0.10.1. All required storage/dialect and prepared modules executed without
skips in their respective eight-cell installed profiles. Whole-run JUnit evidence
retains intentional strict-JSON/NaN and unavailable prepared-API classifications
elsewhere. Qualification fixes #129/#130/#131 and prior coverage incident #107
are resolved; their archives retain the actual failures and recovery evidence.
The #116–#119 tooling/resource/documentation review remains complete.

[MolSysSuite #132](https://github.com/uibcdf/molsyssuite/issues/132) owns this
version's availability notice and guide/pin handoff. The canonical guide is
`standards/PYUNITWIZARD_GUIDE.md`; MolSysSuite owns synchronizing client copies.
Advance consumer-impact/adoption work remains separately linked from suite
#46 and #127. Provider publication does not establish client source adoption.

Remaining feature decisions are #44 (forallpeople), #52 (Pydantic) and
[#87](https://github.com/uibcdf/pyunitwizard/issues/87) (a possible live native
form). Revisit them only with real consumer demand and measured need; #87 has
no queued implementation document. QuantityRecord, bundles, measurement,
attribution and all new record/storage/dialect surfaces remain **provisional**.
[The 1.0 checklist](release_1.0.0_checklist.md) still requires fresh candidate
evidence, explicit admission/scope decisions and release-owner approval.

## 0.19.x checkpoint summary (historical baseline)

Completed in `0.19.x`:
- Public-contract hardening and cross-library smoke coverage are in place.
- Shared collective E2E scenario is implemented in all four library repos.
- Collective test execution policy is now explicit: tests run in library repos
  with CI, while `molsyssuite` remains coordination-only.
- Runtime integration support is implemented and tested for
  `pint`, `openmm.unit`, `unyt`, `astropy.units`, `physipy`, and `quantities`.
- Transparent integrations are now implemented and validated for:
  - NumPy (`setup_numpy` / `numpy_context`),
  - Pandas (`setup_pandas` / `pandas_context` + metadata-safe helpers),
  - Matplotlib (`setup_matplotlib` / `plotting_context`).
- Cross-backend frontend matrix coverage exists for mixed backend pairs across
  NumPy/Pandas/Matplotlib integration surfaces.

Current RC-close status before `1.0.0` go/no-go:
- CI matrix continuity evidence is recorded (see `stability_monitoring_0.21.x.md`);
- release-gates evidence is recorded, including blocker/fix closure;
- ecosystem collective validation evidence is recorded
  (see `ecosystem_validation_0.21.x.md`);
- release-owner explicit RC-close approval is recorded.
- post-RC maintenance hardening in `0.21.1` includes:
  - recursion bugfix for `quantities` unit conversion path,
  - CI/Codecov alignment for optional backend coverage (`physipy`, `quantities`).

Route update:
- `0.20.x` is reserved for interoperability expansion (NumPy/Matplotlib/Pandas).
- `0.21.x` is the completed RC consolidation window.
- `0.22.x` and `0.23.x` contain post-RC performance and API hardening before `1.0.0`.

## Coordination scope

PyUnitWizard must stay aligned with:

- `argdigest`: argument normalization and API contract integration.
- `depdigest`: optional dependency governance and runtime loading.
- `smonitor`: diagnostics catalog, severity semantics, and traceability.

Collective testing policy:
- cross-library E2E tests belong to library repos with CI (including
  duplicated scenarios when needed for coverage and ownership clarity).
- `molsyssuite` is used for coordination artifacts/checklists, not as a test
  execution repository.

## 🥇 Performance Optimization (March 2026)

### Numpy Fast Path
The `get_value` API now implements a high-performance bypass for raw numpy arrays. If the input is already a numpy array and no conversion or standardization is requested, it is returned immediately. This reduces the overhead of the `arg_digest` decorator in tight loops.

### ⚡ Exception-Free Introspection Flow (May 2026)
To avoid severe control-flow exception overhead in type checking:
- **Graceful Form Probing**: `get_form()` has been extended to support `raise_exception=False`. When a form is not recognized, it returns `None` instead of raising a costly `NotImplementedFormError`.
- **Introspection Bypass**: `is_quantity()` queries `get_form(..., raise_exception=False)` to check form validity. If it returns `None`, it gracefully returns `False` immediately. This completely avoids raising exceptions for common Python types, bypassing exception catalog overhead, stack-frame traversal, and telemetry signaling.

### 🔁 Redundant Work Removal (August 2026)

A round of work on PyUnitWizard's *own* cost, after
`completed_proposals/telemetry_cost_remeasured_and_signal_boundary.md` declined the
`@signal` split and established that the remaining time was ours, not the
instrumentation's. Nothing here removes validation or changes a public signature.

Four findings, all of the same shape — paying repeatedly for something already known:

- **Form re-resolution.** `get_dimensionality()` read its unit through the public
  `get_unit()`, re-entering `convert()` and resolving the same form twice more;
  `standardize()` resolved a form its helper then resolved again.
- **The candidate scan.** `standardize()`'s canonical fast path called `has_unit()`
  once per configured standard, re-extracting the same source unit each time, and
  rebuilt a dimensionality key per standard on every call. The deduplicated list is
  now derived once as `kernel.canonical_standards`.
- **The cache key cost more than the lookup.** `get_dimensionality()` keyed on
  `(form, str(unit))`; formatting a pint unit costs 5.95 us against 0.16 us to hash
  it, so most of a cache *hit* was spent building the key.
- **Expensive work before the cheap check.** `get_standard_units()` built an array
  and ran `np.isclose` over seven values *before* consulting its cache, discarding
  all of it on a hit.

| | before | after |
|---|---:|---:|
| `standardize_meter_quantity` | 492.8 us | **64.9 us** (-87%) |
| `get_dimensionality_quantity` | 145.8 us | **6.9 us** (-95%) |
| `get_dimensionality_unit` | 12.5 us | **5.8 us** (-54%) |

Baseline snapshot in `performance_baseline_0.24.x.json`, recorded in both telemetry
modes.

### 🚀 Startup Cost (August 2026)

A second round, on what a consumer pays before doing any unit work at all. It
was driven by a MolSysSuite question -- whether a library can declare its unit
policy when it is imported rather than on first use -- and the answer turned out
to depend entirely on this.

- **Naming a form loaded its backend.** `set_default_form('pint')` cost 477 ms
  because `digest_form()` both validated the name and imported pint. Recording a
  preference is not using it; the first real operation loads the backend anyway.
  **477 ms → 0 ms.**
- **Reaching `puw.configure` imported numpy and the whole API package**, to get
  two functions used by two of its own functions. **63 ms → 1.2 ms.**
- **pint can cache its parsed definitions on disk.** Opt-in through
  `set_pint_registry_cache()` or `PYUNITWIZARD_PINT_CACHE`, off by default
  because writing to a user's filesystem is not a side effect importing a units
  library should cause. Registry construction **180 ms → 17 ms**.
- **`importlib.metadata` was imported to read our own version**, on a path that
  already had the answer in `_version.py`. Currently masked because SMonitor
  imports it first; filed as a proposal there, where it is 33 ms of a 72 ms
  import that every dependent library inherits.

Declaring a full policy cold went from 542 ms to about 310 ms warm, of which
about 256 ms is `import pint` and irreducible. What is *not* worth doing is
recorded too: deferring the resolution of standard units would take that to
near zero, and was rejected because it defers validation with it. The remaining
suite-wide configuration work is tracked by `uibcdf/molsyssuite#18`.
