---
summary: Pilot dependency-free function citation declarations for PyUnitWizard.
issue: uibcdf/pyunitwizard#94
status: partial
opened: 2026-10-04
closed:
verification: reproduced
area: [integration, provenance]
guard: tests/integration/test_function_citation_provider.py::test_normally_installed_consumer_outside_checkout
normative:
blocked_by: [uibcdf/ackredit#84, uibcdf/molsyssuite#97, uibcdf/moli#46]
supersedes: []
---

# Dependency-free function citation provider

## What

Declare PyUnitWizard's existing software bibliography and references for public
`quantity`, `convert`, `conversion_factor` and `standardize` functions without
depending on Ackredit. Applications may explicitly observe this bounded surface
with the provisional Ackredit function-provider API.

## How

The ordinary package module exports an inert `__ackredit__` dictionary using
`ackredit.provider@1`. The version is the original producer's runtime version;
software identifiers distinguish versions. The software DOI and three authors
are the existing authority in `docs/content/about/citation.md`; no new article,
release date or release-specific DOI is invented.

Ordinary import creates only metadata: no Ackredit import, function wrapper,
unit-backend load or credit. Explicit `ackredit.observe_calls(puw)` resolves only
the declared lazy exports through the producer's ordinary module `__getattr__`.
Original function signatures, behavior and object identity are retained outside
observation. Public import aliases obtained before activation remain outside
this observer's contract. `pyunitwizard.api`, internal helpers, other public
functions and dynamically registered fast tracks are not separately declared.

The existing `puw.attribution()` context independently attributes completed
Pint/unyt dispatches. An application can combine both contexts: a public function
entry records PyUnitWizard, while an executed successful child dispatch records
the corresponding backend software and established description article. Loaded
but unused backends are never attached statically to public functions.

When the optional provider exposes `prepare_credit` (Ackredit #87), the host
prepares fixed dispatch credits once and compares current detached declarations
by value before reuse. Invocations still reach every current result capture and
session. Provider bibliography replacement is diagnosed as an attribution gap,
preserving completed numerical results. The existing register/track boundary
remains the fallback for released Ackredit 0.9.0.

## Why

Ackredit's first producer fixture validates the mechanism but is not evidence of
a real scientific library integration. This smaller real client exposes lazy
API constraints and demonstrates the separation between host-function entry and
successful backend execution before protocol stabilization.

## What is measured and what is assumed

The test-first Ackredit lazy-export reproduction failed on previous source;
the corrected observer resolves declared names only and refuses conflicting
function metadata or loader failures before installing observation wrappers.
PyUnitWizard tests run with that real source provider on Python 3.14.

Guards exercise independent captures, exact producer versions, backend selection,
no-op/failed scientific calls, lazy import/activation, BibTeX and a separate reader
that blocks PyUnitWizard/Pint/unyt imports. The installed-consumer guard builds
PyUnitWizard normally using a fresh minimal build interpreter and runs from a
directory outside both repositories. Absence and presence run in separate
interpreters; replacing the provider's importability inside one interpreter would
exercise dependency-discovery caches rather than an ordinary installation.

`devtools/benchmark_backend_attribution.py` measures warmed conversion medians
and retains all seven samples, dependency versions and observer/source hashes.
Activation, imports and initial registration are excluded and reported as such.
Results are machine-specific, not universal performance guarantees.

## Measured receiving evidence (2026-10-04)

Linux/Python 3.14.7, Pint 0.25.3 and unyt 3.1.0. The normally installed
development providers report Ackredit `0.9.0+20.gb67ea77.dirty` and PyUnitWizard
`0.27.0+50.g4792a8a.dirty`; the receipts identify their actual runtime sources
with SHA-256 rather than treating those dirty version strings as exact commits.
The observer, fixed-credit factory and receiver are source improvements; public
0.9.0's archive is unchanged.

Raw seven-repeat measurements are retained in
`devtools/receipts/function_provider_94_before_2026-10-04.json` and
`devtools/receipts/function_provider_94_2026-10-04.json`:

| warmed Pint conversion | 1 value before / after (µs) | 100,000 values before / after (µs) |
| --- | --- | --- |
| ordinary, attribution disabled | 48.95 / 47.33 | 119.67 / 112.30 |
| backend references, workflow | 267.65 / 96.80 | 332.84 / 156.22 |
| backend references, result capture | 272.34 / 96.75 | 338.81 / 165.85 |
| public function plus backend, result capture | 302.02 / 114.79 | 379.25 / 183.55 |

For the small captured conversion, total time drops about 64%; adding the
public-function observation as well drops about 62%. Ordinary timings also
drift, so these are measured local total-time changes rather than universal
percentages or claims that every scientific pipeline becomes faster. Initial
preparation is excluded; the optimized backend capture still adds about 49 µs
above the ordinary small conversion, and combined function/backend capture adds
about 67 µs. Further optimization should use this real boundary and retain its
numerical, reference-identity, gap-diagnostic and independent-capture guards.

Local gates on Python 3.14.7: 633 passed, ten optional/sibling-dependent skips,
one existing deprecated-import warning; Ruff and report indexes pass. `make
html` succeeds with four MyST heading-level warnings in unchanged `docs/index.md`
(lines 25, 31, 51 and 57). Building the unmodified upstream source reproduces
the same four warnings; this pilot changes no public documentation. Ackredit's
own expanded gate passes 1,635 without skips and its strict Sphinx build passes.
Exact published source commits and hosted receipts are linked in the issue.

## What was refuted

Declaring every backend on `convert` would credit unused libraries. Treating
function entry as completed backend work would lose no-op and failure semantics.
Eagerly importing the API or Ackredit to expose declarations would regress the
lazy public facade. Silent discovery through `dir()` is unnecessary: names are
explicitly supplied by the producer.

## Scope and exclusions

Four public synchronous operations and the existing Pint/unyt dispatch pilot.
No complete transitive bibliography, import hooks, enrichment, profiling,
mandatory dependency, public extra, protocol stabilization or release is implied.
Experimental usage remains in the developer guide pending receiver review.

## Acceptance criteria

- The metadata remains readable and scientific operations work without Ackredit.
- Observation captures called operations, producer versions and actual backends.
- Independent results receive reused references and preserve the pipeline graph.
- Detached readers render the original bibliography without loading producers.
- Normal installed consumption outside checkouts and local repository gates pass.
- Real conversion overhead and remaining boundaries are reported to Ackredit #84
  and the cross-component review owners before API promotion.

## Dependencies and risks

Public Ackredit 0.9.0 supports the existing portable backend pilot but does not
contain `observe_calls`. This development protocol remains provisional under
uibcdf/ackredit#84, uibcdf/molsyssuite#97 and uibcdf/moli#46. Tests skip the new
observer integration when that optional capability is absent; ordinary host
operation and existing portable attribution retain their separate guards.

No next tag is created in this iteration. Protocol stabilization, broader
scientific operation coverage and public delivery are separate owner decisions.
