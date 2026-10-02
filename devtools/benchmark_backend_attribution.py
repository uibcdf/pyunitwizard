"""Measure optional backend-attribution cost with the real development provider.

Run ``python devtools/benchmark_backend_attribution.py`` in the suite development
environment. Reports medians of seven repeats in microseconds per conversion.
The original-dispatch control removes only this pilot's observer in this process;
the other cases use public conversion and attribution contexts. Fixed credit is
per completed array operation, not per element. Results are machine-specific.
"""

import json
import platform
import statistics
import timeit

import ackredit
import numpy as np

import pyunitwizard as puw
from pyunitwizard import _ackredit
from pyunitwizard.forms import dict_convert


def main():
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    real_backend = _ackredit.backend
    observed_dispatch = dict_convert["pint"]
    original_dispatch = observed_dispatch.__wrapped__
    results = {"python": platform.python_version(), "ackredit": ackredit.__version__, "pyunitwizard": puw.__version__}
    for size, number in [(1, 1000), (100000, 100)]:
        with ackredit.session("benchmark"):
            q = puw.quantity(np.ones(size), "meter", form="pint")
            target = q._REGISTRY.centimeter

            def convert():
                return puw.convert(q, to_unit=target)

            def median():
                return statistics.median(timeit.repeat(convert, number=number, repeat=7)) / number * 1e6

            convert()
            dict_convert["pint"] = original_dispatch
            original = median()
            dict_convert["pint"] = observed_dispatch
            ordinary = median()
            with puw.attribution():
                _ackredit.backend = lambda: None
                unavailable = median()
                _ackredit.backend = real_backend
                convert()
                workflow = median()
                with ackredit.capture("benchmark"):
                    convert()
                    captured = median()
            results[str(size)] = dict(
                original_us=original,
                ordinary_us=ordinary,
                unavailable_us=unavailable,
                workflow_us=workflow,
                captured_us=captured,
            )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
