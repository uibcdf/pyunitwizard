import pytest
import smonitor

import pyunitwizard._smonitor as puw_smonitor
from pyunitwizard._private.smonitor.catalog import CODES


PROFILES = ["user", "dev", "qa", "agent", "debug"]


def test_smonitor_profiles_expose_expected_consumer_contract():
    profiles = puw_smonitor.PROFILES

    assert set(profiles) == {"user", "dev", "qa", "agent", "debug"}
    assert profiles["user"]["level"] == "WARNING"
    assert profiles["agent"]["level"] == "WARNING"
    assert profiles["dev"]["level"] == "INFO"
    assert profiles["qa"]["level"] == "INFO"
    assert profiles["debug"]["level"] == "DEBUG"

    assert profiles["dev"].get("show_traceback") is True
    assert profiles["qa"].get("show_traceback") is True
    assert profiles["debug"].get("show_traceback") is True


@pytest.mark.parametrize("profile", PROFILES)
def test_every_catalog_code_renders_in_every_profile(profile):
    try:
        smonitor.configure(profile=profile, handlers=[], codes=CODES)

        empty = [
            code for code in CODES if not smonitor.resolve(code=code, extra={})[0]
        ]

        assert not empty, f"empty message under {profile!r}: {empty}"
    finally:
        smonitor.configure(profile="user", handlers=[], codes=CODES)
