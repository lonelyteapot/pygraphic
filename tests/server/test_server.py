from pathlib import Path

from .schema import schema


def test_schema_matches_golden(golden_dir: Path):
    expected = golden_dir.joinpath("server_schema.gql").read_text("utf-8")
    assert schema.as_str() == expected
