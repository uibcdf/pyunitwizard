# Tags and Releases

PyUnitWizard uses numeric Git tags without `v` prefix (for example `0.18.1`).

## Baseline policy

- Pre-1.0 releases follow incremental stabilization.
- `0.19.x` is the formal release-candidate (RC) line and should remain open as a
  stability window before `1.0.0`.
- If RC closure criteria are still unmet, continue with `0.20.x` as an RC
  extension line.
- `1.0.0` is the stable milestone.
- If a tag was created by mistake, do not rewrite history; continue with the
  next correct numeric tag.

## Creating the next tag

From `main`, after CI/release gates are green:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
pytest -q
make -C docs html
# replace X.Y.Z with the next version
git tag X.Y.Z
git push origin main
git push origin X.Y.Z
```

## Release references

- `devguide/roadmap.md`
- `devguide/compatibility_matrix.md`
- `devguide/release_0.19.x_rc_checklist.md`
- `devguide/release_1.0.0_checklist.md`
- [GitHub Releases docs](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Git tagging reference](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
