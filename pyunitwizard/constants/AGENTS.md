# Constants module guidelines

These instructions apply to every file under `pyunitwizard/constants/`.

## Consistency between constant tables
- Keep `_constants` and `_constants_synonyms` synchronized. Whenever you add, rename, or remove a constant, update both structures so every canonical name has the expected synonym coverage.
- Ensure synonym keys always map to canonical names that exist in `_constants`.

## Quantity handling
- Store new constant values as raw magnitude/unit pairs and generate runtime objects through the existing `quantity()` helper.
- Never bypass the helper by instantiating unit objects directly; this keeps conversions consistent across supported backends.
- When adding code paths that return constants, make sure the result still flows through `convert()` so unit conversion keeps working.

## Validation
- Add or update tests that exercise new constants, including synonym lookup and conversion into at least one alternate unit.
- Verify `show_constants()` lists the new entries and their synonyms in the expected format.
