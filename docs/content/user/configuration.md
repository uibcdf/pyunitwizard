# Configuration

`puw.configure` defines runtime behavior. Treat it as application/library
configuration, not as per-call business logic.

A reliable integration starts with one centralized initialization path. That
single decision removes a large amount of hidden runtime drift.

## Who owns the policy

Every library in a Python process shares **one** PyUnitWizard kernel. The active
policy — default form, default parser, standard units — is therefore session-wide,
and authority over it runs from strongest to weakest:

1. an explicit unit, form, or parser passed to a call;
2. an explicitly entered `puw.context(...)`;
3. the policy chosen by you, your application, or your session;
4. PyUnitWizard's factory defaults.

Importing a library is not on that list. A well-behaved library configures
PyUnitWizard only when no policy is active yet, so **your choice survives any
import that happens afterwards**.

```python
puw.configure.report()
# {'default_form': 'pint', 'default_parser': 'pint',
#  'standard_units': ['nm', 'ps', ...], 'provenance': 'molsysmt',
#  'loaded_libraries': ['pint'], 'loaded_parsers': ['pint'],
#  'fast_tracks': ['nanometers']}
```

`report()` answers "which units am I getting, and who decided that?" — the
`provenance` field names whoever set the active policy.

## Changing the policy

For the rest of the session:

```python
puw.configure.set_standard_units(["angstrom", "fs"])   # replace the whole set
puw.configure.add_standard_units(["angstrom"])         # replace one dimensionality
```

Temporarily, restoring the previous policy on exit:

```python
with puw.context(standard_units=["angstrom", "fs"]):
    ...
```

## Locating a configuration module

`puw.configure.resolve_config_module(...)` resolves *which* module holds a
package's configuration, following the ecosystem precedence rule
`runtime > env > file`:

1. runtime override (explicit argument),
2. environment variable (`PYUNITWIZARD_CONFIG`),
3. auto-discovered file (`<root_package>._pyunitwizard`).

It is a resolution helper for integrators to call: it returns a module path and
does not import or apply anything. Setting `PYUNITWIZARD_CONFIG` on its own has
no effect on the active policy — to change that, use the calls above.

## Faster startup with pint

Parsing pint's unit definitions costs about 180 ms in every process that uses
units. Pint can cache the parsed result on disk, which brings that down to
about 17 ms. It is off by default -- writing to your filesystem is not
something importing a units library should do uninvited -- and enabled with:

```bash
export PYUNITWIZARD_PINT_CACHE=1        # pint's own per-user cache location
export PYUNITWIZARD_PINT_CACHE=/path    # or a location you choose
```

The cache is keyed by the content of pint's definitions file plus the pint,
Python and platform versions, so it cannot serve a stale registry: upgrading
pint simply misses and rebuilds. Old entries are left behind rather than
removed, so the folder can be deleted at any time with no consequence beyond
one slower start.

If the folder cannot be written -- read-only containers, ephemeral CI -- the
registry is built without it and nothing fails.

## Core controls

- `load_library(...)`: register backend adapters.
- `set_default_form(...)`: define canonical output form.
- `set_default_parser(...)`: define parser for string inputs.
- `set_standard_units(...)`: define normalization targets.
- `reset()`: clear mutable configuration (useful in tests).
- `has_active_policy()`: whether standard units are already configured.
- `report()`: the active policy and its provenance.
- `resolve_config_module(...)`: resolve config module path with
  `runtime > env > file` precedence.

## Recommended baseline

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])
```

## Read-back checks

```python
print(puw.configure.get_libraries_loaded())
print(puw.configure.get_default_form())
print(puw.configure.get_default_parser())
print(puw.configure.get_standard_units())
```

Use these checks in CI tests to ensure deterministic setup.

## Operational guidance

- Keep one canonical initialization path in your package.
- Guard it with `has_active_policy()`: never overwrite a policy someone else
  already set. See the canonical integration guide for the required pattern.
- Do not reconfigure inside computational functions.
- In tests, call `reset()` before scenario-specific setup.
- If you support multiple backends, define one canonical production backend
  first, then expand with explicit cross-backend tests.

For backend-specific expectations, continue with
[Backend Coverage and Expectations](backend-coverage.md).
