# Release and Versioning

PyUnitWizard tags use numeric versions without `v` prefix.

## Release path to 1.0.0

Current path is tracked in:

- `devguide/roadmap.md`
- `devguide/compatibility_matrix.md`
- `devguide/release_0.21.x_rc_checklist.md`
- `devguide/release_1.0.0_checklist.md`
- `devguide/minimum_quantity_protocol_contract.md`
- `devguide/frontend_transparent_mode_contract.md`

Current policy:

- `0.19.x` is a historical checkpoint line.
- `0.20.x` is interoperability expansion (NumPy/Pandas/Matplotlib hardening).
- `0.21.x` is the completed RC consolidation line.
- `0.22.x` and `0.23.x` contain post-RC performance and API hardening.
- `1.0.0` is created after current hardening and the final release checklist are complete.

## Pre-release checks

1. `python -m pytest -q` passes.
2. `make -C docs html` passes.
3. `release_gates` workflow is green for candidate commit.
4. The full Linux/macOS matrix and suite policy workflow are green at the
   same candidate commit.
5. Docs reflect actual runtime and supported Python versions.
6. When the committed Conda release plan selects `staged`, the exact
   candidate artifact has passed its clean installed-package matrix.
7. Performance baseline snapshot is refreshed when the release changes a
   measured RC performance contract.

## Practical release flow

1. Finalize scope and docs updates.
2. Run local gates.
3. Push coherent commits to `main`.
4. Follow the committed direct or staged Conda route in
   `devtools/conda-build/README.md`; stage and test before publication when
   the route requires it.
5. Create and push the numeric tag, then publish the stable GitHub Release
   only after the exact-commit gates pass.
6. For a staged release, promote the verified file without rebuilding.
   Independently validate the public package and its installability.
