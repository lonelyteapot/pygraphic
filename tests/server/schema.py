from __future__ import annotations

from pathlib import Path
from random import randrange
from uuid import UUID, uuid4

import strawberry
from faker import Faker


fake = Faker()


@strawberry.type
class User:
    id: UUID = strawberry.field(default_factory=uuid4)
    name: str = strawberry.field(default_factory=fake.name)

    @strawberry.field
    def friends(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


schema = strawberry.Schema(query=Query)


def generate_schema_file(directory: Path):
    directory.joinpath("expected_server_schema.gql").write_text(
        schema.as_str(), encoding="utf-8"
    )


if __name__ == "__main__":
    generate_schema_file(Path(__file__).parent)
