# Quantity Protocol Specification

## Purpose

This document defines the **Quantity Interoperability Protocol** for PyUnitWizard.

The goal of the protocol is to define a minimal and stable interface that
allows quantities with units from different libraries to interoperate
within the Scientific Python ecosystem.

Supported libraries may include:

- Pint
- unyt
- astropy.units
- openmm.unit

This specification defines the minimal capabilities required for a
quantity object to participate in PyUnitWizard interoperability.

---

# Design Goals

The protocol is designed with the following goals:

- backend neutrality
- minimal abstraction
- predictable dimensional behavior
- compatibility with numerical workflows
- extensibility

The protocol does **not** attempt to replace existing unit libraries.

Instead it provides a **shared interface layer**.

---

# Minimal Quantity Interface

A quantity compatible with the interoperability protocol must expose
the following information.

## Required properties

### unit

A canonical unit string.

Examples:

nm
angstrom
kcal/mol

### dimensionality

A canonical representation of dimensional exponents.

Example:

{'L': 1, 'T': -1}

### form

Identifier of the backend library.

Examples:

pint
openmm.unit
astropy.units
unyt

---

# Required Operations

## value()

Return the numerical value of the quantity.

The returned value should be compatible with NumPy arrays.

Example:

value()
→ numpy.ndarray or scalar

---

## to(unit)

Convert the quantity to another unit.

Example:

q.to("angstrom")

Conversion must raise an explicit error if dimensionalities are incompatible.

---

## is_compatible(other)

Check dimensional compatibility with another quantity.

Example:

q1.is_compatible(q2)

Returns True if dimensionality matches.

---

# Dimensional Model

Dimensionality must follow a canonical basis:

L — length
M — mass
T — time
I — electric current
Θ — temperature
N — amount of substance
J — luminous intensity

Dimensionality representation uses integer exponents.

Example:

velocity → {'L':1,'T':-1}

---

# Canonical Unit Strings

Units should be expressed using normalized strings.

Examples:

nm
nm/ps
kcal/mol

Multiplication uses "*".

Example:

kg*m/s**2

---

# Adapter Strategy

External libraries are not required to implement this protocol directly.

Instead PyUnitWizard provides **backend adapters**.

Adapters wrap native quantity objects and expose the protocol interface.

Example:

PintQuantityAdapter
OpenMMQuantityAdapter
AstropyQuantityAdapter
UnytQuantityAdapter

---

# Conformance Tests

Any backend integration must pass the PyUnitWizard conformance test suite.

Tests verify:

- dimensional representation
- conversion correctness
- compatibility checks
- numerical extraction

---

# Future Extensions

Future versions of the protocol may include:

- NumPy array protocol integration
- broadcasting rules
- pandas interoperability
- serialization standards

These features will remain optional extensions.
