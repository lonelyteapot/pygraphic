from pathlib import Path

from .get_all_users import GetAllUsers


def test_unnamed_query_generation(golden_dir: Path):
    expected = golden_dir.joinpath("query_unnamed.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string(named=False) == expected


def test_query_generation(golden_dir: Path):
    expected = golden_dir.joinpath("query_get_all_users.gql").read_text("utf-8")
    assert GetAllUsers.get_query_string() == expected
