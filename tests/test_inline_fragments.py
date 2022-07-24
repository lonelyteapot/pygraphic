from pygraphic import GQLQuery, GQLType


def test_query_generation_with_one_inline_fragment():
    class Foo(GQLType):
        i: int

    class Query(GQLQuery):
        fragment: Foo | object

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  fragment {",
            "    ... on Foo {",
            "      i",
            "    }",
            "  }",
            "}",
        )
    )


def test_query_generation_with_two_inline_fragments():
    class Foo(GQLType):
        i: int

    class Bar(GQLType):
        s: float

    class Query(GQLQuery):
        fragment: Foo | Bar

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  fragment {",
            "    ... on Foo {",
            "      i",
            "    }",
            "    ... on Bar {",
            "      s",
            "    }",
            "  }",
            "}",
        )
    )


def test_query_generation_with_two_inline_fragments_in_list():
    class Foo(GQLType):
        i: int

    class Bar(GQLType):
        s: str

    class Query(GQLQuery):
        fragments: list[Foo | Bar]

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  fragments {",
            "    ... on Foo {",
            "      i",
            "    }",
            "    ... on Bar {",
            "      s",
            "    }",
            "  }",
            "}",
        )
    )


def test_query_parsing_with_two_inline_fragments_in_list():
    class Foo(GQLType):
        i: int

    class Bar(GQLType):
        s: str

    class Query(GQLQuery):
        fragments: list[Foo | Bar]

    data = {
        "fragments": [
            {"i": 0},
            {"s": "foo"},
        ]
    }

    result = Query.parse_obj(data)
    assert type(result.fragments[0]) is Foo
    assert type(result.fragments[1]) is Bar
