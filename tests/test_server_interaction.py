from .get_all_users import GetAllUsers
from .server.schema import schema


def test_local_query_execution():
    query = GetAllUsers.get_query_string()
    result = schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None


def test_pydantic_parse_obj():
    query = GetAllUsers.get_query_string()
    result = schema.execute_sync(query)
    assert type(result.data) is dict
    result = GetAllUsers.parse_obj(result.data)
