from pathlib import Path

from examples.server.schema import schema


if __name__ == "__main__":
    Path("golden_files", "server_schema.gql").write_text(
        schema.as_str(), encoding="utf-8"
    )
