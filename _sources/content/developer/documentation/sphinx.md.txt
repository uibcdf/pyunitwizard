# Sphinx Documentation Workflow

PyUnitWizard documentation is built with Sphinx + MyST + myst-nb.

## Local build

```bash
make -C docs html
```

The generated site is written to `docs/_build/`.
Open `docs/_build/index.html`. The alternative command
`sphinx-build -M html docs docs/_build` writes to `docs/_build/html/`, as used
by the hosted action; clean stale autosummary stubs first with
`python docs/clean_api.py` when using that command directly.

## Publication

The documentation workflow runs on stable GitHub Releases and manual dispatch;
pushing `main` alone does not publish the site. Authorized maintainers can run:

```bash
gh workflow run sphinx_docs_to_gh_pages.yaml --repo uibcdf/pyunitwizard --ref main
```

Check the exact source commit, successful deployment and updated served pages.
See the [documentation contributor guide](https://github.com/uibcdf/pyunitwizard/blob/main/docs/README.md)
for environment setup, output layouts and publication verification.

## Contribution expectations

When you update behavior or public contracts:
- update the relevant User and/or Developer pages,
- ensure links and toctrees remain valid,
- keep narrative structure explicit (guided, not fragmentary).

## Common pitfalls

- orphan pages not included in any toctree,
- stale examples that no longer match runtime behavior,
- notebook content copied from unrelated projects.

Run documentation build locally before opening a PR.
