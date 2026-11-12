from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "devtools" / "conda-build" / "meta.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "build_and_upload_conda_packages.yaml"
PROMOTION_WORKFLOW = ROOT / ".github" / "workflows" / "promote_conda_package.yaml"
PROVIDER = "87c70b1443d5f22d738ee3ddf812bdbe0152f6c2"


def test_recipe_declares_one_supported_noarch_python_artifact():
    recipe = RECIPE.read_text(encoding="utf-8")

    assert "noarch: python" in recipe
    assert recipe.count("python >=3.11,<3.15") == 2
    assert "number: \"{{ environ.get('PYUNITWIZARD_CONDA_BUILD_NUMBER', '0') }}\"" in recipe


def test_manual_candidates_are_exact_and_staging_only():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "candidate_sha:" in workflow
    assert "ref: ${{ inputs.candidate_sha || github.event.release.tag_name }}" in workflow
    assert 'test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"' in workflow
    assert "Build, test, and upload the staging candidate" in workflow
    assert "label: staging" in workflow
    assert "id: conda_staging\n        if: github.event_name == 'workflow_dispatch'" in workflow
    assert "--route staged" in workflow


def test_stable_releases_have_a_guarded_direct_route():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "types: ['released']" in workflow
    assert "prereleased" not in workflow
    assert "Build, test, and upload the unstaged release" in workflow
    assert "label: main" in workflow
    assert (
        "id: conda_release\n        if: github.event_name == 'release' && steps.plan.outputs.route == 'direct'"
    ) in workflow
    assert "--route direct" in workflow
    assert workflow.index("--route direct") < workflow.index("label: main")
    assert "pyunitwizard-conda-${{ inputs.version || github.event.release.tag_name }}" in workflow


def test_staged_release_event_checks_plan_but_does_not_rebuild():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "id: route_release_staged" in workflow
    assert "if: github.event_name == 'release' && steps.plan.outputs.route == 'staged'" in workflow
    assert "--route staged" in workflow
    assert (
        "id: conda_release\n        if: github.event_name == 'release' && steps.plan.outputs.route == 'direct'"
    ) in workflow
    assert (
        "Setup the public release build environment\n"
        "        if: github.event_name == 'release' "
        "&& steps.plan.outputs.route == 'direct'"
    ) in workflow


def test_noarch_workflow_has_one_job_and_retains_producer_evidence():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "matrix:" not in workflow
    assert "@" + PROVIDER in workflow
    assert "--python" not in workflow
    assert "platform_linux-64: false" in workflow
    assert "platform_win-64: false" in workflow
    assert "always() && steps.conda_staging.outputs.evidence_path != ''" in workflow
    assert "always() && steps.conda_release.outputs.evidence_path != ''" in workflow
    assert '--built-paths "$BUILT_PATHS"' in workflow
    assert "pyunitwizard-conda-route-${{ github.run_id }}-${{ github.run_attempt }}" in workflow


def test_promotion_workflow_checks_exact_release_and_file_identity():
    workflow = PROMOTION_WORKFLOW.read_text(encoding="utf-8")

    assert 'test "$GITHUB_REF" = refs/heads/main' in workflow
    assert 'test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"' in workflow
    assert 'test "$(git rev-list -n 1 "$RELEASE_VERSION")" = "$CANDIDATE_SHA"' in workflow
    assert "releases/tags/$RELEASE_VERSION" in workflow
    assert (
        "uibcdf/pyunitwizard/$RELEASE_VERSION/noarch/pyunitwizard-$RELEASE_VERSION-py_$BUILD_NUMBER.tar.bz2"
        in workflow
    )
    assert "action-build-and-upload-conda-packages/promote@" + PROVIDER in workflow
    assert "--route staged" in workflow
    assert "expected-sha256: ${{ inputs.sha256 }}" in workflow
    assert "from-label: staging" in workflow
    assert "to-label: main" in workflow
    assert 'record.get("sha256") == expected' in workflow
    assert 'record["channel"] != "https://conda.anaconda.org/uibcdf/noarch"' in workflow
    assert "ANACONDA_UIBCDF_TOKEN" in workflow
    assert (
        "uibcdf/molsyssuite/.github/actions/verify-public-conda@04480983260804113022bc20c214875a5eb5611e" in workflow
    )
    assert "always()" in workflow
    assert "steps.public.outputs['evidence-path']" in workflow


def test_owned_publisher_keeps_noarch_format_and_disables_optional_release_creation():
    workflow = yaml.safe_load(WORKFLOW.read_text())
    steps = workflow["jobs"]["conda_deployment_with_new_tag"]["steps"]
    builds = [step for step in steps if step.get("id") in ("conda_staging", "conda_release")]
    assert len(builds) == 2
    assert {step["with"]["label"] for step in builds} == {"staging", "main"}
    for step in builds:
        inputs = step["with"]
        assert step["uses"] == "uibcdf/action-build-and-upload-conda-packages@" + PROVIDER
        assert inputs["conda_build_args"] == "--package-format 1"
        assert inputs["github_release"] is False
        assert "mambabuild" not in inputs
        assert "conda_convert_args" not in inputs
        for platform in ("linux-64", "osx-64", "osx-arm64", "win-64"):
            assert inputs["platform_" + platform] is False
        assert "overwrite" not in inputs and "anaconda_upload_args" not in inputs


def test_installed_prepared_profile_requires_public_provider_and_real_guards():
    workflow = (ROOT / ".github/workflows/test_staged_conda_package.yaml").read_text(encoding="utf-8")

    assert "profile: [baseline, storage, openff, prepared]" in workflow
    assert "uibcdf::ackredit=0.10.1=py_0" in workflow
    assert "Verify public attribution provider and prepared APIs" in workflow
    assert "test_backend_declarations.py" in workflow
    assert "test_function_citation_provider.py" in workflow
    assert "test_warmed_prepared_conversion_does_not_detach_declarations_again" in workflow
    assert "--junitxml=installed-contracts.xml" in workflow
    assert "case.find('skipped') is None" in workflow


def test_staged_profiles_require_runtime_regressions():
    workflow = (ROOT / ".github/workflows/test_staged_conda_package.yaml").read_text(encoding="utf-8")

    assert "tests/pint/test_length_rounding.py" in workflow
    assert "tests/test_conversion_branches.py tests/test_introspection_probe.py" in workflow
    assert "tests/test_api_layout.py" in workflow
    assert "tests/test_ragged_quantities.py" in workflow
    assert "tests/test_concurrent_first_use.py" in workflow
    assert "test_concurrent_public_first_use_in_fresh_process" in workflow
    assert "test_concurrent_reader_waits_until_backend_and_parser_ready" in workflow
    assert "test_waiting_reader_can_initialize_after_native_failure" in workflow
    assert "test_astropy_rejects_object_rows_with_actionable_diagnostic" in workflow
    assert "test_unyt_row_conversion_has_actionable_diagnostic" in workflow
    assert "test_openff_object_rows_construct_and_convert" in workflow
    assert "test_pint_length_boundaries_round_once" in workflow
    assert "test_pint_string_unit_builds_only_the_requested_quantities" in workflow
    assert "test_filtered_probe_skips_payload_and_follows_live_debug_level" in workflow
    assert "test_main_compatibility_module_exposes_its_creator_origin" in workflow
    assert "No installed cases collected for {guard}" in workflow
    assert "Installed guard skipped: {guard}" in workflow
