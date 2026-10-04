"""Offline software citation for the dependency-free function-provider pilot.

The software DOI and authors come from docs/content/about/citation.md. Backend
references are selected separately at completed dispatch, never declared here.
"""


def declaration(version):
    """Return inert metadata without importing an observer or unit backend."""
    item_id = f"software:pyunitwizard:{version}"
    return {
        "schema": "ackredit.provider@1",
        "software": {"name": "pyunitwizard", "version": version},
        "items": [
            {
                "id": item_id,
                "type": "software",
                "title": "UIBCDF/PyUnitWizard",
                "authors": [
                    "Prada-Gracia, Diego",
                    "Ibarrola-Sánchez, Daniel",
                    "Moreno-Vargas, Liliana M.",
                ],
                "doi": "10.5281/zenodo.8092688",
                "url": "https://github.com/uibcdf/pyunitwizard",
                "version": version,
            }
        ],
        "functions": {
            name: [{"item_id": item_id, "roles": ["executed_software"]}]
            for name in ("quantity", "convert", "conversion_factor", "standardize")
        },
    }
