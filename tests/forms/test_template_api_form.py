import pytest

from pyunitwizard.forms import template_api_form as template


@pytest.mark.parametrize(
    "fn,args",
    [
        (template.is_quantity, ("x",)),
        (template.is_unit, ("x",)),
        (template.dimensionality, ("x",)),
        (template.compatibility, ("x", "y")),
        (template.make_quantity, (1.0, "meter")),
        (template.string_to_quantity, ("1 meter",)),
        (template.to_string, ("meter",)),
        (template.convert, ("x", "meter")),
        (template.get_value, ("x",)),
        (template.get_unit, ("x",)),
    ],
)
def test_template_api_form_methods_raise_not_implemented(fn, args):
    assert template.form_name == "unyt"
    assert template.parser is False
    assert template.is_form == {}

    with pytest.raises(NotImplementedError):
        fn(*args)
