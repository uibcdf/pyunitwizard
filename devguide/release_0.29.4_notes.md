# PyUnitWizard 0.29.4

Published on 2026-11-11 UTC through GitHub and the public `uibcdf` Conda
channel, from original source `d9dd0261d7e1f43624f4dd9356830ab9b126bd14`.
[GitHub Release](https://github.com/uibcdf/pyunitwizard/releases/tag/0.29.4) ·
[Release qualification #150](https://github.com/uibcdf/pyunitwizard/issues/150)

NumPy object arrays of numeric rows have an explicit backend capability and
ownership contract. Direct factory construction retains numeric row buffers
in Pint, OpenMM, unyt and optional OpenFF. Pint, OpenMM and OpenFF support
scaling; unyt cannot natively scale populated row containers. Astropy refuses
this representation, including translation and empty outer object arrays.

Unsupported operations now raise `puw.UnsupportedRepresentationError`, a
`TypeError` subtype with catalog code `PUW-ERR-REP-001`, naming the backend
and operation and suggesting flat numeric values with CSR offsets or per-row
processing. Native unit-dimension errors and dense object scalar behavior
remain. QuantityRecord continues requiring numeric arrays.
[#148](https://github.com/uibcdf/pyunitwizard/issues/148)

Guards qualify unequal rows, equal-length object rows, empty rows, empty
outer shape, native-unit construction, parser selection, explicit scaling,
source immutability, row-buffer lifetime and compatible backend translations.
The optional OpenFF case qualifies unequal rows. Successful direct construction
shares numeric storage; callers needing isolation copy their rows first.
See the [backend contract](../docs/content/user/backend-coverage.md).

All 29 exact-source jobs and all 30 installed cells passed on Linux/macOS
arm64 with Python 3.11–3.14 (OpenFF 3.12–3.14). Installed reports contain
14,276 passing entries; 164 expected skips cover the older Ackredit prepared
API, strict JSON NaN and OpenFF outside its optional profile. Every required
row and prior regression guard executed.

Public file `pyunitwizard-0.29.4-py_0.tar.bz2` is 98,914 bytes, SHA-256
`72dfeb00132ec851b1913d4b5ceabb9426d835c7556d8ad227e9bd6723d170f9`.
Promotion retained the qualified digest. Independent public main-label/index
verification and clean public Linux/Python 3.14 receiving passed, including
126 tests, pip check and actual SDK origin controls. OpenFF was explicitly
deselected in that local receiving run and qualified in its six matrix cells.

Served installation, compatibility and backend documentation identifies
0.29.4 and the reviewed contract. Canonical-guide synchronization and client
receiving belong to [MolSysSuite #187](https://github.com/uibcdf/molsyssuite/issues/187).
The source snapshot is verified under [version DOI](https://doi.org/10.5281/zenodo.24128389).
[Complete publication record](completed_proposals/release_0.29.4.md)
