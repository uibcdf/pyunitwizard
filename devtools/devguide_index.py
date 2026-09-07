"""Render PyUnitWizard queue and archive indexes from report metadata."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from devguide_reports import (
    CLOSED_STATUSES,
    LEGACY_ARCHIVE,
    OPEN_STATUSES,
    ROOT,
    Report,
    validate_all,
)

BEGIN = "<!-- generated: devguide_index -->"
END = "<!-- /generated -->"
INDEXES = {
    "bug": ROOT / "devguide/pending_bugs/README.md",
    "proposal": ROOT / "devguide/pending_proposals/README.md",
    "archive": ROOT / "devguide/archive/README.md",
}


def _issue_link(reference: str) -> str:
    repository, number = reference.rsplit("#", 1)
    return f"[#{number}](https://github.com/{repository}/issues/{number})"


def _report_line(report: Report, base: Path) -> str:
    fields = report.fields
    path = Path(os.path.relpath(report.path, base)).as_posix()
    qualifiers = [
        str(fields[key]) for key in ("severity", "verification") if fields.get(key)
    ]
    suffix = f" *({', '.join(qualifiers)})*" if qualifiers else ""
    return (
        f"- [`{report.path.name}`]({path}) — "
        f"{_issue_link(str(fields['issue']))} — {fields['summary']}{suffix}"
    )


def _render_queue(reports: list[Report], kind: str, base: Path) -> str:
    selected = [
        report for report in reports if not report.archived and report.kind == kind
    ]
    lines: list[str] = []
    for status in OPEN_STATUSES:
        group = sorted(
            (report for report in selected if report.fields["status"] == status),
            key=lambda report: report.path.name,
        )
        if group:
            lines.extend((f"### {status.title()} ({len(group)})", ""))
            lines.extend(_report_line(report, base) for report in group)
            lines.append("")
    return "\n".join(lines).rstrip() or "*No entries.*"


def _render_archive(reports: list[Report], base: Path) -> str:
    selected = [report for report in reports if report.archived]
    lines: list[str] = []
    for status in CLOSED_STATUSES:
        group = sorted(
            (report for report in selected if report.fields["status"] == status),
            key=lambda report: report.path.name,
        )
        if group:
            lines.extend((f"### {status.title()} ({len(group)})", ""))
            lines.extend(_report_line(report, base) for report in group)
            lines.append("")
    if LEGACY_ARCHIVE:
        lines.extend((f"### Legacy pre-adoption records ({len(LEGACY_ARCHIVE)})", ""))
        for relative in sorted(LEGACY_ARCHIVE):
            path = ROOT / relative
            link = Path(os.path.relpath(path, base)).as_posix()
            lines.append(f"- [`{path.name}`]({link})")
    return "\n".join(lines).rstrip() or "*No entries.*"


def _replace(text: str, body: str) -> str:
    if BEGIN not in text or END not in text:
        raise ValueError("generated index markers are missing")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n\n{body}\n\n{END}{tail}"


def process(check: bool) -> list[str]:
    reports, errors = validate_all()
    if errors:
        raise ValueError("\n".join(errors))
    stale: list[str] = []
    for kind, readme in INDEXES.items():
        body = (
            _render_archive(reports, readme.parent)
            if kind == "archive"
            else _render_queue(reports, kind, readme.parent)
        )
        current = readme.read_text(encoding="utf-8")
        updated = _replace(current, body)
        if updated == current:
            continue
        stale.append(readme.relative_to(ROOT).as_posix())
        if not check:
            readme.write_text(updated, encoding="utf-8")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        stale = process(arguments.check)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if arguments.check and stale:
        print("stale generated indexes: " + ", ".join(stale), file=sys.stderr)
        return 1
    for path in stale:
        print(f"wrote {path}")
    if arguments.check:
        print("Generated report indexes are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
