---
summary: Qualify and publish the 0.29.1 maintenance release.
issue: uibcdf/pyunitwizard#138
status: resolved
opened: 2026-11-05
closed: 2026-11-06
verification: measured
area: [release, packaging, documentation]
guard: tests/test_noarch_conda_publication.py::test_promotion_workflow_checks_exact_release_and_file_identity
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.1 preparation

## What

Prepare the maintenance release containing the completed Astropy calorie and
registry correction (#137), numerical floors (#134), actual-license/build
metadata (#135) and reviewed Conda provider adoption (#136). The maintainer
authorized preparation on 2026-11-05. The public version remains 0.29.0.

## How

Use the staged route in `devtools/conda-build/release_plan.toml`. Packaging,
dependency and provider changes need clean installed-file evidence before
public visibility. Retain all 29 required source profiles and all 30 installed
baseline/storage/OpenFF/prepared cells over the existing Linux/macOS arm64 and
Python ranges. Every installed cell must execute the candidate's calorie
regressions; missing or skipped required cases fail the gate.

Commit the plan and notes before selecting the exact candidate SHA. Execute
the five required source workflows at that SHA, plus ordinary CI/coverage.
Earlier source results retain their identities and do not qualify the new
candidate. After source qualification, build one immutable
`pyunitwizard-0.29.1-py_0.tar.bz2` under the staging label,
retain producer/source/digest receipts, and qualify that same file in every
installed cell. Do not rebuild a passing file to update documentation.

Prepare a concrete publication decision with the source, producer, file digest,
required native results, dependency closures and draft notes. Final public
tag/Release/promotion is a separate decision after that reviewable evidence;
preparation does not itself publish a release. The canonical title/tag is
exactly `0.29.1`. A later authorized publication retains the existing independent
public verifier, clean receiving, documentation and central-notice requirements.

## Why

This is a maintenance checkpoint: it corrects existing physical unit behavior
and records compatible dependencies and existing licensing. No new interchange
format or computing quantity class is introduced. qrec/bundle bytes and the
provisional status of record, storage, dialect and attribution APIs remain.

## What is measured and what is assumed

Source `9100cca30b55b4fc1ebed293cd59df45047865bb` has successful ordinary
CI 42086547208/1 and policy 42086547842/1, with native steps verified. Local
maintenance receipts retain 1,007 passing cases and eight skipped JUnit entries
(five optional collection modules, two unavailable-Zarr cases and one
intentional strict-JSON/NaN case). All 25 calorie cases execute without skips
on actual Astropy 8.0.1/Python 3.14.7 and Astropy 6.1.7/Python 3.11.18.
The numerical minimum and real license-archive profiles have independent
receipts. These observations do not replace the new exact-source/installed
release gates.

Preparation checks pass: 34 publication/dependency/workflow/reporting cases,
33 release-route/version/installed-binding controls, current generated report
indexes and clean diff whitespace. The pinned shared dependency preflight
verifies all 22 routes with declared-and-installed public bounds. No runtime
implementation changes are introduced by the release-plan/notes commit.

Earlier full matrix 42086560353/1 has three successful Linux cells (Python
3.11, 3.13 and 3.14); Linux/3.12 and four macOS cells were still queued at
preparation. Runners have not executed those cells. The release candidate's
new exact-source matrix supersedes this checkpoint for release qualification;
record any cancellation explicitly and retain the three successful observations.

## Scope and exclusions

Preserve published 0.29.0 tags, files, producer and historical receipts. No
PyPI route, new optional engine, client migration, stable format admission,
upstream Astropy patch or registry withdrawal is part of preparation.
Astropy #20790 independently confirms the failed native-context mechanism;
PyUnitWizard's prevalidation avoids it without depending on an upstream repair.
The process-wide Astropy registry still needs external serialization for
application-owned concurrent changes.

## Candidate recovery — 2026-11-05

The initial planned source `85c9bf8e398f03df6cc5490ea5e99ed1ff94cc08`
passes ordinary CI and all six Release Gates jobs. Its full matrix nevertheless
fails Linux/Python 3.12 in the record dimension-handshake regression: that test
inherits a worker's unyt policy and requests the known unsupported `nanomolar`
spelling. #139 reproduces the test under all four policies, corrects its explicit
output contract and separately guards the supported `mole/liter` reader route.
The correction changes tests and records only; public adapter behavior is
unchanged. Its complete local twelve-worker suite passes 1,015 cases with eight
skipped JUnit entries (three executed cases and five optional collection modules).

The original failure and successful original-source jobs remain historical
evidence. Select the corrected commit after publishing #139 and execute all
five required source workflows at that new SHA before building the staging file.
No retry at the rejected original source qualifies the corrected candidate.

## Acceptance criteria

- All 29 required exact-candidate source jobs and their named steps execute
  successfully; no backlog-only run, prior SHA or omitted profile qualifies.
- Actual archive metadata, license/notice resources, package version and source
  binding are verified before candidate upload.
- One staged file's digest is verified in all 30 installed cells, with clean
  dependency closures and all required regression/consumer modules executed.
- A reviewable final publication decision identifies all actual receipts and
  pending scope. Publication waits for the maintainer's final decision.
- After an authorized publication, independently verify unchanged promoted
  bytes, public solver-index receiving and served documentation; deliver the
  version-specific MolSysSuite notice before closing this release issue.
- Complete #140's default-branch archival caller before publication, then
  manually probe the exact 0.29.1 tag and retain its actual semantic state.
  Its original source predates that caller; the fixed-cutoff schedule provides
  ongoing recovery without rebuilding or retagging the Conda file. Only a
  verified public record permits a version DOI/archive claim.

## Dependencies and risks

GitHub runner availability is currently delaying installed qualification. Do not
weaken matrices or infer passing results from queue state. Optional-provider
resolution, scientific behavior and new provider operations need actual native
evidence; their previous bounded source checks are not package qualification.
MolSysSuite owns canonical-guide synchronization and consumer receiving through
#127 and the existing floor/license/provider rollouts. Client copies are not
edited here. The shared environment's unrelated dependency conflicts stay with
MolSysSuite #82; clean candidate prefixes have their own required closures.

## Qualified source and staging checkpoint — 2026-11-05

The corrected source is `ab92f1e645dfdd291f76785795b0d15b6a8c1257`.
All 29 mandatory native source profiles and their required steps passed at
that SHA, together with ordinary CI and both coverage-upload steps. The shared
preflight verifies the original candidate's 22 acquisition routes. Retained
semantic source proof is in `devguide/evidence/release_0.29.1_source.json`.

Producer 42125299597/1 built and uploaded exactly one noarch file:
`pyunitwizard-0.29.1-py_0.tar.bz2`, 96,418 bytes, SHA-256
`5bdf9b137c8862f99fc26e6ea5aa6e2ecea5a46ee1dc5e71127565411fedbe27`.
Its producer event, reviewed route and independent downloaded-byte inspection
are retained in `devguide/evidence/release_0.29.1_{producer,route,staged_bytes}.json`.
Registry labels contain staging only. Actual metadata, both original license
payloads, notice/catalogue resources and 92 tracked Python source files match
the original candidate; generated `_version.py` is intentionally separate.

Installed qualification 42129616605/1 binds the same source and file. Its
producer-binding job passed; all 30 expected profiles are registered. Eight
installed profiles have passed at this checkpoint, including macOS arm64 and
Python 3.14, while 22 remain queued. No installed failure has been observed.
These partial results do not authorize publication.

The two CLI dispatch requests that returned HTTP 500 created no matching runs.
A direct REST dispatch with string-valued inputs created exactly one matching
installed run; no candidate-source change or duplicated qualification was
needed. The CLI/backend failure mechanism remains unconfirmed.

Operational archival and evidence commits on main are separate from the
qualified source. Preserve `ab92f1e` as the eventual 0.29.1 tag target and the
same staged bytes; do not rebuild to incorporate those operational records.


## Installed qualification complete — 2026-11-06 UTC

Installed run 42129616605/1 completed successfully at source/qualifier
`ab92f1e645dfdd291f76785795b0d15b6a8c1257`. All 30 expected profiles execute:
8 baseline, 8 storage, 6 OpenFF and 8 prepared across Linux/macOS arm64 and
the declared Python minors. Every native job and all 240 required steps pass.
Downloaded Conda/pip closures, actual Python architecture/version and JUnit
reports were independently audited against the original binding and digest.

There are 10,100 passing JUnit entries, including 750 unskipped calorie cases,
120 policy-handshake cases and 60 explicit concentration-reader cases.
Every required profile-specific storage, OpenFF and prepared-attribution guard
executes without skips. Separately classified skips are the intentional strict
JSON/NaN case (30 entries) and provisional prepared-credit cases under the
intentionally older Ackredit profiles (110 entries); the prepared profiles
execute those required attribution guards using Ackredit 0.10.1.
Safe per-cell job IDs, closure/JUnit hashes, provider versions and results are
retained in `devguide/evidence/release_0.29.1_installed.json`.

The original file remains staging-only with unchanged size and SHA-256.
#140 is resolved with actual hosted verification of existing 0.29.0 archival;
its independently bounded recovery is ready for the first manual 0.29.1 probe
following a future public Release. Documentation-head CI 42139187015/1 and
policy 42139187246/1 pass. These operational commits remain separate from the
qualified source and do not move its eventual tag target.

Preparation is complete. The concrete decision is in
`devguide/release_0.29.1_publication_decision.md`; final public tag/Release,
exact-file promotion, public receiving, served documentation, canonical-guide
update and central version notice remain pending the maintainer's decision.
The issue remains active until those publication outcomes are verified.


## Published outcome — 2026-11-06 UTC

Diego explicitly approved final publication and clean upstream-main closeout.
Stable Release 0.29.1 (436100116) and the dereferenced annotated tag retain
original source `ab92f1e645dfdd291f76785795b0d15b6a8c1257`. Producer, original
96,418-byte archive and SHA-256 remain unchanged. Release event 42162787779/1
verifies the staged decision and skips both build/upload branches. Promotion
42162820178/1 succeeds; the pinned public verifier independently confirms
main label and solver index. Public receiving from a fresh Linux/Python 3.14.10
prefix passes 132 selected guards with one intentional strict-JSON/NaN skip,
clean pip requirements, exact file/version/origin/resources and all 25 calorie
cases. Its freely resolved dependency closure is retained separately from the
30-cell pinned qualification.

Documentation publication 42162787792/1 and Pages deployment 42162885745/1
succeed at the original release source. Fresh served pages show 0.29.1 and
expected content. Exact-tag Zenodo probe 42162823352/1 explicitly verifies
record 23995546, version DOI 10.5281/zenodo.23995546 and one 3,091,218-byte
source ZIP (md5:a24d8034c8dac15ea633b1da7934b49c). Archival coverage is the
source snapshot only, not the Conda file.

The complete safe publication receipt is
`devguide/evidence/release_0.29.1_2026-11-06.json`; full sanitized Conda/pip
closures and JUnit classifications for all 30 cells are retained in
`release_0.29.1_installed_closures.json`, with the public closure separately.
The durable guard protects the original published source/tag identity and
exact-file/digest/public-verification ordering; it complements actual native
science and does not replace those measured results.

Canonical `standards/PYUNITWIZARD_GUIDE.md` is updated in
`de0969242d094f687ff047d08ac950031c882da8`, SHA-256
`1c2c00b7ebafd7c611311fe634e4ac81b4ce30b84ae2a4eccfb0939cc675fb8b`.
[MolSysSuite #172](https://github.com/uibcdf/molsyssuite/issues/172) is the
version-specific release/package and guide handoff. Suite receiving owners
synchronize all client copies; no client installed adoption is implied.
Published 0.29.0 history, deferred feature scope and provisional contracts
remain. Task-owned installation/cache/raw captures are reviewed for cleanup
once their safe semantic evidence is committed; shared workspace and unrelated
caller pytest resources are preserved.
