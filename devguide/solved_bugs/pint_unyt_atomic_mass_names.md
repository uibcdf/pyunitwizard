---
summary: Translate Pint atomic-mass names and prefixes to reversible unyt units.
issue: uibcdf/pyunitwizard#124
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [forms, interoperability]
guard: tests/forms/test_api_pint.py
normative:
blocked_by: []
supersedes: []
---

# Pint atomic masses entering unyt

## What

At source e2ff4e9bf70cf8cb514fb24513e4d91e34cb0326, Pint `dalton`/`Da`
quantities and units cannot enter unyt. Expanded reproduction also fails for
`amu`/`unified_atomic_mass_unit`, kilo/milli prefixes, and compound units.
Native unyt `amu` can travel in the other direction. OpenMM atomic masses
also fail on the existing semantic Pint route to unyt.

## How

unyt 3.1.0's `from_pint` alias table recognizes the historical Pint name
`atomic_mass_unit`, whereas Pint 0.25.3 emits `dalton` or
`unified_atomic_mass_unit`. The owning reusable operation is
`forms/api_pint.py::quantity_to_unyt`; unit translation and OpenMM's semantic
translator already call it.

Recognize canonical atomic-mass factors through Pint's unit-name parser. For
each recognized factor, define its canonical name and actual prefix scale in
a conversion-local unyt registry, using native unyt `amu` as the mass reference.
Copy the existing default registry's definitions and unit system before adding
these aliases, so unrelated application-defined unyt units remain available.
Then delegate magnitude and compound-expression translation to `from_pint`.
Keep the names so reverse quantity and unit translation are both supported.
Unrelated units continue through the original default-registry route. Neither
the shared unyt registry nor Pint definitions are mutated. No Pint registry,
new dependency, parser mode, dispatch key or record layout is introduced.

## Why

Atomic masses are a normal molecular-data boundary. Display-name substitution
alone is insufficient: prefixes must retain scale in unit-only conversions,
and replacing prefixed units with numeric coefficients breaks unyt's native
reverse Pint translation. A trial numeric-coefficient representation exposed
that limitation and was discarded; the retained implementation uses named units.

## Evidence and scientific limits

Python 3.14.7, Pint 0.25.3, unyt 3.1.0 and OpenMM 8.6.1. All 25 initial new
cases fail before the source correction with `UnitParseError`. The expanded
adapter module has 42 passing cases after correction, including 40 new cases.

Pint's atomic mass constant is 1.66053906892e-27 kg and unyt's native `amu`
is 1.660538921e-27 kg in this environment. Retain the existing backend atomic-mass
convention; do not silently update their CODATA definitions. Tests check native
atomic-mass factors and round trips, plus SI agreement within 1 ppm (raised
powers in this bounded test set remain within that tolerance). This is not a
new claim of bit-identical SI constants across providers. The established
OpenMM molar/pure-mass policy is separately exercised.

## Acceptance criteria

- Scalar, 2-D float32/float64 array, unit, compound, inverse and fractional-power
  translations work; source values, dtype and shape are retained.
- Reverse quantity and unit conversions preserve prefix scale. Altered foreign
  Pint definitions are still rejected by the public normalization boundary.
- Shared unyt definitions remain unchanged and no Pint registry is constructed.
- Focused/full tests, Ruff, documentation and final exact-head native gates pass.
- Archive the issue-backed record and synchronize indexes and GitHub state.

## Dependencies and impact

Shared-provider notice and consumer ownership remain in uibcdf/molsyssuite#127.
Source qualification does not publish 0.28.2 or qualify a replacement installed
artifact. No client guide or client copy is changed. Existing global environment
dependency gaps remain independently tracked in uibcdf/molsyssuite#82.

## Resolution and validation

The adapter now supplies the local named-unit registry only for recognized
atomic-mass factors. All other translations retain the existing provider route.
The module guard protects construction, direct/public translation, inverse and
fractional powers, array dtype/shape, reverse unit/quantity factors, the OpenMM
molecular-mass convention, shared-registry isolation and foreign-definition
rejection. A further regression first fails when an unrelated application-defined
unyt unit is absent from the local registry; cloning existing definitions fixes
that case without changing the shared registry. All 40 new cases pass; the
original two adapter cases still pass.

- 108 focused adapter, backend-matrix, foreign-registry and reporting tests pass.
- Final full local suite: 915 passed, one expected strict-JSON/NaN skip and the
  existing `pyunitwizard.main` deprecation warning; Python 3.14.7, 44.81 seconds.
- Physipy 0.2.8 and quantities 0.16.4 live only in a task-owned temporary overlay;
  the isolated installed-consumer build has network access. The shared environment
  is unchanged. This does not clear unrelated global dependency gaps.
- Repository-wide Ruff lint/format passes (214 files), and owned-copy `make html`
  with `-W --keep-going` completes without warnings. Index/diff checks pass.

Final exact-head native CI/policy receipts are exported in #124 at closeout.
Task-owned resources are removed only after the required evidence is retained.
No public release or installed-artifact requalification is performed here.

## Pre-0.28.2 backlog review

The 2026-10-22 authenticated review finds no additional open defect after #124.
There are no open PRs. The eight remaining issues are proposals: #85's remaining
dialects and #102–#105's record/storage extensions require identified measured
consumers; #87 is conditional later work; #44 and #52 explicitly remain post-1.0.
Their acceptance conditions have not acquired evidence justifying implementation
in this patch. Leave them open with their existing records and decisions.

The next useful step is a separately owned 0.28.2 release preparation: review the
accumulated 0.28.1-to-head delta, select the release route, run the mandatory exact
candidate source and installed-file matrices, and then publish the qualified file.
Source CI and this review do not substitute for those release gates. Central
guide delivery (#126) and consumer-impact coordination (#127) remain independent
MolSysSuite owner work, not additional local runtime fixes.
