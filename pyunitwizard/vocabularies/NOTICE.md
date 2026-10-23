# Bounded physical-unit vocabulary

The derived `physical_units.json` catalogue retains identifiers and selected
numerical/semantic facts from QUDT 3.5.3 (QUDT.org, Inc.) and the OBO Units
Ontology, release 2026-10-12 (Units Ontology contributors).

Both source vocabularies are licensed under
[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).
Source URLs, immutable commits, original file SHA-256 values and attribution
are included in the catalogue. Upstream license texts:
[QUDT](https://github.com/qudt/qudt-public-repo/blob/07acd3f9ee2c7189341f322c85154ca63c9198f2/LICENSE),
[UO](https://github.com/bio-ontology-research-group/unit-ontology/blob/311f3d222444fcf8adf032dfa58f3c1b55bd22af/LICENSE.md).

Changes: PyUnitWizard selects three named unit meanings, adds computing-unit
spellings and a reviewed local QUDT/UO correspondence, and packages the result
as JSON. These correspondences are not claimed to be upstream `exactMatch`
assertions. This data's license is distinct from PyUnitWizard's MIT code.

Reproduce offline with `devtools/extract_quantity_vocabulary.py` from the exact
three upstream files identified by the catalogue. The extractor refuses changed
input bytes, undeclared quantity kinds and changed UO semantic ancestry.
