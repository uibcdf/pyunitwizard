import json
import subprocess
import sys


def test_external_quantity_loads_only_its_backend_adapter():
    code = """
import json
import pint
import pyunitwizard as puw

quantity = pint.UnitRegistry().Quantity(2.5, 'nanometer')
value = puw.get_value(quantity)
print(json.dumps({'value': value, 'loaded': puw.configure.get_libraries_loaded()}))
"""

    completed = subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout.strip())

    assert result == {"value": 2.5, "loaded": ["pint"]}
