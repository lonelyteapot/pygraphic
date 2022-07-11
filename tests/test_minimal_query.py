from pathlib import Path

from examples.minimal_query.get_all_users import GetAllUsers
from examples.server import server_schema


def test_query_string_generation():
    expected = Path("golden_files", "query_minimal.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string(named=False) == expected


def test_local_query_execution():
    query = GetAllUsers.get_query_string()
    result = server_schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None


def test_pydantic_object_parsing():
    query = GetAllUsers.get_query_string()
    result = server_schema.execute_sync(query)
    assert type(result.data) is dict
    result = GetAllUsers.parse_obj(result.data)


def test_example():
    from examples.minimal_query.main import result

    assert type(result) is GetAllUsers
    assert len(result.users) > 0
