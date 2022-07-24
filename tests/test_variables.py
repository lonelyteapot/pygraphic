from typing import Optional

from pydantic import Field

from pygraphic import GQLQuery, GQLVariables


def test_creation_of_empty_variables():
    class Variables(GQLVariables):
        pass

    Variables()


def test_creation_of_empty_query_with_empty_variables():
    class Variables(GQLVariables):
        pass

    class Query(GQLQuery, variables=Variables):
        pass

    Query()


def test_creation_of_variables():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    Variables(i=0, f=0.0, s="foo", b=None)


def test_generation_of_variables():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    variables = Variables(i=0, f=0.0, s="foo", b=None)
    json_ = variables.json()
    assert json_ == '{"i": 0, "f": 0.0, "s": "foo", "b": null}'
    dict_ = variables.dict()
    assert dict_ == {"i": 0, "f": 0.0, "s": "foo", "b": None}


def test_creation_of_query_with_variables():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    class Query(GQLQuery, variables=Variables):
        pass

    Query()


def test_generation_of_unnamed_query_with_empty_variables():
    class Variables(GQLVariables):
        pass

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n}"


def test_generation_of_named_query_with_empty_variables():
    class Variables(GQLVariables):
        pass

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string()
    assert gql == "query Query {\n}"


def test_generation_of_unnamed_query_with_variables():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($i: Int!, $f: Float!, $s: String, $b: Boolean) {\n}"


def test_generation_of_named_query_with_variables():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string()
    assert gql == "query Query($i: Int!, $f: Float!, $s: String, $b: Boolean) {\n}"


def test_generation_of_query_with_default_variables():
    class Variables(GQLVariables):
        i: int = Field(default=0)
        f: float = Field(default=0.0)
        s: Optional[str] = Field(default="foo")
        b: Optional[bool] = Field(default=None)

    class Query(GQLQuery, variables=Variables):
        pass

    # Notice that non-nullable variables cannot have default values in GraphQL.
    gql = Query.get_query_string(include_name=False)
    assert gql == (
        'query($i: Int!, $f: Float!, $s: String = "foo", $b: Boolean = null) {\n}'
    )


def test_generation_of_variables_excludes_defaults():
    class Variables(GQLVariables):
        i: int = Field(default=0)
        f: float = Field(default=0.0)
        s: Optional[str] = Field(default="foo")
        b: Optional[bool] = Field(default=None)

    variables = Variables(b=None)
    json_ = variables.json()
    assert json_ == '{"i": 0, "f": 0.0, "b": null}'
    dict_ = variables.dict()
    assert dict_ == {"i": 0, "f": 0.0, "b": None}


def test_generation_of_variables_without_excluding_defaults():
    class Variables(GQLVariables):
        i: int = Field(default=0)
        f: float = Field(default=0.0)
        s: Optional[str] = Field(default="foo")
        b: Optional[bool] = Field(default=None)

    variables = Variables(b=None)
    json_ = variables.json(exclude_defaults=False)
    assert json_ == '{"i": 0, "f": 0.0, "s": "foo", "b": null}'
    dict_ = variables.dict(exclude_defaults=False)
    assert dict_ == {"i": 0, "f": 0.0, "s": "foo", "b": None}


def test_passing_variables_as_field_arguments():
    class Variables(GQLVariables):
        i: int
        f: float
        s: Optional[str]
        b: Optional[bool]

    class Query(GQLQuery, variables=Variables):
        ii: int = Field(ia=Variables.i)
        ff: float = Field(fa=Variables.f)
        ss: str = Field(sa=Variables.s)
        bb: bool = Field(ba=Variables.b)

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query($i: Int!, $f: Float!, $s: String, $b: Boolean) {",
            "  ii(ia: $i)",
            "  ff(fa: $f)",
            "  ss(sa: $s)",
            "  bb(ba: $b)",
            "}",
        )
    )
