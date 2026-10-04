"""Measure optional backend-attribution cost with a real Ackredit provider.

Run ``python devtools/benchmark_backend_attribution.py`` in the suite development
environment. Reports medians of seven repeats in microseconds per conversion.
The original-dispatch control removes only this pilot's observer in this process;
the other cases use public conversion and attribution contexts. Fixed credit is
per completed array operation, not per element. Results are machine-specific.
The released portable provider is sufficient; function observation is measured
only when the provider exposes that provisional capability.
"""

import hashlib
import json
import platform
import statistics
import timeit
from pathlib import Path

import ackredit
import numpy as np

import pyunitwizard as puw
from pyunitwizard import _ackredit
from pyunitwizard._private import citations
from pyunitwizard.forms import dict_convert


def main():
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    real_backend = _ackredit.backend
    observed_dispatch = dict_convert["pint"]
    original_dispatch = observed_dispatch.__wrapped__
    observe_calls = getattr(ackredit, "observe_calls", None)
    function_provider_available = callable(observe_calls)
    sources = {
        "ackredit/__init__.py": ackredit.__file__,
        "pyunitwizard/__init__.py": puw.__file__,
        "pyunitwizard/_private/citations.py": citations.__file__,
        "pyunitwizard/_ackredit.py": _ackredit.__file__,
        "devtools/benchmark_backend_attribution.py": __file__,
    }
    results = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "ackredit": ackredit.__version__,
        "pyunitwizard": puw.__version__,
        "function_provider_available": function_provider_available,
        "source_sha256": {name: hashlib.sha256(Path(path).read_bytes()).hexdigest() for name, path in sources.items()},
        "method": "seven warmed repeats; activation, imports and first-use setup excluded; microseconds per call",
    }
    try:
        for size, number in [(1, 1000), (100000, 100)]:
            with ackredit.session("benchmark"):
                q = puw.quantity(np.ones(size), "meter", form="pint")
                target = q._REGISTRY.centimeter

                def convert():
                    return puw.convert(q, to_unit=target)

                samples = {}

                def median(case):
                    measured = [elapsed / number * 1e6 for elapsed in timeit.repeat(convert, number=number, repeat=7)]
                    samples[case] = measured
                    return statistics.median(measured)

                convert()
                dict_convert["pint"] = original_dispatch
                original = median("original")
                dict_convert["pint"] = observed_dispatch
                ordinary = median("ordinary")
                measurements = {"original_us": original, "ordinary_us": ordinary}
                with puw.attribution():
                    _ackredit.backend = lambda: None
                    measurements["unavailable_us"] = median("unavailable")
                    _ackredit.backend = real_backend
                    convert()
                    measurements["workflow_us"] = median("workflow")
                    with ackredit.capture("benchmark"):
                        convert()
                        measurements["captured_us"] = median("captured")
                    if function_provider_available:
                        with observe_calls(puw):
                            convert()
                            measurements["function_workflow_us"] = median("function_workflow")
                            with ackredit.capture("function-benchmark"):
                                convert()
                                measurements["function_captured_us"] = median("function_captured")
                results[str(size)] = {**measurements, "number": number, "samples_us": samples}
    finally:
        _ackredit.backend = real_backend
        dict_convert["pint"] = observed_dispatch
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
