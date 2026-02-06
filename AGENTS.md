# PyUnitWizard

*A Python Units Wizard that streamlines work with physical quantities.*

---

## 1. Purpose of This File

This file defines how automated agents and human contributors must work with the **PyUnitWizard** repository.  
It serves as a guide for consistent, transparent, and safe collaboration between humans and automated systems.

---

## 2. Project Overview

**PyUnitWizard** is a Python library that standardizes and simplifies the handling of physical units across different unit systems.  
It acts as a bridge between libraries such as `pint`, `unyt`, `openmm.unit`, and `astropy.units`, allowing seamless conversions and interoperability.

Design principles:

- **Composability:** small, reusable components.
- **Extensibility:** easy to add new unit systems or APIs.
- **Robustness:** strict type checking and dimensional consistency.

By integrating PyUnitWizard, scientific libraries can let users choose how
units are represented and handled without changing their workflows. This
ensures that outputs can be used as inputs in other tools regardless of the
unit system, making scientific pipelines compatible, flexible, and
interoperable.

---

## 3. Repository Structure

Main directories and files:

| Path | Description |
|------|--------------|
| `pyunitwizard/` | Core source code. |
| `tests/` | Unit and integration tests. |
| `devtools/` | Environment, build, and maintenance tools. |
| `docs/` | Documentation sources (Sphinx). |
| `examples/` | Example integrations showing how to embed PyUnitWizard into other scientific Python libraries. |
| `sandbox/` | Experimental code and notes. |
| `logos/` | Branding assets. |
| `CODE_OF_CONDUCT.md` | Community standards. |
| `AGENTS.md` | Agent interaction rules (this file). |
| `README.md` | Quick start and overview. |
| `LICENSE` | License information. |
| `MANIFEST.in` | Packaging manifest file. |
| `pyproject.toml` | Build system configuration. |
| `pytest.ini` | Pytest configuration. |
| `setup.cfg` | Setup tools configuration. |

Additional `AGENTS.md` files may exist in submodules with specialized instructions.

---

## 4. Coding Guidelines

### 4.1 General Conventions

- Keep PRs small and focused.  
- Use English for all code, comments, PRs, issues, and docs.  
- Always include or update tests and documentation for user-visible changes.  
- Follow existing patterns and maintain readability.  
- Avoid unnecessary cleverness — clarity first.  

### 4.2 Code Style

- Follow **PEP 8**.  
- Tools: `black` (formatting), `isort` (imports), `flake8` (linting), `mypy` (type checking).  
- Prefer short, modular functions.  
- Use explicit, descriptive names.  
- Run linting and type checks before committing.

### 4.3 Naming

| Element | Convention | Example |
|----------|-------------|---------|
| Variables / functions | `snake_case` | `convert_units()` |
| Classes | `PascalCase` | `UnitSystem` |
| Private members | Prefix with `_` | `_parse_symbol()` |
| Boolean-returning | Suffix `_is` / `_has` | `is_valid()`, `has_units()` |

### 4.4 Docstrings

- Use **NumPy style**.  
- Each public symbol must include **Parameters**, **Returns**, **Raises**, and **Examples** when applicable.

### 4.5 Type Annotations

- Annotate all public functions (PEP 484).  
- Use `Optional[T]` for nullable types.  
- Use `Literal` or `Enum` for restricted values.  

### 4.6 Comments

- Explain *why*, not just *what*.  
- Keep comments up to date.  
- Prefer brief, focused notes.  
- Tags: `TODO`, `FIXME`, `NOTE`, `WARNING` (with author/date if long-term).

### 4.7 Error Handling

- Use custom exceptions in `exceptions.py` for domain-specific errors.  
- Never use bare `except:` clauses.  
- Provide clear and informative error messages.

### 4.8 Logging and Warnings

- Use `logging` for runtime messages.  
- Use `_private/warnings` for non-critical issues or deprecations.

### 4.9 Security and Dependencies

- Use only dependencies listed in `devtools/conda-envs/development_env.yaml`.  
- Avoid deprecated or unmaintained packages.  
- Regularly verify that dependencies are **available, necessary, and pertinent**.  
- Check dependencies periodically using tools such as `safety` or `bandit`.  
- Never commit secrets, credentials, or environment variables.  
- Avoid hardcoding sensitive information in code or logs.  
- Do not report or share secrets, credentials, or environment variables in **issues**, **PRs**, or any communication channel.  

---

## 5. Testing Guidelines

- All public functions and modules must have tests under `tests/`.  
- Use `pytest` for test execution.  
- Run `pytest tests/` before each PR.  
- Test both success and failure cases.  
- Prefer **unit tests** for small functions and **integration tests** for workflows.  
- Keep tests independent and reproducible.  

### 5.1 Test-First Development Mode

- **For new features:** write or update unit tests first, then implement the feature until all tests pass (“code to green”).  
- **For regressions:** add a failing test that reproduces the bug, then fix it.  
- **For UI or state-based modules:** prefer component tests that validate observable changes.  

---

## 6. Documentation Guidelines

- Written in Markdown or MyST (for Sphinx).  
- Each public module must include examples and docstrings.  
- Update documentation after API or behavior changes.  
- Validate generated docs before merging (`make html`).  
- Do not include private or experimental code in public docs.

---

## 7. Version Control and Contributions

### 7.1 Commit Messages

Use the conventional format:

```
<type>(<scope>): <short description>
```

Examples:
- `feat(core): add converter for astropy units`
- `fix(tests): correct numpy array comparison`
- `docs(readme): improve quick-start example`

Keep commits atomic, small, and meaningful.

### 7.2 Pull Requests

- Run all tests before submitting.  
- Ensure lint/type checks pass.  
- Keep PRs under 300 lines of diff when possible.  
- Include context and motivation in the PR body.  
- Link related issues with `Fixes #<id>` or `Closes #<id>`.  

Checklist:
- ✅ All tests and checks pass.  
- ✅ Code reviewed or self-reviewed.  
- ✅ Docs updated if behavior changed.  
- ✅ No debug or leftover code.  

---

## 8. AI Agent Guidelines

These rules apply to automated agents (GitHub Actions, Copilot Agents, CI bots, etc.) collaborating on this repository.

### 8.1 General Behavior

- Always wait for terminal commands to complete before proceeding.  
- Do not modify code outside the assigned scope.  
- Prefer proposing changes via PR rather than direct commits to `main`.  
- Ask for clarification or open a draft PR if unsure.  
- Never overwrite human work or documentation without explicit approval.  
- When stuck, **ask a clarifying question**, propose a short plan, or open a draft PR with notes — do not push large speculative changes without confirmation.  

### 8.2 Citation Format

When referencing files or terminal outputs in responses, use the following citation style:

1. **File citations:** `【F:<path>†L<start>-L<end>】`  
2. **Terminal citations:** `【<chunk_id>†L<start>-L<end>】`  

Only cite relevant, contentful lines — never blank lines.

If referencing code changes or test results in PR summaries, prefer **file citations**; use terminal citations only when output verification is required.

### 8.3 Git Instructions for Agents

- Commit using `git` (no untracked changes).  
- Fix pre-commit issues before retrying.  
- Do not amend existing commits; create new ones.  
- Confirm with `git status` before finishing.  

### 8.4 Testing Protocol for Agents

- Follow **test-first** development: add or update tests before writing new code.  
- For bug fixes, add a failing test first, then implement the fix.  
- Do not skip tests unless justified in the PR.  

### 8.5 Programmatic Checks for Agents

This section defines automated consistency checks to be performed by AI or CI agents before merging changes.  
To be extended in future versions, it may include:

- Verification of documentation coverage.  
- Automatic code style and dependency audits.  
- Validation of cross-repo synchronization for shared components.  

### 8.6 Safety and Permissions

**Allowed without prompt:**  
- Running linters, formatters, or test suites.  
- Generating documentation locally.  
- Checking dependency status.  

**Ask before doing:**  
- Committing code or modifying configuration.  
- Running destructive commands (e.g., deleting branches or files).  
- Editing documentation or CI pipelines.  
- Updating build/test commands, contribution guidelines, or security considerations.  
- Changing commit message conventions or PR workflows.  

---

## 9. Maintenance Reminders

- After any change, verify if documentation, examples, or tests must be updated.  
- After any change, verify if any `AGENTS.md` or `README.md` need to be updated for consistency.  
- Regularly review CI configurations for dependency or policy drift.  
- Keep this file synchronized across UIBCDF projects when possible.  

---

*Last updated: November 2025*

## External Tooling Guides (Required for Development)

These guides are required reading for anyone developing this library. They describe how external tools must be used here.

- `SMONITOR_GUIDE.md` — Required guide for SMonitor integration and diagnostics.
