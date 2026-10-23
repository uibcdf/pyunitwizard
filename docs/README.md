# PyUnitWizard Documentation Guide

This guide explains how the documentation project is organized and how to work
with it day-to-day—from setting up the environment to publishing updates on
GitHub Pages.

## Directory Layout

```
docs/
├── AGENTS.md                # Documentation-specific contribution rules
├── README.md                # This contributor quick-start
├── Makefile / make.bat      # Convenience wrappers for sphinx-build
├── clean_api.py             # Removes stale autosummary outputs
├── execute_notebooks.py     # Batch-executes notebooks & updates markers
├── content/                 # Narrative guides and tutorials (MyST + notebooks)
├── api/                     # Landing pages for API autosummary stubs
├── _static/                 # Custom CSS/JS and other static assets
├── _templates/              # Jinja templates consumed by Sphinx
├── bibliography.bib         # Shared citation database
└── ...
```

Notebooks typically live under `content/` and are tracked together with their
`.nbconvert.last_run` timestamp files. Anything generated during builds—such as
`_build/` or autosummary folders—is temporary and must be recreated locally
when needed.

## Environment Setup

The documentation toolchain is defined in `devtools/conda-envs/docs_env.yaml`.
Create (or update) the environment before running any docs-specific tasks:

```bash
# Run from the repository root. Supported Python versions are 3.11–3.14.
conda env create --name pyunitwizard-docs --file devtools/conda-envs/docs_env.yaml
conda activate pyunitwizard-docs
python -m pip install --no-deps --editable .
```


To update an existing environment after dependency changes:

```bash
conda env update --name pyunitwizard-docs --file devtools/conda-envs/docs_env.yaml
conda activate pyunitwizard-docs
python -m pip install --no-deps --editable .
python -m pip check
```

## Notebook Execution Workflow

Use `docs/execute_notebooks.py` to execute notebooks and refresh
`.nbconvert.last_run` markers. If there is no reason to re-execute all
notebooks, only run those you modified.

```bash
# Run all notebooks below docs/content/
python docs/execute_notebooks.py -r docs/content

# Force execution even when timestamps are current
python docs/execute_notebooks.py -r docs/content --force

# Limit to specific notebooks
python docs/execute_notebooks.py docs/content/.../tutorial1.ipynb
```

The command exits nonzero if any requested notebook fails or a supplied path
does not exist. It still processes the remaining notebooks, retains each
execution log and removes a failed notebook's success timestamp. Notebooks and
their useful logs remain caller-owned; inspect the failures before cleanup.

After every run:

1. Inspect `.nbconvert.log` files for errors. Fix issues and rerun as needed.
2. Remove `.nbconvert.log` files before committing—they are build artifacts.
3. Stage updated notebooks **together with** their `.nbconvert.last_run` companions.

## Cleaning Autosummary Output

Obsolete autosummary trees are cleared for you: `make html` removes them before
every build, so pages for symbols dropped from the public API cannot survive.
These stubs are generated artifacts and git ignores them.

To drop them without rebuilding the site:

```bash
make -C docs clean-api

# equivalent, and callable from any directory
python docs/clean_api.py
```

## Building the Docs Locally

Sphinx builds can be triggered with the provided Makefile or directly via `sphinx-build`.

```bash
# Recommended: removes stale autosummary stubs and builds docs/_build/index.html
make -C docs html

# Alternative Sphinx make mode: builds docs/_build/html/index.html
python docs/clean_api.py
sphinx-build -M html docs docs/_build
```

Common targets include:

- `make clean` – remove the `_build/` tree and generated autosummary stubs
  before a fresh build.
- `make clean-api` – remove only the generated autosummary stubs.
- `make html` – render the full site for local preview.

For `make -C docs html`, open `docs/_build/index.html`; for Sphinx `-M html`,
open `docs/_build/html/index.html`. The hosted action uses the latter layout.
Never commit the `_build/` directory. Cleanup targets apply to generated
resources owned by the current task; preserve other callers' useful outputs.

## Publishing to GitHub Pages

The workflow `.github/workflows/sphinx_docs_to_gh_pages.yaml` builds and
publishes to `gh-pages` on a stable GitHub Release (`release: released`) or
manual dispatch. A push to `main` alone does not publish documentation.
After reviewing and pushing a documentation update, an authorized maintainer
can dispatch it explicitly:

```bash
gh workflow run sphinx_docs_to_gh_pages.yaml --repo uibcdf/pyunitwizard --ref main
```

Inspect the run's source commit and successful build/deployment, then verify
the updated pages at <https://www.uibcdf.org/pyunitwizard/>. The generated
`gh-pages/README.md` records the source commit. A green build alone does not
prove that GitHub Pages has finished serving the new content. Prefer this
workflow to manually replacing the published branch.

## Version Control Expectations

- Track `.nbconvert.last_run` marker files alongside their notebooks.
- Exclude `_build/`, `.nbconvert.log`, and other transient outputs from commits.
- Regenerate autosummary content instead of hand-editing generated files.

## Pre-PR Checklist

Before opening a documentation pull request, confirm that you have:

- [ ] Rebuilt the docs locally (`make html`) and resolved warnings.
- [ ] Executed each modified notebook with `python docs/execute_notebooks.py` and cleaned up `.nbconvert.log` files.
- [ ] Staged updated notebooks together with their `.nbconvert.last_run` markers.
- [ ] Ensured `_build/` and other generated artifacts remain untracked.
- [ ] Updated navigation, toctrees, or cross-references affected by your changes.
- [ ] Documented any new dependencies or Sphinx extensions in the PR description.

Following these steps keeps the documentation consistent and the CI pipeline green for every contributor.
