"""Inspect actual source, wheel and rebuilt-wheel licensing payloads (#135)."""

import email
import shutil
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]
NOTICES = ("LICENSE", "pyunitwizard/vocabularies/NOTICE.md")


def test_build_contract_rejects_pre_pep639_setuptools():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    backend = next(Requirement(r) for r in data["build-system"]["requires"] if Requirement(r).name == "setuptools")
    assert not backend.specifier.contains("76.1.0")
    assert backend.specifier.contains("77.0.3")


def test_sdist_and_rebuilt_wheel_preserve_declared_notices(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    shutil.copytree(ROOT / "pyunitwizard", source / "pyunitwizard", ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("pyproject.toml", "README.md", "MANIFEST.in", "LICENSE", "CODE_OF_CONDUCT.md"):
        shutil.copyfile(ROOT / name, source / name)
    output = tmp_path / "dist"
    output.mkdir()

    def build(directory, operations):
        code = "from setuptools import build_meta\n" + "\n".join(
            f"build_meta.{operation}({str(output)!r})" for operation in operations
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=directory, capture_output=True, text=True, timeout=120
        )
        assert result.returncode == 0, result.stdout + result.stderr

    def check_metadata(raw):
        metadata = email.message_from_bytes(raw)
        assert metadata["License-Expression"] == "MIT AND CC-BY-4.0"
        assert sorted(metadata.get_all("License-File", [])) == sorted(NOTICES)
        assert "License" not in metadata

    def check_wheel(path):
        with zipfile.ZipFile(path) as wheel:
            metadata = next(name for name in wheel.namelist() if name.endswith(".dist-info/METADATA"))
            check_metadata(wheel.read(metadata))
            prefix = metadata.removesuffix("METADATA") + "licenses/"
            for name in NOTICES:
                assert wheel.read(prefix + name) == (ROOT / name).read_bytes()
            for name in ("physical_units.json", "NOTICE.md"):
                resource = "pyunitwizard/vocabularies/" + name
                assert wheel.read(resource) == (ROOT / resource).read_bytes()

    build(source, ("build_sdist", "build_wheel"))
    wheel = next(output.glob("*.whl"))
    check_wheel(wheel)
    source_wheel = tmp_path / "source-wheel"
    source_wheel.mkdir()
    wheel.rename(source_wheel / wheel.name)
    with tarfile.open(next(output.glob("*.tar.gz"))) as sdist:
        prefix = sdist.getnames()[0].split("/")[0]
        check_metadata(sdist.extractfile(prefix + "/PKG-INFO").read())
        for name in NOTICES:
            assert sdist.extractfile(prefix + "/" + name).read() == (ROOT / name).read_bytes()
        unpacked = tmp_path / "unpacked"
        unpacked.mkdir()
        sdist.extractall(unpacked, filter="data")
    build(unpacked / prefix, ("build_wheel",))
    check_wheel(next(output.glob("*.whl")))
