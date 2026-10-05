---
summary: Bounded CF/UDUNITS unit dialect for verified HDF5 quantities.
issue: uibcdf/pyunitwizard#108
status: resolved
opened: 2026-10-05
closed: 2026-10-05
verification: measured
area: [units, interoperability]
guard: tests/dialects/test_cf.py::test_export_refuses_changed_scale_dimensions_and_real_definition_drift
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

## Resolution and qualification — 2026-10-05

Implemented at initial source `381ca5a43801fff488bed9cd0fba13f8de3a3c7e`,
then strengthened the temperature reader handshake at final source
`d4c6089be2f4b8d4c975f31238209ce7348ee4c0`. The final optional eight-cell
Linux/macOS Python 3.11–3.14 matrix 37277539184 passes 822 tests/14 skips
per cell with actual cf-units 3.3.1/h5py 3.16.0. All eight normally installed
consumers pass 69 copied guards outside checkout and pip check; site-packages
origins and versions are printed in native logs. Local final full suite passes
824/12; the baseline without CF passes 764/12 with the integration modules
unexecuted at collection and separate absence guards active. Ruff, docs and
reporting guards pass.

The final normal wheel `pyunitwizard-0.27.0+75.gd4c6089-py3-none-any.whl`
has SHA-256 `0d77f6a499e62d43c9d475274e58d2a5971d2c37f2b4c1ca555b7e2709835746`.
Installed in an actual Conda-solved environment, it passes 69 outside-checkout
guards and pip check; all 85 shipped package files match the original wheel.
The earlier wheel and matrix keep their original identity, without being
relabelled as the strengthened reader.

Initial baseline eight-cell matrix 37276227352 passes 762/14 per cell;
release gates 37276231080 pass four full suites with those counts, four 16-case
smokes, packaging and docs. The final change affects only the optional reader,
its tests and guidance: baseline scientific code, core tests, dependency inputs,
metadata and workflows remain unchanged. Final-source routine CI 37277485846
executes 762/14 and style checks but still fails Codecov ingestion; policy
37277486550 passes. Missing upload evidence stays owned by #107, to recover
through successful exact-head coverage/test-result execution after service recovery.

Receipt: `devguide/evidence/cf_hdf5_interop_2026-10-05.json`. Original qrec/0.3
bytes and seals remain unchanged. No aggregate CI green, new public release,
calendar/full-CF conformance, streaming/append or consumer adoption is claimed.

The named guard rejects wrong dimensions, changed scale and the actual
UDUNITS u/Pint dalton drift; CF labels are never guessed from a display formatter.
Provider-backed cases cover the H5MSM physical units, arrays, compounds, Celsius
points/differences, Kelvin semantics, explicit computing targets and session-form
selection. Unsupported syntax and meanings are refused. Storage consumers reuse
these documented operations rather than carrying their own conversion table.
