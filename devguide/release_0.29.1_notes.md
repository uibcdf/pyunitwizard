# PyUnitWizard 0.29.1

Draft maintenance-release notes. Preparation is tracked in
[release #138](https://github.com/uibcdf/pyunitwizard/issues/138); this version
has not been published. Candidate source, archive and installed qualification
remain pending.

- Astropy quantities, target units, parsing and cross-backend conversion support
  thermochemical cal/calorie/kcal/kilocalorie, including kcal/mol. In all sixteen
  Pint/OpenMM/unyt/Astropy source/default combinations, 12.552 kJ/mol converts
  to 3 kcal/mol. Caller policy and native registry state are preserved (#137).
- Conflicting calorie aliases or registry definitions raise the catalogued
  `UnitDefinitionError` (`PUW-ERR-UNIT-001`). Alias validation occurs before
  native activation to avoid the failed-context leak reported in
  [Astropy #20790](https://github.com/astropy/astropy/issues/20790). The adapter
  serializes its own writers; applications concurrently changing Astropy's
  process-wide registry still need external serialization.
- Required runtime floors are NumPy >=1.23.5 and Pint >=0.25. The deliberately
  tested older numerical profile uses Python 3.11, NumPy 1.23.5 and Pint 0.25;
  Pint's floor preserves CODATA-2022 dalton definitions in canonical records.
  The OpenFF 0.4.0 profile retains its actual Pint <0.26 restriction (#134).
- Distribution metadata records existing `MIT AND CC-BY-4.0` licensing, with
  the original MIT implementation license and derived QUDT/UO catalogue notice
  included in wheels and sdists. Build routes require Setuptools >=77.0.3 and
  versioningit >=3.0; original notices and copyright are unchanged (#135).
- The owned Conda build/upload and exact-file promotion routes use reviewed
  provider v2.3.0 while preserving one noarch .tar.bz2 file, native recipe
  tests, exact source/file/digest checks and installed/public gates (#136).

The existing Linux/macOS arm64 and Python 3.11–3.14 support targets and optional
profile ranges are retained. Their qualification for this release requires its
actual candidate evidence. The new installed gate rejects absent or skipped
calorie regressions in every profile.

This release plan introduces no new record format or stable API admission.
Existing qrec/bundle contracts and provisional record/storage/dialect/attribution
status remain. A successful source test does not certify an installed archive,
an optional provider profile or consumer adoption. MolSysSuite coordinates
guide synchronization and owner receiving; published 0.29.0 history is retained.
