# Release and Versioning

PyUnitWizard tags use numeric versions without `v` prefix.

## Release path to 1.0.0

Current path is tracked in:

- `devguide/roadmap.md`
- `devguide/release_1.0.0_checklist.md`

Current policy:

- `0.19.x` is the RC line used to observe stability in real usage.
- `1.0.0` is created only after the RC window closes without blocker issues.

## Pre-release checks

1. `pytest -q` passes.
2. `make -C docs html` passes.
3. `release_gates` workflow is green for candidate commit.
4. Docs reflect actual runtime and supported Python versions.

## Practical release flow

1. Finalize scope and docs updates.
2. Run local gates.
3. Push coherent commits to `main`.
4. Create and push numeric tag.
5. Validate post-tag CI and package publication.
