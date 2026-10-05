---
summary: Reuse immutable backend declarations after validating their current values.
issue: uibcdf/pyunitwizard#111
status: active
opened: 2026-10-05
closed:
verification: reproduced
area: [attribution, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Backend declaration plans

## What

Issue #111 profiles repeated `backend_references.records` detachment before the
prepared-credit cache lookup. The maintainer authorized this producer-owned
optimization after publishing 0.28.0. Ackredit's independent writer optimization
is owned by uibcdf/ackredit#97; this work changes no provider implementation.

## How

Keep reusable declaration planning in the existing private
`backend_references` owner. A bounded per-backend immutable snapshot is reused
only while current software version and declaration values compare equal.
Nested in-place bibliographic changes must invalidate the plan. Detached mutable
records remain available for normal public provider registration. The prepared
path detaches only when it builds or refreshes a credit plan; it still invokes
the provider credit on every successful operation and independent capture.
The released portable-provider fallback retains its public operations.

Add failing reuse, invalidation, immutability and real-provider guards first.
Check software-only/article-only combinations, original versions, the unyt
description article, enclosing pipeline, repeated independent captures,
provider metadata conflict, scientific parity, genuine provider absence and
fresh saved readers blocked from backend imports and network access. Preserve
provider diagnostics and never skip per-credit conflict checks.

Use paired normally installed baseline/candidate packages with identical
scientific dependencies and the existing benchmark tool. Alternate independent
process order, retain all seven warmed samples, and keep activation/import costs
outside the claimed scope. Profile separately to locate removed allocation,
without interpreting profiler timings as benchmark speedup. Run the portable
0.9.0 integration separately from the provisional prepared-provider route.

## Why and limits

The producer owns its offline metadata and invalidation rule. An immutable plan
must not become identity caching of borrowed mutable inputs or provider registry
access. Cache size is bounded by the pilot backends and does not grow with
versions. Existing public APIs, provider minimum and attribution opt-in remain
unchanged. Ordinary conversions must retain their numerical behavior.

Local receiving evidence does not publish a new package, retag 0.28.0, stabilize
provisional provider APIs or claim a new hosted installed matrix. The default
shell points to Python 3.13 with an old editable provider; use the existing
isolated Python 3.14 environments for relevant source and installed checks.
Their `pip check` passes. Disk pressure precludes another full Conda environment;
small task-owned wheel/venv prefixes may reuse the same scientific dependencies.

## Acceptance

- Unchanged prepared conversions allocate no new detached backend declarations.
- Nested source edits/version changes invalidate the plan; stale provider records
  still cause a catalog diagnostic while completed numerical results survive.
- Repeated captures and saved readers retain original software/article metadata.
- Paired raw installed measurements and actual dependency/source identities are
  retained without claiming a universal percentage improvement.
- Applicable local/full-suite/style/docs/reporting checks and final pushed-head
  CI are inspected; the owning issue and archived record agree.

## Implementation and measured checkpoint — 2026-10-05

`backend_references.plan` retains one immutable current snapshot per backend.
Mapping proxies and immutable sequence snapshots compare against current
metadata values, including nested edits and supported tuple representations.
`_ackredit` selects its prepared credits by the already validated plan, detaches
only when refreshing them, and still invokes every provider credit. The public
0.9.0 registration/tracking path remains unchanged.

The real warmed-conversion regression fails before implementation. Contract
guards additionally cover input replacement with equal values, nested edits,
versions, article/software-only declarations, immutable ownership, detached
exports and absent backends. Real provider guards cover both warmed Pint/unyt
paths, changed versions in independent captures, metadata conflicts preserving
science and earlier captures, original versions/JOSS article, pipeline graph,
and saved reading blocked from producer/backend imports and network access.

Three alternating installed process pairs retain seven raw samples per case
with identical NumPy 2.5.3, Pint 0.26.1 and unyt 3.1.0, and controlled Ackredit
source cfb5140348c94f9c336740a894a1e5961f654e9d. All 64 tracked provider Python
files match that immutable source. Scalar backend-capture trial medians are
87.08–96.84 versus 76.46–84.12 microseconds; function/backend capture is
108.57–120.04 versus 97.68–102.46. Ordinary scalar controls vary
42.76–48.89 versus 43.43–46.71, so these are bounded measurements, not a
universal percentage. The 100,000-value capture cases and all raw controls are
also retained. Profiling 3,000 warmed operations shows 3,000 declaration
reconstructions/45,000 recursive deepcopy calls before, versus 3,000 value
validations and no declaration copy/freeze/detach calls after.

Outside-checkout candidate-wheel receiving passes 43 prepared-provider guards,
with only its nested build test deliberately deselected because it was executed
separately from source. The actual public-0.9.0 installed route passes 28 with
15 explicitly unavailable provisional-API skips. Five unchanged original
Pint/unyt/pipeline/offline-reader guards pass against the baseline installed
wheel as the control. Only the two attribution runtime files and generated
version differ between producer wheels. New version metadata is local
development identity, not a public release.

Source validation includes a complete prepared-provider scientific suite
(850 passed, one deliberate JSON skip), all three later provider regression
guards, and a successful rerun of the nested installer after its isolated disk
failure. A fresh public-provider full suite supplies final fallback evidence.
Ruff and HTML documentation checks pass; the four unchanged H2-heading warnings
in docs/index.md.rst remain visible. The report/proof is
`devguide/evidence/backend_declaration_plans_2026-10-05.json`. Final exact-head
CI remains required before closing this active record.
