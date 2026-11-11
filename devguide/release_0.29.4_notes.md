# PyUnitWizard 0.29.4

Release qualification is in progress under
[#150](https://github.com/uibcdf/pyunitwizard/issues/150). No publication is
claimed by this preparation record.

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
