from pygraphic import GQLQuery, GQLType


def test_creation_of_query_with_scalar_fields():
    class Query(GQLQuery):
        i: int
        f: float
        s: str
        b: bool

    Query(i=0, f=0.0, s="", b=False)


def test_generation_of_query_with_scalar_fields():
    class Query(GQLQuery):
        i: int
        f: float
        s: str
        b: bool

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  i\n  f\n  s\n  b\n}"


def test_creation_of_query_with_custom_field_type():
    class Foo(GQLType):
        i: int
        f: float
        s: str
        b: bool

    class Query(GQLQuery):
        foo: Foo

    Query(foo=Foo(i=0, f=0.0, s="", b=False))


def test_generation_of_query_with_custom_field_type():
    class Foo(GQLType):
        i: int
        f: float
        s: str
        b: bool

    class Query(GQLQuery):
        foo: Foo

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  foo {\n    i\n    f\n    s\n    b\n  }\n}"


def test_creation_of_query_with_custom_nested_field_types():
    class Bar(GQLType):
        f: float

    class Foo(GQLType):
        i: int
        bar: Bar

    class Query(GQLQuery):
        foo: Foo

    Query(foo=Foo(i=0, bar=Bar(f=0.0)))


def test_generation_of_query_with_custom_nested_field_types():
    class Bar(GQLType):
        f: float

    class Foo(GQLType):
        i: int
        bar: Bar

    class Query(GQLQuery):
        foo: Foo

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  foo {",
            "    i",
            "    bar {",
            "      f",
            "    }",
            "  }",
            "}",
        )
    )
