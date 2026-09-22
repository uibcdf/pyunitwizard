from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devtools" / "conda-build" / "meta.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "build_and_upload_conda_packages.yaml"
PROMOTION_WORKFLOW = ROOT / ".github" / "workflows" / "promote_conda_package.yaml"


def test_recipe_declares_one_supported_noarch_python_artifact():
    recipe = RECIPE.read_text(encoding="utf-8")

    assert "noarch: python" in recipe
    assert recipe.count("python >=3.11,<3.15") == 2
    assert (
        "number: \"{{ environ.get('PYUNITWIZARD_CONDA_BUILD_NUMBER', '0') }}\"" in recipe
    )


def test_manual_candidates_are_exact_and_staging_only():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "candidate_sha:" in workflow
    assert (
        "ref: ${{ inputs.candidate_sha || github.event.release.tag_name }}" in workflow
    )
    assert 'test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"' in workflow
    assert "Build, test, and upload the staging candidate" in workflow
    assert "label: staging" in workflow
    assert (
        "id: conda_staging\n        if: github.event_name == 'workflow_dispatch'"
        in workflow
    )
    assert "--route staged" in workflow


def test_stable_releases_have_a_guarded_direct_route():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "types: ['released']" in workflow
    assert "prereleased" not in workflow
    assert "Build, test, and upload the unstaged release" in workflow
    assert "label: main" in workflow
    assert (
        "id: conda_release\n        if: github.event_name == 'release' "
        "&& steps.plan.outputs.route == 'direct'"
    ) in workflow
    assert "--route direct" in workflow
    assert workflow.index("--route direct") < workflow.index("label: main")
    assert (
        "pyunitwizard-conda-${{ inputs.version || github.event.release.tag_name }}"
        in workflow
    )


def test_staged_release_event_checks_plan_but_does_not_rebuild():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "id: route_release_staged" in workflow
    assert (
        "if: github.event_name == 'release' && steps.plan.outputs.route == 'staged'"
        in workflow
    )
    assert "--route staged" in workflow
    assert (
        "id: conda_release\n        if: github.event_name == 'release' "
        "&& steps.plan.outputs.route == 'direct'"
    ) in workflow
    assert (
        "Setup the public release build environment\n"
        "        if: github.event_name == 'release' "
        "&& steps.plan.outputs.route == 'direct'"
    ) in workflow


def test_noarch_workflow_has_one_job_and_retains_producer_evidence():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "matrix:" not in workflow
    assert "@v2.1.0" in workflow
    assert "--python" not in workflow
    assert "platform_linux-64: false" in workflow
    assert "platform_win-64: false" in workflow
    assert "always() && steps.conda_staging.outputs.evidence_path != ''" in workflow
    assert "always() && steps.conda_release.outputs.evidence_path != ''" in workflow
    assert '--built-paths "$BUILT_PATHS"' in workflow
    assert (
        "pyunitwizard-conda-route-${{ github.run_id }}-${{ github.run_attempt }}"
        in workflow
    )


def test_promotion_workflow_checks_exact_release_and_file_identity():
    workflow = PROMOTION_WORKFLOW.read_text(encoding="utf-8")

    assert 'test "$GITHUB_REF" = refs/heads/main' in workflow
    assert 'test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"' in workflow
    assert (
        'test "$(git rev-list -n 1 "$RELEASE_VERSION")" = "$CANDIDATE_SHA"' in workflow
    )
    assert "releases/tags/$RELEASE_VERSION" in workflow
    assert (
        "uibcdf/pyunitwizard/$RELEASE_VERSION/noarch/pyunitwizard-$RELEASE_VERSION-py_$BUILD_NUMBER.tar.bz2"
        in workflow
    )
    assert "action-build-and-upload-conda-packages/promote@v2.2.2" in workflow
    assert "--route staged" in workflow
    assert "expected-sha256: ${{ inputs.sha256 }}" in workflow
    assert "from-label: staging" in workflow
    assert "to-label: main" in workflow
    assert 'record.get("sha256") == expected' in workflow
    assert 'record["channel"] != "https://conda.anaconda.org/uibcdf/noarch"' in workflow
    assert "ANACONDA_UIBCDF_TOKEN" in workflow
