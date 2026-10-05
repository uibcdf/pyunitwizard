---
summary: Optional OpenFF registry interoperability with verified unit definitions.
issue: uibcdf/pyunitwizard#86
status: active
opened: 2026-10-04
closed:
verification: inspected
area: [forms, interoperability]
guard: tests/forms/test_api_openff_units.py::test_altered_foreign_openff_definitions_are_refused
normative: devguide/api_freeze_pre_1.0_decision.md
blocked_by: []
supersedes: []
---

# OpenFF compatibility

What — Own the optional `openff.units` form, native OpenMM conformance and
explicit serialization boundary in PyUnitWizard rather than each consumer.
Prerequisite foreign Pint registry normalization #84 is already implemented.

How — Reuse that normalization operation with an explicit destination registry;
check dimensions, named base units, scale and affine offset at the existing
1e-12 tolerance. Register a lazy form with source/destination adapters, reuse
OpenFF's OpenMM operations, and expose documented val/unit import/export tools
with explicit reader expectations. Existing qrec bytes remain unchanged.

Why — OpenFF uses its own Pint registry. Equal unit strings alone do not prove
equal definitions. Compound and molecular units must survive conversion without
silently transferring changed registry meanings.

Distribution correction — Official 0.4.0 source and conda-forge metadata confirm
Python >=3.12,<3.15 and Pint >=0.24,<0.26. PyPI's sole 0.3.2 upload is yanked
because it was uploaded without coordination with maintainers. Do not publish
an unusable pip extra or recommend that file. Use optional conda-forge 0.4.0;
keep the baseline dependency set/Python 3.11 support unchanged and provide a
clear diagnostic there. Development/optional test environments may constrain
Pint to the supported intersection without pinning the runtime baseline.

Sources: [official 0.4.0 metadata](https://github.com/openforcefield/openff-units/blob/0.4.0/pyproject.toml),
[official API](https://docs.openforcefield.org/projects/units/en/stable/api/generated/openff.units.html),
[PyPI status](https://pypi.org/pypi/openff-units/json).

Acceptance — Real optional artifact installation, scalar/n-D/dtype/compound and
cross-registry arithmetic cases; refuse altered definitions in both directions;
native OpenMM parity including Vec3; scalar strings and unsealed val/unit
boundary checked with field/unit/dimension expectations before codec conversion;
non-default policy, lazy imports, absence/Python 3.11 diagnostics, baseline full
suite and identified optional matrix. No stable schema or public release claim.
