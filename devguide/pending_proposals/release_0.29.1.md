---
summary: Prepare and qualify the 0.29.1 maintenance release.
issue: uibcdf/pyunitwizard#138
status: active
opened: 2026-11-05
closed:
verification: inspected
area: [release, packaging, documentation]
guard:
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

## Dependencies and risks

GitHub runner availability is currently delaying source qualification. Do not
weaken matrices or infer passing results from queue state. Optional-provider
resolution, scientific behavior and new provider operations need actual native
evidence; their previous bounded source checks are not package qualification.
MolSysSuite owns canonical-guide synchronization and consumer receiving through
#127 and the existing floor/license/provider rollouts. Client copies are not
edited here. The shared environment's unrelated dependency conflicts stay with
MolSysSuite #82; clean candidate prefixes have their own required closures.
