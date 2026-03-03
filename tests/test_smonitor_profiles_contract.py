import pyunitwizard._smonitor as puw_smonitor


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
