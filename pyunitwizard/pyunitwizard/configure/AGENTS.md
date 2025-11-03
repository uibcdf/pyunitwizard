# Configure package guardrails

This guide applies to files in `pyunitwizard/configure/` and any future
submodules that feed configuration state back into the runtime kernel.

## `load_library` invariants
- Always normalize user input through `digest_form` so aliases map to the
  canonical library key before comparison or storage.
- Keep the function idempotent: re-loading an already loaded backend must not
  call back into `forms.load_library` or mutate kernel state.
- The first successfully normalized name in the request remains the default
  form until callers explicitly change it. Do not reorder arguments or mutate
  the provided sequence.
- Only set `kernel.default_parser` when it is `None`, and pick the first name
  in the request that is in `configure.parsers`. New parser backends must be
  added to that list to participate in eager selection.
- Preserve backwards compatibility for string inputs: all iterables that are
  not recognized as strings should be rejected with a `TypeError`.

## Default form and parser selection
- Helpers such as `set_default_form` and `set_default_parser` must keep using
  `digest_form` so downstream code can rely on normalized values.
- Any new default-selection logic should continue to respect the kernel state
  set up by `kernel.initialize()`; do not add side effects that depend on prior
  imports or global variables outside the kernel module.

## Kernel reset expectations
- `configure.reset()` is the canonical way to clear runtime state in tests.
  It must reset every collection that `kernel.initialize()` touches, including
  loaded libraries, parsers, default form/parser, and standards dictionaries.
- When introducing new kernel attributes, update both `kernel.initialize()` and
  `configure.reset()` in lockstep and document the addition here.
- Avoid partial resets in new helpers. Instead, expose targeted convenience
  wrappers that call `reset()` and then apply any additional setup needed for a
  test scenario.
