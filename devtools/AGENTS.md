# Devtools

Always follow the guidelines in the main AGENTS.md file in the root directory of the repository.

## Scope
The instructions in this file apply to everything under `devtools/`, including
subdirectories like `conda-build/` and `conda-envs/`. Always follow the
top-level `AGENTS.md` rules as well.

## Purpose and Components
This directory hosts development-support tooling: dependency management, Conda
environment scripts, packaging utilities, and operational guidance.

- `requirements.yaml` is the single source of truth for dependencies across the
  different profiles (setup, production, test, docs, development, and
  conda-build).

- `broadcast_requirements.py` propagates updates from `requirements.yaml` into
  `conda-build/meta.yaml` and the YAML files inside `conda-envs/`. Do not edit
  the generated files manually unless the script cannot cover a specific
  case—document any exception. Always do include the required packages and
  libraries in the file `requirements.yaml` and regenerate the derived files
  running this script.

- `conda-envs/` holds the derived YAML files together with
  `create_conda_env.py`/`update_conda_env.py`, which are used to create or
  refresh environments.

- `conda-build/` contains the Conda build recipe for the package.

- `start_dev_env.sh` automates creation/update of the development environment
  and installs the package in editable mode.

## Dependency and Environment Management
- When dependencies change, update `requirements.yaml`, then run `python
  devtools/broadcast_requirements.py` from the repository root (or `python
  broadcast_requirements.py` from inside `devtools/`) to synchronize the
  derived files. Commit all regenerated YAML files alongside
  `requirements.yaml`.

- Before promoting changes, validate them by creating a disposable environment
  with `python devtools/conda-envs/create_conda_env.py -n tmp-puw -p <version>
  devtools/conda-envs/<profile>_env.yaml`. Remove the temporary environment
  when finished.

- For an existing environment, run `python
  devtools/conda-envs/update_conda_env.py
  devtools/conda-envs/<profile>_env.yaml` from a shell where the environment is
  active, then confirm that `conda env export` matches expectations.

- Do report any issues with dependency resolution or environment creation as
  GitHub issues.

- Always report any change to dependencies in the relevant PR.

- Profiles names are `setup`, `production`, `test`, `docs`, `development`, and
  `conda-build`. In general, use `development` for day-to-day work, `test`
  for CI-related tasks, and `docs` for dependencies to build documentation.

## Python Scripts in devtools
- Maintain compatibility with Python 3.10–3.13 (>=3.10,<3.14), matching `pyproject.toml`.
- Use only the standard library and dependencies already declared in the
  development profile. If you need new packages, add them to
  `requirements.yaml` first and rebroadcast.
- Offer consistent CLI interfaces: rely on `argparse`, keep messages in
  English, and emit output that is automation-friendly. Document new flags in
  `README.md` and in the help mode of each script.

## Script `start_dev_env.sh`
- Preserve `set -euo pipefail`, auto-detection of the YAML profile, and the
  selection logic for conda/mamba/micromamba.
- Ensure `--mode print` remains a no-op that only prints instructions.
- Gate any additional steps (for example, installing extras) behind explicit
  flags and update the inline help (`print_help`).
- Keep the editable installation (`pip install --no-deps --editable .`) as the
  final step and adjust diagnostic output if the package list changes.

## Checklist Before Opening PRs Touching devtools
1. Run the relevant script or command with `--help` and/or `--mode print` to confirm the CLI still behaves as expected.
2. If dependencies were modified, create and update a test environment using the provided scripts to verify resolution.
3. Update the `devtools/` README when you add new workflows or dependencies.


