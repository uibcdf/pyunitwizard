"""Settings a backend adapter reads while it is being built.

These are deployment choices rather than unit policy, so they live here instead
of in the kernel: `configure.reset()` clears what a session decided about units,
not how the machine it runs on is set up.

They are read once, when the adapter module is first imported, which happens on
the first operation that needs that backend. A consumer therefore has to set
them before then -- which is possible because naming a form no longer loads it.
"""

from __future__ import annotations

import os
from typing import Optional, Union

#: ``None`` defers to ``PYUNITWIZARD_PINT_CACHE``; ``False`` disables the cache;
#: ``True`` selects pint's own per-user location; a string selects a path.
pint_registry_cache: Optional[Union[bool, str]] = None

_OFF = {"0", "false", "off", "no"}
_AUTO = {"1", "true", "on", "yes", "auto"}


def resolve_pint_cache_folder() -> Optional[str]:
    """Return the folder pint should cache its parsed definitions in.

    Returns
    -------
    str or None
        A folder, pint's ``":auto:"`` sentinel, or ``None`` to disable caching.
    """

    setting = pint_registry_cache

    if setting is None:
        setting = os.environ.get("PYUNITWIZARD_PINT_CACHE", "").strip()
        if not setting:
            return None

    if setting is False:
        return None
    if setting is True:
        return ":auto:"

    if isinstance(setting, str):
        if setting.lower() in _OFF:
            return None
        if setting.lower() in _AUTO:
            return ":auto:"
        return setting

    return None
