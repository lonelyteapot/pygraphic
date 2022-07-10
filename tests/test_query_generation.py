from pathlib import Path

from .get_all_users import GetAllUsers


def test_query_generation(script_directory: Path):
    with open(script_directory / "expected_query.gql", encoding="utf-8") as fp:
        expected_query = fp.read()
    query_string = GetAllUsers.get_query_string()
    assert query_string == expected_query
