# Tags and releases

This project uses Git tags without `v` prefix (`0.18.0`, `0.19.0`, `1.0.0`).

## Current baseline

- Active release line before stable: `0.17.x` -> `0.18.x` -> `0.19.x`.
- Stable target: `1.0.0`.
- Historical note: existing `1.0.0` tag was created by mistake and must not be used as baseline for release progression.

## How to create the next tag

From `main`, after release gates are green:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
pytest -q
git tag 0.18.0
git push origin main
git push origin 0.18.0
```

If tag already exists remotely, create the next correct tag and do not rewrite history.

## References

- https://docs.github.com/en/github/administering-a-repository/releasing-projects-on-github/about-releases
- https://docs.github.com/en/github/administering-a-repository/releasing-projects-on-github/managing-releases-in-a-repository
- https://git-scm.com/book/en/v2/Git-Basics-Tagging
