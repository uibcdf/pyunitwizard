"""Parse and validate PyUnitWizard developer-guide lifecycle reports."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVGUIDE = ROOT / "devguide"
OPEN_STATUSES = ("active", "partial", "blocked", "open")
CLOSED_STATUSES = ("resolved", "withdrawn", "superseded")
VERIFICATIONS = {"reproduced", "measured", "inspected", "upstream", "asserted"}
SEVERITIES = {"critical", "high", "medium", "low"}
OWN_ISSUE = re.compile(r"^uibcdf/pyunitwizard#[1-9]\d*$")
CROSS_REPOSITORY_ISSUE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9]\d*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

LOCATIONS = (
    ("pending_bugs", "bug", False, set(OPEN_STATUSES)),
    ("pending_proposals", "proposal", False, set(OPEN_STATUSES)),
    ("solved_bugs", "bug", True, {"resolved", "withdrawn", "superseded"}),
    ("completed_proposals", "proposal", True, {"resolved"}),
    ("declined_proposals", "proposal", True, {"withdrawn", "superseded"}),
)

# These reports predate adoption of the issue-backed lifecycle. They remain immutable
# historical evidence. Every new queued or archived report requires full metadata.
LEGACY_ARCHIVE = {
    "devguide/completed_proposals/cheap_canonicity_predicate.md",
    "devguide/completed_proposals/docs_autosummary_artifact_policy.md",
    "devguide/completed_proposals/python_overhead_before_rusterization.md",
    "devguide/completed_proposals/telemetry_cost_remeasured_and_signal_boundary.md",
    "devguide/declined_proposals/rusterization_pyunitwizard_core.md",
}


@dataclass(frozen=True)
class Report:
    path: Path
    fields: dict[str, object]
    kind: str
    archived: bool
    allowed_statuses: set[str]

    @property
    def relative_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def _value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [] if not inner else [item.strip() for item in inner.split(",")]
    return raw


def read_front_matter(path: Path) -> tuple[dict[str, object], list[str]]:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT).as_posix()
    if not text.startswith("---\n") or text.count("---\n") < 2:
        if relative in LEGACY_ARCHIVE:
            return {}, []
        return {}, [f"{relative}: missing YAML front matter"]
    fields: dict[str, object] = {}
    for line in text.split("---\n", 2)[1].splitlines():
        if ":" not in line or line.startswith((" ", "#")):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = _value(value)
    return fields, []


def load_reports() -> tuple[list[Report], list[str]]:
    reports: list[Report] = []
    errors: list[str] = []
    for relative, kind, archived, allowed_statuses in LOCATIONS:
        directory = DEVGUIDE / relative
        if not directory.is_dir():
            errors.append(f"devguide/{relative}: directory is missing")
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            fields, header_errors = read_front_matter(path)
            errors.extend(header_errors)
            if fields:
                reports.append(Report(path, fields, kind, archived, allowed_statuses))
    return reports, errors


def validate_report(report: Report) -> list[str]:
    fields = report.fields
    prefix = report.relative_path
    errors = [
        f"{prefix}: {key} is missing or empty"
        for key in ("summary", "issue", "status", "opened", "verification", "area")
        if not fields.get(key)
    ]
    if not OWN_ISSUE.fullmatch(str(fields.get("issue", ""))):
        errors.append(f"{prefix}: issue must be uibcdf/pyunitwizard#<positive integer>")
    if not DATE.fullmatch(str(fields.get("opened", ""))):
        errors.append(f"{prefix}: opened must be an ISO date")

    status = str(fields.get("status", ""))
    if status not in OPEN_STATUSES + CLOSED_STATUSES:
        errors.append(f"{prefix}: unknown status {status!r}")
    elif status not in report.allowed_statuses:
        errors.append(f"{prefix}: status {status!r} does not belong in this location")
    closed = str(fields.get("closed", ""))
    if status in CLOSED_STATUSES and not DATE.fullmatch(closed):
        errors.append(f"{prefix}: a closed status requires an ISO closed date")
    if status in OPEN_STATUSES and closed:
        errors.append(f"{prefix}: an open status cannot have a closed date")
    if str(fields.get("verification", "")) not in VERIFICATIONS:
        errors.append(f"{prefix}: unknown verification value")
    area = fields.get("area")
    if not isinstance(area, list) or not area:
        errors.append(f"{prefix}: area must be a non-empty inline list")
    if report.kind == "bug" and fields.get("severity") not in SEVERITIES:
        errors.append(f"{prefix}: bugs require a valid severity")

    for key in ("blocked_by", "supersedes"):
        references = fields.get(key, [])
        if not isinstance(references, list):
            errors.append(f"{prefix}: {key} must be an inline list")
            continue
        for reference in references:
            if not CROSS_REPOSITORY_ISSUE.fullmatch(reference):
                errors.append(f"{prefix}: invalid {key} reference {reference!r}")
    if status == "blocked" and not fields.get("blocked_by"):
        errors.append(f"{prefix}: blocked requires at least one blocked_by issue")
    if status == "resolved" and not (fields.get("guard") or fields.get("normative")):
        errors.append(f"{prefix}: resolved requires guard or normative")
    return errors


def validate_all() -> tuple[list[Report], list[str]]:
    reports, errors = load_reports()
    for report in reports:
        errors.extend(validate_report(report))
    return reports, errors
