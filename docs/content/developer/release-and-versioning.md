# Release and Versioning

PyUnitWizard tags use numeric versions without `v` prefix.
The public GitHub Release title is exactly `X.Y.Z`, matching its tag and
package version. Put descriptions in the release body. See the accepted
[release-title rule](https://github.com/uibcdf/pyunitwizard/blob/main/devguide/release_titles.md).

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
- `0.24.x`–`0.28.x` continue hardening, qualified interchange and optional providers.
- `0.28.1` is the current published checkpoint; its
  [publication record](https://github.com/uibcdf/pyunitwizard/blob/main/devguide/completed_proposals/release_0.28.1.md)
  retains the exact source, artifact and qualification evidence.
- `1.0.0` requires final scope approval and the final release checklist. The
  record, measurement, optional attribution and storage surfaces remain
  provisional until separately admitted.

## Pre-release checks

1. `python -m pytest --receptor=llm tests` passes.
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

When creating the GitHub Release, set the title explicitly, for example
`gh release create X.Y.Z --verify-tag --title X.Y.Z --notes-file RELEASE_NOTES`.
Replace placeholders only after the exact-candidate gates above pass. Do not
move an existing published tag or rebuild a previously qualified artifact.
