# PyUnitWizard 0.29.1

Published [0.29.1](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.1)
on 2026-11-06 UTC through GitHub and the public `uibcdf` Conda channel.
Original source: `ab92f1e645dfdd291f76785795b0d15b6a8c1257`.
Publication owner: [#138](completed_proposals/release_0.29.1.md).

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
profile ranges are retained. All 29 required source jobs and all 30 installed
profiles passed for the original candidate and file. All 25 calorie guards
execute in every installed profile. Independent public main/index verification
and a clean public-channel receiving check passed; served docs show 0.29.1.

This release introduces no new record format or stable API admission.
Existing qrec/bundle contracts and provisional record/storage/dialect/attribution
status remain. A successful source test does not certify an installed archive,
an optional provider profile or consumer adoption. MolSysSuite coordinates
guide synchronization and owner receiving; published 0.29.0 history is retained.


The unchanged noarch file is `pyunitwizard-0.29.1-py_0.tar.bz2`, 96,418 bytes,
SHA-256 `5bdf9b137c8862f99fc26e6ea5aa6e2ecea5a46ee1dc5e71127565411fedbe27`.
Producer 42125299597/1, installed qualifier 42129616605/1 and promotion
42162820178/1 retain their separate identities. The public-only Linux/Python
3.14.10 installation passes 132 selected tests with one intentional JSON skip;
it does not replace the 30-cell pinned qualification. Complete receipts are
`evidence/release_0.29.1_2026-11-06.json` and the linked closure records.

Zenodo independently verifies the exact source snapshot:
[10.5281/zenodo.23995546](https://doi.org/10.5281/zenodo.23995546).
That coverage does not include the Conda artifact. Publication and canonical-guide
receiving are communicated in [MolSysSuite #172](https://github.com/uibcdf/molsyssuite/issues/172);
client synchronization and installed adoption remain with the receiving owners.
