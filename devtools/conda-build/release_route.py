"""Checking an exact PyUnitWizard Conda release route and its public outcome."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

PLAN = Path(__file__).with_name("release_plan.toml")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
PUBLIC_CHANNEL = "https://conda.anaconda.org/uibcdf/noarch"
FULL_MATRIX = ".github/workflows/CI_full_matrix.yaml"


class ReleaseRouteError(ValueError):
    """Rejecting an unsafe or unproven release route."""


def read_plan(path: Path = PLAN) -> dict:
    """Loading and validating the pre-tag release decision."""
    plan = tomllib.loads(path.read_text(encoding="utf-8"))
    if not VERSION.fullmatch(str(plan.get("version", ""))):
        raise ReleaseRouteError("release plan needs a canonical X.Y.Z version")
    if plan.get("route") not in {"direct", "staged"}:
        raise ReleaseRouteError("release plan route must be direct or staged")
    for field in ("reason", "decision_by"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            raise ReleaseRouteError(f"release plan needs a reviewed {field}")
    workflows = plan.get("required_workflows")
    if (
        not isinstance(workflows, list)
        or any(not isinstance(value, str) for value in workflows)
        or FULL_MATRIX not in workflows
        or len(workflows) != len(set(workflows))
        or any(
            not value.startswith(".github/workflows/")
            or not value.endswith((".yaml", ".yml"))
            for value in workflows
        )
    ):
        raise ReleaseRouteError(
            "release plan must include the unique full-matrix workflow"
        )
    return plan


def _read_json(url: str, *, token: str | None = None) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "pyunitwizard-release-route"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    with urlopen(Request(url, headers=headers), timeout=20) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise ReleaseRouteError("registry or GitHub returned a non-object response")
    return result


def verified_workflow_runs(
    repository: str, sha: str, workflows: list[str], token: str
) -> list[dict]:
    """Finding completed successful runs of each required workflow at one SHA."""
    if not token:
        raise ReleaseRouteError("GitHub token is required to verify release gates")
    results = []
    for workflow in workflows:
        filename = quote(Path(workflow).name, safe="")
        query = urlencode({"head_sha": sha, "status": "success", "per_page": 100})
        url = f"https://api.github.com/repos/{repository}/actions/workflows/{filename}/runs?{query}"
        runs = _read_json(url, token=token).get("workflow_runs")
        if not isinstance(runs, list):
            raise ReleaseRouteError(f"GitHub did not return runs for {workflow}")
        matching = [
            run
            for run in runs
            if run.get("head_sha") == sha
            and run.get("path") == workflow
            and run.get("status") == "completed"
            and run.get("conclusion") == "success"
        ]
        if not matching:
            raise ReleaseRouteError(f"no successful exact-commit run for {workflow}")
        chosen = max(matching, key=lambda run: int(run["id"]))
        results.append({"workflow": workflow, "run_id": chosen["id"]})
    return results


def assert_version_unoccupied(version: str) -> dict:
    """Failing closed unless Anaconda returns an explicit absent-version response."""
    url = f"https://api.anaconda.org/release/uibcdf/pyunitwizard/{quote(version, safe='')}"
    try:
        existing = _read_json(url)
    except HTTPError as error:
        if error.code == 404:
            return {"url": url, "state": "absent", "http_status": 404}
        raise ReleaseRouteError(
            f"Anaconda preflight failed with HTTP {error.code}"
        ) from error
    distributions = existing.get("distributions")
    if not isinstance(distributions, list):
        raise ReleaseRouteError("Anaconda preflight did not list distributions")
    raise ReleaseRouteError(
        f"PyUnitWizard {version} already has {len(distributions)} distribution records; "
        "direct upload is forbidden, use exact-file staging promotion or investigate"
    )


def check_route(
    *, version: str, route: str, sha: str, repository: str, receipt: Path
) -> dict:
    """Checking the committed decision, exact gates, and direct-route registry state."""
    if not VERSION.fullmatch(version) or not SHA.fullmatch(sha):
        raise ReleaseRouteError(
            "release identity needs a canonical version and full SHA"
        )
    if repository != "uibcdf/pyunitwizard":
        raise ReleaseRouteError("release route must run in uibcdf/pyunitwizard")
    plan = read_plan()
    if plan["version"] != version or plan["route"] != route:
        raise ReleaseRouteError(
            "tag or dispatch does not match the committed release plan"
        )
    gates = verified_workflow_runs(
        repository, sha, plan["required_workflows"], os.environ.get("GH_TOKEN", "")
    )
    evidence = {
        "schema": "pyunitwizard.conda-route@1",
        "version": version,
        "route": route,
        "candidate_sha": sha,
        "decision_by": plan["decision_by"],
        "reason": plan["reason"],
        "gates": gates,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    if route == "direct":
        evidence["preflight"] = assert_version_unoccupied(version)
    receipt.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return evidence


def verify_public(
    *, version: str, built_paths: str, receipt: Path, attempts: int = 6
) -> dict:
    """Matching the uploaded public record to the exact locally built noarch file."""
    evidence = json.loads(receipt.read_text(encoding="utf-8"))
    if evidence.get("version") != version or evidence.get("route") != "direct":
        raise ReleaseRouteError(
            "public verification requires the matching direct receipt"
        )
    paths = shlex.split(built_paths, posix=os.name != "nt")
    if len(paths) != 1:
        raise ReleaseRouteError("PyUnitWizard noarch release must build exactly one file")
    package = Path(paths[0])
    expected_name = f"pyunitwizard-{version}-py_0.tar.bz2"
    if package.name != expected_name or not package.is_file():
        raise ReleaseRouteError("built package is not the expected noarch release file")
    with package.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    last_error = "public record not available"
    for attempt in range(attempts):
        result = subprocess.run(
            [
                "conda",
                "search",
                "--json",
                "--override-channels",
                "-c",
                "uibcdf",
                f"pyunitwizard={version}=py_0",
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            records = json.loads(result.stdout).get("pyunitwizard", [])
            matching = [
                record
                for record in records
                if record.get("sha256") == digest
                and record.get("channel") == PUBLIC_CHANNEL
                and record.get("fn") == expected_name
                and record.get("noarch") == "python"
            ]
            if len(matching) == 1:
                evidence["public"] = {
                    "coordinate": f"uibcdf/pyunitwizard/{version}/noarch/{expected_name}",
                    "sha256": digest,
                    "channel": PUBLIC_CHANNEL,
                    "url": matching[0]["url"],
                }
                receipt.write_text(
                    json.dumps(evidence, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                return evidence
            last_error = "public record does not match the built file and channel"
        else:
            last_error = "public Conda search did not resolve the exact build"
        if attempt + 1 < attempts:
            time.sleep(5)
    raise ReleaseRouteError(last_error)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    check = subcommands.add_parser("check")
    check.add_argument("--version", required=True)
    check.add_argument("--route", choices=("direct", "staged"), required=True)
    check.add_argument("--sha", required=True)
    check.add_argument("--repository", required=True)
    check.add_argument("--receipt", required=True, type=Path)
    public = subcommands.add_parser("verify-public")
    public.add_argument("--version", required=True)
    public.add_argument("--built-paths", required=True)
    public.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "check":
        check_route(
            version=args.version,
            route=args.route,
            sha=args.sha,
            repository=args.repository,
            receipt=args.receipt,
        )
    else:
        verify_public(
            version=args.version, built_paths=args.built_paths, receipt=args.receipt
        )


if __name__ == "__main__":
    main()
