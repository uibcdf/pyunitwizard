# Compatibility Matrix

The current 0.28.x baseline supports Python `>=3.11,<3.15` on Linux and
macOS arm64. NumPy and Pint are required, together with these infrastructure
dependencies declared in `pyproject.toml`:

| Component | Minimum Version | Role |
|---|---:|---|
| `argdigest` | `0.14.0` | owned runtime argument validation and normalization |
| `depdigest` | `0.11.0` | optional backend governance |
| `smonitor` | `0.16.0` | diagnostics and catalog-backed signals |
| `ackredit` (optional) | `0.9.0` when enabled | portable executed-backend attribution |

The optional prepared-credit/observer profile additionally qualifies public
Ackredit `0.10.1`; this does not raise the portable fallback floor or admit a
newer provider merely because its guide has been delivered. OpenFF `0.4.0`
is qualified on Python `3.12`–`3.14` with Pint `>=0.24,<0.26`; CF/HDF5 uses
cf-units `3.3.1` and h5py `3.16.0`. These optional interfaces remain provisional.

Exact installed pins, files and dependency closures belong to the
[0.28.1 publication record](https://github.com/uibcdf/pyunitwizard/blob/main/devguide/completed_proposals/release_0.28.1.md).

## Operational rules

When this matrix changes:

1. Update `devguide/compatibility_matrix.md`.
2. Update release notes for the affected tag.
3. Refresh affected exact-source and installed qualification evidence, including
   clean environments and applicable sibling workflows before `1.0.0`.

This matrix is a compatibility floor. It does not imply pinning these exact
versions in downstream environments.
