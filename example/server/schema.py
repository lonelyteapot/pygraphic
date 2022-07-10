from __future__ import annotations

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
