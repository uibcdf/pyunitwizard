# Docs

Always follow the repository-wide guidelines from the root `AGENTS.md` in addition to the rules
below.

## Scope
These instructions apply to every file under `docs/`, including the `content/`,
`api/`, `_static/`, `_templates/`, notebooks, and helper scripts.

## Purpose and Layout
The documentation is built with Sphinx and mixes MyST Markdown,
reStructuredText, and Jupyter notebooks. Key areas:

- `index.ipynb` is the main entry point referenced by the Sphinx toctree.
- `content/` holds author-maintained guides:
  - `about/` – project overview and installation notes.
  - `user/` – end-user tutorials stored as notebooks plus supporting Markdown.
  - `developer/` – contributor guides and conventions.
  - `showcase/` – highlight notebooks and quick-start examples.
- `api/` contains the API landing pages for users and developers. Autosummary
  will create `autosummary/` subfolders under these trees; remove stale
  directories with `python docs/clean_api.py` when the API surface changes.
- `_static/` and `_templates/` provide static assets and Jinja templates referenced by `conf.py`.
- `bibliography.bib` stores citation metadata shared across the site.
- `execute_notebooks.py` automates notebook execution and `.nbconvert.last_run`
  timestamps; `clean_api.py` trims generated autosummary artifacts.
- `Makefile`/`make.bat` wrap common Sphinx build targets such as `make html`.

## Authoring Guidelines
- Write all content in English and keep tone consistent with the rest of the
  documentation.
- Prefer MyST Markdown (`.md`) for narrative pages and Jupyter notebooks
  (`.ipynb`) for executable tutorials. reStructuredText (`.rst`) is still
  accepted for sections that need it but avoid it possible.
- Keep notebooks lightweight: avoid long-running cells, hide credentials, and
  use deterministic seeds when random behavior is required.
- When editing notebooks, re-run them so outputs match inputs and save the
  notebook in a clean state (no stray debugging cells, collapsed metadata
  preserved).
- Use Sphinx roles/directives already enabled in `conf.py` (autosummary,
  autodoc, todo, math, tabs, design components, bibliography, etc.). Avoid
  introducing new extensions without coordinating updates to `conf.py` and the
  docs dependency profile. Always report new extension needs in PR descriptions.
- Reference reusable assets from `_static/` and register new CSS/JS via
  `conf.py` instead of hardcoding HTML in pages.
- Place cross-references in MyST/RestructuredText syntax (e.g., `{ref}` or
  `:ref:`) and add bibliography citations via `cite` roles pointing to
  `bibliography.bib`.
- Do not commit Sphinx build outputs (`_build/`) or `.nbconvert.log` files. The
  `.nbconvert.last_run` markers should remain under version control to skip
  unnecessary notebook executions.

## Notebook Execution Workflow
1. Activate the docs environment (see the docs dependency profile in
   `devtools/requirements.yaml`) before running notebooks so Pint, OpenMM,
   Astropy, Unyt, and Sphinx integrations resolve correctly.
2. Execute updated notebooks with `python docs/execute_notebooks.py -r
   docs/content` (or target a narrower path). Use `--force` when you need to
   refresh timestamps even without content changes.
3. Inspect the generated `.nbconvert.log` files for failures; fix issues and
   rerun until logs show success. Delete log files before committing.
4. Commit the updated notebooks together with their `.nbconvert.last_run`
   companions so CI and other contributors can detect which notebooks are
   current.

## Building and Previewing
- Use `make html` from inside `docs/` for local previews. The resulting site
  lives in `_build/html`; open `index.html` in a browser to inspect the output.
  Clean prior builds with `make clean` if assets look stale.
- Alternatively, call `sphinx-build -M html . _build` when scripting builds
  (mirrors the Makefile target).
- When the API reference changes, run Sphinx with autosummary enabled (default)
  and, afterwards, invoke `python docs/clean_api.py` to remove outdated
  autosummary directories before regenerating them on the next build.
- The documentation is configured for the `pydata_sphinx_theme`, myst-nb, and
  notebook execution mode `"off"`—keep these defaults unless you have buy-in
  from maintainers.

## Publishing
- The docs site is hosted on GitHub Pages via the `gh-pages` branch and
  automatically built by the GitHub Action in workflow file: `.github/workflows/sphinx_docs_to_gh_pages.yaml`.
- GitHub Pages deployments expect the HTML output under `_build/html`; push
  updates with `git subtree push --prefix docs/_build/html origin gh-pages` if
  you are maintaining the pages manually -though the Action should handle this
  for you, unless it is explicitly disabled and you have specific orders to
  do so from the maintainers.

## Review Checklist for Docs Changes
Before opening a PR that touches `docs/`:

1. Rebuild the docs (`make html`) and confirm warnings are addressed.
2. Run `python docs/execute_notebooks.py` for any notebook you touched and verify timestamps/logs.
3. Ensure no generated artifacts (`_build/`, `.nbconvert.log`, temporary autosummary directories) are staged.
4. Update or add cross-references, navigation entries, and toctrees where
   relevant (e.g., `index.ipynb`, section `index.md` files).
5. If you add dependencies or Sphinx extensions, sync
   `devtools/requirements.yaml` via the broadcast workflow and mention the
   requirement in the PR description.

