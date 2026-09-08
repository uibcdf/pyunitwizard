import logging

import pytest
import smonitor

from pyunitwizard._private.smonitor.catalog import CATALOG, CODES, SIGNALS
from pyunitwizard.api import conversion

PROFILES = ["user", "dev", "qa", "agent", "debug"]


def test_catalog_and_code_registry_are_consistent():
    catalog_codes = {
        payload["code"] for section in CATALOG.values() for payload in section.values()
    }
    registered_codes = set(CODES.keys())

    assert catalog_codes == registered_codes


def test_all_code_messages_include_stable_hint_fields():
    for code, payload in CODES.items():
        assert payload["title"].strip() != "", f"{code} must define a non-empty title"
        assert payload["user_hint"].strip() != "", f"{code} must define user_hint"
        assert payload["dev_hint"].strip() != "", f"{code} must define dev_hint"


@pytest.mark.parametrize("profile", PROFILES)
def test_every_code_renders_in_every_profile(profile):
    try:
        smonitor.configure(profile=profile, handlers=[], codes=CODES)
        empty = [code for code in CODES if not smonitor.resolve(code=code, extra={})[0]]

        assert not empty, f"empty message under {profile!r}: {empty}"
    finally:
        smonitor.configure(profile="user", handlers=[], codes=CODES)


def test_signal_contract_declares_required_extra_per_source():
    sources = {
        payload["source"]
        for section in CATALOG.values()
        for payload in section.values()
    }
    assert sources == set(SIGNALS.keys())

    for source, spec in SIGNALS.items():
        assert isinstance(spec.get("extra_required"), list), source
        assert len(spec["extra_required"]) >= 1, source


def test_redundant_conversion_telemetry_failure_has_logging_fallback(
    monkeypatch, caplog
):
    import smonitor.core.manager

    conversion._REDUNDANT_CONVERSION_FALLBACK_EMITTED = False

    def fail_to_get_manager():
        raise RuntimeError("manager unavailable")

    monkeypatch.setattr(smonitor.core.manager, "get_manager", fail_to_get_manager)

    with caplog.at_level(logging.WARNING, logger="pyunitwizard.api.conversion"):
        conversion._record_redundant_conversion(
            form_in="pint",
            to_unit=None,
            to_form=None,
            to_type="quantity",
        )

    assert "redundant-conversion telemetry" in caplog.text
    assert "manager unavailable" in caplog.text
