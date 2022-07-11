from pathlib import Path

from examples.server.schema import schema


def test_schema_matches_golden():
    expected = Path("golden_files", "server_schema.gql").read_text("utf-8")
    assert schema.as_str() == expected
