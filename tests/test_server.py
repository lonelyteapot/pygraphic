from pathlib import Path

from examples.server import server_schema


def test_schema_matches_golden():
    expected = Path("golden_files", "server_schema.gql").read_text("utf-8")
    assert server_schema.as_str() == expected
