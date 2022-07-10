from __future__ import annotations

from random import choices, randint, randrange
from string import hexdigits

import strawberry
from faker import Faker
from strawberry import ID


fake = Faker()

fake_id = lambda: "".join(choices(hexdigits, k=16)).lower()  # noqa
fake_name = lambda: fake.name()  # noqa
fake_age = lambda: randint(14, 80)  # noqa
fake_balance = lambda: randint(0, 1000) / 100  # noqa
fake_is_active = lambda: bool(randint(0, 1))  # noqa


@strawberry.type
class User:
    id: ID = strawberry.field(default_factory=fake_id)
    name: str = strawberry.field(default_factory=fake_name)
    age: int = strawberry.field(default_factory=fake_age)
    balance: float = strawberry.field(default_factory=fake_balance)
    is_active: bool = strawberry.field(default_factory=fake_is_active)

    @strawberry.field
    def friends(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


schema = strawberry.Schema(query=Query)
