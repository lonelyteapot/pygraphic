from pathlib import Path

from .schema import schema


def test_schema_matches_expected(script_directory: Path):
    expected = script_directory.joinpath("expected_server_schema.gql").read_text(
        encoding="utf-8"
    )
    assert schema.as_str() == expected
