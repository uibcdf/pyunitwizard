# PyUnitWizard 0.28.0

PyUnitWizard 0.28.0 expands verified quantity interchange and optional scientific
interoperability. Existing computing forms and the `qrec/0.3` wire format remain
compatible. New interfaces and formats described below remain **provisional**;
this release does not promote them to stable 1.0 contracts.

## Records and stated uncertainty

- QuantityRecord numeric snapshots remain immutable even when a caller attempts
  to re-enable NumPy write access. Empty multidimensional arrays round-trip
  through base64 without losing shape, dtype or their seal (#100, #109).
- `MeasurementRecord` stores an explicitly stated scalar value with SD, SEM,
  unspecified half-width or confidence-interval bounds. Its separate
  `qrec-measurement/0.1` envelope preserves association, sample count and confidence
  level when supplied. Temperature half-widths are differences and interval
  bounds are points. The library does not estimate or propagate uncertainty
  (#90).
- QuantityRecord, QuantityRecordBundle, `qrec/0.3` and MeasurementRecord remain
  provisional. Completed MVP and consumer tests do not imply admission to 1.0
  (#82, #83).

## Optional interoperability

- The `openff.units` computing form bridges actual OpenFF quantities through
  verified unit definitions, including arrays, OpenMM vectors, foreign Pint
  registries and sealed records. The qualified provider is **openff-units 0.4.0**
  from conda-forge, on **Python 3.12–3.14**, with **Pint >=0.24,<0.26**. Python 3.11
  retains baseline support and reports the provider's installation limitation
  (#86).
- `pyunitwizard.dialects.cf` validates an explicitly negotiated CF unit spelling
  and converts numeric values through **cf-units 3.3.1 / UDUNITS**. It checks
  physical dimensions, scale and offset, and requires explicit point/difference
  temperature metadata. Unknown units, calendar coordinates, time origins and
  unsupported spellings are refused. This bounded tool does not certify an
  entire dataset against CF conventions (#108).
- `pyunitwizard.storage.hdf5` writes and verifies immutable numeric snapshots
  using optional **h5py 3.16.0** and cf-units. The separate **qrec-hdf5/0.1** binding
  checks dtype, shape, manifest, seals, CF metadata and reader expectations. A
  temperature read requires matching explicit `units_metadata`. Reads materialize
  and verify the entire array. Append, streaming, concurrent/crash transactions
  and adoption into MolSysMT's file format are outside this release (#101).
- OpenFF, CF and HDF5 providers remain optional and lazy. Their APIs and the
  HDF5 binding remain provisional; no mandatory provider dependency is added.

## Computing and attribution

- Compatible foreign Pint quantities are normalized without discarding their
  registry's meaning; incompatible definitions are refused. Array quantities
  round-trip through text.
- Automatic parser selection uses parser-capable forms; Astropy parsing also
  handles bare units (#95, #96).
- Runtime configuration validates and normalizes owned arguments with the
  published **ArgDigest >=0.14.0** contract. The dependency floor is reflected
  in the package and Conda recipe (#98).
- Optional executed-backend attribution and function citation declarations use
  **Ackredit >=0.9.0**. Executed-backend attribution remains opt-in and does not enable automatic
  import hooks. Function-observer and prepared-credit paths are provisional:
  the corresponding APIs are absent from the qualified public 0.9.0 provider,
  and their deferred tests do not count as executed qualification (#92, #94).

## Distribution and qualification

The public distribution route is the **uibcdf Conda channel**, with conda-forge
for third-party providers. Baseline and CF/HDF5 qualification covers Linux and
macOS arm64 with Python 3.11–3.14; OpenFF covers Python 3.12–3.14. Neither a
source checkout nor this GitHub Release establishes a public PyPI installation
route.

Release preparation and exact-candidate evidence are tracked in
[uibcdf/pyunitwizard#110](https://github.com/uibcdf/pyunitwizard/issues/110).
The release uses staging, tests the exact installed Conda archive, and promotes
the original verified bytes without rebuilding. Gate results, producer identity,
dependency closure, archive digest and public-install evidence are retained
there. Codecov upload debt is tracked independently in
[uibcdf/pyunitwizard#107](https://github.com/uibcdf/pyunitwizard/issues/107);
scientific test success must not be described as successful external ingestion.

## Publication identity

The original qualified source is `2d12b37ac8b20566afc82cb51eb67e98d762bc47`.
The original Conda archive is `pyunitwizard-0.28.0-py_1.tar.bz2`, SHA-256
`0fe6bde7f399db85a5cd764a803a222dc66a7d3f8a48ebd81dd67da90b00f69c`.
Producer 37284526657 and final installed qualification 37288810671 preserve
those exact bytes. All mandatory source and installed profiles passed, and
exact-source CI attempt 2 successfully uploaded coverage and test results to
Codecov. No release exception was used.

See the [pre-tag decision and executed evidence](https://github.com/uibcdf/pyunitwizard/issues/110#issuecomment-5991713724).
Promotion 37290090364 verifies the public main label and solver index. A clean
public-channel Linux/Python 3.14 installation verifies the exact digest and
executes record, measurement, CF and HDF5 success/refusal checks. Full receipts
and all 22 installed dependency closures are retained under `devguide/evidence/`.
