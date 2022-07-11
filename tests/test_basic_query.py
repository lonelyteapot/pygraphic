from pathlib import Path

from examples.basic_query.get_all_users import GetAllUsers
from examples.server.schema import schema


def test_unnamed_query_generation():
    expected = Path("golden_files", "query_unnamed.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string(named=False) == expected


def test_query_generation():
    expected = Path("golden_files", "query_get_all_users.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string() == expected


def test_local_query_execution():
    query = GetAllUsers.get_query_string()
    result = schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None


def test_pydantic_object_parsing():
    query = GetAllUsers.get_query_string()
    result = schema.execute_sync(query)
    assert type(result.data) is dict
    result = GetAllUsers.parse_obj(result.data)
