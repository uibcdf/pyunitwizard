---
summary: Pilot optional attribution of executed third-party software and its articles.
issue: uibcdf/pyunitwizard#92
status: partial
opened: 2026-10-02
closed:
verification: reproduced
area: [integration, provenance]
guard: tests/integration/test_backend_attribution.py
normative:
blocked_by: []
supersedes: []
---

# Optional backend attribution pilot

## What

Attribute third-party libraries actually used by a workflow, citing software,
associated articles, or both as appropriate. The maintainer selected PyUnitWizard
as a smaller real client of portable attribution under uibcdf/ackredit#75.

## How

The dispatch registry observes completed construction, conversion and translation
operations for Pint and unyt only inside explicit `with puw.attribution():`
blocks. This provisional context-local opt-in restores nested choices on exit. Direct translators credit the reached endpoints;
Pint bridges credit their executed child dispatches. A loaded but unused backend,
identity return and failed dispatch earn no completed-operation credit. Earlier
completed children remain valid observations if a later operation fails.

`_ackredit.py` lazily checks the optional provider through DepDigest after a
successful operation. No provider import or registration occurs on host import
or adapter loading. Scope and contextual track calls contribute to the caller's
session. Software version IDs distinguish executed versions; article uses carry
the same software name/version without changing the article bibliography.

Host-owned offline declarations remain readable independently of the provider.
Provider absence preserves scientific results; failures emit `PUW-WARN-ACK-001`.
The application uses Ackredit's provisional capture/export/import; there is no
second bibliography schema and no change to QuantityRecord's seal or codec.

## Why

Pint software metadata is checked against its
[upstream repository](https://github.com/hgrecco/pint) and
[README](https://github.com/hgrecco/pint/blob/master/README.rst). No unit-library
Pint article or DOI has been established for this pilot; the unrelated pulsar
timing package PINT must not be cited.

unyt recommends its software and the
[JOSS article](https://doi.org/10.21105/joss.00809) in its
[upstream README](https://github.com/yt-project/unyt/blob/main/README.rst).
Software references identify repositories and actual runtime versions; no
software DOI or release-specific author list is invented.

## What is measured and what is assumed

Tests use the real editable Ackredit development provider on Python 3.13.
They verify reused references, workflow propagation, separate roles, numerical
parity, empty arrays, failure/absence, lazy import, and a fresh reader rendering
original bibliography without importing Pint or unyt or crediting another
calculation. QuantityRecord reading separately verifies its existing descriptor
through Pint without new scientific credit; its codec is unchanged. The first automatic-credit experiment measured about 195–200 microseconds of
additional cost per conversion (1 versus 100,000 elements), which is too costly
for ordinary small conversions merely because the provider is installed. This
evidence led to explicit attribution contexts; final gates and measurements
will be appended after validation. This is not published-installation evidence.

## What was refuted

Installed or loaded libraries are not a bibliography of execution. Subtracting
session IDs loses reused references. Article publication dates cannot identify
the executed software version. Catching the scientific call inside the provider
error handler would incorrectly hide scientific failures.

## Scope and exclusions

Initial coverage is dispatched construction, conversion and translation involving
Pint and unyt. Introspection, direct adapter calls, cached parse returns, internal
backend calls bypassing dispatch, other backend bibliographies and NumPy's own
citation are outside this pilot. It does not claim complete transitive software
attribution. No hooks, enrichment, journals, reminders, required dependency,
public extra, release or reduced Python support range are introduced.

## Acceptance criteria

- Real-provider credit and each detached capture retain the reached bibliography.
- Software-only and software-plus-article uses keep original runtime versions.
- Provider absence/failure preserve completed science with catalog diagnostics
  for failures, and scientific exceptions propagate.
- Fresh imports stay lazy; saved readers retain exact records without new credit.
- Fixed integration cost is measured and reviewed before expanding coverage.
- Local gates pass; publication and compatibility remain separate decisions.

## Dependencies and risks

The portable provider API is provisional under uibcdf/ackredit#75. Publication
and distribution remain in uibcdf/ackredit#22; no installation route is promised.
MolSysMT adaptation is requested from its maintainers, not implemented here.
The shared policy is uibcdf/molsyssuite#68.


## Validated source evidence (2026-10-02)

Python 3.13.14, local Ackredit development source `2e9f509` plus this work;
Pint 0.25.3, unyt 3.1.0, PyUnitWizard source `2ffe188` plus this work.

- `python -m pytest --receptor=llm tests/`: 656 passed, one skip (strict
  JSON/NaN case covered separately), one existing compatibility deprecation.
- Ruff checks/format and devguide index checks passed.
- `make html`: succeeded with four existing index-heading warnings.
- `python devtools/benchmark_backend_attribution.py` reproduces the fixed-cost
  comparison below (seven repeats; 1,000 scalar calls or 100 large-array calls).

| Elements | Original dispatcher | Ordinary observer | Explicit, provider unavailable | Workflow credit | Result capture |
| --- | --- | --- | --- | --- | --- |
| 1 | 47.0 us | 48.4 us | 47.8 us | 260.1 us | 276.0 us |
| 100,000 | 118.1 us | 115.4 us | 114.4 us | 326.9 us | 352.0 us |

Small differences in the ordinary/unavailable cases are measurement noise, not
a speedup claim. Active attribution costs roughly 200–240 us per completed
dispatch on this machine, independent of array length. This cost is explicitly
opted into; ordinary conversion does not load the provider. No timing assertion
depends on this hardware, and broader coverage remains a separate review.

The owning reports are cross-linked to uibcdf/molsysmt#292 (member-owned
adaptation) and uibcdf/molsyssuite#71 (registered guide delivery). Portable API
adoption and publication remain pending; this record stays open/partial until
their corresponding acceptance gates are met. No published-installation claim
is made from this editable-source test run.
