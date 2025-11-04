# Form adapter guidelines

This file applies to every document and module inside `pyunitwizard/pyunitwizard/forms`.

## Dispatcher population rules
- `pyunitwizard.forms.load_library` discovers adapters and fills the shared dispatcher dictionaries (`dict_is_form`, `dict_translate_quantity`, and friends). Keep the documentation in sync with the actual function names stored in these tables when you add or rename helpers.
- Describe new dispatch keys in docstrings or READMEs so contributors know which functions get registered. When wiring new entries, note both the source form (dictionary key) and the helper name that is bound.

## Parser availability contract
- Each adapter module must expose a module-level boolean named `parser`. Set it to `True` only when the form can parse strings directly; otherwise set it to `False` and mention any follow-up work in this directory.
- Updates to parser support must document the supported inputs and how to activate them. If the parser flag changes, update the README checklist so reviewers can spot new dependencies.

## Translator naming conventions
- Outgoing translators use the pattern `quantity_to_<target>` and `unit_to_<target>`, where `<target>` matches the dispatcher key for the destination form. Use underscores instead of dots in the function name (`quantity_to_openmm_unit` for the `"openmm.unit"` target).
- Keep helper names stable. When a translator is renamed, update every reference in the documentation, unit tests, and translator dictionaries.
- String translators live in `api_string.py` and mirror the same naming scheme. New adapters must provide symmetric helpers so round-trip conversions remain available.
