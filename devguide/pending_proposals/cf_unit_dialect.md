---
summary: Bounded CF/UDUNITS unit dialect for verified HDF5 quantities.
issue: uibcdf/pyunitwizard#108
status: active
opened: 2026-10-05
closed:
verification: inspected
area: [units, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bounded CF/UDUNITS unit dialect

What — Implement the independently closable physical-unit slice of #85 needed
by #101. Published MolSysMT #240 and its H5MSM datasets identify coordinates,
time intervals, velocities, B factors, temperature and energies as a real boundary.

How — Keep tools in `pyunitwizard.dialects.cf`, separate from core forms and
session parser selection. Use optional actual cf-units 3.3.1 / UDUNITS for
explicitly negotiated spellings. Import values with an explicit computing target;
validate exported spellings against dimensions, scale and offset, using the
existing computing registry's SI basis and provider conversions. Never infer CF
semantics by replacing Pint unit names. Keep provider imports deferred through
DepDigest. Validate supported named products/integer powers; refuse arbitrary
numeric scale/offset syntax, logarithmic units and unknown/no-unit sentinels.

Why — HDF5 requires labels that describe the unchanged stored numbers. A known
spelling is insufficient if definitions differ. CF temperature metadata must
also distinguish on-scale values from differences, including Kelvin.

Scope — Physical units only. Calendar/time-origin coordinates, full CF dataset
conformance, standard names, geographic angle semantics, UCUM/QUDT/ASDF and
new record schemas are outside this implementation. Require explicit supported
`units_metadata` for temperature; unknown semantics are refused. Do not change
session defaults or install a mandatory dependency.

Acceptance — Actual provider installation; H5MSM-derived length/time/velocity/
B-factor/temperature/energy cases; compound and affine/difference behavior;
refuse mismatched labels, unknown/calendar/arbitrary syntax and definition drift;
lazy-import/absence diagnostics, public docstrings, baseline and optional
matrix, installed-package tests outside checkout. Qualification preserves exact
producer identities and names coverage debt #107 independently.

Sources — [CF physical units and temperature semantics](https://cfconventions.org/cf-conventions/cf-conventions.html#units),
[cf-units public Unit operations](https://cf-units.readthedocs.io/en/stable/unit.html).
