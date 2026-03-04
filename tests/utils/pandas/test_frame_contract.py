import numpy as np
import pyunitwizard as puw
import pytest


pd = pytest.importorskip("pandas")


def configure_libraries():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])


def test_dataframe_from_quantities_stores_values_and_units_map():
    configure_libraries()

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {
            "length": puw.quantity([1.0, 2.0], "nanometer"),
            "time": puw.quantity([10.0, 20.0], "picosecond"),
        },
        to_units={"length": "angstrom"},
    )

    np.testing.assert_allclose(dataframe["length"].to_numpy(), np.array([10.0, 20.0]))
    np.testing.assert_allclose(dataframe["time"].to_numpy(), np.array([10.0, 20.0]))
    assert dataframe.attrs["pyunitwizard_units"]["length"] == "angstrom"
    assert dataframe.attrs["pyunitwizard_units"]["time"] == "picosecond"


def test_add_quantity_column_updates_units_map():
    configure_libraries()

    dataframe = pd.DataFrame({"a": [1, 2]})
    out = puw.utils.pandas.add_quantity_column(
        dataframe,
        "distance",
        puw.quantity([1.0, 2.0], "meter"),
        to_unit="centimeter",
    )

    np.testing.assert_allclose(out["distance"].to_numpy(), np.array([100.0, 200.0]))
    assert out.attrs["pyunitwizard_units"]["distance"] == "centimeter"
    assert "distance" not in dataframe.columns


def test_get_quantity_column_uses_metadata_or_explicit_unit():
    configure_libraries()

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {"mass": puw.quantity([1.0, 2.0], "gram")}
    )

    from_metadata = puw.utils.pandas.get_quantity_column(dataframe, "mass")
    explicit = puw.utils.pandas.get_quantity_column(dataframe, "mass", unit_name="kilogram")

    assert puw.get_unit(from_metadata, to_form="string") == "gram"
    np.testing.assert_allclose(puw.get_value(from_metadata), np.array([1.0, 2.0]))
    assert puw.get_unit(explicit, to_form="string") == "kilogram"
    np.testing.assert_allclose(puw.get_value(explicit), np.array([1.0, 2.0]))


def test_get_quantity_column_raises_without_unit_metadata():
    configure_libraries()

    dataframe = pd.DataFrame({"x": [1.0, 2.0]})
    with pytest.raises(ValueError):
        puw.utils.pandas.get_quantity_column(dataframe, "x")


def test_get_quantity_column_invalid_value_type():
    configure_libraries()

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {"x": puw.quantity([1.0, 2.0], "meter")}
    )
    with pytest.raises(ValueError):
        puw.utils.pandas.get_quantity_column(dataframe, "x", value_type="invalid")


def test_setup_pandas_adds_dataframe_accessor():
    configure_libraries()
    puw.utils.pandas.setup_pandas(enable=False)

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {"x": puw.quantity([1.0, 2.0], "meter")}
    )

    puw.utils.pandas.setup_pandas(enable=True)
    q = dataframe.puw.get_quantity("x")
    assert puw.get_unit(q, to_form="string") == "meter"
    np.testing.assert_allclose(puw.get_value(q), np.array([1.0, 2.0]))

    puw.utils.pandas.setup_pandas(enable=False)
    assert not hasattr(pd.DataFrame, "puw")


def test_pandas_context_temporarily_registers_accessor():
    configure_libraries()
    puw.utils.pandas.setup_pandas(enable=False)
    assert not hasattr(pd.DataFrame, "puw")

    dataframe = pd.DataFrame({"a": [1.0, 2.0]})
    with puw.utils.pandas.pandas_context():
        assert hasattr(pd.DataFrame, "puw")
        dataframe.puw.set_quantity("distance", puw.quantity([1.0, 2.0], "meter"), to_unit="centimeter")
        assert dataframe.attrs["pyunitwizard_units"]["distance"] == "centimeter"

    assert not hasattr(pd.DataFrame, "puw")
