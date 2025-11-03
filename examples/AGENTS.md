# Examples

Always follow the repository-wide guidelines from the root `AGENTS.md` in
addition to the rules below.

## Scope
These instructions apply to every file under `examples/`, including `testlib/`
and `testlib2/`.

## Purpose
This directory hosts two intentionally minimal reference libraries that
demonstrate how PyUnitWizard can be embedded in external projects. They are
referenced from the documentation and should stay simple and dependency-free.

## Guidance
- Keep both libraries pedagogical: rely only on the Python standard library and
  PyUnitWizard, and avoid extra packaging metadata or CI hooks.
- Preserve the current public surface (`sum_quantities`, `get_form`,
  `libraries_loaded`, and the `box` helpers) so the documentation examples
  continue to work without edits.
- Maintain the contrast between the two packages: `testlib` uses relative
  imports while `testlib2` mirrors the same API with absolute imports.
- Configure PyUnitWizard exclusively through the `_pyunitwizard/__init__.py`
  modules. Do not load additional unit backends unless you also update the
  tutorials that describe them.
- If you rename files, functions, or change the directory layout, update every
  affected snippet in the documentation and any other
  pages/files that showcase these libraries such as `docs/content/user/In_Your_Library.ipynb`.

## Review Checklist
1. Import both packages in a Python shell and confirm that `libraries_loaded()` still reports the expected unit libraries.
2. Compare the documentation snippets with the updated files and synchronize any differences.
3. Ensure `examples/README.md` reflects new instructions or structural changes you introduce.

