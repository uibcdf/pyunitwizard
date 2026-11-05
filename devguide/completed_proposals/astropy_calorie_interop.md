---
summary: Support native Astropy thermochemical calories at energy-per-mole boundaries.
issue: uibcdf/pyunitwizard#137
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: reproduced
area: [forms, interoperability]
guard: tests/astropy_units/test_calorie_interop.py::test_energy_per_mole_with_every_source_and_default
normative:
blocked_by: []
supersedes: []
---

# Astropy calorie interoperability

What — DockingMT's energy-per-mole boundary fails when Astropy is the input or
default form. Native Astropy imperial calories exist but are disabled by default.
Use the existing thermochemical definition: one calorie is 4.184 joules.

How — The Astropy adapter owns narrowly scoped native-unit activation while
parsing quantities/units and conversion targets. Restore the native registry on
success and failure, serialize adapter-owned registry writers and preserve the
application's PyUnitWizard policy. Reuse the Pint foreign-registry verifier;
refuse conflicting named physical definitions rather than relabeling values.
Native Astropy registry contexts are process-wide; concurrent application-owned
Astropy registry changes require application serialization.

Why — Consumers must not install their own calorie aliases or switch users'
quantity policies. Reuse native backend parsing and scientific definitions,
rather than maintaining another unit parser or calorie convention.

Acceptance — Test all sixteen source/default combinations of Pint, OpenMM,
unyt and Astropy; 12.552 kJ/mol equals 3 kcal/mol. Cover strings, unit objects,
round trips, wrong dimensions/definitions, caller policy, registry restoration
after failure and fresh-process initialization. Source qualification does not
publish a new package or qualify a complete DockingMT workflow.

Initial Python 3.14.7/Astropy 8.0.1/Pint 0.25.3 regression run fails before the
implementation. Test policy was then made explicit so an inherited non-parser
default cannot obscure the energy regression. Shared-environment external
closure findings remain owned by MolSysSuite #82; no unrelated dependency is
changed here. Local editable metadata was refreshed without dependencies.


## Implemented outcome — 2026-11-05

All 16 input/default pairs now convert 12.552 kJ/mol to 3 kcal/mol and back.
Native scalar-string parsing, unit objects, missing/wrong dimensions, conflicting
Astropy definitions, foreign and modified shared Pint definitions, policy
preservation and fresh-process activation are covered. No global imperial
namespace is permanently enabled. Unit-definition failures have catalog code
`PUW-ERR-UNIT-001`, with rebuild-safe structured exception fields.

Python 3.14.7, Astropy 8.0.1, Pint 0.25.3, unyt 3.1.0 and OpenMM 8.6.1:
47 targeted scientific/catalog cases pass; the complete local source suite
passes 1,004 cases with three classified skips (two unavailable Zarr modules
and the existing strict-JSON/NaN case), plus the existing deprecated-main
warning. The first full attempt had six missing-physipy/quantities failures;
actual physipy 0.2.8/quantities 0.16.4 were then supplied in a task-owned
no-dependency overlay, not by altering the shared environment. Original shared
closure findings stay under MolSysSuite #82. Ruff and warning-free Sphinx pass.

The guard checks observable energy/unit equivalence for all 16 backend-policy
combinations. Other named-definition and registry-restoration guards protect
against a misleading success at the same numeric dimensions. Publication and
installed/consumer qualification remain separate: no tag, archive, public
package or DockingMT source was changed by this implementation.
