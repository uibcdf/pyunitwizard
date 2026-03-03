# Showcase

This section provides practical, copy-ready scenarios for teams adopting
PyUnitWizard in real scientific workflows.

Each showcase is narrative first and runnable second: you get the decision
context, the integration pattern, and the notebook companion for quick
validation.

## Example Catalog

| Showcase | What you will find |
|---|---|
| [Library Integration Contract](library-integration-contract.md) | How maintainers centralize configuration, normalize API inputs, and standardize outputs to keep unit behavior deterministic. |
| [Scientific Script Workflow](scientific-script-workflow.md) | How end users of integrating libraries write robust scripts with explicit units, compatibility checks, and reproducible issue reports. |
| [QA and CI Regression Gates](qa-ci-regression-gates.md) | How maintainers prevent unit regressions with targeted tests, boundary invariants, and release-time quality gates. |
| [Showcase Notebook: Quick Guide](Quick_Guide.ipynb) | First contact with configuration, quantity construction, and basic conversions. |
| [Showcase Notebook: Configuration](Configuration.ipynb) | Runtime policy examples for parser/form defaults and standards. |
| [Showcase Notebook: End-to-End Tour](PyUnitWizard_Showcase.ipynb) | Broader cross-library usage including checks, conversions, and standardization. |

Use these showcases as blueprints. Start with the one closest to your current
need, then continue through the full [User](../user/index.md) route.

```{toctree}
:maxdepth: 1
:hidden:

library-integration-contract.md
scientific-script-workflow.md
qa-ci-regression-gates.md
Quick_Guide.ipynb
Configuration.ipynb
PyUnitWizard_Showcase.ipynb
```
