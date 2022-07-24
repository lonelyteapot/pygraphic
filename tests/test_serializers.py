import pytest


# TODO Rewrite tests for serializers

# from pygraphic.types import class_to_graphql_type, register_graphql_type


@pytest.mark.skip("Code was migrated")
def test_class_to_typename_crashes_on_unknown_class():
    with pytest.raises(TypeError):
        class_to_graphql_type(object, allow_none=True)


@pytest.mark.skip("Code was migrated")
def test_class_to_typename_with_default_scalars():
    assert class_to_graphql_type(int, allow_none=True) == "Int"
    assert class_to_graphql_type(float, allow_none=True) == "Float"
    assert class_to_graphql_type(str, allow_none=True) == "String"
    assert class_to_graphql_type(int, allow_none=True) == "Int"
    # assert class_to_graphql_type(str, allow_none=True) == 'ID'


@pytest.mark.skip("Code was migrated")
def test_class_to_typename_with_non_nullable():
    assert class_to_graphql_type(int, allow_none=False) == "Int!"


@pytest.mark.skip("Code was migrated")
def test_class_to_typename_with_registered_type():
    register_graphql_type("CustomType", object)
    assert class_to_graphql_type(object, allow_none=True) == "CustomType"
