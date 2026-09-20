"""Parse and validate PyUnitWizard developer-guide lifecycle reports."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DEVGUIDE = ROOT / "devguide"
OPEN_STATUSES = ("active", "partial", "blocked", "open")
CLOSED_STATUSES = ("resolved", "withdrawn", "superseded")
VERIFICATIONS = {"reproduced", "measured", "inspected", "upstream", "asserted"}
SEVERITIES = {"critical", "high", "medium", "low"}
OWN_ISSUE = re.compile(r"^uibcdf/pyunitwizard#[1-9]\d*$")
CROSS_REPOSITORY_ISSUE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9]\d*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PYTHON_IDENTIFIER = re.compile(r"^[A-Za-z_]\w*$")
GUARD_POLICY_EFFECTIVE_DATE = "2026-09-20"
PYTEST_ROOTS = (PurePosixPath("tests"), PurePosixPath("devtools/tests"))

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


def _is_test_class(node: ast.ClassDef) -> bool:
    if node.name.startswith("Test"):
        return True
    return any(
        (isinstance(base, ast.Name) and base.id.endswith("TestCase"))
        or (isinstance(base, ast.Attribute) and base.attr.endswith("TestCase"))
        for base in node.bases
    )


def _test_functions(nodes: list[ast.stmt]) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in nodes
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
    }


def validate_pytest_guard(root: Path, selector: str) -> list[str]:
    if any(character.isspace() for character in selector) or any(
        token in selector for token in (",", "(", ")", "*", "?")
    ):
        return [f"guard {selector!r} uses unsupported selector syntax"]
    parts = selector.split("::")
    if not 1 <= len(parts) <= 3 or any(not part for part in parts):
        return [f"guard {selector!r} uses unsupported selector syntax"]
    if any("[" in part or "]" in part for part in parts[1:]):
        return [
            (
                f"guard {selector!r}: parameterized selectors are not supported by "
                "the static Python profile; name the unparameterized test or the module"
            )
        ]

    relative = PurePosixPath(parts[0])
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or relative.suffix != ".py"
        or not any(relative.is_relative_to(base) for base in PYTEST_ROOTS)
    ):
        return [(f"guard {selector!r} must name a safe Python file under tests/ or devtools/tests/")]
    target = root.joinpath(*relative.parts)
    if not target.is_file():
        return [f"guard {selector!r} names a file that does not exist"]
    try:
        tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
    except (OSError, SyntaxError) as error:
        return [f"guard {selector!r} cannot be statically indexed: {error}"]

    functions = _test_functions(tree.body)
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef) and _is_test_class(node)}
    if len(parts) == 1:
        if functions or any(_test_functions(node.body) for node in classes.values()):
            return []
        return [f"guard {selector!r} does not resolve to a collected test"]
    if not all(PYTHON_IDENTIFIER.fullmatch(part) for part in parts[1:]):
        return [f"guard {selector!r} uses unsupported selector syntax"]
    if len(parts) == 2 and parts[1] in functions:
        return []
    if len(parts) == 3:
        class_node = classes.get(parts[1])
        if class_node is not None and parts[2] in _test_functions(class_node.body):
            return []
    return [f"guard {selector!r} does not resolve to a collected test"]


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
    closed = str(fields.get("closed", ""))
    guard = fields.get("guard")
    if status == "resolved" and guard and closed >= GUARD_POLICY_EFFECTIVE_DATE:
        errors.extend(f"{prefix}: {error}" for error in validate_pytest_guard(ROOT, str(guard)))
    return errors


def validate_all() -> tuple[list[Report], list[str]]:
    reports, errors = load_reports()
    for report in reports:
        errors.extend(validate_report(report))
    return reports, errors
