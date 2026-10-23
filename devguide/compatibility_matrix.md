# Sibling Compatibility Matrix

This matrix records the current 0.29.x sibling-library floors from
`pyproject.toml` and the Conda recipe. Earlier release lines retain their own
historical contracts. Exact installed pins and dependency closures are retained
in the [0.29.0 publication record](completed_proposals/release_0.29.0.md).

| Component | Minimum Version | Current role |
|---|---:|---|
| `argdigest` | `0.14.0` | required runtime dependency for owned argument validation and normalization |
| `depdigest` | `0.11.0` | required runtime dependency for optional backend governance |
| `smonitor` | `0.16.0` | required runtime dependency for diagnostics and catalog-backed signals |
| `ackredit` | `0.9.0` when enabled | optional portable executed-backend attribution; not a mandatory runtime dependency |

The optional prepared-credit/observer profile additionally qualifies public
Ackredit `0.10.1`; it does not raise the fallback floor. OpenFF `0.4.0` is
qualified on Python `3.12`–`3.14` with Pint `>=0.24,<0.26`; CF/HDF5 uses
cf-units `3.3.1` and h5py `3.16.0`. These optional interfaces remain provisional.

Published 0.29.0 (#128) additionally qualifies Zarr `3.1.6`, PyArrow
`25.0.0`, ucumvert `0.3.2` (Pint >=0.25), asdf `6.0.0` and asdf-astropy
`0.11.0` on Linux/macOS Python 3.11–3.14. Exact-source and original-file installed receipts are retained in
`evidence/release_0.29.0_source.json` and `evidence/release_0.29.0_installed.json`;
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
