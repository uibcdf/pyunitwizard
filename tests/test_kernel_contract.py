import pyunitwizard.kernel as kernel


def test_fundamental_dimension_order_is_locked():
    assert kernel.order_fundamental_units == ["[L]", "[M]", "[T]", "[K]", "[mol]", "[A]", "[Cd]"]
