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
cd devtools/conda-envs
python create_conda_env.py -n pyunitwizard-docs -p 3.12 docs_env.yaml # adjust Python version as needed
conda activate pyunitwizard-docs
```


Or if you already have the environment, is sufficient to pick up new dependencies if any were added:

```bash
conda activate pyunitwizard-docs
cd devtools/conda-envs
python update_conda_env.py docs_env.yaml
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

After every run:

1. Inspect `.nbconvert.log` files for errors. Fix issues and rerun as needed.
2. Remove `.nbconvert.log` files before committing—they are build artifacts.
3. Stage updated notebooks **together with** their `.nbconvert.last_run` companions.

## Cleaning Autosummary Output

Whenever the public API changes, clear obsolete autosummary trees to avoid stale reference pages:

```bash
python docs/clean_api.py
```

Run the command after a docs build that touches API pages, or before committing
when you notice outdated files under `docs/api/autosummary/`.

## Building the Docs Locally

Sphinx builds can be triggered with the provided Makefile or directly via `sphinx-build`.

```bash
# Recommended: uses configuration from docs/Makefile
(cd docs && make html)

# Equivalent explicit invocation
sphinx-build -M html docs docs/_build
```

Common targets include:

- `make clean` – remove the `_build/` tree before a fresh build.
- `make html` – render the full site for local preview.

Open `docs/_build/html/index.html` in your browser to inspect the result. Never commit the `_build/` directory.

## Publishing to GitHub Pages

Documentation is published from the HTML output in `docs/_build/html`. The
default workflow relies on GitHub Actions
(`.github/workflows/sphinx_docs_to_gh_pages.yaml`), which automatically builds
and deploys the site whenever the main branch is updated. Manual publishing is
rarely needed, but when required:

1. Build the site locally (`make html`).
2. Push the rendered site to the `gh-pages` branch, for example:
   ```bash
   git subtree push --prefix docs/_build/html origin gh-pages
   ```
   Ensure the CI workflow is disabled or coordinated with maintainers before manual pushes.

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
