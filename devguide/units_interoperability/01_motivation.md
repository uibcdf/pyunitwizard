# Motivation

Scientific Python uses multiple unit systems that are not interoperable.

Examples:

- openmm.unit for molecular simulations
- astropy.units for astronomy
- pint for data science workflows
- unyt for physics simulations

These libraries work well independently but become difficult to combine
within a single workflow.

Consequences include:

- fragile conversion code
- silent unit stripping
- inconsistent dimensional checks
- duplicated logic

PyUnitWizard aims to solve this problem by providing a **thin
interoperability layer** between these ecosystems.
