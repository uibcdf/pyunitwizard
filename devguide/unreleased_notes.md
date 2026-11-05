# Unreleased source maintenance

These changes follow published 0.29.0. No next version/tag, new Conda file,
public installation or client migration is implied by their source delivery.

- #137: Astropy construction, scalar parsing, target units and cross-backend
  conversions accept native thermochemical cal/calorie/kcal/kilocalorie, including
  kcal/mol. Native activation is scoped; aliases are checked before activation
  so a failing native context constructor cannot leak registry state. Conflicting
  definitions receive `PUW-ERR-UNIT-001`. All sixteen input/default combinations
  are guarded. Native registry contexts remain process-wide, and concurrent
  application-owned changes need external serialization. Future installed
  profiles refuse absent/skipped calorie cases. Provider issue:
  `astropy/astropy#20790`.
- #134: NumPy >=1.23.5 is the deliberately tested Python 3.11 numerical baseline;
  Pint >=0.25 preserves the CODATA-2022 definitions in canonical qrec vectors.
  The older Pint 0.24.4 control fails exact dalton-vector reproduction. Optional
  providers remain optional; OpenFF 0.4.0 retains its actual Pint <0.26 limit,
  giving an effective >=0.25,<0.26 source profile.
- #135: distribution metadata explicitly records `MIT AND CC-BY-4.0` for the
  existing MIT implementation and separately licensed derived QUDT/UO catalogue.
  Original copyright/notice bytes are preserved. PEP 639 build routes require
  Setuptools >=77.0.3 with versioningit >=3.0. Real wheel, sdist and rebuilt-wheel
  notice guards pass on current tools and the deliberately selected minimum.
- #136: owned build/upload and exact-file promotion use provider v2.3.0 at
  `87c70b1443d5f22d738ee3ddf812bdbe0152f6c2`. The noarch .tar.bz2 format,
  source/file/digest gates and producer receipts remain; native conversion,
  force/overwrite and the optional provider GitHub Release creator stay disabled.
  Provider title limitation: `uibcdf/action-build-and-upload-conda-packages#53`.

The complete local source runtime suite passes 1,007 cases, with two unavailable
Zarr-dependent case skips and the existing strict-JSON/NaN case skip. JUnit
also retains five optional module-collection skips (CF, UCUM, ASDF, HDF5 and
Zarr), eight skipped entries total; no complete optional matrix is claimed. Separate final workflow
controls exercise missing/skipped installed calorie cases. Minimum numerical,
license/build and simulated provider-operation evidence has its own retained
scope; none certifies a new full installed OS/Python matrix. The public 0.29.0
release, original source, producer, bytes/digest and historical receipts remain.
Before publication, choose a new release plan and execute every applicable exact
candidate, installed-artifact and independent public gate. MolSysSuite owns
canonical-guide distribution and consumer receiving under #127/#137/#162/#87.
