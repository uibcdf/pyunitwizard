
# Historical conceptual note

This document is retained as historical conceptual material.

The consolidated and actively curated version of its forward-looking ideas is:
`devguide/interop_future_directions.md`.

Operational planning remains in:
- `devguide/roadmap.md`
- `devguide/release_0.21.x_rc_checklist.md`

# Toward a Units Interoperability Layer for Scientific Python

## Motivation

Working with physical quantities and units remains a persistent source of friction in the Scientific Python ecosystem.

Several mature libraries exist to represent quantities with units, including:

- Pint
- unyt
- astropy.units
- openmm.unit

Each of these libraries provides a robust internal model for quantities and unit manipulation. However, they are largely **incompatible with one another**, which introduces significant challenges when:

- combining tools from different scientific domains,
- building reusable scientific libraries,
- integrating simulation, data analysis, and visualization pipelines.

For example, molecular simulation libraries may use `openmm.unit`, astrophysical tools use `astropy.units`, and data science workflows may rely on `pint`. Converting between these systems is often ad‑hoc and fragile.

The goal of **PyUnitWizard** is not to replace existing unit libraries, but to provide a **thin interoperability layer** that allows them to coexist within a unified interface.

In the long term, PyUnitWizard aims to evolve into a **units interoperability layer for the Scientific Python ecosystem**, conceptually similar to what a hypothetical `scipy.units` module could provide.

---

# Vision

PyUnitWizard aims to become a **standard interoperability layer for quantities with units** in Scientific Python.

The core idea is simple:

> Scientific software should be able to exchange quantities with units without needing to know which units library is used internally.

Rather than competing with existing libraries, PyUnitWizard acts as a **compatibility bridge** that allows multiple unit systems to operate together.

The project focuses on:

- interoperability
- minimal abstraction
- predictable behavior
- explicit conversions
- compatibility with numerical libraries

---

# Core Concept

PyUnitWizard provides a unified API for interacting with quantities, regardless of the underlying backend.

Supported backends include:

- Pint
- unyt
- astropy.units
- openmm.unit

A quantity can be created, inspected, converted, or standardized through the PyUnitWizard interface without requiring direct knowledge of the backend implementation.

Example:

```python
import pyunitwizard as puw

puw.configure.load_library(['pint', 'openmm.unit'])
puw.configure.set_default_form('pint')

q = puw.quantity(2.5, 'nanometers/picoseconds')

q2 = puw.convert(q, to_unit='angstroms/femtoseconds', to_form='openmm.unit')
```

---

# Strategic Direction

To become a reliable interoperability layer, PyUnitWizard must move beyond a convenience API and define a **clear interoperability specification** for quantities.

This specification defines the minimal behavior required for a quantity object to participate in a multi‑library scientific workflow.

---

# Quantity Interoperability Specification (Concept)

A quantity compatible with the PyUnitWizard interoperability layer should expose the following capabilities.

## Core properties

- numerical value
- associated unit
- dimensionality
- backend form

## Core operations

- unit conversion
- dimensional compatibility checks
- value extraction
- unit extraction
- dimensionality inspection

## Required functionality

A compatible quantity object should allow:

- retrieving the numerical value
- retrieving the unit
- converting to another unit
- verifying dimensional compatibility
- interacting with NumPy‑compatible numerical values

This minimal protocol enables libraries to interact with quantities **without committing to a specific units implementation**.

---

# Canonical Dimensional Representation

One of the main obstacles to interoperability between units libraries is the lack of a shared representation of dimensionality.

PyUnitWizard aims to define a **canonical dimensional representation** that can be compared across backends.

Possible representations include:

- exponent vectors in a fixed dimensional basis
- normalized dimensional dictionaries
- standardized dimensional identifiers

This canonical representation would allow reliable dimensional comparisons between quantities originating from different libraries.

---

# NumPy and Scientific Computing Compatibility

A critical requirement for any units interoperability layer is compatibility with numerical computing libraries.

Scientific workflows frequently involve:

- NumPy
- SciPy
- pandas
- Matplotlib
- machine learning libraries

PyUnitWizard must ensure that:

- quantities can safely interact with numerical arrays
- unit information is not silently lost
- operations that change dimensionality behave predictably
- clear errors are raised when operations are physically invalid

To achieve this, PyUnitWizard will provide:

- safe wrappers for common numerical operations
- utilities for extracting numerical arrays when necessary
- explicit dimensional validation when performing operations

---

# Conformance Tests

For an interoperability layer to become a de facto standard, the specification must be supported by **conformance tests**.

PyUnitWizard will include a test suite that validates whether a backend implementation satisfies the interoperability protocol.

These tests will verify:

- value extraction
- unit extraction
- dimensional compatibility
- conversion correctness
- numerical interoperability

Any new backend integration must pass the conformance suite.

---

# Roadmap

The following milestones outline the path toward establishing PyUnitWizard as a robust interoperability layer.

## Phase 1 — Specification

- Define a **Quantity Interoperability Specification**
- Document required properties and operations
- Introduce type hints and protocols

Deliverables:

- `docs/spec/quantity-protocol.md`
- API documentation updates

---

## Phase 2 — Canonical Dimensional Model

- Define a canonical dimensional representation
- Implement dimensional comparison utilities
- Validate compatibility across backends

Deliverables:

- dimensional representation utilities
- cross‑backend comparison tests

---

## Phase 3 — Conformance Test Suite

- Implement backend‑independent tests
- Ensure each supported backend passes the suite

Deliverables:

tests/spec/

Test categories:

- dimensional equivalence
- conversion correctness
- quantity introspection
- backend consistency

---

## Phase 4 — Scientific Python Compatibility

Develop safe interoperability utilities for:

- NumPy
- SciPy
- Matplotlib

Examples:

puw.numpy.mean()
puw.numpy.linalg.norm()
puw.plot()

These utilities will ensure that units are preserved or correctly transformed during numerical operations.

---

## Phase 5 — Backend Integrations

Prioritized backend support:

1. Pint
2. OpenMM units
3. astropy.units
4. unyt

Each backend integration must satisfy the conformance test suite.

---

## Phase 6 — Ecosystem Adoption

Promote PyUnitWizard as a lightweight interoperability layer by providing:

- integration examples
- real scientific workflows
- documentation recipes

Example workflows:

- OpenMM → NumPy → Matplotlib pipelines
- Pint ↔ Astropy conversions
- standardized units in simulation pipelines

---

# Long‑Term Goal

The long‑term objective is for PyUnitWizard to serve as a **shared interoperability layer for quantities with units in Scientific Python**.

Rather than replacing existing libraries, the project aims to provide:

- a stable interoperability interface
- a canonical dimensional representation
- a reliable cross‑library conversion mechanism
- predictable behavior in scientific workflows

If widely adopted, this approach could provide the foundation for a **community‑wide units interoperability standard**.

---

# Relationship to Other Projects

PyUnitWizard is complementary to existing units libraries.

| Library | Role |
|------|------|
| Pint | General‑purpose units system |
| unyt | Scientific computing quantities |
| astropy.units | Astronomy units framework |
| openmm.unit | Molecular simulation units |

PyUnitWizard provides a **thin abstraction layer** that allows these libraries to interact without direct coupling.

---

# Summary

The Scientific Python ecosystem contains multiple excellent units libraries, but interoperability between them remains limited.

PyUnitWizard addresses this challenge by providing:

- a unified API for quantities
- cross‑library unit conversion
- canonical dimensional comparison
- compatibility with numerical workflows

The long‑term vision is to establish PyUnitWizard as a **units interoperability layer for Scientific Python**, enabling robust and predictable handling of physical quantities across scientific software.
