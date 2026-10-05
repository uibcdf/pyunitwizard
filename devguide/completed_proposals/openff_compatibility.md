---
summary: Optional OpenFF registry interoperability with verified unit definitions.
issue: uibcdf/pyunitwizard#86
status: resolved
opened: 2026-10-04
closed: 2026-10-05
verification: measured
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

## Qualification progress — 2026-10-05

Runtime source e7ecdb8 passes the local optional full suite (775 passed/12
skips) and base full suite (755 passed/13 skips, including the absent optional
module). Its normally installed wheel in a fresh actual Conda OpenFF 0.4.0 /
Pint 0.25.3 environment passes 22 copied guards outside checkout and pip check.
Existing frozen vectors, 47 measurement cases, Ruff and docs continue passing.

Initial optional run 37271566721 fails collection on all six cells: the pytest
executable does not include checkout root for imports of the repository's
`tests` helper namespace. Use `python -m pytest` for the full source suite;
installed canaries remain in an independent temporary directory. No scientific
assertion is waived. Qualified runtime source and later workflow recovery retain
their separate identities. Coverage ingestion remains independently #107.

## Resolution — 2026-10-05

The optional `openff.units` form is implemented at runtime source
`e7ecdb86dc11082bbc3766dbfbc979210f8e44db`. Its adapter remains lazy;
PyUnitWizard's baseline runtime requirements and Python 3.11 support are retained.
The supported OpenFF 0.4.0 distribution is conda-forge, with Python 3.12–3.14
and Pint >=0.24,<0.26. Documentation names this bounded optional installation
rather than a broken PyPI extra.

The existing reusable Pint registry verifier now accepts an explicit destination
registry. OpenFF adapters reuse its dimensions, base names, scale and affine-offset
checks before conversion and same-form fast paths. The named guard rejects a
foreign OpenFF registry that doubles nanometer, including record conversion;
companion cases reject changed Pint definitions on entering OpenFF. Actual-provider
cases cover scalar/n-D/dtype/compound/affine round trips, array strings, registry
arithmetic, native OpenMM/Vec3 parity and the explicit unsealed val/unit boundary.
Raw nodes require finite values and reader expectations before conversion to a
field-bound sealed record; qrec/0.3 and qrec-bundle/0.3 remain unchanged.

Baseline matrix 37271569329 passes all eight Linux/macOS Python 3.11–3.14
cells with 753 passed/14 skips each. Release gates 37271572072 pass four
full suites with those counts, four 16-case smokes, packaging and docs. These
retain the original runtime source identity.

Workflow-only recovery source `778964021d07169f7327c674cadfbc4c2b6a23ac`
passes optional matrix 37272537988: all six Linux/macOS Python 3.12–3.14
cells execute 773 passed/14 skips with actual OpenFF 0.4.0/Pint 0.25.3.
Each normally installed consumer then passes 22 copied guards outside checkout,
with site-packages origin, versions and successful pip check recorded. No assertion
or scientific scope was removed to recover the collection failure.

The original runtime wheel `pyunitwizard-0.27.0+70.ge7ecdb8-py3-none-any.whl`
retains SHA-256 `92f52fd8c5de1fbd7787180983c33535809e2fabe6c5ad78fe33141b411d39df`.
In a fresh actual Conda solve it passes 22 outside-checkout guards and pip check;
all 81 shipped package files are byte-identical to the original wheel. Hosted
recovery consumers have their distinct producer/version identities. Receipt:
`devguide/evidence/openff_interop_2026-10-05.json`.

Routine recovery CI 37272521807 executes 753 passed/14 skips and style checks,
but coverage ingestion still fails after retries. Policy 37272522434 passes.
Missing successful coverage/test-result upload evidence remains owned by #107;
recover it by executing and inspecting exact-head CI after service recovery.
This closure resolves the bounded interoperability implementation. It does not
claim aggregate CI green, Windows qualification, optional Ackredit observer
coverage, a new public release, or adoption by a consumer. Other formats and
unit dialects remain independently owned by #85.
