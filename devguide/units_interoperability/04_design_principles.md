# Design Principles

The interoperability layer follows several core principles.

## Backend neutrality
PyUnitWizard must support multiple unit libraries.

## Explicit conversions
Unit conversions must always be explicit.

## Dimensional safety
Operations violating dimensional rules must raise clear errors.

## No silent unit stripping
Units must never be removed implicitly.

## Minimal abstraction
The interoperability layer should remain lightweight.
