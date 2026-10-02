"""Offline declarations for the bounded Pint/unyt attribution pilot.

Sources: https://github.com/hgrecco/pint and
https://github.com/yt-project/unyt/blob/main/README.rst.
An article's publication year is independent of the executed software version.
"""

import sys
from copy import deepcopy

_SOFTWARE = {
    "pint": {
        "type": "software",
        "title": "Pint: makes units easy",
        "authors": ["Pint contributors"],
        "url": "https://github.com/hgrecco/pint",
    },
    "unyt": {
        "type": "software",
        "title": "unyt",
        "authors": ["unyt developers"],
        "url": "https://github.com/yt-project/unyt",
    },
}
_ARTICLES = {
    "unyt": [
        {
            "id": "doi:10.21105/joss.00809",
            "type": "article",
            "title": "unyt: Handle, manipulate, and convert data with units in Python",
            "authors": [
                "Goldbaum, Nathan J.",
                "ZuHone, John A.",
                "Turk, Matthew J.",
                "Kowalik, Kacper",
                "Rosen, Anna L.",
            ],
            "doi": "10.21105/joss.00809",
            "year": 2018,
            "journal": "Journal of Open Source Software",
            "volume": 3,
            "number": 28,
            "pages": "809",
        }
    ],
}


def records(library):
    """Detach bibliographic declarations for an already executed pilot backend.

    Does not import the backend or provider, or look up a DOI. Software-only,
    article-only and combined declarations have the same credit boundary.
    """
    module = sys.modules.get(library)
    if module is None or library not in _SOFTWARE:
        return []
    version = str(module.__version__)
    context = {"software": library, "version": version}
    result = []
    if _SOFTWARE[library] is not None:
        software = deepcopy(_SOFTWARE[library])
        software.update(id=f"software:{library}:{version}", version=version)
        result.append({"record": software, "roles": ["executed_software"], "context": deepcopy(context)})
    result.extend(
        {"record": deepcopy(article), "roles": ["software_description"], "context": deepcopy(context)}
        for article in _ARTICLES.get(library, [])
    )
    return result
