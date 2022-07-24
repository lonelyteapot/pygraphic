from enum import Enum, auto

import pytest

from pygraphic import GQLVariables
from pygraphic.serializers import (
    class_to_graphql,
    register_graphql_type,
    value_to_graphql,
)


def test_basic_scalars_to_graphql():
    assert value_to_graphql(0) == "0"
    assert value_to_graphql(0.0) == "0.0"
    assert value_to_graphql("foo") == '"foo"'
    assert value_to_graphql(False) == "false"
    assert value_to_graphql(True) == "true"
    assert value_to_graphql(None) == "null"


def test_enum_to_graphql():
    class Foo(Enum):
        BAR = auto()

    assert value_to_graphql(Foo.BAR) == "BAR"


def test_variable_name_to_graphql():
    class Variables(GQLVariables):
        foo: int

    assert value_to_graphql(Variables.foo) == "$foo"


def test_basic_nullable_scalar_types_to_graphql():
    assert class_to_graphql(int, allow_none=True) == "Int"
    assert class_to_graphql(float, allow_none=True) == "Float"
    assert class_to_graphql(str, allow_none=True) == "String"
    assert class_to_graphql(bool, allow_none=True) == "Boolean"


def test_basic_non_nullable_scalar_types_to_graphql():
    assert class_to_graphql(int, allow_none=False) == "Int!"
    assert class_to_graphql(float, allow_none=False) == "Float!"
    assert class_to_graphql(str, allow_none=False) == "String!"
    assert class_to_graphql(bool, allow_none=False) == "Boolean!"


def test_fail_of_unkown_type_to_graphql():
    with pytest.raises(TypeError):
        class_to_graphql(object, allow_none=True)
    with pytest.raises(TypeError):
        class_to_graphql(object, allow_none=False)


def test_custom_registered_type_to_graphql():
    register_graphql_type("Object", object)
    assert class_to_graphql(object, allow_none=True) == "Object"
    assert class_to_graphql(object, allow_none=False) == "Object!"
