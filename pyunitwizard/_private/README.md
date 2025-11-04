# `_private` helpers overview

This package groups the internal building blocks that power the public-facing import and parsing APIs. Each module consolidates a specific piece of infrastructure so that higher layers can keep their surface small and predictable. Everything documented here is considered implementation detail: consumers should continue to rely on the public helpers exposed through `pyunitwizard.*` rather than importing `_private` modules directly.

## `forms.py`
Centralizes transformations between supported unit libraries and the canonical PyUnitWizard representation. Helper functions here normalize "form" objects before the kernel exposes them through the public API. Keep conversions symmetric with the user-visible helpers in `pyunitwizard.forms`.

## `parsers.py`
Implements low-level parsing utilities for strings, quantity-like objects, and mixed inputs. These helpers standardize coercion and validation logic before values reach `pyunitwizard.parse`, ensuring consistent error reporting across backends.

## `quantity_or_unit.py`
Provides convenience helpers that detect whether an input behaves like a quantity or a bare unit and resolves it into a unified internal structure. The public-facing kernel relies on these utilities to negotiate dispatch with third-party libraries.

## `exceptions/`
Defines the internal exception hierarchy shared across the private helpers. Message templates should stay concise, mention the offending value or type, and point users to the relevant public function when possible. Whenever you update an error message, cross-reference the corresponding user documentation so examples and troubleshooting tips stay aligned.

## `functions.py`
Offers stack-introspection helpers used to enrich diagnostic messages emitted by the exception classes. By centralizing utilities such as `caller_name`, all private modules generate consistent error prefixes without having to duplicate `inspect` logic or leak stack details to the public surface.

## `lists_and_tuples.py`
Keeps lightweight predicates and stringification helpers for sequence-like inputs. These functions back configuration routines—e.g., `pyunitwizard.configure.configure`—and internal validators so that higher layers can accept either scalars or iterables while producing predictable error messages and telemetry payloads.

## `webs.py`
Stores canonical project URLs in a single place. Private helpers reuse these constants when crafting guidance in exceptions or logs, ensuring that any reference to the website, repository, or issue tracker stays in sync without touching public modules.
