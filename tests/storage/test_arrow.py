"""Arrow/Parquet retain the codec seal and distinguish null from NaN."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError
from pyunitwizard.storage import arrow

pa = pytest.importorskip("pyarrow")


@pytest.mark.parametrize(
    "values",
    [
        np.arange(12, dtype=np.float32).reshape(2, 2, 3),
        np.array([np.nan, np.inf, -0.0]),
        np.array(3, dtype=np.int32),
        np.empty((0, 3), dtype=np.float32),
    ],
)
def test_arrow_and_parquet_roundtrip(tmp_path, values):
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        source = QuantityRecord.from_quantity(puw.quantity(values, "nm", form="pint"), field="x")
        table = arrow.to_table(source)
        result = arrow.from_table(table, field="x", unit="angstrom")
        assert result.digest == source.digest
        assert result.values.dtype == values.dtype and result.values.shape == values.shape
        np.testing.assert_array_equal(result.values, values)
        arrow.write(tmp_path / "data.parquet", source)
        assert arrow.read(tmp_path / "data.parquet", unit="nm").digest == source.digest
        with pytest.raises(RecordError):
            arrow.write(tmp_path / "data.parquet", source)


def test_heterogeneous_table_requires_descriptor_expectations(tmp_path):
    source = QuantityRecord.from_tagged(
        [puw.quantity(3, "nM", form="pint"), puw.quantity(50, "percent", form="pint")], field="activities"
    )
    table = arrow.to_table(source)
    with pytest.raises(RecordError):
        arrow.from_table(table, unit="nM")
    with pytest.raises(RecordError):
        arrow.from_table(table, units=["second", "percent"])
    result = arrow.from_table(table, field="activities", units=["uM", "percent"])
    assert result.digest == source.digest
    arrow.write(tmp_path / "tagged.parquet", source)
    assert arrow.read(tmp_path / "tagged.parquet", units=["nM", "percent"]).digest == source.digest


@pytest.mark.parametrize("edit", ["values", "null", "metadata", "extra", "dtype", "field_metadata"])
def test_arrow_changes_are_refused(edit):
    source = QuantityRecord.from_quantity(puw.quantity(np.array([1.0, np.nan]), "nm", form="pint"))
    table = arrow.to_table(source)
    if edit in ("values", "null", "dtype"):
        data = pa.array([2.0, np.nan]) if edit == "values" else pa.array([1.0, None])
        if edit == "dtype":
            data = pa.array([1.0, np.nan], type=pa.float32())
        table = table.set_column(0, table.schema.field(0).name, data)
    elif edit == "metadata":
        table = table.replace_schema_metadata(None)
    elif edit == "extra":
        table = table.append_column("extra", pa.array([1, 2]))
    else:
        schema = table.schema.set(0, table.schema.field(0).with_metadata({b"units": b"meter"}))
        table = pa.Table.from_arrays(table.columns, schema=schema)
    with pytest.raises(RecordError):
        arrow.from_table(table, unit="nm")
