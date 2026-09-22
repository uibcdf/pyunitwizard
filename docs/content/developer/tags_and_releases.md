# Tags and Releases

PyUnitWizard uses numeric Git tags without `v` prefix (for example `0.18.1`).

## Baseline policy

- Pre-1.0 releases follow incremental stabilization.
- `0.19.x` is a historical checkpoint line.
- `0.20.x` is the interoperability expansion line.
- `0.21.x` is the completed RC consolidation line.
- `0.22.x` and `0.23.x` are post-RC hardening lines before `1.0.0`.
- `1.0.0` is the stable milestone.
- If a tag was created by mistake, do not rewrite history; continue with the
  next correct numeric tag.

## Creating the next tag

From `main`, after the full matrix, policy, release gates, and any required
staged installed-package tests are green at the same commit:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
python -m pytest --receptor=llm -n 12 -q
make -C docs html
# replace X.Y.Z with the next version
git tag X.Y.Z
git push origin main
git push origin X.Y.Z
```

For a staged Conda route, publishing the GitHub Release verifies the
committed plan but does not rebuild the package. Promote the digest-verified
staged file afterward; see `devtools/conda-build/README.md`. A direct route
builds once on the stable release event, after its registry preflight.

## Release references

- `devguide/roadmap.md`
- `devguide/compatibility_matrix.md`
- `devguide/release_0.21.x_rc_checklist.md`
- `devguide/release_1.0.0_checklist.md`
- [GitHub Releases docs](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Git tagging reference](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
