from pyunitwizard._private.smonitor.catalog import CATALOG, CODES, SIGNALS


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


def test_signal_contract_declares_required_extra_per_source():
    sources = {
        payload["source"] for section in CATALOG.values() for payload in section.values()
    }
    assert sources == set(SIGNALS.keys())

    for source, spec in SIGNALS.items():
        assert isinstance(spec.get("extra_required"), list), source
        assert len(spec["extra_required"]) >= 1, source
