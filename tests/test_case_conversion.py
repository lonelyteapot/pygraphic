from pydantic import Field

from pygraphic import GQLQuery, GQLVariables


def test_field_name_conversion():
    class Query(GQLQuery):
        snake_case: bool

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  snakeCase\n}"


def test_field_argument_conversion():
    class Query(GQLQuery):
        i: int = Field(snake_case=False)

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  i(snakeCase: false)\n}"


def test_query_generation_variable_conversion():
    class Variables(GQLVariables):
        snake_case: bool

    class Query(GQLQuery, variables=Variables):
        pass

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($snakeCase: Boolean!) {\n}"


def test_variable_generation_conversion():
    class Variables(GQLVariables):
        snake_case: bool

    variables = Variables(snake_case=False)
    json = variables.json()
    assert json == '{"snakeCase": false}'


def test_passing_variable_in_field_argument_conversion():
    class Variables(GQLVariables):
        snake_case: bool

    class Query(GQLQuery, variables=Variables):
        i: int = Field(camel_case=Variables.snake_case)

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($snakeCase: Boolean!) {\n  i(camelCase: $snakeCase)\n}"
