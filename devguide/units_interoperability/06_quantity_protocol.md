# Quantity Protocol

A minimal interoperability protocol defines how quantities behave
across backends.

Required properties:

- unit
- dimensionality
- backend form

Required operations:

- convert units
- check dimensional compatibility
- extract numerical value

This protocol allows libraries to interact with quantities without
knowing which backend produced them.
