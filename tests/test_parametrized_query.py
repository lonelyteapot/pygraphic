from pathlib import Path

from examples.parametrized_query.get_users_born_after import GetUsersBornAfter
from examples.server import server_schema


def test_query_string_generation():
    expected = Path("golden_files", "query_parametrized.gql").read_text("utf-8")
    assert GetUsersBornAfter.get_query_string() == expected


def test_local_query_execution():
    query = GetUsersBornAfter.get_query_string()
    # variables = GetAllUsers.variables()
    result = server_schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None


def test_pydantic_object_parsing():
    query = GetUsersBornAfter.get_query_string()
    result = server_schema.execute_sync(query)
    assert type(result.data) is dict
    result = GetUsersBornAfter.parse_obj(result.data)


def test_example():
    from examples.parametrized_query.main import born_after, result

    assert type(result) is GetUsersBornAfter
    assert all(user.birthday > born_after for user in result.users)
    assert all(all(friend.isOnline for friend in user.friends) for user in result.users)
