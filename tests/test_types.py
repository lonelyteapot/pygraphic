import pytest

from pygraphic.types import class_to_graphql_type, register_graphql_type


def test_class_to_typename_crashes_on_unknown_class():
    with pytest.raises(KeyError) as e_info:
        class_to_graphql_type(object)


def test_class_to_typename_with_default_scalars():
    assert class_to_graphql_type(int) == "Int"
    assert class_to_graphql_type(float) == "Float"
    assert class_to_graphql_type(str) == "String"
    assert class_to_graphql_type(int) == "Int"
    # assert class_to_graphql_type(str) == 'ID'


def test_class_to_typename_with_registered_type():
    register_graphql_type("CustomType", object)
    assert class_to_graphql_type(object) == "CustomType"
