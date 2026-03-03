# User

PyUnitWizard appears in two very different contexts, and each context needs a
clear reading path.

Some readers are maintainers evaluating whether to integrate PyUnitWizard in a
scientific library. Others are scientists using a library that already embeds
PyUnitWizard and just want reliable, predictable behavior in their scripts.

This section is written for both profiles. Pick the route that matches your
role first, then skim the other route so you understand the full contract
between library maintainers and library users.

## Route A: Library Integrators

Go to [Library Integrators](library-integrators.md).

In this route you will learn how to:
- configure PyUnitWizard once and keep runtime deterministic,
- normalize and validate quantities at API boundaries,
- standardize outputs so downstream tools receive consistent units.

## Route B: End Users of Integrating Libraries

Go to [End Users](end-users.md).

In this route you will learn how to:
- reason about quantity parsing, conversion, and compatibility in day-to-day scripts,
- diagnose common failures quickly,
- communicate reproducible unit issues to library maintainers.

Both routes converge on the same objective: unit-safe workflows across
scientific Python libraries without hidden assumptions.

## Public API Map

When you need complete function-level reference:
- [Users API Reference](../../api/users/api_user.rst)
- [Developers API Reference](../../api/developers/api_developers.rst)

## Notebook Route

If you prefer notebook-first learning, follow this practical sequence:
1. [Importing.ipynb](Importing.ipynb)
2. [Quantities_and_Units.ipynb](Quantities_and_Units.ipynb)
3. [Convert.ipynb](Convert.ipynb)
4. [Dimensionality.ipynb](Dimensionality.ipynb)
5. [In_Your_Library.ipynb](In_Your_Library.ipynb)

## Notebook Reference

```{toctree}
:maxdepth: 1
:hidden:

library-integrators.md
end-users.md
what-pyunitwizard-solves.md
adoption-story.md
backend-coverage.md
quickstart.md
mini-library-walkthrough.md
configuration.md
integrating-your-library.md
troubleshooting.md
production-checklist.md
faq.md
Importing.ipynb
Quantities_and_Units.ipynb
Convert.ipynb
Strings.ipynb
Dimensionality.ipynb
Check.ipynb
Similarity.ipynb
Standardize.ipynb
Lists_and_arrays.ipynb
In_Your_Library.ipynb
```
