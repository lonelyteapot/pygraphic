from pygraphic import GQLQuery


def test_generation_of_empty_named_query():
    class Query(GQLQuery):
        pass

    gql = Query.get_query_string()
    assert gql == "query Query {\n}"


def test_generation_of_named_query_with_scalar_fields():
    class Query(GQLQuery):
        i: int
        f: float
        s: str
        b: bool

    gql = Query.get_query_string()
    assert gql == "query Query {\n  i\n  f\n  s\n  b\n}"
