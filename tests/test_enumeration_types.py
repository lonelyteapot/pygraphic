from enum import auto
from typing import Optional

from pydantic import Field

from pygraphic import GQLEnum, GQLQuery, GQLVariables


def test_generation_of_query_with_enum_field():
    class Foo(GQLEnum):
        BAR = auto()

    class Query(GQLQuery):
        baz: Foo

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  baz\n}"


def test_parsing_enum_from_query_field():
    class Foo(GQLEnum):
        BAR = auto()

    class Query(GQLQuery):
        baz: Foo

    data = {
        "baz": "BAR",
    }
    result = Query.parse_obj(data)
    assert result.baz == Foo.BAR


def test_passing_enum_as_field_argument():
    class Foo(GQLEnum):
        BAR = auto()

    class Query(GQLQuery):
        i: int = Field(ia=Foo.BAR)

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  i(ia: BAR)\n}"


def test_passing_enum_as_query_variable():
    class Foo(GQLEnum):
        BAR = auto()

    class Variables(GQLVariables):
        baz: Foo

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($baz: Foo!) {\n}"


def test_passing_enum_as_default_query_variable():
    class Foo(GQLEnum):
        BAR = auto()

    class Variables(GQLVariables):
        baz: Optional[Foo] = Field(default=Foo.BAR)

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($baz: Foo = BAR) {\n}"
