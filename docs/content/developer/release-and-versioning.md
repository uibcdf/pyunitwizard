# Release and Versioning

PyUnitWizard tags use numeric versions without `v` prefix.

## Release path to 1.0.0

Current path is tracked in:

- `devguide/roadmap.md`
- `devguide/compatibility_matrix.md`
- `devguide/release_0.19.x_rc_checklist.md`
- `devguide/release_1.0.0_checklist.md`

Current policy:

- `0.19.x` is a historical checkpoint line.
- `0.20.x` is interoperability expansion (NumPy/Pandas/Matplotlib hardening).
- `0.21.x` is the active RC consolidation line.
- `1.0.0` is created only after the `0.21.x` RC closure criteria are met.

## Pre-release checks

1. `pytest -q` passes.
2. `make -C docs html` passes.
3. `release_gates` workflow is green for candidate commit.
4. Docs reflect actual runtime and supported Python versions.
5. Performance baseline snapshot is refreshed for the RC line.

## Practical release flow

1. Finalize scope and docs updates.
2. Run local gates.
3. Push coherent commits to `main`.
4. Create and push numeric tag.
5. Validate post-tag CI and package publication.
