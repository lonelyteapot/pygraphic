from pygraphic import GQLQuery


def test_creation_of_empty_query():
    class Query(GQLQuery):
        pass

    Query()


def test_generation_of_empty_unnamed_query():
    class Query(GQLQuery):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n}"
