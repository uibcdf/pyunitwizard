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

PyUnitWizard provides a unified interface to work with physical units and to
convert between different unit libraries. Its modular design makes it easy to
integrate into scientific projects and ensures compatibility across diverse
workflows.

The design philosophy is:
- **Composability:** small, reusable components.
- **Extensibility:** easy to add new unit systems, conversions, or APIs.
- **Robustness:** strict type checking and dimensional consistency.

### Repository Structure

The repository is organized into the following main directories and files:

- **AGENTS.md** – Main guidelines for automated agents (this file).
- **CODE_OF_CONDUCT.md** – Community standards and contribution expectations.
- **devtools/** – Development tools and scripts for installing and maintaining the project.
- **docs/** – Documentation sources to be built with Sphinx.
- **examples/** – Example integrations showing how to embed PyUnitWizard into other scientific Python libraries.
- **LICENSE** – License information.
- **logos/** – Project logos and branding assets.
- **MANIFEST.in** – Packaging manifest file.
- **pyproject.toml** – Build system configuration.
- **pytest.ini** – Pytest configuration.
- **pyunitwizard/** – Main source code directory containing the core modules.
- **README.md** – Project overview and quick start guide.
- **sandbox/** – Experimental code and development notes.
- **setup.cfg** – Setup tools configuration.
- **tests/** – Unit and integration tests.
  
Additional `AGENTS.md` files may exist in some of these directories with
specific instructions for automated agents operating there.

## Coding

This section outlines the coding standards and conventions followed in the PyUnitWizard project.

### General Conventions For New Contributors

- Keep PRs small and focused.
- Write code, comments, docs, commits, PRs, and github issues in English.
- Add tests and docs for any user-visible change.
- Follow this `AGENTS.md` and existing patterns.
- Prefer readability over cleverness.
- Ensure code is clean, readable, and well-organized.

### Code Style

- Follow PEP 8 style guide for Python code.
- Use `black` (format), `isort` (imports), `flake8` (lint), `mypy` (types).
- Keep functions short when possible; avoid deep nesting.
- Use meaningful names; avoid abbreviations.
- Run style/type checks before committing.
- Maintain a consistent coding style throughout the codebase.

### Naming Conventions

- Follow PEP 8 naming conventions.
- Use `snake_case` for functions and variables.
- Use `PascalCase` for class names.
- Prefix internal/private functions with `_`.
- Suffix boolean-returning functions with `_is` or `_has` when util.

### Docstrings

- NumPy style.
- Each public symbol must document: Parameters (types), Returns, Raises, Examples (cuando aplique).

### Type Annotations

- Annotate all public functions (PEP 484).
- Use `Optional[T]` para nulos.
- Use `Literal`/`Enum` para valores restringidos.

### Comments in the code

- Explain **why**, not just **what**.
- Keep comments current with the code.
- Prefer brief notes for non-obvious logic.
- Use comments to clarify complex logic or decisions.
- Brief comments about what is done by non-obvious code sections are encouraged but should be concise.
- Avoid obvious comments that do not add value.
- Tags: `TODO`, `FIXME`, `NOTE`, `WARNING` (with date/author if it is long).

### Error Handling

- Use custom exception classes defined under exceptions.py for domain-specific errors.
- Never use bare except: blocks.
- Always provide informative error messages.

### Exceptions

- Use custom exception classes defined under exceptions.py for domain-specific errors.

### Warnings

- Use the `_private/warnings` module to issue warnings for deprecated features or non-critical issues.

### Logging

- Use the `logging` module for logging.

### Security and Dependencies

- Only use packages listed in `devtools/conda-envs/development_env.yaml`.
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

- Siempre despues de un cambio, revisar si hay que actualizar la documentación, tests, ejemplos, etc.
- Siempre despues de un cambio, revisar si hay que actualizar o corregir ficheros AGENTS.md o README.md.
