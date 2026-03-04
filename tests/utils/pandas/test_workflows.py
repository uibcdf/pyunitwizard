import numpy as np
import pyunitwizard as puw
import pytest


pd = pytest.importorskip("pandas")


def configure_libraries():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])


def test_concat_preserves_and_merges_units_map():
    configure_libraries()

    left = puw.utils.pandas.dataframe_from_quantities(
        {"length": puw.quantity([1.0], "nanometer")}
    )
    right = puw.utils.pandas.dataframe_from_quantities(
        {"length": puw.quantity([2.0], "nanometer")}
    )

    out = puw.utils.pandas.concat([left, right], ignore_index=True)

    np.testing.assert_allclose(out["length"].to_numpy(), np.array([1.0, 2.0]))
    assert out.attrs["pyunitwizard_units"]["length"] == "nanometer"


def test_concat_raises_on_units_metadata_conflict():
    configure_libraries()

    left = puw.utils.pandas.dataframe_from_quantities(
        {"length": puw.quantity([1.0], "nanometer")}
    )
    right = puw.utils.pandas.dataframe_from_quantities(
        {"length": puw.quantity([2.0], "meter")}
    )

    with pytest.raises(ValueError):
        puw.utils.pandas.concat([left, right], ignore_index=True)


def test_merge_preserves_units_map_for_output_columns():
    configure_libraries()

    left = puw.utils.pandas.dataframe_from_quantities(
        {
            "id": puw.quantity([1, 2], "dimensionless"),
            "length": puw.quantity([1.0, 2.0], "nanometer"),
        }
    )
    right = puw.utils.pandas.dataframe_from_quantities(
        {
            "id": puw.quantity([1, 2], "dimensionless"),
            "time": puw.quantity([10.0, 20.0], "picosecond"),
        }
    )

    out = puw.utils.pandas.merge(left, right, on="id")

    assert out.attrs["pyunitwizard_units"]["id"] == "dimensionless"
    assert out.attrs["pyunitwizard_units"]["length"] == "nanometer"
    assert out.attrs["pyunitwizard_units"]["time"] == "picosecond"


def test_assign_and_copy_can_be_resynced():
    configure_libraries()

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {"length": puw.quantity([1.0, 2.0], "nanometer")}
    )
    assigned = dataframe.assign(raw=[5.0, 6.0])
    copied = assigned.copy()

    # sync trims stale metadata and keeps only columns currently present.
    synced = puw.utils.pandas.sync_units_map(copied, inplace=False)
    assert synced.attrs["pyunitwizard_units"]["length"] == "nanometer"
    assert "raw" not in synced.attrs["pyunitwizard_units"]


def test_set_units_map_allows_recovery_after_attrs_loss():
    configure_libraries()

    dataframe = puw.utils.pandas.dataframe_from_quantities(
        {"energy": puw.quantity([1.0, 2.0], "kilocalorie")}
    )
    dataframe.attrs.clear()
    assert puw.utils.pandas.get_units_map(dataframe) == {}

    restored = puw.utils.pandas.set_units_map(
        dataframe,
        {"energy": "kilocalorie"},
        inplace=False,
    )
    q = puw.utils.pandas.get_quantity_column(restored, "energy")
    assert puw.get_unit(q, to_form="string") == "kilocalorie"
