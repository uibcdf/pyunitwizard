# Sibling Compatibility Matrix

This matrix records the current 0.29.x sibling-library floors from
`pyproject.toml` and the Conda recipe. Earlier release lines retain their own
historical contracts. Exact installed pins and dependency closures are retained
in the [0.29.1 publication record](completed_proposals/release_0.29.1.md).

Published 0.29.1 (#134/#138) delivers the explicit inclusive NumPy/Pint
minimums below. Published 0.29.0 metadata is preserved.
The exact numerical-baseline and older-Pint refusal evidence is retained in
`evidence/runtime_dependency_floors_2026-11-05.json`.

| Component | Minimum Version | Current role |
|---|---:|---|
| `numpy` | `1.23.5` | dtype, immutable buffers, broadcasting, tagged/empty arrays and numerical record operations on the supported Python 3.11 baseline |
| `pint` | `0.25` | registry translation and CODATA-2022 definitions required to reproduce published qrec vectors |
| `argdigest` | `0.14.0` | required runtime dependency for owned argument validation and normalization |
| `depdigest` | `0.11.0` | required runtime dependency for optional backend governance |
| `smonitor` | `0.16.0` | required runtime dependency for diagnostics and catalog-backed signals |
| `ackredit` | `0.9.0` when enabled | optional portable executed-backend attribution; not a mandatory runtime dependency |

The optional prepared-credit/observer profile additionally qualifies public
Ackredit `0.10.1`; it does not raise the fallback floor. OpenFF `0.4.0` is
qualified on Python `3.12`–`3.14`; published 0.29.1 uses Pint `>=0.25,<0.26`.
The upper limit is OpenFF 0.4.0's provider restriction, not a general Pint cap. CF/HDF5 uses
cf-units `3.3.1` and h5py `3.16.0`. These optional interfaces remain provisional.

Published 0.29.1 (#138) additionally qualifies Zarr `3.1.6`, PyArrow
`25.0.0`, ucumvert `0.3.2` (Pint >=0.25), asdf `6.0.0` and asdf-astropy
`0.11.0` on Linux/macOS Python 3.11–3.14. Exact-source and original-file installed receipts are retained in
`evidence/release_0.29.1_source.json` and `evidence/release_0.29.1_installed.json`;
all dependency closures and case classifications are retained alongside them. The offline QUDT/UO resource is
part of the required artifact; runtime use does not require RDF/UCUM/Astropy.

## Policy

- Floors and optional qualification versions are separate from preferred pins.
- Required runtime dependencies are NumPy, Pint, SMonitor, DepDigest and ArgDigest.
- Baseline support covers Python `>=3.11,<3.15` on Linux/macOS arm64; optional
  provider profiles retain their separately qualified limits.
- Any matrix change must be reflected in:
  - this file,
  - release notes for the affected tag,
  - affected exact-source and installed qualification evidence.
- Before `1.0.0`, matrix floors must be validated in clean environments and in
  local sibling workflows (`../argdigest`, `../depdigest`, `../smonitor`).
