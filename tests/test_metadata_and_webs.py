import pyunitwizard as puw


def test_public_version_and_private_version_match():
    from pyunitwizard._version import __version__ as private_version

    assert isinstance(puw.__version__, str)
    assert puw.__version__ == private_version


def test_private_web_constants_are_well_formed():
    from pyunitwizard._private import webs

    assert webs.documentation_web__.startswith("https://")
    assert webs.github_web.endswith("/PyUnitWizard")
    assert webs.github_issues_web == f"{webs.github_web}/issues"
