# `_private` helpers overview

This package groups the internal building blocks that power the public-facing import and parsing APIs. Each module consolidates a specific piece of infrastructure so that higher layers can keep their surface small and predictable.

## `forms.py`
Centralizes transformations between supported unit libraries and the canonical PyUnitWizard representation. Helper functions here normalize "form" objects before the kernel exposes them through the public API. Keep conversions symmetric with the user-visible helpers in `pyunitwizard.forms`.

## `parsers.py`
Implements low-level parsing utilities for strings, quantity-like objects, and mixed inputs. These helpers standardize coercion and validation logic before values reach `pyunitwizard.parse`, ensuring consistent error reporting across backends.

## `quantity_or_unit.py`
Provides convenience helpers that detect whether an input behaves like a quantity or a bare unit and resolves it into a unified internal structure. The public-facing kernel relies on these utilities to negotiate dispatch with third-party libraries.

## `exceptions/`
Defines the internal exception hierarchy shared across the private helpers. Message templates should stay concise, mention the offending value or type, and point users to the relevant public function when possible. Whenever you update an error message, cross-reference the corresponding user documentation so examples and troubleshooting tips stay aligned.
