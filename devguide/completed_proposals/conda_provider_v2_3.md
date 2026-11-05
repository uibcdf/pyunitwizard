---
summary: Adopt the reviewed immutable Conda build/upload/promotion provider without changing publication scope.
issue: uibcdf/pyunitwizard#136
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: inspected
area: [ci, packaging, dependencies]
guard: tests/test_noarch_conda_publication.py::test_owned_publisher_keeps_noarch_format_and_disables_optional_release_creation
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Conda provider v2.3.0 owner review

What — Receive MolSysSuite #87's local-publisher handoff and immutable provider
`87c70b1443d5f22d738ee3ddf812bdbe0152f6c2` (v2.3.0), with central delivery
`95f693be10c9205ab9b912cb53453710a207bf45` as review evidence, not an action pin.

How — Keep the owned noarch workflow, recipe, environment, exact-source gates,
source/file binding, independent public verifier and staged/direct decision.
Pin both build/upload invocations and separate exact-file promotion to the
reviewed provider source. Preserve outputs and attempt-qualified evidence
retention. Remove the unnecessary deprecated `mambabuild: false` input; use
explicit `--package-format 1` so the existing .tar.bz2 filename/receiving
contract is preserved. No cross-platform conversion is requested. A noarch
artifact is not a cross-compiled native extension.

Why — v2.3.0 selects the active environment's Conda executable instead of an
activated base shell function, and guards unsupported conversion formats.
The local consumer keeps its scientific/runtime and installed receiving gates;
central provider tests do not replace them.

## Review boundary

Actual build/profile source and both prior action refs were inspected. Native
recipe tests still execute before upload; version/import/physical smoke gates,
exact candidate and installed-artifact validation are retained. No --no-test,
force/overwrite, credential change, withdrawal or activation of a suspended
publisher is introduced. The optional provider GitHub Release creator is
explicitly disabled: PyUnitWizard owns its canonical Release/title route.
Its descriptive-title limitation is reported to the provider in
`uibcdf/action-build-and-upload-conda-packages#53`; it is not an active consumer
path and does not block this adoption.

Acceptance — Protect owned format/platform/label/release inputs and all
existing publication guards, inspect the pinned source and run its relevant
offline build/producer/upload/promotion operation controls. Distinguish
simulated transports from real registry or scientific qualification. Refresh
only reviewed workflow fingerprints, retain exact source/check scopes and
respond Review completed in the owner issue and MolSysSuite #87. All mandatory
candidate/installed/public gates remain due for a future actual release.


## Review completed — 2026-11-05

Both local build/upload steps and exact-file promotion now use the reviewed
full provider SHA. The owned publisher/format/platform/label/release controls
fail before the change and pass afterwards. All 37 selected local publication,
workflow, dependency and reporting contracts pass; the 22-route dependency
preflight passes. The shared action's 29 relevant immutable-source operation
fixtures pass on Python 3.14.7/anaconda-client 1.14.1, with simulated registry
transports. Source/native/installed/scientific proof remains separate.

The complete final local source suite passes 1,007 cases, with two unavailable
Zarr-module skips, the existing strict-JSON/NaN skip and deprecated-main
warning. No upload/promotion workflow was dispatched, no credentials changed
and no old producer receipt, tag or package archive modified. The selected
guard protects the actual owned noarch format, disabled conversion/optional
Release route and absence of force inputs. It does not replace executed
publication gates. The known inactive provider title limitation is reported
at `uibcdf/action-build-and-upload-conda-packages#53`.

Exact provider/consumer source hashes, operation case classifications, JUnit
identities and verified scope are retained in
`devguide/evidence/conda_provider_adoption_2026-11-05.json`. Source/runtime
floor and licensing adoption have their own #134/#135 records. Respond to
MolSysSuite #87 with the final published consumer commit and actual gates;
a future normal candidate still owns real archive/installed/public evidence.
