# Future Coverage Expansion for PyUnitWizard

This document outlines the roadmap for extending PyUnitWizard's interoperability with specialized Python libraries for physical quantities.

## 1. SymPy (Physics)
**URL:** [https://github.com/sympy/sympy](https://github.com/sympy/sympy)
- **Role:** Symbolic engine.
- **Benefit:** Allows PyUnitWizard to simplify complex unit expressions and validate physical formulas before numerical evaluation.

## 2. ucon
**URL:** [https://github.com/nuclab/ucon](https://github.com/nuclab/ucon)
- **Role:** Uncertainty and AI-compatible engine.
- **Benefit:** Provides native support for experimental uncertainties and integrates with the Model Context Protocol (MCP) for LLM workflows.

## 3. physipy
**URL:** [https://github.com/hgrecco/physipy](https://github.com/hgrecco/physipy)
- **Role:** Visualization-centric engine.
- **Benefit:** Deep integration with Matplotlib for automatic axis labeling and scaling.

## 4. Pydantic (Serialization)
**URL:** [https://github.com/pydantic/pydantic](https://github.com/pydantic/pydantic)
- **Role:** Data integrity.
- **Benefit:** Facilitates robust serialization for APIs and microservices within MolSysSuite.

## 5. SciPy Constants
It does not handle unit algebra, but PyUnitWizard could use it as a "source of truth" for conversion factors.
