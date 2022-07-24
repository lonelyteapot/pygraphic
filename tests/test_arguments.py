from pydantic import Field

from pygraphic import GQLQuery


def test_creation_of_query_with_field_arguments():
    class Query(GQLQuery):
        i: int = Field(ia=0)
        f: float = Field(fa=0.0)
        s: str = Field(sa="")
        b: bool = Field(ba=False)

    Query(i=0, f=0.0, s="", b=False)


def test_generation_of_query_with_one_field_argument():
    class Query(GQLQuery):
        i: int = Field(ia=0)
        f: float = Field(fa=0.0)
        s: str = Field(sa="foo")
        b: bool = Field(ba=False)

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  i(ia: 0)",
            "  f(fa: 0.0)",
            '  s(sa: "foo")',
            "  b(ba: false)",
            "}",
        )
    )


def test_generation_of_query_with_two_field_arguments():
    class Query(GQLQuery):
        i: int = Field(ia=0, ib=1)
        f: float = Field(fa=0.0, fb=1.1)
        s: str = Field(sa="foo", sb="bar")
        b: bool = Field(ba=False, bb=True)

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            "  i(ia: 0, ib: 1)",
            "  f(fa: 0.0, fb: 1.1)",
            '  s(sa: "foo", sb: "bar")',
            "  b(ba: false, bb: true)",
            "}",
        )
    )
