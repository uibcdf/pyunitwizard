"""The measurement tool also supports the released portable provider."""

import json

import pytest


@pytest.fixture
def benchmark():
    pytest.importorskip("ackredit")
    from devtools import benchmark_backend_attribution

    return benchmark_backend_attribution


def test_benchmark_runs_without_the_provisional_function_observer(benchmark, monkeypatch, capsys):
    provider = benchmark.ackredit

    class PortableSurface:
        __version__ = provider.__version__
        __file__ = provider.__file__
        session = staticmethod(provider.session)
        capture = staticmethod(provider.capture)

    def repeat(convert, number, repeat):
        convert()
        return [0.001] * repeat

    monkeypatch.setattr(benchmark, "ackredit", PortableSurface)
    monkeypatch.setattr(benchmark.timeit, "repeat", repeat)
    benchmark.main()
    result = json.loads(capsys.readouterr().out)
    assert result["function_provider_available"] is False
    for size in ("1", "100000"):
        assert set(result[size]["samples_us"]) == {"original", "ordinary", "unavailable", "workflow", "captured"}
        assert all(len(samples) == 7 for samples in result[size]["samples_us"].values())
        assert "function_captured_us" not in result[size]


@pytest.mark.parametrize("failure_call", [1, 3])
def test_benchmark_failure_restores_provider_and_dispatch(benchmark, monkeypatch, failure_call):
    calls = 0
    original_backend = benchmark._ackredit.backend
    original_dispatch = None

    def fail_during_measurement(convert, number, repeat):
        nonlocal calls
        calls += 1
        if calls == failure_call:
            raise RuntimeError("measurement failed")
        return [0.001] * repeat

    monkeypatch.setattr(benchmark.timeit, "repeat", fail_during_measurement)
    try:
        benchmark.puw.configure.load_library("pint")
        original_dispatch = benchmark.dict_convert["pint"]
        monkeypatch.setattr(benchmark.puw.configure, "reset", lambda: None)
        with pytest.raises(RuntimeError, match="measurement failed"):
            benchmark.main()
        assert benchmark._ackredit.backend is original_backend
        assert benchmark.dict_convert["pint"] is original_dispatch
    finally:
        benchmark._ackredit.backend = original_backend
        if original_dispatch is not None:
            benchmark.dict_convert["pint"] = original_dispatch
