from enum import Enum, auto
from typing import Optional

import pytest
from pydantic import Field

from pygraphic import GQLQuery, GQLVariables


def test_generation_of_query_with_enum_field():
    class Foo(Enum):
        BAR = auto()

    class Query(GQLQuery):
        baz: Foo

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  baz\n}"


@pytest.mark.skip("Parsing enum from query field not yet implemented")
def test_parsing_enum_from_query_field():
    class Foo(Enum):
        BAR = auto()

    class Query(GQLQuery):
        baz: Foo

    data = {
        "baz": "BAR",
    }
    result = Query.parse_obj(data)

    assert result.baz == Foo.BAR


def test_passing_enum_as_field_argument():
    class Foo(Enum):
        BAR = auto()

    class Query(GQLQuery):
        i: int = Field(ia=Foo.BAR)

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  i(ia: BAR)\n}"


@pytest.mark.skip("Passing enum as query variable not yet implemented")
def test_passing_enum_as_query_variable():
    class Foo(Enum):
        BAR = auto()

    class Variables(GQLVariables):
        baz: Foo

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($baz: Foo) {\n}"


@pytest.mark.skip("Passing enum as query variable not yet implemented")
def test_passing_enum_as_default_query_variable():
    class Foo(Enum):
        BAR = auto()

    class Variables(GQLVariables):
        baz: Optional[Foo] = Field(default=Foo.BAR)

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($baz: Foo = BAR) {\n}"
