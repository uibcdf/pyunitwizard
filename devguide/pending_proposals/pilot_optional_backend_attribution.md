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
The application uses Ackredit's accepted capture/export/import contract; there is no
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

The portable provider API is accepted in source under uibcdf/ackredit#75 for
the prepared 0.9.0 candidate. Publication and distribution remain in
uibcdf/ackredit#22; no public installation route is promised.
MolSysMT adaptation is requested from its maintainers, not implemented here.
The shared policy is uibcdf/molsyssuite#68.

## Delivery and function-provider follow-up (2026-10-04)

The earlier candidate/publication boundary is now historical: Ackredit 0.9.0 is
public, and uibcdf/ackredit#22/#75 are closed with exact artifact and installed
matrix evidence. The existing portable backend pilot can use that release.
The separate dependency-free public function declarations in
uibcdf/pyunitwizard#94 require Ackredit's development observer under
uibcdf/ackredit#84; they do not change this pilot's completed-dispatch semantics
or add a mandatory dependency. Protocol promotion remains open upstream.


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


## Provider source and guide delivery (2026-10-02)

The tested portable API source is now published in Ackredit commit `4228444`,
with source-qualification fix `4577c83`. The central guarded synchronizer
delivered the canonical `ACKREDIT_GUIDE.md` to this checkout and its read-only
check confirms byte equality. PyUnitWizard pilot commit `4be3500` remains local;
provider package publication and member compatibility remain separate gates.
The benchmark provider-unavailable column uses a controlled no-provider return;
genuine missing-provider behavior is verified independently in a fresh-process
integration regression.

The synchronized root guide is routed from `AGENTS.md` and explicitly excluded
from Ruff, as required by the common read-only guide contract.


## Authorized source publication

The maintainer explicitly authorized direct push without a pull request for this
pilot and guide delivery. Source commits `4be3500` (optional backend attribution)
and `c3b7117` (synchronized guide and contributor routing) are prepared for
publication to `origin/main` together with this record update. Provider source
commit `561989e` corrects explicit CSL authors; its seven remote checks pass.
Publication does not promote the provisional API or establish package-release
compatibility. After guide routing, the focused integration/dependency/reporting
gates pass 30 tests and Ruff/index checks pass.


Final publication qualification on Python 3.13.14: the full PyUnitWizard suite
passes 656 tests with one documented strict-JSON/NaN skip and one existing
compatibility deprecation. The published Ackredit provider is now `6420407`
(implementation `561989e` plus archived record); its primary checkout passes
1,541 tests with all original maintainer edits restored unchanged. The canonical
guide bytes are unchanged. Publication receipts are recorded in this issue;
API promotion and released-installation qualification remain separate.


## Accepted provider contract and synchronized guide (2026-10-03)

Ackredit source `840aab3d415312144e4f5754d5def11b3068832f` accepts
`Attribution`, `capture` and `get_attribution`, with the documented
`ackredit.attribution@1` compatibility boundary and a frozen real unyt workflow
fixture. It assigns the first accepted contract to the prepared 0.9.0 candidate;
this is not an already published release.

The central guarded synchronizer refreshed this repository's read-only
`ACKREDIT_GUIDE.md` from that committed provider source, replacing the
provisional-provider wording. Registration remains tracked in
uibcdf/molsyssuite#71. Real source-provider compatibility passes all 17 backend
attribution integration tests on Python 3.13; this evidence remains distinct
from the forthcoming exact Conda installed-provider qualification. The local
`puw.attribution()` opt-in remains a pilot; guide delivery does not promote its
product contract or add a public dependency floor.
