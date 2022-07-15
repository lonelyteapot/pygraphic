import json
from pathlib import Path

from examples.required_parametrized_query.get_user import GetUser, Parameters
from examples.server import server_schema


def test_query_string_generation():
    expected = Path("golden_files", "query_parametrized_required.gql").read_text(
        "utf-8"
    )
    assert GetUser.get_query_string() == expected


def test_local_query_execution():
    query = GetUser.get_query_string()
    variables = Parameters(user_id=1)
    result = server_schema.execute_sync(query, json.loads(variables.json()))
    assert result.errors is None
    assert result.data is not None


def test_pydantic_object_parsing():
    query = GetUser.get_query_string()
    variables = Parameters(user_id=1)
    result = server_schema.execute_sync(query, json.loads(variables.json()))
    assert type(result.data) is dict
    result = GetUser.parse_obj(result.data)


def test_example():
    from examples.required_parametrized_query.main import result

    assert type(result) is GetUser
    assert result.user.id == 1
