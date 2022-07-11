from pathlib import Path

from examples.server import server_schema


if __name__ == "__main__":
    Path("golden_files", "server_schema.gql").write_text(
        server_schema.as_str(), encoding="utf-8"
    )
