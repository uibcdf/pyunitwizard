# PyUnitWizard

A Python Units Wizard that streamlines work with physical quantities.

## What is this AGENTS.md file for?

This file defines how automated agents and human contributors should work with
the PyUnitWizard repository. It provides an overview of the project — including
its purpose, description, and structure — and sets the main rules for coding,
testing, documentation, and contributions to ensure safe and consistent
collaboration.

## Purpose of the project

PyUnitWizard is a Python library that standardizes and simplifies the use of
physical units across different unit systems. Its main goal is to act as a
bridge between popular unit libraries — currently pint, unyt, openmm.unit, and
astropy.units — enabling seamless conversion between them.

By integrating PyUnitWizard, scientific libraries can let users choose how
units are represented and handled without changing their workflows. This
ensures that outputs can be used as inputs in other tools regardless of the
unit system, making scientific pipelines compatible, flexible, and
interoperable.

## Project Overview and Structure

PyUnitWizard provides a unified interface to work with physical units and
convert between different unit libraries. Its modular design makes it easy to
integrate into scientific projects and ensures compatibility across diverse
workflows.

The design philosophy is:
- **Composability:** small, reusable components.
- **Extensibility:** easy to add new unit systems, conversions, or APIs.
- **Robustness:** strict type checking and dimensional consistency.

### Repository Structure

The repository is organized into the following main directories and files:

- **AGENTS.md** – Main guidelines for automated agents (This same file).
- **CODE_OF_CONDUCT.md** – Community guidelines and expectations.
- **devtools/** – Development tools and scripts for installing and maintaining the project.
- **docs/** – Documentation files to be compiled with sphinx.
- **examples/** – Directory with example files to embed PyUnitWizard in a third scientific python library.
- **LICENSE** – License information.
- **logos/** – Project logos and branding assets.
- **MANIFEST.in** – Manifest file for packaging.
- **pyproject.toml** – Build system configuration.
- **pytest.ini** – Configuration for pytest.
- **pyunitwizard/** – Main source code directory containing the core modules.
- **README.md** – Main project overview and quick start guide for humans.
- **sandbox/** – Experimental code and developing notes.
- **setup.cfg** – Configuration file for setup tools.
- **tests/** – Unit and integration tests to be run with pytest.

#### devtools/

The `devtools/` directory contains scripts and configuration files to
facilitate installation, development, maintainance, and deployment of PyUnitWizard.
It includes tools for setting up development environments, managing dependencies,
and automating common tasks.

- **broadcast_requirements.py** – Script to synchronize required packages with the files in `conda-build/` and `conda-envs/`.
- **conda-build/** – Recipes for building conda packages.
- **conda-envs/** – Conda environment files for development, testing, production, setup...
- **README.md** – Instructions for using the development tools for humans.
- **README_pip.md** – Instructions to install PyUnitWizard with pip (this is a temporary file).
- **requirements.yaml** – Required packages in a format to be read by broadcast\_requirements.py.
- **start_dev.sh** – Script to set up a development environment with conda.

#### docs/

The `docs/` directory contains the source files for the project documentation.
It is structured to be built with Sphinx, with the Pydata Sphinx theme and using MyST.

- **api/** – Auto-generated API documentation.
- **bibliography.bib** – Bibliography file for references in documentation.
- **clean_api.py** – Script to clean up auto-generated API docs.
- **conf.py** – Sphinx configuration file.
- **content/** - Main documentation content in MyST markdown files and jupyter notebooks.


## Coding

This section outlines the coding standards and conventions followed in the PyUnitWizard project.

### General Conventions For New Contributors

### Code Style

- Follow PEP 8 style guide for Python code.
- Use `black` for code formatting.
- Use `isort` for import sorting.
- Use `flake8` for linting.
- Use `mypy` for type checking.
- Ensure code is clean, readable, and well-organized.
- Avoid deeply nested code and long functions. Break them into smaller, manageable pieces.
- Use meaningful variable and function names that convey their purpose.
- Avoid abbreviations in variable names.
- Maintain a consistent coding style throughout the codebase.

### Naming Conventions

### Docstrings

### Type Annotations

### Comments in the code

### Error Handling

### Exceptions

### Warnings

### Logging

### Security and Dependencies
- Only use packages listed in `requirements.txt` and `dev-requirements.txt`.
- Keep dependencies up to date and monitor they are available, necessary and pertinence.
- Avoid using deprecated or unmaintained packages.
- Regularly check for security vulnerabilities in dependencies using tools like `safety` or `bandit`.
- Follow best practices for handling sensitive data, such as using environment variables for secrets and avoiding hardcoding them in the codebase.
- Do not log sensitive information.
- Do not commit secrets, credentials, environment variables or sensitive information to version control.
- Do not report secretes, credentials, environment variables or sensitive information in issues or pull requests.

## Testing

## Documentation

## Version Control

## Contribution Guidelines

### Commit Messages

### Pull Request Guidelines

#### PR Checklist

- title: `feat(scope): short description`
- lint, type check, unit tests - all green before commit
- diff is small and focused. include a brief summary of what changed and why
- remove any excessive logs or comments before sending a PR
- Run pytest tests/ before finalizing a PR.
- Ensure all new and existing tests pass.
- Link relevant issues or tasks in the PR description.
- Title format: [Fix] Short description
- Include a one-line summary and a "Testing Done" section

## IA Agents Guidelines
- The user will provide a task.
- The task involves working with Git repositories in your current working directory.
- Wait for all terminal commands to be completed (or terminate them) before finishing.

### Citation Instructions

- If you browsed files or used terminal commands, you must add citations to the
  final response (not the body of the PR message) where relevant. Citations
  reference file paths and terminal outputs with the following formats:
  1) `【F:<file_path>†L<line_start>(-L<line_end>)?】`
  - File path citations must start with `F:`. `file_path` is the exact file
    path of the file relative to the root of the repository that contains the
    relevant text.
  - `line_start` is the 1-indexed start line number of the relevant output
    within that file.
  2) `【<chunk_id>†L<line_start>(-L<line_end>)?】`
  - Where `chunk_id` is the chunk_id of the terminal output, `line_start` and
    `line_end` are the 1-indexed start and end line numbers of the relevant
    output within that chunk.
- Line ends are optional, and if not provided, line end is the same as line
  start, so only 1 line is cited.
- Ensure that the line numbers are correct, and that the cited file paths or
  terminal outputs are directly relevant to the word or clause before the
  citation.
- Do not cite completely empty lines inside the chunk, only cite lines that
  have content.
- Only cite from file paths and terminal outputs, DO NOT cite from previous pr
  diffs and comments, nor cite git hashes as chunk ids.
- Use file path citations that reference any code changes, documentation or
  files, and use terminal citations only for relevant terminal output.
- Prefer file citations over terminal citations unless the terminal output is
  directly relevant to the clauses before the citation, i.e. clauses on test
  results.
- For PR creation tasks, use file citations when referring to code changes in
  the summary section of your final response, and terminal citations in the
  testing section.
- For question-answering tasks, you should only use terminal citations if you
  need to programmatically verify an answer (i.e. counting lines of code).
  Otherwise, use file citations.

### Git Instructions

- Use git to commit your changes.
- If pre-commit fails, fix issues and retry.
- Check git status to confirm your commit. You must leave your worktree in a clean state.
- Only committed code will be evaluated.
- Do not modify or amend existing commits. Create new commits instead.

### Test first mode
- when adding new features: write or update unit tests first, then code to green
- prefer component tests for UI state changes
- for regressions: add a failing test that reproduces the bug, then fix to green

### Programmatic Checks for IA Agents

### When stuck
- ask a clarifying question, propose a short plan, or open a draft PR with notes
- do not push large speculative changes without confirmation

### Safety and Permissions

#### Allowed without prompt

There is no especific instructions for the AI agents yet in this section.

#### Ask before doing

There is no especific instructions for the AI agents yet in this section.

- Project overview
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations

- Commit messages
- Contribution guidelines
- Pull request guidelines
- Se pueden poner otros ficheros AGENTS.md

- Definir convenciones de código.
- Incluir protocolos de testeo.

