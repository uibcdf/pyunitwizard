from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from devtools import devguide_reports

ROOT = Path(__file__).resolve().parents[1]


def test_all_managed_reports_have_valid_lifecycle_metadata():
    reports, errors = devguide_reports.validate_all()

    assert not errors
    assert any(report.fields["issue"] == "uibcdf/pyunitwizard#72" for report in reports)


def test_generated_queue_and_archive_indexes_are_current():
    result = subprocess.run(
        [sys.executable, "devtools/devguide_index.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_pre_adoption_archive_is_explicit_and_immutable_by_default():
    expected = {
        "devguide/completed_proposals/cheap_canonicity_predicate.md",
        "devguide/completed_proposals/docs_autosummary_artifact_policy.md",
        "devguide/completed_proposals/python_overhead_before_rusterization.md",
        "devguide/completed_proposals/telemetry_cost_remeasured_and_signal_boundary.md",
        "devguide/declined_proposals/rusterization_pyunitwizard_core.md",
    }

    assert devguide_reports.LEGACY_ARCHIVE == expected
    assert all((ROOT / relative).is_file() for relative in expected)


def test_report_validator_rejects_wrong_ownership_and_invalid_closed_state():
    fields = {
        "summary": "Example",
        "issue": "uibcdf/molsyssuite#18",
        "status": "resolved",
        "opened": "2026-09-07",
        "closed": "",
        "verification": "asserted",
        "area": ["core"],
        "blocked_by": [],
        "supersedes": [],
    }
    report = devguide_reports.Report(
        ROOT / "devguide/pending_bugs/example.md",
        fields,
        "bug",
        False,
        set(devguide_reports.OPEN_STATUSES),
    )

    errors = devguide_reports.validate_report(report)

    assert any("issue must be uibcdf/pyunitwizard" in error for error in errors)
    assert any("does not belong in this location" in error for error in errors)
    assert any("closed status requires" in error for error in errors)
    assert any("bugs require a valid severity" in error for error in errors)
    assert any("resolved requires guard or normative" in error for error in errors)


def test_protocol_routes_shared_work_and_defines_archive_semantics():
    protocol = (ROOT / "devguide/reporting_protocol.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    for required in (
        "Every queued document has an owning issue",
        "uibcdf/molsyssuite",
        "Archive, never delete",
        "python devtools/devguide_index.py --check",
    ):
        assert required in protocol
    assert "devguide/reporting_protocol.md" in agents


def test_suite_owned_configuration_proposal_left_no_local_active_copy():
    assert not (
        ROOT / "devguide/pending_proposals/molsyssuite_unit_configuration_authority.md"
    ).exists()
    lifecycle_record = (
        ROOT / "devguide/completed_proposals/adopt_shared_reporting_lifecycle.md"
    ).read_text(encoding="utf-8")

    assert "uibcdf/molsyssuite#18" in lifecycle_record
