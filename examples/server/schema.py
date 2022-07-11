from __future__ import annotations

from datetime import datetime, timedelta
from random import randint, randrange
from uuid import UUID, uuid4

import strawberry
from faker import Faker


fake = Faker()

fake_name = lambda: fake.name()  # noqa
fake_age = lambda: randint(14, 80)  # noqa
fake_balance = lambda: randint(0, 1000) / 100  # noqa
fake_is_active = lambda: bool(randint(0, 1))  # noqa
fake_last_seen = lambda: datetime.now() - timedelta(minutes=randint(1, 200))  # noqa


@strawberry.type
class User:
    id: UUID = strawberry.field(default_factory=uuid4)
    name: str = strawberry.field(default_factory=fake_name)
    age: int = strawberry.field(default_factory=fake_age)
    balance: float = strawberry.field(default_factory=fake_balance)
    is_active: bool = strawberry.field(default_factory=fake_is_active)
    last_seen: datetime = strawberry.field(default_factory=fake_last_seen)

    @strawberry.field
    def friends(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User() for _ in range(randrange(5, 10))]


schema = strawberry.Schema(query=Query)
