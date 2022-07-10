from pathlib import Path

from example.get_all_users import GetAllUsers


def test_unnamed_query_generation():
    expected = Path("golden_files", "query_unnamed.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string(named=False) == expected


def test_basic_query_generation():
    expected = Path("golden_files", "query_get_all_users.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string() == expected
