from .get_all_users import GetAllUsers
from .server.schema import schema


def test_successful_query_execution():
    query = GetAllUsers.get_query_string()
    result = schema.execute_sync(query)
    assert result.errors is None
